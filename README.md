# Popular-Rules-Source

Official-source-driven missing-service domain source generation for Popular-Rules-Collection.

## Core pipeline

```text
Official source
  -> fetch
  -> raw snapshot
  -> domain extraction
  -> normalization
  -> service boundary / exclusions
  -> validation
  -> generated source
  -> immutable snapshot
  -> release
```

The repository is a supplemental source/evidence layer. It does not implement the V3 runtime, canonical model, or client adapters of Popular-Rules-Collection.

## First-wave services

- 1688
- cainiao
- dingding
- qqmail
- qqmusic
- taobao
- tencentcloud
- tmall

Service status is audit-derived. A service may be MISSING, PARTIAL, COVERED, SOURCE_DRIFT, INTENTIONAL, CONFLICT, or REVIEW.

## Commands

```bash
python -m source_engine audit
python -m source_engine generate --service 1688
python -m source_engine generate --all
python -m source_engine test-determinism
python -m source_engine release --service 1688
```

## Design rules

1. Official source evidence is preferred.
2. Official pages do not imply every referenced domain belongs to the target service.
3. Shared infrastructure, provider ranges, and third-party dependencies are excluded by policy.
4. Fetch failure never produces an empty replacement release.
5. Published snapshots are immutable.
6. Every generated domain is traceable to source, parser, evidence, and snapshot metadata.
