from __future__ import annotations

from pathlib import Path

import requests
import yaml

COLLECTION_RAW_BASE = "https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main"


def _get_text(url: str, timeout: int = 20) -> str:
    response = requests.get(
        url,
        timeout=timeout,
        headers={"User-Agent": "Popular-Rules-Source/0.1"},
    )
    response.raise_for_status()
    return response.text


def audit_collection(service_ids: list[str]) -> dict:
    registry_text = _get_text(f"{COLLECTION_RAW_BASE}/sources/registry.yaml")
    intentional_text = _get_text(
        f"{COLLECTION_RAW_BASE}/config/intentional_unmaterialized.yaml"
    )
    registry = yaml.safe_load(registry_text) or {}
    intentional = yaml.safe_load(intentional_text) or {}

    registry_services: set[str] = set()
    for source in registry.get("sources", []):
        for rule in source.get("rules", []) or []:
            service = rule.get("service") or rule.get("name")
            if service:
                registry_services.add(str(service))

    intentional_services = set((intentional.get("services") or {}).keys())

    result: dict = {"schema": "collection_reconciliation_v1", "services": {}}
    for service_id in sorted(service_ids):
        in_registry = service_id in registry_services
        in_intentional = service_id in intentional_services
        if in_intentional and not in_registry:
            status = "INTENTIONAL"
        elif in_registry:
            status = "REGISTERED"
        else:
            status = "MISSING"
        result["services"][service_id] = {
            "status": status,
            "collection_registry": in_registry,
            "collection_intentional": in_intentional,
        }

    Path("reports").mkdir(exist_ok=True)
    Path("reports/reconciliation.json").write_text(
        __import__("json").dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return result
