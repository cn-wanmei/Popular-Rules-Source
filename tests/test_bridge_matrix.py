from __future__ import annotations

import pytest

from source_engine.bridge_matrix import (
    ZERO_SHA,
    changed_service_ids,
    parse_wave_services,
    resolve_service_matrix,
)


DEFAULT_BATCH = ["existing-a", "existing-b"]
BEFORE_SHA = "1" * 40


def test_changed_service_ids_selects_added_and_modified_in_current_order() -> None:
    previous = {
        "unchanged": {"exact": ["old.example"]},
        "modified": {"exact": ["before.example"]},
        "removed": {"exact": ["removed.example"]},
    }
    current = {
        "unchanged": {"exact": ["old.example"]},
        "new-service": {"exact": ["new.example"]},
        "modified": {"exact": ["after.example"]},
    }

    assert changed_service_ids(previous, current) == ["new-service", "modified"]


def test_changed_service_ids_returns_empty_for_identical_mappings() -> None:
    services = {"stable": {"exact": ["stable.example"]}}

    assert changed_service_ids(services, dict(services)) == []


def test_removed_only_wave_change_fails_closed() -> None:
    with pytest.raises(ValueError, match="refusing to fall back"):
        changed_service_ids({"removed": {"exact": ["removed.example"]}}, {})


def test_push_uses_only_changed_p1_p2_services() -> None:
    previous = {
        "unchanged": {"exact": ["unchanged.example"]},
        "huawei-iam-api": {"exact": ["iam.example"]},
        "huawei-ecs-api": {"exact": ["ecs-old.example"]},
    }
    current = {
        "unchanged": {"exact": ["unchanged.example"]},
        "huawei-iam-api": {"exact": ["iam.example"]},
        "huawei-ecs-api": {"exact": ["ecs-new.example"]},
        "huawei-obs-api": {"exact": ["obs.example"]},
    }

    services, mode = resolve_service_matrix(
        services_input="",
        event_name="push",
        before_sha=BEFORE_SHA,
        previous_services=previous,
        current_services=current,
        default_batch=DEFAULT_BATCH,
    )

    assert services == ["huawei-ecs-api", "huawei-obs-api"]
    assert mode == "push_changed_p1_p2_services"


def test_manual_selective_input_is_deduplicated_and_preserves_order() -> None:
    services, mode = resolve_service_matrix(
        services_input="huawei-iam-api, huawei-ecs-api;huawei-iam-api",
        event_name="workflow_dispatch",
        before_sha="",
        previous_services=None,
        current_services={},
        default_batch=DEFAULT_BATCH,
    )

    assert services == ["huawei-iam-api", "huawei-ecs-api"]
    assert mode == "selective"


@pytest.mark.parametrize("value", ["", "default", "batch", "all-batch", "all"])
def test_default_mode_keeps_existing_default_batch(value: str) -> None:
    services, mode = resolve_service_matrix(
        services_input=value,
        event_name="workflow_dispatch",
        before_sha="",
        previous_services=None,
        current_services={},
        default_batch=DEFAULT_BATCH,
    )

    assert services == DEFAULT_BATCH
    assert mode == "default_processing_batch"


def test_push_without_p1_p2_changes_keeps_default_batch() -> None:
    stable = {"existing": {"exact": ["stable.example"]}}

    services, mode = resolve_service_matrix(
        services_input="",
        event_name="push",
        before_sha=BEFORE_SHA,
        previous_services=stable,
        current_services=stable,
        default_batch=DEFAULT_BATCH,
    )

    assert services == DEFAULT_BATCH
    assert mode == "default_processing_batch"


def test_push_without_previous_commit_keeps_default_batch() -> None:
    services, mode = resolve_service_matrix(
        services_input="",
        event_name="push",
        before_sha=ZERO_SHA,
        previous_services=None,
        current_services={"new": {"exact": ["new.example"]}},
        default_batch=DEFAULT_BATCH,
    )

    assert services == DEFAULT_BATCH
    assert mode == "default_processing_batch"


def test_push_diff_requires_previous_configuration() -> None:
    with pytest.raises(ValueError, match="previous P1/P2 service mapping"):
        resolve_service_matrix(
            services_input="",
            event_name="push",
            before_sha=BEFORE_SHA,
            previous_services=None,
            current_services={},
            default_batch=DEFAULT_BATCH,
        )


def test_parse_wave_services_requires_services_mapping() -> None:
    parsed = parse_wave_services(
        "version: 1\nservices:\n  one: {exact: [one.example]}\n"
    )

    assert list(parsed) == ["one"]
    with pytest.raises(ValueError, match="services mapping"):
        parse_wave_services("version: 1\n")
