# Operations

## Active CI

| Workflow | 作用 |
|---|---|
| validate.yml | 配置、单元、Snapshot Schema、Conflict、Audit |
| generate.yml | 定时官方抓取，创建自动刷新 PR |
| reconcile.yml | 与 Collection Registry / Intentional 状态进行对账 |
| release.yml | 手动 Release Gate，输出 Artifact，不直接发布到 Collection |

## CLI

~~~bash
python -m source_engine validate
python -m source_engine audit
python -m source_engine gap
python -m source_engine reconcile
python -m source_engine discover --service 1688
python -m source_engine generate --service 1688
python -m source_engine release --service 1688
python -m source_engine schema-validate
python -m source_engine conflict
python -m source_engine health
~~~

## Operational Rule

Fetch failure 不等于 service coverage = 0。

失败时保留 Last Known Good，并把 Source Health 标记为 degraded/blocked。

## Metrics

重点关注：

- verified coverage
- evidence completeness
- conflict rate
- false attribution rate
- reconciliation completeness
- source freshness
- deterministic reproducibility

不要用域名数量作为唯一质量指标。
