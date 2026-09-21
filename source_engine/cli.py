from __future__ import annotations

import argparse
import json
from pathlib import Path

from .build import build_all, build_service, load_services
from .candidates import audit_candidates
from .conflict import detect_conflicts
from .gap import gap
from .health import probe_all
from .qualification import qualify_all
from .reconcile import audit_collection
from .release import create_release
from .schema_validate import validate_all_snapshots
from .status import write_status
from .tombstone import load_tombstones, revoke_domain
from .validate import run_validation


def audit() -> dict:
    services = load_services()["services"]
    result = {"schema": "service_audit_v3", "services": {}}
    for service_id, cfg in sorted(services.items()):
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
        result["services"][service_id] = {
            "ecosystem": cfg.get("ecosystem"),
            "official_sources": len(cfg.get("official_sources", [])),
            "latest_snapshot": None if latest is None else {
                key: latest.get(key)
                for key in (
                    "snapshot_id",
                    "content_digest",
                    "evidence_digest",
                    "policy_digest",
                    "generator_digest",
                    "release_digest",
                    "release_state",
                    "domain_count",
                )
            },
        }
    Path("reports").mkdir(exist_ok=True)
    Path("reports/service-audit.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return result


def main() -> None:
    parser = argparse.ArgumentParser(prog="source-engine")
    sub = parser.add_subparsers(dest="command", required=True)

    for command in (
        "validate", "audit", "candidate-audit", "test-determinism",
        "schema-validate", "conflict", "health", "qualify", "status"
    ):
        sub.add_parser(command)

    p = sub.add_parser("gap")
    p.add_argument("--service", required=True)
    p.add_argument("--collection-ref")
    p.add_argument("--domain", action="append")

    p = sub.add_parser("discover")
    p.add_argument("--service", required=True)

    p = sub.add_parser("reconcile")
    p.add_argument("--service", action="append")

    p = sub.add_parser("generate")
    p.add_argument("--service")
    p.add_argument("--all", action="store_true")
    p.add_argument("--allow-blocked", action="store_true")

    p = sub.add_parser("release")
    p.add_argument("--service", required=True)

    p = sub.add_parser("revoke")
    p.add_argument("--service", required=True)
    p.add_argument("--domain", required=True)
    p.add_argument("--reason", default="incorrect_attribution")

    p = sub.add_parser("tombstones")
    p.add_argument("--service", required=True)

    args = parser.parse_args()

    if args.command == "validate":
        run_validation()
    elif args.command == "audit":
        print(json.dumps(audit(), ensure_ascii=False, indent=2))
    elif args.command == "candidate-audit":
        print(json.dumps(audit_candidates(), ensure_ascii=False, indent=2))
    elif args.command == "gap":
        print(json.dumps(
            gap(args.service, collection_ref=args.collection_ref, target_domains=args.domain),
            ensure_ascii=False, indent=2
        ))
    elif args.command == "test-determinism":
        from .normalize import normalize_domain, service_asset_id
        cfg = load_services()["services"]["qqmail"]
        configured = cfg.get("allowed_host_exact", []) or cfg.get("allowed_host_suffixes", [])
        values = [normalize_domain(str(x)) for x in configured]
        values = [x for x in values if x]
        assert [service_asset_id("qqmail", x) for x in values] == [service_asset_id("qqmail", x) for x in values]
        print(json.dumps({"determinism": "PASS"}))
    elif args.command == "discover":
        from .discover import discover_from_config
        print(json.dumps(discover_from_config(args.service), ensure_ascii=False, indent=2))
    elif args.command == "reconcile":
        print(json.dumps(
            audit_collection(args.service or sorted(load_services()["services"])),
            ensure_ascii=False, indent=2
        ))
    elif args.command == "qualify":
        print(json.dumps(qualify_all(), ensure_ascii=False, indent=2))
    elif args.command == "status":
        print(json.dumps(write_status(), ensure_ascii=False, indent=2))
    elif args.command == "conflict":
        print(json.dumps(detect_conflicts(), ensure_ascii=False, indent=2))
    elif args.command == "health":
        print(json.dumps(probe_all(), ensure_ascii=False, indent=2))
    elif args.command == "schema-validate":
        errors = validate_all_snapshots()
        if errors:
            print("\n".join(errors))
            raise SystemExit(2)
        print("schema-validate: PASS")
    elif args.command == "generate":
        run_validation()
        if args.all:
            result = build_all()
        elif args.service:
            result = [build_service(args.service)]
        else:
            parser.error("generate requires --service or --all")
        print(json.dumps(result, ensure_ascii=False, indent=2))
        if any(x.get("release_state") == "BLOCKED" for x in result) and not args.allow_blocked:
            raise SystemExit(2)
    elif args.command == "release":
        run_validation()
        print(json.dumps(create_release(args.service), ensure_ascii=False, indent=2))
    elif args.command == "revoke":
        print(json.dumps(
            revoke_domain(args.service, args.domain, reason_type=args.reason),
            ensure_ascii=False, indent=2
        ))
    elif args.command == "tombstones":
        print(json.dumps(load_tombstones(args.service), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
