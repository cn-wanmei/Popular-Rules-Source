from pathlib import Path

from source_engine.adapters import _domains_from_values, validate_adapter_contract


def test_adapter_contract_is_complete():
    assert validate_adapter_contract() == []


def test_structured_adapter_domain_filter():
    found = _domains_from_values(
        ["https://open.taobao.com/", "https://example.org/"],
        ("open.taobao.com",),
        (),
    )
    assert found == ["open.taobao.com"]


def test_official_fixture_exists():
    assert Path("tests/fixtures/official_web.html").exists()
