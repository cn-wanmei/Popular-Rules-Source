"""Tombstone / revoke layer — prevents re-introduction of incorrect assets."""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .normalize import service_asset_id


TOMBSTONE_ROOT = Path("tombstones")


def _path(service_id: str) -> Path:
    return TOMBSTONE_ROOT / f"{service_id}.json"


def load_tombstones(service_id: str) -> dict[str, Any]:
    path = _path(service_id)
    if not path.exists():
        return {"service_id": service_id, "items": []}
    return json.loads(path.read_text(encoding="utf-8"))


def load_revoked_domains(service_id: str) -> set[str]:
    data = load_tombstones(service_id)
    out: set[str] = set()
    for item in data.get("items", []):
        if item.get("status") == "revoked" and item.get("type") == "domain":
            out.add(str(item.get("value", "")).lower())
    return out


def revoke_domain(
    service_id: str,
    domain: str,
    reason_type: str = "incorrect_attribution",
    evidence: list[str] | None = None,
    notes: str = "",
) -> dict[str, Any]:
    TOMBSTONE_ROOT.mkdir(parents=True, exist_ok=True)
    data = load_tombstones(service_id)
    asset_id = service_asset_id(service_id, domain)
    items = data.setdefault("items", [])
    for item in items:
        if item.get("asset_id") == asset_id:
            item["status"] = "revoked"
            item["revoked_at"] = datetime.now(timezone.utc).isoformat()
            item["reason"] = {"type": reason_type, "notes": notes}
            item["evidence"] = evidence or item.get("evidence") or []
            break
    else:
        items.append(
            {
                "asset_id": asset_id,
                "type": "domain",
                "value": domain,
                "status": "revoked",
                "reason": {"type": reason_type, "notes": notes},
                "evidence": evidence or [],
                "revoked_at": datetime.now(timezone.utc).isoformat(),
            }
        )
    data["service_id"] = service_id
    data["updated_at"] = datetime.now(timezone.utc).isoformat()
    _path(service_id).write_text(
        json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return data


def filter_revoked(service_id: str, domains: set[str]) -> set[str]:
    revoked = load_revoked_domains(service_id)
    return {d for d in domains if d not in revoked}
