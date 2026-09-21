from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Iterable

import requests
import yaml

from .build import load_services
from .candidates import load_candidates
from .normalize import normalize_domain

DEFAULT_ROOT = "https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection"
DEFAULT_SERVICE_RULES = "data/generated/canonical/service_rules.jsonl"
DEFAULT_RULES = "data/generated/canonical/rules.jsonl"

class GapEngineError(RuntimeError):
    pass

def _cfg() -> dict[str, Any]:
    path = Path("config/gap.yaml")
    return yaml.safe_load(path.read_text(encoding="utf-8")) if path.exists() else {}

def _stream_jsonl(url: str, timeout: int, max_bytes: int) -> Iterable[dict[str, Any]]:
    total = 0
    with requests.get(url, timeout=timeout, headers={"User-Agent": "Popular-Rules-Source/3.x"}, stream=True) as response:
        response.raise_for_status()
        for raw in response.iter_lines(decode_unicode=False):
            if not raw:
                continue
            total += len(raw) + 1
            if total > max_bytes:
                raise GapEngineError(f"collection artifact exceeds max_bytes={max_bytes}")
            try:
                item = json.loads(raw.decode("utf-8"))
            except (UnicodeDecodeError, json.JSONDecodeError):
                continue
            if isinstance(item, dict):
                yield item

def _normalize_rule_domains(item: dict[str, Any]) -> set[str]:
    if str(item.get("type", "")).lower() not in {"domain", "host", "hostname"}:
        return set()
    raw = item.get("value")
    values = raw if isinstance(raw, list) else [raw]
    out: set[str] = set()
    for value in values:
        if isinstance(value, str):
            domain = normalize_domain(value)
            if domain:
                out.add(domain)
    return out

def collection_domains(service_id: str, collection_ref: str | None = None) -> dict[str, Any]:
    cfg = _cfg()
    root = collection_ref or os.getenv("COLLECTION_RAW_ROOT") or cfg.get("collection_raw_root") or DEFAULT_ROOT
    service_path = str(cfg.get("service_rules_path") or DEFAULT_SERVICE_RULES)
    rules_path = str(cfg.get("rules_path") or DEFAULT_RULES)
    timeout = int(cfg.get("timeout_seconds", 45))
    max_bytes = int(cfg.get("max_bytes", 80_000_000))

    wanted: set[str] = set()
    membership_count = 0
    for item in _stream_jsonl(f"{root.rstrip('/')}/{service_path.lstrip('/')}", timeout, max_bytes):
        service = str(item.get("service") or item.get("entity") or "")
        if service != service_id:
            continue
        rule_id = str(item.get("rule_id") or item.get("id") or "")
        if rule_id:
            wanted.add(rule_id)
            membership_count += 1

    domains: set[str] = set()
    matched_rules = 0
    if wanted:
        for item in _stream_jsonl(f"{root.rstrip('/')}/{rules_path.lstrip('/')}", timeout, max_bytes):
            rule_id = str(item.get("id") or item.get("rule_id") or "")
            if rule_id not in wanted:
                continue
            found = _normalize_rule_domains(item)
            if found:
                matched_rules += 1
                domains.update(found)

    return {
        "domains": sorted(domains),
        "membership_rule_count": membership_count,
        "matched_domain_rule_count": matched_rules,
        "membership_url": f"{root.rstrip('/')}/{service_path.lstrip('/')}",
        "rules_url": f"{root.rstrip('/')}/{rules_path.lstrip('/')}",
    }

def _latest_manifest(service_id: str) -> dict[str, Any] | None:
    latest = None
    for path in Path("snapshots").glob("*/manifest.json"):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        if data.get("schema") != "source_snapshot_v2" or data.get("service_id") != service_id:
            continue
        if latest is None or str(data.get("created_at", "")) > str(latest.get("created_at", "")):
            latest = data
    return latest

def _candidate_matches(service_id: str, missing: set[str]) -> list[dict[str, Any]]:
    out = []
    for item in load_candidates(service_id):
        domain = normalize_domain(str(item.get("value", "")))
        if domain and domain in missing:
            out.append({
                "domain": domain,
                "candidate_id": item.get("candidate_id"),
                "status": item.get("status"),
                "source_url": item.get("source_url"),
                "source_method": item.get("source_method"),
                "evidence_ids": item.get("evidence_ids") or [],
                "reason": item.get("reason"),
                "location": f"{item.get('_path')}:{item.get('_line')}",
            })
    return sorted(out, key=lambda x: (x["domain"], str(x.get("candidate_id") or "")))

