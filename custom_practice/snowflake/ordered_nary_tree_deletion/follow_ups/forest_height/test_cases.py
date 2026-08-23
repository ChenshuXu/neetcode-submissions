from custom_practice.snowflake.ordered_nary_tree_deletion.models import t
from custom_practice.runner import Case


TEST_CASES = [
    Case(name="empty forest", args=((),), expected=0),
    Case(name="single leaf root", args=((t(1),),), expected=1),
    Case(
        name="one tree with four levels",
        args=((t(1, t(2, t(3, t(4)))),),),
        expected=4,
    ),
    Case(
        name="several roots with different heights",
        args=((t(1, t(2)), t(10, t(11, t(12, t(13)))), t(20)),),
        expected=4,
    ),
    Case(
        name="wide forest does not increase height",
        args=((t(1, t(2), t(3), t(4)), t(5, t(6), t(7))),),
        expected=2,
    ),
    Case(
        name="forest produced by root deletion",
        args=((t(2, t(4)), t(3, t(5), t(6))),),
        expected=2,
    ),
]
