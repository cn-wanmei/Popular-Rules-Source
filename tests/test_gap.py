from __future__ import annotations

import json

from source_engine import gap as gap_module


def test_gap_reports_missing_source_domain_and_candidate(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    (tmp_path / "config").mkdir()
    snapshot = tmp_path / "snapshots" / "snap-taobao-test"
    snapshot.mkdir(parents=True)
    candidate_dir = tmp_path / "authoring" / "candidates"
    candidate_dir.mkdir(parents=True)

    (tmp_path / "config" / "services.yaml").write_text(
        "services:\n  taobao:\n    official_sources: [https://open.taobao.com/]\n",
        encoding="utf-8",
    )
    (snapshot / "manifest.json").write_text(json.dumps({
        "schema": "source_snapshot_v2",
        "service_id": "taobao",
        "snapshot_id": "snap-taobao-test",
        "content_digest": "a" * 64,
        "evidence_digest": "b" * 64,
        "policy_digest": "c" * 64,
        "generator_digest": "d" * 64,
        "release_digest": "e" * 64,
        "release_state": "CANDIDATE",
        "domain_count": 2,
        "official_extracted": 2,
        "domains": ["open.taobao.com", "api.taobao.com"],
        "evidence": [{
            "evidence_id": "EV-1",
            "authority": "official",
            "status": "verified",
            "source_url": "https://open.taobao.com/",
        }],
        "assets": [{"value": "api.taobao.com", "evidence_ids": ["EV-1"]}],
    }), encoding="utf-8")
    (candidate_dir / "taobao.jsonl").write_text(json.dumps({
        "candidate_id": "C-1",
        "service_id": "taobao",
        "value": "api.taobao.com",
        "asset_type": "domain",
        "status": "candidate",
        "evidence_ids": ["EV-1"],
    }) + "\n", encoding="utf-8")

    monkeypatch.setattr(gap_module, "collection_domains", lambda *a, **k: {
        "domains": ["open.taobao.com"],
        "membership_rule_count": 1,
        "matched_domain_rule_count": 1,
        "membership_url": "fixture",
        "rules_url": "fixture",
    })

    result = gap_module.gap("taobao")
    assert result["missing"] == ["api.taobao.com"]
    assert result["candidate_matches"][0]["domain"] == "api.taobao.com"
    assert result["recommended_action"] == "official_evidence_required"
