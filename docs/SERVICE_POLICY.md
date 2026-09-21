# Service Policy

## Gap states

| State | Meaning |
|---|---|
| `COVERED` | trusted source coverage is complete for the audited scope |
| `PARTIAL` | source exists but evidence coverage is incomplete |
| `MISSING` | no usable dedicated official source is available |
| `SOURCE_DRIFT` | known source moved or failed persistently |
| `INTENTIONAL` | explicitly not materialized |
| `CONFLICT` | ownership conflict unresolved |
| `REVIEW` | evidence or boundary proof incomplete |

Gap classification must come from the Gap Engine and evidence chain, not from the existence of a URL alone.

## Source platform lifecycle

`config/source_canary_state.yaml` is the only lifecycle state database.

`config/services.yaml` is static configuration.

Collection lifecycle is a separate authority and may lag Source lifecycle while Canary or Production gates run.

## Production prerequisites

    Official Evidence
      + Boundary
      + Exclusion
      + Conflict = 0
      + Deterministic Snapshot
      + Durable Release
      + Immutable provenance
      + Collection reconciliation

## Service scope

Alibaba and Tencent are ecosystem groupings, not automatic ownership inheritance. Shared CDN and provider infrastructure stay outside dedicated service rules unless explicitly proven.