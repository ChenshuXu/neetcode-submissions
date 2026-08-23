from custom_practice.runner import Case


TEST_CASES = [
    Case(
        name="empty counter",
        args=((
            ("getHits", 1),
            ("getHits", 500),
        ),),
        expected=(0, 0),
    ),
    Case(
        name="canonical example and exact 300-second boundary",
        args=((
            ("hit", 1),
            ("hit", 2),
            ("hit", 3),
            ("getHits", 4),
            ("hit", 300),
            ("getHits", 300),
            ("getHits", 301),
        ),),
        expected=(3, 4, 3),
    ),
    Case(
        name="many hits in the same second",
        args=((
            ("hit", 10),
            ("hit", 10),
            ("hit", 10),
            ("hit", 10),
            ("hit", 10),
            ("getHits", 10),
            ("getHits", 309),
            ("getHits", 310),
        ),),
        expected=(5, 5, 0),
    ),
    Case(
        name="new hits arrive as old hits expire",
        args=((
            ("hit", 1),
            ("hit", 300),
            ("hit", 300),
            ("getHits", 300),
            ("hit", 301),
            ("getHits", 301),
        ),),
        expected=(3, 3),
    ),
    Case(
        name="queries advance time without writes",
        args=((
            ("hit", 1),
            ("hit", 150),
            ("getHits", 150),
            ("getHits", 300),
            ("getHits", 301),
            ("getHits", 450),
        ),),
        expected=(2, 2, 1, 0),
    ),
    Case(
        name="calls may share a timestamp",
        args=((
            ("hit", 20),
            ("getHits", 20),
            ("hit", 20),
            ("getHits", 20),
            ("getHits", 319),
            ("getHits", 320),
        ),),
        expected=(1, 2, 2, 0),
    ),
]
