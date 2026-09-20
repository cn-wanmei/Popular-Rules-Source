# Popular-Rules-Source

> **Popular-Rules-Collection 的独立补充型 Source / Evidence Supply Layer**  
> Official-source-driven domain generation for missing / partial services.

Repository: `cn-wanmei/Popular-Rules-Source`  
Upstream production: `cn-wanmei/Popular-Rules-Collection`  
Version: see `VERSION`

## Positioning

```text
发现缺口 → 定位官方来源 → 采集 → 提取域名 → 归属验证
      → 排除共享基础设施 → Domain Source → Immutable Snapshot
      → Release → Promotion Bridge → Collection V3
```

This repository does **not** re-implement Canonical, IR, hierarchy, V3 runtime, or the 7 client adapters.

## Core capability: Official Direct Domain Generation

Priority order:

1. Official machine-readable list  
2. Official API / structured data  
3. Official config / SDK / manifest  
4. Official documentation extraction  
5. Runtime discovery  
6. External cross-check  

Current implemented path: **official web + JSON domain extraction** with allow-list policy, exclusion catalogs, evidence binding, count-change gates, and content-addressed immutable snapshots.

## First-wave services

| Service | Ecosystem | Notes |
| ------- | --------- | ----- |
| 1688 | alibaba | Official open platform |
| cainiao | alibaba | Logistics; strict boundary vs Taobao |
| dingding | alibaba | DingTalk open platform |
| qqmail | tencent | Mail endpoints; avoid general QQ infra |
| qqmusic | tencent | Music; CDN review required |
| taobao | alibaba | Open platform / API |
| tencentcloud | tencent | **PARTIAL** — audit existing Collection registry first |
| tmall | alibaba | Open / business endpoints |

Status is audit-derived (`MISSING` / `PARTIAL` / `COVERED` / `REVIEW` / …), not a static “all missing” list.

## Commands

```bash
pip install -r requirements.txt

python -m source_engine validate
python -m source_engine audit          # service gap report → reports/service-gap.json
python -m source_engine reconcile      # Collection-oriented reconciliation stub
python -m source_engine generate --service qqmail
python -m source_engine generate --all
python -m source_engine release --service qqmail
python -m source_engine test-determinism
python -m source_engine dod
python -m source_engine discover --service 1688
python -m source_engine revoke --service 1688 --domain bad.example.com
python -m source_engine promote --service 1688 --snapshot <snap-id>
pytest -q
```

## Layout (aligned with final architecture)

```text
authoring/          # human input (service manifests, overrides, exclusions)
adapters/           # reserved structured official adapters
config/             # services.yaml, source_adapters.yaml, validation.yaml
docs/               # architecture & policies
exclusions/         # runtime exclusion catalogs
schemas/            # JSON schemas for service/asset/evidence/snapshot/release
source_engine/      # fetch → extract → normalize → policy → build → release
generated/          # build outputs (not Collection generated/)
snapshots/          # immutable snapshots
raw/                # optional local raw upstream (not committed by default)
reports/            # gap / reconciliation reports
tests/
.github/workflows/  # validate / generate / reconcile
```

## Design rules (non-negotiable)

1. Official source evidence is preferred; never invent domains.  
2. Official page ≠ every hostname is service-owned.  
3. Shared CDN / provider / third-party dependencies are excluded.  
4. Fetch failure never replaces last-known-good with an empty list.  
5. Snapshots are immutable; fixes produce N+1.  
6. Every generated domain is traceable (asset_id, evidence, source, snapshot).  
7. False attribution is worse than missing coverage.

## Safety gates

- Empty replacement blocked when previous count > 0  
- Large removal / growth ratios force `REVIEW`  
- Exclusion suffix catalog applied before materialization  
- Schema / config validation on CI  

## Promotion

Release packages are inputs to a **Promotion Bridge** into Popular-Rules-Collection’s existing Source Registry / collect path. This repo never writes Collection Canonical or client outputs.

## Documentation

- [ARCHITECTURE.md](docs/ARCHITECTURE.md)
- [OFFICIAL_SOURCE_GENERATION.md](docs/OFFICIAL_SOURCE_GENERATION.md)
- [SERVICE_POLICY.md](docs/SERVICE_POLICY.md)
- [EVIDENCE_POLICY.md](docs/EVIDENCE_POLICY.md)
- [DOMAIN_POLICY.md](docs/DOMAIN_POLICY.md)
- [RELEASE_POLICY.md](docs/RELEASE_POLICY.md)
- [PROMOTION_CONTRACT.md](docs/PROMOTION_CONTRACT.md)
- [SECURITY.md](docs/SECURITY.md)
- [OPERATIONS.md](docs/OPERATIONS.md)
