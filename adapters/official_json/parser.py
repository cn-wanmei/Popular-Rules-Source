"""Parse official JSON endpoint payloads into domain candidates."""
from __future__ import annotations

import json
from typing import Any

from source_engine.normalize import host_allowed, normalize_domain


def _walk(value: Any) -> list[str]:
    out: list[str] = []
    if isinstance(value, str):
        out.append(value)
    elif isinstance(value, dict):
        for v in value.values():
            out.extend(_walk(v))
    elif isinstance(value, list):
        for v in value:
            out.extend(_walk(v))
    return out


def extract_domains_from_official_json(
    body: bytes | str,
    exact: tuple[str, ...] = (),
    suffixes: tuple[str, ...] = (),
) -> list[str]:
    if isinstance(body, bytes):
        payload = json.loads(body.decode("utf-8"))
    else:
        payload = json.loads(body)
    candidates = _walk(payload)
    found: set[str] = set()
    for c in candidates:
        d = normalize_domain(c)
        if d and host_allowed(d, exact, suffixes):
            found.add(d)
    return sorted(found)
