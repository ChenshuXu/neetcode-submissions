from custom_practice.runner import Case


TEST_CASES = [
    Case(
        name="start already equals target",
        args=({}, "Home", "Home"),
        expected=["Home"],
    ),
    Case(
        name="direct link",
        args=(
            {
                "Home": ("Target",),
            },
            "Home",
            "Target",
        ),
        expected=["Home", "Target"],
    ),
    Case(
        name="shorter path beats first longer branch",
        args=(
            {
                "Home": ("A", "B"),
                "A": ("C",),
                "B": ("Target",),
                "C": ("Target",),
            },
            "Home",
            "Target",
        ),
        expected=["Home", "B", "Target"],
    ),
    Case(
        name="cycle and self link terminate",
        args=(
            {
                "A": ("A", "B"),
                "B": ("C", "A"),
                "C": ("B", "Target"),
            },
            "A",
            "Target",
        ),
        expected=["A", "B", "C", "Target"],
    ),
    Case(
        name="duplicate links do not duplicate work",
        args=(
            {
                "A": ("B", "B", "C", "B"),
                "B": ("Target",),
                "C": ("Target",),
            },
            "A",
            "Target",
        ),
        expected=["A", "B", "Target"],
    ),
    Case(
        name="callback order breaks equal length tie",
        args=(
            {
                "Start": ("Right", "Left"),
                "Left": ("Target",),
                "Right": ("Target",),
            },
            "Start",
            "Target",
        ),
        expected=["Start", "Right", "Target"],
    ),
    Case(
        name="target may be a page with no outgoing entry",
        args=(
            {
                "A": ("B",),
                "B": ("Target",),
            },
            "A",
            "Target",
        ),
        expected=["A", "B", "Target"],
    ),
    Case(
        name="unreachable target",
        args=(
            {
                "A": ("B",),
                "B": ("C",),
                "C": ("A",),
                "Other": ("Target",),
            },
            "A",
            "Target",
        ),
        expected=[],
    ),
    Case(
        name="start page has no outgoing links",
        args=({}, "Lonely", "Target"),
        expected=[],
    ),
]
