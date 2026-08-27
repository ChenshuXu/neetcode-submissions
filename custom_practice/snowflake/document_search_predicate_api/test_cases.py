from custom_practice.runner import Case


TEST_CASES = [
    Case(
        name="empty store answers every predicate shape",
        args=((
            ("search", None),
            ("search", ("contains", "body", "alpha")),
            ("search", ("not", ("contains", "body", "alpha"))),
            ("search", ("and",)),
            ("delete", "missing.txt"),
        ),),
        expected=((), (), (), (), False),
    ),
    Case(
        name="contains matches a whole word and eq matches the whole value",
        args=((
            ("insert", "clean_room.txt", {"title": "Snowflake Data Clean Room", "owner": "newton"}),
            ("insert", "sharing.txt", {"title": "Data Sharing", "owner": "atindra"}),
            ("search", ("contains", "title", "Data")),
            ("search", ("contains", "title", "Dat")),
            ("search", ("eq", "title", "Data Sharing")),
            ("search", ("eq", "title", "Data")),
            ("search", ("eq", "owner", "newton")),
        ),),
        expected=(
            ("clean_room.txt", "sharing.txt"),
            (),
            ("sharing.txt",),
            (),
            ("clean_room.txt",),
        ),
    ),
    Case(
        name="matching is case sensitive",
        args=((
            ("insert", "notes.txt", {"body": "Alpha beta"}),
            ("search", ("contains", "body", "Alpha")),
            ("search", ("contains", "body", "alpha")),
            ("search", ("eq", "body", "alpha beta")),
        ),),
        expected=(("notes.txt",), (), ()),
    ),
    Case(
        name="a missing field matches nothing and its negation matches",
        args=((
            ("insert", "tagged.txt", {"body": "alpha", "tag": "internal"}),
            ("insert", "untagged.txt", {"body": "alpha"}),
            ("search", ("contains", "tag", "internal")),
            ("search", ("contains", "author", "newton")),
            ("search", ("not", ("contains", "tag", "internal"))),
            ("search", ("and", ("contains", "body", "alpha"), ("not", ("eq", "tag", "internal")))),
        ),),
        expected=(("tagged.txt",), (), ("untagged.txt",), ("untagged.txt",)),
    ),
    Case(
        name="multiple conditions combine and nest",
        args=((
            ("insert", "d1.txt", {"body": "alpha beta", "owner": "newton"}),
            ("insert", "d2.txt", {"body": "beta gamma", "owner": "newton"}),
            ("insert", "d3.txt", {"body": "alpha gamma", "owner": "atindra"}),
            ("search", ("and", ("contains", "body", "alpha"), ("contains", "body", "beta"))),
            ("search", ("or", ("contains", "body", "alpha"), ("contains", "body", "gamma"))),
            (
                "search",
                (
                    "and",
                    ("eq", "owner", "newton"),
                    ("or", ("contains", "body", "gamma"), ("contains", "body", "delta")),
                ),
            ),
            ("search", ("not", ("or", ("contains", "body", "alpha"), ("eq", "owner", "atindra")))),
            ("search", ("and",)),
            ("search", ("or",)),
        ),),
        expected=(
            ("d1.txt",),
            ("d1.txt", "d2.txt", "d3.txt"),
            ("d2.txt",),
            ("d2.txt",),
            ("d1.txt", "d2.txt", "d3.txt"),
            (),
        ),
    ),
    Case(
        name="re-inserting a filename replaces its content and keeps its position",
        args=((
            ("insert", "one.txt", {"body": "alpha"}),
            ("insert", "two.txt", {"body": "beta"}),
            ("insert", "one.txt", {"body": "gamma"}),
            ("search", ("contains", "body", "alpha")),
            ("search", ("contains", "body", "gamma")),
            ("search", None),
        ),),
        expected=((), ("one.txt",), ("one.txt", "two.txt")),
    ),
    Case(
        name="delete retracts the document from postings and from the NOT universe",
        args=((
            ("insert", "keep.txt", {"body": "alpha"}),
            ("insert", "drop.txt", {"body": "alpha beta"}),
            ("delete", "drop.txt"),
            ("delete", "drop.txt"),
            ("search", ("contains", "body", "alpha")),
            ("search", ("not", ("contains", "body", "beta"))),
            ("search", None),
        ),),
        expected=(True, False, ("keep.txt",), ("keep.txt",), ("keep.txt",)),
    ),
    Case(
        name="a filename reinserted after delete is a new document at the end",
        args=((
            ("insert", "first.txt", {"body": "x"}),
            ("insert", "second.txt", {"body": "x"}),
            ("delete", "first.txt"),
            ("insert", "first.txt", {"body": "x"}),
            ("search", None),
            ("search", ("contains", "body", "x")),
        ),),
        expected=(True, ("second.txt", "first.txt"), ("second.txt", "first.txt")),
    ),
    Case(
        name="repeated words and shared words across fields never duplicate a filename",
        args=((
            ("insert", "dup.txt", {"title": "alpha alpha", "body": "alpha"}),
            ("search", ("contains", "title", "alpha")),
            ("search", ("or", ("contains", "title", "alpha"), ("contains", "body", "alpha"))),
            ("search", ("contains", "body", "alpha")),
        ),),
        expected=(("dup.txt",), ("dup.txt",), ("dup.txt",)),
    ),
    Case(
        name="whitespace runs collapse into words and an empty value has none",
        args=((
            ("insert", "ws.txt", {"body": "  alpha   beta  ", "note": ""}),
            ("search", ("contains", "body", "beta")),
            ("search", ("eq", "body", "  alpha   beta  ")),
            ("search", ("eq", "note", "")),
            ("search", ("contains", "note", "")),
        ),),
        expected=(("ws.txt",), ("ws.txt",), ("ws.txt",), ()),
    ),
]
