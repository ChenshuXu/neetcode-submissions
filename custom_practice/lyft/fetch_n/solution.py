"""Lyft Q004 — Stateful fetch_n over a Paginated API

Description
-----------
You are given fetch(page), which returns (items, next_page).
Implement a class with fetch_n(n). Each call returns up to n items in order.
Continue from where the previous call stopped, including unused items from
an already fetched page. Fetch more pages as needed. At the end, return any
remaining items; later calls return [].

You must use fetch(page); do not access the source's page dictionary directly.
This is not "fetch all pages" and it is not independently fetching n items
from the beginning on each call.

Input assumptions — confirm verbally; no runtime input checks
------------------------------------------------------------
- n is a nonnegative integer; fetch_n(0) returns [] without fetching.
- first_page is a valid token, or None for an already exhausted source.
- fetch(page) returns a list of items and the next token, or None at EOF.
- Tokens are opaque. Follow the returned token; do not add 1 to a page number.
  0 is a valid token. Only None means there are no more pages.
- Pages may be empty and still have a next token. A short page is not EOF.
- Items may repeat. Preserve duplicates and source order.
- The token chain is finite and acyclic; page contents are stable.
- A reader is used sequentially, with no concurrent calls or source updates.

Example
-------
Pages:
    0 -> ([10, 20, 30], 5)
    5 -> ([], 9)
    9 -> ([40, 50], None)

Calls and outputs on the SAME reader:
    fetch_n(2) -> [10, 20]       # Keep 30 for the next call.
    fetch_n(2) -> [30, 40]       # Follow the empty page; keep 50.
    fetch_n(5) -> [50]           # EOF with fewer than requested.
    fetch_n(1) -> []

LC158 connection
----------------
Read N Characters Given read4 II - Call Multiple Times requires preserving
unread characters across calls. Here a variable-sized page replaces read4's
batch, and next_page replaces the hidden file position. LC158 writes into
buf and returns a count; this exercise returns an item list. Its read4 EOF
rule does not imply that an empty pagination page is terminal.

Optional follow-up: transient failures
-------------------------------------
The secondary report mentions retrying fetch without corrupting continuation.
Practice choices: retry only TimeoutError, at most max_attempts per page
(default 1 = no retry). The same token may safely be fetched again.
No sleep/backoff is simulated. A production retry delay is discussion only.

If retries are exhausted, propagate the error. That fetch_n call returns no
items, so none of its items should be consumed. Previously fetched items
remain buffered, and the failed page token is unchanged. A later call can
continue without skipping or duplicating an item.

Approach / invariant
--------------------
The buffer contains exactly the items fetched but not yet returned, in order.
next_page points to the first page not successfully fetched, or None.
First fill the buffer; only then remove items for the response. This avoids
losing partial results if a later page fails during the same fetch_n call.

Time per call: O(k + m), excluding upstream latency/retries, where k is the
number of items returned and m is the number of items loaded from new pages.
Also count p page calls: empty pages still cost calls, so O(k + m + p).
Each successfully fetched item is buffered and removed once across calls.
Space: O(N + B) peak including the output, where N is the largest request
so far and B is the largest page size. A failed call can retain its buffered
prefix even if the next call requests fewer items.

Source requirements vs chosen semantics are detailed in README.md.
"""

from collections import deque


class Fetcher:
    def __init__(self, fetch, first_page=0, max_attempts=1):
        self.fetch = fetch
        self.next_page = first_page
        self.buffer = deque()
        self.max_attempts = max_attempts  # 口头确认：正整数；1 表示不重试。

    def _fetch_page(self):
        for attempt in range(self.max_attempts):
            try:
                return self.fetch(self.next_page)
            except TimeoutError:
                if attempt == self.max_attempts - 1:
                    raise

    def fetch_n(self, n):
        # 先读够再交付；中途失败时，已经读到的数据仍保留在 buffer 中。
        while len(self.buffer) < n:
            if self.next_page is None:
                break

            items, next_page = self._fetch_page()
            self.buffer.extend(items)
            # 只有 fetch 成功后才推进 token；空页也要继续跟随 next_page。
            self.next_page = next_page

        result = []
        while len(result) < n:
            if not self.buffer:
                break
            result.append(self.buffer.popleft())
        return result


# Local stand-in for the provided API. Fetcher must not inspect .pages.
class MockClient:
    def __init__(self, pages, failures=None):
        self.pages = pages
        self.failures = {}
        if failures is not None:
            self.failures = failures.copy()
        self.calls = []

    def fetch(self, page):
        self.calls.append(page)
        if self.failures.get(page, 0) > 0:
            self.failures[page] -= 1
            raise TimeoutError("Temporary upstream failure")
        return self.pages[page]


if __name__ == "__main__":
    # 1. Preserve leftovers across calls, cross pages, and skip an empty page.
    client = MockClient({
        0: ([10, 20, 30], 5),
        5: ([], 9),
        9: ([40, 50], None),
    })
    reader = Fetcher(client.fetch)
    print(reader.fetch_n(0))  # []
    print(client.calls)  # []
    print(reader.fetch_n(2))  # [10, 20]
    print(client.calls)  # [0]
    print(reader.fetch_n(2))  # [30, 40]
    print(client.calls)  # [0, 5, 9]
    print(reader.fetch_n(5))  # [50]
    print(reader.fetch_n(1))  # []
    print(client.calls)  # [0, 5, 9]

    # 2. Exact page boundary: do not fetch the next page until it is needed.
    client = MockClient({"start": ([1, 1], "last"), "last": ([2], None)})
    reader = Fetcher(client.fetch, first_page="start")
    print(reader.fetch_n(2))  # [1, 1]
    print(client.calls)  # ['start']
    print(reader.fetch_n(2))  # [2]
    print(reader.fetch_n(2))  # []

    # 3. Empty source represented by a terminal empty page.
    client = MockClient({0: ([], None)})
    reader = Fetcher(client.fetch)
    print(reader.fetch_n(3))  # []
    print(reader.fetch_n(3))  # []
    print(client.calls)  # [0]

    # 4. Follow-up: the second page times out once, then succeeds.
    client = MockClient({0: ([1, 2], 7), 7: ([3, 4], None)}, failures={7: 1})
    reader = Fetcher(client.fetch, max_attempts=2)
    print(reader.fetch_n(3))  # [1, 2, 3]
    print(client.calls)  # [0, 7, 7]
    print(reader.fetch_n(3))  # [4]
