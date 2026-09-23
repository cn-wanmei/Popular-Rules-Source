from source_engine.adapters import AdapterExtraction
from source_engine import build as build_module


def test_build_accumulates_domains_from_successful_adapter(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)
    (tmp_path / "VERSION").write_text("0.5.0\n", encoding="utf-8")

    monkeypatch.setattr(
        build_module,
        "load_services",
        lambda path="config/services.yaml": {
            "services": {
                "taobao": {
                    "official_sources": ["https://open.taobao.com/"],
                    "allowed_host_exact": ["open.taobao.com"],
                    "allowed_host_suffixes": [],
                }
            }
        },
    )
    monkeypatch.setattr(
        build_module,
        "load_yaml",
        lambda path: {
            "runtime": {
                "timeout_seconds": 1,
                "retry_attempts": 1,
                "retry_backoff_seconds": 0,
                "max_bytes": 1024,
                "user_agent": "test",
            }
        } if "source_adapters" in path else {
            "thresholds": {
                "max_removal_ratio": 0.5,
                "max_growth_ratio_without_review": 10.0,
            }
        },
    )
    monkeypatch.setattr(build_module, "adapter_names_for", lambda service_id: ["official_web"])
    monkeypatch.setattr(
        build_module,
        "extract_with_adapter",
        lambda **kwargs: AdapterExtraction(
            ("open.taobao.com",),
            {
                "source_method": "official_web",
                "source_type": "official_web",
                "authority": "official",
                "parser_version": "domain-extractor-v4",
                "retrieved_at": "2026-09-22T00:00:00+00:00",
                "content_hash": "a" * 64,
            },
        ),
    )
    monkeypatch.setattr(build_module, "load_exclusion_suffixes", lambda: ())
    monkeypatch.setattr(build_module, "filter_revoked", lambda service_id, values: values)
    monkeypatch.setattr(build_module, "load_service_overrides", lambda service_id: [])
    monkeypatch.setattr(build_module, "apply_overrides", lambda domains, *args, **kwargs: domains)

    result = build_module.build_service("taobao")
    assert result["domains"] == ["open.taobao.com"]
    assert result["domain_count"] == 1
    assert result["release_state"] == "CANDIDATE"


def test_source_bound_preserves_upstream_domains_without_manual_allowlist(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)
    (tmp_path / "VERSION").write_text("0.5.0\n", encoding="utf-8")

    monkeypatch.setattr(
        build_module,
        "load_services",
        lambda path="config/services.yaml": {
            "services": {
                "alibabacloud": {
                    "official_sources": ["https://example.invalid/rules.list"],
                    "source_bindings": [
                        {
                            "url": "https://example.invalid/rules.list",
                            "adapter": "upstream_rule",
                        }
                    ],
                    "allowed_host_exact": [],
                    "allowed_host_suffixes": [],
                    "boundary": {"shared_infrastructure_allowed": False, "mode": "source_bound"},
                    "source_policy": {
                        "official_required": False,
                        "allowed_authorities": ["upstream"],
                        "min_confidence": "high",
                    },
                }
            }
        },
    )
    monkeypatch.setattr(
        build_module,
        "load_yaml",
        lambda path: {
            "runtime": {
                "timeout_seconds": 1,
                "retry_attempts": 1,
                "retry_backoff_seconds": 0,
                "max_bytes": 1024,
                "user_agent": "test",
            }
        } if "source_adapters" in path else {
            "thresholds": {
                "max_removal_ratio": 0.5,
                "max_growth_ratio_without_review": 10.0,
            }
        },
    )
    monkeypatch.setattr(
        build_module,
        "extract_with_adapter",
        lambda **kwargs: AdapterExtraction(
            ("alibabacloud.com", "foo.alibabacloud.com"),
            {
                "source_method": "upstream_rule",
                "source_type": "upstream_rule",
                "authority": "upstream",
                "parser_version": "upstream-rule-v1",
                "retrieved_at": "2026-09-23T00:00:00+00:00",
                "content_hash": "b" * 64,
            },
        ),
    )
    monkeypatch.setattr(build_module, "load_exclusion_suffixes", lambda: ())
    monkeypatch.setattr(build_module, "filter_revoked", lambda service_id, values: values)
    monkeypatch.setattr(build_module, "load_service_overrides", lambda service_id: [])
    monkeypatch.setattr(build_module, "apply_overrides", lambda domains, *args, **kwargs: domains)

    result = build_module.build_service("alibabacloud")
    assert result["domains"] == ["alibabacloud.com", "foo.alibabacloud.com"]
    assert result["domain_count"] == 2
    assert result["release_state"] == "CANDIDATE"
