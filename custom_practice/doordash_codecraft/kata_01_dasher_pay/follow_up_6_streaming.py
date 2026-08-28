"""Follow-up 6: process an ordered event stream without loading a batch.

Evolution from Follow-up 5:
- Keep peak pay, cancellation rules, retry, and idempotent issuance.
- Add an incremental accumulator for events that arrive in time order.
- Track open orders and seen event IDs instead of sorting a complete batch.
"""

import time
from dataclasses import dataclass
from enum import Enum
from threading import Lock


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
    event_id: str
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


@dataclass
class IssuedPayout:
    idempotency_key: str
    amount_cents: int
    payment_id: str


class EventClientError(RuntimeError):
    pass


class EventClientTimeoutError(EventClientError):
    pass


class InvalidTimelineError(ValueError):
    pass


class LateEventError(InvalidTimelineError):
    pass


class PayoutUnavailableError(RuntimeError):
    pass


class IdempotencyConflictError(RuntimeError):
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
    unique_events = {}
    for event in events:
        existing = unique_events.get(event.event_id)
        if existing is not None and existing != event:
            raise InvalidTimelineError("event_id reused with different data")
        unique_events[event.event_id] = event
    ordered = sorted(
        unique_events.values(),
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


def calculate_activities(dasher_id, activities, windows, cancellation_mode):
    amount_cents = 0
    completed_count = 0
    paid_cancellation_count = 0

    for activity in activities:
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


class RetryingEventClient:
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

        activities = build_activities(events)
        return calculate_activities(
            dasher_id,
            activities,
            windows,
            cancellation_mode,
        )


class IdempotentPayoutIssuer:
    def __init__(self, payment_gateway):
        self.payment_gateway = payment_gateway
        self.records = {}
        self.lock = Lock()

    def issue(self, dasher_id, payout_period, amount_cents):
        if not dasher_id or not payout_period or amount_cents < 0:
            raise ValueError("invalid payout request")

        key = f"{dasher_id}:{payout_period}"

        # ponytail: process-local lock; use a DB unique key and outbox in production.
        with self.lock:
            existing = self.records.get(key)
            if existing is not None:
                if existing.amount_cents != amount_cents:
                    raise IdempotencyConflictError("same key, different amount")
                return existing

            payment_id = self.payment_gateway.issue_payment(
                dasher_id,
                amount_cents,
                key,
            )
            result = IssuedPayout(key, amount_cents, payment_id)
            self.records[key] = result
            return result


class StreamingPayoutAccumulator:
    # New in Follow-up 6: update payout state one ordered event at a time.
    def __init__(
        self,
        dasher_id,
        peak_windows=(),
        cancellation_mode=IGNORE_CANCELLATION,
    ):
        if cancellation_mode not in {
            IGNORE_CANCELLATION,
            FIXED_CANCELLATION,
            DURATION_CANCELLATION,
        }:
            raise ValueError("unknown cancellation mode")
        self.dasher_id = dasher_id
        self.peak_windows = merge_peak_windows(peak_windows)
        self.cancellation_mode = cancellation_mode
        self.open_orders = {}
        self.closed_orders = set()
        self.seen_events = {}
        self.last_event_time = None
        self.amount_cents = 0
        self.completed_count = 0
        self.paid_cancellation_count = 0

    def apply(self, event):
        existing = self.seen_events.get(event.event_id)
        if existing is not None:
            if existing != event:
                raise InvalidTimelineError("event_id reused with different data")
            return
        if self.last_event_time is not None and event.at < self.last_event_time:
            raise LateEventError("event arrived behind the stream position")

        if event.action is EventAction.PICKED_UP:
            if event.order_id in self.open_orders or event.order_id in self.closed_orders:
                raise InvalidTimelineError("duplicate pickup")
            self.open_orders[event.order_id] = event.at
        else:
            start = self.open_orders.get(event.order_id)
            if start is None or event.order_id in self.closed_orders:
                raise InvalidTimelineError("terminal event without pickup")
            if event.at <= start:
                raise InvalidTimelineError("activity must have positive duration")

            self.open_orders.pop(event.order_id)
            self.closed_orders.add(event.order_id)
            if event.action is EventAction.DELIVERED:
                self.amount_cents += interval_pay(start, event.at, self.peak_windows)
                self.completed_count += 1
            elif self.cancellation_mode == DURATION_CANCELLATION:
                self.amount_cents += interval_pay(start, event.at, self.peak_windows)
                self.paid_cancellation_count += 1
            elif self.cancellation_mode == FIXED_CANCELLATION and event.at - start >= 5:
                self.amount_cents += 200
                self.paid_cancellation_count += 1

        self.seen_events[event.event_id] = event
        self.last_event_time = event.at

    def finalize(self):
        if self.open_orders:
            raise InvalidTimelineError("unfinished pickup")
        return PayoutResponse(
            self.dasher_id,
            self.amount_cents,
            self.completed_count,
            self.paid_cancellation_count,
        )


def main():
    accumulator = StreamingPayoutAccumulator(
        "dasher-1",
        [PeakWindow(8, 12)],
    )
    events = [
        OrderEvent("e1", "a", 0, EventAction.PICKED_UP),
        OrderEvent("e2", "b", 5, EventAction.PICKED_UP),
        OrderEvent("e3", "a", 10, EventAction.DELIVERED),
        OrderEvent("e4", "b", 15, EventAction.DELIVERED),
    ]
    for event in events:
        accumulator.apply(event)
    accumulator.apply(events[-1])

    result = accumulator.finalize()
    assert result == PayoutResponse("dasher-1", 780, 2, 0)
    print(result)


if __name__ == "__main__":
    main()
