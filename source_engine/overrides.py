"""Load auditable authoring overrides (include/exclude)."""
from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


def load_service_overrides(service_id: str) -> list[dict[str, Any]]:
    path = Path("authoring") / "services" / service_id / "overrides.yaml"
    if not path.exists():
        return []
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return list(data.get("items") or [])


def apply_overrides(domains: set[str], overrides: list[dict[str, Any]]) -> set[str]:
    out = set(domains)
    for item in overrides:
        asset = str(item.get("asset", "")).lower().strip()
        action = str(item.get("action", "")).lower()
        if not asset:
            continue
        if action == "include":
            out.add(asset)
        elif action == "exclude":
            out.discard(asset)
    return out
