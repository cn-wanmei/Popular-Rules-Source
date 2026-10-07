# Funnel acceleration (P0 ops)

## Weekly quota

≥ 8 services: `VERIFIED → CANARY` (reason: `weekly_funnel_quota_YYYY-MM-DD`).

Do **not** skip to `PRODUCTION` without Collection immutable binding.

## 2026-10-07 snapshot guidance

1. Run `python -m source_engine health` and list `degraded`.
2. For each degraded: `gap` → `repair` → re-`health`. Do not overwrite LKG with empty fetch.
3. From `VERIFIED` with high domain count / product priority, batch canary (Apple/Microsoft/AI already partly canary as of Oct 3 batch).
4. `BLOCKED` or `domains=0` (e.g. cloudflare in historical table): keep blocked or tombstone; do not canary.
5. Collection side: follow handoff PRs; `sources/immutable_registry.yaml` is binding SSOT.

## Degraded triage template

| Service | Class | Action | Owner |
|---------|-------|--------|-------|
| (fill from health) | degraded | repair / blocked | |

## Related

- Collection `docs/FUNNEL_OPS.md`
- Collection `docs/SOURCE_COLLECTION_FUNNEL.md`
- `config/source_canary_state.yaml`
