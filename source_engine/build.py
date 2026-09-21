from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

from .adapters import adapter_names_for, extract_with_adapter
from .diff import domain_diff
from .normalize import host_allowed, normalize_domain, service_asset_id
from .overrides import apply_overrides, load_service_overrides
from .policy import assess_count_change, is_excluded, load_exclusion_suffixes
from .tombstone import filter_revoked
from .fetch import fetch, FetchError

PARSER_VERSION = "domain-extractor-v4"
GENERATOR_VERSION = "3.0.0"


def load_yaml(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as fh:
        import yaml
        return yaml.safe_load(fh) or {}


def load_services(path: str = "config/services.yaml") -> dict:
    return load_yaml(path)


def latest_domains(service_id: str) -> list[str]:
    candidates = []
    for manifest_path in Path("snapshots").glob("*/manifest.json"):
        try:
            data = json.loads(manifest_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        if data.get("schema") != "source_snapshot_v2" or data.get("service_id") != service_id:
            continue
        if data.get("release_state") not in {"CANDIDATE", "PUBLISHED"}:
            continue
        domains = manifest_path.parent / "domains.txt"
        if domains.exists():
            candidates.append((str(data.get("created_at", "")), domains))
    if not candidates:
        return []
    return [x.strip() for x in sorted(candidates)[-1][1].read_text(encoding="utf-8").splitlines() if x.strip()]


def _digest(value: object) -> str:
    raw = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def _file_digest(path: str) -> str:
    try:
        return hashlib.sha256(Path(path).read_bytes()).hexdigest()
    except OSError:
        return ""


def _generator_digest() -> str:
    return _digest({
        "version": Path("VERSION").read_text(encoding="utf-8").strip(),
        "parser_version": PARSER_VERSION,
        "generator_version": GENERATOR_VERSION,
        "build": _file_digest("source_engine/build.py"),
        "extract": _file_digest("source_engine/extract.py"),
        "adapters": _file_digest("source_engine/adapters.py"),
    })


def build_service(service_id: str, config_path: str = "config/services.yaml") -> dict:
    services = load_services(config_path)["services"]
    if service_id not in services:
        raise KeyError(f"unknown service: {service_id}")

    cfg = services[service_id]
    adapters_cfg = load_yaml("config/source_adapters.yaml")
    adapter_policy = adapters_cfg["runtime"]
    validation = load_yaml("config/validation.yaml")
    exact = tuple(cfg.get("allowed_host_exact", []))
    suffixes = tuple(cfg.get("allowed_host_suffixes", []))
    domains: set[str] = set()
    evidence_items: list[dict] = []
    domain_evidence: dict[str, set[str]] = {}
    errors: list[str] = []
    official_extracted = 0

    for idx, source_url in enumerate(cfg.get("official_sources", []), 1):
        used = None
        meta = None
        selected_domains: tuple[str, ...] = ()
        empty_success: tuple[str, dict] | None = None
        source_errors: list[str] = []
        for adapter_name in adapter_names_for(service_id):
            try:
                extraction = extract_with_adapter(
                    service_id=service_id,
                    adapter_name=adapter_name,
                    source_url=str(source_url),
                    exact=exact,
                    suffixes=suffixes,
                    adapter_policy=adapter_policy,
                )
                if extraction.domains:
                    selected_domains = extraction.domains
                    used = adapter_name
                    meta = extraction.evidence
                    break
                if empty_success is None:
                    empty_success = (adapter_name, extraction.evidence)
            except Exception as exc:
                source_errors.append(f"{adapter_name}: {exc}")
        if used is None and empty_success is not None:
            used, meta = empty_success
            selected_domains = ()
        if used is None:
            errors.append(f"{source_url}: " + " | ".join(source_errors or ["no adapter produced evidence"]))
            continue

        domains.update(selected_domains)
        domain_list = sorted(set(selected_domains))
        content_hash = str((meta or {}).get("content_hash") or _digest(meta or {}))
        evidence_id = f"EV-{service_id}-{idx:03d}-{content_hash[:12]}"
        evidence = {
            "evidence_id": evidence_id,
            "service_id": service_id,
            "source_url": source_url,
            "resolved_url": (meta or {}).get("resolved_url", source_url),
            "source_method": (meta or {}).get("source_method", used),
            "source_type": (meta or {}).get("source_type", used),
            "authority": "official",
            "retrieved_at": (meta or {}).get("retrieved_at", datetime.now(timezone.utc).isoformat()),
            "content_hash": content_hash,
            "parser_version": (meta or {}).get("parser_version", PARSER_VERSION),
            "confidence": "high",
            "strength": "S3",
            "status": "verified",
            "domains_extracted": len(domain_list),
        }
        evidence_items.append(evidence)
        official_extracted += len(domain_list)
        for domain in domain_list:
            domain_evidence.setdefault(domain, set()).add(evidence_id)

    blocked_suffixes = load_exclusion_suffixes()
    domains = {
        d for d in domains
        if host_allowed(d, exact, suffixes) and not is_excluded(d, blocked_suffixes)
    }
    revoked = set()
    before_revocation = set(domains)
    domains = filter_revoked(service_id, domains)
    revoked = before_revocation - domains

    overrides = load_service_overrides(service_id)
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
    last_known_good = False
    if errors and not sorted_domains and previous:
        sorted_domains = list(previous)
        diff = domain_diff(previous, sorted_domains)
        last_known_good = True

    assessment = assess_count_change(
        len(previous),
        len(sorted_domains),
        float(validation["thresholds"]["max_removal_ratio"]),
        float(validation["thresholds"]["max_growth_ratio_without_review"]),
    )

    unverified = [
        d for d in sorted_domains
        if not any(
            evidence.get("authority") == "official"
            and evidence.get("status") == "verified"
            for evidence in evidence_items
            if evidence["evidence_id"] in domain_evidence.get(d, set())
        )
    ]

    content_digest = _digest({
        "schema": "source_snapshot_content_v2",
        "service_id": service_id,
        "domains": sorted_domains,
        "official_source_hashes": sorted(x["content_hash"] for x in evidence_items),
    })
    evidence_identity = [
        {
            "evidence_id": item["evidence_id"],
            "service_id": item["service_id"],
            "source_url": item["source_url"],
            "resolved_url": item.get("resolved_url"),
            "source_method": item["source_method"],
            "source_type": item.get("source_type"),
            "authority": item["authority"],
            "content_hash": item["content_hash"],
            "parser_version": item["parser_version"],
            "confidence": item["confidence"],
            "strength": item["strength"],
            "status": item["status"],
            "domains_extracted": item.get("domains_extracted", 0),
        }
        for item in evidence_items
    ]
    evidence_digest = _digest({
        "service_id": service_id,
        "evidence": evidence_identity,
        "domain_evidence": {k: sorted(v) for k, v in sorted(domain_evidence.items())},
    })
    policy_digest = _digest({
        "allowed_host_exact": list(exact),
        "allowed_host_suffixes": list(suffixes),
        "blocked_suffixes": list(blocked_suffixes),
        "overrides": overrides,
        "revoked": sorted(revoked),
        "thresholds": validation.get("thresholds") or {},
    })
    generator_digest = _generator_digest()
    release_digest = _digest({
        "content_digest": content_digest,
        "evidence_digest": evidence_digest,
        "policy_digest": policy_digest,
        "generator_digest": generator_digest,
    })
    snapshot_id = f"snap-{service_id}-{release_digest[:24]}"

    release_state = "CANDIDATE"
    release_reasons: list[str] = []
    if errors:
        release_state = "REVIEW"
        release_reasons.append("source_fetch_degraded")
    if unverified:
        release_state = "REVIEW"
        release_reasons.append("contains_unverified_candidate_asset")
    if last_known_good:
        release_state = "REVIEW"
        release_reasons.append("last_known_good_retained")
    if assessment.status != "OK":
        release_state = "REVIEW"
        release_reasons.append(f"count_change:{assessment.status}")
    if not sorted_domains:
        release_state = "BLOCKED"
        release_reasons.append("empty_domain_output")

    assets = [{
        "asset_id": service_asset_id(service_id, d),
        "service_id": service_id,
        "type": "domain",
        "value": d,
        "classification": "service" if d not in unverified else "candidate",
        "evidence_ids": sorted(domain_evidence.get(d, set())),
    } for d in sorted_domains]

    manifest = {
        "schema": "source_snapshot_v2",
        "snapshot_id": snapshot_id,
        "content_digest": content_digest,
        "evidence_digest": evidence_digest,
        "policy_digest": policy_digest,
        "generator_digest": generator_digest,
        "release_digest": release_digest,
        "snapshot_content_sha256": content_digest,
        "service_id": service_id,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "parser_version": PARSER_VERSION,
        "generator_version": GENERATOR_VERSION,
        "service_config_digest": _digest(cfg),
        "source_count": len(cfg.get("official_sources", [])),
        "domain_count": len(sorted_domains),
        "official_extracted": official_extracted,
        "unverified_candidate_count": len(unverified),
        "unverified_candidate_domains": unverified,
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
        "last_known_good": last_known_good,
    }

    snapshot_dir = Path("snapshots") / snapshot_id
    if (snapshot_dir / "manifest.json").exists():
        return json.loads((snapshot_dir / "manifest.json").read_text(encoding="utf-8"))
    snapshot_dir.mkdir(parents=True, exist_ok=True)
    domains_text = "\n".join(sorted_domains) + ("\n" if sorted_domains else "")

    (snapshot_dir / "snapshot_content.json").write_text(
        json.dumps({
            "schema": "source_snapshot_content_v2",
            "service_id": service_id,
            "domains": sorted_domains,
            "official_source_hashes": sorted(x["content_hash"] for x in evidence_items),
            "content_digest": content_digest,
        }, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (snapshot_dir / "domains.txt").write_text(domains_text, encoding="utf-8")
    (snapshot_dir / "provenance.json").write_text(
        json.dumps({
            "schema": "source_provenance_v3",
            "service_id": service_id,
            "snapshot_id": snapshot_id,
            "content_digest": content_digest,
            "evidence_digest": evidence_digest,
            "policy_digest": policy_digest,
            "generator_digest": generator_digest,
            "release_digest": release_digest,
            "assets": assets,
            "evidence": evidence_items,
        }, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (snapshot_dir / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    checksums = {
        name: hashlib.sha256((snapshot_dir / name).read_bytes()).hexdigest()
        for name in ("snapshot_content.json", "domains.txt", "provenance.json", "manifest.json")
    }
    (snapshot_dir / "checksums.json").write_text(
        json.dumps(checksums, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    generated = Path("generated/source") / service_id
    generated.mkdir(parents=True, exist_ok=True)
    (generated / "domains.txt").write_text(domains_text, encoding="utf-8")
    (generated / "provenance.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return manifest


def build_all(config_path: str = "config/services.yaml") -> list[dict]:
    return [build_service(s, config_path) for s in sorted(load_services(config_path)["services"])]
