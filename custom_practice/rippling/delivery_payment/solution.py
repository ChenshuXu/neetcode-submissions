"""Rippling Q048 — Delivery Payment

Description
-----------
Track drivers and their recorded deliveries, calculate total delivery cost,
pay completed deliveries up to a cutoff, and report unpaid cost. Then find
how many DISTINCT drivers were simultaneously delivering in the last 24 hours,
including the time intervals when that maximum was reached.

Existing reports disclose the API families and follow-ups, but not complete
parameters, rates or boundary semantics. The following is a local practice
contract. This is separate from Q010: add_driver registers a driver here.

Stage 1 — Cost tracking
    add_driver(driver_id) -> None
    add_delivery(driver_id, start_time, end_time) -> None
    get_total_cost() -> int

Stage 2 — Payments
    pay_upto_time(cutoff) -> int: return the amount newly paid in this call.
    get_total_unpaid_cost() -> int

Stage 3 — Last 24 hours
    get_maximum_simultaneous_drivers_in_last_24hrs(current_time) -> int
    get_peak_driver_intervals_in_last_24hrs(current_time)
        -> (maximum_count, [(start, end), ...])
    The second method implements the interval-returning variant reported in
    S-W3-040; its method name and output format are local practice choices.

Input assumptions — confirm verbally before coding
--------------------------------------------------
- IDs are strings. Times are integer minutes on one shared timeline.
- Drivers are registered once, before their deliveries. start_time < end_time.
- Each delivery is recorded once. Records may arrive out of chronological order.
- For simple integer arithmetic, every driver earns $1 per minute PER DELIVERY.
  cost = end_time - start_time. Rates were not disclosed by the reports.
  Overlapping deliveries are billed separately, even for the same driver.
- Recording a delivery adds its FULL cost to total and unpaid cost.
- Pay only recorded, unpaid deliveries with end_time <= cutoff. No partial pay
  for deliveries crossing the cutoff; repeated calls must not pay twice.
- Late records can be paid on the next eligible call. No increasing-cutoff rule.
- Total cost is lifetime cost; paying never reduces it.
- The analytics window is [current_time - 1440, current_time).
  Delivery intervals are [start_time, end_time); clip them to the window.
- Count each driver once even when their deliveries overlap. Touching intervals
  do not overlap. Paid deliveries still count in historical analytics.
- Return all maximal positive-length peak intervals, sorted by start time.
  Merge adjacent peak intervals even if the set of drivers changes.
  No activity returns (0, []); the count-only method returns 0.
- Inputs are valid. No runtime input checks, real money transfers or concurrency.

Example
-------
Input:
    system.add_driver("alice")
    system.add_driver("bob")
    system.add_delivery("alice", 10, 30)
    system.add_delivery("bob", 20, 40)
    system.get_total_cost()
    system.pay_upto_time(30)
    system.get_total_unpaid_cost()
    system.get_peak_driver_intervals_in_last_24hrs(1440)
Output:
    40
    20
    20
    (2, [(20, 30)])

Complexity
----------
N = recorded deliveries, U = unpaid deliveries, K = deliveries paid this call.
add_driver: O(1) average. add_delivery: O(log U).
Cost getters: O(1). pay_upto_time: O(1 + K log U).
Either analytics query: O(N log N) time, O(N) temporary space.
Stored state: O(N + number of drivers); history is retained for analytics.
"""

import heapq


