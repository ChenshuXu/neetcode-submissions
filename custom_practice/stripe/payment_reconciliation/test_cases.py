from custom_practice.runner import Case


TEST_CASES = [
    Case(
        name="exact records produce no discrepancy",
        args=(("t1,m1,10.00,USD,SETTLED",), ("t1,m1,10,USD,SETTLED",)),
        expected=[],
    ),
    Case(
        name="missing records are classified on each side",
        args=(("t2,m,5,USD,SETTLED",), ("t0,m,5,USD,SETTLED",)),
        expected=["t0,MISSING_INTERNAL", "t2,MISSING_PROCESSOR"],
    ),
    Case(
        name="single status mismatch names field",
        args=(("t1,m,5,USD,PENDING",), ("t1,m,5,USD,SETTLED",)),
        expected=["t1,MISMATCH,status"],
    ),
    Case(
        name="multiple mismatches use fixed field order",
        args=(("t1,m1,5,USD,PENDING",), ("t1,m2,7,EUR,SETTLED",)),
        expected=["t1,MISMATCH,merchant_id|amount|currency|status"],
    ),
    Case(
        name="decimal representations compare numerically",
        args=(("t1,m,1.0,USD,SETTLED",), ("t1,m,1.000,USD,SETTLED",)),
        expected=[],
    ),
    Case(
        name="case remains significant for text fields",
        args=(("t1,m,1,usd,settled",), ("t1,m,1,USD,SETTLED",)),
        expected=["t1,MISMATCH,currency|status"],
    ),
    Case(
        name="mixed discrepancies sort by transaction ID",
        args=((
            "z,m,1,USD,SETTLED",
            "a,m,1,USD,PENDING",
            "m,m,1,USD,SETTLED",
        ), (
            "a,m,2,USD,PENDING",
            "b,m,1,USD,SETTLED",
            "m,m,1,USD,SETTLED",
        )),
        expected=[
            "a,MISMATCH,amount",
            "b,MISSING_INTERNAL",
            "z,MISSING_PROCESSOR",
        ],
    ),
    Case(
        name="both empty inputs return empty output",
        args=((), ()),
        expected=[],
    ),
]
