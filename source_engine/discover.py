from __future__ import annotations

from .build import load_services


def discover_from_config(service_id: str) -> dict:
    services = load_services()["services"]
    if service_id not in services:
        raise KeyError(f"unknown service: {service_id}")
    cfg = services[service_id]
    return {
        "service_id": service_id,
        "ecosystem": cfg.get("ecosystem"),
        "status": cfg.get("status", "review"),
        "official_sources": list(cfg.get("official_sources", [])),
        "seed_domains": list(cfg.get("seed_domains", [])),
        "source_contract": {
            "official_required": bool(
                (cfg.get("source_policy") or {}).get("official_required", True)
            ),
            "minimum_confidence": (cfg.get("source_policy") or {}).get(
                "min_confidence", "high"
            ),
        },
        "note": "Discovery returns configured source candidates only; it does not assert production ownership.",
    }
