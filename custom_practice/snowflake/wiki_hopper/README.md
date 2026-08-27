# Snowflake P1-12 — Wiki Hopper

This is a runnable custom-practice reconstruction of a reported Snowflake live-coding problem. The
recoverable evidence confirms the core task: call `getLinkedPages(page)` and use BFS to find a
shortest route or distance from one internal Wiki page to another. One report also explicitly says
the candidate had to write runnable tests.

The archive does not expose the complete original signature, return format, tie-breaking rule, or
invalid-input behavior. This package therefore fixes one deterministic training contract below. The
Python API, path output, empty-list sentinel, and adjacency-order tie break are practice assumptions,
not claims about verbatim interview wording.

## Contract

Implement `find_shortest_path` in `solution.py`:

```python
def find_shortest_path(
    start_page: str,
    target_page: str,
    get_linked_pages: Callable[[str], Iterable[str]],
) -> list[str]:
    ...
```

`get_linked_pages(page)` returns the pages linked directly from `page`. Treat the Wiki as a directed
graph: a link from `A` to `B` does not imply a link from `B` to `A`.

Return one shortest path from `start_page` to `target_page`, including both endpoints.

- If `start_page == target_page`, return `[start_page]` without fetching any page.
- If the target is unreachable, return `[]`.
- The graph may contain cycles, self-links, duplicate links, and links to pages that are not keys in
  the test graph. A missing key has no outgoing links.
- `get_linked_pages` is deterministic, preserves link order, and does not raise in the base problem.
- If several shortest paths exist, return the one discovered first under the callback's link order.
  Do not sort the linked pages.
- Page names are valid strings. Invalid-input behavior is outside this practice contract.

## Example

```text
Home -> [A, B]
A    -> [C]
B    -> [Target]
C    -> [Target]

find_shortest_path(Home, Target, get_linked_pages)
    -> [Home, B, Target]
```

Following `A` first reaches a longer route. BFS must finish the shallower frontier before accepting
the path through `C`.

## Run it

Implement only `find_shortest_path` in `solution.py`, then run:

```bash
python3 custom_practice/snowflake/wiki_hopper/run_tests.py
```

Useful options:

```bash
python3 custom_practice/snowflake/wiki_hopper/run_tests.py --list
python3 custom_practice/snowflake/wiki_hopper/run_tests.py --case shorter
python3 custom_practice/snowflake/wiki_hopper/run_tests.py --case unreachable
```

The supplied starter intentionally raises `NotImplementedError` and contains no retained reference
solution. The verified assisted answer is recorded in Newton's Notion `💽 code` card.

## Interview target

- 0–5 minutes: clarify directed edges, path versus distance, unreachable output, target equal to
  start, and shortest-path tie behavior.
- 5–10 minutes: state BFS, the queue/parent-map invariant, and `O(V + E)` time / `O(V)` space.
- 10–25 minutes: implement BFS and path reconstruction.
- 25–35 minutes: write deterministic tests for the identity case, direct link, a shorter path that
  beats a longer branch, cycles, duplicate links, multiple shortest paths, and unreachable target.

Here `V` is the number of pages discovered before the search ends and `E` is the total number of
outgoing links scanned from expanded pages.

## Variants to discuss after the base passes

These come from the broader crawler family; the archive does not establish that they were asked as
follow-ups in the same Wiki Hopper interview:

1. Return only the shortest distance: `len(path) - 1` when a path exists.
2. Define retry/skip/fail semantics when `getLinkedPages` raises.
3. Add per-host or global rate limiting.
4. Bound concurrent fetches while preserving shortest-path correctness.
5. Replace exact `visited` storage with a Bloom filter and explain the false-positive trade-off.
