"""Visible, locally authored contract cases; these are not official tests."""
from custom_practice.runner import Case


def expense(eid, amount, trip="t1", kind="meal", vendor="restaurant", name="Cafe"):
    return dict(expense_id=eid, trip_id=trip, amount_usd=amount,
                expense_type=kind, vendor_type=vendor, vendor_name=name)


BAN_AIR = dict(rule_id="no_airfare", kind="ban", field="expense_type", value="airfare")
BAN_ENT = dict(rule_id="no_entertainment", kind="ban", field="expense_type", value="entertainment")
RESTAURANT = dict(rule_id="restaurant_75", kind="max_amount", limit_usd=75,
                  field="vendor_type", value="restaurant")
SINGLE = dict(rule_id="single_250", kind="max_amount", limit_usd=250)
TRIP = dict(rule_id="trip_2000", kind="trip_total", limit_usd=2000)
MEALS = dict(rule_id="meals_200", kind="trip_total", limit_usd=200,
             field="expense_type", value="meal")
BASE = [RESTAURANT, BAN_AIR, BAN_ENT, SINGLE]
ALL = BASE + [TRIP, MEALS]

TEST_CASES = [
    Case("stage1 empty expenses", {}, (BASE, [])),
    Case("stage1 no rules", {"e1": []}, ([], [expense("e1", 999)])),
    Case("stage1 all initial individual policies",
         {"e1": [], "e2": ["restaurant_75"], "e3": ["no_airfare", "single_250"],
          "e4": ["no_entertainment"]},
         (BASE, [expense("e1", 75), expense("e2", 76),
                 expense("e3", 251, kind="airfare", vendor="airline"),
                 expense("e4", 10, kind="entertainment", vendor="theater")])),
    Case("stage1 exact single cap and zero", {"e1": [], "e2": []},
         ([SINGLE], [expense("e1", 250), expense("e2", 0)])),
    Case("stage1 multiple violations preserve rule order",
         {"e1": ["single_250", "restaurant_75", "no_entertainment"]},
         ([SINGLE, RESTAURANT, BAN_ENT], [expense("e1", 300, kind="entertainment")])),
    Case("stage1 filter does not match", {"e1": []},
         ([RESTAURANT], [expense("e1", 100, vendor="hotel")])),
    Case("stage1 generic vendor name and type bans", {"e1": ["name", "type"], "e2": []},
         ([dict(rule_id="name", kind="ban", field="vendor_name", value="ReviewCo"),
           dict(rule_id="type", kind="ban", field="vendor_type", value="casino")],
          [expense("e1", 0, vendor="casino", name="ReviewCo"), expense("e2", 10)])),
    Case("stage1 external rule without changing evaluator", {"e1": ["external_review"], "e2": []},
         ([], [expense("e1", 1, name="ReviewCo"), expense("e2", 1)]),
         {"extension": True}),
    Case("stage2 exact trip cap", {"e1": [], "e2": []},
         ([TRIP], [expense("e1", 1200), expense("e2", 800)])),
    Case("stage2 over cap attributes all trip expenses", {"e1": ["trip_2000"], "e2": ["trip_2000"]},
         ([TRIP], [expense("e1", 1200), expense("e2", 801)])),
    Case("stage2 interleaved independent trips", {"e1": ["trip_2000"], "e2": [], "e3": ["trip_2000"]},
         ([TRIP], [expense("e1", 1500), expense("e2", 1999, trip="t2"),
                   expense("e3", 600)])),
    Case("stage2 meal cap exact", {"e1": [], "e2": []},
         ([MEALS], [expense("e1", 100), expense("e2", 100)])),
    Case("stage2 filtered aggregation marks matching expenses only",
         {"e1": ["meals_200"], "e2": [], "e3": ["meals_200"]},
         ([MEALS], [expense("e1", 100), expense("e2", 999, kind="lodging"),
                    expense("e3", 101)])),
    Case("stage2 all six policies interact",
         {"e1": ["restaurant_75", "meals_200"], "e2": ["restaurant_75", "meals_200"],
          "e3": ["no_airfare", "single_250"]},
         (ALL, [expense("e1", 120), expense("e2", 100),
                expense("e3", 1000, trip="t2", kind="airfare", vendor="airline")])),
    Case("stage2 rejected expenses still count in totals",
         {"e1": ["no_airfare", "trip_2000"], "e2": ["trip_2000"]},
         ([BAN_AIR, TRIP], [expense("e1", 1900, kind="airfare"), expense("e2", 101)])),
    Case("stage2 repeated evaluation is stateless", {"e1": ["meals_200"]},
         ([MEALS], [expense("e1", 201)]), {"repeat": True}),
    Case("stage3 API filtered vendor total",
         {"e1": ["hotel_100"], "e2": [], "e3": ["hotel_100"]},
         ([dict(rule_id="hotel_100", kind="trip_total", limit_usd=100,
                field="vendor_type", value="hotel")],
          [expense("e1", 60, vendor="hotel"), expense("e2", 500),
           expense("e3", 41, vendor="hotel")])),
]

TEST_CASES.append(Case(
    "stage2 zero expense in exceeded trip",
    {"e1": ["cap"], "e2": ["cap"], "e3": ["cap"]},
    ([dict(rule_id="cap", kind="trip_total", limit_usd=2000)],
     [expense("e1", 2000),
      expense("e2", 1), expense("e3", 0)]),
))
