from source_engine.diff import domain_diff
from source_engine.tombstone import filter_revoked, revoke_domain, load_revoked_domains
from source_engine.overrides import apply_overrides


def test_domain_diff():
    d = domain_diff(["a.com", "b.com"], ["b.com", "c.com"])
    assert d["added"] == ["c.com"]
    assert d["removed"] == ["a.com"]
    assert d["unchanged"] == ["b.com"]


def test_tombstone_filter(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    (tmp_path / "tombstones").mkdir()
    revoke_domain("demo", "bad.example.com", reason_type="incorrect_attribution")
    assert "bad.example.com" in load_revoked_domains("demo")
    kept = filter_revoked("demo", {"bad.example.com", "good.example.com"})
    assert kept == {"good.example.com"}


def test_overrides():
    domains = {"a.com", "b.com"}
    out = apply_overrides(
        domains,
        [
            {"asset": "c.com", "action": "include"},
            {"asset": "a.com", "action": "exclude"},
        ],
    )
    assert out == {"b.com", "c.com"}
