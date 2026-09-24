"""Recovered call sequence plus local boundary cases, not official hidden tests."""
from datetime import datetime, timedelta, timezone
from runner import Case


def at(hours=0, minutes=0, seconds=0):
    return datetime(1970, 1, 1, tzinfo=timezone.utc) + timedelta(
        hours=hours, minutes=minutes, seconds=seconds
    )


def delivery(delivery_id, driver_id, start, end):
    return ("record_delivery", (delivery_id, driver_id, start, end))


QUERY = ("get_total_cost", ())
CASES = [
    Case("recovered interview sequence (half-up assumed at 57.925)",
         ["0.00", "35.10", "35.20", "57.93", "65.90", "65.90", "81.05", "111.05"],
         ([
             *[("add_driver", (i, rate)) for i, rate in enumerate(
                 ["35.10", "15.15", "8.55", "11.28", "0.10"], 1)],
             QUERY,
             delivery("d1", 1, at(), at(1)), QUERY,
             delivery("d2", 5, at(), at(1)), QUERY,
             delivery("d3", 2, at(), at(1, 30)), QUERY,
             delivery("d4", 2, at(1, 13, 20), at(1, 43, 20)),
             delivery("d5", 5, at(1), at(2)),
             delivery("d6", 5, at(2), at(3)),
             delivery("d1", 1, at(2, 46, 39), at(3, 46, 39)),
             delivery("d7", 5, at(3), at(4)),
             delivery("d8", 5, at(4), at(5)), QUERY,
             ("update_driver_rate", (2, "30", at(4, 30))), QUERY,
             delivery("d10", 2, at(4, 15), at(5, 15)), QUERY,
             delivery("d9", 2, at(4, 40), at(5, 40)), QUERY,
         ],)),
    Case("fractional cents, read isolation, overlap and global duplicate ID",
         ["22.73", "22.73", "30.30", "30.30"], ([
             ("add_driver", (1, "15.15")),
             delivery("a", 1, at(), at(1, 30)), QUERY, QUERY,
             delivery("b", 1, at(1), at(1, 30)), QUERY,
             delivery("b", 999, at(), at(2)), QUERY,
         ],)),
    Case("historical rates, unordered updates, inclusive boundary, frozen charges",
         ["15.15", "35.15", "65.15", "65.15", "105.15"], ([
             ("add_driver", (1, "15.15")),
             ("update_driver_rate", (1, "30", at(2))),
             ("update_driver_rate", (1, "20", at(1))),
             delivery("a", 1, at(0, 30), at(1, 30)), QUERY,
             delivery("b", 1, at(1), at(2)), QUERY,
             delivery("c", 1, at(2), at(3)), QUERY,
             ("update_driver_rate", (1, "40", at(2))), QUERY,
             delivery("d", 1, at(2), at(3)), QUERY,
         ],)),
    Case("seconds, three-hour limit, ignored ID retry, zero and midnight",
         ["0.01", "0.01", "54.01", "54.01", "72.01", "72.01", "90.01"], ([
             ("add_driver", (1, "18")),
             delivery("a", 1, at(), at(seconds=1)), QUERY,
             delivery("b", 1, at(seconds=1), at(seconds=2)), QUERY,
             delivery("c", 1, at(), at(3)), QUERY,
             delivery("long", 1, at(), at(3, seconds=1)), QUERY,
             delivery("long", 1, at(), at(1)), QUERY,
             delivery("zero", 1, at(), at()), QUERY,
             delivery("midnight", 1, at(23, 30), at(24, 30)), QUERY,
         ],)),
    Case("local invalid-input policy and failed ID retry",
         ["ValueError", "ValueError", "ValueError", "KeyError", "0.00", "18.00"], ([
             ("add_driver", (1, "18")),
             ("add_driver", (1, "20")),
             ("update_driver_rate", (1, "-1", at())),
             delivery("bad", 1, at(2), at(1)),
             delivery("unknown", 999, at(), at(1)), QUERY,
             delivery("bad", 1, at(), at(1)), QUERY,
         ],)),
]
