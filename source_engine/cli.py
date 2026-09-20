from __future__ import annotations

import argparse
import json
from pathlib import Path

from .build import build_all, build_service, load_services


def audit() -> dict:
    services = load_services()["services"]
    result = {
        "schema": "service_gap_v1",
        "services": {},
    }
    for service_id, cfg in sorted(services.items()):
        result["services"][service_id] = {
            "configured_status": cfg.get("status", "review"),
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


def main() -> None:
    parser = argparse.ArgumentParser(prog="source-engine")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("audit")
    generate = sub.add_parser("generate")
    generate.add_argument("--service")
    generate.add_argument("--all", action="store_true")
    release = sub.add_parser("release")
    release.add_argument("--service", required=True)

    args = parser.parse_args()

    if args.command == "audit":
        print(json.dumps(audit(), ensure_ascii=False, indent=2))
        return

    if args.command == "generate":
        if args.all:
            manifests = build_all()
        elif args.service:
            manifests = [build_service(args.service)]
        else:
            parser.error("generate requires --service or --all")
        print(json.dumps(manifests, ensure_ascii=False, indent=2))
        if any(m["release_state"] == "BLOCKED" for m in manifests):
            raise SystemExit(2)
        return

    if args.command == "release":
        manifest = build_service(args.service)
        if manifest["release_state"] != "CANDIDATE":
            raise SystemExit(f"release blocked/review: {manifest['release_state']}")
        print(json.dumps({
            "release_state": "CANDIDATE",
            "snapshot_id": manifest["snapshot_id"],
        }, ensure_ascii=False, indent=2))
        return
