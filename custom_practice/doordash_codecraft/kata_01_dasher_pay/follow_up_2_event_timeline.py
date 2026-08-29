"""Follow-up 2: replace delivery rows with an unordered event timeline.

Evolution from Follow-up 1:
- Keep peak-window pay calculation.
- Replace complete Delivery rows with pickup and terminal events.
- Sort, deduplicate, and pair events before calculating each activity.
"""

from dataclasses import dataclass
from enum import Enum


RATE_CENTS_PER_MINUTE = 30


class EventAction(Enum):
    PICKED_UP = "picked_up"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


@dataclass(frozen=True)
class OrderEvent:
    """One immutable event; frozen allows exact duplicates to be removed."""

    order_id: str
    at: int
    action: EventAction


@dataclass
class Activity:
    """One validated pickup-to-terminal interval."""

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
    """Rebuild validated activity intervals from unordered order events."""

    # For equal timestamps, process pickup first. The positive-duration check
    # below still rejects a pickup and terminal occurring at the same time.
    priority = {
        EventAction.PICKED_UP: 0,
        EventAction.DELIVERED: 1,
        EventAction.CANCELLED: 1,
    }

    # set removes exact duplicate events; sorting creates one timeline to scan.
    ordered = sorted(
        set(events),
        key=lambda event: (event.at, priority[event.action], event.order_id),
    )

    # order_id -> pickup time for intervals waiting for a terminal event.
    open_orders = {}

    # Orders that already reached DELIVERED or CANCELLED. Keeping them prevents
    # a second terminal event or a new pickup from reopening a finished order.
    closed_orders = set()

    # Valid pickup-to-terminal pairs. Only DELIVERED activities are paid later.
    activities = []

    for event in ordered:
        if event.action is EventAction.PICKED_UP:
            # A pickup is valid only for an order that has never been opened.
            if event.order_id in open_orders or event.order_id in closed_orders:
                raise InvalidTimelineError("duplicate pickup")
            open_orders[event.order_id] = event.at
            continue

        # A terminal event must close exactly one currently open interval.
        start = open_orders.pop(event.order_id, None)
        if start is None or event.order_id in closed_orders:
            raise InvalidTimelineError("terminal event without pickup")
        if event.at <= start:
            raise InvalidTimelineError("activity must have positive duration")

        # The order moves permanently from open to closed.
        closed_orders.add(event.order_id)
        activities.append(Activity(event.order_id, start, event.at, event.action))

    # Every pickup must be paired before the timeline can be finalized.
    if open_orders:
        raise InvalidTimelineError("unfinished pickup")

    return activities


class PayoutService:
    def __init__(self, event_client):
        self.event_client = event_client

    def get_payout(self, dasher_id, peak_windows=()):
        if not isinstance(dasher_id, str) or not dasher_id.strip():
            raise ValueError("dasher_id must not be blank")

        windows = merge_peak_windows(peak_windows)
        try:
            events = self.event_client.list_events(dasher_id)
        except EventClientError as error:
            raise PayoutUnavailableError("event service unavailable") from error

        amount_cents = 0
        completed_count = 0
        for activity in build_activities(events):
            if activity.action is EventAction.DELIVERED:
                amount_cents += interval_pay(activity.start, activity.end, windows)
                completed_count += 1

        return PayoutResponse(dasher_id, amount_cents, completed_count)


class FakeEventClient:
    def __init__(self, events):
        self.events = events

    def list_events(self, dasher_id):
        return self.events


def main():
    pickup = OrderEvent("a", 0, EventAction.PICKED_UP)
    events = [
        OrderEvent("b", 15, EventAction.DELIVERED),
        pickup,
        OrderEvent("a", 10, EventAction.DELIVERED),
        OrderEvent("b", 5, EventAction.PICKED_UP),
        pickup,
    ]
    result = PayoutService(FakeEventClient(events)).get_payout("dasher-1")
    assert result == PayoutResponse("dasher-1", 600, 2)
    print(result)


if __name__ == "__main__":
    main()
