#!/usr/bin/env python3
import json
from source_engine.reconcile import audit_collection
from source_engine.build import load_services
print(json.dumps(audit_collection(sorted(load_services()["services"])), ensure_ascii=False, indent=2))
