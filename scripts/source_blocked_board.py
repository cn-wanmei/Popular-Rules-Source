#!/usr/bin/env python3
"""source_blocked_board.py — Emit BLOCKED / domains=0 / failed board from lifecycle SSOT + README table.

Outputs:
  docs/BLOCKED_BOARD.md
  reports/blocked_board.json (if reports/ exists or created)
"""
from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / "config" / "source_canary_state.yaml"
README = ROOT / "README.md"
OUT_MD = ROOT / "docs" / "BLOCKED_BOARD.md"
OUT_JSON = ROOT / "reports" / "blocked_board.json"


def _parse_yaml_services(text: str) -> dict[str, dict]:
    services: dict[str, dict] = {}
    cur = None
    in_services = False
    for line in text.splitlines():
        if line.startswith("services:"):
            in_services = True
            continue
        if not in_services:
            continue
        if line and not line.startswith(" ") and not line.startswith("\t"):
            break
        m = re.match(r"^  ([\'\"]?)([A-Za-z0-9_.-]+)\1:\s*$", line)
        if m:
            cur = m.group(2)
            services[cur] = {}
            continue
        if cur is None:
            continue
        m2 = re.match(r"^    ([a-z_]+):\s*(.+)$", line)
        if m2:
            k, v = m2.group(1), m2.group(2).strip().strip("'\"")
            services[cur][k] = v
    return services


def _parse_readme_table(text: str) -> list[dict]:
    rows = []
    for line in text.splitlines():
        if not line.startswith("|") or "Lifecycle" in line or line.startswith("|---"):
            continue
        parts = [p.strip() for p in line.strip("|").split("|")]
        if len(parts) < 4:
            continue
        svc, life, rel, domains = parts[0], parts[1], parts[2], parts[3]
        life_c = re.sub(r"\*+", "", life).strip()
        rel_c = re.sub(r"\*+", "", rel).strip()
        try:
            dom_n = int(re.sub(r"[^0-9-]", "", domains) or "0")
        except ValueError:
            dom_n = -1
        rows.append({"service": svc, "lifecycle": life_c, "release": rel_c, "domains": dom_n})
    return rows


def main() -> int:
    services = {}
    if STATE.is_file():
        services = _parse_yaml_services(STATE.read_text(encoding="utf-8"))
    rows = []
    if README.is_file():
        rows = _parse_readme_table(README.read_text(encoding="utf-8"))

    blocked = []
    zero_dom = []
    for r in rows:
        if r["release"].upper() == "BLOCKED" or r["lifecycle"].upper() == "BLOCKED":
            blocked.append(r)
        if r["domains"] == 0:
            zero_dom.append(r)

    yaml_blocked = [
        {"service": k, **v}
        for k, v in services.items()
        if str(v.get("state", "")).lower() == "blocked"
    ]

    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    payload = {
        "generated_at": now,
        "blocked_from_readme": blocked,
        "domains_zero": zero_dom,
        "blocked_from_yaml": yaml_blocked,
        "priority": [
            "1. state=blocked or Release=BLOCKED",
            "2. domains=0",
            "3. Collection PUBLISH_STATUS source failed",
            "4. long-lived REVIEW without snapshot growth",
        ],
    }

    lines = [
        "# Source 阻塞看板（自动生成）",
        "",
        f"> generated_at: `{now}`",
        "",
        "权威：`config/source_canary_state.yaml` + README lifecycle 表。",
        "",
        "## BLOCKED",
        "",
    ]
    if blocked or yaml_blocked:
        lines.append("| Service | Lifecycle | Release | Domains |")
        lines.append("|---|---|---|---:|")
        seen = set()
        for r in blocked:
            seen.add(r["service"])
            lines.append(f"| {r['service']} | {r['lifecycle']} | {r['release']} | {r['domains']} |")
        for r in yaml_blocked:
            if r["service"] in seen:
                continue
            lines.append(f"| {r['service']} | blocked | — | — |")
    else:
        lines.append("_当前 README/YAML 无 BLOCKED 条目。_")

    lines += ["", "## domains = 0", ""]
    if zero_dom:
        lines.append("| Service | Lifecycle | Release | Domains |")
        lines.append("|---|---|---|---:|")
        for r in zero_dom:
            lines.append(f"| {r['service']} | {r['lifecycle']} | {r['release']} | {r['domains']} |")
    else:
        lines.append("_无 domains=0 行（或 README 表未嵌入）。_")

    lines += [
        "",
        "## 处理原则",
        "",
        "1. 禁止用空结果覆盖 Last Known Good。",
        "2. BLOCKED / domains=0 必须先修 adapter 或明确策略，再谈晋升。",
        "3. Collection Source health `failed` 与本表交叉核对。",
        "",
    ]
    OUT_MD.parent.mkdir(parents=True, exist_ok=True)
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {OUT_MD} blocked={len(blocked)+len(yaml_blocked)} domains0={len(zero_dom)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
