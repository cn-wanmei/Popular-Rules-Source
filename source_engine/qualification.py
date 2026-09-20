from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .build import load_services
from .reconcile import audit_collection

SERVICE_IDS = (
    "1688",
    "cainiao",
    "dingding",
    "qqmail",
    "qqmusic",
    "taobao",
    "tencentcloud",
    "tmall",
)


def _latest_manifest(service_id: str) -> dict[str, Any] | None:
    root = Path("snapshots")
    latest: dict[str, Any] | None = None
    if not root.exists():
        return None
    for path in root.glob("*/manifest.json"):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        if data.get("schema") != "source_snapshot_v2":
            continue
        if data.get("service_id") != service_id:
            continue
        if latest is None or str(data.get("created_at", "")) > str(latest.get("created_at", "")):
            latest = data
    return latest


def _service_result(service_id: str, manifest: dict[str, Any] | None) -> dict[str, Any]:
    blockers: list[str] = []
    if manifest is None:
        blockers.append("no_snapshot")
    else:
        if manifest.get("release_state") != "CANDIDATE":
            blockers.append(f"release_state:{manifest.get('release_state')}")
        if manifest.get("errors"):
            blockers.append("source_errors")
        if int(manifest.get("unverified_candidate_count", 0) or 0) != 0:
            blockers.append("unverified_candidates")
        if int(manifest.get("seed_only_count", 0) or 0) != 0:
            blockers.append("seed_only_assets")
        if int(manifest.get("domain_count", 0) or 0) <= 0:
            blockers.append("empty_domain_output")
        if int(manifest.get("official_extracted", 0) or 0) <= 0:
            blockers.append("no_official_extraction")
        evidence = manifest.get("evidence") or []
        if not evidence:
            blockers.append("no_evidence")
        elif not all(item.get("source_method") == "official_web" for item in evidence if isinstance(item, dict)):
            blockers.append("non_official_evidence")

    verified = not blockers
    return {
        "service_id": service_id,
        "stage": "VERIFIED" if verified else "REVIEW",
        "verified": verified,
        "blockers": blockers,
        "snapshot_id": manifest.get("snapshot_id") if manifest else None,
        "content_digest": manifest.get("content_digest") if manifest else None,
        "domain_count": manifest.get("domain_count") if manifest else 0,
        "official_extracted": manifest.get("official_extracted") if manifest else 0,
        "unverified_candidate_count": manifest.get("unverified_candidate_count") if manifest else 0,
        "seed_only_count": manifest.get("seed_only_count", 0) if manifest else 0,
        "canary_stage": "BLOCKED_UNTIL_COLLECTION_GATE",
        "production_stage": "BLOCKED_UNTIL_CANARY_AND_OBSERVATION",
    }


def qualify_all() -> dict[str, Any]:
    services = load_services()["services"]
    ids = [sid for sid in SERVICE_IDS if sid in services]
    reconciliation = audit_collection(ids)
    result = {
        "schema": "phase2_service_qualification_v1",
        "services": {},
        "verified_count": 0,
        "canary_ready_count": 0,
        "production_count": 0,
        "reconciliation": reconciliation,
    }
    for service_id in ids:
        item = _service_result(service_id, _latest_manifest(service_id))
        result["services"][service_id] = item
        if item["verified"]:
            result["verified_count"] += 1
    Path("reports").mkdir(exist_ok=True)
    Path("reports/phase2-service-qualification.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return result
