from custom_practice.runner import Case


RAISES_VALUE_ERROR = "<raises ValueError>"


TEST_CASES = [
    Case(
        name="empty graph",
        args=(0, (), {}, {}),
        expected=[],
    ),
    Case(
        name="single root resolves local conflict with deny",
        args=(
            1,
            (),
            {0: ("write", "read", "write")},
            {0: ("write",)},
        ),
        expected=[["read"]],
    ),
    Case(
        name="chain propagates allow and local deny",
        args=(
            3,
            ((0, 1), (1, 2)),
            {
                0: ("read", "write"),
                1: ("share",),
                2: ("admin",),
            },
            {1: ("write",)},
        ),
        expected=[
            ["read", "write"],
            ["read", "share"],
            ["admin", "read", "share"],
        ],
    ),
    Case(
        name="diamond merges parents and deny wins across paths",
        args=(
            4,
            ((0, 1), (0, 2), (1, 3), (2, 3)),
            {
                0: ("read",),
                1: ("write",),
                2: ("share",),
                3: ("admin",),
            },
            {
                2: ("write",),
                3: ("read",),
            },
        ),
        expected=[
            ["read"],
            ["read", "write"],
            ["read", "share"],
            ["admin", "share"],
        ],
    ),
    Case(
        name="multiple roots and disconnected component",
        args=(
            4,
            ((0, 2), (1, 2)),
            {
                0: ("read",),
                1: ("write",),
                2: ("delete",),
                3: ("audit",),
            },
            {1: ("delete",)},
        ),
        expected=[
            ["read"],
            ["write"],
            ["read", "write"],
            ["audit"],
        ],
    ),
    Case(
        name="duplicate edges do not change inheritance",
        args=(
            2,
            ((0, 1), (0, 1), (0, 1)),
            {0: ("read",), 1: ("write",)},
            {},
        ),
        expected=[
            ["read"],
            ["read", "write"],
        ],
    ),
    Case(
        name="local allow cannot override inherited deny",
        args=(
            2,
            ((0, 1),),
            {1: ("write",)},
            {0: ("write",)},
        ),
        expected=[[], []],
    ),
    Case(
        name="directed cycle is invalid",
        args=(
            3,
            ((0, 1), (1, 2), (2, 0)),
            {0: ("read",)},
            {},
        ),
        expected=RAISES_VALUE_ERROR,
    ),
    Case(
        name="self loop is invalid",
        args=(
            1,
            ((0, 0),),
            {},
            {},
        ),
        expected=RAISES_VALUE_ERROR,
    ),
]
