# Validate Cart — Base 与 Follow-up 说明

这是一套 DoorDash Code Craft 风格的渐进练习，不是已确认的原题全文。
公开信息只稳定支持“数量、库存、最小/最大购买限制”这些方向；重复商品、
错误顺序、整单限制、预占接口和状态机是这套练习固定下来的训练契约。

目录中只保留这一份说明文档。代码按下面的顺序逐步演进：

```text
Base
  -> Follow-up 1: 合并重复商品
  -> Follow-up 2: 整单数量限制
  -> Follow-up 3: 原子预占库存
  -> Follow-up 4: request_id 幂等
  -> Follow-up 5: confirm / release / expire
  -> Follow-up 6: stale snapshot 与并发最后一件
```

每个 Python 文件都是 standalone：不 import Base，也不 import 前一个
Follow-up。后面的文件会重复前面的代码，是为了可以单独打开和运行。真实面试中，
应在当前代码上只写该 Follow-up 的增量。

## 运行方式

先运行 Base，再按编号运行 Follow-up：

```bash
cd "/Users/Newton/Documents/job search/neetcode-submissions/custom_practice/doordash_codecraft/kata_03_validate_cart"
python3 validate_cart.py
for file in follow_up_*.py; do python3 "$file" || exit 1; done
```

每个文件末尾只有一个 `main()` 和少量 `assert` smoke check，没有 unit-test
harness。

## 面试开始先确认

这些问题会直接改变代码，不要默默假设：

1. 重复 `item_id` 是报错、合并数量，还是 last-write-wins？
2. min/max 是每个商品的限制，还是整个购物车的限制？边界是否 inclusive？
3. 返回第一个错误，还是返回所有可修复错误？错误顺序是否需要稳定？
4. 这里只验证 snapshot，还是必须真正预占库存？
5. 如果要预占，幂等键是什么？是否有 confirm、cancel 和 expiration？

---

## Base — 只验证，不修改库存

文件：`validate_cart.py`

### 要做什么

实现：

```python
CartValidator.validate_cart(lines, inventory) -> CartValidationResult
```

- `lines` 是购物车商品行：`item_id` 和 `quantity`。
- `inventory` 是一次只读库存 snapshot，以 `item_id` 为 key。
- 返回所有 validation errors；没有错误时 `is_valid` 为 `True`。
- 不修改 `lines` 或 `inventory`，也不承诺库存会一直可用。

### 固定规则

1. 空购物车返回一个 `EMPTY_CART`。
2. `quantity` 必须是 exact positive `int`；`bool`、float、0 和负数无效。
3. Base 不合并重复商品。同一 `item_id` 出现多次时，只返回一个
   `DUPLICATE_ITEM`，并跳过该商品的其他检查。
4. 商品不在库存 snapshot 中时返回 `ITEM_UNAVAILABLE`。
5. `min_quantity` 和 `max_quantity` 都是 inclusive。
6. 请求数量超过 `available_quantity` 时返回
   `INSUFFICIENT_INVENTORY`。
7. 返回全部错误，保持 first-seen item order。一个商品内部的规则顺序是：
   `BELOW_MINIMUM`、`ABOVE_MAXIMUM`、`INSUFFICIENT_INVENTORY`。

### 实现思路

先扫描一次，统计每个 `item_id` 的出现次数；再按原顺序扫描，只处理每个商品的
第一次出现。这样在验证第一行时，就已经知道它是否属于重复商品。

Invariant：处理完一个 first-seen item 后，`errors` 已包含所有已处理商品的全部
适用错误，并且顺序稳定。

复杂度：`O(n)` time，`O(u + e)` extra space；`u` 是 unique item 数量，
`e` 是返回的错误数量。

### 完成标准

- 空购物车、正常购物车、invalid quantity、duplicate、missing item 均正确。
- min/max 和 available inventory 可以同时产生多个错误。
- 输入未被修改，错误顺序稳定。

---

## Follow-up 1 — 重复商品改为合并

文件：`follow_up_1_merge_duplicates.py`

### 新需求

Interviewer 改变重复商品契约：重复 `item_id` 不再报错，而是先把数量相加，
再运行 Base 的商品规则。

### 相对 Base 要改什么

- 删除 `DUPLICATE_ITEM` 路径和重复计数逻辑。
- 新增 `merge_duplicate_lines(lines)`。
- 合并前先确认每一行都是 positive exact `int`，否则抛出 `ValueError`；
  不要用无效数量参与求和。
- 使用普通 `dict` 累加。Python `dict` 保持插入顺序，因此结果保持
  first-seen item order。
- 调用顺序是：先 `merge_duplicate_lines`，再 `validate_cart`。

### 例子与完成标准

```text
输入:  apple x1, soup x2, apple x3
合并:  apple x4, soup x2
```

合并后每个商品只验证一次。复杂度仍为 `O(n)` time 和 `O(u)` merge space。

---

## Follow-up 2 — 增加整单数量限制

文件：`follow_up_2_restaurant_totals.py`

### 新需求

除了每个商品自己的 min/max，restaurant 还要求整个购物车的商品总数落在：

```text
[min_cart_quantity, max_cart_quantity]
```

### 相对 Follow-up 1 要改什么

- `validate_cart` 增加 `min_cart_quantity` 和 `max_cart_quantity` 参数。
- 新增 `BELOW_CART_MINIMUM`、`ABOVE_CART_MAXIMUM`。
- 遍历商品时累计所有 positive integer quantity。
- 先完成 item-level errors，再把 cart-level errors 追加到结果末尾，保证顺序稳定。

