# Phase 2 — Official Source Production Completion

## Objective

把第一阶段的“Source Engine 可运行”推进到第二阶段的“按 Service 独立进入正常生产”。

不追求一次性把 8 个服务全部标记 Production，而是建立统一的、可复制的服务补全框架。

## Parallel Workstreams

### A. Source Engine
Live official fetch、Parser、Normalize、Allow/Exclusion、Evidence、Conflict、Snapshot、Determinism、Release。

### B. Service Completion
每个 Service 建立独立 profile：

~~~text
service_id
official_sources
source_method
allow_policy
negative_evidence
expected_scope
known_shared_infra
reconciliation_target
~~~

### C. Gap Discovery
缺失规则补全顺序：

~~~text
Official source
  ↓
Official docs / API / SDK / manifest
  ↓
Controlled discovery
  ↓
Evidence verification
  ↓
Materialization
~~~

第三方规则只能交叉参考。

### D. Collection Integration
PRS Release → Collection Registry → Collect → V3 Engine。

### E. QA
Schema、Evidence、Boundary、Exclusion、Conflict、Count Drift、Determinism、Reconciliation、Collection V3、7-client semantic。

## Service Matrix

| Service | Initial | Gate |
|---|---|---|
| 1688 | REVIEW | official evidence only + Alibaba boundary |
| cainiao | REVIEW | logistics-only boundary |
| dingding | REVIEW | official open-platform evidence |
| qqmail | REVIEW | exact mail endpoints |
| qqmusic | REVIEW | music scope + CDN exclusion |
| taobao | REVIEW | official platform/API evidence |
| tencentcloud | PARTIAL | supplement existing Collection |
| tmall | REVIEW | official business/open evidence |

## Production Qualification

~~~text
Candidate
  ↓
Verified
  ↓
Immutable Snapshot
  ↓
Reconciliation PASS
  ↓
Collection V3 PASS
  ↓
Canary
  ↓
Production
~~~

Seed-only assets cannot pass Production.

## Parallel implementation

服务可以并行开发；生产 Gate 必须服务级独立。

一个服务失败不能污染其他服务，也不能降低其他服务的证据标准。

## Phase 2 Exit

- 首个 official-evidence-only Release
- Source ↔ Collection Reconciliation 稳定
- 正常 V3 Build 成功
- 7-client semantic pass
- observation window 启动
- canary activation 可回滚

“8/8 PUBLISHED”不是唯一 Exit 条件。

## No-go

Fixture→Production、Seed→Production、批量强推、绕过 Collection Gate、直接覆盖 main。
