"""Load explicit, auditable service overrides."""
from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from .normalize import host_allowed, normalize_domain
from .policy import is_excluded


def load_service_overrides(service_id: str) -> list[dict[str, Any]]:
    path = Path("authoring") / "services" / service_id / "overrides.yaml"
    if not path.exists():
        return []
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return list(data.get("items") or [])


def apply_overrides(
    domains: set[str],
    overrides: list[dict[str, Any]],
    *,
    exact: tuple[str, ...],
    suffixes: tuple[str, ...],
    blocked_suffixes: tuple[str, ...],
    revoked: set[str] | None = None,
) -> set[str]:
    out = set(domains)
    revoked = revoked or set()
    for item in overrides:
        raw_asset = str(item.get("asset", ""))
        action = str(item.get("action", "")).lower()
        reason = item.get("reason")
        evidence = item.get("evidence") or item.get("evidence_ids")
        domain = normalize_domain(raw_asset)

        if not domain or action not in {"include", "exclude"}:
            raise ValueError("override requires a valid domain and action include/exclude")
        if not reason and not evidence:
            raise ValueError(f"override for {domain} requires reason or evidence")

        if action == "include":
            if not host_allowed(domain, exact, suffixes):
                raise ValueError(f"override include outside service allow policy: {domain}")
            if is_excluded(domain, blocked_suffixes):
                raise ValueError(f"override include conflicts with exclusion policy: {domain}")
            if domain in revoked:
                raise ValueError(f"override include conflicts with tombstone: {domain}")
            out.add(domain)
        else:
            out.discard(domain)
    return out
