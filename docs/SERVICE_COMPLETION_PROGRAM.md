# Service Completion Program (P0A/P0B/P0C/P1/P2)

本文件是执行方案在 Source 仓库中的落地索引。原则是：上游无专用服务规则时，由 Popular-Rules-Source 直接建立独立服务 candidate，证据仍必须来自官方来源或明确允许的高可信来源；candidate 不等于 production。

## Lineage Lock

`qqmail → qqmusic → taobao → tencentcloud → tmall`

历史 Snapshot/Release 不改写、不回算覆盖；新内容只创建新 immutable identity。

## Current execution layers

- P0-A：既有 lineage 闭环。
- P0-B：Source 已有服务的新 current-lineage materialization，必要时 self-built fallback。
- P0-C：Google / Microsoft / Apple 官方产品目录 ↔ 独立 hostname ↔ Source evidence reconciliation。
- P1：国内核心集团服务树。
- P2：海外 SaaS / AI / Cloud / Payments 服务树。

## Self-built rule policy

`self_built/*/domains.list` 仅表示当前候选规则资产；只有通过官方 evidence、deterministic snapshot、semantic/overlap、seven-client、Collection canary 后才能进入 Production。

## Current official verification

Google Workspace 官方学习中心明确列出 Calendar、Chat、Contacts、Docs、Drive、Forms、Gmail、Groups、Meet、Sheets、Sites、Slides、Vids、Workspace Studio 的独立浏览器入口。Microsoft 统一 cloud.microsoft 文档确认该域用于用户面向 Microsoft SaaS 体验，并列举 Word、Excel、PowerPoint、Outlook、OneNote、Planner、Loop、Mesh 等产品。Apple 官方 Services / 产品页明确展示 Apple Podcasts、Books、Maps 等服务。

