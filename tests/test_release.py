from __future__ import annotations

import json

from source_engine import release


def test_create_release_binds_content_digest(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    (tmp_path / "snapshots" / "snap-dingding").mkdir(parents=True)
    (tmp_path / "releases").mkdir()
    (tmp_path / "VERSION").write_text("2.0.0\n", encoding="utf-8")
    (tmp_path / "snapshots" / "snap-dingding" / "domains.txt").write_text("ding.example.com\n", encoding="utf-8")
    (tmp_path / "snapshots" / "snap-dingding" / "provenance.json").write_text("{}\n", encoding="utf-8")
    (tmp_path / "snapshots" / "snap-dingding" / "manifest.json").write_text("{}\n", encoding="utf-8")
    (tmp_path / "snapshots" / "snap-dingding" / "checksums.json").write_text("{}\n", encoding="utf-8")

    digest = "a" * 64
    monkeypatch.setattr(
        release,
        "build_service",
        lambda service_id: {
            "schema": "source_snapshot_v2",
            "service_id": service_id,
            "snapshot_id": "snap-dingding",
            "content_digest": digest,
            "release_state": "CANDIDATE",
            "change_assessment": {"status": "OK"},
            "errors": [],
        },
    )

    doc = release.create_release("dingding")
    assert doc["snapshot_id"] == "snap-dingding"
    assert doc["content_digest"] == digest
    saved = json.loads((tmp_path / "releases" / "dingding" / "snap-dingding" / "release.json").read_text())
    assert saved["content_digest"] == digest
