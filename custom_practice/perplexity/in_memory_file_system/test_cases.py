from custom_practice.runner import Case


TEST_CASES = [
    Case("core part1 empty root", [[]], args=([("ls", "/")],)),
    Case("core part1 create list and sort", [True, True, True, ["a", "z"], ["note"], ["note"]], args=([
        ("mkdir", "/z"), ("mkdir", "/a"), ("touch", "/a/note"),
        ("ls", "/"), ("ls", "/a"), ("ls", "/a/note"),
    ],)),
    Case("core part1 duplicates and type collisions", [True, False, False, True, True, False, ["d", "f"]], args=([
        ("mkdir", "/d"), ("mkdir", "/d"), ("touch", "/d"),
        ("touch", "/f"), ("touch", "/f"), ("mkdir", "/f"), ("ls", "/"),
    ],)),
    Case("core part1 missing parents create nothing", [False, False, None, []], args=([
        ("mkdir", "/missing/child"), ("touch", "/missing/file"),
        ("ls", "/missing"), ("ls", "/"),
    ],)),
    Case("core part1 file cannot be a parent", [True, False, False, None, ["f"]], args=([
        ("touch", "/f"), ("mkdir", "/f/d"), ("touch", "/f/x"),
        ("ls", "/f/x"), ("ls", "/"),
    ],)),
    Case("core part1 same name in different directories", [True, True, True, True, ["x"], ["x"], False, False], args=([
        ("mkdir", "/a"), ("mkdir", "/b"), ("touch", "/a/x"),
        ("mkdir", "/b/x"), ("ls", "/a"), ("ls", "/b"),
        ("mkdir", "/"), ("touch", "/"),
    ],)),
    Case("core part2 delete file and recreate as directory", [True, True, False, True, []], args=([
        ("touch", "/x"), ("rm", "/x"), ("rm", "/x"),
        ("mkdir", "/x"), ("ls", "/x"),
    ],)),
    Case("core part2 nonempty directory stays intact", [True, True, False, False, ["x"], True, True, []], args=([
        ("mkdir", "/d"), ("touch", "/d/x"), ("rmdir", "/d"),
        ("rm", "/d"), ("ls", "/d"), ("rm", "/d/x"),
        ("rmdir", "/d"), ("ls", "/"),
    ],)),
    Case("core part2 wrong type missing and protected root", [True, False, False, False, False, False, ["f"]], args=([
        ("touch", "/f"), ("rmdir", "/f"), ("rm", "/absent"),
        ("rmdir", "/absent"), ("rm", "/"), ("rmdir", "/"), ("ls", "/"),
    ],)),
    Case("core part2 remove nested empty directories", [True, True, False, True, True, []], args=([
        ("mkdir", "/a"), ("mkdir", "/a/b"), ("rmdir", "/a"),
        ("rmdir", "/a/b"), ("rmdir", "/a"), ("ls", "/"),
    ],)),
    Case("core part3 current directory affects earlier methods", [True, True, True, True, ["d", "x"], True, True, []], args=([
        ("mkdir", "/a"), ("cd", "/a"), ("touch", "x"), ("mkdir", "d"),
        ("ls", "."), ("rm", "x"), ("rmdir", "d"), ("ls", "/a"),
    ],)),
    Case("core part3 parents dots and repeated slashes", [True, True, True, True, True, ["f"], True, ["a"]], args=([
        ("mkdir", "/a"), ("mkdir", "/a/b"), ("cd", "//a//b/"),
        ("cd", ".."), ("touch", "./b/f"), ("ls", "b/./"),
        ("cd", "../../../"), ("ls", "."),
    ],)),
    Case("core part3 failed cd preserves current directory", [True, True, True, False, False, True, ["f", "stay"]], args=([
        ("mkdir", "/a"), ("cd", "/a"), ("touch", "f"),
        ("cd", "f"), ("cd", "/missing"), ("touch", "stay"), ("ls", "/a"),
    ],)),
    Case("core part3 do not erase unresolved segments", [True, True, True, False, None, False, ["f"]], args=([
        ("touch", "/f"), ("mkdir", "/a"), ("cd", "/a"),
        ("cd", "/f/.."), ("ls", "/missing/.."),
        ("touch", "/missing/../x"), ("ls", "/f"),
    ],)),
    Case("core part3 cannot remove current directory", [True, True, False, False, True, True, []], args=([
        ("mkdir", "/a"), ("cd", "/a"), ("rmdir", "."),
        ("rmdir", "/a"), ("cd", "/"), ("rmdir", "/a"), ("ls", "/"),
    ],)),
    Case("core part3 special targets and trailing slash", [True, ["f"], None, False, False, False, None], args=([
        ("touch", "/f"), ("ls", "/f/"), ("ls", "/f/."),
        ("mkdir", "/."), ("touch", "/.."), ("cd", "/f/."), ("ls", "/missing"),
    ],)),
    Case("variant command input reuses filesystem state", [True, True, True, ["f"], True, True, True, []], args=([
        ("execute", "mkdir /a"), ("execute", "cd /a"), ("execute", "touch f"),
        ("ls", "/a"), ("execute", "rm f"), ("execute", "cd /"),
        ("execute", "rmdir /a"), ("execute", "ls /"),
    ],)),
    Case("variant malformed commands leave state unchanged", [False, False, False, False, False, [], True, ["x"]], args=([
        ("execute", ""), ("execute", "pwd /"), ("execute", "touch"),
        ("execute", "touch /a /b"), ("execute", "execute /"), ("ls", "/"),
        ("execute", "  touch\t/x  "), ("execute", "ls /"),
    ],)),
]
