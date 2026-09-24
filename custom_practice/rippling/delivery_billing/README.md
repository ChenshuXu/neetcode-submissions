# Rippling Delivery Billing — 2026-09-15 实际面试

来源：[题目还原与解法](../../../../projects/context/Interview/rippling/rippling-delivery-billing-problem-and-solution-2026-09-15.md)、
[面试复盘](../../../../projects/context/Interview/rippling/rippling-financial-product-technical-debrief-2026-09-15.md)。
这是 Newton 实际参加的 Financial Product 技术面，题目依据现场记录还原，不是原题逐字副本。
本目录使用 float 美元累计的参考实现，可直接运行；与相邻的 `delivery_payment` 面经练习分别保存。

## 题目

实现 `BillingSystem`，管理司机小时费率、记录配送费用并查询累计金额。

| API | 行为 |
| --- | --- |
| `add_driver(driver_id, usd_hourly_rate_per_delivery)` | 添加司机及初始美元/小时费率 |
| `record_delivery(delivery_id, driver_id, start_time, end_time)` | 记录已完成配送的费用 |
| `update_driver_rate(driver_id, new_rate, effective_time)` | 设置从指定时刻起（含该时刻）生效的新费率 |
| `get_total_cost()` | 返回累计美元金额字符串，固定两位小数 |

核心约定：

- 整单使用配送**开始时刻**适用的费率，途中变价不分段计费。
- delivery ID 全局去重；重复提交即使参数不同也忽略。
- 已入账金额冻结；费率更新不回算已有配送。
- 保留每单的小数分，只在查询最终总额时舍入；查询不修改内部金额。
- 使用可比较的 UTC `datetime`。每笔配送结束后记录，同一司机的重叠配送分别收费。
- 恰好三小时有效；超过三小时忽略。

精度反例：费率 $15.15/h，两单分别 1.5 小时和 0.5 小时，
`22.725 + 7.575 = 30.30`。逐单 half-up 到分会错误地得到 `30.31`。

## 本地实现选择（现场未完全确认）

- 查询时用 `int(total_cost * 100 + 0.5)` 将非负总额舍入到 cents，再格式化。
  这是浮点数上的 half-up 计算；二进制误差可能影响半分附近的结果，不保证精确十进制舍入。
  现场未确认最终 tie 规则；已有测试中的 `57.93` 是本地约定。
- 更新可乱序插入；相同生效时刻后一次调用优先。
- 重复司机、负费率和负时长抛 `ValueError`；未知司机按字典访问抛 `KeyError`。
- 费率转换为 float，须为有限非负数；时间输入由调用方保证为 UTC datetime。
- 零时长有效；超长配送不占用 ID，可用有效时长重试。重复 ID 在其他检查之前忽略。
- 单线程内存实现，不添加支付、数据库或并发功能。

## 文件与运行

- [solution.py](solution.py)：完整参考实现及两单金额示例。
- [test_cases.py](test_cases.py)：还原的面试调用序列，以及明确标注的本地边界案例。
- [run_tests.py](run_tests.py)：操作回放适配器，复用[共享 runner](../../runner.py)。

从仓库根目录执行：

```bash
python3 custom_practice/rippling/delivery_billing/solution.py
python3 custom_practice/rippling/delivery_billing/run_tests.py
python3 custom_practice/rippling/delivery_billing/run_tests.py --case fractional
```

也可在本目录执行 `python3 run_tests.py`；支持 `--list`。
测试不依赖外部转写文件，不运行隐藏测试。参考实现通过不代表限时独立完成能力。

## 实现要点

字典保存每位司机的排序费率历史，`bisect_right` 按开始时刻选价；集合保存已入账 ID，
`total_cost: float` 按美元累计，单笔费用为 `rate * duration.total_seconds() / 3600`，
查询时才舍入。不存储全部配送详情，也不逐单转为整数 cents，以免丢掉小数分。
此版本优先使用熟悉的基础运算，仍有浮点累计误差；严格精确计费需要另行约定金额和时间的最小单位。

设某司机有 K 次更新，系统有 D 位司机、U 次更新和 N 个已接受配送 ID：
添加司机平均 O(1)，记录配送 O(log(K+1))，更新最坏 O(K)，查询 O(1)，
总空间 O(D+U+N)。这些界限忽略输出长度成本。
