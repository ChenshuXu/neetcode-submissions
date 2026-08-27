# Snowflake Custom Practice

All Snowflake exercises live in this folder. Each standalone problem has one folder. Follow-ups and
variants for Ordered N-ary Tree Deletion are nested under that base problem instead of appearing as
unrelated top-level exercises.

```text
snowflake/
├── acl_inheritance_dag/
├── bounded_event_frequency_tracker/
├── binary_search_repeated_queries/
├── closest_bathroom_for_each_desk/
├── hit_counter/
├── log_storage/
├── multi_rule_rate_limiter/
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
├── parallel_schedule_limited_workers/
├── person_cake/
│   ├── solution.py, test_cases.py, run_tests.py
│   ├── follow_ups/
│   │   └── global_assignment/
│   └── variants/
│       └── grid_nearest_cake/
├── recent_custom_bank/
├── task_executor_ood/
├── timestamped_versioned_kv/
├── transactional_kv/
└── wiki_hopper/
```

The base tree problem keeps its shared `models.py` at the base folder. Its follow-ups and variant
import that model rather than duplicating the tree definition.

`person_cake/` follows the same rule: the 1-D row is the base, the reported 2-D round is a variant,
and the reported one-to-one assignment question is the follow-up.

Run any exercise from the repository root, for example:

```bash
python3 custom_practice/snowflake/acl_inheritance_dag/run_tests.py
python3 custom_practice/snowflake/ordered_nary_tree_deletion/run_tests.py
python3 custom_practice/snowflake/ordered_nary_tree_deletion/follow_ups/multiple_deletions/run_tests.py
python3 custom_practice/snowflake/binary_search_repeated_queries/run_tests.py
python3 custom_practice/snowflake/closest_bathroom_for_each_desk/run_tests.py
python3 custom_practice/snowflake/hit_counter/run_tests.py
python3 custom_practice/snowflake/multi_rule_rate_limiter/run_tests.py
python3 custom_practice/snowflake/parallel_schedule_limited_workers/run_tests.py
python3 custom_practice/snowflake/person_cake/run_tests.py
python3 custom_practice/snowflake/task_executor_ood/run_tests.py
python3 custom_practice/snowflake/timestamped_versioned_kv/run_tests.py
python3 custom_practice/snowflake/wiki_hopper/run_tests.py
```
