# Perplexity Q001 — In-Memory File System

Implement `FileSystem` in [solution.py](solution.py). The starter intentionally contains
no solution. Python 3.9+; standard library only. Do not access the real filesystem.

## Evidence boundary

The confirmed operation sequence is from [S-W3-002](https://www.1point3acres.com/bbs/thread-1183004-1-1.html):
Part 1 `mkdir/touch/ls`, Part 2 `rm/rmdir`, Part 3 `cd`.
[S-W3-001](https://www.1point3acres.com/bbs/thread-1188262-1-1.html) reports a class skeleton
and supplied tests, with no need to write a CLI runner.
[S-W3-005](https://www.1point3acres.com/bbs/thread-1182665-1-1.html) reports a command-line
parsing variant; that is an optional exercise below, not a claimed Part 4.

**Every signature, return value, path rule, error rule, example and test below is a
local practice assumption. These are not official or recovered interview tests.**
Part 4 `mv/cp` remains an unanswered comment and Part 5 is undisclosed, so neither is
invented here. Detailed research: [Q001 preparation](</Users/Newton/Documents/job search/projects/context/Interview/perplexity/perplexity-connector-platform-interview-prep-2026-09-22.md>).

## Prompt and common contract

Maintain files and directories in memory. A new instance contains only the root `/`.
Files are empty markers: there is no file-content API in this exercise.
A directory may contain files and directories, with unique names among its children.
Different instances must have independent state. Choose your own data structures.

- Inputs are strings. Direct method paths are nonempty. Names contain only ASCII
  letters, digits and underscores; `.` and `..` become special segments in Part 3.
- For Parts 1–2, inputs are absolute paths with a single slash between names, no
  trailing slash except `/`, and no `.` or `..`.
- Parents must already exist. Creation is **not recursive**.
- A failed operation returns the value below and leaves all state unchanged.
- No permissions, timestamps, symbolic links, persistence or concurrency are required.
- Local scale: at most 10,000 operations, 1,000 characters per path. After implementing,
  explain each operation's time and space cost, including sorting for `ls`.

## Part 1 — Creation and listing

| Method | Success | Failure / existing target |
| --- | --- | --- |
| `mkdir(path) -> bool` | Create one directory; return `True` | `False` if target exists, parent is missing, or an ancestor is a file |
| `touch(path) -> bool` | Create an empty file; return `True` | Existing file: `True`, no change. Existing directory, missing parent or file ancestor: `False` |
| `ls(path) -> list[str] \| None` | Directory: sorted immediate child names. File: `[basename]` | Missing target or a file used as an ancestor: `None` |

`mkdir('/')` and `touch('/')` return `False`. Listing an empty directory returns `[]`.

```python
fs = FileSystem()
fs.mkdir('/work')       # True
fs.touch('/work/b')     # True
fs.touch('/work/a')     # True
fs.ls('/work')          # ['a', 'b']
fs.mkdir('/absent/new') # False; /absent must not be created
```

## Part 2 — Deletion

Keep all earlier behavior working.

- `rm(path) -> bool`: delete an existing file and return `True`; a directory or
  missing target returns `False`.
- `rmdir(path) -> bool`: delete an existing **empty** directory and return `True`;
  a file, missing target, nonempty directory or root returns `False`.
- Deletion is never recursive. After successful deletion, the name can be reused
  for either a file or a directory.

## Part 3 — Current directory and path traversal

Add `cd(path) -> bool`. Initially the current directory is `/`. A successful `cd`
selects an existing directory and returns `True`; any failure returns `False` and
preserves the current directory. Extend **all** earlier methods:

- An initial `/` starts at root; otherwise start at the current directory.
- Repeated and trailing slashes are ignored. `.` stays in the current resolved
  directory; `..` moves to its parent, staying at root if already there.
- Resolve left to right through existing directories. Do not discard a missing or
  file segment simply because a later segment is `..`: `/missing/../x` is invalid,
  and `/file/..` is invalid if `/file` is a file. `/file/.` is invalid too.
- A plain trailing slash does not require a directory: `ls('/file/')` returns
  `['file']`, consistent with ignoring trailing slashes in this local contract.
- Creation applies to the final ordinary name only. A final `.` or `..` denotes an
  existing directory, so `mkdir` and `touch` return `False` for such targets.
- `rmdir` must also reject the current directory, even when empty. An ancestor of
  the current directory is nonempty and is already protected by Part 2.

```python
fs.mkdir('/work')       # True on a fresh instance
fs.cd('/work')          # True
fs.touch('note')        # True
fs.ls('.')             # ['note']
fs.cd('/missing')       # False; still in /work
fs.cd('..')             # True; now at /
fs.ls('/work/note')     # ['note']
```

## Optional variant — Command input

Implement `execute(command)` on the same instance. Supported commands are exactly
`mkdir`, `touch`, `ls`, `rm`, `rmdir`, and `cd`, each with exactly one path argument.
Split on whitespace; leading/trailing whitespace and tabs are allowed. No quoting,
spaces in names, flags, pipelines or shell execution. Unknown commands or a token
count other than two return `False` without changing state. Otherwise return the
corresponding method's result. Direct method calls and commands share state.

## Run the visible tests

From this directory:

```bash
python3 run_tests.py --list
python3 run_tests.py --case part1
python3 run_tests.py --case part2
python3 run_tests.py --case part3
python3 run_tests.py --case core
python3 run_tests.py --case variant
python3 run_tests.py
```

Stage filters run only that stage's cases; rerun earlier stages after each change.
`--case core` runs all three stages together without the optional command variant.
Each case starts with a fresh instance and compares every operation's return value.
The unchanged starter is expected to fail with `NotImplementedError`.

These visible tests check representative behavior, not exhaustive correctness or
interview readiness. Add your own adversarial cases while practicing.
