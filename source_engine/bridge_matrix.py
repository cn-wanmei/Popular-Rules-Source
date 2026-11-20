from __future__ import annotations

import json
import os
import re
import subprocess
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

import yaml


WAVE_CONFIG = Path("config/p1_p2_self_built_official_wave.yaml")
POLICY_CONFIG = Path("config/durable_release_policy.yaml")
ZERO_SHA = "0" * 40
DEFAULT_ALIASES = {"default", "batch", "all-batch", "all"}


def _deduplicate(values: Sequence[str]) -> list[str]:
    ordered: list[str] = []
    seen: set[str] = set()
    for value in values:
        service_id = str(value).strip()
        if service_id and service_id not in seen:
            seen.add(service_id)
            ordered.append(service_id)
    return ordered


def parse_wave_services(document_text: str, *, source: str = "P1/P2 wave") -> dict[str, Any]:
    document = yaml.safe_load(document_text) or {}
    services = document.get("services") if isinstance(document, dict) else None
    if not isinstance(services, dict):
        raise ValueError(f"{source} must contain a services mapping")
    return {str(service_id): value for service_id, value in services.items()}


def changed_service_ids(
    previous_services: Mapping[str, Any],
    current_services: Mapping[str, Any],
) -> list[str]:
    """Return changed service IDs that still exist in the current P1/P2 wave.

    The current wave's insertion order is retained for deterministic matrix output.
    Removed-only changes fail closed rather than silently falling back to the
    default processing batch.
    """
    sentinel = object()
    changed = {
        service_id
        for service_id in set(previous_services) | set(current_services)
        if previous_services.get(service_id, sentinel) != current_services.get(service_id, sentinel)
    }
    selected = [service_id for service_id in current_services if service_id in changed]
    if changed and not selected:
        raise ValueError(
            "P1/P2 wave changed, but no changed service remains in the current wave; "
            "refusing to fall back to the default processing batch"
        )
    return selected


def resolve_service_matrix(
    *,
    services_input: str,
    event_name: str,
    before_sha: str,
    previous_services: Mapping[str, Any] | None,
    current_services: Mapping[str, Any],
    default_batch: Sequence[str],
) -> tuple[list[str], str]:
    default_services = _deduplicate(default_batch)
    if not default_services:
        raise ValueError("default_processing_batch missing or empty in durable_release_policy.yaml")

    raw = (services_input or "").strip()
    if raw:
        if raw.lower() in DEFAULT_ALIASES:
            return default_services, "default_processing_batch"
        explicit = _deduplicate(re.split(r"[,;\s]+", raw))
        if not explicit:
            raise ValueError("explicit services input produced an empty service matrix")
        return explicit, "selective"

    if event_name == "push" and before_sha and before_sha != ZERO_SHA:
        if previous_services is None:
            raise ValueError("previous P1/P2 service mapping is required for push-diff planning")
        changed = changed_service_ids(previous_services, current_services)
        if changed:
            return changed, "push_changed_p1_p2_services"

    return default_services, "default_processing_batch"


def _load_yaml_mapping(path: Path, *, key: str | None = None) -> dict[str, Any]:
    if not path.is_file():
        raise ValueError(f"required configuration file is missing: {path}")
    document = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    value = document.get(key) if key else document
    if not isinstance(value, dict):
        label = f" field {key!r}" if key else ""
        raise ValueError(f"configuration{label} in {path} must be a mapping")
    return value


def _load_previous_wave(before_sha: str) -> dict[str, Any]:
    result = subprocess.run(
        ["git", "show", f"{before_sha}:{WAVE_CONFIG.as_posix()}"],
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(
            "cannot read the previous P1/P2 wave from push base commit "
            f"{before_sha}: {result.stderr.strip()}"
        )
    return parse_wave_services(result.stdout, source=f"{before_sha}:{WAVE_CONFIG.as_posix()}")


def main() -> int:
    current_services = parse_wave_services(
        WAVE_CONFIG.read_text(encoding="utf-8"),
        source=str(WAVE_CONFIG),
    )
    policy = _load_yaml_mapping(POLICY_CONFIG)
    default_batch = policy.get("default_processing_batch")
    if not isinstance(default_batch, list):
        raise ValueError("default_processing_batch must be a list in durable_release_policy.yaml")

    event_name = os.environ.get("BRIDGE_EVENT_NAME", "")
    before_sha = os.environ.get("BRIDGE_EVENT_BEFORE", "")
    services_input = os.environ.get("SERVICES_INPUT", "")

    previous_services: dict[str, Any] | None = None
    if event_name == "push" and before_sha and before_sha != ZERO_SHA and not services_input.strip():
        previous_services = _load_previous_wave(before_sha)

    services, mode = resolve_service_matrix(
        services_input=services_input,
        event_name=event_name,
        before_sha=before_sha,
        previous_services=previous_services,
        current_services=current_services,
        default_batch=default_batch,
    )

    matrix = {"service": services}
    output_path = os.environ.get("GITHUB_OUTPUT")
    if not output_path:
        raise ValueError("GITHUB_OUTPUT is required when running inside GitHub Actions")
    with Path(output_path).open("a", encoding="utf-8") as output:
        output.write(f"matrix={json.dumps(matrix, separators=(',', ':'))}\n")
        output.write(f"service_count={len(services)}\n")
        output.write(f"planned_services={json.dumps(services, separators=(',', ':'))}\n")

    print(json.dumps({"mode": mode, "count": len(services), "services": services}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
