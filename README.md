# Popular-Rules-Source

> Popular-Rules-Collection 的官方证据补全平台（Evidence Supply Layer）。负责官方来源发现、证据化、Gap Detection、Repair、Snapshot、Release、Immutable Seal，并把可消费的完整 provenance 交给 Collection。

## Platform status

Source Platform 三层能力已经进入可运行生产形态：

| Layer | Status |
|---|---|
| P0 Gap Engine | ✅ |
| P0 Lifecycle SSOT | ✅ |
| P0 Repair | ✅ |
| P0 Durable Release / Immutable Seal | ✅ |
| P1 Provenance v2 | ✅ |
| P1 Adapter Contract | ✅ |
| P1 Browser / JS architecture | ✅ |
| P1 Retry / Health | ✅ |
| Collection Auto Handoff | ✅ Collection-owned |
| Cross-repo secret | ✅ removed |

Lifecycle SSOT 是 `config/source_canary_state.yaml`；`config/services.yaml` 只保存静态 Service Definition；旧 `phase2_service_completion.yaml` 已移除/不再作为生命周期数据库。

## Source service lifecycle

Source lifecycle 只描述 Source 自身证据/Release 资格，不等同于 Collection 的最终 Production 发布状态。Collection 的 Canary、Production、Observation 与最终消费绑定仍由 Collection 负责。

| Service | Source lifecycle |
|---|---|
| 1688 | production |
| cainiao | production |
| dingding | production |
| qqmail | production |
| qqmusic | production |
| taobao | verified → awaiting Collection canary |
| tencentcloud | production |
| tmall | verified → awaiting Collection canary |

## Gap Engine

    Collection current state
            ↓
    Source current snapshot
            ↓
    official source evidence
            ↓
    Candidate / Evidence completeness
            ↓
    Release blockers
            ↓
    recommended repair action

CLI：

    python -m source_engine gap --service taobao
    python -m source_engine gap --service qqmusic
    python -m source_engine repair --service taobao --domain example.taobao.com

Gap 报告必须能回答：当前 Collection 缺什么、Source 有没有、官方源是否发现、Candidate 是否存在、Evidence 是否完整、为什么没进 Release。

## Immutable identity

Source Release 使用四层 provenance digest：

    content_digest
    evidence_digest
    policy_digest
    generator_digest

最终：

    release_digest = identity(content, evidence, policy, generator)

老 Snapshot/Release 永不覆写。相同 identity 重跑必须复用；provenance 变化必须产生新的 immutable identity。

## Release and Collection handoff

    Official Refresh
        ↓
    Gap Detection / Generate / Repair
        ↓
    Candidate Snapshot
        ↓
    Evidence Gate
        ↓
    Durable Release
        ↓
    Immutable Seal
        ↓
    Collection-owned Auto Handoff PR
        ↓
    Collection Source Gate → Canary → Production

Source 不直接写 Collection Canonical、IR 或最终客户端目录。

## CLI

    python -m source_engine validate
    python -m source_engine gap --service taobao
    python -m source_engine generate --service taobao
    python -m source_engine repair --service taobao
    python -m source_engine release --service taobao
    python -m source_engine reconcile
    python -m source_engine health
    python -m source_engine qualify
    pytest -q

## Production invariants

- 官方证据优先，不猜 Service Ownership。
- Provider / ASN / CDN 不能直接转化为 Product Service。
- Fetch 失败不能用空结果覆盖 Last Known Good。
- Candidate 无完整 Evidence 不能进入 Release。
- Snapshot / Release immutable。
- Collection 绑定必须 exact SHA + exact provenance equality。
- 跨仓库自动交接由 Collection 持有，不依赖跨仓库 Secret。

## Upstream relationship

Popular-Rules-Collection 是唯一最终发布仓库。Source 只提供 Supplemental Source / Evidence Supply。

<!-- SOURCE_STATUS:START -->
### Source lifecycle (generated)

