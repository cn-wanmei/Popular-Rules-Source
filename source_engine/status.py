from __future__ import annotations

import json
from datetime import datetime, timezone
from collections import Counter
from pathlib import Path
from typing import Any

import yaml

from .build import load_services
from .qualification import qualify_all

START = "<!-- SOURCE_STATUS:START -->"
END = "<!-- SOURCE_STATUS:END -->"


def _latest(service_id: str) -> dict[str, Any] | None:
    latest = None
    for path in Path("snapshots").glob("*/manifest.json"):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        if data.get("service_id") != service_id:
            continue
        if latest is None or str(data.get("created_at", "")) > str(latest.get("created_at", "")):
            latest = data
    return latest


def build_status_report() -> dict[str, Any]:
    lifecycle = yaml.safe_load(Path("config/source_canary_state.yaml").read_text(encoding="utf-8")) or {}
    services = load_services()["services"]
    declared = lifecycle.get("services") or {}
    result = {"schema": "popular_rules_source_lifecycle_report_v1", "services": {}}
    for service_id in sorted(services):
        state = declared.get(service_id) or {}
        manifest = _latest(service_id)
        result["services"][service_id] = {
            "state": state.get("state", "review"),
            "enabled": state.get("enabled") is True,
            "snapshot_id": (manifest or {}).get("snapshot_id"),
            "release_state": (manifest or {}).get("release_state", "NO_SNAPSHOT"),
            "domain_count": (manifest or {}).get("domain_count", 0),
            "content_digest": (manifest or {}).get("content_digest"),
            "evidence_digest": (manifest or {}).get("evidence_digest"),
            "policy_digest": (manifest or {}).get("policy_digest"),
            "generator_digest": (manifest or {}).get("generator_digest"),
            "release_digest": (manifest or {}).get("release_digest"),
        }
    return result


def _render(report: dict[str, Any]) -> str:
    """Compact README block. Full table is in reports/generated/lifecycle.json only."""
    counts: Counter[str] = Counter()
    blocked_release = 0
    for item in report["services"].values():
        counts[str(item.get("state") or "review").lower()] += 1
        if str(item.get("release_state") or "").upper() == "BLOCKED":
            blocked_release += 1
    total = sum(counts.values())
    by_state = ", ".join(f"{k.upper()}={v}" for k, v in sorted(counts.items()))
    lines = [
        START,
        "### Source lifecycle (summary)",
        "",
        f"- **Services tracked:** {total}",
        f"- **By state:** {by_state}",
        f"- **Release BLOCKED:** {blocked_release}",
        "",
        "> Per-service rows: [`reports/generated/lifecycle.json`](reports/generated/lifecycle.json)  ",
        "> Lifecycle SSOT: [`config/source_canary_state.yaml`](config/source_canary_state.yaml)  ",
        "> Ops: [`docs/FUNNEL_ACCELERATION.md`](docs/FUNNEL_ACCELERATION.md) · [`docs/BLOCKED_BOARD.md`](docs/BLOCKED_BOARD.md)",
        "",
        "```bash",
        "python -m source_engine health",
        "python -m source_engine qualify",
        "```",
        END,
    ]
    return "\n".join(lines)


def _render_blocked_board(
    report: dict[str, Any], generated_at: str | None = None
) -> str:
    """Render the operational blocked board from the lifecycle read model."""
    stamp = generated_at or datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")
    services = report.get("services") or {}
    blocked = []
    zero_domains = []
    for service_id, item in sorted(services.items()):
        state = str(item.get("state") or "review").upper()
        release_state = str(item.get("release_state") or "NO_SNAPSHOT").upper()
        domains = int(item.get("domain_count") or 0)
        row = (service_id, state, release_state, domains)
        if state == "BLOCKED" or release_state == "BLOCKED":
            blocked.append(row)
        if domains == 0:
            zero_domains.append(row)

    def render_rows(rows: list[tuple[str, str, str, int]]) -> list[str]:
        if not rows:
            return ["| — | — | — | — |"]
        return [
            f"| {service} | {state} | {release} | {domains} |"
            for service, state, release, domains in rows
        ]

    lines = [
        "# Source 阻塞看板（自动生成）",
        "",
        f"> generated_at: `{stamp}`",
        "",
        "权威：`config/source_canary_state.yaml` + `reports/generated/lifecycle.json`。",
        "",
        "## BLOCKED",
        "",
        "| Service | Lifecycle | Release | Domains |",
        "|---|---|---|---:|",
        *render_rows(blocked),
        "",
        "## domains = 0",
        "",
        "| Service | Lifecycle | Release | Domains |",
        "|---|---|---|---:|",
        *render_rows(zero_domains),
        "",
        "## 处理原则",
        "",
        "1. 禁止用空结果覆盖 Last Known Good。",
        "2. BLOCKED / domains=0 必须先修 adapter 或明确策略，再谈晋升。",
        "3. Collection Source health 与本表交叉核对。",
        "",
    ]
    return "\n".join(lines)


def write_status() -> dict[str, Any]:
    report = build_status_report()
    readme = Path("README.md")
    text = readme.read_text(encoding="utf-8")
    block = _render(report)
    if START in text and END in text:
        before = text.split(START, 1)[0].rstrip()
        after = text.split(END, 1)[1].lstrip()
        text = before + "\n\n" + block + "\n" + after
    else:
        text = text.rstrip() + "\n\n" + block + "\n"
    readme.write_text(text, encoding="utf-8")

    Path("reports/generated").mkdir(parents=True, exist_ok=True)
    (Path("reports/generated") / "lifecycle.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    qualification = qualify_all()
    derived = {
        "schema": "phase2_service_completion_derived_v1",
        "source_of_truth": "config/source_canary_state.yaml",
        "services": qualification["services"],
        "state_drift": qualification["state_drift"],
    }
    (Path("reports/generated") / "phase2_service_completion.json").write_text(
        json.dumps(derived, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    blocked_board = Path("docs/BLOCKED_BOARD.md")
    blocked_board.parent.mkdir(parents=True, exist_ok=True)
    blocked_board.write_text(_render_blocked_board(report), encoding="utf-8")
    return report
