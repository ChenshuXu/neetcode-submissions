# Dasher Pay — Base 与 Follow-up 要求

这是一套 DoorDash Code Craft 风格的渐进练习，不是已确认的原题全文。
公开面经支持直接按配送时长计算 payout、使用 mocked upstream，以及继续讨论
timeline 和 upstream failure；精确费率、数据模型和 Follow-up 顺序是本地训练契约。
真实面试题与本文不同时，以 interviewer 给出的 contract 为准。

目录中的 Python 文件按下面的顺序累积需求，但每个文件都可以独立运行：

```text
Base
  -> Follow-up 1: Peak Pay
  -> Follow-up 2: Event Timeline
  -> Follow-up 3: Cancellation Pay
  -> Follow-up 4: Timeout Retry
  -> Follow-up 5: Idempotent Payout Issuance
  -> Follow-up 6: Ordered Event Stream
```

## 统一训练契约

- 时间使用整数分钟，区间是 half-open `[start, end)`。
- 金额使用 integer cents；基础费率是每个 active delivery-minute `30` cents。
- 同时进行的 delivery 各自计费，重叠时长不会合并或去重。
- 所有 upstream client 都通过 constructor 注入。
- 每个 Follow-up 保留前一阶段的行为，只增加本阶段明确要求的变化。

---

## Base — 按已完成配送的时长计算收入

文件：`dasher_pay.py`

实现：

```python
PayoutService.get_payout(dasher_id) -> PayoutResponse
```

### 输入

`DeliveryClient.list_deliveries(dasher_id)` 返回该 dasher 的 delivery records。
每条记录包含：

- `delivery_id`
- `accepted_at`
- `completed_at`
- `status`: `COMPLETED`、`CANCELLED` 或 `ACTIVE`

### 要求

1. `dasher_id` 必须是非空、非纯空格字符串；无效输入要在调用 client 前拒绝。
2. 只计算 `COMPLETED` delivery；`ACTIVE` 和 `CANCELLED` 不计费。
3. 已完成 delivery 必须有 `completed_at`，并且
   `completed_at > accepted_at`；否则报 invalid-delivery error。
4. 每条已完成 delivery 的金额是：

   ```text
   (completed_at - accepted_at) * 30 cents
   ```

5. 每条 delivery 的时长独立加入总额。两个 delivery 即使重叠，也都完整计费。
6. 返回 `amount_cents` 和 `completed_delivery_count`。
7. 没有已完成 delivery 时，金额和数量都返回 `0`。
8. `DeliveryClientError` 要映射成稳定的 `PayoutUnavailableError`，并保留原错误为 cause。

---

## Follow-up 1 — Peak Pay

文件：`follow_up_1_peak_pay.py`

在 Base 上增加 `peak_windows`：

1. 每个 peak window 也是 half-open `[start, end)`，且必须有正时长。
2. delivery 在任意 peak window 内的 active minutes 按 `2x` 计费；其余时段仍按基础费率计费。
3. 相邻或重叠的 peak windows 不叠加倍率；同一分钟最高只按 `2x` 计费。
4. window 与 delivery 只在边界接触时，没有 overlap pay。
5. Base 的 status filtering、invalid interval、overlapping-delivery 和 upstream-error 行为保持不变。

---

## Follow-up 2 — Event Timeline

文件：`follow_up_2_event_timeline.py`

upstream 不再返回完整 delivery rows，而是返回无序事件：

```text
(order_id, time, action)
```

`action` 可以是 `PICKED_UP`、`DELIVERED` 或 `CANCELLED`。

要求：

1. `PICKED_UP` 打开一个 activity interval；`DELIVERED` 或 `CANCELLED` 关闭它。
2. 输入可以是无序的；相同内容的 exact duplicate event 只处理一次。
3. 只有以 `DELIVERED` 结束的 interval 计费；`CANCELLED` 目前只负责关闭 interval。
4. 已完成 interval 继续沿用 Follow-up 1 的基础费率与 peak pay 规则。
5. 以下 timeline 必须拒绝：
   - 同一 order 重复 pickup；
   - 没有 pickup 的 terminal event；
   - 同一 order 出现非 exact duplicate 的第二个 terminal event；
   - terminal time 不晚于 pickup time；
   - finalize 时仍有未关闭的 pickup。

