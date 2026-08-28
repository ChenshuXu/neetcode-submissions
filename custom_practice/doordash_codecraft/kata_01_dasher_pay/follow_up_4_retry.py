"""Follow-up 4: retry only named timeouts inside one total deadline.

Evolution from Follow-up 3:
- Keep peak pay, event processing, and cancellation policy unchanged.
- Wrap the upstream event client with timeout-only retry.
- Bound all attempts and exponential backoff by one total deadline.
"""

import time
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


class EventClientTimeoutError(EventClientError):
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


class RetryingEventClient:
    # New in Follow-up 4: retry the read, not the payout calculation.
    def __init__(
        self,
        client,
        max_attempts=3,
        backoff_seconds=0.05,
        total_timeout_seconds=0.3,
        clock=time.monotonic,
        sleep=time.sleep,
    ):
        if max_attempts < 1 or backoff_seconds < 0 or total_timeout_seconds <= 0:
            raise ValueError("invalid retry settings")
        self.client = client
        self.max_attempts = max_attempts
        self.backoff_seconds = backoff_seconds
        self.total_timeout_seconds = total_timeout_seconds
        self.clock = clock
        self.sleep = sleep

    def list_events(self, dasher_id):
        deadline = self.clock() + self.total_timeout_seconds
        delay = self.backoff_seconds

        for attempt in range(self.max_attempts):
            try:
                events = self.client.list_events(dasher_id)
            except EventClientTimeoutError:
                last_attempt = attempt == self.max_attempts - 1
                if last_attempt or self.clock() + delay >= deadline:
                    raise
                self.sleep(delay)
                delay *= 2
                continue

            if self.clock() >= deadline:
                raise EventClientTimeoutError("total deadline exceeded")
            return events

        raise EventClientTimeoutError("retry attempts exhausted")


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


class FlakyEventClient:
    def __init__(self, events):
        self.events = events
        self.calls = 0

    def list_events(self, dasher_id):
        self.calls += 1
        if self.calls == 1:
            raise EventClientTimeoutError("slow upstream")
        return self.events


def main():
    events = [
        OrderEvent("a", 0, EventAction.PICKED_UP),
        OrderEvent("a", 5, EventAction.DELIVERED),
    ]
    client = FlakyEventClient(events)
    retrying_client = RetryingEventClient(client, backoff_seconds=0)
    result = PayoutService(retrying_client).get_payout("dasher-1")

    assert result.amount_cents == 150
    assert client.calls == 2
    print(result)


if __name__ == "__main__":
    main()
