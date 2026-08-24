from custom_practice.runner import Case


TEST_CASES = [
    Case(
        name="empty store and future versions are invisible",
        args=((
            ("get", "missing", 10),
            ("snapshot", 10),
            ("set", "future", "v1", 20, 5),
            ("get", "future", 19),
            ("snapshot", 19),
        ),),
        expected=(None, {}, None, {}),
    ),
    Case(
        name="latest version at or before the query wins",
        args=((
            ("set", "plan", "v1", 10, 100),
            ("set", "plan", "v2", 20, 100),
            ("get", "plan", 9),
            ("get", "plan", 10),
            ("get", "plan", 19),
            ("get", "plan", 20),
            ("get", "plan", 119),
            ("get", "plan", 120),
        ),),
        expected=(None, "v1", "v1", "v2", "v2", None),
    ),
    Case(
        name="TTL uses a half-open validity interval",
        args=((
            ("set", "session", "active", 10, 5),
            ("get", "session", 10),
            ("get", "session", 14),
            ("snapshot", 14),
            ("get", "session", 15),
            ("snapshot", 15),
        ),),
        expected=("active", "active", {"session": "active"}, None, {}),
    ),
    Case(
        name="out of order writes build the correct history",
        args=((
            ("set", "config", "v3", 30, 50),
            ("set", "config", "v1", 10, 50),
            ("set", "config", "v2", 20, 50),
            ("get", "config", 15),
            ("get", "config", 25),
            ("snapshot", 25),
            ("get", "config", 35),
        ),),
        expected=("v1", "v2", {"config": "v2"}, "v3"),
    ),
    Case(
        name="a second out of order sequence preserves point in time views",
        args=((
            ("set", "feature", "new", 40, 20),
            ("set", "feature", "old", 5, 50),
            ("set", "feature", "middle", 25, 50),
            ("snapshot", 20),
            ("snapshot", 30),
            ("snapshot", 45),
        ),),
        expected=(
            {"feature": "old"},
            {"feature": "middle"},
            {"feature": "new"},
        ),
    ),
    Case(
        name="expired latest version does not revive an older value",
        args=((
            ("set", "token", "old", 10, 100),
            ("set", "token", "new", 20, 5),
            ("get", "token", 24),
            ("get", "token", 25),
            ("get", "token", 50),
            ("snapshot", 50),
        ),),
        expected=("new", None, None, {}),
    ),
    Case(
        name="same key and timestamp replaces value and TTL",
        args=((
            ("set", "mode", "original", 10, 100),
            ("set", "mode", "replacement", 10, 3),
            ("get", "mode", 12),
            ("snapshot", 12),
            ("get", "mode", 13),
            ("snapshot", 13),
        ),),
        expected=("replacement", {"mode": "replacement"}, None, {}),
    ),
    Case(
        name="snapshot includes every valid key and omits expired keys",
        args=((
            ("set", "alpha", "a1", 10, 10),
            ("set", "beta", "b1", 12, 3),
            ("set", "gamma", "g1", 20, 10),
            ("snapshot", 14),
            ("snapshot", 15),
            ("snapshot", 20),
        ),),
        expected=(
            {"alpha": "a1", "beta": "b1"},
            {"alpha": "a1"},
            {"gamma": "g1"},
        ),
    ),
    Case(
        name="different keys keep independent out of order histories",
        args=((
            ("set", "alpha", "a2", 30, 100),
            ("set", "beta", "b2", 25, 100),
            ("set", "alpha", "a1", 10, 100),
            ("set", "beta", "b1", 5, 100),
            ("snapshot", 15),
            ("snapshot", 27),
            ("snapshot", 35),
        ),),
        expected=(
            {"alpha": "a1", "beta": "b1"},
            {"alpha": "a1", "beta": "b2"},
            {"alpha": "a2", "beta": "b2"},
        ),
    ),
    Case(
        name="empty strings remain distinguishable from missing keys",
        args=((
            ("set", "empty", "", 0, 2),
            ("get", "empty", 0),
            ("snapshot", 1),
            ("get", "empty", 2),
        ),),
        expected=("", {"empty": ""}, None),
    ),
]
