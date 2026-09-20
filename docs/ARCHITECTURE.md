# Architecture — Popular-Rules-Source

## Role

Popular-Rules-Source 是 Popular-Rules-Collection 的 Supplemental Source / Evidence Supply Layer。

它负责 Source 侧的采集、证据、边界、材料化、Snapshot 与 Release Candidate；不负责 Collection Canonical、Semantic IR、V3 Runtime、客户端 Adapter 和最终发布树。

## Invariant

~~~text
Source ≠ Canonical ≠ Runtime ≠ Generated
~~~

## Pipeline

~~~text
Official Source
      ↓
Fetch / Raw Hash
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
Diff / Conflict
      ↓
Immutable Snapshot
      ↓
Release Candidate
      ↓
Collection Reconciliation
~~~

## Source authority

Authority、source method、evidence strength、service ownership、classification 五个维度独立维护。

“官方网页出现过某 Host”不等于“该 Host 属于目标服务”。

## Materialization

只有 service classification 可以进入服务域名 Source。

shared、external_dependency、provider、infrastructure、unknown、candidate 均不能直接进入 Production。

## Authoring 与生成

authoring 是人工输入。  
generated/source 是构建输出。  
Seed-only 结果必须为 REVIEW。

## Snapshot

Snapshot ID 由内容摘要决定；运行时间只是元数据。

已经存在的 Snapshot 不允许覆写。

## Collection Integration

~~~text
Popular-Rules-Source
        ↓
Immutable Source Release
        ↓
Popular-Rules-Collection
        ↓
V3 Collection / Canonical / IR
        ↓
7 Clients
~~~

当前 Collection 中 PRS Source Registry 入口保持 disabled，直到官方-evidence-only Source Release 通过 Reconciliation 和 Production Gate。

## Forbidden

- 猜域名 / IP
- ASN → Product 直接归属
- CDN → Product 直接归属
- Fixture → Production
- 一次 Fetch 失败自动删源
- 修改已发布 Snapshot
- 直接写 Collection Canonical
