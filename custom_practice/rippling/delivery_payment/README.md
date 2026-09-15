# Rippling Q048 — Delivery Payment

打开 [solution.py](solution.py)：顶部有 Description、接口、口头确认的输入约定和例子；下方是完整实现；底部直接 `print`，预期输出写在注释中。

```bash
python3 solution.py
```

## 已有信息与练习约定

依据 [Q048 题单](</Users/Newton/Documents/job search/projects/context/Interview/rippling/rippling-financial-product-interview-prep-2026-09-15.md>) 和 [证据账](</Users/Newton/Documents/job search/projects/context/Interview/rippling/rippling-financial-product-interview-evidence-2026-09-15.md>)，仅使用已保存材料：

| 来源 | 已披露内容 |
| --- | --- |
| S-W1-020 · London SWE II phone | 三个基础函数，名字未披露；pay_upto_time、get_total_unpaid_cost；最近24小时最大同时配送司机数；金额精度讨论 |
| S-W1-021 · 旧 SDE2 screen | add_driver(driverId)、add_delivery(driverId,startTime,endTime)、get_total_cost；pay_up_to_time、get_cost_to_be_paid；最近24小时最大活跃司机数 |
| S-W3-040 · phone | addDriver、recordDelivery、getTotalCost；payUpTo、getTotalCostUnpaid；最大同时配送司机数及对应时间区间 |

本练习沿用旧来源的三个基础接口、London 来源的支付/未付接口名。`add_delivery` 对应另一变体的 `recordDelivery`，不重复实现别名。最大值区间通过额外方法返回，其名称是本地约定。

**以下是为运行练习补全的假设，不是原帖已确认要求：**

- 时间为整数分钟，金额为整数美元；固定每分钟每笔配送 $1，所以 cost = end - start。不向 add_driver 增加来源没有披露的 rate 参数。
- 支付按结束时间 ≤ cutoff 整笔处理，返回本次新支付总额。不做部分支付；重复调用不重复支付；补录也能支付。
- 总成本包含所有已记录配送，支付后不减少。重叠配送分别计费。
- 统计窗口为 [now - 1440, now)，配送区间为 [start, end)。同一司机重叠配送只算一个司机；相邻最大值区间合并；返回所有最大区间。
- 已支付配送仍参与历史统计；空窗口返回 (0, [])。

类型、输入合法性和调用顺序在写代码前口头确认，不写防御性检查。金额精度是已有面经的真实讨论点；本轮按用户要求使用整数，不添加金额解析或转换函数。

## 怎么讲实现

费用部分：字典保存每位司机的配送历史，最小堆保存未付配送，两个整数保存累计总额和未付总额。每笔配送只入堆、出堆一次。

窗口部分：把配送裁剪到窗口，收集开始/结束事件。记录每位司机当前配送数；只有从0变为正数、从正数变为0时才改变司机总数。同一时刻全部事件处理后，当前司机数适用于到下一个事件的区间。

不变式：未付堆内金额之和等于 unpaid_cost；扫描中 active_drivers 等于当前配送数大于0的司机数量。

复杂度写在代码顶部。费用查询 O(1)；支付 K 笔为 O(1 + K log U)；历史统计 O(N log N)，保留所有历史 O(N + 司机数)。

核对底部输出可运行 `python3 test_solution.py`。独立练习时先完成计费和支付，再写窗口统计及返回区间的 follow-up；当前完整实现属于辅助准备，不代表独立演练已完成。
