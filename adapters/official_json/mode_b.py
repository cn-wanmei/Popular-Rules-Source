"""Mode B: Official structured endpoint JSON → domain list."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from source_engine.normalize import host_allowed, normalize_domain


def parse_official_endpoint_list(
    body: bytes | str | dict[str, Any],
    exact: tuple[str, ...] = (),
    suffixes: tuple[str, ...] = (),
) -> list[str]:
    if isinstance(body, dict):
        payload = body
    elif isinstance(body, bytes):
        payload = json.loads(body.decode("utf-8"))
    else:
        payload = json.loads(body)

    hosts: list[str] = []
    endpoints = payload.get("endpoints") or payload.get("domains") or []
    if isinstance(endpoints, dict):
        endpoints = list(endpoints.values())
    for item in endpoints:
        if isinstance(item, str):
            hosts.append(item)
        elif isinstance(item, dict):
            for key in ("hostname", "host", "domain", "value", "url"):
                if key in item and item[key]:
                    hosts.append(str(item[key]))
                    break
    found: set[str] = set()
    for h in hosts:
        d = normalize_domain(h)
        if d is None:
            continue
        # apex: allow when suffix list contains the apex itself
        if exact and d in exact:
            found.add(d)
        elif suffixes and host_allowed(d, exact, suffixes):
            found.add(d)
        elif suffixes and d in suffixes:
            found.add(d)
        elif not exact and not suffixes:
            found.add(d)
    return sorted(found)


def load_fixture(service_id: str) -> list[str]:
    path = Path("tests/fixtures") / service_id / "mode_b" / "official_endpoints_v1.json"
    if not path.exists():
        return []
    cfg_suffixes = ()
    cfg_exact = ()
    # light load from services.yaml if present
    try:
        import yaml
        services = yaml.safe_load(Path("config/services.yaml").read_text())["services"]
        cfg = services.get(service_id, {})
        cfg_suffixes = tuple(cfg.get("allowed_host_suffixes") or [])
        cfg_exact = tuple(cfg.get("allowed_host_exact") or [])
    except Exception:
        pass
    return parse_official_endpoint_list(path.read_bytes(), cfg_exact, cfg_suffixes)
