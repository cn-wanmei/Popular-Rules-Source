from __future__ import annotations

from pathlib import Path

import yaml


EXPECTED = {
    "huawei-iam-api": {
        "hosts": ["iam.myhuaweicloud.com"],
        "source": "https://support.huaweicloud.com/intl/en-us/api-iam/iam-api-pdf.pdf",
    },
    "huawei-ecs-api": {
        "hosts": ["ecs.cn-south-1.myhuaweicloud.com"],
        "source": "https://support.huaweicloud.com/intl/en-us/sms_faq/sms_faq_0001.html",
    },
    "huawei-evs-api": {
        "hosts": ["evs.cn-south-1.myhuaweicloud.com"],
        "source": "https://support.huaweicloud.com/tg-mgc/tg-mgc-pdf.pdf",
    },
    "huawei-vpc-api": {
        "hosts": ["vpc.cn-south-1.myhuaweicloud.com"],
        "source": "https://support.huaweicloud.com/tg-mgc/tg-mgc-pdf.pdf",
    },
    "huawei-ims-api": {
        "hosts": ["ims.cn-south-1.myhuaweicloud.com"],
        "source": "https://support.huaweicloud.com/tg-mgc/tg-mgc-pdf.pdf",
    },
    "huawei-dns-api": {
        "hosts": ["dns.cn-south-1.myhuaweicloud.com"],
        "source": "https://support.huaweicloud.com/intl/en-us/sms_faq/sms_faq_0001.html",
    },
    "huawei-obs-api": {
        "hosts": [
            "obs.cn-north-4.myhuaweicloud.com",
            "obs.cn-south-1.myhuaweicloud.com",
        ],
        "source": "https://support.huaweicloud.com/intl/en-us/usermanual-obs/obs_41_0003.html",
    },
}


def _load(root: Path, relative: str):
    return yaml.safe_load((root / relative).read_text(encoding="utf-8"))


def test_huawei_cloud_api_children_are_exact_review_only_nodes() -> None:
    root = Path(__file__).resolve().parents[1]
    services = _load(root, "config/services.yaml")["services"]
    self_built = _load(root, "config/self_built_services.yaml")["services"]
    adapters = _load(root, "config/source_adapters.yaml")["services"]
    lifecycle = _load(root, "config/source_canary_state.yaml")["services"]
    wave = _load(root, "config/p1_p2_self_built_official_wave.yaml")["services"]
    program = _load(root, "config/service_completion_program.yaml")

    default_batch = _load(root, "config/durable_release_policy.yaml")["default_processing_batch"]
    p1 = program["verified_priority_wave"]["p1"]

    for service_id, definition in EXPECTED.items():
        hosts = definition["hosts"]
        source = definition["source"]

        service = services[service_id]
        assert service["allowed_host_exact"] == hosts
        assert service["allowed_host_suffixes"] == []
        assert service["official_sources"] == [source]
        assert service["source_policy"]["official_required"] is True
        assert service["source_policy"]["allowed_authorities"] == ["official"]
        assert service["boundary"]["mode"] == "source_bound"
        assert service["boundary"]["shared_infrastructure_allowed"] is False

        source_definition = self_built[service_id]
        assert source_definition["allowed_host_exact"] == hosts
        assert source_definition["official_sources"] == [source]
        assert source_definition["current_state"] == "review"
        assert adapters[service_id]["adapters"] == ["self_built"]

        state = lifecycle[service_id]
        assert state["state"] == "review"
        assert state["enabled"] is True
        assert service_id not in default_batch
        assert service_id in p1
        assert wave[service_id]["exact"] == hosts
        assert wave[service_id]["phase"] == "P1"

        asset_path = root / "self_built" / service_id / "domains.list"
        lines = [
            line.strip()
            for line in asset_path.read_text(encoding="utf-8").splitlines()
            if line.strip() and not line.lstrip().startswith("#")
        ]
        assert lines == [f"DOMAIN,{host}" for host in hosts]


def test_huawei_cloud_api_tree_excludes_dynamic_and_wildcard_boundaries() -> None:
    root = Path(__file__).resolve().parents[1]
    services = _load(root, "config/services.yaml")["services"]
    for service_id in EXPECTED:
        service = services[service_id]
        assert service["allowed_host_suffixes"] == []
        assert all("*" not in host for host in service["allowed_host_exact"])

    program = _load(root, "config/service_completion_program.yaml")["huawei_cloud_api_endpoint_scope"]
    assert program["exact_host_only"] is True
    assert "wildcard_myhuaweicloud_com" in program["excluded"]
    assert "dynamic_obs_bucket_hostnames" in program["excluded"]
    assert "dynamic_cce_cluster_id_subdomains" in program["excluded"]