| Service | Lifecycle | Release | Domains | Snapshot |
|---|---|---|---:|---|
| 1688 | **PRODUCTION** | CANDIDATE | 3 | snap-1688-39272fe7087048097f0c13f9 |
| alibabacloud | **REVIEW** | CANDIDATE | 12 | snap-alibabacloud-461ca160d076aaffa913407c |
| appledev | **VERIFIED** | NO_SNAPSHOT | 0 | none |
| applemusic | **VERIFIED** | NO_SNAPSHOT | 0 | none |
| appletv | **REVIEW** | NO_SNAPSHOT | 0 | none |
| appstore | **VERIFIED** | NO_SNAPSHOT | 0 | none |
| azure | **VERIFIED** | NO_SNAPSHOT | 0 | none |
| baidunetdisk | **REVIEW** | CANDIDATE | 2 | snap-baidunetdisk-0a8e64e56c03019bef5f6c1e |
| baidutieba | **VERIFIED** | NO_SNAPSHOT | 0 | none |
| cainiao | **PRODUCTION** | CANDIDATE | 1 | snap-cainiao-9c79bba6516f87de3d163407 |
| deepseek | **REVIEW** | CANDIDATE | 2 | snap-deepseek-e74c191a25236d73593d589b |
| dingding | **PRODUCTION** | CANDIDATE | 6 | snap-dingding-e4c0f3c3b4e57308277a22db |
| doubao | **REVIEW** | CANDIDATE | 4 | snap-doubao-9a5b57cdb4a46ae1210f2e4b |
| douyin | **VERIFIED** | NO_SNAPSHOT | 0 | none |
| feishu | **VERIFIED** | NO_SNAPSHOT | 0 | none |
| findmy | **VERIFIED** | NO_SNAPSHOT | 0 | none |
| firebase | **REVIEW** | CANDIDATE | 2 | snap-firebase-888fcde17bd4c384a1f0eac1 |
| github | **REVIEW** | NO_SNAPSHOT | 0 | none |
| googlecloud | **REVIEW** | CANDIDATE | 5 | snap-googlecloud-13cf610100c06a4ea5b42d73 |
| googledrive | **VERIFIED** | NO_SNAPSHOT | 0 | none |
| googlefcm | **REVIEW** | NO_SNAPSHOT | 0 | none |
| groq | **REVIEW** | CANDIDATE | 1 | snap-groq-c073c7adcd8f0db5ebe9a92a |
| huggingface | **REVIEW** | CANDIDATE | 3 | snap-huggingface-c41977bf6c8dade8b423273a |
| icloud | **VERIFIED** | NO_SNAPSHOT | 0 | none |
| messenger | **REVIEW** | CANDIDATE | 4 | snap-messenger-0a0d45654f4b394bb85deabf |
| neteasemusic | **VERIFIED** | NO_SNAPSHOT | 0 | none |
| onedrive | **VERIFIED** | NO_SNAPSHOT | 0 | none |
| perplexity | **REVIEW** | CANDIDATE | 4 | snap-perplexity-5843c1ce73203b9d968be9fc |
| qq | **REVIEW** | NO_SNAPSHOT | 0 | none |
| qqmail | **PRODUCTION** | CANDIDATE | 1 | snap-qqmail-0f8103b3188739c880f10aff |
| qqmusic | **PRODUCTION** | CANDIDATE | 1 | snap-qqmusic-7c0a2fae200d3fbbec51a4a3 |
| roblox | **REVIEW** | CANDIDATE | 47 | snap-roblox-36d3732a073e69dc0d883708 |
| signal | **REVIEW** | CANDIDATE | 8 | snap-signal-82644ff2cbaddc4da87ede48 |
| siri | **REVIEW** | NO_SNAPSHOT | 0 | none |
| taobao | **VERIFIED** | CANDIDATE | 14 | snap-taobao-1e6d38ed82f9483e344a3181 |
| teams | **VERIFIED** | NO_SNAPSHOT | 0 | none |
| tencentcloud | **PRODUCTION** | CANDIDATE | 1 | snap-tencentcloud-621d7e757e9f59085c87f2ce |
| tencentmeeting | **REVIEW** | CANDIDATE | 3 | snap-tencentmeeting-8854ae3be565c11d5a877850 |
| tencentvideo | **REVIEW** | NO_SNAPSHOT | 0 | none |
| testflight | **VERIFIED** | NO_SNAPSHOT | 0 | none |
| tmall | **VERIFIED** | CANDIDATE | 8 | snap-tmall-6c5457a183ccb42575023864 |
| wechat | **VERIFIED** | NO_SNAPSHOT | 0 | none |
| wecom | **REVIEW** | CANDIDATE | 3 | snap-wecom-b0be7ae90ea2a66d6fe083c0 |
| xbox | **REVIEW** | NO_SNAPSHOT | 0 | none |
| youdao | **REVIEW** | CANDIDATE | 15 | snap-youdao-b0e2b0246cd52df7418f5c14 |
| youtube | **REVIEW** | NO_SNAPSHOT | 0 | none |
| youtubemusic | **VERIFIED** | NO_SNAPSHOT | 0 | none |
<!-- SOURCE_STATUS:END -->
