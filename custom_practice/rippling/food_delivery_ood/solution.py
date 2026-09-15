"""Rippling Q010 — Food Delivery OOD

Description
-----------
Build a food delivery system that tracks delivery jobs and pays drivers.
Add a delivery, record when it finishes, and pay completed deliveries up to
an inclusive cutoff time. Each delivery must be paid only once.

The reports name AddDelivery, RecordDelivery and PayUpto, but do not give
parameters or payment semantics. The following is our local practice contract,
not a recovered verbatim interview prompt. AddDelivery creates a delivery job;
it does not register a driver.

APIs
----
AddDelivery(delivery_id: str, driver_id: str, amount: int) -> None
    Register an unfinished delivery with its driver and fixed payment amount.
    Amount is an integer number of dollars, e.g. 20. No rate calculation.

RecordDelivery(delivery_id: str, end_time: int) -> None
    Mark the delivery completed at end_time. It is now eligible for payment.
    Completion records can arrive out of order.

PayUpto(cutoff: int) -> dict[str, int]
    Pay every recorded, unpaid delivery whose end_time <= cutoff.
    Return {driver_id: amount_paid_in_this_call}, summing multiple deliveries
    for the same driver. An empty payout returns {}. Dictionary order is irrelevant.
    This updates in-memory payment state; it does not transfer real money.

Input assumptions — confirm verbally before coding
--------------------------------------------------
- Inputs have the declared types; amounts and times are nonnegative integers.
- Delivery IDs are globally unique. Driver IDs may appear in multiple deliveries.
- RecordDelivery refers to an added delivery and is called once per delivery.
- All timestamps use the same unit. Payment cutoffs need not be increasing.
- A delivery added but not recorded is not payable.
- Repeating PayUpto does not pay an already paid delivery again.
- A completion recorded after an earlier PayUpto is paid by the next eligible
  PayUpto call, even if its end_time is older than that earlier cutoff.
- All calls are sequential. No input checks, database, concurrency or external API.

Example 1
---------
Input:
    system = FoodDeliverySystem()
    system.AddDelivery("d1", "alice", 20)
    system.AddDelivery("d2", "alice", 30)
    system.AddDelivery("d3", "bob", 15)
    system.RecordDelivery("d2", 20)
    system.RecordDelivery("d3", 10)
    system.RecordDelivery("d1", 10)
    system.PayUpto(10)
    system.PayUpto(10)
    system.PayUpto(20)
Output:
    {'alice': 20, 'bob': 15}
    {}
    {'alice': 30}
Explanation: the cutoff includes time 10, and a delivery is never paid twice.

Example 2 — Late completion record
----------------------------------
Input:
    system = FoodDeliverySystem()
    system.AddDelivery("d1", "alice", 20)
    system.PayUpto(100)
    system.RecordDelivery("d1", 5)
    system.PayUpto(100)
Output:
    {}
    {'alice': 20}

Complexity
----------
With N outstanding deliveries and K deliveries paid in one call:
- AddDelivery: O(1) average time; O(1) additional space.
- RecordDelivery: O(log N) time; O(1) additional space, excluding heap resizing.
- PayUpto: O(1 + K log N) time; O(D) result space for D paid drivers.
- Total stored state: O(N). Each completed delivery enters and leaves the heap once.
"""

from dataclasses import dataclass
import heapq


@dataclass
class Delivery:
    driver_id: str
    amount: int


class FoodDeliverySystem:
    def __init__(self):
        self.pending = {}
        self.unpaid = []

    def AddDelivery(self, delivery_id: str, driver_id: str, amount: int):
        self.pending[delivery_id] = Delivery(driver_id, amount)

    def RecordDelivery(self, delivery_id: str, end_time: int):
        delivery = self.pending.pop(delivery_id)
        # 按完成时间取最早的配送；唯一 ID 处理完成时间相同的情况。
        heapq.heappush(self.unpaid, (end_time, delivery_id, delivery))

    def PayUpto(self, cutoff: int) -> dict[str, int]:
        payments = {}
        while self.unpaid:
            end_time, delivery_id, delivery = self.unpaid[0]
            if end_time > cutoff:
                break

            # 从未支付队列移除，所以后续调用不会重复支付。
            heapq.heappop(self.unpaid)
            driver_id = delivery.driver_id
            if driver_id not in payments:
                payments[driver_id] = 0
            payments[driver_id] += delivery.amount

        return payments


if __name__ == "__main__":
    system = FoodDeliverySystem()
    print(system.PayUpto(10))  # {}

    system.AddDelivery("d1", "alice", 20)
    system.AddDelivery("d2", "alice", 30)
    system.AddDelivery("d3", "bob", 15)
    print(system.PayUpto(100))  # {} — none completed yet

    # Out-of-order completion records, with two deliveries finishing at time 10.
    system.RecordDelivery("d2", 20)
    system.RecordDelivery("d3", 10)
    system.RecordDelivery("d1", 10)
    print(system.PayUpto(9))   # {}
    print(system.PayUpto(10))  # {'alice': 20, 'bob': 15}
    print(system.PayUpto(10))  # {} — no duplicate payment
    print(system.PayUpto(20))  # {'alice': 30}

    # Multiple deliveries for one driver are summed in the same payout.
    system.AddDelivery("d4", "alice", 12)
    system.AddDelivery("d5", "alice", 8)
    system.RecordDelivery("d4", 30)
    system.RecordDelivery("d5", 40)
    print(system.PayUpto(40))  # {'alice': 20}

    # Late record with an older completion time, followed by a smaller cutoff.
    system.AddDelivery("d6", "bob", 7)
    system.RecordDelivery("d6", 5)
    print(system.PayUpto(5))  # {'bob': 7}
    print(system.PayUpto(100))  # {}
