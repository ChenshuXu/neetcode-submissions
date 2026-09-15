# Rippling Q010 — Food Delivery OOD

完整题干、输入约定、代码与 `print` 示例都在 [solution.py](solution.py)。金额用整数美元；输入约定先口头确认，代码不做合法性检查。

## 来源与练习约定

已有 [Q010 题单](</Users/Newton/Documents/job search/projects/context/Interview/rippling/rippling-financial-product-interview-prep-2026-09-15.md>) 与 [证据账](</Users/Newton/Documents/job search/projects/context/Interview/rippling/rippling-financial-product-interview-evidence-2026-09-15.md>)：

- S-W1-019、S-W3-017 披露 Food Delivery System，以及 `AddDelivery`、`RecordDelivery`、`PayUpto` 三个接口。考点包括类的职责、数据结构和各接口复杂度。
- S-W2-011 营销材料也列出这三个接口，没有补充确定的输入输出。
- 原材料没有参数、计费方式、支付截止边界。下表是本练习补全的约定，不代表已恢复原题细节，也不把 Q048 的司机计费题接口合并过来。

| 接口 | 本练习定义 |
| --- | --- |
| `AddDelivery(delivery_id, driver_id, amount)` | 新增配送任务，指定司机和固定报酬，返回 None |
| `RecordDelivery(delivery_id, end_time)` | 记录完成时间，返回 None |
| `PayUpto(cutoff)` | 支付完成时间 ≤ cutoff 的已记录未支付配送，返回本次每位司机的合计金额 |

金额和时间均为非负整数；ID 唯一、记录只发生一次等输入保证写在代码顶部。相同完成时间、乱序记录、重复支付调用、同一司机多笔合计和补录都包含在可运行示例中。未记录完成的配送不能支付；补录的旧配送在下一次符合截止条件的调用中支付。支付只更新内存状态。

## 实现

- `Delivery` 保存司机与金额。
- `pending` 保存尚未记录完成的配送，按 ID 查找。
- `unpaid` 用最小堆保存已完成未支付的配送，按完成时间取出。付款后移除，避免重复支付。

不变式：每笔尚未支付的配送只在 pending 或 unpaid 中出现；已支付配送不再留在这两个容器中。

扫描全部配送也可以实现，但每次支付需要 O(N)；这里用标准库 heapq，使支付只处理已经到期的记录。新增平均 O(1)，记录完成 O(log N)，支付 K 笔为 O(1 + K log N)，总状态 O(N)。

## 运行

在当前目录直接运行：

```bash
python3 solution.py
```

底部直接 `print`，预期输出写在注释中。无需测试框架或额外依赖。

练习顺序：先确认三个接口的含义与边界，再解释字典和堆各自负责什么，最后自己复写并跑示例。这份实现已由 Codex 协助完成，不代表独立面试演练已完成。
