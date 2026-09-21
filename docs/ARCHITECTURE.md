# Architecture — Popular-Rules-Source

## Role

Popular-Rules-Source is the upstream Evidence Supply Layer for Popular-Rules-Collection.

It owns discovery, official evidence, boundary policy, Gap Detection, Repair, immutable Snapshot/Release, provenance identity and reconciliation.

It does not own Collection Canonical, Semantic IR, client adapters or final distribution.

## Pipeline

    Official Sources
         ↓
    Fetch / Retry / Health
         ↓
    Extract / Adapter Contract
         ↓
    Normalize / Boundary / Exclusion
         ↓
    Evidence Binding
         ↓
    Gap Engine / Repair
         ↓
    Immutable Snapshot
         ↓
    Evidence Gate
         ↓
    Durable Release
         ↓
    Immutable Seal
         ↓
    Collection Auto Handoff

## Lifecycle SSOT

`config/source_canary_state.yaml` is the only lifecycle state database.

`config/services.yaml` is static service definition.

Snapshot identity lives in the immutable snapshot manifest.

Collection consumes the Source immutable binding from its own `sources/immutable_registry.yaml`.

## Provenance v2

Every releasable service has:

- content digest
- evidence digest
- policy digest
- generator digest
- release digest
- immutable source reference
- verified input commit

Collection must verify all of them for equality before acquisition.

## Adapter architecture

The adapter contract supports official_web, official_json, official_api, official_manifest, official_sdk and official_browser.

Browser/JS execution is a controlled official-source adapter, not a general-purpose crawler. It is allowed only for explicitly configured official origins and must emit deterministic evidence metadata.

## Fail-closed boundaries

- third-party hosts are not automatically first-party service assets;
- provider/ASN infrastructure never establishes product ownership;
- external cross-checks are auxiliary evidence only;
- fetch degradation retains Last Known Good and blocks unsafe replacement;
- immutable artifacts are never rewritten.