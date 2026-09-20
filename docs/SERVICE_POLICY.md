# Service Policy

## Gap Status

| 状态 | 含义 |
|---|---|
| COVERED | 完整可信覆盖 |
| PARTIAL | 已有 Source 但覆盖不足 |
| MISSING | 没有可用专用 Source |
| SOURCE_DRIFT | 已知来源永久迁移/失效 |
| INTENTIONAL | 明确不物化 |
| CONFLICT | 归属冲突未解决 |
| REVIEW | 证据不足 |

Missing Service 必须由 Multi-dimensional Gap Audit 得出，而不是简单判断有没有 URL。

## First Wave

1688、cainiao、dingding、qqmail、qqmusic、taobao、tencentcloud、tmall。

当前默认状态：7 个 REVIEW，Tencent Cloud PARTIAL。

## Production

必须满足：

~~~text
Official Evidence
+
Service Boundary
+
Exclusion
+
Conflict = 0
+
Deterministic Snapshot
+
Reconciliation PASS
~~~

## Seed

Manual seed_domains 是候选输入，不是 Production Evidence。

## Ecosystem

Alibaba / Tencent 是生态关系，不是资产继承关系。

Shared CDN、Provider Infrastructure、Generic Gateway 必须单独处理。

## DoD

每个服务都必须完成官方来源、Evidence、边界、排除、冲突审计、生成、Snapshot、Reconciliation 和 CI Gate。
