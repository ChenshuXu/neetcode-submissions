from custom_practice.runner import Case


TEST_CASES = [
    Case(
        name="basic least load with target index tie break",
        args=(2, 3, (
            "CONNECT,c1,u1,o1",
            "CONNECT,c2,u2,o2",
            "CONNECT,c3,u3,o3",
        )),
        expected=["c1,u1,1", "c2,u2,2", "c3,u3,1"],
    ),
    Case(
        name="object affinity overrides lower load target",
        args=(2, 4, (
            "CONNECT,c1,u1,shared",
            "CONNECT,c2,u2,o2",
            "CONNECT,c3,u3,o3",
            "CONNECT,c4,u4,shared",
        )),
        expected=["c1,u1,1", "c2,u2,2", "c3,u3,1", "c4,u4,1"],
    ),
    Case(
        name="affinity disappears after final disconnect",
        args=(2, 2, (
            "CONNECT,c1,u1,shared",
            "CONNECT,c2,u2,other",
            "DISCONNECT,c1,ignored,ignored",
            "CONNECT,c3,u3,shared",
        )),
        expected=["c1,u1,1", "c2,u2,2", "c3,u3,1"],
    ),
    Case(
        name="pinned full target rejects without moving object",
        args=(2, 1, (
            "CONNECT,c1,u1,shared",
            "CONNECT,c2,u2,shared",
            "CONNECT,c3,u3,other",
        )),
        expected=["c1,u1,1", "c3,u3,2"],
    ),
    Case(
        name="duplicate ID unknown disconnect and all full are no ops",
        args=(1, 1, (
            "CONNECT,c1,u1,o1",
            "CONNECT,c1,u2,o2",
            "CONNECT,c2,u2,o2",
            "DISCONNECT,missing,x,y",
        )),
        expected=["c1,u1,1"],
    ),
    Case(
        name="shutdown removes all before least load reroutes",
        args=(3, 3, (
            "CONNECT,c1,u1,o1",
            "CONNECT,c2,u2,o2",
            "CONNECT,c3,u3,o3",
            "CONNECT,c4,u4,o4",
            "SHUTDOWN,1",
        )),
        expected=[
            "c1,u1,1", "c2,u2,2", "c3,u3,3", "c4,u4,1",
            "c1,u1,2", "c4,u4,3",
        ],
    ),
    Case(
        name="shutdown rebuilds affinity during ordered reroute",
        args=(3, 3, (
            "CONNECT,a,u1,shared",
            "CONNECT,b,u2,shared",
            "SHUTDOWN,1",
        )),
        expected=["a,u1,1", "b,u2,1", "a,u1,2", "b,u2,2"],
    ),
    Case(
        name="failed shutdown reroute drops connection then restores target",
        args=(2, 1, (
            "CONNECT,c1,u1,o1",
            "CONNECT,c2,u2,o2",
            "SHUTDOWN,1",
            "CONNECT,c3,u3,o1",
        )),
        expected=["c1,u1,1", "c2,u2,2", "c3,u3,1"],
    ),
    Case(
        name="shutdown uses lexicographic connection ID order",
        args=(3, 3, (
            "CONNECT,c2,u2,o2",
            "CONNECT,x,u0,anchor",
            "CONNECT,y,u0,anchor2",
            "CONNECT,c10,u10,o10",
            "SHUTDOWN,1",
        )),
        expected=[
            "c2,u2,1", "x,u0,2", "y,u0,3", "c10,u10,1",
            "c10,u10,2", "c2,u2,3",
        ],
    ),
]
