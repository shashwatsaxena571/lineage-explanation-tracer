"""Scenario: a loan model makes a bad prediction. The top feature turns out to be
'debt_ratio', which derives from the 'transactions_raw' table — and that table
failed its quality check yesterday.
"""
import sys, json; sys.path.insert(0, "src")
from tracer import LineageGraph, ExplanationTracer

g = LineageGraph()
g.add_source("customers_raw", last_updated="2026-07-27", quality_status="OK")
g.add_source("transactions_raw", last_updated="2026-07-25", quality_status="FAILED: 34% nulls in amount")
g.add_source("bureau_data", last_updated="2026-07-27", quality_status="OK")

g.add_feature("monthly_income", ["customers_raw"], "avg(salary) last 3m")
g.add_feature("total_debt", ["transactions_raw"], "sum(amount) where type=debit")
g.add_feature("debt_ratio", ["total_debt", "monthly_income"], "total_debt / monthly_income")
g.add_feature("credit_score", ["bureau_data"], "passthrough")

attributions = [
    {"feature": "debt_ratio", "attribution": 0.61},
    {"feature": "credit_score", "attribution": 0.28},
    {"feature": "monthly_income", "attribution": 0.11},
]

report = ExplanationTracer(g).root_cause_report(attributions)
print(json.dumps(report, indent=2))
print("\nThe story is clear: debt_ratio drove the prediction, and its upstream "
      "table (transactions_raw) was corrupt. End-to-end root cause — in seconds.")
