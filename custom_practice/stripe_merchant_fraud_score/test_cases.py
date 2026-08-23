from custom_practice.runner import Case


TEST_CASES = [
    Case(
        name="amount repeat and hourly rules accumulate",
        args=(
            (
                "2026-01-01T10:00,t1,m1,c1,100",
                "2026-01-01T10:10,t2,m1,c1,150",
                "2026-01-01T10:20,t3,m1,c1,10",
            ),
            ("m1,10", "m2,5"),
            (
                "AMOUNT,100,2",
                "CUSTOMER_REPEAT,3,4",
                "HOURLY_COUNT,2,3",
            ),
        ),
        expected=["m1,30.00", "m2,5.00"],
    ),
    Case(
        name="amount threshold is strict greater than",
        args=(
            (
                "2026-01-01T10:00,t1,m,c,50",
                "2026-01-01T10:01,t2,m,c,50.01",
            ),
            ("m,8",),
            ("AMOUNT,50,1.5",),
        ),
        expected=["m,12.00"],
    ),
    Case(
        name="repeat rule applies at threshold and every later event",
        args=(
            (
                "2026-01-01T01:00,t1,m,c,1",
                "2026-01-01T02:00,t2,m,c,1",
                "2026-01-01T03:00,t3,m,c,1",
                "2026-01-01T04:00,t4,m,c,1",
            ),
            ("m,0",),
            ("CUSTOMER_REPEAT,3,2.5",),
        ),
        expected=["m,5.00"],
    ),
    Case(
        name="hour bucket resets at hour boundary",
        args=(
            (
                "2026-01-01T10:59,t1,m,a,1",
                "2026-01-01T10:59,t2,m,b,1",
                "2026-01-01T11:00,t3,m,c,1",
                "2026-01-01T11:01,t4,m,d,1",
            ),
            ("m,1",),
            ("HOURLY_COUNT,2,3",),
        ),
        expected=["m,7.00"],
    ),
    Case(
        name="rule list order is observable",
        args=(("2026-01-01T10:00,t,m,c,5",), ("m,10",), (
            "CUSTOMER_REPEAT,1,5",
            "AMOUNT,0,2",
        )),
        expected=["m,30.00"],
    ),
    Case(
        name="multiple matching rules of one type all apply",
        args=(("2026-01-01T10:00,t,m,c,20",), ("m,2",), (
            "AMOUNT,5,2",
            "AMOUNT,10,3",
        )),
        expected=["m,12.00"],
    ),
    Case(
        name="merchant output is alphabetical with two decimals",
        args=((), ("z,1.2", "a,0", "m,3.456"), ()),
        expected=["a,0.00", "m,3.46", "z,1.20"],
    ),
]
