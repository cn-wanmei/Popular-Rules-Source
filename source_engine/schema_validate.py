"""Validate current snapshots while keeping historical snapshots out of the active contract."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import jsonschema


def _load_schema(name: str) -> dict[str, Any]:
    return json.loads(Path("schemas", name).read_text(encoding="utf-8"))


def validate_snapshot_dir(path: Path) -> list[str]:
    errors: list[str] = []
    manifest_path = path / "manifest.json"
    provenance_path = path / "provenance.json"

    if not manifest_path.exists():
        return [f"{path}: missing manifest.json"]
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [f"{path}: invalid manifest JSON: {exc}"]

    # v1 snapshots are immutable historical evidence. They are not active runtime
    # baselines and are intentionally excluded from the v2 production contract.
    if manifest.get("schema") == "source_snapshot_v1":
        return []

    try:
        jsonschema.validate(manifest, _load_schema("snapshot.schema.json"))
    except jsonschema.ValidationError as exc:
        errors.append(f"{path.name}: {exc.message}")

    evidence_ids = {
        item.get("evidence_id")
        for item in manifest.get("evidence", [])
        if isinstance(item, dict)
    }
    for asset in manifest.get("assets", []):
        for evidence_id in asset.get("evidence_ids", []):
            if evidence_id not in evidence_ids:
                errors.append(
                    f"{path.name}: asset {asset.get('asset_id')} references unknown evidence {evidence_id}"
                )

    if manifest.get("domain_count") != len(manifest.get("domains", [])):
        errors.append(f"{path.name}: domain_count does not match domains length")

    if provenance_path.exists():
        try:
            provenance = json.loads(provenance_path.read_text(encoding="utf-8"))
            if provenance.get("snapshot_id") not in {None, manifest.get("snapshot_id")}:
                errors.append(f"{path.name}: provenance snapshot_id mismatch")
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"{path.name}: invalid provenance JSON: {exc}")

    return errors


def validate_all_snapshots() -> list[str]:
    root = Path("snapshots")
    if not root.exists():
        return []
    errors: list[str] = []
    for path in sorted(root.iterdir()):
        if path.is_dir() and (path / "manifest.json").exists():
            errors.extend(validate_snapshot_dir(path))
    return errors


def validate_release_file(path: Path) -> list[str]:
    if not path.exists():
        return [f"{path}: missing"]
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        jsonschema.validate(data, _load_schema("release.schema.json"))
    except (OSError, json.JSONDecodeError, jsonschema.ValidationError) as exc:
        return [f"{path}: {exc}"]
    return []
