from dataclasses import dataclass
from typing import Sequence


WINDOW_SECONDS = 30 * 60


@dataclass(frozen=True)
class QueryRecord:
    query_id: str
    warehouse_id: str
    user_id: str
    start_time: int
    end_time: int
    credits_used: int


@dataclass(frozen=True)
class WindowSummary:
    warehouse_id: str
    window_start: int
    window_end: int
    total_credits: int
    top_user_id: str
    top_user_credits: int


def find_peak_query_windows(
    queries: Sequence[QueryRecord],
) -> list[WindowSummary]:
    """Return the maximum-credit 30-minute start-time window per warehouse."""

    raise NotImplementedError("Implement find_peak_query_windows")
