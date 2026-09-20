# Architecture — Popular-Rules-Source

## Positioning

`Popular-Rules-Source` is the **supplemental Source / Evidence Supply Layer** for
`Popular-Rules-Collection`.

It does **not** implement:

- Canonical model
- Semantic IR
- Hierarchy / Decision
- V3 Runtime
- Client adapters (egern / loon / mihomo / quantumultx / shadowrocket / singbox / surge)
- Atomic promotion into production generated/

It **does** implement:

```text
Discovery → Evidence → Ownership → Boundary → Materialization
         → Immutable Snapshot → Release → Promotion Bridge input
```

## Core invariant

```text
Source ≠ Canonical ≠ Runtime ≠ Generated
```

## Data layers

| Layer | Responsibility |
| ----- | -------------- |
| Discovery | Candidate assets only |
| Evidence | Positive + negative evidence, hashes, retrieval metadata |
| Materialization | Verified service-owned domains/IPs after boundary checks |
| Release Snapshot | Immutable, deterministic, checksummed package |

## Official Direct Domain Generation

First-class capability:

```text
Official source
  → Source Adapter
  → Raw Snapshot
  → Parser / Domain Extractor
  → Normalizer
  → Ownership / Boundary / Exclusion
  → Domain List + Evidence Binding
  → Diff / Quality Gate
  → Immutable Snapshot / Release
```

## Source priority

1. Official machine-readable domain list
2. Official API / structured endpoint
3. Official config / SDK / manifest
4. Official documentation extraction
5. Official runtime discovery
6. External cross-verification

## Safety gates

- Fetch failure must not produce empty replacement of last-known-good
- Empty-list / large-removal thresholds block or force review
- Shared infrastructure and external dependencies excluded by policy
- Snapshots are immutable; corrections create N+1
- Tombstones prevent re-introduction of revoked assets

## Dual-repo flow

```text
Popular-Rules-Source
        │ immutable release
        ▼
Promotion Bridge
        │
        ▼
Popular-Rules-Collection (V3: collect → canonical → IR → 7 clients)
```

## Forbidden

- Guess domains / IPs
- ASN → product direct attribution
- CDN auto-map to product
- Single third-party rule promotion without evidence
- Auto-delete on one HTTP failure
- Mutate published snapshots
- Re-implement V3 engine or client adapters
