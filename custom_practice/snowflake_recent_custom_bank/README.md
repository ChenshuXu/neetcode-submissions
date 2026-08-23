# Snowflake Recent Custom Question Bank

This runnable pack covers recent Snowflake prep-plan questions for which no sufficiently close
LeetCode contract was found. The public evidence ranges from first-hand reports to commercial
Xiaohongshu/HackerRank screenshots. Marketing provenance does not exclude a prompt, but incomplete
details are called out below as deterministic practice assumptions rather than original wording.

`solution.py` intentionally contains blank starters only. No reference solutions are included.

## Run

From the repository root:

```bash
python3 custom_practice/snowflake_recent_custom_bank/run_tests.py --list-problems
python3 custom_practice/snowflake_recent_custom_bank/run_tests.py horizontal_pod_autoscaler
python3 custom_practice/snowflake_recent_custom_bank/run_tests.py sql_table_extraction --list
python3 custom_practice/snowflake_recent_custom_bank/run_tests.py sessionization --case gap
```

A blank starter is expected to fail visibly with `NotImplementedError`; that confirms the runner,
problem selection, and test discovery are working without supplying an answer.

## Contracts

### `single_query_revenue`

Implement `maximize_single_query_type(budget_minutes, query_types)`. Each query type is
`(name, duration_minutes, revenue_per_run)`. Choose exactly one type and repeat it as many whole
times as the budget allows. Return `(maximum_revenue, name)`; return `(0, None)` if none fits.
The public report does not expose tie behavior, so this drill uses lexicographically smallest name.

### `horizontal_pod_autoscaler`

Implement `final_pod_counts(initial, operations)`. `("set", i, x)` assigns service `i` exactly
`x` pods. `("raise_min", x)` raises every current count below `x` to `x`. Return the final counts.
This is the recovered HackerRank/OA contract.

### `string_xor`

Implement `minimum_string_xor(word)`. Assign every distinct lowercase letter used in `word` a
different positive integer in `[1, 100]`; XOR the assigned value once for each character occurrence
and return the minimum possible XOR. The screenshots expose the distinct-value bound and the
minimization goal but not all original output details, so this drill returns only the minimum value.

### `database_configuration`

Implement `subtree_pairability(parent)`. Nodes are `0..n-1`; `parent[0] == -1`. For every node in
index order, determine whether all nodes in its rooted subtree can be covered exactly once by
parent-child pairs. Return a `T`/`F` string. This preserves the recovered adjacent-pair perfect
matching contract while making the screenshot's output marker unambiguous.

### `string_patterns`

Implement `count_constrained_strings(word_len, max_vowels)`. Count lowercase strings of exactly
`word_len` whose longest consecutive-vowel run is at most `max_vowels`; there are five vowels and
21 consonants. Return the count modulo `1_000_000_007`.

### `acl_inheritance`

Implement `resolve_acl(parents, local_allow, local_deny, node)`. `parents[i]` may contain multiple
parents. Collect permissions from the node and every reachable ancestor; a deny at any of those nodes
overrides an allow. Return the effective permissions sorted. Detect a reachable parent cycle and raise
`ValueError`. Updates and iterative traversal for very deep graphs are follow-ups.

### `distributed_nary_count`

Implement `count_distributed_nodes(root, responses, max_attempts)`. Each node is owned by a remote
service. `responses[node]` is the deterministic sequence returned by successive fetch attempts:
`None` means timeout and a sequence of child IDs means success. Retry a node up to `max_attempts`,
count each node ID once even if duplicate responses or edges arrive, and raise `TimeoutError` after
exhaustion. Bounded concurrency and cancellation are follow-ups.

### `http_retry_backoff`

Implement `execute_with_retry(statuses, retry_after, base_delay, max_attempts, deadline)`. Treat 429
and 5xx as retryable; all other statuses stop. `retry_after[attempt_index]` overrides exponential
delay `base_delay * 2**attempt_index`. Do not schedule a delay that would consume the remaining total
deadline, and never exceed `max_attempts`. Return `(final_status, tuple_of_delays)`. Jitter is disabled
in visible tests so output is deterministic; idempotency keys and injectable clock/sleep are follow-ups.

### `result_cache_invalidation`

Implement `run_result_cache(operations)`. Supported operations are:

- `("query", sql, role, warehouse, session_digest, tables, computed_result)`
- `("mutate", table)`

Normalize insignificant SQL whitespace/case. A cache hit requires the same SQL, role, warehouse,
session digest, and current version of every referenced table. A mutation increments that table's
version. Return query results in order. Concurrency/singleflight/versioned-CAS is a follow-up, not
part of these sequential visible tests.

### `sql_table_extraction`

Implement `extract_sql_tables(sql)`. Return physical tables referenced by `FROM` or `JOIN` in
first-appearance order, including inside subqueries. Ignore aliases, comments, and CTE names.
Preserve qualified names such as `sales.orders`. Quoted identifiers and dialect-specific table
functions are follow-ups.

### `redundant_parentheses`

Implement `has_redundant_parentheses(expression)` for identifiers/numbers and binary `+ - * /`.
Return `True` if any pair of parentheses encloses no operator at its own nesting depth. Inputs are
syntactically valid; unary operators are a follow-up.

### `sessionization`

Implement `sessionize_events(events, gap_minutes=30)`. Events are `(user_id, minute)` and may be
out of order. For each user, sort by time and start a new session only when the inactivity gap is
strictly greater than `gap_minutes`; an exact 30-minute gap stays in one session. Return sorted
`(user_id, start, end, event_count)` rows.

### `preaggregate_three_tables`

Implement `summarize_accounts(accounts, orders, usage)`. `accounts` contains `(id, name)`;
`orders` contains `(account_id, revenue)`; `usage` contains `(account_id, units)`. Independently
aggregate both fact tables, left-join them to every account, and return sorted
`(id, name, total_revenue, total_units)` rows without many-to-many fanout.

### `census_nl2sql`

Implement `answer_census_question(question, rows)` for this offline take-home slice. Rows contain
`state`, `population`, and `median_income`. Support `highest population state` and
`population of <STATE>`. Return `{"answer": ..., "value": ..., "sources": (<state>, ...)}` so
every answer carries row-level provenance. Unknown questions must raise `ValueError`; deployment,
broader NL2SQL, RAG, access control, and link validation remain project-level follow-ups.
