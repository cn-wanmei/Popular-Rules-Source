#!/usr/bin/env python3
import argparse, json
from source_engine.discover import discover_from_config
p = argparse.ArgumentParser()
p.add_argument("--service", required=True)
print(json.dumps(discover_from_config(p.parse_args().service), ensure_ascii=False, indent=2))
