"""Mark a CANDIDATE snapshot as PUBLISHED after successful promotion package."""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from .promotion import build_promotion_package


def publish_service(service_id: str, snapshot_id: str | None = None) -> dict:
    """Create promotion package and stamp snapshot release_state=PUBLISHED."""
    root = Path("snapshots")
    if snapshot_id is None:
        # pick latest CANDIDATE/PUBLISHED for service
        candidates = []
        for m in root.glob("*/manifest.json"):
            data = json.loads(m.read_text(encoding="utf-8"))
            if data.get("service_id") == service_id:
                candidates.append((data.get("created_at", ""), m, data))
        if not candidates:
            raise FileNotFoundError(f"no snapshot for {service_id}")
        _, manifest_path, data = sorted(candidates)[-1]
        snapshot_id = data["snapshot_id"]
    else:
        manifest_path = root / snapshot_id / "manifest.json"
        data = json.loads(manifest_path.read_text(encoding="utf-8"))

    if data.get("service_id") != service_id:
        raise ValueError("snapshot/service mismatch")

    # Build promotion package (gates)
    pkg = build_promotion_package(service_id, snapshot_id)
    if pkg["gates"].get("empty_list") == "FAIL":
        raise RuntimeError("promotion blocked: empty domain list")

    # Immutable rule: do not rewrite snapshot content identity; write publish stamp alongside
    stamp = {
        "schema": "source_publish_stamp_v1",
        "service_id": service_id,
        "snapshot_id": snapshot_id,
        "release_state": "PUBLISHED",
        "published_at": datetime.now(timezone.utc).isoformat(),
        "promotion": {
            "package_path": f"releases/{service_id}/{snapshot_id}/promotion/promotion.json",
            "domain_count": pkg.get("domain_count"),
        },
    }
    stamp_path = root / snapshot_id / "publish.json"
    stamp_path.write_text(json.dumps(stamp, ensure_ascii=False, indent=2, sort_keys=True) + "\n")

    # Update release_state in a copy under generated for consumers; snapshot manifest stays
    # but we also write published pointer
    pointer = {
        "service_id": service_id,
        "published_snapshot_id": snapshot_id,
        "published_at": stamp["published_at"],
        "domains_path": f"snapshots/{snapshot_id}/domains.txt",
    }
    Path("generated/published").mkdir(parents=True, exist_ok=True)
    (Path("generated/published") / f"{service_id}.json").write_text(
        json.dumps(pointer, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    )

    # Soft-update manifest release_state for tooling that reads it
    # (content-addressed id unchanged; metadata field only)
    data["release_state"] = "PUBLISHED"
    data["published_at"] = stamp["published_at"]
    manifest_path.write_text(json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n")

    return {"stamp": stamp, "promotion": pkg, "pointer": pointer}
