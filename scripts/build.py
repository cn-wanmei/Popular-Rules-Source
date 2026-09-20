#!/usr/bin/env python3
from source_engine.build import build_all
import json
print(json.dumps(build_all(), ensure_ascii=False, indent=2))
