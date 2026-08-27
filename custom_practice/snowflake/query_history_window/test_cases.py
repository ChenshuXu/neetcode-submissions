from custom_practice.runner import Case
from solution import QueryRecord, WindowSummary


def query(
    query_id: str,
    warehouse_id: str,
    user_id: str,
    start_time: int,
    end_time: int,
    credits_used: int,
) -> QueryRecord:
    return QueryRecord(
        query_id=query_id,
        warehouse_id=warehouse_id,
        user_id=user_id,
        start_time=start_time,
        end_time=end_time,
        credits_used=credits_used,
    )


TEST_CASES = [
    Case(
        name="window shifts to the heavier cluster",
        args=(
            (
                query("q1", "wh-a", "u1", 0, 300, 5),
                query("q2", "wh-a", "u2", 600, 900, 4),
                query("q3", "wh-a", "u1", 1700, 2000, 3),
                query("q4", "wh-a", "u2", 1800, 2100, 10),
            ),
        ),
        expected=[
            WindowSummary("wh-a", 600, 2400, 17, "u2", 14),
        ],
    ),
    Case(
        name="half open boundary excludes exactly thirty minutes",
        args=(
            (
                query("q1", "wh-a", "alice", 0, 100, 10),
                query("q2", "wh-a", "bob", 1800, 1900, 10),
            ),
        ),
        expected=[
            WindowSummary("wh-a", 0, 1800, 10, "alice", 10),
        ],
    ),
    Case(
        name="equal start times stay in one candidate window",
        args=(
            (
                query("q1", "wh-a", "alice", 1000, 1100, 2),
                query("q2", "wh-a", "alice", 1000, 1200, 3),
                query("q3", "wh-a", "bob", 1000, 1300, 4),
            ),
        ),
        expected=[
            WindowSummary("wh-a", 1000, 2800, 9, "alice", 5),
        ],
    ),
    Case(
        name="crossing query belongs wholly to its start window",
        args=(
            (
                query("q1", "wh-a", "alice", 0, 7200, 10),
                query("q2", "wh-a", "bob", 1799, 2000, 1),
                query("q3", "wh-a", "bob", 1800, 2100, 9),
            ),
        ),
        expected=[
            WindowSummary("wh-a", 0, 1800, 11, "alice", 10),
        ],
    ),
    Case(
        name="top user tie uses lexicographically smaller id",
        args=(
            (
                query("q1", "wh-a", "zoe", 100, 200, 5),
                query("q2", "wh-a", "amy", 200, 300, 5),
            ),
        ),
        expected=[
            WindowSummary("wh-a", 100, 1900, 10, "amy", 5),
        ],
    ),
    Case(
        name="unsorted warehouses return in warehouse id order",
        args=(
            (
                query("q3", "wh-b", "bob", 100, 200, 3),
                query("q1", "wh-a", "alice", 50, 100, 4),
                query("q4", "wh-b", "bob", 3000, 3100, 8),
                query("q2", "wh-a", "amy", 100, 200, 2),
            ),
        ),
        expected=[
            WindowSummary("wh-a", 50, 1850, 6, "alice", 4),
            WindowSummary("wh-b", 3000, 4800, 8, "bob", 8),
        ],
    ),
    Case(
        name="equal peak totals keep the earlier window",
        args=(
            (
                query("q1", "wh-a", "alice", 0, 100, 5),
                query("q2", "wh-a", "bob", 2000, 2100, 5),
            ),
        ),
        expected=[
            WindowSummary("wh-a", 0, 1800, 5, "alice", 5),
        ],
    ),
    Case(
        name="empty history",
        args=((),),
        expected=[],
    ),
]
