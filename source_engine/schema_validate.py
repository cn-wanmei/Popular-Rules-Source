"""Validate snapshot/release artifacts against JSON schemas.

Uses jsonschema when available; falls back to required-field checks.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

try:
    import jsonschema
    HAS_JSONSCHEMA = True
except ImportError:  # pragma: no cover
    HAS_JSONSCHEMA = False


def _load_schema(name: str) -> dict[str, Any]:
    return json.loads(Path("schemas", name).read_text(encoding="utf-8"))


def _required_fields_check(data: dict[str, Any], schema: dict[str, Any], label: str) -> list[str]:
    errors: list[str] = []
    for key in schema.get("required") or []:
        if key not in data:
            errors.append(f"{label}: missing required field '{key}'")
    return errors


def validate_snapshot_dir(path: Path) -> list[str]:
    errors: list[str] = []
    manifest_path = path / "manifest.json"
    if not manifest_path.exists():
        return [f"{path}: missing manifest.json"]
    data = json.loads(manifest_path.read_text(encoding="utf-8"))
    schema = _load_schema("snapshot.schema.json")
    if HAS_JSONSCHEMA:
        try:
            jsonschema.validate(data, schema)
        except jsonschema.ValidationError as exc:
            errors.append(f"{path.name}: {exc.message}")
    else:
        errors.extend(_required_fields_check(data, schema, path.name))
        if data.get("schema") != "source_snapshot_v1" and "schema" in data:
            pass  # allow forward
    return errors


def validate_all_snapshots() -> list[str]:
    root = Path("snapshots")
    if not root.exists():
        return []
    errors: list[str] = []
    for d in sorted(root.iterdir()):
        if d.is_dir() and (d / "manifest.json").exists():
            errors.extend(validate_snapshot_dir(d))
    return errors
