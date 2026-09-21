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


def test_create_release_fails_closed_on_identity_collision(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    snapshot_id = "snap-dingding-collision"
    snapshot = tmp_path / "snapshots" / snapshot_id
    snapshot.mkdir(parents=True)
    for name, payload in {
        "domains.txt": "ding.example.com\n",
        "provenance.json": "{}\n",
        "manifest.json": "{}\n",
        "checksums.json": "{}\n",
    }.items():
        (snapshot / name).write_text(payload, encoding="utf-8")
    release_root = tmp_path / "releases" / "dingding" / snapshot_id
    release_root.mkdir(parents=True)
    (release_root / "release.json").write_text(
        json.dumps({
            "schema": "popular_rules_source_release_v1",
            "service_id": "dingding",
            "snapshot_id": snapshot_id,
            "content_digest": "old" + "0" * 61,
            "evidence_digest": "b" * 64,
            "policy_digest": "c" * 64,
            "generator_digest": "d" * 64,
            "release_digest": "e" * 64,
            "release_identity_version": "1",
        }),
        encoding="utf-8",
    )
    monkeypatch.setattr(
        release,
        "build_service",
        lambda service_id: {
            "service_id": service_id,
            "snapshot_id": snapshot_id,
            "content_digest": "a" * 64,
            "evidence_digest": "b" * 64,
            "policy_digest": "c" * 64,
            "generator_digest": "d" * 64,
            "release_digest": "f" * 64,
            "release_identity_version": "2",
            "release_state": "CANDIDATE",
            "change_assessment": {"status": "OK"},
            "errors": [],
        },
    )
    try:
        release.create_release("dingding")
    except RuntimeError as exc:
        assert "immutable release collision" in str(exc)
    else:
        raise AssertionError("identity collision must fail closed")


def test_release_identity_version_is_explicit_in_release_contract(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    (tmp_path / "VERSION").write_text("0.5.0\n", encoding="utf-8")
    snapshot_id = "snap-dingding-v2"
    snapshot = tmp_path / "snapshots" / snapshot_id
    snapshot.mkdir(parents=True)
    for name, payload in {
        "domains.txt": "ding.example.com\n",
        "provenance.json": "{}\n",
        "manifest.json": "{}\n",
        "checksums.json": "{}\n",
    }.items():
        (snapshot / name).write_text(payload, encoding="utf-8")
    monkeypatch.setattr(
        release,
        "build_service",
        lambda service_id: {
            "service_id": service_id,
            "snapshot_id": snapshot_id,
            "content_digest": "a" * 64,
            "evidence_digest": "b" * 64,
            "policy_digest": "c" * 64,
            "generator_digest": "d" * 64,
            "release_digest": "e" * 64,
            "release_identity_version": "2",
            "release_state": "CANDIDATE",
            "change_assessment": {"status": "OK"},
            "errors": [],
        },
    )
    doc = release.create_release("dingding")
    assert doc["release_identity_version"] == "2"
