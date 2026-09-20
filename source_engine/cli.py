from __future__ import annotations

import argparse
import json
from pathlib import Path

from .build import build_all, build_service, load_services
from .conflict import detect_conflicts
from .health import probe_all
from .quality import score_services
from .engineering import engineering_report
from .schema_validate import validate_all_snapshots
from .discover import discover_from_config
from .promotion import build_promotion_package
from .reconcile import audit_collection
from .release import create_release
from .tombstone import load_tombstones, revoke_domain
from .validate import run_validation


def audit() -> dict:
    services = load_services()["services"]
    result = {"schema": "service_gap_v1", "services": {}}
    snaps = list(Path("snapshots").glob("*/manifest.json")) if Path("snapshots").exists() else []
    for service_id, cfg in sorted(services.items()):
        latest = None
        for m in snaps:
            try:
                data = json.loads(m.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                continue
            if data.get("service_id") == service_id:
                if latest is None or data.get("created_at", "") > latest.get("created_at", ""):
                    latest = data
        result["services"][service_id] = {
            "configured_status": cfg.get("status", "review"),
            "ecosystem": cfg.get("ecosystem"),
            "official_sources": len(cfg.get("official_sources", [])),
            "seed_domains": len(cfg.get("seed_domains", [])),
            "allowed_suffixes": len(cfg.get("allowed_host_suffixes", [])),
            "allowed_exact": len(cfg.get("allowed_host_exact", [])),
            "latest_snapshot": None
            if latest is None
            else {
                "snapshot_id": latest.get("snapshot_id"),
                "release_state": latest.get("release_state"),
                "domain_count": latest.get("domain_count"),
            },
        }
    Path("reports").mkdir(exist_ok=True)
    Path("reports/service-gap.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return result


def definition_of_done() -> dict:
    """Report DoD checklist status per plan section 73."""
    services = load_services()["services"]
    report = {"schema": "definition_of_done_v1", "services": {}}
    for service_id in sorted(services):
        cfg = services[service_id]
        has_snap = any(
            json.loads(p.read_text()).get("service_id") == service_id
            for p in Path("snapshots").glob("*/manifest.json")
            if p.exists()
        )
        authoring = Path("authoring/services") / service_id
        report["services"][service_id] = {
            "service_manifest": (authoring / "service.yaml").exists(),
            "official_sources": bool(cfg.get("official_sources")),
            "seed_or_generated": bool(cfg.get("seed_domains")) or has_snap,
            "snapshot_exists": has_snap,
            "exclusions_file": (authoring / "exclusions.yaml").exists(),
            "boundary_documented": cfg.get("ecosystem") in {"alibaba", "tencent"},
            "status": cfg.get("status"),
        }
    Path("reports").mkdir(exist_ok=True)
    Path("reports/definition-of-done.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return report


def test_determinism(service_id: str = "qqmail") -> None:
    from .normalize import normalize_domain, service_asset_id

    services = load_services()["services"]
    cfg = services[service_id]
    domains = sorted(
        {
            d
            for x in cfg.get("seed_domains", [])
            if (d := normalize_domain(str(x))) is not None
        }
    )
    a = [service_asset_id(service_id, d) for d in domains]
    b = [service_asset_id(service_id, d) for d in domains]
    if a != b:
        raise SystemExit("determinism fail: asset ids diverged")
    print(json.dumps({"service_id": service_id, "domains": domains, "determinism": "PASS"}, indent=2))


def main() -> None:
    parser = argparse.ArgumentParser(prog="source-engine")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("validate")
    sub.add_parser("audit")
    sub.add_parser("gap")
    sub.add_parser("test-determinism")
    sub.add_parser("dod")
    sub.add_parser("conflict")
    sub.add_parser("health")
    sub.add_parser("quality")
    sub.add_parser("schema-validate")
    sub.add_parser("engineering")

    discover = sub.add_parser("discover")
    discover.add_argument("--service", required=True)

    reconcile = sub.add_parser("reconcile")
    reconcile.add_argument("--service", action="append")

    generate = sub.add_parser("generate")
    generate.add_argument("--service")
    generate.add_argument("--all", action="store_true")

    release = sub.add_parser("release")
    release.add_argument("--service", required=True)

    promote = sub.add_parser("promote")
    promote.add_argument("--service", required=True)
    promote.add_argument("--snapshot", required=True)

    revoke = sub.add_parser("revoke")
    revoke.add_argument("--service", required=True)
    revoke.add_argument("--domain", required=True)
    revoke.add_argument("--reason", default="incorrect_attribution")

    tombstones = sub.add_parser("tombstones")
    tombstones.add_argument("--service", required=True)

    args = parser.parse_args()

    if args.command == "validate":
        run_validation()
        return

    if args.command in {"audit", "gap"}:
        print(json.dumps(audit(), ensure_ascii=False, indent=2))
        return

    if args.command == "dod":
        print(json.dumps(definition_of_done(), ensure_ascii=False, indent=2))
        return

    if args.command == "discover":
        print(json.dumps(discover_from_config(args.service), ensure_ascii=False, indent=2))
        return

    if args.command == "test-determinism":
        test_determinism()
        return

    if args.command == "reconcile":
        service_ids = args.service or sorted(load_services()["services"])
        print(json.dumps(audit_collection(service_ids), ensure_ascii=False, indent=2))
        return

    if args.command == "conflict":
        print(json.dumps(detect_conflicts(), ensure_ascii=False, indent=2))
        return

    if args.command == "health":
        print(json.dumps(probe_all(), ensure_ascii=False, indent=2))
        return

    if args.command == "quality":
        print(json.dumps(score_services(), ensure_ascii=False, indent=2))
        return

    if args.command == "schema-validate":
        errs = validate_all_snapshots()
        if errs:
            print("\n".join(errs))
            raise SystemExit(2)
        print("schema-validate: PASS")
        return

    if args.command == "engineering":
        print(json.dumps(engineering_report(), ensure_ascii=False, indent=2))
        return

    if args.command == "generate":
        run_validation()
        if args.all:
            manifests = build_all()
        elif args.service:
            manifests = [build_service(args.service)]
        else:
            parser.error("generate requires --service or --all")
        print(json.dumps(manifests, ensure_ascii=False, indent=2))
        blocked = [m for m in manifests if m["release_state"] == "BLOCKED"]
        if blocked:
            raise SystemExit(2)
        return

    if args.command == "promote":
        pkg = build_promotion_package(args.service, args.snapshot)
        print(json.dumps(pkg, ensure_ascii=False, indent=2))
        if not pkg["gates"]["release_state_ok"] or pkg["gates"]["empty_list"] == "FAIL":
            raise SystemExit(2)
        return

    if args.command == "release":
        run_validation()
        print(json.dumps(create_release(args.service), ensure_ascii=False, indent=2))
        return

    if args.command == "revoke":
        data = revoke_domain(args.service, args.domain, reason_type=args.reason)
        print(json.dumps(data, ensure_ascii=False, indent=2))
        return

    if args.command == "tombstones":
        print(json.dumps(load_tombstones(args.service), ensure_ascii=False, indent=2))
        return


if __name__ == "__main__":
    main()
