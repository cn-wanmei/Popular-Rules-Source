from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
import shutil

from .build import build_service


def create_release(
    service_id: str,
    repository: str = "cn-wanmei/Popular-Rules-Source",
) -> dict:
    manifest = build_service(service_id)
    release_state = str(manifest.get("release_state") or "BLOCKED")

    # REVIEW is a valid audit outcome: keep the generated snapshot/provenance
    # for inspection and preserve any previously durable release. REVIEW must
    # never delete last-known-good production artifacts or fail the whole bridge.
    if release_state == "REVIEW":
        review_root = Path("reports") / "release-review" / service_id
        review_root.mkdir(parents=True, exist_ok=True)
        review_file = review_root / f"{manifest['snapshot_id']}.json"
        review_file.write_text(
            json.dumps(
                {
                    "schema": "popular_rules_source_release_review_v1",
                    "service_id": service_id,
                    "snapshot_id": manifest["snapshot_id"],
                    "release_state": release_state,
                    "release_reasons": manifest.get("release_reasons", []),
                    "content_digest": manifest.get("content_digest"),
                    "evidence_digest": manifest.get("evidence_digest"),
                    "policy_digest": manifest.get("policy_digest"),
                    "generator_digest": manifest.get("generator_digest"),
                    "release_digest": manifest.get("release_digest"),
                    "change_assessment": manifest.get("change_assessment", {}),
                    "errors": manifest.get("errors", []),
                },
                ensure_ascii=False,
                indent=2,
                sort_keys=True,
            )
            + "\n",
            encoding="utf-8",
        )
        return {
            "schema": "popular_rules_source_review_result_v1",
            "service_id": service_id,
            "snapshot_id": manifest["snapshot_id"],
            "release_state": release_state,
            "review_path": str(review_file),
            "release_reasons": manifest.get("release_reasons", []),
            "content_digest": manifest.get("content_digest"),
        }

    if release_state != "CANDIDATE":
        raise RuntimeError(f"release blocked: {release_state}")

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
            "release_state": manifest["release_state"],
            "change_assessment": manifest["change_assessment"],
            "errors": manifest["errors"],
        },
        "reconciliation": {
            "status": "PENDING_COLLECTION_AUDIT"
        },
    }
    release_file.write_text(
        json.dumps(release, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return release
