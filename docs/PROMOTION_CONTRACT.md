# Promotion Contract

## Source → Collection

    Source Snapshot
        ↓
    Evidence Gate
        ↓
    Durable Release
        ↓
    Immutable provenance v2 seal
        ↓
    Collection-owned handoff PR
        ↓
    Collection Source Gate
        ↓
    Collection Canary
        ↓
    Production / Observation

## Binding

Collection must bind the exact Source commit and verify:

`snapshot_id` · `content_digest` · `evidence_digest` · `policy_digest` · `generator_digest` · `release_digest` · `expected_sha256`.

Any equality failure blocks acquisition.

## Ownership

Source never writes Collection Canonical, IR or client output.

Collection Auto Handoff uses the Collection workflow token. No cross-repository Secret is required.

## Lifecycle semantics

Source `production` means the Source evidence/release lifecycle is active. It does not by itself authorize Collection final production.

Collection Canary, Production and Observation remain authoritative for final publication.