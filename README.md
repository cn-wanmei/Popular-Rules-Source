# Popular-Rules-Source

> Popular-Rules-Collection 的独立补充型 Source / Evidence Supply Layer。核心能力是从目标服务的官方来源自动提取、验证并生成可审计的域名 Source。

仓库：cn-wanmei/Popular-Rules-Source  
上游生产项目：cn-wanmei/Popular-Rules-Collection  
版本：见 VERSION

## 当前真实状态

本仓库已完成 Source Engine 工程骨架，但当前没有任何服务获得 Production / Published 资格。

| Service | 当前状态 | 当前判断 |
|---|---|---|
| 1688 | REVIEW | 候选资产需要官方证据化 |
| cainiao | REVIEW | 需要独立物流边界审计 |
| dingding | REVIEW | 需要官方开放平台证据 |
| qqmail | REVIEW | 仅允许明确 Mail Endpoint |
| qqmusic | REVIEW | CDN / Shared Infrastructure 需排除 |
| taobao | REVIEW | 需要官方来源覆盖审计 |
| tencentcloud | PARTIAL | Collection 已有 Registry 映射，只做补充 |
| tmall | REVIEW | 需要官方来源覆盖审计 |

Authoring Seed 不是 Production Evidence。现有候选数据不得被描述为已发布服务规则。

## 核心流水线

~~~text
官方来源
  ↓
Fetch
  ↓
Raw Hash
  ↓
Extract
  ↓
Normalize
  ↓
Service Boundary
  ↓
Exclusion
  ↓
Evidence Binding
  ↓
Diff / Conflict Gate
  ↓
Immutable Snapshot
  ↓
Release Candidate
  ↓
Collection Reconciliation
~~~

## CLI

~~~bash
python -m source_engine validate
python -m source_engine audit
python -m source_engine gap
python -m source_engine reconcile
python -m source_engine discover --service 1688
python -m source_engine generate --service 1688
python -m source_engine generate --all
python -m source_engine release --service 1688
python -m source_engine test-determinism
python -m source_engine schema-validate
python -m source_engine conflict
python -m source_engine health
pytest -q
~~~

## 生产规则

- 不猜域名、不猜 IP。
- 官方页面中的第三方 Host 不自动属于目标服务。
- ASN、Provider、CDN 不得直接映射 Product Service。
- Authoring Seed 只能作为 Candidate/Fallback。
- Fetch 失败不能用空列表覆盖 Last Known Good。
- Snapshot 一旦形成不得覆盖。
- 每个 Asset 必须能追溯到 Source、Evidence、Parser/Generator 和 Snapshot。
- Tombstone 永久防止错误资产回流。
- 本仓库不写 Collection Canonical、IR 或客户端生成树。

## 与 Collection 的关系

~~~text
Popular-Rules-Source
        ↓
Supplemental Source Release
        ↓
Popular-Rules-Collection Source Registry / Collect
        ↓
V3 Engine
        ↓
7 Client Outputs
~~~

当前 Collection 已登记 PRS，但入口保持 disabled，直到官方-evidence-only Release 通过生产门禁。

## 文档

ARCHITECTURE.md  
OFFICIAL_SOURCE_GENERATION.md  
SERVICE_POLICY.md  
EVIDENCE_POLICY.md  
DOMAIN_POLICY.md  
IP_POLICY.md  
RELEASE_POLICY.md  
PROMOTION_CONTRACT.md  
OPERATIONS.md  
SECURITY.md  
PHASES.md  
AUDIT_2026-09-20.md  
CI_AUTOMATION.md
