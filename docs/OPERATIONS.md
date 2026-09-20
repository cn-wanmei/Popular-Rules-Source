# Operations

## Daily / scheduled

| Workflow | Purpose |
| -------- | ------- |
| validate.yml | Config + unit tests + audit on push/PR |
| generate.yml | Scheduled official fetch → generate snapshots |
| reconcile.yml | Compare with Collection registry/canonical signals |

## CLI

```bash
python -m source_engine validate
python -m source_engine audit
python -m source_engine reconcile
python -m source_engine generate --service taobao
python -m source_engine generate --all
python -m source_engine release --service taobao
python -m source_engine test-determinism
```

## Observability KPIs

Prefer quality over quantity:

- Verified coverage
- Evidence completeness
- Conflict rate
- False attribution rate
- Reconciliation completeness
- Release determinism
- Source freshness

Do not optimize solely for domain/IP counts.

## Retention guidance

- Snapshots: 90–180 days
- Release / audit evidence: ~180 days
- Current releases + tombstones: permanent