def _evidence_for(manifest: dict[str, Any] | None, domains: set[str]) -> dict[str, Any]:
    evidence_by_id = {
        str(item["evidence_id"]): item
        for item in (manifest or {}).get("evidence") or []
        if isinstance(item, dict) and item.get("evidence_id")
    }
    mapping = {}
    uncovered = []
    for domain in sorted(domains):
        asset = next((a for a in (manifest or {}).get("assets") or [] if a.get("value") == domain), None)
        verified = [
            evidence_by_id[eid] for eid in (asset or {}).get("evidence_ids") or []
            if eid in evidence_by_id
            and evidence_by_id[eid].get("authority", "official") == "official"
            and evidence_by_id[eid].get("status", "verified") == "verified"
        ]
        mapping[domain] = [
            {
                "evidence_id": item.get("evidence_id"),
                "source_url": item.get("source_url"),
                "resolved_url": item.get("resolved_url"),
                "source_method": item.get("source_method"),
                "content_hash": item.get("content_hash"),
            }
            for item in verified
        ]
        if not verified:
            uncovered.append(domain)
    return {"complete_for_missing": not uncovered, "domain_evidence": mapping, "uncovered": uncovered}

def gap(service_id: str, *, collection_ref: str | None = None, target_domains: list[str] | None = None) -> dict[str, Any]:
    services = load_services()["services"]
    if service_id not in services:
        raise GapEngineError(f"unknown service: {service_id}")

    collection = collection_domains(service_id, collection_ref)
    manifest = _latest_manifest(service_id)
    collection_set = set(collection["domains"])
    source_set = set((manifest or {}).get("domains") or [])
    missing = source_set - collection_set
    unexpected = collection_set - source_set
    focus = missing
    if target_domains:
        focus |= {
            domain for raw in target_domains
            if (domain := normalize_domain(raw)) and domain not in collection_set
        }

    candidates = _candidate_matches(service_id, focus)
    evidence = _evidence_for(manifest, focus)
    blockers: set[str] = set()
    if manifest is None:
        blockers.add("no_snapshot")
    else:
        if manifest.get("release_state") not in {"CANDIDATE", "PUBLISHED"}:
            blockers.add(f"release_state:{manifest.get('release_state')}")
        if manifest.get("errors"):
            blockers.add("source_fetch_errors")
        if int(manifest.get("unverified_candidate_count", 0) or 0):
            blockers.add("unverified_candidates")
        if int(manifest.get("official_extracted", 0) or 0) == 0:
            blockers.add("no_official_extraction")
    if missing and not evidence["complete_for_missing"]:
        blockers.add("missing_official_evidence")
    if unexpected:
        blockers.add("collection_contains_domains_not_in_current_source")

    if missing:
        action = "official_evidence_required" if candidates else "discover_official_evidence"
    elif blockers:
        action = "resolve_release_blockers"
    elif manifest and manifest.get("release_state") == "CANDIDATE":
        action = "collection_promotion_pr"
    else:
        action = "no_action"

    result = {
        "schema": "source_gap_v3",
        "service": service_id,
        "collection_domains": sorted(collection_set),
        "source_domains": sorted(source_set),
        "missing": sorted(missing),
        "unexpected": sorted(unexpected),
        "candidate_matches": candidates,
        "official_sources": list(services[service_id].get("official_sources") or []),
        "latest_snapshot": None if manifest is None else {
            "snapshot_id": manifest.get("snapshot_id"),
            "content_digest": manifest.get("content_digest"),
            "evidence_digest": manifest.get("evidence_digest"),
            "policy_digest": manifest.get("policy_digest"),
            "generator_digest": manifest.get("generator_digest"),
            "release_digest": manifest.get("release_digest"),
            "release_state": manifest.get("release_state"),
        },
        "evidence": {**evidence, "target_domains": sorted(focus)},
        "release_blockers": sorted(blockers),
        "why_not_release": sorted(blockers),
        "recommended_action": action,
        "collection_sources": {
            "membership_rule_count": collection["membership_rule_count"],
            "matched_domain_rule_count": collection["matched_domain_rule_count"],
            "membership_url": collection["membership_url"],
            "rules_url": collection["rules_url"],
        },
    }
    Path("reports").mkdir(exist_ok=True)
    Path(f"reports/gap-{service_id}.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return result
