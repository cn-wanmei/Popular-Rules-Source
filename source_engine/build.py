from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

import yaml

from .diff import domain_diff
from .extract import extract_domains
from .fetch import FetchError, fetch
from .normalize import host_allowed, normalize_domain, service_asset_id
from .overrides import apply_overrides, load_service_overrides
from .policy import assess_count_change, is_excluded, load_exclusion_suffixes
from .tombstone import filter_revoked

PARSER_VERSION = "domain-extractor-v3"
GENERATOR_VERSION = "2.0.0"


def load_yaml(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as fh:
        return yaml.safe_load(fh) or {}


def load_services(path: str = "config/services.yaml") -> dict:
    return load_yaml(path)


def latest_domains(service_id: str) -> list[str]:
    root = Path("snapshots")
    if not root.exists():
        return []
    candidates: list[tuple[str, Path]] = []
    for manifest_path in root.glob("*/manifest.json"):
        try:
            data = json.loads(manifest_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        if data.get("schema") != "source_snapshot_v2":
            continue
        if data.get("service_id") != service_id:
            continue
        if data.get("release_state") not in {"CANDIDATE", "PUBLISHED"}:
            continue
        domains_path = manifest_path.parent / "domains.txt"
        if domains_path.exists():
            candidates.append((data.get("created_at", ""), domains_path))
    if not candidates:
        return []
    _, path = sorted(candidates)[-1]
    return [x.strip() for x in path.read_text(encoding="utf-8").splitlines() if x.strip()]


def _service_config_digest(cfg: dict) -> str:
    payload = json.dumps(cfg, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def build_service(service_id: str, config_path: str = "config/services.yaml") -> dict:
    services = load_services(config_path)["services"]
    if service_id not in services:
        raise KeyError(f"unknown service: {service_id}")

    cfg = services[service_id]
    adapter_policy = load_yaml("config/source_adapters.yaml")["adapters"]["official_web"]
    validation = load_yaml("config/validation.yaml")
    exact = tuple(cfg.get("allowed_host_exact", []))
    suffixes = tuple(cfg.get("allowed_host_suffixes", []))

    domains: set[str] = set()
    domain_evidence: dict[str, set[str]] = {}
    evidence_items: list[dict] = []
    errors: list[str] = []
    official_extracted = 0

    for idx, source_url in enumerate(cfg.get("official_sources", []), start=1):
        try:
            result = fetch(
                source_url,
                timeout=int(adapter_policy["timeout_seconds"]),
                max_bytes=int(adapter_policy["max_bytes"]),
                user_agent=str(adapter_policy["user_agent"]),
            )
        except FetchError as exc:
            errors.append(str(exc))
            continue

        raw_dir = Path("raw") / result.retrieved_at[:10] / service_id
        raw_dir.mkdir(parents=True, exist_ok=True)
        (raw_dir / f"{idx:03d}-{result.sha256[:12]}.bin").write_bytes(result.body)

        extracted = extract_domains(
            result.body,
            result.content_type,
            result.url,
            exact,
            suffixes,
        )
        evidence_id = f"EV-{service_id}-{idx:03d}-{result.sha256[:12]}"
        evidence_items.append({
            "evidence_id": evidence_id,
            "service_id": service_id,
            "source_url": source_url,
            "resolved_url": result.url,
            "source_method": "official_web",
            "retrieved_at": result.retrieved_at,
            "content_hash": result.sha256,
            "parser_version": PARSER_VERSION,
            "confidence": "high",
            "status": "verified",
            "domains_extracted": len(extracted),
        })
        official_extracted += len(extracted)
        for domain in extracted:
            domains.add(domain)
            domain_evidence.setdefault(domain, set()).add(evidence_id)

    blocked_suffixes = load_exclusion_suffixes()
    domains = {
        d for d in domains
        if host_allowed(d, exact, suffixes)
        and not is_excluded(d, blocked_suffixes)
    }
    revoked = domains - filter_revoked(service_id, domains)
    domains = filter_revoked(service_id, domains)

    overrides = load_service_overrides(service_id)
    for item in overrides:
        raw_domain = str(item.get("asset", ""))
        domain = normalize_domain(raw_domain)
        if domain and str(item.get("action", "")).lower() == "include":
            evidence = item.get("evidence_ids") or item.get("evidence") or []
            if isinstance(evidence, str):
                evidence = [evidence]
            domain_evidence.setdefault(domain, set()).update(map(str, evidence))
    domains = apply_overrides(
        domains,
        overrides,
        exact=exact,
        suffixes=suffixes,
        blocked_suffixes=blocked_suffixes,
        revoked=revoked,
    )
    sorted_domains = sorted(domains)

    previous = latest_domains(service_id)
    diff = domain_diff(previous, sorted_domains)
    used_last_known_good = False
    if errors and not sorted_domains and previous:
        sorted_domains = list(previous)
        diff = domain_diff(previous, sorted_domains)
        used_last_known_good = True

    assessment = assess_count_change(
        len(previous),
        len(sorted_domains),
        float(validation["thresholds"]["max_removal_ratio"]),
        float(validation["thresholds"]["max_growth_ratio_without_review"]),
    )

    evidence_map = {
        item["evidence_id"]: item
        for item in evidence_items
    }
    unverified_domains = [
        domain for domain in sorted_domains
        if not any(
            evidence_map.get(eid, {}).get("source_method") == "official_web"
            for eid in domain_evidence.get(domain, set())
        )
    ]

    service_digest = _service_config_digest(cfg)

    snapshot_content = {
        "schema": "source_snapshot_content_v1",
        "service_id": service_id,
        "domains": sorted_domains,
        "official_source_hashes": sorted(
            item["content_hash"]
            for item in evidence_items
            if item["source_method"] == "official_web"
        ),
        "parser_version": PARSER_VERSION,
        "generator_version": GENERATOR_VERSION,
        "service_config_digest": service_digest,
        "unverified_candidate_domains": unverified_domains,
    }
    snapshot_content_bytes = json.dumps(
        snapshot_content,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    content_digest = hashlib.sha256(snapshot_content_bytes).hexdigest()

    snapshot_id = f"snap-{service_id}-{content_digest[:24]}"
    created_at = datetime.now(timezone.utc).isoformat()

    assets = [
        {
            "asset_id": service_asset_id(service_id, domain),
            "service_id": service_id,
            "type": "domain",
            "value": domain,
            "classification": "service" if domain not in unverified_domains else "candidate",
            "evidence_ids": sorted(domain_evidence.get(domain, set())),
        }
        for domain in sorted_domains
    ]

    domains_text = "\n".join(sorted_domains) + ("\n" if sorted_domains else "")
    generated_dir = Path("generated/source") / service_id
    generated_dir.mkdir(parents=True, exist_ok=True)
    (generated_dir / "domains.txt").write_text(domains_text, encoding="utf-8")
    (generated_dir / "provenance.json").write_text(
        json.dumps(
            {
                "schema": "source_provenance_v2",
                "service_id": service_id,
                "snapshot_id": snapshot_id,
                "content_digest": content_digest,
                "official_extracted": official_extracted,
                "unverified_candidate_count": len(unverified_domains),
                "assets": assets,
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        ) + "\n",
        encoding="utf-8",
    )

    release_state = "CANDIDATE"
    release_reasons: list[str] = []
    if errors:
        release_state = "REVIEW"
        release_reasons.append("source_fetch_degraded")
    if unverified_domains:
        release_state = "REVIEW"
        release_reasons.append("contains_unverified_candidate_asset")
    if used_last_known_good:
        release_state = "REVIEW"
        release_reasons.append("last_known_good_retained")
    if assessment.status != "OK":
        release_state = "REVIEW"
        release_reasons.append(f"count_change:{assessment.status}")
    if not sorted_domains:
        release_state = "BLOCKED"
        release_reasons.append("empty_domain_output")

    manifest = {
        "schema": "source_snapshot_v2",
        "snapshot_id": snapshot_id,
        "content_digest": content_digest,
        "service_id": service_id,
        "created_at": created_at,
        "parser_version": PARSER_VERSION,
        "generator_version": GENERATOR_VERSION,
        "service_config_digest": service_digest,
        "source_count": len(cfg.get("official_sources", [])),
        "snapshot_content_sha256": content_digest,
        "domain_count": len(sorted_domains),
        "official_extracted": official_extracted,
        "unverified_candidate_count": len(unverified_domains),
        "unverified_candidate_domains": unverified_domains,
        "domains": sorted_domains,
        "assets": assets,
        "evidence": evidence_items,
        "previous_domain_count": len(previous),
        "change_assessment": {
            "status": assessment.status,
            "removal_ratio": assessment.removal_ratio,
            "growth_ratio": assessment.growth_ratio,
        },
        "domain_diff": diff,
        "errors": errors,
        "release_state": release_state,
        "release_reasons": release_reasons,
        "last_known_good": used_last_known_good,
    }

    snapshot_dir = Path("snapshots") / snapshot_id
    snapshot_dir.mkdir(parents=True, exist_ok=True)
    existing_manifest = snapshot_dir / "manifest.json"
    if existing_manifest.exists():
        return json.loads(existing_manifest.read_text(encoding="utf-8"))

    (snapshot_dir / "snapshot_content.json").write_bytes(
        json.dumps(
            snapshot_content,
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        ).encode("utf-8") + b"\n"
    )
    (snapshot_dir / "domains.txt").write_text(domains_text, encoding="utf-8")
    (snapshot_dir / "provenance.json").write_text(
        json.dumps(
            {"schema": "source_provenance_v2", "service_id": service_id, "assets": assets},
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        ) + "\n",
        encoding="utf-8",
    )
    (snapshot_dir / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    checksums = {
        name: hashlib.sha256((snapshot_dir / name).read_bytes()).hexdigest()
        for name in ("snapshot_content.json", "domains.txt", "provenance.json")
    }
    (snapshot_dir / "checksums.json").write_text(
        json.dumps(checksums, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return manifest


def build_all(config_path: str = "config/services.yaml") -> list[dict]:
    services = load_services(config_path)["services"]
    return [build_service(service_id, config_path) for service_id in sorted(services)]
