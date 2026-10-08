# Funnel acceleration (P0 ops)

## Weekly quota

≥ 8 services: `VERIFIED → CANARY` (reason: `weekly_funnel_quota_YYYY-MM-DD`).

Do **not** skip to `PRODUCTION` without Collection immutable binding.

## Playbook

1. `python -m source_engine health` — list degraded/failed
2. For each degraded: `gap` → `repair` → re-health; never overwrite LKG with empty fetch
3. VERIFIED + high domains / P0 product → canary batch
4. BLOCKED or domains=0 → keep blocked / tombstone; do not canary
5. Long **REVIEW** without official evidence → do not promote; consider BLOCKED or drop from qualify queue
6. Collection side: handoff PRs; binding SSOT is Collection `sources/immutable_registry.yaml`

## Scope note

Collection `PUBLISH_STATUS` health counts are **Collection telemetry subset**, not this repo's full lifecycle histogram (see README summary / `reports/generated/lifecycle.json`).

## Related

- Collection `docs/FUNNEL_OPS.md` · `docs/FUNNEL_TRIAGE.md`
- Collection `docs/SOURCE_COLLECTION_FUNNEL.md`
- `config/source_canary_state.yaml`
