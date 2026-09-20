from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class SourceConfig:
    service_id: str
    source_url: str
    seed_domains: tuple[str, ...]
    allowed_exact: tuple[str, ...]
    allowed_suffixes: tuple[str, ...]
    timeout_seconds: int = 30
    max_bytes: int = 5_000_000
    user_agent: str = "Popular-Rules-Source/0.1"


@dataclass(frozen=True)
class Evidence:
    evidence_id: str
    service_id: str
    source_url: str
    source_method: str
    retrieved_at: str
    content_hash: str
    parser_version: str
    confidence: str = "high"
    notes: str = ""


@dataclass(frozen=True)
class GeneratedDomain:
    domain: str
    service_id: str
    asset_id: str
    evidence_id: str
    source_url: str
    source_method: str
    classification: str = "service"


@dataclass
class Snapshot:
    snapshot_id: str
    service_id: str
    created_at: str
    domains: list[str] = field(default_factory=list)
    evidence: list[dict[str, Any]] = field(default_factory=list)
    source_hashes: dict[str, str] = field(default_factory=dict)
