from custom_practice.runner import Case


TEST_CASES = [
    Case(
        name="count threshold includes equality",
        args=(("m1,retail,COUNT,2", "m2,travel,COUNT,1"), ("F",), ("OK",), (
            "CHARGE,c1,m1,10,F",
            "CHARGE,c2,m1,20,F",
        )),
        expected=["m1"],
    ),
    Case(
        name="ratio threshold includes equality",
        args=(("m,retail,RATIO,0.5",), ("F",), ("OK",), (
            "CHARGE,c1,m,10,F",
            "CHARGE,c2,m,10,OK",
        )),
        expected=["m"],
    ),
    Case(
        name="zero eligible denominator is never flagged",
        args=(("m,retail,RATIO,0",), ("F",), ("OK",), (
            "CHARGE,c1,m,10,UNKNOWN",
        )),
        expected=[],
    ),
    Case(
        name="fraud dispute can unflag count merchant",
        args=(("m,retail,COUNT,2",), ("F",), ("OK",), (
            "CHARGE,c1,m,10,F",
            "CHARGE,c2,m,10,F",
            "DISPUTE,c1",
        )),
        expected=[],
    ),
    Case(
        name="nonfraud dispute can raise fraud ratio",
        args=(("m,retail,RATIO,0.6",), ("F",), ("OK",), (
            "CHARGE,c1,m,10,F",
            "CHARGE,c2,m,10,OK",
            "DISPUTE,c2",
        )),
        expected=["m"],
    ),
    Case(
        name="duplicate charges and disputes are idempotent",
        args=(("m,retail,COUNT,1",), ("F",), ("OK",), (
            "CHARGE,c1,m,10,F",
            "CHARGE,c1,m,10,OK",
            "DISPUTE,c1",
            "DISPUTE,c1",
        )),
        expected=[],
    ),
    Case(
        name="unknown charge code does not enter denominator",
        args=(("m,retail,RATIO,0.75",), ("F",), ("OK",), (
            "CHARGE,c1,m,10,F",
            "CHARGE,c2,m,10,UNKNOWN",
        )),
        expected=["m"],
    ),
    Case(
        name="final flagged output is alphabetical",
        args=((
            "z,retail,COUNT,1",
            "a,retail,COUNT,1",
            "m,retail,COUNT,2",
        ), ("F",), ("OK",), (
            "CHARGE,c1,z,1,F",
            "CHARGE,c2,a,1,F",
            "CHARGE,c3,m,1,F",
        )),
        expected=["a", "z"],
    ),
]
