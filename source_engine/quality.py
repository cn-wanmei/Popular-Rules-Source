"""Promotion-readiness quality score per service (0-100).

Weights are calibrated so a solid first-wave service lands ~90–95,
not auto-100. Perfect 100 requires PUBLISHED + deep coverage + no issues.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .build import load_services
from .conflict import detect_conflicts
from .tombstone import load_revoked_domains


def score_services() -> dict[str, Any]:
    services = load_services()["services"]
    conflicts = detect_conflicts()
    conflicted = set()
    for c in conflicts.get("conflicts", []):
        conflicted.update(c.get("services", []))

    has_catalog = Path("config/official_endpoint_catalog.yaml").exists()
    report: dict[str, Any] = {"schema": "quality_score_v1", "services": {}, "summary": {}}
    scores: list[int] = []

    for sid, cfg in sorted(services.items()):
        score = 0
        notes: list[str] = []

        # --- Evidence / policy (max 35) ---
        if cfg.get("official_sources"):
            score += 12
        else:
            notes.append("no_official_sources")
        exact = cfg.get("allowed_host_exact") or []
        suffixes = cfg.get("allowed_host_suffixes") or []
        if exact or suffixes:
            score += 8
        if exact and not suffixes:
            score += 4
            notes.append("exact_host_policy")
        seeds = cfg.get("seed_domains") or []
        if len(seeds) >= 8:
            score += 8
        elif len(seeds) >= 5:
            score += 6
        elif len(seeds) >= 3:
            score += 4
        elif seeds:
            score += 2
        if has_catalog:
            score += 3

        # --- Snapshot / materialization (max 40) ---
        latest = None
        for m in Path("snapshots").glob("*/manifest.json"):
            try:
                data = json.loads(m.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                continue
            if data.get("service_id") == sid:
                if latest is None or data.get("created_at", "") > latest.get("created_at", ""):
                    latest = data
        domain_count = 0
        if latest:
            score += 10
            domain_count = int(latest.get("domain_count") or 0)
            st = latest.get("release_state")
            if st == "PUBLISHED":
                score += 12
            elif st == "CANDIDATE":
                score += 10
            elif st == "REVIEW":
                score += 3
                notes.append("review_state")
            if domain_count >= 12:
                score += 12
            elif domain_count >= 8:
                score += 10
            elif domain_count >= 5:
                score += 8
            elif domain_count >= 3:
                score += 5
            elif domain_count >= 1:
                score += 2
            if latest.get("errors"):
                score -= 8
                notes.append("snapshot_errors")
            if latest.get("last_known_good"):
                score -= 5
                notes.append("used_last_known_good")
        else:
            notes.append("no_snapshot")

        # --- Governance (max 25) ---
        if cfg.get("ecosystem"):
            score += 4
        if cfg.get("boundary", {}).get("shared_infrastructure_allowed") is False:
            score += 4
        if (Path("authoring/services") / sid / "service.yaml").exists():
            score += 4
        if (Path("authoring/services") / sid / "exclusions.yaml").exists():
            score += 3
        if sid not in conflicted:
            score += 6
        else:
            score -= 20
            notes.append("cross_service_conflict")
        if load_revoked_domains(sid):
            score += 2
            notes.append("has_tombstones")
        # coverage field
        cov = (cfg.get("coverage") or {}).get("domain")
        if cov == "complete":
            score += 8
            notes.append("coverage_complete")
        elif cov == "high":
            score += 5
        elif cov == "partial":
            score += 2

        score = max(0, min(100, score))
        scores.append(score)
        report["services"][sid] = {
            "score": score,
            "domain_count": domain_count,
            "release_state": None if not latest else latest.get("release_state"),
            "status": cfg.get("status"),
            "notes": notes,
            "promotion_ready": (
                score >= 80
                and sid not in conflicted
                and domain_count >= 2
                and (latest or {}).get("release_state") in {"CANDIDATE", "PUBLISHED"}
            ),
        }

    avg = round(sum(scores) / len(scores), 1) if scores else 0
    report["summary"] = {
        "avg_score": avg,
        "min_score": min(scores) if scores else 0,
        "max_score": max(scores) if scores else 0,
        "promotion_ready_count": sum(1 for s in report["services"].values() if s["promotion_ready"]),
        "conflict_count": conflicts.get("conflict_count", 0),
        "target_avg": 95,
        "meets_target_avg": avg >= 95,
        "engineering_completeness_note": (
            "Skeleton gates (conflict/health/schema/LKG/tombstone/promotion) are in tree; "
            "score reflects domain-track promotion readiness under evidence policy."
        ),
    }
    Path("reports").mkdir(exist_ok=True)
    Path("reports/quality-score.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return report
