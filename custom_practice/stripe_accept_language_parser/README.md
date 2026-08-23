# Stripe-style Custom — Accept-Language Header Parser

The Stripe bank names an older recurring Accept-Language parser but does not preserve one current full
prompt. This runnable practice uses a small, explicit negotiation contract inspired by the HTTP header;
it is a pattern drill, not a recovered verbatim question.

## Contract

Implement:

```python
def negotiate_languages(header: str, supported: Sequence[str]) -> List[str]:
    ...
```

- `supported` contains unique valid language tags and its original spelling must be preserved.
- Split `header` on commas. Each range is `tag` or `tag;q=value`; whitespace around pieces is ignored.
- Tags and matching are case-insensitive. A valid tag contains alphanumeric subtags separated by a
  single `-`. `*` is the wildcard.
- Default quality is `1`. Quality must be a decimal in `[0, 1]`; invalid ranges and `q=0` are ignored.
- Process ranges by descending quality, then original header position.
- A specific tag containing `-` matches only that exact supported tag.
- A base tag such as `fr` matches every supported tag whose first subtag is `fr`, in supported order.
- `*` matches every still-unreturned supported language, in supported order.
- Never return a supported language more than once.

## Related LeetCode

No close LeetCode problem covers weighted language-range parsing and negotiation. String parsing problems
help only superficially, so this family receives a custom exercise.

## Run

```bash
python3 custom_practice/stripe_accept_language_parser/run_tests.py
```
