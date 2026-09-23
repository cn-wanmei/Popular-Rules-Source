from pathlib import Path

from source_engine.adapters import _domains_from_rule_text, _domains_from_values, validate_adapter_contract


def test_adapter_contract_is_complete():
    assert validate_adapter_contract() == []


def test_structured_adapter_domain_filter():
    found = _domains_from_values(
        ["https://open.taobao.com/", "https://example.org/"],
        ("open.taobao.com",),
        (),
    )
    assert found == ["open.taobao.com"]


def test_upstream_rule_domain_filter():
    found = _domains_from_values(
        ["DOMAIN-SUFFIX,drive.google.com\nDOMAIN,www.googleapis.com\n+.ignored.example"],
        ("www.googleapis.com",),
        ("drive.google.com",),
    )
    assert found == ["drive.google.com", "www.googleapis.com"]


def test_official_fixture_exists():
    assert Path("tests/fixtures/official_web.html").exists()


def test_upstream_fixture_exists():
    assert Path("tests/fixtures/upstream_rule.list").exists()


def test_upstream_rule_parser_handles_rule_syntax():
    found = _domains_from_rule_text(
        "DOMAIN-SUFFIX,drive.google.com\nDOMAIN,www.googleapis.com\nHOST-SUFFIX,music.youtube.com\n+.ignored.example\n",
        ("www.googleapis.com",),
        ("drive.google.com", "music.youtube.com"),
    )
    assert found == ["drive.google.com", "music.youtube.com", "www.googleapis.com"]


def test_upstream_rule_parser_handles_geosite_entries():
    found = _domains_from_rule_text(
        "+.feishu.cn\nazure.microsoft.com\nazure\n",
        ("azure.microsoft.com",),
        ("feishu.cn",),
    )
    assert found == ["azure.microsoft.com", "feishu.cn"]
