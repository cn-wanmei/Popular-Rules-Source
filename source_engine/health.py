"""Source health tracking (persisted under reports/source-health.json)."""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .fetch import FetchError, fetch
from .build import load_services, load_yaml


HEALTH_PATH = Path("reports/source-health.json")


def load_health() -> dict[str, Any]:
    if HEALTH_PATH.exists():
        return json.loads(HEALTH_PATH.read_text(encoding="utf-8"))
    return {"schema": "source_health_v1", "sources": {}}


def probe_all() -> dict[str, Any]:
    services = load_services()["services"]
    adapter = load_yaml("config/source_adapters.yaml")["adapters"]["official_web"]
    health = load_health()
    sources = health.setdefault("sources", {})
    now = datetime.now(timezone.utc).isoformat()

    for sid, cfg in services.items():
        for url in cfg.get("official_sources", []):
            key = f"{sid}|{url}"
            entry = sources.get(key, {
                "service_id": sid,
                "url": url,
                "consecutive_failures": 0,
                "status": "unknown",
            })
            try:
                result = fetch(
                    url,
                    timeout=int(adapter["timeout_seconds"]),
                    max_bytes=min(int(adapter["max_bytes"]), 500_000),
                    user_agent=str(adapter["user_agent"]),
                )
                entry.update(
                    {
                        "status": "healthy",
                        "last_success": now,
                        "last_http_status": result.status_code,
                        "content_hash": result.sha256,
                        "consecutive_failures": 0,
                        "latency_note": "ok",
                    }
                )
            except FetchError as exc:
                fails = int(entry.get("consecutive_failures", 0)) + 1
                entry.update(
                    {
                        "status": "degraded" if fails < 3 else "blocked",
                        "last_failure": now,
                        "last_error": str(exc)[:300],
                        "consecutive_failures": fails,
                    }
                )
            sources[key] = entry

    health["updated_at"] = now
    HEALTH_PATH.parent.mkdir(exist_ok=True)
    HEALTH_PATH.write_text(
        json.dumps(health, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return health
