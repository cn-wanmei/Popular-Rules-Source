#!/usr/bin/env python3
"""Alias: generate creates immutable snapshots."""
import argparse, json
from source_engine.build import build_service, build_all
p = argparse.ArgumentParser()
p.add_argument("--service")
p.add_argument("--all", action="store_true")
args = p.parse_args()
if args.all:
    print(json.dumps(build_all(), ensure_ascii=False, indent=2))
elif args.service:
    print(json.dumps([build_service(args.service)], ensure_ascii=False, indent=2))
else:
    raise SystemExit("require --service or --all")
