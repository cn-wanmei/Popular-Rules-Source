# Evidence Policy

## Dimensions

Evidence 分为：

~~~text
authority
source_method
evidence_strength
confidence
service_scope
~~~

## Grades

| Grade | 示例 | 作用 |
|---|---|---|
| S0 | 官方机器可读列表 / 官方 API / 官方配置 | Production-capable |
| S1 | 官方技术 Endpoint / 文档 / SDK | Production-capable after boundary validation |
| S2 | 高质量外部交叉证据 | Auxiliary |
| S3 | Blog / Forum / 单一第三方规则 | Discovery only |

## Required Fields

evidence_id、service_id、asset、asset_type、source_url、source_method、retrieved_at、content_hash、parser_version、confidence、status。

## Positive / Negative

必须可以解释：

~~~text
Why included?
Why excluded?
~~~

排除证据覆盖 Shared Infrastructure、Provider CDN、External Dependency、Ambiguous Ownership、Wrong Product Scope。

## Seed

Authoring Seed 的 Evidence 为：

source_method = authoring_seed  
confidence = unknown  
status = candidate

Seed 不能直接提升为 Production Evidence。
