from __future__ import annotations

import json
import re
from html import unescape
from urllib.parse import urljoin, urlparse

from .normalize import host_allowed, normalize_domain

_URL_RE = re.compile(r"https?://[^\s\"'<>]+", re.I)
_HOSTLIKE_RE = re.compile(
    r"(?<![A-Za-z0-9_-])(?:[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?\.)+[A-Za-z]{2,63}(?![A-Za-z0-9_-])"
)
_HREF_RE = re.compile(r"""(?:href|src)\s*=\s*["']([^"']+)["']""", re.I)


def extract_domains_from_html(
    text: str,
    source_url: str,
    exact: tuple[str, ...],
    suffixes: tuple[str, ...],
) -> list[str]:
    candidates: set[str] = set()

    for raw_url in _URL_RE.findall(unescape(text)):
        parsed = urlparse(raw_url.rstrip(".,);"))
        if parsed.hostname:
            candidates.add(parsed.hostname)

    for href in _HREF_RE.findall(text):
        absolute = urljoin(source_url, href)
        parsed = urlparse(absolute)
        if parsed.hostname:
            candidates.add(parsed.hostname)

    candidates.update(_HOSTLIKE_RE.findall(unescape(text)))

    return sorted(
        d for raw in candidates
        if (d := normalize_domain(raw)) is not None
        and host_allowed(d, exact, suffixes)
    )


def _walk_json(value: object) -> list[str]:
    result: list[str] = []
    if isinstance(value, str):
        result.append(value)
    elif isinstance(value, list):
        for item in value:
            result.extend(_walk_json(item))
    elif isinstance(value, dict):
        for item in value.values():
            result.extend(_walk_json(item))
    return result


def extract_domains_from_json(
    body: bytes,
    exact: tuple[str, ...],
    suffixes: tuple[str, ...],
) -> list[str]:
    try:
        payload = json.loads(body.decode("utf-8", errors="strict"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        return []
    candidates = _walk_json(payload)
    return sorted({
        d for value in candidates
        if (d := normalize_domain(value)) is not None
        and host_allowed(d, exact, suffixes)
    })


def extract_domains(
    body: bytes,
    content_type: str,
    source_url: str,
    exact: tuple[str, ...],
    suffixes: tuple[str, ...],
) -> list[str]:
    if "json" in content_type.lower() or body.lstrip().startswith((b"{", b"[")):
        result = extract_domains_from_json(body, exact, suffixes)
        if result:
            return result
    return extract_domains_from_html(
        body.decode("utf-8", errors="replace"),
        source_url,
        exact,
        suffixes,
    )
