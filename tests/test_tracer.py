import sys; sys.path.insert(0, "src")
from tracer import LineageGraph, ExplanationTracer

def test_flags_bad_source():
    g = LineageGraph()
    g.add_source("bad", "2026-01-01", "FAILED: nulls")
    g.add_feature("f1", ["bad"], "t")
    rep = ExplanationTracer(g).root_cause_report([{"feature": "f1", "attribution": 1.0}])
    assert rep[0]["flag"] == "INVESTIGATE"
