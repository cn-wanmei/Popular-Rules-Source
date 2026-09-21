from __future__ import annotations

from pathlib import Path
from urllib.parse import urlparse

import yaml

from .adapters import adapter_names_for, validate_adapter_contract
from .build import load_services
from .schema_validate import validate_all_snapshots


class ValidationError(RuntimeError):
    pass


def validate_config() -> list[str]:
    services = load_services()["services"]
    errors: list[str] = []

    lifecycle_path = Path("config/source_canary_state.yaml")
    if not lifecycle_path.exists():
        errors.append("missing lifecycle source of truth: config/source_canary_state.yaml")
    else:
        lifecycle = yaml.safe_load(lifecycle_path.read_text(encoding="utf-8")) or {}
        lifecycle_services = set((lifecycle.get("services") or {}).keys())
        if lifecycle_services != set(services):
            errors.append(
                "lifecycle/service mismatch: "
                f"missing={sorted(set(services)-lifecycle_services)}, "
                f"extra={sorted(lifecycle_services-set(services))}"
            )
        allowed = set(lifecycle.get("state_machine") or [])
        for service_id, item in (lifecycle.get("services") or {}).items():
            if str(item.get("state", "")) not in allowed:
                errors.append(f"{service_id}: invalid lifecycle state")

    for service_id, cfg in services.items():
        if not service_id.islower():
            errors.append(f"{service_id}: invalid service_id")
        sources = cfg.get("official_sources", [])
        if not sources:
            errors.append(f"{service_id}: no official_sources")
        for source_url in sources:
            parsed = urlparse(str(source_url))
            if parsed.scheme not in {"http", "https"} or not parsed.netloc:
                errors.append(f"{service_id}: invalid source URL {source_url}")
        if not cfg.get("allowed_host_exact") and not cfg.get("allowed_host_suffixes"):
            errors.append(f"{service_id}: no domain allow policy")
        if not adapter_names_for(service_id):
            errors.append(f"{service_id}: no source adapter configured")

    errors.extend(validate_adapter_contract())
    return errors


def validate_schemas_present() -> list[str]:
    required = [
        "schemas/service.schema.json",
        "schemas/source.schema.json",
        "schemas/asset.schema.json",
        "schemas/evidence.schema.json",
        "schemas/snapshot.schema.json",
        "schemas/release.schema.json",
        "schemas/exclusion.schema.json",
        "schemas/tombstone.schema.json",
        "schemas/discovery_candidate.schema.json",
    ]
    return [f"missing schema: {x}" for x in required if not Path(x).exists()]


def run_validation() -> None:
    errors = validate_config() + validate_schemas_present() + validate_all_snapshots()
    if errors:
        raise ValidationError("\n".join(errors))
    print(f"validation: PASS ({len(load_services()['services'])} services)")
