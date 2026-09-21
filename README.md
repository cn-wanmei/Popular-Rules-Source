# Popular-Rules-Source

> Popular-Rules-Collection 的独立补充型 Source / Evidence Supply Layer。核心能力是从目标服务的官方来源自动提取、验证并生成可审计的域名 Source。

仓库：cn-wanmei/Popular-Rules-Source  
上游生产项目：cn-wanmei/Popular-Rules-Collection  
版本：见 VERSION

## 当前真实状态

生命周期唯一真源：`config/source_canary_state.yaml`。  
`config/services.yaml` 只保存静态服务定义；历史 `config/phase2_service_completion.yaml` 已废弃，派生状态写入 `reports/generated/phase2_service_completion.json`。

<!-- SOURCE_STATUS:START -->
### Source lifecycle (generated)

| Service | Lifecycle | Release | Domains | Snapshot |
|---|---|---|---:|---|
| 1688 | **PRODUCTION** | CANDIDATE | 3 | snap-1688-b48b14f407530d49052090e7 |
| cainiao | **PRODUCTION** | CANDIDATE | 1 | snap-cainiao-f98c960e71406bdad7f6f2aa |
| dingding | **PRODUCTION** | CANDIDATE | 6 | snap-dingding-a8d439dd579c51318213ff4d |
| qqmail | **PRODUCTION** | CANDIDATE | 1 | snap-qqmail-e18e92f661d4032c002d436c |
| qqmusic | **PRODUCTION** | CANDIDATE | 1 | snap-qqmusic-e903c9a62ef0a67f01a7d15d |
| taobao | **VERIFIED** | CANDIDATE | 14 | snap-taobao-f4c1d298c6aec90f470a3681 |
| tencentcloud | **PRODUCTION** | CANDIDATE | 1 | snap-tencentcloud-b971976c1cdd15a737dcc2c1 |
| tmall | **VERIFIED** | CANDIDATE | 8 | snap-tmall-e789778d5553d7ddf454595c |
<!-- SOURCE_STATUS:END -->
### 三层平台能力

P0：Gap Engine 对 Collection Canonical 与 Source Snapshot 做域名级 diff，并把 Candidate、Evidence、Release Blocker 串成一条可审计链。

P0：Generate → Evidence Gate → Durable Release → Immutable Seal → Collection Auto-Handoff PR；Collection 仍保留自己的 Source Gate、Canary、Production Gate。

P1：Source Adapter Plugin Contract 已提供 official_web、official_json、official_api、official_manifest、official_sdk、official_browser 接口；默认只有 official_web 启用。

P1：content_digest、evidence_digest、policy_digest、generator_digest 独立计算，最终 release_digest 由四者确定，旧 immutable snapshot 永不覆盖。

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
