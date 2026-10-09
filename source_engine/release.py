from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from .build import build_service

# P1-05 contract (audit 2026-10-09 / docs/RELEASE_POLICY.md):
# - BLOCKED: fail-closed; never written under releases/
# - REVIEW: may be archived as durable *audit evidence* under releases/
#   but is NOT a Qualified Durable Release (handoff_eligible=false)
# - CANDIDATE (and other non-blocked states with full evidence): Qualified path
#   with handoff_eligible=true only when release_state == "CANDIDATE"
#
# Collection must only bind handoff_eligible=true releases.


def create_release(
    service_id: str,
    repository: str = "cn-wanmei/Popular-Rules-Source",
) -> dict:
    manifest = build_service(service_id)
    state = manifest["release_state"]

    # Only BLOCKED is hard-rejected at the release layer.
    # REVIEW is retained as audit archive; it is not Collection-handoff eligible.
    if state == "BLOCKED":
        raise RuntimeError(f"release blocked: {state}")

    handoff_eligible = state == "CANDIDATE"

    release_root = Path("releases") / service_id / manifest["snapshot_id"]
    release_root.mkdir(parents=True, exist_ok=True)
    release_file = release_root / "release.json"

    expected_identity = {
        "service_id": service_id,
        "snapshot_id": manifest["snapshot_id"],
        "content_digest": manifest["content_digest"],
        "evidence_digest": manifest.get("evidence_digest"),
        "policy_digest": manifest.get("policy_digest"),
        "generator_digest": manifest.get("generator_digest"),
        "release_digest": manifest.get("release_digest"),
        "release_identity_version": manifest.get("release_identity_version"),
    }
    if release_file.exists():
        existing = json.loads(release_file.read_text(encoding="utf-8"))
        if all(existing.get(key) == value for key, value in expected_identity.items()):
            return existing
        raise RuntimeError(
            "immutable release collision: existing release identity does not match current snapshot"
        )

    snapshot_dir = Path("snapshots") / manifest["snapshot_id"]
    required = ("domains.txt", "provenance.json", "manifest.json", "checksums.json")
    for name in required:
        source = snapshot_dir / name
        if not source.exists():
            raise RuntimeError(f"snapshot artifact missing: {source}")
        (release_root / name).write_bytes(source.read_bytes())

    version = Path("VERSION").read_text(encoding="utf-8").strip()
    release = {
        "schema": "popular_rules_source_release_v1",
        "repository": repository,
        "service_id": service_id,
        "snapshot_id": manifest["snapshot_id"],
        "content_digest": manifest["content_digest"],
        "evidence_digest": manifest.get("evidence_digest"),
        "policy_digest": manifest.get("policy_digest"),
        "generator_digest": manifest.get("generator_digest"),
        "release_digest": manifest.get("release_digest"),
        "release_identity_version": manifest.get("release_identity_version"),
        "version": version,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "checksums": json.loads(
            (release_root / "checksums.json").read_text(encoding="utf-8")
        ),
        "validation": {
            "release_state": state,
            "change_assessment": manifest["change_assessment"],
            "errors": manifest["errors"],
            "handoff_eligible": handoff_eligible,
        },
        "reconciliation": {
            "status": "PENDING_COLLECTION_AUDIT" if handoff_eligible else "AUDIT_ARCHIVE_ONLY"
        },
    }
    release_file.write_text(
        json.dumps(release, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return release
