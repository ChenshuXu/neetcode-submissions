"""Follow-up 1: add non-stacking 2x peak-pay windows.

Evolution from Base:
- Keep the completed-delivery duration calculation.
- Add peak windows where overlapping minutes earn one extra base rate.
- Merge overlapping windows first so peak multipliers never stack.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Optional


RATE_CENTS_PER_MINUTE = 30


class DeliveryStatus(Enum):
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    ACTIVE = "active"


@dataclass
class Delivery:
    delivery_id: str
    accepted_at: int
    completed_at: Optional[int]
    status: DeliveryStatus


@dataclass
class PeakWindow:
    start: int
    end: int


@dataclass
class PayoutResponse:
    dasher_id: str
    amount_cents: int
    completed_delivery_count: int


class DeliveryClientError(RuntimeError):
    pass


class InvalidDeliveryError(ValueError):
    pass


class PayoutUnavailableError(RuntimeError):
    pass


def merge_peak_windows(windows):
    # New in Follow-up 1: normalize overlapping windows into disjoint ranges.
    ordered = sorted(windows, key=lambda window: window.start)
    return merge_sorted_peak_windows(ordered)


def merge_sorted_peak_windows(windows):
    merged = []

    for window in windows:
        if window.end <= window.start:
            raise ValueError("peak windows must have positive duration")

        if not merged or window.start > merged[-1].end:
            merged.append(PeakWindow(window.start, window.end))
        else:
            merged[-1].end = max(merged[-1].end, window.end)

    return merged


def interval_pay(start, end, peak_windows):
    # New in Follow-up 1: base pay plus extra pay for peak overlap only.
    if end <= start:
        raise InvalidDeliveryError("delivery must have positive duration")

    amount_cents = (end - start) * RATE_CENTS_PER_MINUTE

    # ponytail: O(deliveries * peak windows); use one boundary sweep if large.
    for window in peak_windows:
        overlap_start = max(start, window.start)
        overlap_end = min(end, window.end)
        if overlap_start < overlap_end:
            peak_minutes = overlap_end - overlap_start
            amount_cents += peak_minutes * RATE_CENTS_PER_MINUTE

    return amount_cents


class PayoutService:
    def __init__(self, delivery_client):
        self.delivery_client = delivery_client

    def get_payout(self, dasher_id, peak_windows=()):
        if not isinstance(dasher_id, str) or not dasher_id.strip():
            raise ValueError("dasher_id must not be blank")

        windows = merge_peak_windows(peak_windows)

        try:
            deliveries = self.delivery_client.list_deliveries(dasher_id)
        except DeliveryClientError as error:
            raise PayoutUnavailableError("delivery service unavailable") from error

        amount_cents = 0
        completed_count = 0

        for delivery in deliveries:
            if delivery.status is not DeliveryStatus.COMPLETED:
                continue
            if delivery.completed_at is None:
                raise InvalidDeliveryError(delivery.delivery_id)

            amount_cents += interval_pay(
                delivery.accepted_at,
                delivery.completed_at,
                windows,
            )
            completed_count += 1

        return PayoutResponse(dasher_id, amount_cents, completed_count)

    def get_payout_two(self, dasher_id, peak_windows=()):
        """Use O(P + D log P) time when peak_windows are sorted by start."""
        if not isinstance(dasher_id, str) or not dasher_id.strip():
            raise ValueError("dasher_id must not be blank")

        windows = merge_sorted_peak_windows(peak_windows)
        starts = [window.start for window in windows]
        peak_prefix = [0]
        for window in windows:
            peak_prefix.append(peak_prefix[-1] + window.end - window.start)

        def find_last_window_starting_at_or_before(timestamp):
            left = 0
            right = len(starts) - 1
            answer = -1

            while left <= right:
                middle = (left + right) // 2
                if starts[middle] <= timestamp:
                    answer = middle
                    left = middle + 1
                else:
                    right = middle - 1

            return answer

        def peak_minutes_before(timestamp):
            index = find_last_window_starting_at_or_before(timestamp)
            if index < 0:
                return 0

            window = windows[index]
            minutes_in_window = min(timestamp, window.end) - window.start
            return peak_prefix[index] + minutes_in_window

        try:
            deliveries = self.delivery_client.list_deliveries(dasher_id)
        except DeliveryClientError as error:
            raise PayoutUnavailableError("delivery service unavailable") from error

        amount_cents = 0
        completed_count = 0

        for delivery in deliveries:
            if delivery.status is not DeliveryStatus.COMPLETED:
                continue
            if delivery.completed_at is None:
                raise InvalidDeliveryError(delivery.delivery_id)

            delivery_minutes = delivery.completed_at - delivery.accepted_at
            if delivery_minutes <= 0:
                raise InvalidDeliveryError("delivery must have positive duration")

            peak_minutes = peak_minutes_before(
                delivery.completed_at
            ) - peak_minutes_before(delivery.accepted_at)
            amount_cents += (
                delivery_minutes + peak_minutes
            ) * RATE_CENTS_PER_MINUTE
            completed_count += 1

        return PayoutResponse(dasher_id, amount_cents, completed_count)


class FakeDeliveryClient:
    def __init__(self, deliveries):
        self.deliveries = deliveries

    def list_deliveries(self, dasher_id):
        return self.deliveries


def main():
    deliveries = [
        Delivery("d1", 0, 10, DeliveryStatus.COMPLETED),
        Delivery("d2", 5, 15, DeliveryStatus.COMPLETED),
    ]
    peak_windows = [PeakWindow(8, 12), PeakWindow(10, 14)]
    service = PayoutService(FakeDeliveryClient(deliveries))
    result = service.get_payout("dasher-1", peak_windows)
    result_two = service.get_payout_two("dasher-1", peak_windows)
    assert result == PayoutResponse("dasher-1", 840, 2)
    assert result_two == result
    print(result)


if __name__ == "__main__":
    main()
