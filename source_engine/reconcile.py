"""Reconciliation against Popular-Rules-Collection public signals."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any
from urllib.request import urlopen, Request

from .build import load_services

COLLECTION_REGISTRY = (
    "https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/sources/registry.yaml"
)
COLLECTION_TENCENTCLOUD_LIST = (
    "https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/"
    "main/config/p0_batch01_snapshots/2026-09-20/tencentcloud.list"
)


def _fetch_text(url: str, timeout: int = 30) -> str | None:
    try:
        req = Request(url, headers={"User-Agent": "Popular-Rules-Source/0.2"})
        with urlopen(req, timeout=timeout) as resp:
            return resp.read().decode("utf-8", errors="replace")
    except Exception:
        return None


def audit_collection(service_ids: list[str] | None = None) -> dict[str, Any]:
    services = load_services()["services"]
    ids = service_ids or sorted(services)
    registry_text = _fetch_text(COLLECTION_REGISTRY) or ""
    tc_list = _fetch_text(COLLECTION_TENCENTCLOUD_LIST) or ""

    result: dict[str, Any] = {
        "schema": "collection_reconciliation_v1",
        "collection_registry_reachable": bool(registry_text),
        "notes": [],
        "services": {},
    }

    # Collection tencentcloud is IP-CIDR heavy (provider ranges) — domain track stays separate
    if "IP-CIDR" in tc_list:
        result["notes"].append(
            "Collection tencentcloud snapshot is primarily IP-CIDR from third-party list; "
            "Source project keeps domain track separate per IP_POLICY (no ASN→product auto map)."
        )
        result["tencentcloud_collection"] = {
            "list_reachable": True,
            "line_count": len([x for x in tc_list.splitlines() if x.strip() and not x.startswith("#")]),
            "track": "ip_cidr_external",
            "source_action": "supplement_domains_only_do_not_import_provider_ranges",
        }

    for service_id in ids:
        cfg = services.get(service_id, {})
        # local snapshot domains
        local_domains: list[str] = []
        for m in Path("snapshots").glob("*/manifest.json"):
            try:
                data = json.loads(m.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                continue
            if data.get("service_id") == service_id:
                local_domains = list(data.get("domains") or [])
        mentioned = service_id.lower() in registry_text.lower()
        result["services"][service_id] = {
            "configured_status": cfg.get("status"),
            "local_domain_count": len(local_domains),
            "collection_registry_mention": mentioned,
            "recommendation": (
                "keep_domain_track_separate"
                if service_id == "tencentcloud"
                else "promotion_candidate" if local_domains else "needs_materialization"
            ),
        }

    Path("reports").mkdir(exist_ok=True)
    Path("reports/reconciliation.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return result
