from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import yaml

from .build import load_services
from .reconcile import audit_collection

STATE_PATH = Path("config/source_canary_state.yaml")


def _lifecycle() -> dict[str, Any]:
    if not STATE_PATH.exists():
        raise RuntimeError("missing lifecycle source of truth")
    return yaml.safe_load(STATE_PATH.read_text(encoding="utf-8")) or {}


def _latest(service_id: str) -> dict[str, Any] | None:
    latest = None
    for p in Path("snapshots").glob("*/manifest.json"):
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        if data.get("service_id") != service_id:
            continue
        if latest is None or str(data.get("created_at", "")) > str(latest.get("created_at", "")):
            latest = data
    return latest


def qualify_all() -> dict[str, Any]:
    services = load_services()["services"]
    lifecycle = _lifecycle()
    declared = lifecycle.get("services") or {}
    if set(services) != set(declared):
        raise RuntimeError(
            f"lifecycle/service mismatch: missing={sorted(set(services)-set(declared))}, "
            f"extra={sorted(set(declared)-set(services))}"
        )
    reconciliation = audit_collection(sorted(services))
    result = {
        "schema": "phase2_service_qualification_v2",
        "source_of_truth": str(STATE_PATH),
        "services": {},
        "verified_count": 0,
        "production_count": 0,
        "state_drift": [],
        "reconciliation": reconciliation,
    }
    for service_id in sorted(services):
        item_state = declared[service_id]
        state = str(item_state.get("state", "review")).lower()
        manifest = _latest(service_id)
        blockers = []
        if manifest is None:
            blockers.append("no_snapshot")
        else:
            if manifest.get("release_state") not in {"CANDIDATE", "PUBLISHED"}:
                blockers.append(f"release_state:{manifest.get('release_state')}")
            if manifest.get("errors"):
                blockers.append("source_errors")
            if int(manifest.get("unverified_candidate_count", 0) or 0):
                blockers.append("unverified_candidates")
            if int(manifest.get("official_extracted", 0) or 0) <= 0:
                blockers.append("no_official_extraction")
            if not manifest.get("evidence"):
                blockers.append("no_evidence")
        verified = not blockers
        if state == "production" and not verified:
            blockers.append("declared_production_without_verified_evidence")
            result["state_drift"].append(service_id)
        result["services"][service_id] = {
            "declared_state": state,
            "enabled": item_state.get("enabled") is True,
            "verified": verified,
            "production_activated": state == "production" and verified,
            "blockers": blockers,
            "snapshot_id": (manifest or {}).get("snapshot_id"),
            "release_digest": (manifest or {}).get("release_digest"),
            "domain_count": (manifest or {}).get("domain_count", 0),
        }
        result["verified_count"] += int(verified)
        result["production_count"] += int(state == "production" and verified)
    Path("reports").mkdir(exist_ok=True)
    Path("reports/phase2-service-qualification.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return result
