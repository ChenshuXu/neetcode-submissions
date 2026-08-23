# Stripe-style Custom — Linked Merchant / Entity Clustering

This is a runnable reconstruction of a publicly reported Stripe HackerRank question family. The
public report establishes shared-attribute connected components, link durations, three daily
batches, and stateful pin rules, but it does not expose every line of the original contract. The
assumptions below make the exercise deterministic; this is not a verbatim copy of the live prompt.

## Contract

Implement `linked_merchants` in `solution.py`:

```python
def linked_merchants(
    day1: Sequence[str],
    day2: Sequence[str],
    day3: Sequence[str],
) -> List[str]:
    ...
```

Each record has this comma-separated form:

```text
merchant_id,link_type,duration
```

- `merchant_id` and `link_type` are non-empty strings that do not contain commas.
- `duration` is `1`, `2`, or `3`.
- A record first seen on day `d` is active on days `d` through `d + duration - 1`, inclusive.
- A merchant becomes known on its first record and remains known, even after all of its links expire.
- If the same `(merchant_id, link_type)` association is reported more than once, keep the latest
  expiration day. Duplicate records never create duplicate edges.

All records are valid. Across the three batches there are at most 2,000 records.

## Daily merchant graph

For each day:

- Each known merchant is a node.
- Two distinct merchants have one undirected edge when they share at least one active `link_type`.
- Sharing several active link types still creates only one edge.
- A cluster is a transitive connected component.
- A merchant's degree is its number of distinct neighboring merchants in that day's graph.
- Size-one clusters are omitted from output and do not carry a pin into the next day.

Rebuild the graph for each day. A normal incremental Union-Find cannot undo expired links and split a
component.

## Pin rules

Each output cluster has one `pin` merchant. For a current cluster, first collect all pins from the
**previous day's output clusters** whose merchant is now inside the current cluster.

1. **No previous pin is present:** choose the current member with highest degree; break a tie with the
   lexicographically smaller `merchant_id`.
2. **Exactly one previous pin is present:** keep it, even if another member now has higher degree.
3. **Several previous pins are present after a merge:** choose the candidate pin with highest current
   degree; break a tie lexicographically.

This one rule set covers the reported transitions:

- a cluster that only gains merchants keeps its pin;
- merged clusters compare their old pins;
- after a split, the fragment containing the old pin keeps it, while every other fragment chooses a
  new pin.

For a simultaneous split and merge, only old pins physically present in the new component are
candidates. This is an explicit practice assumption because the public report does not fully expose
that edge case.

## Output

Return one flat list of strings covering all three days.

- Always include `Day 1:`, `Day 2:`, and `Day 3:`, even when that day has no output cluster.
- Format each cluster as `pin:[member1,member2,...]`, with no spaces.
- Sort members lexicographically.
- Sort clusters by descending size, then by pin lexicographically.

Example:

```python
day1 = [
    "m1,email:a,3",
    "m2,email:a,3",
    "m2,device:x,3",
    "m3,device:x,3",
]
day2 = []
day3 = []
```

```text
[
  "Day 1:",
  "m2:[m1,m2,m3]",
  "Day 2:",
  "m2:[m1,m2,m3]",
  "Day 3:",
  "m2:[m1,m2,m3]",
]
```

## Run it

Implement only `linked_merchants` in `solution.py`, then run:

```bash
python3 custom_practice/stripe_linked_merchant_clustering/run_tests.py
```

Useful options:

```bash
python3 custom_practice/stripe_linked_merchant_clustering/run_tests.py --list
python3 custom_practice/stripe_linked_merchant_clustering/run_tests.py --case split
```

The visible suite covers transitive links, expiration boundaries, pin continuity, split, merge,
simultaneous split-and-merge, duplicate/simple-edge semantics, sorting, and empty output days.

## Target

A direct implementation can rebuild three adjacency sets and run DFS/BFS each day:

- parsing and active-association maintenance: `O(R)` over the fixed three days;
- graph construction: `O(sum(k_a^2))` per day, where `k_a` merchants share active attribute `a`;
- component traversal: `O(V + E)` per day;
- graph/component storage: `O(V + E)`.

Prefer clear state transitions and exact output over a complicated dynamic-connectivity structure.

## Follow-ups to discuss after the base passes

1. Support an arbitrary number of days rather than exactly three.
2. Scale one link type to millions of merchants without materializing its entire clique.
3. Process late or corrected records that retroactively change prior days.
4. Return only clusters changed since the previous day.
5. Preserve pin rules under distributed or streaming processing.
