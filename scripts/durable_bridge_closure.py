from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path


PROVENANCE_FIELDS = (
    "content_digest",
    "evidence_digest",
    "policy_digest",
    "generator_digest",
    "release_digest",
    "release_identity_version",
)


def materialize_durable_closure(root: Path, report: dict) -> None:
    """Rebuild every persisted generated domains file from its immutable snapshot.

    The bridge matrix refreshes only a subset of services. Historical seal records
    must nevertheless point at a persistence commit that contains a matching
    generated artifact for every retained immutable release.
    """
    errors: list[str] = []
    services = report.get("services") or {}
    if not isinstance(services, dict):
        raise RuntimeError("durable report services must be a mapping")

    for service, item in sorted(services.items()):
        if not isinstance(item, dict) or item.get("status") != "PERSISTED":
            continue
        snapshot_id = str(item.get("snapshot_id") or "")
        release_rel = str(item.get("release_path") or "")
        expected_release_path = f"releases/{service}/{snapshot_id}/release.json"
        if not snapshot_id or release_rel != expected_release_path:
            errors.append(f"{service}: unsafe or missing immutable release path")
            continue

        release_path = root / release_rel
        snapshot_root = root / "snapshots" / snapshot_id
        checksums_path = snapshot_root / "checksums.json"
        snapshot_domains = snapshot_root / "domains.txt"
        if not release_path.is_file() or not checksums_path.is_file() or not snapshot_domains.is_file():
            errors.append(f"{service}: immutable release/snapshot/checksum artifact missing")
            continue

        try:
            release = json.loads(release_path.read_text(encoding="utf-8"))
            checksums = json.loads(checksums_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"{service}: cannot parse immutable release/snapshot checksums: {exc}")
            continue

        expected = str(checksums.get("domains.txt") or "")
        release_checksums = release.get("checksums") or {}
        if not expected or expected != str(release_checksums.get("domains.txt") or ""):
            errors.append(f"{service}: snapshot/release domains checksum mismatch")
            continue
        actual = hashlib.sha256(snapshot_domains.read_bytes()).hexdigest()
        if actual != expected:
            errors.append(f"{service}: immutable snapshot domains checksum mismatch")
            continue
        if str(release.get("service_id")) != service or str(release.get("snapshot_id")) != snapshot_id:
            errors.append(f"{service}: release identity mismatch")
            continue
        mismatched = [
            field for field in PROVENANCE_FIELDS
            if str(release.get(field) or "") != str(item.get(field) or "")
        ]
        if mismatched:
            errors.append(f"{service}: release provenance mismatch: {', '.join(mismatched)}")
            continue

        generated_dir = root / "generated" / "source" / service
        generated_dir.mkdir(parents=True, exist_ok=True)
        generated_domains = generated_dir / "domains.txt"
        shutil.copy2(snapshot_domains, generated_domains)
        materialized_sha = hashlib.sha256(generated_domains.read_bytes()).hexdigest()
        if materialized_sha != expected:
            errors.append(f"{service}: materialized generated artifact checksum mismatch")
            continue
        item["expected_sha256"] = expected

    if errors:
        raise RuntimeError(
            "durable artifact closure failed for "
            f"{len(errors)} service(s):\n" + "\n".join(errors)
        )
    print(f"durable_artifact_closure=PASS services={sum(1 for x in services.values() if isinstance(x, dict) and x.get('status') == 'PERSISTED')}")
