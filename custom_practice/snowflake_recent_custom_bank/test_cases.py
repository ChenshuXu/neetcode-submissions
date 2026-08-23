from custom_practice.runner import Case


TEST_CASES = {
    "single_query_revenue": [
        Case(
            name="choose the best repeatable query type",
            args=(10, (("scan", 3, 5), ("join", 4, 8))),
            expected=(16, "join"),
        ),
        Case(
            name="lexicographic tie and no runnable type",
            args=(2, (("zeta", 3, 20), ("alpha", 5, 100))),
            expected=(0, None),
        ),
        Case(
            name="tie chooses the smaller type name",
            args=(12, (("beta", 3, 4), ("alpha", 4, 6))),
            expected=(18, "alpha"),
        ),
    ],
    "horizontal_pod_autoscaler": [
        Case(
            name="point assignment then global floor",
            args=((2, 1, 5), (("set", 1, 4), ("raise_min", 3))),
            expected=[3, 4, 5],
        ),
        Case(
            name="later point assignment can go below an earlier floor",
            args=((1, 2), (("raise_min", 5), ("set", 0, 3), ("raise_min", 4))),
            expected=[4, 5],
        ),
    ],
    "string_xor": [
        Case(name="all counts are even", args=("aabb",), expected=0),
        Case(name="two odd letters", args=("ab",), expected=1),
        Case(name="three odd letters", args=("abc",), expected=0),
        Case(name="one odd letter", args=("aaab",), expected=1),
    ],
    "database_configuration": [
        Case(name="one edge", args=((-1, 0),), expected="TF"),
        Case(name="four-node chain", args=((-1, 0, 1, 2),), expected="TFTF"),
        Case(name="three-node star", args=((-1, 0, 0),), expected="FFF"),
    ],
    "string_patterns": [
        Case(name="no vowels allowed", args=(1, 0), expected=21),
        Case(name="one position", args=(1, 1), expected=26),
        Case(name="two positions and no adjacent vowels", args=(2, 1), expected=651),
        Case(name="three positions and no adjacent vowels", args=(3, 1), expected=16401),
    ],
    "acl_inheritance": [
        Case(
            name="multiple parents and inherited deny",
            args=(
                ((), (0,), (0,), (1, 2)),
                {0: ("read",), 1: ("write",), 2: ("share",), 3: ("admin",)},
                {2: ("write",), 3: ("read",)},
                3,
            ),
            expected=["admin", "share"],
        ),
        Case(
            name="local deny overrides inherited allow",
            args=(
                ((), (0,)),
                {0: ("read", "write")},
                {1: ("write",)},
                1,
            ),
            expected=["read"],
        ),
    ],
    "distributed_nary_count": [
        Case(
            name="transient timeout then successful fanout",
            args=(
                "a",
                {
                    "a": (None, ("b", "c")),
                    "b": ((),),
                    "c": (("d",),),
                    "d": ((),),
                },
                2,
            ),
            expected=4,
        ),
        Case(
            name="duplicate responses are idempotent",
            args=(
                "a",
                {
                    "a": (("b", "b", "c"),),
                    "b": (("c",),),
                    "c": ((),),
                },
                1,
            ),
            expected=3,
        ),
    ],
    "http_retry_backoff": [
        Case(
            name="exponential retry then success",
            args=((500, 503, 200), {}, 1, 3, 10),
            expected=(200, (1, 2)),
        ),
        Case(
            name="retry after overrides exponential delay",
            args=((429, 200), {0: 5}, 1, 3, 10),
            expected=(200, (5,)),
        ),
        Case(
            name="non retryable status stops immediately",
            args=((400, 200), {}, 1, 3, 10),
            expected=(400, ()),
        ),
        Case(
            name="total deadline prevents another attempt",
            args=((500, 500, 200), {}, 4, 3, 5),
            expected=(500, (4,)),
        ),
    ],
    "result_cache_invalidation": [
        Case(
            name="same context hits cache and a table mutation invalidates it",
            args=((
                ("query", "select * from t", "analyst", "wh1", "utc", ("t",), "v1"),
                ("query", "SELECT  *  FROM t", "analyst", "wh1", "utc", ("t",), "ignored"),
                ("mutate", "t"),
                ("query", "select * from t", "analyst", "wh1", "utc", ("t",), "v2"),
            ),),
            expected=("v1", "v1", "v2"),
        ),
        Case(
            name="role warehouse and session digest isolate entries",
            args=((
                ("query", "select 1", "role_a", "wh1", "utc", (), "a"),
                ("query", "select 1", "role_b", "wh1", "utc", (), "b"),
                ("query", "select 1", "role_a", "wh2", "utc", (), "c"),
                ("query", "select 1", "role_a", "wh1", "pst", (), "d"),
            ),),
            expected=("a", "b", "c", "d"),
        ),
    ],
    "sql_table_extraction": [
        Case(
            name="qualified tables aliases and join",
            args=("SELECT * FROM sales.orders o JOIN users u ON u.id=o.user_id",),
            expected=["sales.orders", "users"],
        ),
        Case(
            name="subquery and comments",
            args=("SELECT * FROM (SELECT * FROM raw.events -- source\n) e JOIN dim_users d ON 1=1",),
            expected=["raw.events", "dim_users"],
        ),
        Case(
            name="cte name is not a physical table",
            args=("WITH recent AS (SELECT * FROM logs) SELECT * FROM recent JOIN users ON 1=1",),
            expected=["logs", "users"],
        ),
    ],
    "redundant_parentheses": [
        Case(name="single value is redundant", args=("(a)",), expected=True),
        Case(name="operator makes the group meaningful", args=("(a+b)",), expected=False),
        Case(name="outer wrapper is redundant", args=("((a+b))",), expected=True),
        Case(name="nested multiplication is meaningful", args=("a+(b*c)",), expected=False),
    ],
    "sessionization": [
        Case(
            name="exact gap stays in the session and larger gap splits",
            args=((('u', 61), ('u', 0), ('v', 5), ('u', 30)), 30),
            expected=[('u', 0, 30, 2), ('u', 61, 61, 1), ('v', 5, 5, 1)],
        ),
        Case(name="empty events", args=((), 30), expected=[]),
    ],
    "preaggregate_three_tables": [
        Case(
            name="independent aggregates avoid fact-table fanout",
            args=(
                ((1, "A"), (2, "B")),
                ((1, 10.0), (1, 5.5), (2, 7.0)),
                ((1, 3), (1, 4), (2, 2), (2, 1)),
            ),
            expected=[(1, "A", 15.5, 7), (2, "B", 7.0, 3)],
        ),
        Case(
            name="accounts with no facts are retained",
            args=(((1, "A"),), (), ()),
            expected=[(1, "A", 0.0, 0)],
        ),
    ],
    "census_nl2sql": [
        Case(
            name="highest population answer includes source row",
            args=(
                "highest population state",
                (
                    {"state": "CA", "population": 39000000, "median_income": 91000},
                    {"state": "TX", "population": 30000000, "median_income": 76000},
                ),
            ),
            expected={"answer": "CA", "value": 39000000, "sources": ("CA",)},
        ),
        Case(
            name="state population lookup",
            args=(
                "population of TX",
                (
                    {"state": "CA", "population": 39000000, "median_income": 91000},
                    {"state": "TX", "population": 30000000, "median_income": 76000},
                ),
            ),
            expected={"answer": "TX", "value": 30000000, "sources": ("TX",)},
        ),
    ],
}
