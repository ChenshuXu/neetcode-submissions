from collections import deque
from typing import Deque, Dict, Optional, Tuple


class BoundedEventFrequency:
    """Track the most frequent key in a bounded recent-time window."""

    def __init__(self, window_seconds: int) -> None:
        """Initialize any state needed for a positive-length window."""
        self.window_seconds = window_seconds

        # 双端队列按时间顺序保存当前窗口内的 (timestamp, key)，队首是最旧事件。
        self.events: Deque[Tuple[int, str]] = deque()

        # 字典保存当前窗口内每个 key 的出现次数：key -> frequency。
        self.frequencies: Dict[str, int] = {}

    def _evict_stale_events(self, now: int) -> None:
        """Remove events outside the active interval (now - window, now]."""
        cutoff = now - self.window_seconds

        # 左边界不属于有效窗口，所以 timestamp == cutoff 也要删除。
        while self.events and self.events[0][0] <= cutoff:
            _, key = self.events.popleft()
            self.frequencies[key] -= 1

            # 及时移除频次为 0 的 key，使字典大小只依赖当前窗口。
            if self.frequencies[key] == 0:
                del self.frequencies[key]

    def record(self, timestamp: int, key: str) -> None:
        """Record one event at a timestamp no earlier than previous calls."""
        self._evict_stale_events(timestamp)

        self.events.append((timestamp, key))
        self.frequencies[key] = self.frequencies.get(key, 0) + 1

    def most_frequent(self, now: int) -> Optional[str]:
        """Return the most frequent active key, using lexicographic tie-breaking."""
        self._evict_stale_events(now)

        best_key: Optional[str] = None
        best_frequency = 0

        for key, frequency in self.frequencies.items():
            # 频次更高时更新；频次相同时选择字典序更小的 key。
            if frequency > best_frequency:
                best_key = key
                best_frequency = frequency
            elif frequency == best_frequency and (
                best_key is None or key < best_key
            ):
                best_key = key

        return best_key
