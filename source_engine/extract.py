from __future__ import annotations

import re
from html import unescape
from urllib.parse import urljoin, urlparse

from .normalize import normalize_domain, host_allowed

_URL_RE = re.compile(r"https?://[^\s\"'<>]+", re.I)
_HOSTLIKE_RE = re.compile(r"(?<![A-Za-z0-9_-])(?:[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?\.)+[A-Za-z]{2,63}(?![A-Za-z0-9_-])")
_HREF_RE = re.compile(r"""(?:href|src)\s*=\s*["']([^"']+)["']""", re.I)


def extract_domains(text: str, source_url: str, exact: tuple[str, ...], suffixes: tuple[str, ...]) -> list[str]:
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

    for host in _HOSTLIKE_RE.findall(unescape(text)):
        candidates.add(host)

    normalized = {
        d for raw in candidates
        if (d := normalize_domain(raw)) is not None
        and host_allowed(d, exact, suffixes)
    }
    return sorted(normalized)
