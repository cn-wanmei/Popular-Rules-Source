# Release Policy

## Snapshot immutability

Once a snapshot directory exists with a manifest, it is never overwritten.
Corrections produce snapshot N+1.

## Determinism

Same raw content + parser version + config → identical domains, order, checksums.
Timestamps are metadata only and must not affect content identity.

## Hard gates (block release)

- schema_error > 0
- invalid_evidence > 0
- unresolved_conflict > 0
- unexpected empty list (previous non-empty → current empty)
- determinism_fail > 0
- removal_ratio above threshold without review confirmation

## Soft conditions (degraded, not fail)

- temporary HTTP 429 / 5xx / timeout
- single upstream rate limit
- temporary DNS failure

Retain last-known-good; mark source health degraded.

## Release package minimum

- manifest.json
- domains (or domains.txt)
- provenance / evidence
- exclusions / tombstones (when applicable)
- checksums
- reconciliation summary when available

## Rollback

Restore promotion pointer to previous release. Do not rewrite history.