当前训练契约中，quantity 合法但库存中不存在的商品仍计入 cart total；invalid
quantity 不计入。真实面试必须确认这一点。

复杂度仍为 `O(n)` time；不需要第二套复杂的数据结构。

---

## Follow-up 3 — 原子预占库存

文件：`follow_up_3_atomic_reservation.py`

### 新需求

只做 snapshot validation 不能防止 oversell。验证通过后，必须真正预占库存：

```text
所有商品都有库存 -> 一次性扣减全部商品，返回 held
任意商品库存不足 -> 一个都不扣，返回 rejected
```

### 相对 Follow-up 2 要改什么

- 新增 `ReservationResult` 和 `CartResponse`。
- 新增 `InventoryGateway.snapshot()` 和 `InventoryGateway.reserve()`。
- 新增 `CartService.reserve_cart()`，执行：
  1. 合并重复商品；
  2. 读取 snapshot；
  3. 运行纯 validation；
  4. validation 成功后调用一次 atomic `reserve`；
  5. atomic rejection 覆盖之前成功的 stale snapshot 结果。
- `reserve` 必须先检查所有商品，再扣减任何商品，不能边检查边扣减。

当前文件用一个 process-local `Lock` 表达 critical section。它只证明单进程模型，
生产环境应把 compare-and-decrement 放进数据库事务或 conditional update。

对 `k` 个预占商品，atomic reserve 是 `O(k)` time。完成标准是 multi-item
reservation 要么全部成功，要么库存完全不变。

---

## Follow-up 4 — request_id 幂等

文件：`follow_up_4_idempotency.py`

### 新需求

客户端可能因为 timeout 重试。相同请求不能重复扣减库存。

### 相对 Follow-up 3 要改什么

- `reserve` 和 `reserve_cart` 增加 `request_id`。
- 为请求构造 fingerprint：

```text
(restaurant_id, sorted quantities)
```

- 保存 `request_id -> (fingerprint, original result)`。
- 同一个 `request_id` + 同一个 payload：直接返回原结果，不再次扣库存。
- 同一个 `request_id` + 不同 payload：抛出 `ValueError`。
- 成功的 `held` 和失败的 `rejected` 都要保存；否则失败请求重试时结果可能变化。
- 成功时生成一个 `reservation_id`。

因为 fingerprint 对 `k` 个商品排序，这一阶段是 `O(k log k)` time。生产环境应由
authoritative database 的 unique constraint 保证幂等，而不是进程内字典。

---

## Follow-up 5 — confirm、release 与 expiration

文件：`follow_up_5_reservation_lifecycle.py`

### 新需求

`held` reservation 不能永久占用库存。增加 lease 和状态转换：

```text
held -> confirmed
held -> released
held -> expired
```

### 相对 Follow-up 4 要改什么

- `reserve(..., now)` 记录 `expires_at = now + lease_duration`。
- 保存 reservation 和它实际扣减的 quantities，便于恢复库存。
- 新增：
  - `confirm(reservation_id, now)`
  - `release(reservation_id)`
  - `expire_due(now)`
- `now >= expires_at` 时，`held` 先变为 `expired` 并恢复库存一次。
- 重复 confirm 已确认订单，返回同一个 `confirmed` 结果。
- 重复 release 已释放/过期订单，不再次增加库存。
- `confirmed` 后不能 release；过期扫描也不能恢复 confirmed stock。
- 不存在的 `reservation_id` 使用内置 `KeyError`，非法转换使用 `ValueError`；
  不增加一组面试时写不完的自定义 error classes。

`confirm` 通常是 `O(1)`；`release`/expiration 恢复 `k` 个商品时是 `O(k)`；
`expire_due` 还要扫描当前 reservation 集合。

---

## Follow-up 6 — stale snapshot 与并发最后一件

文件：`follow_up_6_stale_snapshot_and_concurrency.py`

### 新需求

验证两个 race condition：

1. snapshot 显示有库存，但真正 reserve 时库存已经没有了；
2. 两个请求同时抢最后一件商品。

### 相对 Follow-up 5 要改什么

- 保持 `CartService` 的原则：snapshot 只用于给用户早期错误，atomic reserve 才是
  最终 authority。
- 当 snapshot validation 成功、reserve 返回 `rejected` 时，把 authoritative
  shortage 映射回 `INSUFFICIENT_INVENTORY`。
- 用 `StaleSnapshotGateway` 演示 stale read。
- 用两个 `Thread` 同时预占最后一件；结果必须恰好是一个 `held`、一个
  `rejected`，最终库存为 0。

这一阶段没有假装实现 distributed hot-SKU infrastructure。process-local `Lock`
无法保护多个 service instances；真实系统需要数据库 conditional update、row lock
或按 SKU 串行化。cache 可以帮助早期筛选，但不能成为出售库存的 authority。

---

## 面试时如何使用这些文件

| Interviewer 的要求 | 打开哪个阶段 | 核心点 |
|---|---|---|
| 只验证购物车 | Base | 两遍扫描、稳定返回全部错误 |
| 重复商品要相加 | Follow-up 1 | 先 merge，再 validate |
| min/max 是整单限制 | Follow-up 2 | item errors 后追加 cart errors |
| 必须防止部分扣减和 oversell | Follow-up 3 | 一个 atomic boundary |
| 客户端会 retry | Follow-up 4 | request fingerprint + 原结果 |
| 订单需要确认、取消、过期 | Follow-up 5 | guarded state transitions |
| snapshot 会 stale / 最后一件竞争 | Follow-up 6 | atomic result 才是 authority |

不要在 Base 中提前写后面所有功能。先让当前 contract 跑通，再只加入 interviewer
要求的下一层。
