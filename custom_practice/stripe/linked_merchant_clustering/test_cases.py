from custom_practice.runner import Case


TEST_CASES = [
    Case(
        name="transitive links persist for all three days",
        args=(
            (
                "m1,email:a,3",
                "m2,email:a,3",
                "m2,device:x,3",
                "m3,device:x,3",
                "solo,phone:z,3",
            ),
            (),
            (),
        ),
        expected=[
            "Day 1:",
            "m2:[m1,m2,m3]",
            "Day 2:",
            "m2:[m1,m2,m3]",
            "Day 3:",
            "m2:[m1,m2,m3]",
        ],
    ),
    Case(
        name="expiring bridge splits one cluster into two",
        args=(
            (
                "a,left,3",
                "b,left,3",
                "b,bridge,1",
                "c,bridge,1",
                "c,right,3",
                "d,right,3",
            ),
            (),
            (),
        ),
        expected=[
            "Day 1:",
            "b:[a,b,c,d]",
            "Day 2:",
            "b:[a,b]",
            "c:[c,d]",
            "Day 3:",
            "b:[a,b]",
            "c:[c,d]",
        ],
    ),
    Case(
        name="gaining merchant keeps lower-degree old pin",
        args=(
            (
                "a,ab,3",
                "b,ab,3",
            ),
            (
                "b,bc,2",
                "c,bc,2",
            ),
            (),
        ),
        expected=[
            "Day 1:",
            "a:[a,b]",
            "Day 2:",
            "a:[a,b,c]",
            "Day 3:",
            "a:[a,b,c]",
        ],
    ),
    Case(
        name="merge chooses old pin with higher current degree",
        args=(
            (
                "a,left,3",
                "b,left,3",
                "c,right,3",
                "d,right,3",
            ),
            (
                "b,bridge,2",
                "c,bridge,2",
            ),
            (),
        ),
        expected=[
            "Day 1:",
            "a:[a,b]",
            "c:[c,d]",
            "Day 2:",
            "c:[a,b,c,d]",
            "Day 3:",
            "c:[a,b,c,d]",
        ],
    ),
    Case(
        name="merge tie compares old pins not higher-degree non-pins",
        args=(
            (
                "a,left,3",
                "b,left,3",
                "c,right,3",
                "d,right,3",
            ),
            (
                "b,bridge,2",
                "d,bridge,2",
            ),
            (),
        ),
        expected=[
            "Day 1:",
            "a:[a,b]",
            "c:[c,d]",
            "Day 2:",
            "a:[a,b,c,d]",
            "Day 3:",
            "a:[a,b,c,d]",
        ],
    ),
    Case(
        name="old pin becomes isolated after split",
        args=(
            (
                "a,left,1",
                "b,left,1",
                "b,right,1",
                "c,right,1",
            ),
            (
                "a,new,2",
                "c,new,2",
            ),
            (),
        ),
        expected=[
            "Day 1:",
            "b:[a,b,c]",
            "Day 2:",
            "a:[a,c]",
            "Day 3:",
            "a:[a,c]",
        ],
    ),
    Case(
        name="duplicate records and shared attributes make one edge",
        args=(
            (
                "a,x,1",
                "a,x,1",
                "b,x,1",
                "a,y,1",
                "b,y,1",
            ),
            (
                "a,x,2",
                "b,x,1",
            ),
            (),
        ),
        expected=[
            "Day 1:",
            "a:[a,b]",
            "Day 2:",
            "a:[a,b]",
            "Day 3:",
        ],
    ),
    Case(
        name="cluster and member ordering is deterministic",
        args=(
            (
                "acct_2,large,1",
                "acct_10,large,1",
                "acct_3,large,1",
                "a2,small,1",
                "a1,small,1",
                "solo,alone,3",
            ),
            (),
            (),
        ),
        expected=[
            "Day 1:",
            "acct_10:[acct_10,acct_2,acct_3]",
            "a1:[a1,a2]",
            "Day 2:",
            "Day 3:",
        ],
    ),
    Case(
        name="simultaneous split and merge uses pins still present",
        args=(
            (
                "a,left,1",
                "b,left,1",
                "b,stable,3",
                "c,stable,3",
                "d,pair,3",
                "e,pair,3",
            ),
            (
                "a,join,2",
                "e,join,2",
            ),
            (),
        ),
        expected=[
            "Day 1:",
            "b:[a,b,c]",
            "d:[d,e]",
            "Day 2:",
            "d:[a,d,e]",
            "b:[b,c]",
            "Day 3:",
            "d:[a,d,e]",
            "b:[b,c]",
        ],
    ),
]
