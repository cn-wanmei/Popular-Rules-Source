"""Domain list diff between previous and current materializations."""
from __future__ import annotations


def domain_diff(previous: list[str], current: list[str]) -> dict:
    prev = set(previous)
    curr = set(current)
    return {
        "added": sorted(curr - prev),
        "removed": sorted(prev - curr),
        "unchanged": sorted(prev & curr),
        "added_count": len(curr - prev),
        "removed_count": len(prev - curr),
        "unchanged_count": len(prev & curr),
        "previous_count": len(prev),
        "current_count": len(curr),
    }
