from __future__ import annotations

from pathlib import Path
from urllib.parse import urlparse

from .build import load_services
from .normalize import host_allowed
from .schema_validate import validate_all_snapshots


class ValidationError(RuntimeError):
    pass


def validate_config() -> list[str]:
    services = load_services()["services"]
    errors: list[str] = []
    for service_id, cfg in services.items():
        if service_id != service_id.lower() or not all(
            c.islower() or c.isdigit() or c == "-" for c in service_id
        ):
            errors.append(f"{service_id}: invalid service_id")

        sources = cfg.get("official_sources", [])
        if not sources:
            errors.append(f"{service_id}: no official_sources")
        for url in sources:
            parsed = urlparse(str(url))
            if parsed.scheme not in {"http", "https"} or not parsed.netloc:
                errors.append(f"{service_id}: invalid source URL {url}")

        exact = tuple(cfg.get("allowed_host_exact", []))
        suffixes = tuple(cfg.get("allowed_host_suffixes", []))
        if not exact and not suffixes:
            errors.append(f"{service_id}: no domain allow policy")

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
    return [f"missing schema: {path}" for path in required if not Path(path).exists()]


def run_validation() -> None:
    errors = validate_config() + validate_schemas_present() + validate_all_snapshots()
    if errors:
        raise ValidationError("\n".join(errors))
    print(f"validation: PASS ({len(load_services()['services'])} services)")
