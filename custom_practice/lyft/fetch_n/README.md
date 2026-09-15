# Lyft Q004 — 跨调用连续读取 fetch_n

[solution.py](solution.py) 包含 Description、完整实现、中文逻辑注释、输入假设和底部 `print` + 预期输出注释。直接运行：

```bash
python3 custom_practice/lyft/fetch_n/solution.py
```

## 已有证据

依据 [Q004 题单](</Users/Newton/Documents/job search/projects/context/Interview/lyft/lyft-fulfillment-core-services-interview-prep-2026-09-15.md>) 和 [证据账](</Users/Newton/Documents/job search/projects/context/Interview/lyft/lyft-fulfillment-core-services-interview-evidence-2026-09-15.md>)：

- **S-W3-005**：亲历电话题，已有 `fetch(page)` 返回 items 与 nextPage，另一 class 实现跨调用 `fetch_n`，保存未交付余量。
- **S-W2-001 / S-W1-045**：同一 Chill 汇总及转载来源组，补充跨页、EOF、不稳定 upstream 的重试与 continuation state。重试不是已独立验证的现场追问。
- **S-NR-001**：只有相关标题，不提供更多约束。
- 原题没有明确 Python 返回结构、初始 token、空页、异常类型、重试次数或失败后的交付语义。代码里的这些细节均为本练习补全；不合并 Q009 的 fetch-all、每页最多 10 条或 -1 终点契约。

## LeetCode 近似题

[LC158 — Read N Characters Given read4 II - Call Multiple Times](https://leetcode.com/problems/read-n-characters-given-read4-ii-call-multiple-times/) 的完整题面已在现有 [9/15 归档](</Users/Newton/Documents/job search/projects/context/Interview/lyft/research-2026-09-15/lc158-001.json>) 中核对，本轮复读该归档，没有新增网络调研。

| LC158 | 本题 |
| --- | --- |
| read4(buf4)，最多 4 个字符 | fetch(page)，每页数量不固定 |
| 文件位置由 read4 保存 | reader 保存下一个 page token |
| 未交付字符留到下一次 read | 未交付 items 留到下一次 fetch_n |
| 写入 buf，返回数量 | 返回 item 列表 |
| read4 少于 4 表示到文件末尾 | 只有 next_page=None 表示无下一页；空页可继续 |

LC158 是状态缓冲机制的近似题，不是 Lyft 原题。可以把 LC 的连续读取 `abc`、请求 `[1, 2, 1]`，映射成这里的返回 `['a']`、`['b', 'c']`、`[]`。

## 练习约定与实现取舍

- 数据用整数列表；n 非负；0 不触发 fetch。token 可以是整数或字符串，只有 None 表示终点。输入合法、token 链有限且无环，这些只在注释中口头确认。
- 先练 `max_attempts=1` 的跨调用缓冲，再看 `_fetch_page` 中的重试。失败只重试同一 token，不跳页；达到上限后抛出 TimeoutError。
- 本练习选择“失败调用不交付任何条目”：先填 buffer，再取出结果。失败前已成功读取的页仍保存在 buffer，后续调用可以继续。这需要 O(N+B) 峰值空间（N 为至今最大请求量，B 为最大页长）；若要求仅保留一页，应先讨论失败是否允许返回部分结果。
- 不实现并发、异步、退避计时或服务端分页；MockClient 只是让本地代码可以直接运行的已有 API 替身。
