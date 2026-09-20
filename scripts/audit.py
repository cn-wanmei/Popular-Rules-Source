#!/usr/bin/env python3
from source_engine.cli import audit
import json
print(json.dumps(audit(), ensure_ascii=False, indent=2))
