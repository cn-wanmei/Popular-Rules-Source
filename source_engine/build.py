from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

import yaml

from .diff import domain_diff
from .extract import extract_domains
from .fetch import FetchError, fetch
from .normalize import normalize_domain, service_asset_id
from .overrides import apply_overrides, load_service_overrides
from .policy import assess_count_change, is_excluded, load_exclusion_suffixes
from .tombstone import filter_revoked

PARSER_VERSION = "domain-extractor-v2"
GENERATOR_VERSION = "1.1.0"


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
    for manifest in root.glob("*/manifest.json"):
        try:
            data = json.loads(manifest.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue
        if data.get("service_id") != service_id:
            continue
        if data.get("release_state") not in {"CANDIDATE", "PUBLISHED"}:
            continue
        path = manifest.parent / "domains.txt"
        if path.exists():
            candidates.append((data.get("created_at", ""), path))
    if not candidates:
        return []
    _, path = sorted(candidates)[-1]
    return [x.strip() for x in path.read_text(encoding="utf-8").splitlines() if x.strip()]


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
        raw_path = raw_dir / f"{idx:03d}-{result.sha256[:12]}.bin"
        raw_path.write_bytes(result.body)

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
        for domain in extracted:
            domains.add(domain)
            domain_evidence.setdefault(domain, set()).add(evidence_id)

    seed_values = [normalize_domain(x) for x in cfg.get("seed_domains", [])]
    seed_domains = sorted({x for x in seed_values if x})
    if seed_domains:
        seed_evidence_id = f"EV-{service_id}-SEED"
        evidence_items.append({
            "evidence_id": seed_evidence_id,
            "service_id": service_id,
            "source_url": cfg.get("official_sources", [""])[0],
            "source_method": "official_seed",
            "retrieved_at": datetime.now(timezone.utc).isoformat(),
            "content_hash": hashlib.sha256("\n".join(seed_domains).encode()).hexdigest(),
            "parser_version": PARSER_VERSION,
            "confidence": "high",
            "status": "verified",
            "domains_extracted": len(seed_domains),
        })
        for domain in seed_domains:
            domains.add(domain)
            domain_evidence.setdefault(domain, set()).add(seed_evidence_id)

    blocked_suffixes = load_exclusion_suffixes()
    domains = {d for d in domains if not is_excluded(d, blocked_suffixes)}
    domains = filter_revoked(service_id, domains)
    domains = apply_overrides(domains, load_service_overrides(service_id))
    sorted_domains = sorted(domains)
    previous = latest_domains(service_id)
    # last-known-good retained by latest_domains when new build is blocked
    diff = domain_diff(previous, sorted_domains)
    used_last_known_good = False
    if errors and not sorted_domains and previous:
        # Fetch failures must not replace last-known-good with empty list
        sorted_domains = list(previous)
        used_last_known_good = True
        diff = domain_diff(previous, sorted_domains)
    assessment = assess_count_change(
        len(previous),
        len(sorted_domains),
        float(validation["thresholds"]["max_removal_ratio"]),
        float(validation["thresholds"]["max_growth_ratio_without_review"]),
    )

    now = datetime.now(timezone.utc)
    fingerprint = hashlib.sha256("\n".join(sorted_domains).encode()).hexdigest()[:16]
    snapshot_id = f"snap-{now.strftime('%Y%m%dT%H%M%SZ')}-{service_id}-{fingerprint}"

    assets = [
        {
            "asset_id": service_asset_id(service_id, domain),
            "service_id": service_id,
            "type": "domain",
            "value": domain,
            "classification": "service",
            "evidence_ids": sorted(domain_evidence.get(domain, [])),
        }
        for domain in sorted_domains
    ]

    domains_text = "\n".join(sorted_domains) + ("\n" if sorted_domains else "")
    generated_dir = Path("generated/source") / service_id
    generated_dir.mkdir(parents=True, exist_ok=True)
    (generated_dir / "domains.txt").write_text(domains_text, encoding="utf-8")
    (generated_dir / "provenance.json").write_text(
        json.dumps({"service_id": service_id, "assets": assets}, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    manifest = {
        "schema": "source_snapshot_v1",
        "snapshot_id": snapshot_id,
        "service_id": service_id,
        "created_at": now.isoformat(),
        "parser_version": PARSER_VERSION,
        "generator_version": GENERATOR_VERSION,
        "source_count": len(cfg.get("official_sources", [])),
        "domain_count": len(sorted_domains),
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
        "release_state": (
            "BLOCKED" if assessment.status == "BLOCK_EMPTY" and not used_last_known_good
            else "REVIEW" if used_last_known_good or errors or assessment.status != "OK"
            else "CANDIDATE"
        ),
        "last_known_good": used_last_known_good,
    }

    snapshot_dir = Path("snapshots") / snapshot_id
    snapshot_dir.mkdir(parents=True, exist_ok=True)

    # Snapshot identity is content-addressed. Once created, it is never overwritten.
    existing_manifest = snapshot_dir / "manifest.json"
    if existing_manifest.exists():
        return json.loads(existing_manifest.read_text(encoding="utf-8"))

    (snapshot_dir / "domains.txt").write_text(domains_text, encoding="utf-8")
    (snapshot_dir / "provenance.json").write_text(
        json.dumps({"service_id": service_id, "assets": assets}, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (snapshot_dir / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    checksums = {
        name: hashlib.sha256((snapshot_dir / name).read_bytes()).hexdigest()
        for name in ("domains.txt", "provenance.json", "manifest.json")
    }
    (snapshot_dir / "checksums.json").write_text(
        json.dumps(checksums, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return manifest


def build_all(config_path: str = "config/services.yaml") -> list[dict]:
    services = load_services(config_path)["services"]
    return [build_service(service_id, config_path) for service_id in sorted(services)]
