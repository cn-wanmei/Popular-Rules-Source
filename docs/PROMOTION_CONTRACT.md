# Promotion Contract

## Flow

~~~text
Popular-Rules-Source
        ↓
Immutable Source Release
        ↓
Popular-Rules-Collection Source Registry / Collect
        ↓
V3 Engine
        ↓
7 client outputs
~~~

PRS 不直接写 Collection Canonical、IR 或 generated client tree。

## Current

Collection 已登记 PRS Source，但当前入口为 disabled。

原因：PRS 当前首批服务仍存在 Authoring Seed 候选，尚未完成 official-evidence-only Production Gate。

## Promotion Gate

必须：

- Schema PASS
- Official Evidence PASS
- Ownership PASS
- Boundary PASS
- Exclusion PASS
- Duplicate PASS
- Conflict = 0
- Deterministic PASS
- Reconciliation PASS

## Contract Version

Source Release schema 破坏性变更需要 MAJOR 版本。

Source Repo 与 Collection Adapter 必须协调升级。
