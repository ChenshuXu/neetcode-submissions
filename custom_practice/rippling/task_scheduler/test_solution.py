"""Small regression check; run solution.py for the interview-style print examples."""
from copy import deepcopy
from solution import schedule_tasks


if __name__ == "__main__":
    # A deep chain must remain parent-first even when every child outranks its parent.
    tasks = []
    for i in range(1500):
        parent_id = None
        if i > 0:
            parent_id = str(i - 1)
        tasks.append({"id": str(i), "description": str(i), "due_date": 10,
                      "priority": -i, "completed": False,
                      "parent_id": parent_id, "created_at": i})
    tasks.reverse()
    before = deepcopy(tasks)
    expected = list(map(str, range(1500)))
    assert schedule_tasks(tasks) == expected
    assert tasks == before
    print("Deep chain and input preservation passed.")
