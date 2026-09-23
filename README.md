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
| applemedia | **VERIFIED** | CANDIDATE | 52 | snap-applemedia-66f80c88e1491611ceed3131 |
| applemusic | **VERIFIED** | CANDIDATE | 9 | snap-applemusic-3b672c7c1ed52f0df7b897fa |
| applenews | **VERIFIED** | CANDIDATE | 2 | snap-applenews-d79f669856813f2232441a1f |
| appletv | **REVIEW** | NO_SNAPSHOT | 0 | none |
| appstore | **VERIFIED** | CANDIDATE | 2 | snap-appstore-ad9887965cf7199654327dde |
| azure | **VERIFIED** | NO_SNAPSHOT | 0 | none |
| baidu | **VERIFIED** | CANDIDATE | 251 | snap-baidu-12cb314a6f44baee71c49056 |
| baidunetdisk | **REVIEW** | CANDIDATE | 2 | snap-baidunetdisk-0a8e64e56c03019bef5f6c1e |
| baidutieba | **VERIFIED** | CANDIDATE | 32 | snap-baidutieba-4d29b0251917fe7adfa58912 |
| bing | **VERIFIED** | CANDIDATE | 9 | snap-bing-ca4ee0da4665d61b81b670a6 |
| cainiao | **PRODUCTION** | CANDIDATE | 1 | snap-cainiao-9c79bba6516f87de3d163407 |
| claude | **VERIFIED** | CANDIDATE | 3 | snap-claude-5761d575bc1cb9a1c2c52cd1 |
| copilot | **VERIFIED** | CANDIDATE | 45 | snap-copilot-faa83bc25fd7cfe3613e5095 |
| deepseek | **REVIEW** | CANDIDATE | 2 | snap-deepseek-e74c191a25236d73593d589b |
| dingding | **PRODUCTION** | CANDIDATE | 6 | snap-dingding-e4c0f3c3b4e57308277a22db |
| discord | **VERIFIED** | CANDIDATE | 28 | snap-discord-d107dd92c46855cd62787064 |
| doubao | **REVIEW** | CANDIDATE | 4 | snap-doubao-9a5b57cdb4a46ae1210f2e4b |
| douyin | **VERIFIED** | NO_SNAPSHOT | 0 | none |
| feishu | **VERIFIED** | NO_SNAPSHOT | 0 | none |
| findmy | **VERIFIED** | NO_SNAPSHOT | 0 | none |
| firebase | **REVIEW** | CANDIDATE | 2 | snap-firebase-888fcde17bd4c384a1f0eac1 |
| gemini | **VERIFIED** | CANDIDATE | 9 | snap-gemini-15a1d7df0f1f42afaab98eba |
| github | **REVIEW** | NO_SNAPSHOT | 0 | none |
| googlecloud | **REVIEW** | CANDIDATE | 5 | snap-googlecloud-13cf610100c06a4ea5b42d73 |
| googledrive | **VERIFIED** | CANDIDATE | 4 | snap-googledrive-02103e6fb8fc4685d8e65a7a |
| googlefcm | **REVIEW** | NO_SNAPSHOT | 0 | none |
| groq | **REVIEW** | CANDIDATE | 1 | snap-groq-c073c7adcd8f0db5ebe9a92a |
| honorofkings_cn | **REVIEW** | CANDIDATE | 1 | snap-honorofkings_cn-57adb02773f5157159b68a91 |
| honorofkings_global | **REVIEW** | CANDIDATE | 2 | snap-honorofkings_global-fe8b3504fe8ce38843ef7009 |
| huggingface | **REVIEW** | CANDIDATE | 3 | snap-huggingface-c41977bf6c8dade8b423273a |
| icloud | **VERIFIED** | CANDIDATE | 60 | snap-icloud-6a7847125f008375cb98e14c |
| messenger | **REVIEW** | CANDIDATE | 4 | snap-messenger-0a0d45654f4b394bb85deabf |
| neteasemail | **REVIEW** | NO_SNAPSHOT | 0 | none |
| neteasemusic | **VERIFIED** | NO_SNAPSHOT | 0 | none |
| netflix | **VERIFIED** | CANDIDATE | 31 | snap-netflix-44c03024f97a209b65b001f1 |
| onedrive | **VERIFIED** | CANDIDATE | 13 | snap-onedrive-fbc5932baea8147fd7425b85 |
| openai | **VERIFIED** | CANDIDATE | 31 | snap-openai-959bece38ef894600083c410 |
| perplexity | **REVIEW** | CANDIDATE | 4 | snap-perplexity-5843c1ce73203b9d968be9fc |
| qq | **REVIEW** | CANDIDATE | 15 | snap-qq-42284c05d41505b9e118a7f1 |
| qqmail | **PRODUCTION** | CANDIDATE | 1 | snap-qqmail-0f8103b3188739c880f10aff |
| qqmusic | **PRODUCTION** | CANDIDATE | 1 | snap-qqmusic-7c0a2fae200d3fbbec51a4a3 |
| roblox | **REVIEW** | CANDIDATE | 47 | snap-roblox-36d3732a073e69dc0d883708 |
| signal | **REVIEW** | CANDIDATE | 8 | snap-signal-82644ff2cbaddc4da87ede48 |
| siri | **REVIEW** | NO_SNAPSHOT | 0 | none |
| taobao | **VERIFIED** | CANDIDATE | 14 | snap-taobao-1e6d38ed82f9483e344a3181 |
| teams | **VERIFIED** | CANDIDATE | 4 | snap-teams-6229a157b04da9c33c785d2f |
| telegram | **VERIFIED** | CANDIDATE | 24 | snap-telegram-6160beb35201b697571d9973 |
| tencentcloud | **PRODUCTION** | CANDIDATE | 1 | snap-tencentcloud-621d7e757e9f59085c87f2ce |
| tencentmeeting | **REVIEW** | CANDIDATE | 3 | snap-tencentmeeting-8854ae3be565c11d5a877850 |
| tencentvideo | **REVIEW** | NO_SNAPSHOT | 0 | none |
| testflight | **VERIFIED** | CANDIDATE | 2 | snap-testflight-aef28e222598764f34a5f052 |
| tiktok | **VERIFIED** | CANDIDATE | 29 | snap-tiktok-5e3d1c0ed7550d26495f0f24 |
| tmall | **VERIFIED** | CANDIDATE | 8 | snap-tmall-6c5457a183ccb42575023864 |
| wechat | **VERIFIED** | CANDIDATE | 28 | snap-wechat-fe8dc34d271a68b11a79ae3f |
| wecom | **REVIEW** | CANDIDATE | 3 | snap-wecom-b0be7ae90ea2a66d6fe083c0 |
| xbox | **REVIEW** | NO_SNAPSHOT | 0 | none |
| youdao | **REVIEW** | CANDIDATE | 15 | snap-youdao-b0e2b0246cd52df7418f5c14 |
| youtube | **REVIEW** | NO_SNAPSHOT | 0 | none |
| youtubemusic | **VERIFIED** | CANDIDATE | 1 | snap-youtubemusic-56acd7f93290f648cbc4c5ca |
<!-- SOURCE_STATUS:END -->
