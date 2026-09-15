"""Rippling Q058 — Task Scheduler

Description
-----------
Given a list of tasks, return their IDs in the order they should run:
1. Deduplicate tasks by (description, due_date).
2. Remove completed tasks.
3. Sort the remaining tasks by the agreed priority rule.
4. Run every prerequisite before the tasks that depend on it.
5. Among currently runnable tasks, choose by the agreed priority rule.

Each task is a dictionary:
    id: unique string ID
    description: string used for deduplication
    due_date: integer timestamp (simple numbers in the examples)
    priority: integer; smaller values run first in this practice
    completed: boolean
    parent_ids: list of prerequisite task IDs; empty for an independent task
    created_at: integer timestamp

Input assumptions — confirm verbally before coding, do not validate here
----------------------------------------------------------------------
- All fields exist and have the types above. IDs are unique.
- Dependency links form a DAG. A task may have multiple prerequisites.
- Deduplication keeps the FIRST input occurrence, even if it is completed.
  Filter completed tasks AFTER deduplication; a later duplicate is not revived.
- Duplicate descriptions with DIFFERENT due dates are different tasks.
- Priority order is (priority, due_date, created_at), ascending.
  Complete ties preserve input order.
- At each step, choose the smallest priority key among zero-indegree tasks.
- Missing, completed or deduplicated-away prerequisite IDs are ignored.
  Do not redirect a dependency to a duplicate's retained ID.
- Return IDs, not task objects. Do not mutate the input.
- This function orders one supplied batch; it does not execute tasks or sleep.
  due_date is a sort key, not a filter against the current time.

These are explicit practice choices where the reports leave details open.
The source does NOT establish the comparator, duplicate winner, orphan policy,
or multiple-parent behavior. See README.md for evidence.

Example
-------
Input:
    tasks = [
        {"id": "child", "description": "Send report", "due_date": 10,
         "priority": 0, "completed": False, "parent_ids": ["parent"], "created_at": 1},
        {"id": "other", "description": "Review invoice", "due_date": 10,
         "priority": 1, "completed": False, "parent_ids": [], "created_at": 2},
        {"id": "parent", "description": "Build report", "due_date": 10,
         "priority": 2, "completed": False, "parent_ids": [], "created_at": 3},
    ]
Output:
    ["other", "parent", "child"]
Explanation:
    The two initially runnable tasks are ordered by priority. The child must wait for its parent,
    even though the child has the smallest priority number.

Approach
--------
Build an adjacency list and indegree count, then run Kahn's topological sort.
A min-heap chooses the highest-priority task among all currently runnable tasks.
Invariant: every task in the heap has no unfinished retained prerequisite.

Let V be the retained tasks and E their retained dependency links.
Time: O((V + E) log V). Space: O(V + E).
"""

import heapq

def schedule_tasks(tasks: list[dict]) -> list[str]:
    # 先去重，再过滤完成任务；后面的副本不会替换第一个副本。
    seen = set()
    remaining = []
    for task in tasks:
        key = (task["description"], task["due_date"])
        if key in seen:
            continue
        seen.add(key)

        if task["completed"]:
            continue
        remaining.append(task)

    by_id = {}  # task ID -> complete task dictionary
    graph = {}  # prerequisite task ID -> dependent task IDs
    indegree = {}  # task ID -> number of retained prerequisites
    input_order = {}  # task ID -> position among retained input tasks
    for index, task in enumerate(remaining):
        task_id = task["id"]
        by_id[task_id] = task
        graph[task_id] = []
        indegree[task_id] = 0
        input_order[task_id] = index

    for task in remaining:
        task_id = task["id"]
        for prerequisite_id in task["parent_ids"]:
            if prerequisite_id in by_id:
                graph[prerequisite_id].append(task_id)
                indegree[task_id] += 1

    available = []  # priority tuples for all zero-indegree task IDs
    for task in remaining:
        task_id = task["id"]
        if indegree[task_id] == 0:
            heapq.heappush(
                available,
                (
                    task["priority"],
                    task["due_date"],
                    task["created_at"],
                    input_order[task_id],
                    task_id,
                ),
            )

    result = []
    while available:
        *_, task_id = heapq.heappop(available)
        result.append(task_id)

        for dependent_id in graph[task_id]:
            indegree[dependent_id] -= 1
            if indegree[dependent_id] == 0:
                dependent = by_id[dependent_id]
                heapq.heappush(
                    available,
                    (
                        dependent["priority"],
                        dependent["due_date"],
                        dependent["created_at"],
                        input_order[dependent_id],
                        dependent_id,
                    ),
                )

    if len(result) != len(remaining):
        raise ValueError("task dependencies contain a cycle")

    return result


