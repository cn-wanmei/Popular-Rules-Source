from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

from .build import build_service, load_yaml, load_services


def create_release(service_id: str, repository: str = "cn-wanmei/Popular-Rules-Source") -> dict:
    manifest = build_service(service_id)
    if manifest["release_state"] != "CANDIDATE":
        raise RuntimeError(f"release blocked: {manifest['release_state']}")

    release_root = Path("releases") / service_id / manifest["snapshot_id"]
    release_root.mkdir(parents=True, exist_ok=True)

    snapshot_dir = Path("snapshots") / manifest["snapshot_id"]
    for name in ("domains.txt", "provenance.json", "manifest.json", "checksums.json"):
        source = snapshot_dir / name
        if source.exists():
            (release_root / name).write_bytes(source.read_bytes())

    version = Path("VERSION").read_text(encoding="utf-8").strip()
    release = {
        "schema": "popular_rules_source_release_v1",
        "repository": repository,
        "service_id": service_id,
        "snapshot_id": manifest["snapshot_id"],
        "version": version,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "checksums": json.loads((release_root / "checksums.json").read_text(encoding="utf-8")),
        "validation": {
            "release_state": manifest["release_state"],
            "change_assessment": manifest["change_assessment"],
            "errors": manifest["errors"],
        },
        "reconciliation": {
            "status": "PENDING_COLLECTION_AUDIT"
        },
    }
    (release_root / "release.json").write_text(
        json.dumps(release, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return release
