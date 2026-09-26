from __future__ import annotations

import json
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]


def load_yaml(path: str) -> dict:
    value = yaml.safe_load((ROOT / path).read_text(encoding="utf-8"))
    return value if isinstance(value, dict) else {}


def main() -> int:
    program = load_yaml("config/service_completion_program.yaml")
    targets = load_yaml("config/company_targets.yaml")
    self_built = load_yaml("config/self_built_services.yaml")
    services = load_yaml("config/services.yaml").get("services") or {}

    companies = targets.get("companies") or []
    failures: list[str] = []
    if len(companies) != 200:
        failures.append(f"company target count != 200: {len(companies)}")
    ids = [str(x.get("company_id")) for x in companies]
    if len(set(ids)) != len(ids):
        failures.append("duplicate company_id in target registry")
    for phase in ("P0-A", "P0-B", "P0-C", "P1", "P2"):
        if phase not in (program.get("phases") or {}):
            failures.append(f"missing phase: {phase}")

    lineage = ((program.get("lineage_lock") or {}).get("sequence") or [])
    expected = ["qqmail", "qqmusic", "taobao", "tencentcloud", "tmall"]
    if lineage != expected:
        failures.append(f"lineage lock mismatch: {lineage!r}")

    catalog = self_built.get("services") or {}
    priority = load_yaml("config/p1_p2_self_built_official_wave.yaml").get("services") or {}
    p0c = (((program.get("phases") or {}).get("P0-C") or {}).get("platform_groups") or {})
    p0c_ids: set[str] = set()
    for group in p0c.values():
        for item in group.get("confirmed_independent_hosts") or []:
            sid = item.get("service_id")
            if sid:
                p0c_ids.add(str(sid))
    missing = sorted(sid for sid in p0c_ids if sid not in catalog or sid not in services)
    if missing:
        failures.append(f"P0-C service IDs missing from self-built catalog/services: {missing}")

    expected_priority = set(priority)
    service_config_ids = set(services)
    missing_priority = sorted(expected_priority - service_config_ids)
    if missing_priority:
        failures.append(f"priority wave missing from services.yaml: {missing_priority}")
    report = {
        "schema": "service_completion_program_audit_v1",
        "pass": not failures,
        "company_count": len(companies),
        "p0c_confirmed_service_count": len(p0c_ids),
        "priority_wave_service_count": len(expected_priority),
        "p0a_lineage": lineage,
        "failures": failures,
    }
    reports = ROOT / "reports"
    reports.mkdir(exist_ok=True)
    (reports / "service-completion-program.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
