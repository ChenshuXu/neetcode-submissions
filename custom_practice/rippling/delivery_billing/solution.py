"""Rippling Delivery Billing — actual interview, 2026-09-15.

See README.md for the reconstructed problem; run run_tests.py for checks.

Assumptions beyond recovered evidence: nonnegative finite rates, comparable UTC
datetimes, latest call wins for equal effective times, final rounding is half-up.
The supplied tests do not establish the exact half-cent tie rule.
"""

from bisect import bisect_right
from datetime import datetime, timedelta, timezone
from math import isfinite


class BillingSystem:
    def __init__(self):
        self.driver_info = {}
        self.delivery_ids = set()
        self.total_cost: float = 0.0  # Dollars; do not round individual deliveries.

    @staticmethod
    def _rate(value):
        rate = float(value)
        if not isfinite(rate) or rate < 0:
            raise ValueError("Rate must be finite and nonnegative")
        return rate

    def add_driver(self, driver_id, usd_hourly_rate_per_delivery):
        if driver_id in self.driver_info:
            raise ValueError("Driver already exists")
        rate = self._rate(usd_hourly_rate_per_delivery)
        self.driver_info[driver_id] = ([], [rate])

    def update_driver_rate(self, driver_id, new_rate, effective_time):
        rate = self._rate(new_rate)
        times, rates = self.driver_info[driver_id]
        index = bisect_right(times, effective_time)
        times.insert(index, effective_time)
        rates.insert(index + 1, rate)

    def record_delivery(self, delivery_id, driver_id, start_time, end_time):
        if delivery_id in self.delivery_ids:
            return
        duration = end_time - start_time
        if duration < timedelta(0):
            raise ValueError("End precedes start")
        if duration > timedelta(hours=3):
            return
        times, rates = self.driver_info[driver_id]
        index = bisect_right(times, start_time)
        hours = duration.total_seconds() / 3600
        self.total_cost += rates[index] * hours
        self.delivery_ids.add(delivery_id)

    def get_total_cost(self):
        # ponytail: float can drift near half cents; use fixed-point if exact ties matter.
        cents = int(self.total_cost * 100 + 0.5)
        return f"{cents // 100}.{cents % 100:02d}"



if __name__ == "__main__":
    billing = BillingSystem()
    billing.add_driver("driver-1", "15.15")
    start = datetime(1970, 1, 1, tzinfo=timezone.utc)
    billing.record_delivery("d1", "driver-1", start, start + timedelta(minutes=90))
    print(billing.get_total_cost())  # 22.73 (half-up assumption)
    billing.record_delivery("d2", "driver-1", start, start + timedelta(minutes=30))
    print(billing.get_total_cost())  # 30.30: no per-delivery rounding
