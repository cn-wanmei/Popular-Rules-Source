from __future__ import annotations

import json
import os
from pathlib import Path

import requests
import yaml

COLLECTION_RAW_ROOT = "https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection"


def _get_yaml(url: str, timeout: int = 20) -> dict:
    response = requests.get(url, timeout=timeout, headers={"User-Agent": "Popular-Rules-Source/3.x"})
    response.raise_for_status()
    data = yaml.safe_load(response.text) or {}
    return data if isinstance(data, dict) else {}


def _get_yaml_optional(url: str, timeout: int = 20) -> dict:
    try:
        return _get_yaml(url, timeout)
    except (requests.RequestException, yaml.YAMLError):
        return {}


def _latest_manifest(service_id: str) -> dict | None:
    latest = None
    for path in Path("snapshots").glob("*/manifest.json"):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        if data.get("service_id") != service_id:
            continue
        if latest is None or str(data.get("created_at", "")) > str(latest.get("created_at", "")):
            latest = data
    return latest


def audit_collection(service_ids: list[str]) -> dict:
    ref = os.getenv("COLLECTION_REF", "main")
    registry = _get_yaml(f"{COLLECTION_RAW_ROOT}/{ref}/sources/registry.yaml")
    immutable = _get_yaml_optional(f"{COLLECTION_RAW_ROOT}/{ref}/sources/immutable_registry.yaml")
    intentional = _get_yaml(f"{COLLECTION_RAW_ROOT}/{ref}/config/intentional_unmaterialized.yaml")

    prs_entry = next((x for x in registry.get("sources", []) if x.get("id") == "popular-rules-source"), None)
    prs_rules = {
        str(rule.get("service") or rule.get("name"))
        for rule in (prs_entry or {}).get("rules", []) or []
        if rule.get("service") or rule.get("name")
    }
    bindings = immutable.get("bindings") or {}
    result = {
        "schema": "collection_reconciliation_v3",
        "collection": {
            "reference": ref,
            "prs_registered": prs_entry is not None,
            "prs_enabled": bool((prs_entry or {}).get("enabled", False)),
            "prs_services": sorted(prs_rules),
            "immutable_registry_present": isinstance(bindings, dict),
        },
        "services": {},
    }
    intentional_services = set((intentional.get("services") or {}).keys())

    for service_id in sorted(service_ids):
        latest = _latest_manifest(service_id)
        binding = bindings.get(service_id) or {}
        result["services"][service_id] = {
            "source_snapshot_id": (latest or {}).get("snapshot_id"),
            "source_release_digest": (latest or {}).get("release_digest"),
            "source_domain_count": (latest or {}).get("domain_count", 0),
            "source_state": (latest or {}).get("release_state", "NO_SNAPSHOT"),
            "collection_prs_registered": service_id in prs_rules,
            "collection_prs_enabled": bool((prs_entry or {}).get("enabled", False)),
            "collection_intentional": service_id in intentional_services,
            "immutable_binding_exact": (
                binding.get("status") == "active"
                and binding.get("snapshot_id") == (latest or {}).get("snapshot_id")
                and binding.get("content_digest") == (latest or {}).get("content_digest")
            ),
            "immutable_registry_source_ref": binding.get("source_ref"),
            "immutable_registry_verified_input_commit": binding.get("verified_input_commit"),
        }

    Path("reports").mkdir(exist_ok=True)
    Path("reports/reconciliation.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return result
