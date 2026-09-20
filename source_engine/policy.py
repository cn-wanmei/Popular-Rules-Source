from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import yaml


@dataclass(frozen=True)
class ChangeAssessment:
    previous_count: int
    current_count: int
    removal_ratio: float
    growth_ratio: float
    status: str


def assess_count_change(
    previous_count: int,
    current_count: int,
    max_removal_ratio: float,
    max_growth_ratio: float,
) -> ChangeAssessment:
    if previous_count <= 0:
        return ChangeAssessment(previous_count, current_count, 0.0, 0.0, "OK")
    removal_ratio = max(0.0, (previous_count - current_count) / previous_count)
    growth_ratio = current_count / previous_count
    if current_count == 0:
        return ChangeAssessment(previous_count, current_count, 1.0, growth_ratio, "BLOCK_EMPTY")
    if removal_ratio > max_removal_ratio:
        return ChangeAssessment(previous_count, current_count, removal_ratio, growth_ratio, "REVIEW_REMOVAL")
    if growth_ratio > max_growth_ratio:
        return ChangeAssessment(previous_count, current_count, removal_ratio, growth_ratio, "REVIEW_GROWTH")
    return ChangeAssessment(previous_count, current_count, removal_ratio, growth_ratio, "OK")


def load_exclusion_suffixes(paths: Iterable[str] | None = None) -> tuple[str, ...]:
    """Load blocked host suffixes from exclusion catalogs."""
    default_paths = [
        "exclusions/default.yaml",
        "exclusions/shared.yaml",
        "authoring/exclusions/shared.yaml",
        "authoring/exclusions/provider.yaml",
    ]
    use_paths = list(paths) if paths is not None else default_paths
    blocked: set[str] = set()
    for path in use_paths:
        p = Path(path)
        if not p.exists():
            continue
        data = yaml.safe_load(p.read_text(encoding="utf-8")) or {}
        global_cfg = data.get("global") or {}
        for s in global_cfg.get("blocked_suffixes") or []:
            blocked.add(str(s).lower().strip("."))
        for item in data.get("items") or []:
            asset = str(item.get("asset", "")).lower().strip(".")
            if asset and item.get("include", False) is False:
                blocked.add(asset)
    return tuple(sorted(blocked))


def is_excluded(domain: str, blocked_suffixes: tuple[str, ...]) -> bool:
    d = domain.lower().strip(".")
    for suffix in blocked_suffixes:
        if d == suffix or d.endswith("." + suffix):
            return True
    return False


_NOISE_LABELS = (
    "jstracker", "tracker", "beacon", "analytics", "utm", "log.", "logs.",
)


def is_noise_domain(domain: str) -> bool:
    d = domain.lower()
    return any(x in d for x in _NOISE_LABELS)
