# Changelog

## 0.2.0 - 2026-09-20

### Full plan residual capabilities

- Tombstone / revoke layer (`tombstones/`, CLI `revoke` / `tombstones`)
- Domain diff in every snapshot manifest
- Last-known-good retention when fetch fails and domain set would be empty
- Authoring overrides (include/exclude) applied at materialization
- Discovery CLI (`discover`) — candidates only
- Definition-of-Done report (`dod` → reports/definition-of-done.json)
- scripts/ wrappers: audit, build, validate, release, reconcile, discover, snapshot
- CI: audit.yml, build.yml, release.yml (+ existing validate/generate/reconcile)
- config/release.yaml, config/schemas.yaml (schema freeze)
- docs/IP_POLICY.md
- Audit report includes latest snapshot status

## 0.1.1 - 2026-09-20

- Phase 3–6: 1688 sample, Alibaba/Tencent fixtures, promotion bridge stub

## 0.1.0 - 2026-09-20

- V1.1 architecture baseline
