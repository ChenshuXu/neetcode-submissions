# Rippling Q003 + LC 588 — File System

[solution.py](solution.py) 包含完整 Description、接口、口头确认的输入约定、代码以及底部 `print` / 预期输出注释。

```bash
python3 solution.py
```

## 来源与范围

- [Rippling Q003](</Users/Newton/Documents/job search/projects/context/Interview/rippling/rippling-financial-product-interview-prep-2026-09-15.md>) / [证据账](</Users/Newton/Documents/job search/projects/context/Interview/rippling/rippling-financial-product-interview-evidence-2026-09-15.md>)：S-W3-006 披露创建文件、创建目录、删除、列目录，以及深层目录和高效搜索。S-W1-034 是类似内容的营销补充，不能当独立完整题面。
- [LC 588 官方题面](https://leetcode.com/problems/design-in-memory-file-system/)：2026-09-15 已通过 Newton 的 Premium 登录会话完整核验。四个接口、文件名/目录列表返回规则、字典序、自动创建中间目录、追加内容和官方示例与当前实现一致。先前的 Premium 限制来自未登录抓取，不是用户没有会员。
- delete、search 属于 Rippling 扩展。删除整棵非空子树、按 basename 精确匹配、同时搜文件和目录、返回排序绝对路径、排除起始目录，均为明确的本地练习约定。

## LC 原题与本地扩展的边界

LC 保证输入合法，读取/列出的目标存在，写文件的父目录存在。路径为绝对路径，除根目录外没有末尾斜线；名称只含小写字母，同目录不重名。路径长度为1–100，写入内容长度为1–50，四个接口合计最多调用300次；mkdir 的目标目录保证尚不存在。

本地额外覆盖：空文件、对已有目录再次 mkdir、1500层路径，以及 Rippling 的删除和搜索。这些用于练习扩展能力，不是 LC 588 的原始测试约束。输入仍只口头确认，不增加合法性检查。

## 分阶段练习

| 阶段 | 要做什么 |
| --- | --- |
| 基础 | ls 列即时子项，文件路径返回文件名；mkdir 创建中间目录；写入不存在的文件或追加内容；读取完整内容 |
| 删除 | 删除文件或目录子树；不允许删除根目录，输入中保证这一点 |
| 搜索与深层嵌套 | 在指定目录的所有后代中找同名文件/目录，返回绝对路径；用循环和显式栈处理深层目录 |

输入为合法绝对路径，所需父目录存在，名字不冲突，读/列/删/搜目标存在；这些只在编码前确认，不添加运行时检查。允许空文件；mkdir 已有目录保留内容。所有操作只修改内存对象，不访问真实磁盘。

## 实现思路

一个 Node 表示文件或目录：children 按名称找孩子，is_file 区分类型，content 保存文本。FileSystem 持有根节点。

- `_find` 按路径逐层查找，访问量由路径长度决定。
- 删除从父节点的 children 移除目标，整个子树随之不可访问。
- 按名称搜索遍历目标子树，文件和目录都参与名称匹配。循环避免递归调用的深度限制。

不变式：每个父目录的 children 精确表示其直接子项；文件节点没有孩子。

复杂度在代码顶部。这里没有维护全局名称索引；若追问大量重复搜索，可以讨论 name → paths 索引，以及创建/删除时的维护成本。搜索规则尚未在原报告中披露，不预设索引是面试官要求。

## 验证

`python3 test_solution.py` 核对18个打印结果，包括基础例子、追加、排序、空文件、同名节点、搜索范围、子树删除、删除后重建和1500层目录。保留底部直接 print 的面试写法。

当前为已实现的辅助练习，不代表独立复写或限时面试演练已完成。
