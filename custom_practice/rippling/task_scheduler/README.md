# Rippling Q058 — Task Scheduler

[solution.py](solution.py) 包含完整 Description、口头确认的输入约定、实现、复杂度，以及底部 `print` + 预期输出注释的示例。

```bash
python3 custom_practice/rippling/task_scheduler/solution.py
```

从 neetcode-submissions 根目录运行以上命令；也可在本目录直接运行 `python3 solution.py`。无额外依赖。

## 已有来源与练习补全

依据 [Q058 题单](</Users/Newton/Documents/job search/projects/context/Interview/rippling/rippling-financial-product-interview-prep-2026-09-15.md>) 和 [证据账](</Users/Newton/Documents/job search/projects/context/Interview/rippling/rippling-financial-product-interview-evidence-2026-09-15.md>)，本轮仅使用已有资料，未新增网络调研：

- **S-W3-021**：description、due date、priority、completed、parent id；按 `(description, due date)` 去重，剔除 completed，按给定规则排序，孩子接在父任务后。具体比较器、去重保留哪个副本等未披露。
- **S-W3-018**：电话轮变体披露 id、due date、create time、parent id，输出父先子后的任务列表。其余题干有隐藏。
- **S-W3-018/019 评论**：讨论孩子排序、DFS 与 heap/BFS；作者的 DFS 作答不是统一标准答案。续页作者表示没有第三问，不将该说法套用到其他来源。

这份练习合并已知字段，并将单数 `parent id` 扩展为 `parent_ids`，用于练习一个任务依赖多个前置任务的 DAG 版本。明确补全为：priority 数字小的优先，其次 due_date、created_at；并列时保留输入顺序；先保留首个副本再过滤完成任务；缺失、完成或被去重移除的依赖不阻塞当前任务；每次从所有 zero-indegree tasks 中选择最高优先级任务。时间用整数，依赖图必须无环。以上未披露的语义都是**练习约定**，不是来源确认的原题 contract，现场应先口头确认。

建议分阶段理解代码：去重与过滤 → 建立 graph 和 indegree → zero-indegree heap → Kahn topological sort。代码不是分布式调度器，不执行任务，不按当前时间过滤。

## 已有追问的边界

- S-W3-021 提及 scheduler 运行频率、拉取停止条件，但没有明确接口或答案。讨论时先确认允许的延迟和批次规模；分页拉取可讨论空页或无 next cursor 的停止条件，不将它们加进当前纯排序函数。
- 当前练习采用“所有当前可执行任务中选最高优先级”的就绪任务堆，不再保证子树连续；多个 prerequisite 时也不存在唯一父树。
- 文章跨分类去重、feed 无限增长、第三方 API 故障、容量数字属于来源中轮次不明的其他片段，不补成 Q058 编程功能。

实现已辅助完成；直接运行样例不等于已独立完成面试练习。
