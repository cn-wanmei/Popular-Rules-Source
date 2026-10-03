#!/usr/bin/env python3
"""One-shot restore canary from known-good commit + apply weekly funnel batch."""
from __future__ import annotations
import re
import urllib.request
from pathlib import Path
URL = "https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Source/898b20a5b4b1420edb76bd8e13d2fca0e905d1ce/config/source_canary_state.yaml"
OUT = Path("config/source_canary_state.yaml")
TARGETS = ["appledev", "appstore", "icloud", "applemusic", "applemedia", "azure", "openai", "claude"]
req = urllib.request.Request(URL, headers={"User-Agent": "restore-canary"})
with urllib.request.urlopen(req, timeout=60) as r:
    text = r.read().decode("utf-8")
for svc in TARGETS:
    pat = rf"(  {re.escape(svc)}:\n    state: )verified(\n    enabled: true\n    reason: )[^\n]+(\n    last_transition: )'[0-9-]+'"
    repl = rf"\1canary\2weekly_funnel_quota_2026-10-03\3'2026-10-03'"
    text, n = re.subn(pat, repl, text, count=1)
    if n != 1:
        raise SystemExit(f"fail {svc} n={n}")
OUT.write_text(text, encoding="utf-8")
print(f"restored {OUT} bytes={len(text)} canary={text.count('state: canary')}")
