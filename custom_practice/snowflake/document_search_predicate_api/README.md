# Snowflake Custom — Document Search / Predicate API

This is a runnable cold-practice contract for the Snowflake coding-screen family reported as a
document-retrieval API with `InsertDoc(filename)` plus predicate / `contains` queries
([1173789](https://www.1point3acres.com/bbs/thread-1173789-1-1.html), 2026-04, coding round).

This is not a verbatim copy of a private prompt. The public report does not expose the document
representation, the predicate grammar, update/delete semantics, the result ordering, or the indexing
objective, so this exercise fixes all of those below to make the visible tests deterministic. Treat
the fixed choices as *one* defensible contract, not as the interviewer's contract: in the real round,
ask for each of them before writing code.

## Contract

Implement `DocumentStore` in `solution.py`:

```python
class DocumentStore:
    def insert_doc(self, filename: str, fields: Mapping[str, str]) -> None:
        ...

    def delete_doc(self, filename: str) -> bool:
        ...

    def search(self, predicate) -> list[str]:
        ...
```

A document is a filename plus a mapping of named text fields, for example
`{"title": "Data Sharing", "owner": "atindra"}`.

A predicate is either `None` or a tuple whose first element names the operator:

| Predicate | Matches a document when |
|---|---|
| `None` | always — an empty predicate selects the whole corpus |
| `("eq", field, value)` | the document has `field` and its **whole value** equals `value` |
| `("contains", field, word)` | the document has `field` and `word` is one of that field's whitespace-separated words |
| `("and", *children)` | every child matches; `("and",)` matches every document |
| `("or", *children)` | some child matches; `("or",)` matches no document |
| `("not", child)` | the child does not match |

Rules:

- Field values are plain strings. Words are the whitespace-separated tokens of a value; runs of
  whitespace collapse and an empty value has no words.
- Matching is **case-sensitive** and does no punctuation stripping. `contains` matches a whole word,
  never a substring: `("contains", "title", "Dat")` does not match `"Data Sharing"`.
- A field that a document does not carry matches nothing. It is not an error, and
  `("not", ("contains", "tag", "internal"))` therefore *does* match a document with no `tag` field.
- `insert_doc` with an existing filename **replaces** that document's fields and keeps its original
  insertion position. Words from the replaced content must stop matching.
- `delete_doc` returns `True` when the document existed and `False` otherwise. A deleted document
  leaves the corpus entirely — including the universe that `not` complements against. A filename
  inserted again after a delete is a **new** document and sorts at the end.
- `search` returns filenames in **insertion order**, with no duplicates.

Example:

```text
store.insert_doc("clean_room.txt", {"title": "Snowflake Data Clean Room", "owner": "newton"})
store.insert_doc("sharing.txt",    {"title": "Data Sharing",              "owner": "atindra"})

search(("contains", "title", "Data"))              -> ["clean_room.txt", "sharing.txt"]
search(("eq", "title", "Data Sharing"))            -> ["sharing.txt"]
search(("and", ("contains", "title", "Data"),
               ("eq", "owner", "newton")))         -> ["clean_room.txt"]
search(("not", ("eq", "owner", "newton")))         -> ["sharing.txt"]
search(None)                                       -> ["clean_room.txt", "sharing.txt"]
```

## Run it

Implement only the class in `solution.py`, then run:

```bash
python3 custom_practice/snowflake/document_search_predicate_api/run_tests.py
```

Useful options:

```bash
python3 custom_practice/snowflake/document_search_predicate_api/run_tests.py --list
python3 custom_practice/snowflake/document_search_predicate_api/run_tests.py --case missing
```

The runner creates a fresh store for every case and replays a list of operations. `insert` produces
no output; `delete` records its Boolean, and `search` records its filenames as a tuple.

## Scan versus inverted index

This is the whole point of the question. Do not skip straight to the index — say the scan out loud,
name its bottleneck, then remove the bottleneck.

**Baseline scan.** Keep documents in a list and evaluate the predicate per document.
`insert_doc` is `O(1)`, `delete_doc` is `O(1)` amortized, and `search` is `O(D · P)` for `D` live
documents and `P` predicate nodes — every query touches every document even when one word narrows the
answer to two files. Space is `O(total field text)`.

**Inverted index.** Map `(field, word) -> set of doc ids` and `(field, whole value) -> set of doc ids`.
A leaf is one dict lookup, `and` is set intersection, `or` is union, `not` is the live universe minus
the child. `insert_doc` and `delete_doc` become `O(T)` in that document's token count because postings
must be maintained on both sides of a replace. `search` becomes:

| Node | Cost |
|---|---|
| `eq` / `contains` leaf | `O(len(posting list))` |
| `and` | bounded by the **smallest** child posting list once children are ordered by size |
| `or` | `O(sum of child results)` |
| `not`, `None`, `("and",)` | `O(D)` — negation and match-all still touch the whole universe |

Space is `O(total words across live documents)`. The honest statement to make aloud: the index only
helps queries whose *selective* leaf is small. A negation-dominated or match-all query is `O(D)` under
either design, and that is a property of the answer size, not of the index.

The trap worth naming: the index has to be retracted on overwrite and delete. An index that is only
ever appended to will happily return a document for a word it no longer contains, and the visible
tests are built to catch exactly that.

## Interview target

Assume a single 45–60 minute problem.

- 0–6 minutes: clarify the document representation, the predicate grammar, case sensitivity,
  word-versus-substring, missing fields, duplicate filenames, delete, and result ordering. Every one
  of those changes the implementation — none of them is a ceremonial question.
- 6–10 minutes: state the representation and the invariant, and give the scan baseline with its
  bottleneck before naming the index.
- 10–30 minutes: implement insert plus predicate evaluation.
- 30–40 minutes: run tests for duplicate filenames, an empty predicate, multiple nested conditions,
  and a field no document carries. Then state time and space for both operations.
- 40–60 minutes: index maintenance under delete, AND ordering by selectivity, and whichever follow-up
  the interviewer pulls.

State the invariant in one sentence, for example: *every live document id appears in the posting list
of `(field, word)` exactly when that document's `field` currently contains that word* — which is what
makes retraction on overwrite mandatory.

## Follow-ups to discuss after the base passes

1. Why is `not` evaluated against live documents rather than against everything ever inserted, and
   what breaks if the universe is wrong?
2. Order `and` children by posting-list size. Which children have a cheap size estimate, and what do
   you do with a compound child that has none?
3. Support `("contains_prefix", field, prefix)`. What changes — a trie per field, or sorted word lists
   per field with binary search?
4. Range predicates on numeric or timestamp fields: what does the hash-keyed posting map cost you, and
   what replaces it?
5. The corpus no longer fits in memory. What is partitioned by what, and which operation stops being
   `O(1)`?
6. Concurrent `insert_doc` and `search`: which steps must be one atomic operation, and what does a
   reader see mid-replace?
7. Ranking instead of a boolean answer: what has to be stored per posting to return the top-`k`?
