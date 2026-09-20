from __future__ import annotations

from pathlib import Path

from adapters.official_json.parser import extract_domains_from_official_json
from source_engine.extract import extract_domains_from_html
from source_engine.policy import is_excluded, load_exclusion_suffixes


FIXTURES = Path("tests/fixtures/1688")


def test_1688_html_fixture_extracts_service_domains_only():
    html = (FIXTURES / "official_open_v1.html").read_text(encoding="utf-8")
    expected = [
        x.strip()
        for x in (FIXTURES / "official_open_v1.expected.txt").read_text().splitlines()
        if x.strip()
    ]
    domains = extract_domains_from_html(
        html, "https://open.1688.com/", (), ("1688.com",)
    )
    blocked = load_exclusion_suffixes()
    domains = [d for d in domains if not is_excluded(d, blocked)]
    assert domains == expected
    assert "g.alicdn.com" not in domains
    assert "evil.example.com" not in domains


def test_1688_json_fixture_extracts_gateway():
    body = (FIXTURES / "official_endpoints_v1.json").read_bytes()
    expected = [
        x.strip()
        for x in (FIXTURES / "official_endpoints_v1.expected.txt").read_text().splitlines()
        if x.strip()
    ]
    domains = extract_domains_from_official_json(body, (), ("1688.com",))
    blocked = load_exclusion_suffixes()
    domains = [d for d in domains if not is_excluded(d, blocked)]
    assert domains == expected
    assert "g.alicdn.com" not in domains
