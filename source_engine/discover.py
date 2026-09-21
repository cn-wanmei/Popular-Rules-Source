from __future__ import annotations

from .adapters import adapter_names_for, extract_with_adapter
from .build import load_services


def discover_from_config(service_id: str, live: bool = False) -> dict:
    services = load_services()["services"]
    if service_id not in services:
        raise KeyError(f"unknown service: {service_id}")
    cfg = services[service_id]
    result = {
        "schema": "source_discovery_v2",
        "service_id": service_id,
        "ecosystem": cfg.get("ecosystem"),
        "official_sources": list(cfg.get("official_sources", [])),
        "seed_domains": list(cfg.get("seed_domains", [])),
        "adapters": adapter_names_for(service_id),
        "source_contract": {
            "official_required": bool((cfg.get("source_policy") or {}).get("official_required", True)),
            "minimum_confidence": (cfg.get("source_policy") or {}).get("min_confidence", "high"),
        },
        "note": "Configured discovery candidates never assert production ownership.",
    }
    if not live:
        return result

    exact = tuple(cfg.get("allowed_host_exact", []))
    suffixes = tuple(cfg.get("allowed_host_suffixes", []))
    from .build import load_yaml
    runtime = load_yaml("config/source_adapters.yaml")["runtime"]
    result["live_evidence"] = []
    for source_url in cfg.get("official_sources", []):
        source_result = {"source_url": source_url, "attempts": []}
        for adapter_name in adapter_names_for(service_id):
            try:
                extraction = extract_with_adapter(
                    service_id=service_id,
                    adapter_name=adapter_name,
                    source_url=str(source_url),
                    exact=exact,
                    suffixes=suffixes,
                    adapter_policy=runtime,
                )
                source_result["attempts"].append({
                    "adapter": adapter_name,
                    "domains": list(extraction.domains),
                    "evidence": extraction.evidence,
                    "status": "verified" if extraction.domains else "empty",
                })
                if extraction.domains:
                    break
            except Exception as exc:
                source_result["attempts"].append({
                    "adapter": adapter_name,
                    "status": "error",
                    "error": str(exc),
                })
        result["live_evidence"].append(source_result)
    return result
