import collections
from typing import Sequence


class MultiRuleRateLimiter:
    """Apply every configured sliding-window rule independently per key."""

    def __init__(self, rules: Sequence[tuple[int, int]]) -> None:
        """Initialize a limiter with fixed (max_requests, window_seconds) rules."""
        self.rules = tuple(rules)
        # Each key has one queue per rule, so every sliding window is maintained
        # incrementally instead of scanning the full shared history each time.
        # queue_map: key -> queues; queue element = [timestamp, count]
        self.queue_map = {}
        # count_map: key -> active accepted-request count for each rule
        self.count_map = {}

    def allow(self, key: str, timestamp: int) -> bool:
        """Return whether this request is accepted, recording it only if accepted."""
        # A new key starts with an independent queue and count for every rule.
        if key not in self.queue_map:
            queues = []
            for _ in self.rules:
                queues.append(collections.deque())
            self.queue_map[key] = queues
            self.count_map[key] = [0] * len(self.rules)

        queues = self.queue_map[key]
        active_counts = self.count_map[key]

        # For each rule:
        # 1. remove accepted requests outside this rule's window;
        # 2. check whether adding the current request would exceed its limit.
        # After removal, each queue contains exactly the accepted requests that
        # are still active for that rule.
        allowed = True
        for i, rule in enumerate(self.rules):
            max_requests, window_seconds = rule
            queue = queues[i]

            # Active window is (timestamp - window_seconds, timestamp],
            # so accepted timestamps <= cutoff have expired.
            cutoff = timestamp - window_seconds

            while queue and queue[0][0] <= cutoff:
                _, expired_count = queue.popleft()
                active_counts[i] -= expired_count

            if active_counts[i] >= max_requests:
                allowed = False

        # Check every rule first. A rejected request must not be added to any
        # queue, otherwise it would incorrectly consume future quota.
        if not allowed:
            return False

        # The request passed every rule, so record it in every rule's queue.
        # If the last accepted request has the same timestamp, increase its
        # bucket count instead of appending another queue element.
        for i, queue in enumerate(queues):
            if queue and queue[-1][0] == timestamp:
                queue[-1][1] += 1
            else:
                queue.append([timestamp, 1])
            active_counts[i] += 1

        return True
