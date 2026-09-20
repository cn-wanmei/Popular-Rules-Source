from __future__ import annotations

import hashlib
import ipaddress
import re
from urllib.parse import urlparse

_LABEL_RE = re.compile(r"^(?=.{1,63}$)[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?$")


def normalize_domain(value: str) -> str | None:
    value = value.strip().strip("[](){}<>,;\"'")
    if not value:
        return None
    if "://" in value:
        value = urlparse(value).hostname or ""
    value = value.strip().rstrip(".").lower()
    if value.startswith("*."):
        return None
    try:
        ipaddress.ip_address(value)
        return None
    except ValueError:
        pass
    if len(value) < 3 or len(value) > 253 or "." not in value:
        return None
    try:
        value = value.encode("idna").decode("ascii")
    except UnicodeError:
        return None
    if any(not _LABEL_RE.match(label) for label in value.split(".")):
        return None
    if value in {"example.com", "example.org", "example.net", "localhost"}:
        return None
    return value


def service_asset_id(service_id: str, domain: str) -> str:
    material = f"{service_id}\0domain\0{domain}".encode("utf-8")
    return "sha256:" + hashlib.sha256(material).hexdigest()


def host_allowed(domain: str, exact: tuple[str, ...], suffixes: tuple[str, ...]) -> bool:
    if domain in exact:
        return True
    return any(domain == suffix or domain.endswith("." + suffix) for suffix in suffixes)
