# Changelog

## 0.1.0 - 2026-09-20

### Architecture baseline

- Bootstrap official-source-driven domain generation engine.
- First-wave service registry (8 services) with allow policies.
- HTML + JSON domain extraction with hostname allow-list.
- Exclusion catalogs (shared infrastructure / provider / external dependency).
- Evidence and provenance binding; content-addressed immutable snapshots.
- Count-change safety gates (empty list / large removal / growth).
- Collection reconciliation audit stub.
- Full policy documentation set (architecture, service, evidence, domain, release, promotion, security, operations).
- JSON schemas for service / asset / evidence / snapshot / release / exclusion / source.
- Authoring tree for human overrides and per-service stubs.
- Adapter package placeholders for future structured official sources.
- GitHub Actions: validate, scheduled generate, weekly reconcile.