class DeliveryPayment:
    def __init__(self):
        self.deliveries = {}
        self.unpaid = []
        self.total_cost = 0
        self.unpaid_cost = 0

    def add_driver(self, driver_id: str):
        self.deliveries[driver_id] = []

    def add_delivery(self, driver_id: str, start_time: int, end_time: int):
        cost = end_time - start_time
        self.deliveries[driver_id].append((start_time, end_time))
        heapq.heappush(self.unpaid, (end_time, cost))
        self.total_cost += cost
        self.unpaid_cost += cost

    def get_total_cost(self) -> int:
        return self.total_cost

    def pay_upto_time(self, cutoff: int) -> int:
        paid = 0
        while self.unpaid:
            end_time, cost = self.unpaid[0]
            if end_time > cutoff:
                break
            heapq.heappop(self.unpaid)
            paid += cost
        self.unpaid_cost -= paid
        return paid

    def get_total_unpaid_cost(self) -> int:
        return self.unpaid_cost

    def get_maximum_simultaneous_drivers_in_last_24hrs(self, current_time: int) -> int:
        maximum, intervals = self.get_peak_driver_intervals_in_last_24hrs(current_time)
        return maximum

    def get_peak_driver_intervals_in_last_24hrs(self, current_time: int):
        window_start = current_time - 1440
        events = []
        for driver_id, deliveries in self.deliveries.items():
            for start_time, end_time in deliveries:
                start = max(start_time, window_start)
                end = min(end_time, current_time)
                if start < end:
                    events.append((start, driver_id, 1))
                    events.append((end, driver_id, -1))
        events.sort()

        # 每位司机当前进行中的配送数；只有 0 -> 1 / 1 -> 0 才改变司机总数。
        active_deliveries = {}
        active_drivers = 0
        maximum = 0
        intervals = []
        index = 0
        while index < len(events):
            time = events[index][0]
            # 同一时刻的开始和结束全部处理后，再统计到下一个时刻的区间。
            while index < len(events) and events[index][0] == time:
                _, driver_id, change = events[index]
                before = active_deliveries.get(driver_id, 0)
                after = before + change
                active_deliveries[driver_id] = after
                if before == 0 and after > 0:
                    active_drivers += 1
                elif before > 0 and after == 0:
                    active_drivers -= 1
                index += 1

            if index == len(events):
                break
            next_time = events[index][0]
            if active_drivers > maximum:
                maximum = active_drivers
                intervals = [(time, next_time)]
            elif active_drivers == maximum and maximum > 0:
                if intervals and intervals[-1][1] == time:
                    start, end = intervals[-1]
                    intervals[-1] = (start, next_time)
                else:
                    intervals.append((time, next_time))

        return maximum, intervals


if __name__ == "__main__":
    system = DeliveryPayment()
    print(system.get_total_cost())  # 0
    print(system.get_peak_driver_intervals_in_last_24hrs(1440))  # (0, [])

    system.add_driver("alice")
    system.add_driver("bob")
    system.add_driver("carol")
    system.add_delivery("alice", 20, 40)
    system.add_delivery("alice", 10, 30)
    system.add_delivery("bob", 20, 35)
    system.add_delivery("carol", 35, 50)
    print(system.get_total_cost())  # 70
    print(system.get_total_unpaid_cost())  # 70
    print(system.pay_upto_time(29))  # 0 — no partial payment
    print(system.pay_upto_time(30))  # 20 — inclusive cutoff
    print(system.pay_upto_time(30))  # 0 — no duplicate payment
    print(system.get_total_unpaid_cost())  # 50
    print(system.pay_upto_time(50))  # 50
    print(system.get_total_cost())  # 70 — lifetime total does not change
    print(system.get_total_unpaid_cost())  # 0

    # Alice's overlapping jobs count as one driver; Bob ends when Carol starts.
    print(system.get_maximum_simultaneous_drivers_in_last_24hrs(1440))  # 2
    print(system.get_peak_driver_intervals_in_last_24hrs(1440))  # (2, [(20, 40)])
    print(system.get_peak_driver_intervals_in_last_24hrs(1470))  # (2, [(30, 40)])
    print(system.get_peak_driver_intervals_in_last_24hrs(1490))  # (0, [])

    system.add_delivery("bob", 1, 5)  # Late record older than the previous cutoff.
    print(system.pay_upto_time(5))  # 4
    print(system.get_total_unpaid_cost())  # 0

    separate = DeliveryPayment()
    separate.add_driver("alice")
    separate.add_delivery("alice", -10, 10)
    separate.add_delivery("alice", 20, 30)
    separate.add_delivery("alice", 1430, 1450)
    print(separate.get_peak_driver_intervals_in_last_24hrs(1440))
    # (1, [(0, 10), (20, 30), (1430, 1440)]) — clip both window boundaries
