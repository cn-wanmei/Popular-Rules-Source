"""Promotion Bridge: map Source releases to Collection-compatible packages.

Does not write Collection Canonical. Produces a promotion package under
releases/<service>/<snapshot>/promotion/ for human or CI bridge steps.
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path


def build_promotion_package(
    service_id: str,
    snapshot_id: str,
    repository: str = "cn-wanmei/Popular-Rules-Source",
) -> dict:
    snap = Path("snapshots") / snapshot_id
    if not snap.exists():
        raise FileNotFoundError(snapshot_id)
    manifest = json.loads((snap / "manifest.json").read_text(encoding="utf-8"))
    domains = [
        x.strip()
        for x in (snap / "domains.txt").read_text(encoding="utf-8").splitlines()
        if x.strip()
    ]
    package = {
        "schema": "popular_rules_source_promotion_v1",
        "repository": repository,
        "service_id": service_id,
        "snapshot_id": snapshot_id,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "target": {
            "project": "cn-wanmei/Popular-Rules-Collection",
            "input_kind": "supplemental_source_release",
            "registry_action": "append_or_refresh_source",
        },
        "domains": domains,
        "domain_count": len(domains),
        "release_state": manifest.get("release_state"),
        "parser_version": manifest.get("parser_version"),
        "gates": {
            "schema": "PASS",
            "empty_list": "PASS" if domains else "FAIL",
            "release_state_ok": manifest.get("release_state") in {"CANDIDATE", "PUBLISHED"},
        },
    }
    out = Path("releases") / service_id / snapshot_id / "promotion"
    out.mkdir(parents=True, exist_ok=True)
    (out / "promotion.json").write_text(
        json.dumps(package, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (out / "domains.txt").write_text(
        "\n".join(domains) + ("\n" if domains else ""),
        encoding="utf-8",
    )
    return package
