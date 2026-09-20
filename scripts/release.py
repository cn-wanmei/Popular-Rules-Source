#!/usr/bin/env python3
import argparse, json
from source_engine.release import create_release
p = argparse.ArgumentParser()
p.add_argument("--service", required=True)
args = p.parse_args()
print(json.dumps(create_release(args.service), ensure_ascii=False, indent=2))
