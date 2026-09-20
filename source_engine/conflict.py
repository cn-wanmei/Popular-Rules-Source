"""Cross-service domain conflict detection within an ecosystem."""
from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path
from typing import Any

from .build import load_services
from .normalize import normalize_domain


def _latest_domains_map() -> dict[str, set[str]]:
    out: dict[str, set[str]] = defaultdict(set)
    root = Path("snapshots")
    if not root.exists():
        return {}
    latest: dict[str, tuple[str, set[str]]] = {}
    for manifest in root.glob("*/manifest.json"):
        try:
            data = json.loads(manifest.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue
        sid = data.get("service_id")
        if not sid:
            continue
        created = data.get("created_at", "")
        domains = set()
        path = manifest.parent / "domains.txt"
        if path.exists():
            domains = {
                x.strip().lower()
                for x in path.read_text(encoding="utf-8").splitlines()
                if x.strip()
            }
        prev = latest.get(sid)
        if prev is None or created > prev[0]:
            latest[sid] = (created, domains)
    return {k: v[1] for k, v in latest.items()}


def detect_conflicts() -> dict[str, Any]:
    services = load_services()["services"]
    ecosystem: dict[str, list[str]] = defaultdict(list)
    for sid, cfg in services.items():
        ecosystem[str(cfg.get("ecosystem", "unknown"))].append(sid)

    domains_map = _latest_domains_map()
    # also include seeds for services without snapshots
    for sid, cfg in services.items():
        if sid not in domains_map:
            domains_map[sid] = set()
        for s in cfg.get("seed_domains", []):
            d = normalize_domain(str(s))
            if d:
                domains_map[sid].add(d)

    conflicts: list[dict[str, Any]] = []
    # Global domain → services
    inverted: dict[str, list[str]] = defaultdict(list)
    for sid, domains in domains_map.items():
        for d in domains:
            inverted[d].append(sid)

    for domain, owners in sorted(inverted.items()):
        if len(owners) < 2:
            continue
        # same domain claimed by multiple services
        ecos = {str(services.get(o, {}).get("ecosystem", "")) for o in owners}
        conflicts.append(
            {
                "domain": domain,
                "services": sorted(owners),
                "ecosystems": sorted(ecos),
                "severity": "cross_service_domain",
            }
        )

    report = {
        "schema": "conflict_report_v1",
        "conflict_count": len(conflicts),
        "conflicts": conflicts,
        "service_domain_counts": {k: len(v) for k, v in sorted(domains_map.items())},
    }
    Path("reports").mkdir(exist_ok=True)
    Path("reports/conflicts.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return report
