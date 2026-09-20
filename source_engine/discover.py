"""Discovery layer — produces candidates only, never publishes."""
from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from .normalize import normalize_domain


def discover_from_config(service_id: str, config_path: str = "config/services.yaml") -> dict[str, Any]:
    data = yaml.safe_load(Path(config_path).read_text(encoding="utf-8")) or {}
    cfg = data.get("services", {}).get(service_id)
    if not cfg:
        raise KeyError(service_id)
    candidates = []
    for seed in cfg.get("seed_domains", []):
        d = normalize_domain(str(seed))
        if d:
            candidates.append(
                {
                    "asset": d,
                    "type": "domain",
                    "source": "seed",
                    "status": "DISCOVERED",
                }
            )
    for url in cfg.get("official_sources", []):
        candidates.append(
            {
                "asset": url,
                "type": "source_url",
                "source": "config",
                "status": "DISCOVERED",
            }
        )
    return {
        "service_id": service_id,
        "candidates": candidates,
        "note": "Discovery only — not promotion-ready",
    }
