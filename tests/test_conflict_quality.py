from source_engine.conflict import detect_conflicts
from source_engine.diff import domain_diff


def test_conflict_report_runs():
    report = detect_conflicts()
    assert report["schema"] == "conflict_report_v1"
    assert "conflict_count" in report


def test_diff_identity():
    d = domain_diff(["a.com"], ["a.com"])
    assert d["added_count"] == 0
    assert d["unchanged_count"] == 1
