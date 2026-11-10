from __future__ import annotations

import pytest

from source_engine.overrides import apply_overrides
from source_engine.policy import is_excluded


GLOBAL_BLOCKED = ("cloudflare.com",)
EVIDENCE_URL = "https://developers.cloudflare.com/cloudflare-one/traffic-controls/global-policies/"


def test_exact_service_host_can_override_global_suffix_exclusion() -> None:
    domains = set()
    exact = ("api.cloudflare.com",)
    overrides = [{
        "asset": "api.cloudflare.com",
        "action": "include",
        "allow_global_exclusion": True,
        "reason": "official Cloudflare API endpoint",
        "evidence": EVIDENCE_URL,
    }]

    result = apply_overrides(
        domains,
        overrides,
        exact=exact,
        suffixes=(),
        blocked_suffixes=GLOBAL_BLOCKED,
    )

    assert result == {"api.cloudflare.com"}
    assert is_excluded("api.cloudflare.com", GLOBAL_BLOCKED)


def test_global_exclusion_exception_rejects_suffix_widening() -> None:
    overrides = [{
        "asset": "api.cloudflare.com",
        "action": "include",
        "allow_global_exclusion": True,
        "reason": "official endpoint",
        "evidence": EVIDENCE_URL,
    }]

    with pytest.raises(ValueError, match="outside service allow policy"):
        apply_overrides(
            set(),
            overrides,
            exact=("cloudflare.com",),
            suffixes=("cloudflare.com",),
            blocked_suffixes=GLOBAL_BLOCKED,
        )


def test_global_exclusion_exception_requires_explicit_opt_in() -> None:
    overrides = [{
        "asset": "api.cloudflare.com",
        "action": "include",
        "reason": "official endpoint",
        "evidence": EVIDENCE_URL,
    }]

    with pytest.raises(ValueError, match="conflicts with exclusion policy"):
        apply_overrides(
            set(),
            overrides,
            exact=("api.cloudflare.com",),
            suffixes=(),
            blocked_suffixes=GLOBAL_BLOCKED,
        )


def test_other_service_cannot_reuse_cloudflare_exact_exception() -> None:
    overrides = [{
        "asset": "api.cloudflare.com",
        "action": "include",
        "allow_global_exclusion": True,
        "reason": "official endpoint",
        "evidence": EVIDENCE_URL,
    }]

    with pytest.raises(ValueError, match="outside service allow policy"):
        apply_overrides(
            set(),
            overrides,
            exact=("api.other-service.example",),
            suffixes=(),
            blocked_suffixes=GLOBAL_BLOCKED,
        )
