# Service Policy

## Gap states

| State | Meaning |
|---|---|
| `COVERED` | trusted source coverage is complete for the audited scope |
| `PARTIAL` | source exists but evidence coverage is incomplete |
| `MISSING` | no usable dedicated source is available |
| `SOURCE_DRIFT` | known source moved or failed persistently |
| `INTENTIONAL` | explicitly not materialized |
| `CONFLICT` | ownership conflict unresolved |
| `REVIEW` | evidence or boundary proof incomplete |

Gap classification must come from the Gap Engine and evidence chain, not from the existence of a URL alone.

## Source platform lifecycle

`config/source_canary_state.yaml` is the only lifecycle state database.

`config/services.yaml` is static service configuration and boundary policy.

Collection lifecycle is a separate authority and may lag Source lifecycle while Canary or Production gates run.

## Source priority

For every independent service the acquisition order is:

    dedicated upstream rule
          ↓
    trusted upstream service-specific rule
          ↓
    official evidence discovery
          ↓
    self-built candidate chain

A provider aggregate is never automatically inherited by a child service. A service-specific upstream file must be explicitly bound by `source_bindings` and constrained by `allowed_host_exact` / `allowed_host_suffixes`.

## Production prerequisites

    Trusted Source Evidence
      + Boundary
      + Exclusion
      + Conflict = 0
      + Deterministic Snapshot
      + Durable Release
      + Immutable provenance
      + Collection reconciliation

`source_policy.allowed_authorities` defines which evidence authorities are valid for a service. `official_required: true` keeps the original official-evidence gate; services that explicitly opt into trusted upstream evidence may set it to false.

## Service scope

Alibaba, Tencent, Baidu, NetEase and ByteDance are ecosystem groupings, not automatic ownership inheritance. Shared CDN, provider infrastructure and third-party dependencies stay outside dedicated service rules unless explicitly proven by the bound service-specific source.
