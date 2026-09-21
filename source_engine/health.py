"""Source health tracking with the same retry contract used by Build."""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from .build import load_services, load_yaml
from .fetch import FetchError, fetch

HEALTH_PATH = Path("reports/source-health.json")


def load_health() -> dict:
    if HEALTH_PATH.exists():
        return json.loads(HEALTH_PATH.read_text(encoding="utf-8"))
    return {"schema": "source_health_v2", "sources": {}}


def probe_all() -> dict:
    services = load_services()["services"]
    policy = load_yaml("config/source_adapters.yaml")["adapters"]["official_web"]
    health = load_health()
    now = datetime.now(timezone.utc).isoformat()

    for service_id, cfg in services.items():
        for url in cfg.get("official_sources", []):
            key = f"{service_id}|{url}"
            entry = health["sources"].setdefault(
                key, {"service_id": service_id, "url": url, "consecutive_failures": 0}
            )
            try:
                result = fetch(
                    url,
                    timeout=int(policy["timeout_seconds"]) if "timeout_seconds" in policy else 45,
                    max_bytes=min(int(policy.get("max_bytes", 5_000_000)), 500_000),
                    user_agent=str(policy.get("user_agent", "Popular-Rules-Source/3.x")),
                    retry_attempts=int(policy.get("retry_attempts", 2)),
                    retry_backoff_seconds=float(policy.get("retry_backoff_seconds", 2)),
                )
                entry.update({
                    "status": "healthy",
                    "last_success": now,
                    "last_http_status": result.status_code,
                    "content_hash": result.sha256,
                    "consecutive_failures": 0,
                })
            except FetchError as exc:
                failures = int(entry.get("consecutive_failures", 0)) + 1
                entry.update({
                    "status": "degraded" if failures < 3 else "blocked",
                    "last_failure": now,
                    "last_error": str(exc)[:500],
                    "consecutive_failures": failures,
                })

    health["updated_at"] = now
    HEALTH_PATH.parent.mkdir(exist_ok=True)
    HEALTH_PATH.write_text(
        json.dumps(health, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return health
