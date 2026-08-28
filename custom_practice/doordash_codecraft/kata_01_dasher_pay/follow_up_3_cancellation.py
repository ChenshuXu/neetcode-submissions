"""Follow-up 3: add explicit fixed or duration-based cancellation pay.

Evolution from Follow-up 2:
- Keep event pairing and peak-window delivery pay.
- Add a configurable rule for cancelled activities.
- Support ignore, fixed compensation, or duration-based compensation.
"""

from dataclasses import dataclass
from enum import Enum


RATE_CENTS_PER_MINUTE = 30
IGNORE_CANCELLATION = "ignore"
FIXED_CANCELLATION = "fixed"
DURATION_CANCELLATION = "duration"


class EventAction(Enum):
    PICKED_UP = "picked_up"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


@dataclass(frozen=True)
class OrderEvent:
    order_id: str
    at: int
    action: EventAction


@dataclass
class Activity:
    order_id: str
    start: int
    end: int
    action: EventAction


@dataclass
class PeakWindow:
    start: int
    end: int


@dataclass
class PayoutResponse:
    dasher_id: str
    amount_cents: int
    completed_delivery_count: int
    paid_cancellation_count: int


class EventClientError(RuntimeError):
    pass


class InvalidTimelineError(ValueError):
    pass


class PayoutUnavailableError(RuntimeError):
    pass


def merge_peak_windows(windows):
    ordered = sorted(windows, key=lambda window: window.start)
    merged = []

    for window in ordered:
        if window.end <= window.start:
            raise ValueError("peak windows must have positive duration")
        if not merged or window.start > merged[-1].end:
            merged.append(PeakWindow(window.start, window.end))
        else:
            merged[-1].end = max(merged[-1].end, window.end)

    return merged


def interval_pay(start, end, peak_windows):
    if end <= start:
        raise InvalidTimelineError("activity must have positive duration")

    amount_cents = (end - start) * RATE_CENTS_PER_MINUTE
    for window in peak_windows:
        overlap_start = max(start, window.start)
        overlap_end = min(end, window.end)
        if overlap_start < overlap_end:
            amount_cents += (overlap_end - overlap_start) * RATE_CENTS_PER_MINUTE
    return amount_cents


def build_activities(events):
    priority = {
        EventAction.PICKED_UP: 0,
        EventAction.DELIVERED: 1,
        EventAction.CANCELLED: 1,
    }
    ordered = sorted(
        set(events),
        key=lambda event: (event.at, priority[event.action], event.order_id),
    )
    open_orders = {}
    closed_orders = set()
    activities = []

    for event in ordered:
        if event.action is EventAction.PICKED_UP:
            if event.order_id in open_orders or event.order_id in closed_orders:
                raise InvalidTimelineError("duplicate pickup")
            open_orders[event.order_id] = event.at
            continue

        start = open_orders.pop(event.order_id, None)
        if start is None or event.order_id in closed_orders:
            raise InvalidTimelineError("terminal event without pickup")
        if event.at <= start:
            raise InvalidTimelineError("activity must have positive duration")

        closed_orders.add(event.order_id)
        activities.append(Activity(event.order_id, start, event.at, event.action))

    if open_orders:
        raise InvalidTimelineError("unfinished pickup")

    return activities


class PayoutService:
    def __init__(self, event_client):
        self.event_client = event_client

    def get_payout(
        self,
        dasher_id,
        peak_windows=(),
        cancellation_mode=IGNORE_CANCELLATION,
    ):
        if not isinstance(dasher_id, str) or not dasher_id.strip():
            raise ValueError("dasher_id must not be blank")
        if cancellation_mode not in {
            IGNORE_CANCELLATION,
            FIXED_CANCELLATION,
            DURATION_CANCELLATION,
        }:
            raise ValueError("unknown cancellation mode")

        windows = merge_peak_windows(peak_windows)
        try:
            events = self.event_client.list_events(dasher_id)
        except EventClientError as error:
            raise PayoutUnavailableError("event service unavailable") from error

        amount_cents = 0
        completed_count = 0
        paid_cancellation_count = 0

        for activity in build_activities(events):
            if activity.action is EventAction.DELIVERED:
                amount_cents += interval_pay(activity.start, activity.end, windows)
                completed_count += 1
            elif cancellation_mode == DURATION_CANCELLATION:
                amount_cents += interval_pay(activity.start, activity.end, windows)
                paid_cancellation_count += 1
            elif (
                cancellation_mode == FIXED_CANCELLATION
                and activity.end - activity.start >= 5
            ):
                amount_cents += 200
                paid_cancellation_count += 1

        return PayoutResponse(
            dasher_id,
            amount_cents,
            completed_count,
            paid_cancellation_count,
        )


class FakeEventClient:
    def __init__(self, events):
        self.events = events

    def list_events(self, dasher_id):
        return self.events


def main():
    events = [
        OrderEvent("a", 0, EventAction.PICKED_UP),
        OrderEvent("a", 5, EventAction.CANCELLED),
    ]
    service = PayoutService(FakeEventClient(events))

    fixed = service.get_payout("dasher-1", cancellation_mode=FIXED_CANCELLATION)
    duration = service.get_payout(
        "dasher-1",
        [PeakWindow(0, 10)],
        DURATION_CANCELLATION,
    )
    assert fixed.amount_cents == 200
    assert duration.amount_cents == 300
    print(fixed)
    print(duration)


if __name__ == "__main__":
    main()
