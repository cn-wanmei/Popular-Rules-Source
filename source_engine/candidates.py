from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import jsonschema

from .normalize import normalize_domain

ROOT = Path("authoring/candidates")
SCHEMA = Path("schemas/discovery_candidate.schema.json")


def _load_schema() -> dict[str, Any]:
    return json.loads(SCHEMA.read_text(encoding="utf-8"))


def load_candidates(service_id: str | None = None) -> list[dict[str, Any]]:
    if not ROOT.exists():
        return []
    paths = [ROOT / (str(service_id) + ".jsonl")] if service_id else sorted(ROOT.glob("*.jsonl"))
    rows: list[dict[str, Any]] = []
    for path in paths:
        if not path.exists():
            continue
        for line_no, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
            if not raw.strip():
                continue
            item = json.loads(raw)
            item["_path"] = str(path)
            item["_line"] = line_no
            rows.append(item)
    return rows


def audit_candidates(service_id: str | None = None) -> dict[str, Any]:
    schema = _load_schema()
    errors: list[str] = []
    rows = load_candidates(service_id)
    for item in rows:
        label = str(item.get("_path")) + ":" + str(item.get("_line"))
        try:
            jsonschema.validate(item, schema)
        except jsonschema.ValidationError as exc:
            errors.append(label + ": " + exc.message)
            continue
        if item.get("asset_type") == "domain" and not normalize_domain(str(item.get("value", ""))):
            errors.append(label + ": invalid domain")
        if item.get("status") == "promoted" and not (item.get("evidence_ids") or []):
            errors.append(label + ": promoted candidate requires evidence_ids")
    return {
        "schema": "candidate_audit_v1",
        "service_id": service_id,
        "candidate_count": len(rows),
        "errors": errors,
        "pass": not errors,
    }
