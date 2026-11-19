# Huawei Cloud API endpoint discovery — 2026-11-19

> Scope: P1/P2 independent API sub-services already registered in `config/services.yaml`.
> This is an evidence-discovery record, not a lifecycle promotion or a production binding.

## Official evidence

The Huawei Cloud Server Migration Service (SMS) FAQ documents the network dependencies used by its agent. It explicitly distinguishes global-level services from region-level services and lists the concrete endpoint hosts for the CN South-Guangzhou (`cn-south-1`) migration target:

- [How Do I Set Up a Secure Migration Network for Using SMS?](https://support.huaweicloud.com/intl/en-us/sms_faq/sms_faq_0001.html)
  - IAM global endpoint: `iam.myhuaweicloud.com`
  - ECS regional endpoint: `ecs.cn-south-1.myhuaweicloud.com`
  - EVS regional endpoint: `evs.cn-south-1.myhuaweicloud.com`
  - VPC regional endpoint: `vpc.cn-south-1.myhuaweicloud.com`
  - IMS regional endpoint: `ims.cn-south-1.myhuaweicloud.com`
  - DNS regional endpoint: `dns.cn-south-1.myhuaweicloud.com`
  - OBS endpoints: `obs.cn-north-1.myhuaweicloud.com` and `obs.cn-south-1.myhuaweicloud.com`

The same documentation states that ECS, EVS, IMS, VPC, and DNS endpoints depend on the target region; the listed regional hosts are therefore a confirmed regional sample, not a complete global inventory.

## Per-service official API documentation

| Source service ID | Official API / endpoint documentation | Confirmed endpoint scope |
|---|---|---|
| `huawei-iam-api` | [IAM API Reference — Before You Start](https://support.huaweicloud.com/intl/en-us/api-iam/iam_01_0001.html) | Global `iam.myhuaweicloud.com`; the page also enumerates regional IAM endpoints |
| `huawei-ecs-api` | [ECS API Reference — Before You Start](https://support.huaweicloud.com/intl/en-us/api-ecs/en-us_topic_0020805967.html) | Regional; CN South-1 host confirmed by the SMS FAQ |
| `huawei-evs-api` | [EVS API Reference — Before You Start](https://support.huaweicloud.com/intl/en-us/api-evs/evs_04_0001.html) | Regional; CN South-1 host confirmed by the SMS FAQ |
| `huawei-vpc-api` | [VPC API Reference — Before You Start](https://support.huaweicloud.com/intl/en-us/api-vpc/en-us_topic_0173364201.html) | Regional; CN South-1 host confirmed by the SMS FAQ |
| `huawei-ims-api` | [IMS API Reference — Before You Start](https://support.huaweicloud.com/intl/en-us/api-ims/ims_03_0101.html) | Regional; CN South-1 host confirmed by the SMS FAQ |
| `huawei-dns-api` | [DNS API Reference — Before You Start](https://support.huaweicloud.com/intl/en-us/api-dns/dns_api_10000.html) | Regional; CN South-1 host confirmed by the SMS FAQ |
| `huawei-obs-api` | [OBS — Accessing OBS](https://support.huaweicloud.com/intl/en-us/usermanual-obs/obs_41_0003.html) and [OBS — Endpoints and Domain Names](https://support.huaweicloud.com/intl/en-us/productdesc-obs/obs_03_0152.html) | Regional endpoints; CN North-1 and CN South-1 confirmed by the SMS FAQ; OBS docs explain region-specific endpoint and bucket-hostname formats |

## Boundary decisions

1. Treat only the API endpoint hosts above as service candidates. Do not add the SMS service endpoint, documentation hosts, console hosts, or unrelated Huawei Cloud web properties to these API sub-services.
2. Do not add the SMS-Agent bucket hosts (`sms-resource-intl-ap-southeast-3.obs.ap-southeast-3.myhuaweicloud.com`, `sms-agent-config-inter.obs.ap-southeast-3.myhuaweicloud.com`) to the OBS API service. They are named migration buckets, not the generic OBS API endpoint.
3. Do not infer every regional hostname from a naming pattern. Expand regional hosts only from Huawei Cloud's official Regions and Endpoints inventory or another official service document that explicitly enumerates them.
4. Do not use a broad `myhuaweicloud.com` suffix allowlist. Keep service boundaries explicit and service-specific.
5. Do not change lifecycle state, create a release, or add a Collection immutable binding based on this discovery note alone.

## Current gap and next validation

The Source lifecycle report currently records all seven services as `REVIEW` with `domain_count=0`. The configuration already contains one or more endpoint candidates for these services, but a candidate allowlist is not itself evidence and does not create a generated snapshot.

Next steps:

1. Validate the official-source fetch and extraction path for each service against the cited pages.
2. Persist per-service official evidence with source URL, retrieval timestamp, response/content hash, parser version, and extracted host list.
3. Run service-boundary and deterministic-output checks; confirm that each service receives only its own API endpoint host(s).
4. Generate immutable snapshots/releases only after completeness gates pass.
5. Keep all seven services in REVIEW until their own evidence and release gates pass; then qualify individually. No bulk promotion.

## Source references

- IAM: `https://support.huaweicloud.com/intl/en-us/api-iam/iam_01_0001.html`
- ECS: `https://support.huaweicloud.com/intl/en-us/api-ecs/en-us_topic_0020805967.html`
- EVS: `https://support.huaweicloud.com/intl/en-us/api-evs/evs_04_0001.html`
- VPC: `https://support.huaweicloud.com/intl/en-us/api-vpc/en-us_topic_0173364201.html`
- IMS: `https://support.huaweicloud.com/intl/en-us/api-ims/ims_03_0101.html`
- DNS: `https://support.huaweicloud.com/intl/en-us/api-dns/dns_api_10000.html`
- OBS: `https://support.huaweicloud.com/intl/en-us/usermanual-obs/obs_41_0003.html`
- Shared official endpoint evidence: `https://support.huaweicloud.com/intl/en-us/sms_faq/sms_faq_0001.html`
