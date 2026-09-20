from __future__ import annotations

import json
import os
from pathlib import Path

import requests
import yaml

COLLECTION_RAW_ROOT = "https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection"
COLLECTION_REF = os.getenv("COLLECTION_REF", "main")


def _get_yaml(url: str, timeout: int = 20) -> dict:
    response = requests.get(
        url,
        timeout=timeout,
        headers={"User-Agent": "Popular-Rules-Source/1.x"},
    )
    response.raise_for_status()
    data = yaml.safe_load(response.text) or {}
    return data if isinstance(data, dict) else {}


def audit_collection(service_ids: list[str]) -> dict:
    registry = _get_yaml(f"{COLLECTION_RAW_ROOT}/{COLLECTION_REF}/sources/registry.yaml")
    intentional = _get_yaml(
        f"{COLLECTION_RAW_ROOT}/{COLLECTION_REF}/config/intentional_unmaterialized.yaml"
    )

    prs_entry = next(
        (item for item in registry.get("sources", [])
         if item.get("id") == "popular-rules-source"),
        None,
    )
    prs_rules = {
        str(rule.get("service") or rule.get("name"))
        for rule in (prs_entry or {}).get("rules", []) or []
        if rule.get("service") or rule.get("name")
    }
    prs_enabled = bool((prs_entry or {}).get("enabled", False))

    intentional_services = set((intentional.get("services") or {}).keys())

    result = {
        "schema": "collection_reconciliation_v2",
        "collection": {
            "prs_registered": prs_entry is not None,
            "prs_enabled": prs_enabled,
            "prs_services": sorted(prs_rules),
        },
        "services": {},
    }

    for service_id in sorted(service_ids):
        in_registry = service_id in prs_rules
        in_intentional = service_id in intentional_services
        source_snapshot_paths = sorted(
            Path("snapshots").glob(f"*/manifest.json")
        )
        source_snapshots = []
        for path in source_snapshot_paths:
            try:
                data = json.loads(path.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError):
                continue
            if data.get("service_id") == service_id:
                source_snapshots.append(data)

        latest = max(
            source_snapshots,
            key=lambda item: item.get("created_at", ""),
            default=None,
        )
        result["services"][service_id] = {
            "source_state": (
                latest.get("release_state")
                if latest else "NO_SNAPSHOT"
            ),
            "source_domain_count": latest.get("domain_count", 0) if latest else 0,
            "source_seed_only_count": latest.get("seed_only_count", 0) if latest else 0,
            "collection_prs_registered": in_registry,
            "collection_prs_enabled": prs_enabled,
            "collection_intentional": in_intentional,
        }

    Path("reports").mkdir(exist_ok=True)
    Path("reports/reconciliation.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return result
