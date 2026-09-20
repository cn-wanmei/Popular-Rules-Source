# Changelog

## 0.1.1 - 2026-09-20

### Phase 3–6 progress

- **1688 sample**: official HTML/JSON fixtures, regression tests, CANDIDATE snapshot (7 domains).
- **Alibaba group**: taobao / tmall / cainiao fixtures, seeds, CANDIDATE snapshots; `docs/ALIBABA_BOUNDARY.md`.
- **Tencent group**: dingding / qqmusic / tencentcloud fixtures and partial seeds; `docs/TENCENT_BOUNDARY.md`.
- **Promotion Bridge stub**: `source_engine.promotion` + `python -m source_engine promote`.
- Exclusion catalogs filter shared CDN (alicdn / gtimg / providers) before materialization.
- Full V1.1 architecture baseline docs and schemas (0.1.0).

## 0.1.0 - 2026-09-20

- Bootstrap official-source-driven domain generation.
- First-wave service registry, HTML/JSON extraction, immutable snapshots, CI.
