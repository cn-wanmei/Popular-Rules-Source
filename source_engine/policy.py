from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ChangeAssessment:
    previous_count: int
    current_count: int
    removal_ratio: float
    growth_ratio: float
    status: str


def assess_count_change(previous_count: int, current_count: int, max_removal_ratio: float, max_growth_ratio: float) -> ChangeAssessment:
    if previous_count <= 0:
        return ChangeAssessment(previous_count, current_count, 0.0, 0.0, 'OK')
    removal_ratio = max(0.0, (previous_count - current_count) / previous_count)
    growth_ratio = current_count / previous_count
    if current_count == 0:
        return ChangeAssessment(previous_count, current_count, 1.0, growth_ratio, 'BLOCK_EMPTY')
    if removal_ratio > max_removal_ratio:
        return ChangeAssessment(previous_count, current_count, removal_ratio, growth_ratio, 'REVIEW_REMOVAL')
    if growth_ratio > max_growth_ratio:
        return ChangeAssessment(previous_count, current_count, removal_ratio, growth_ratio, 'REVIEW_GROWTH')
    return ChangeAssessment(previous_count, current_count, removal_ratio, growth_ratio, 'OK')
