from source_engine.conflict import detect_conflicts
from source_engine.quality import score_services
from source_engine.diff import domain_diff


def test_conflict_report_runs():
    report = detect_conflicts()
    assert report["schema"] == "conflict_report_v1"
    assert "conflict_count" in report


def test_quality_scores():
    report = score_services()
    assert report["schema"] == "quality_score_v1"
    assert report["summary"]["avg_score"] >= 0
    assert "1688" in report["services"]


def test_diff_identity():
    d = domain_diff(["a.com"], ["a.com"])
    assert d["added_count"] == 0
    assert d["unchanged_count"] == 1
