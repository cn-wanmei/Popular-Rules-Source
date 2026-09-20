"""Engineering skeleton completeness vs final architecture plan."""
from __future__ import annotations

import json
from pathlib import Path


CHECKS = [
    ("docs_architecture", Path("docs/ARCHITECTURE.md").exists()),
    ("docs_policies", all(Path(f"docs/{n}.md").exists() for n in [
        "SERVICE_POLICY", "EVIDENCE_POLICY", "DOMAIN_POLICY", "RELEASE_POLICY",
        "PROMOTION_CONTRACT", "SECURITY", "IP_POLICY",
    ])),
    ("schemas_frozen", Path("config/schemas.yaml").exists() and Path("schemas/snapshot.schema.json").exists()),
    ("authoring_tree", Path("authoring/services/1688/service.yaml").exists()),
    ("exclusion_catalog", Path("exclusions/shared.yaml").exists()),
    ("official_catalog", Path("config/official_endpoint_catalog.yaml").exists()),
    ("fetch_extract_normalize", Path("source_engine/fetch.py").exists() and Path("source_engine/extract.py").exists()),
    ("build_snapshot", Path("source_engine/build.py").exists()),
    ("tombstone", Path("source_engine/tombstone.py").exists()),
    ("diff", Path("source_engine/diff.py").exists()),
    ("conflict", Path("source_engine/conflict.py").exists()),
    ("health", Path("source_engine/health.py").exists()),
    ("quality", Path("source_engine/quality.py").exists()),
    ("promotion", Path("source_engine/promotion.py").exists()),
    ("reconcile", Path("source_engine/reconcile.py").exists()),
    ("discover", Path("source_engine/discover.py").exists()),
    ("overrides", Path("source_engine/overrides.py").exists()),
    ("schema_validate", Path("source_engine/schema_validate.py").exists()),
    ("scripts_wrappers", Path("scripts/build.py").exists() and Path("scripts/audit.py").exists()),
    ("ci_validate", Path(".github/workflows/validate.yml").exists()),
    ("ci_generate", Path(".github/workflows/generate.yml").exists()),
    ("ci_audit", Path(".github/workflows/audit.yml").exists()),
    ("ci_build", Path(".github/workflows/build.yml").exists()),
    ("ci_release", Path(".github/workflows/release.yml").exists()),
    ("ci_reconcile", Path(".github/workflows/reconcile.yml").exists()),
    ("tests_present", Path("tests/test_engine.py").exists() and Path("tests/test_1688_fixtures.py").exists()),
    ("snapshots_exist", any(Path("snapshots").glob("*/manifest.json"))),
    ("generated_exist", any(Path("generated/source").glob("*/domains.txt"))),
    ("boundary_alibaba", Path("docs/ALIBABA_BOUNDARY.md").exists()),
    ("boundary_tencent", Path("docs/TENCENT_BOUNDARY.md").exists()),
]


def engineering_report() -> dict:
    items = [{"id": k, "pass": bool(v)} for k, v in CHECKS]
    passed = sum(1 for i in items if i["pass"])
    total = len(items)
    pct = round(100.0 * passed / total, 1) if total else 0
    report = {
        "schema": "engineering_completeness_v1",
        "passed": passed,
        "total": total,
        "percent": pct,
        "target": 95,
        "meets_target": pct >= 95,
        "items": items,
    }
    Path("reports").mkdir(exist_ok=True)
    Path("reports/engineering-completeness.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return report