if __name__ == "__main__":
    # 1. Child appears first in the input and has higher priority than its parent.
    tasks = [
        {"id": "child", "description": "Send report", "due_date": 10,
         "priority": 0, "completed": False, "parent_ids": ["parent"], "created_at": 1},
        {"id": "other", "description": "Review invoice", "due_date": 10,
         "priority": 1, "completed": False, "parent_ids": [], "created_at": 2},
        {"id": "parent", "description": "Build report", "due_date": 10,
         "priority": 2, "completed": False, "parent_ids": [], "created_at": 3},
    ]
    print(schedule_tasks(tasks))  # ['other', 'parent', 'child']
    print(schedule_tasks([]))  # []

    # 2. Completed first copy wins deduplication; another due date is distinct.
    duplicates = [
        {"id": "done", "description": "Email", "due_date": 10,
         "priority": 2, "completed": True, "parent_ids": [], "created_at": 1},
        {"id": "copy", "description": "Email", "due_date": 10,
         "priority": 0, "completed": False, "parent_ids": [], "created_at": 2},
        {"id": "tomorrow", "description": "Email", "due_date": 11,
         "priority": 2, "completed": False, "parent_ids": [], "created_at": 3},
        {"id": "followup", "description": "Follow up", "due_date": 10,
         "priority": 1, "completed": False, "parent_ids": ["done"], "created_at": 4},
    ]
    print(schedule_tasks(duplicates))  # ['followup', 'tomorrow']
    print(schedule_tasks(duplicates[:1]))  # []

    # 3. Always choose the best priority among tasks whose prerequisites are done.
    tree = [
        {"id": "A", "description": "A", "due_date": 10,
         "priority": 1, "completed": False, "parent_ids": [], "created_at": 0},
        {"id": "D", "description": "D", "due_date": 10,
         "priority": 2, "completed": False, "parent_ids": ["A"], "created_at": 0},
        {"id": "C", "description": "C", "due_date": 10,
         "priority": 1, "completed": False, "parent_ids": ["A"], "created_at": 0},
        {"id": "E", "description": "E", "due_date": 10,
         "priority": 99, "completed": False, "parent_ids": ["C", "D"], "created_at": 0},
        {"id": "B", "description": "B", "due_date": 10,
         "priority": 2, "completed": False, "parent_ids": [], "created_at": 0},
    ]
    print(schedule_tasks(tree))  # ['A', 'C', 'D', 'B', 'E']
    assert schedule_tasks(tree) == ["A", "C", "D", "B", "E"]

    # 4. Due date, then creation time, then original input order break ties.
    ties = [
        {"id": "late", "description": "Late", "due_date": 20,
         "priority": 1, "completed": False, "parent_ids": [], "created_at": 0},
        {"id": "new", "description": "New", "due_date": 10,
         "priority": 1, "completed": False, "parent_ids": [], "created_at": 2},
        {"id": "z", "description": "Z", "due_date": 10,
         "priority": 1, "completed": False, "parent_ids": [], "created_at": 1},
        {"id": "a", "description": "A", "due_date": 10,
         "priority": 1, "completed": False, "parent_ids": [], "created_at": 1},
    ]
    print(schedule_tasks(ties))  # ['z', 'a', 'new', 'late']

    # 5. Missing or discarded prerequisites do not block a retained task.
    missing = [
        {"id": "first", "description": "Parent", "due_date": 10,
         "priority": 2, "completed": False, "parent_ids": [], "created_at": 0},
        {"id": "copy", "description": "Parent", "due_date": 10,
         "priority": 0, "completed": False, "parent_ids": [], "created_at": 1},
        {"id": "child", "description": "Child", "due_date": 10,
         "priority": 1, "completed": False, "parent_ids": ["copy"], "created_at": 2},
        {"id": "orphan", "description": "Orphan", "due_date": 10,
         "priority": 0, "completed": False, "parent_ids": ["absent"], "created_at": 3},
    ]
    print(schedule_tasks(missing))  # ['orphan', 'child', 'first']
