from __future__ import annotations

from typing import Any

from .build import build_service
from .gap import gap
from .normalize import normalize_domain
from .release import create_release


def repair(service_id: str, domains: list[str]) -> dict[str, Any]:
    targets = sorted({d for raw in domains if (d := normalize_domain(raw))})
    if not targets:
        raise ValueError("repair requires at least one valid --domain")

    before = gap(service_id, target_domains=targets)
    manifest = build_service(service_id)
    after = gap(service_id, target_domains=targets)

    target_set = set(targets)
    source_set = set(manifest.get("domains") or [])
    unresolved = sorted(target_set - source_set)
    if unresolved:
        return {
            "schema": "source_repair_v1",
            "service": service_id,
            "targets": targets,
            "status": "BLOCKED",
            "reason": "official_sources_did_not_yield_target_domains",
            "unresolved": unresolved,
            "before": before,
            "after": after,
            "snapshot": {
                "snapshot_id": manifest.get("snapshot_id"),
                "release_state": manifest.get("release_state"),
                "release_reasons": manifest.get("release_reasons") or [],
            },
        }

    if manifest.get("release_state") != "CANDIDATE":
        return {
            "schema": "source_repair_v1",
            "service": service_id,
            "targets": targets,
            "status": "BLOCKED",
            "reason": "release_gate_blocked",
            "release_reasons": manifest.get("release_reasons") or [],
            "before": before,
            "after": after,
        }

    release = create_release(service_id)
    return {
        "schema": "source_repair_v1",
        "service": service_id,
        "targets": targets,
        "status": "RELEASED",
        "snapshot_id": release.get("snapshot_id"),
        "release_digest": release.get("release_digest"),
        "before": before,
        "after": after,
    }
