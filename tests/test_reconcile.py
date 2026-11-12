from __future__ import annotations

import base64
import json

from source_engine import reconcile


def test_reconcile_reports_registered_but_disabled(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    def fake_get_yaml(url: str, timeout: int = 20) -> dict:
        if url.endswith("/sources/immutable_registry.yaml"):
            return {"bindings": {}}
        if url.endswith("/sources/registry.yaml"):
            return {
                "sources": [
                    {
                        "id": "popular-rules-source",
                        "enabled": False,
                        "rules": [{"service": "dingding"}, {"service": "qqmail"}],
                    }
                ]
            }
        if url.endswith("/config/intentional_unmaterialized.yaml"):
            return {"services": {}}
        raise AssertionError(url)

    monkeypatch.setattr(reconcile, "_get_collection_yaml", lambda path, ref, timeout=20: fake_get_yaml(f"{ref}/{path}", timeout))

    snapshot_dir = tmp_path / "snapshots" / "snap-dingding"
    snapshot_dir.mkdir(parents=True)
    (snapshot_dir / "manifest.json").write_text(
        json.dumps(
            {
                "schema": "source_snapshot_v2",
                "service_id": "dingding",
                "snapshot_id": "snap-dingding",
                "content_digest": "digest",
                "release_state": "CANDIDATE",
                "domain_count": 1,
                "seed_only_count": 0,
                "created_at": "2026-09-20T10:00:00Z",
            }
        ),
        encoding="utf-8",
    )

    result = reconcile.audit_collection(["dingding", "qqmail"])
    assert result["collection"]["prs_registered"] is True
    assert result["collection"]["prs_enabled"] is False
    assert result["services"]["dingding"]["collection_prs_registered"] is True
    assert result["services"]["dingding"]["collection_prs_enabled"] is False
    assert result["services"]["dingding"]["source_state"] == "CANDIDATE"
    assert result["services"]["qqmail"]["source_state"] == "NO_SNAPSHOT"
    assert (tmp_path / "reports" / "reconciliation.json").is_file()

# CI checkpoint after fixing the collection YAML fetcher mock target.


def test_collection_yaml_fetch_uses_workflow_token(monkeypatch):
    monkeypatch.setenv("GITHUB_TOKEN", "test-workflow-token")
    payload = {
        "encoding": "base64",
        "content": base64.b64encode(b"services:\n  - id: example\n").decode("ascii"),
    }
    captured = {}

    class Response:
        def raise_for_status(self):
            return None

        def json(self):
            return payload

    def fake_get(url, params, timeout, headers):
        captured.update({"url": url, "params": params, "timeout": timeout, "headers": headers})
        return Response()

    monkeypatch.setattr(reconcile.requests, "get", fake_get)
    result = reconcile._get_collection_yaml("sources/registry.yaml", "main")

    assert result == {"services": [{"id": "example"}]}
    assert captured["headers"]["Authorization"] == "Bearer test-workflow-token"
    assert captured["headers"]["Accept"] == "application/vnd.github+json"
    assert captured["params"] == {"ref": "main"}
