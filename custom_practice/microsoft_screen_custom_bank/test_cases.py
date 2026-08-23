from custom_practice.runner import Case


RAISES_VALUE_ERROR = "<raises ValueError>"


TEST_CASES = {
    "tagged_sequence_assembly": [
        Case(name="empty input", args=((),), expected=[]),
        Case(
            name="unordered single chain",
            args=(
                (
                    ("s2", "b", "c", "B"),
                    ("s1", "a", "b", "A"),
                    ("s3", "c", "d", "C"),
                ),
            ),
            expected=[(("s1", "s2", "s3"), "ABC")],
        ),
        Case(
            name="multiple chains sorted by first id",
            args=(
                (
                    ("z2", "y", "z", "Y2"),
                    ("a2", "b", "c", "A2"),
                    ("z1", "x", "y", "Y1"),
                    ("a1", "a", "b", "A1"),
                ),
            ),
            expected=[
                (("a1", "a2"), "A1A2"),
                (("z1", "z2"), "Y1Y2"),
            ],
        ),
        Case(
            name="single fragment with empty payload",
            args=((("only", "start", "end", ""),),),
            expected=[(("only",), "")],
        ),
        Case(
            name="duplicate sequence id is invalid",
            args=(
                (
                    ("dup", "a", "b", "A"),
                    ("dup", "b", "c", "B"),
                ),
            ),
            expected=RAISES_VALUE_ERROR,
        ),
        Case(
            name="branching start tag is invalid",
            args=(
                (
                    ("s1", "a", "b", "A"),
                    ("s2", "a", "c", "B"),
                ),
            ),
            expected=RAISES_VALUE_ERROR,
        ),
        Case(
            name="merging end tag is invalid",
            args=(
                (
                    ("s1", "a", "c", "A"),
                    ("s2", "b", "c", "B"),
                ),
            ),
            expected=RAISES_VALUE_ERROR,
        ),
        Case(
            name="directed cycle is invalid",
            args=(
                (
                    ("s1", "a", "b", "A"),
                    ("s2", "b", "a", "B"),
                ),
            ),
            expected=RAISES_VALUE_ERROR,
        ),
    ],
    "bidirectional_movie_index": [
        Case(
            name="one user has sorted movies",
            args=(
                (
                    ("add", "u1", "m2"),
                    ("add", "u1", "m1"),
                    ("movies_for_user", "u1"),
                ),
            ),
            expected=(("m1", "m2"),),
        ),
        Case(
            name="one movie has sorted users",
            args=(
                (
                    ("add", "u2", "m1"),
                    ("add", "u1", "m1"),
                    ("users_for_movie", "m1"),
                ),
            ),
            expected=(("u1", "u2"),),
        ),
        Case(
            name="duplicate add is idempotent",
            args=(
                (
                    ("add", "u1", "m1"),
                    ("add", "u1", "m1"),
                    ("movies_for_user", "u1"),
                    ("users_for_movie", "m1"),
                ),
            ),
            expected=(("m1",), ("u1",)),
        ),
        Case(
            name="missing user and movie return empty",
            args=(
                (
                    ("movies_for_user", "missing-user"),
                    ("users_for_movie", "missing-movie"),
                ),
            ),
            expected=((), ()),
        ),
        Case(
            name="relationships stay isolated",
            args=(
                (
                    ("add", "u1", "m1"),
                    ("add", "u1", "m2"),
                    ("add", "u2", "m2"),
                    ("movies_for_user", "u2"),
                    ("users_for_movie", "m1"),
                    ("users_for_movie", "m2"),
                ),
            ),
            expected=(("m2",), ("u1",), ("u1", "u2")),
        ),
        Case(
            name="queries do not create relationships",
            args=(
                (
                    ("movies_for_user", "u1"),
                    ("users_for_movie", "m1"),
                    ("movies_for_user", "u1"),
                ),
            ),
            expected=((), (), ()),
        ),
    ],
    "extensible_calculator": [
        Case(name="multiplication before addition", args=("2+3*4",), expected=14),
        Case(name="multiple multiplication groups", args=("2*3+4*5",), expected=26),
        Case(name="spaces and multi digit values", args=(" 12 + 3 * 4 + 5 ",), expected=29),
        Case(name="single number and leading zeros", args=("007",), expected=7),
        Case(name="zero multiplication", args=("0*99+8",), expected=8),
        Case(name="invalid empty expression", args=("",), expected=RAISES_VALUE_ERROR),
        Case(name="invalid trailing operator", args=("2+3*",), expected=RAISES_VALUE_ERROR),
        Case(name="invalid consecutive operators", args=("2++3",), expected=RAISES_VALUE_ERROR),
        Case(name="invalid unsupported parentheses", args=("(2+3)*4",), expected=RAISES_VALUE_ERROR),
    ],
    "find_work_schedules": [
        Case(
            name="two unknown days",
            args=(3, 2, "??"),
            expected=["12", "21"],
        ),
        Case(
            name="fixed middle day and lexicographic order",
            args=(5, 3, "?2?"),
            expected=["023", "122", "221", "320"],
        ),
        Case(name="fully fixed valid schedule", args=(6, 3, "123"), expected=["123"]),
        Case(name="fully fixed wrong total", args=(5, 3, "123"), expected=[]),
        Case(name="no solution within daily limit", args=(10, 2, "??"), expected=[]),
        Case(name="zero daily limit", args=(0, 0, "??"), expected=["00"]),
        Case(
            name="invalid fixed digit above daily limit",
            args=(3, 2, "3?"),
            expected=RAISES_VALUE_ERROR,
        ),
        Case(
            name="invalid pattern character",
            args=(3, 2, "?x"),
            expected=RAISES_VALUE_ERROR,
        ),
        Case(
            name="invalid negative total",
            args=(-1, 2, "??"),
            expected=RAISES_VALUE_ERROR,
        ),
    ],
    "shortest_weighted_string": [
        Case(name="zero target", args=(0,), expected=""),
        Case(name="single a weight", args=(1,), expected="a"),
        Case(name="single b weight", args=(3,), expected="b"),
        Case(name="mixed a and b", args=(4,), expected="ab"),
        Case(name="repeated lower weights", args=(11,), expected="aabbb"),
        Case(name="single c weight", args=(12,), expected="c"),
        Case(name="mixed b and c", args=(15,), expected="bc"),
        Case(name="single d weight", args=(60,), expected="d"),
        Case(name="factorial weight mixture", args=(75,), expected="bcd"),
        Case(name="single e weight", args=(360,), expected="e"),
        Case(name="invalid negative target", args=(-1,), expected=RAISES_VALUE_ERROR),
    ],
    "two_minimum_values": [
        Case(name="unsorted distinct values", args=((3, 1, 2),), expected=(1, 2)),
        Case(name="duplicate minimum values", args=((1, 1),), expected=(1, 1)),
        Case(name="negative values", args=((-5, -2, -9),), expected=(-9, -5)),
        Case(name="descending values", args=((9, 7, 5, 3),), expected=(3, 5)),
        Case(name="already sorted values", args=((1, 2, 3, 4),), expected=(1, 2)),
        Case(name="duplicate second minimum", args=((0, 2, 2, 5),), expected=(0, 2)),
        Case(name="invalid empty input", args=((),), expected=RAISES_VALUE_ERROR),
        Case(name="invalid single value", args=((7,),), expected=RAISES_VALUE_ERROR),
    ],
    "distinct_nonempty_subsequences": [
        Case(name="empty string", args=("",), expected=[]),
        Case(name="single character", args=("a",), expected=["a"]),
        Case(name="two distinct characters", args=("ab",), expected=["a", "ab", "b"]),
        Case(name="duplicate characters are deduplicated", args=("aa",), expected=["a", "aa"]),
        Case(
            name="three distinct characters",
            args=("abc",),
            expected=["a", "ab", "abc", "ac", "b", "bc", "c"],
        ),
        Case(
            name="duplicate character in separated positions",
            args=("aba",),
            expected=["a", "aa", "ab", "aba", "b", "ba"],
        ),
        Case(
            name="all repeated characters",
            args=("aaa",),
            expected=["a", "aa", "aaa"],
        ),
    ],
}