---

## Follow-up 3 — Cancellation Pay

文件：`follow_up_3_cancellation.py`

在 Follow-up 2 上增加明确的 cancellation policy。三种 mode 互斥，不能静默组合：

1. `IGNORE_CANCELLATION`
   - cancelled interval 不计费。
2. `FIXED_CANCELLATION`
   - active duration 至少 5 分钟时支付固定 `200` cents；
   - 不足 5 分钟不支付；
   - 固定金额不乘 peak multiplier。
3. `DURATION_CANCELLATION`
   - cancelled interval 按普通时长计费；
   - peak overlap 继续按 `2x` 计费。

返回值增加 `paid_cancellation_count`。未知 mode 必须拒绝。真实面试中如果题目只给出
一种 cancellation rule，只实现那一种。

---

## Follow-up 4 — Slow or Unavailable Upstream

文件：`follow_up_4_retry.py`

为 event client 增加 bounded retry：

1. 只重试明确的 `EventClientTimeoutError`；其他错误不重试。
2. 总尝试次数必须有上限。
3. retry delay 使用 exponential backoff。
4. 所有 attempts 和 delays 共用一个 total deadline；如果下一次 delay 已无法放进 deadline，就立即停止。
5. 一次成功调用如果已经超过 total deadline，也不能当作成功返回。
6. retry 用尽后，`PayoutService` 仍向 caller 返回稳定的 `PayoutUnavailableError`。

本地代码只负责 retry policy。真实网络 client 还必须为每次请求设置 per-attempt timeout；
jitter、metrics 和 circuit breaker 不属于这道 coding follow-up 的必写代码。

---

## Follow-up 5 — Actually Issue the Payout

文件：`follow_up_5_issue_payout.py`

从“只计算金额”扩展为调用 payment gateway 发放金额：

```python
IdempotentPayoutIssuer.issue(dasher_id, payout_period, amount_cents)
```

要求：

1. 使用 `(dasher_id, payout_period)` 作为稳定 idempotency key。
2. 第一次请求调用 payment gateway，并保存完整 `IssuedPayout` 结果。
3. 相同 key、相同金额的 retry 返回已保存结果，不能再次调用 gateway。
4. 相同 key、不同金额必须报 idempotency conflict。
5. 并发的相同请求也只能发放一次。
6. empty `dasher_id`、empty `payout_period` 或负金额必须拒绝。

本地 dictionary 和 process-local lock 只是练习模型。生产环境需要 durable unique key、
provider idempotency 和 outbox 才能跨进程与重启保持这个 contract。

---

## Follow-up 6 — Large Ordered Event Stream

文件：`follow_up_6_streaming.py`

event history 不再一次性加载；事件按时间顺序逐条到达，并新增稳定的 `event_id`。

要求：

1. 每收到一个 event 就增量更新 payout，不加载或排序完整 batch。
2. 保存 open orders、closed orders、seen event IDs、累计金额、计数和最后处理时间。
3. 相同 `event_id` + 相同内容的 replay 直接忽略，不能重复计费。
4. 相同 `event_id` + 不同内容必须拒绝。
5. `event.at` 早于最后处理时间时必须作为 late event 拒绝；相同时间不触发 late-event
   error，但仍必须通过下面的 pairing 和 positive-interval 检查。
6. pickup/terminal pairing、positive interval、cancellation mode 和 peak pay 继续遵守前面阶段的规则。
7. `finalize()` 时如果仍有 open order，必须拒绝；否则返回累计的 `PayoutResponse`。
8. 同一组 chronological events 的 streaming 结果应与 batch calculation 一致。

如果真实输入允许 out-of-order events，必须先确认 allowed lateness、watermark、buffer、
finalized payout 的 correction 规则，以及如何按 `dasher_id` partition；本练习不自行假设这些规则。
