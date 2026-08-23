# Snowflake Custom Practice

All Snowflake exercises live in this folder. Each standalone problem has one folder. Follow-ups and
variants for Ordered N-ary Tree Deletion are nested under that base problem instead of appearing as
unrelated top-level exercises.

```text
snowflake/
├── bounded_event_frequency_tracker/
├── hit_counter/
├── log_storage/
├── ordered_nary_tree_deletion/
│   ├── solution.py, test_cases.py, run_tests.py, models.py
│   ├── follow_ups/
│   │   ├── multiple_deletions/
│   │   ├── forest_height/
│   │   ├── minimum_deletions_for_height/
│   │   ├── parent_index_forest/
│   │   └── reported_height_limit_greedy/
│   └── variants/
│       └── subtree_deletion/
├── recent_custom_bank/
└── transactional_kv/
```

The base tree problem keeps its shared `models.py` at the base folder. Its follow-ups and variant
import that model rather than duplicating the tree definition.

Run any exercise from the repository root, for example:

```bash
python3 custom_practice/snowflake/ordered_nary_tree_deletion/run_tests.py
python3 custom_practice/snowflake/ordered_nary_tree_deletion/follow_ups/multiple_deletions/run_tests.py
python3 custom_practice/snowflake/hit_counter/run_tests.py
```
