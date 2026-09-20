# Official Source Generation

## Objective

给定 Service ID，优先从该服务官方来源自动提取并生成经过验证的 Domain Source。

## Priority

~~~text
Official machine-readable
        ↓
Official API / structured
        ↓
Official config / SDK / manifest
        ↓
Official documentation
        ↓
Controlled runtime discovery
        ↓
External cross-check
~~~

## Current production implementation

当前主干实际可用的是 official_web：

~~~text
Official Web
  ↓
HTML / JSON extraction
  ↓
Per-service allow policy
  ↓
Exclusion
  ↓
Evidence
  ↓
Candidate / Release Candidate
~~~

Fixture-only Mode B 已从生产链删除。

## Seed

seed_domains 仅用于人工候选锚点。

只要最终输出包含 seed-only domain：

~~~text
release_state = REVIEW
~~~

直到该资产获得真实官方 Evidence。

## Evidence Trace

~~~text
domain
 ↓
asset_id
 ↓
evidence_id
 ↓
source_url
 ↓
content_hash
 ↓
parser_version
 ↓
snapshot_id
~~~

没有完整追溯链的资产不能进入 Production。

## Future Adapter Contract

新 Adapter 必须同时提交真实官方来源、字段契约、Parser、Fixture、Regression Test 和 Evidence Mapping。

没有完整契约的 Adapter 必须保持 disabled。
