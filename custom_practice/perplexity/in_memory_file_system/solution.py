"""Perplexity-inspired practice. Read README.md; implement one stage at a time.

All storage stays in memory. These are local practice contracts, not a recovered
verbatim interview prompt. No reference solution is included.
"""

from __future__ import annotations


class FileSystem:
    def __init__(self):
        # Initialize an empty root directory and, for Part 3, a current directory.
        pass

    # Part 1
    def mkdir(self, path: str) -> bool:
        raise NotImplementedError

    def touch(self, path: str) -> bool:
        raise NotImplementedError

    def ls(self, path: str) -> list[str] | None:
        raise NotImplementedError

    # Part 2: keep Part 1 working.
    def rm(self, path: str) -> bool:
        raise NotImplementedError

    def rmdir(self, path: str) -> bool:
        raise NotImplementedError

    # Part 3: extend all earlier operations to support relative paths.
    def cd(self, path: str) -> bool:
        raise NotImplementedError

    # Optional input variant, NOT a claimed interview Part 4.
    def execute(self, command: str):
        raise NotImplementedError
