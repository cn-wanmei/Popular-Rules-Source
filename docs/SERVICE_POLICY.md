# Service Policy

## Gap statuses

| Status | Meaning |
| ------ | ------- |
| `COVERED` | Full verified coverage exists |
| `PARTIAL` | Source exists but coverage incomplete |
| `MISSING` | No usable dedicated source |
| `SOURCE_DRIFT` | Known upstream moved or failed permanently |
| `INTENTIONAL` | Explicitly not to be materialized |
| `CONFLICT` | Ownership conflict unresolved |
| `REVIEW` | Evidence insufficient; needs human review |

"Missing service" means **coverage gap after multi-dimensional audit**, not merely "no upstream URL found".

## First-wave services

- 1688, cainiao, dingding, qqmail, qqmusic, taobao, tencentcloud, tmall

`tencentcloud` starts as `PARTIAL` / `REVIEW` because Collection already has registry mapping.

## Ecosystem boundaries

Alibaba ecosystem and Tencent ecosystem are modeled separately.
Shared infrastructure (CDN, login, object storage, API gateway) must not be
attributed to a single product service without service-specific evidence.

## Definition of Done (per service)

- [ ] Service manifest
- [ ] Gap audit
- [ ] Official evidence (positive)
- [ ] Negative evidence / exclusions where relevant
- [ ] Domain validation
- [ ] Shared-infrastructure audit
- [ ] Duplicate / conflict checks
- [ ] Materialization
- [ ] Deterministic snapshot
- [ ] Reconciliation
- [ ] CI pass
- [ ] Promotion-ready release
