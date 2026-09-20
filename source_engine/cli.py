from __future__ import annotations

import argparse
import json
from pathlib import Path

from .build import build_all, build_service, load_services
from .candidates import audit_candidates
from .conflict import detect_conflicts
from .health import probe_all
from .schema_validate import validate_all_snapshots
from .discover import discover_from_config
from .reconcile import audit_collection
from .release import create_release
from .tombstone import load_tombstones, revoke_domain
from .validate import run_validation


def audit() -> dict:
    services = load_services()["services"]
    result = {"schema": "service_gap_v2", "services": {}}
    manifests = {}
    if Path("snapshots").exists():
        for path in Path("snapshots").glob("*/manifest.json"):
            try:
                data = json.loads(path.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError):
                continue
            manifests.setdefault(data.get("service_id"), []).append(data)

    for service_id, cfg in sorted(services.items()):
        latest = None
        for data in manifests.get(service_id, []):
            if latest is None or data.get("created_at", "") > latest.get("created_at", ""):
                latest = data
        result["services"][service_id] = {
            "configured_status": cfg.get("status", "review"),
            "ecosystem": cfg.get("ecosystem"),
            "official_sources": len(cfg.get("official_sources", [])),
            "authoring_seed_domains": 0,
            "latest_snapshot": None if latest is None else {
                "snapshot_id": latest.get("snapshot_id"),
                "content_digest": latest.get("content_digest"),
                "release_state": latest.get("release_state"),
                "domain_count": latest.get("domain_count"),
                "official_extracted": latest.get("official_extracted"),
                "seed_only_count": latest.get("seed_only_count"),
            },
        }

    Path("reports").mkdir(exist_ok=True)
    Path("reports/service-gap.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return result


def test_determinism(service_id: str = "qqmail") -> None:
    from .normalize import normalize_domain, service_asset_id
    cfg = load_services()["services"][service_id]
    configured = cfg.get("allowed_host_exact", []) or cfg.get("allowed_host_suffixes", [])
    domains = sorted({
        d for raw in configured
        if (d := normalize_domain(str(raw))) is not None
    })
    if not domains:
        domains = [normalize_domain(service_id + ".example.invalid")]
    a = [service_asset_id(service_id, d) for d in domains]
    b = [service_asset_id(service_id, d) for d in domains]
    if a != b:
        raise SystemExit("determinism fail: asset IDs diverged")
    print(json.dumps({"service_id": service_id, "determinism": "PASS"}, indent=2))


def main() -> None:
    parser = argparse.ArgumentParser(prog="source-engine")
    sub = parser.add_subparsers(dest="command", required=True)

    for command in [
        "validate", "audit", "gap", "candidate-audit", "test-determinism", "schema-validate",
        "conflict", "health"
    ]:
        sub.add_parser(command)

    discover = sub.add_parser("discover")
    discover.add_argument("--service", required=True)

    reconcile = sub.add_parser("reconcile")
    reconcile.add_argument("--service", action="append")

    generate = sub.add_parser("generate")
    generate.add_argument("--service")
    generate.add_argument("--all", action="store_true")

    release = sub.add_parser("release")
    release.add_argument("--service", required=True)

    revoke = sub.add_parser("revoke")
    revoke.add_argument("--service", required=True)
    revoke.add_argument("--domain", required=True)
    revoke.add_argument("--reason", default="incorrect_attribution")

    tombstones = sub.add_parser("tombstones")
    tombstones.add_argument("--service", required=True)

    args = parser.parse_args()

    if args.command == "candidate-audit":
        print(json.dumps(audit_candidates(), ensure_ascii=False, indent=2))
    elif args.command == "validate":
        run_validation()
    elif args.command in {"audit", "gap"}:
        print(json.dumps(audit(), ensure_ascii=False, indent=2))
    elif args.command == "test-determinism":
        test_determinism()
    elif args.command == "discover":
        print(json.dumps(discover_from_config(args.service), ensure_ascii=False, indent=2))
    elif args.command == "reconcile":
        ids = args.service or sorted(load_services()["services"])
        print(json.dumps(audit_collection(ids), ensure_ascii=False, indent=2))
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
            manifests = build_all()
        elif args.service:
            manifests = [build_service(args.service)]
        else:
            parser.error("generate requires --service or --all")
        print(json.dumps(manifests, ensure_ascii=False, indent=2))
        if any(m["release_state"] == "BLOCKED" for m in manifests):
            raise SystemExit(2)
    elif args.command == "release":
        run_validation()
        print(json.dumps(create_release(args.service), ensure_ascii=False, indent=2))
    elif args.command == "revoke":
        print(json.dumps(
            revoke_domain(args.service, args.domain, reason_type=args.reason),
            ensure_ascii=False,
            indent=2,
        ))
    elif args.command == "tombstones":
        print(json.dumps(load_tombstones(args.service), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
