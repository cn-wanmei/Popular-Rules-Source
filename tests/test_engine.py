from __future__ import annotations

from source_engine.normalize import host_allowed, normalize_domain, service_asset_id
from source_engine.policy import assess_count_change, is_excluded, load_exclusion_suffixes
from source_engine.validate import validate_config


def test_normalize_domain_basic():
    assert normalize_domain("HTTPS://Open.Taobao.com/path") == "open.taobao.com"
    assert normalize_domain("open.taobao.com.") == "open.taobao.com"
    assert normalize_domain("127.0.0.1") is None
    assert normalize_domain("localhost") is None
    assert normalize_domain("example.com") is None


def test_host_allowed():
    assert host_allowed("api.taobao.com", (), ("taobao.com",))
    assert host_allowed("mail.qq.com", ("mail.qq.com",), ())
    assert not host_allowed("evil.com", (), ("taobao.com",))


def test_asset_id_stable():
    a = service_asset_id("taobao", "api.taobao.com")
    b = service_asset_id("taobao", "api.taobao.com")
    assert a == b
    assert a.startswith("sha256:")


def test_change_gates():
    assert assess_count_change(100, 0, 0.5, 5.0).status == "BLOCK_EMPTY"
    assert assess_count_change(100, 40, 0.5, 5.0).status == "REVIEW_REMOVAL"
    assert assess_count_change(10, 80, 0.5, 5.0).status == "REVIEW_GROWTH"
    assert assess_count_change(10, 11, 0.5, 5.0).status == "OK"


def test_exclusions_loaded():
    blocked = load_exclusion_suffixes()
    assert "alicdn.com" in blocked or "cloudflare.com" in blocked
    assert is_excluded("static.alicdn.com", ("alicdn.com",))
    assert not is_excluded("open.taobao.com", ("alicdn.com",))


def test_validate_config_passes():
    errors = validate_config()
    assert errors == [], errors
