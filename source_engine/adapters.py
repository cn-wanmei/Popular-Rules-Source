from __future__ import annotations

import importlib
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

import yaml

from .extract import extract_domains
from .fetch import fetch
from .normalize import host_allowed, normalize_domain


class AdapterContractError(RuntimeError):
    pass


@dataclass(frozen=True)
class AdapterExtraction:
    domains: tuple[str, ...]
    evidence: dict[str, Any]


def _config() -> dict[str, Any]:
    return yaml.safe_load(Path("config/source_adapters.yaml").read_text(encoding="utf-8")) or {}


def adapter_specs() -> dict[str, dict[str, Any]]:
    return dict(_config().get("adapters") or {})


def adapter_names_for(service_id: str) -> list[str]:
    item = ((_config().get("services") or {}).get(service_id)) or {}
    return list(item.get("adapters") or ["official_web"])


def _pointer(payload: Any, path: str) -> Any:
    if path in {"", "/"}:
        return payload
    value = payload
    for token in path.lstrip("/").split("/"):
        token = token.replace("~1", "/").replace("~0", "~")
        if isinstance(value, list):
            value = value[int(token)]
        else:
            value = value[token]
    return value


def _domains_from_values(values: list[Any], exact: tuple[str, ...], suffixes: tuple[str, ...]) -> list[str]:
    output: set[str] = set()
    for value in values:
        raw = value if isinstance(value, str) else json.dumps(value, ensure_ascii=False)
        tokens = re.findall(
            r"""https?://[^\s"'<>]+|(?:[A-Za-z0-9-]+\.)+[A-Za-z]{2,63}""",
            raw,
        )
        for token in tokens:
            domain = normalize_domain(token)
            if domain and host_allowed(domain, exact, suffixes):
                output.add(domain)
    return sorted(output)


def extract_with_adapter(
    *,
    service_id: str,
    adapter_name: str,
    source_url: str,
    exact: tuple[str, ...],
    suffixes: tuple[str, ...],
    adapter_policy: dict[str, Any],
) -> AdapterExtraction:
    spec = adapter_specs().get(adapter_name)
    if not spec or spec.get("enabled") is not True:
        raise AdapterContractError(f"adapter disabled or undefined: {adapter_name}")

    allowed_authorities = set(_config().get("contract", {}).get("authorities") or ["official"])
    authority = str(spec.get("authority") or "")
    if authority not in allowed_authorities:
        raise AdapterContractError(
            f"{adapter_name}: authority {authority!r} not in contract authorities"
        )

    common = {
        "source_method": adapter_name,
        "source_type": adapter_name,
        "authority": authority,
        "parser_version": str(spec.get("parser")),
        "confidence": "high",
        "strength": "S3" if authority == "official" else "S2",
        "status": "verified",
    }

    if adapter_name == "official_sdk":
        module_name = str(spec.get("module") or "")
        if not module_name:
            raise AdapterContractError("official_sdk requires module")
        module = importlib.import_module(module_name)
        values = getattr(module, str(spec.get("function") or "discover"))(service_id)
        return AdapterExtraction(
            tuple(_domains_from_values(list(values or []), exact, suffixes)),
            {**common, "source_url": source_url},
        )

    if adapter_name == "official_browser":
        try:
            from playwright.sync_api import sync_playwright
        except ImportError as exc:
            raise AdapterContractError("official_browser requires optional Playwright") from exc
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            network_urls: list[str] = []
            page.on("response", lambda response: network_urls.append(response.url))
            page.goto(source_url, wait_until="domcontentloaded", timeout=int(adapter_policy["timeout_seconds"]) * 1000)
            page.wait_for_timeout(int(spec.get("settle_ms", 1500)))
            html = page.content()
            browser.close()
        domains = set(_domains_from_values(network_urls, exact, suffixes))
        domains.update(extract_domains(html.encode("utf-8"), "text/html", source_url, exact, suffixes))
        return AdapterExtraction(
            tuple(sorted(domains)),
            {**common, "source_url": source_url, "rendered": True},
        )

    result = fetch(
        source_url,
        timeout=int(adapter_policy["timeout_seconds"]),
        max_bytes=int(adapter_policy["max_bytes"]),
        user_agent=str(adapter_policy["user_agent"]),
        retry_attempts=int(adapter_policy.get("retry_attempts", 1)),
        retry_backoff_seconds=float(adapter_policy.get("retry_backoff_seconds", 1)),
    )

    if adapter_name == "official_web":
        domains = extract_domains(result.body, result.content_type, result.url, exact, suffixes)
        source_host = normalize_domain(urlparse(result.url).hostname or "")
        if source_host and host_allowed(source_host, exact, suffixes):
            domains = sorted(set(domains) | {source_host})
    elif adapter_name == "upstream_rule":
        text = result.body.decode("utf-8", errors="replace")
        domains = _domains_from_values([text], exact, suffixes)
    elif adapter_name in {"official_json", "official_api", "official_manifest"}:
        payload = json.loads(result.body.decode("utf-8"))
        paths = list(spec.get("field_paths") or [])
        values = [_pointer(payload, path) for path in paths] if paths else [payload]
        domains = _domains_from_values(values, exact, suffixes)
    else:
        raise AdapterContractError(f"unsupported adapter: {adapter_name}")

    return AdapterExtraction(
        tuple(domains),
        {
            **common,
            "source_url": source_url,
            "resolved_url": result.url,
            "retrieved_at": result.retrieved_at,
            "content_hash": result.sha256,
            "domains_extracted": len(domains),
        },
    )


def validate_adapter_contract() -> list[str]:
    config = _config()
    required = set((config.get("contract") or {}).get("required_fields") or [])
    allowed_authorities = set((config.get("contract") or {}).get("authorities") or ["official"])
    errors: list[str] = []
    for name, spec in adapter_specs().items():
        missing = sorted(field for field in required if field not in spec)
        if missing:
            errors.append(f"{name}: missing contract fields: {missing}")
        if spec.get("authority") not in allowed_authorities:
            errors.append(
                f"{name}: authority {spec.get('authority')!r} not in {sorted(allowed_authorities)}"
            )
    for service_id, item in (config.get("services") or {}).items():
        for name in item.get("adapters") or []:
            if name not in adapter_specs():
                errors.append(f"{service_id}: unknown adapter {name}")
    return errors
