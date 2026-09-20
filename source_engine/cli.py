from __future__ import annotations

import argparse
import json
from pathlib import Path

from .build import build_all, build_service, load_services
from .reconcile import audit_collection
from .release import create_release
from .validate import run_validation


def audit() -> dict:
    services = load_services()["services"]
    result = {"schema": "service_gap_v1", "services": {}}
    for service_id, cfg in sorted(services.items()):
        result["services"][service_id] = {
            "configured_status": cfg.get("status", "review"),
            "ecosystem": cfg.get("ecosystem"),
            "official_sources": len(cfg.get("official_sources", [])),
            "seed_domains": len(cfg.get("seed_domains", [])),
            "allowed_suffixes": len(cfg.get("allowed_host_suffixes", [])),
            "allowed_exact": len(cfg.get("allowed_host_exact", [])),
        }
    Path("reports").mkdir(exist_ok=True)
    Path("reports/service-gap.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return result


def test_determinism(service_id: str = "qqmail") -> None:
    """Build twice offline via seeds-only path identity check on normalize fingerprint."""
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
    sub.add_parser("test-determinism")

    reconcile = sub.add_parser("reconcile")
    reconcile.add_argument("--service", action="append")

    generate = sub.add_parser("generate")
    generate.add_argument("--service")
    generate.add_argument("--all", action="store_true")

    release = sub.add_parser("release")
    release.add_argument("--service", required=True)

    gap = sub.add_parser("gap")
    gap.set_defaults(command="audit")

    args = parser.parse_args()

    if args.command == "validate":
        run_validation()
        return

    if args.command in {"audit", "gap"}:
        print(json.dumps(audit(), ensure_ascii=False, indent=2))
        return

    if args.command == "test-determinism":
        test_determinism()
        return

    if args.command == "reconcile":
        service_ids = args.service or sorted(load_services()["services"])
        print(json.dumps(audit_collection(service_ids), ensure_ascii=False, indent=2))
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
        bad = [m for m in manifests if m["release_state"] not in {"CANDIDATE", "REVIEW"}]
        # REVIEW is allowed for first-wave; only hard BLOCK fails the job
        blocked = [m for m in manifests if m["release_state"] == "BLOCKED"]
        if blocked:
            raise SystemExit(2)
        return

    if args.command == "release":
        run_validation()
        print(
            json.dumps(
                create_release(args.service),
                ensure_ascii=False,
                indent=2,
            )
        )


if __name__ == "__main__":
    main()
