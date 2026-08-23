# Stripe-style Custom — WebSocket Load Balancer

This runnable exercise follows the publicly recovered five-part `route_requests` contract: least-load
routing, disconnect, object affinity, per-target capacity, and temporary shutdown with rerouting.

## Contract

Implement:

```python
def route_requests(
    num_targets: int,
    max_connections_per_target: int,
    requests: Sequence[str],
) -> List[str]:
    ...
```

Targets are numbered `1..num_targets`. Request forms are:

```text
CONNECT,connection_id,user_id,object_id
DISCONNECT,connection_id,user_id,object_id
SHUTDOWN,target_index
```

- A normal `CONNECT` chooses the eligible target with minimum `(active_load, target_index)`.
- If `object_id` has any active connection, it is pinned to that connection's target.
- Reject a duplicate active `connection_id`, an affinity target at capacity, or a request when all
  eligible targets are full. Rejection has no output and no partial state.
- `DISCONNECT` uses `connection_id` as identity. Unknown IDs are ignored. Object affinity disappears
  after its last active connection disconnects.
- `SHUTDOWN` temporarily excludes its target. Remove all of its connections first, then reroute them
  in lexicographic `connection_id` order using the ordinary rules. Failed reroutes are dropped. Restore
  target availability after the operation.
- Return `connection_id,user_id,target_index` for every successful initial connection and reroute.
- Inputs and target indices are otherwise valid.

## Related LeetCode

- [LC 1606 — Find Servers That Handled Most Number of Requests](https://leetcode.com/problems/find-servers-that-handled-most-number-of-requests/)
- [LC 1882 — Process Tasks Using Servers](https://leetcode.com/problems/process-tasks-using-servers/)

They cover availability and tie-breaking, but not object affinity or shutdown/reroute state.

## Run

```bash
python3 custom_practice/stripe/websocket_load_balancer/run_tests.py
```
