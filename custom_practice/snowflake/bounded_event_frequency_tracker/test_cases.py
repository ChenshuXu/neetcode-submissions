from custom_practice.runner import Case


TEST_CASES = [
    Case(
        name="empty tracker",
        args=(
            5,
            (
                ("most_frequent", 1),
                ("most_frequent", 10),
            ),
        ),
        expected=(None, None),
    ),
    Case(
        name="prompt example and exact left boundary",
        args=(
            5,
            (
                ("record", 1, "a"),
                ("record", 2, "b"),
                ("record", 3, "a"),
                ("most_frequent", 3),
                ("record", 6, "b"),
                ("most_frequent", 6),
                ("record", 7, "a"),
                ("most_frequent", 7),
            ),
        ),
        expected=("a", "b", "a"),
    ),
    Case(
        name="event exactly on left boundary is expired",
        args=(
            5,
            (
                ("record", 10, "only"),
                ("most_frequent", 14),
                ("most_frequent", 15),
            ),
        ),
        expected=("only", None),
    ),
    Case(
        name="same timestamp duplicates and lexicographic tie",
        args=(
            10,
            (
                ("record", 20, "red"),
                ("record", 20, "blue"),
                ("record", 20, "red"),
                ("record", 20, "blue"),
                ("most_frequent", 20),
            ),
        ),
        expected=("blue",),
    ),
    Case(
        name="former winner disappears after expiry",
        args=(
            5,
            (
                ("record", 1, "a"),
                ("record", 2, "a"),
                ("record", 3, "b"),
                ("most_frequent", 3),
                ("most_frequent", 7),
            ),
        ),
        expected=("a", "b"),
    ),
    Case(
        name="queries advance time without new records",
        args=(
            3,
            (
                ("record", 10, "x"),
                ("record", 11, "y"),
                ("most_frequent", 12),
                ("most_frequent", 13),
                ("most_frequent", 14),
            ),
        ),
        expected=("x", "y", None),
    ),
    Case(
        name="winner changes as several timestamps expire",
        args=(
            4,
            (
                ("record", 1, "cat"),
                ("record", 1, "cat"),
                ("record", 2, "dog"),
                ("record", 4, "dog"),
                ("most_frequent", 4),
                ("record", 5, "dog"),
                ("most_frequent", 5),
                ("record", 6, "cat"),
                ("most_frequent", 6),
            ),
        ),
        expected=("cat", "dog", "dog"),
    ),
    Case(
        name="key can return after its old events expire",
        args=(
            2,
            (
                ("record", 1, "z"),
                ("most_frequent", 1),
                ("most_frequent", 3),
                ("record", 3, "z"),
                ("most_frequent", 3),
            ),
        ),
        expected=("z", None, "z"),
    ),
]
