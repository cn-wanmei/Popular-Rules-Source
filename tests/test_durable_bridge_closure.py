from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from scripts.durable_bridge_closure import materialize_durable_closure


def _fixture(root: Path, *, stale_generated: bool = True) -> dict:
    service = "example"
    snapshot_id = "snap-example-abc"
    snapshot = root / "snapshots" / snapshot_id
    snapshot.mkdir(parents=True)
    domains = b"example.org\nwww.example.org\n"
    (snapshot / "domains.txt").write_bytes(domains)
    digest = hashlib.sha256(domains).hexdigest()
    (snapshot / "checksums.json").write_text(
        json.dumps({"domains.txt": digest}), encoding="utf-8"
    )
    release_dir = root / "releases" / service / snapshot_id
    release_dir.mkdir(parents=True)
    release = {
        "service_id": service,
        "snapshot_id": snapshot_id,
        "checksums": {"domains.txt": digest},
        "content_digest": "c" * 64,
        "evidence_digest": "d" * 64,
        "policy_digest": "e" * 64,
        "generator_digest": "f" * 64,
        "release_digest": "0" * 64,
        "release_identity_version": "2",
    }
    (release_dir / "release.json").write_text(json.dumps(release), encoding="utf-8")
    generated = root / "generated" / "source" / service
    generated.mkdir(parents=True)
    (generated / "domains.txt").write_bytes(b"stale.example.org\n" if stale_generated else domains)
    return {
        "services": {
            service: {
                "status": "PERSISTED",
                "snapshot_id": snapshot_id,
                "release_path": f"releases/{service}/{snapshot_id}/release.json",
                "content_digest": release["content_digest"],
                "evidence_digest": release["evidence_digest"],
                "policy_digest": release["policy_digest"],
                "generator_digest": release["generator_digest"],
                "release_digest": release["release_digest"],
                "release_identity_version": "2",
                "expected_sha256": "0" * 64,
            }
        }
    }


def test_closure_replaces_stale_generated_artifact_from_snapshot(tmp_path: Path) -> None:
    report = _fixture(tmp_path, stale_generated=True)
    materialize_durable_closure(tmp_path, report)
    generated = (tmp_path / "generated/source/example/domains.txt").read_bytes()
    snapshot = (tmp_path / "snapshots/snap-example-abc/domains.txt").read_bytes()
    assert generated == snapshot
    assert report["services"]["example"]["expected_sha256"] == hashlib.sha256(snapshot).hexdigest()


def test_closure_fails_when_snapshot_checksum_is_inconsistent(tmp_path: Path) -> None:
    report = _fixture(tmp_path, stale_generated=True)
    checksums = tmp_path / "snapshots/snap-example-abc/checksums.json"
    checksums.write_text(json.dumps({"domains.txt": "0" * 64}), encoding="utf-8")
    with pytest.raises(RuntimeError, match="checksum mismatch"):
        materialize_durable_closure(tmp_path, report)


def test_closure_fails_when_release_provenance_drifts(tmp_path: Path) -> None:
    report = _fixture(tmp_path, stale_generated=True)
    release_path = tmp_path / report["services"]["example"]["release_path"]
    release = json.loads(release_path.read_text(encoding="utf-8"))
    release["release_digest"] = "9" * 64
    release_path.write_text(json.dumps(release), encoding="utf-8")
    with pytest.raises(RuntimeError, match="provenance mismatch"):
        materialize_durable_closure(tmp_path, report)
