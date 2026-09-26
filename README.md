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
| 1688 | **PRODUCTION** | CANDIDATE | 2 | snap-1688-954c3b4b2e56716d074be878 |
| alibabacloud | **REVIEW** | CANDIDATE | 12 | snap-alibabacloud-461ca160d076aaffa913407c |
| appledev | **VERIFIED** | CANDIDATE | 38 | snap-appledev-0f9aebbb855d26eaea22e764 |
| applemedia | **VERIFIED** | CANDIDATE | 52 | snap-applemedia-31ff5d9442c181964b8f3d56 |
| applemusic | **VERIFIED** | CANDIDATE | 9 | snap-applemusic-4ee97f97c6f22ef5c36b6c8a |
| applenews | **VERIFIED** | CANDIDATE | 2 | snap-applenews-07e74bbd3fe8e9d1e9ebbe8d |
| appletv | **REVIEW** | CANDIDATE | 7 | snap-appletv-36044ac0ef189622fcd1c9bd |
| appstore | **VERIFIED** | CANDIDATE | 2 | snap-appstore-4d616cf91c8481511685c580 |
| azure | **VERIFIED** | CANDIDATE | 149 | snap-azure-1272a5f03d5d3e7c4fa32ba5 |
| baidu | **VERIFIED** | CANDIDATE | 251 | snap-baidu-2ac63201e603702a873e8313 |
| baidunetdisk | **REVIEW** | CANDIDATE | 2 | snap-baidunetdisk-0d9bcb5a5362097ed3bf61c9 |
| baidutieba | **VERIFIED** | CANDIDATE | 32 | snap-baidutieba-8b4d600c509ceac6efde41b2 |
| bing | **VERIFIED** | CANDIDATE | 9 | snap-bing-2a7e85faeb2c486827a45b4e |
| cainiao | **PRODUCTION** | CANDIDATE | 1 | snap-cainiao-6fb6742fb29460ba81c778ea |
| claude | **VERIFIED** | CANDIDATE | 3 | snap-claude-29e8c63e592f1f2898514fd7 |
| copilot | **VERIFIED** | CANDIDATE | 45 | snap-copilot-ced3ecb233dd43400f0485e9 |
| deepseek | **REVIEW** | CANDIDATE | 2 | snap-deepseek-e74c191a25236d73593d589b |
| dingding | **PRODUCTION** | CANDIDATE | 3 | snap-dingding-b3ed8aa626ef40fbdcd7f27d |
| discord | **VERIFIED** | CANDIDATE | 28 | snap-discord-82f6a47f92e47ffa9d0382d6 |
| doubao | **REVIEW** | CANDIDATE | 4 | snap-doubao-83627a3a7eb8c73da79a8cb4 |
| douyin | **VERIFIED** | CANDIDATE | 13 | snap-douyin-d70de7165afed60394f679be |
| feishu | **VERIFIED** | CANDIDATE | 43 | snap-feishu-774ba504c00dc3a9c58bb77b |
| findmy | **VERIFIED** | CANDIDATE | 3 | snap-findmy-685aad71cf0c0a95171921de |
| firebase | **REVIEW** | CANDIDATE | 2 | snap-firebase-687d093cfbb05c60602d8c99 |
| gemini | **VERIFIED** | CANDIDATE | 9 | snap-gemini-b808a3bfa09f41603d94ed24 |
| github | **REVIEW** | CANDIDATE | 29 | snap-github-995bb5798306780932ce16f1 |
| googlecloud | **REVIEW** | CANDIDATE | 5 | snap-googlecloud-7ac90cbe3331f1a7d9668755 |
| googledrive | **VERIFIED** | CANDIDATE | 4 | snap-googledrive-cee3bfde150a7392cd48a8d2 |
| googlefcm | **REVIEW** | CANDIDATE | 13 | snap-googlefcm-0a56c2f6cc053405abb62c45 |
| groq | **REVIEW** | CANDIDATE | 1 | snap-groq-c073c7adcd8f0db5ebe9a92a |
| honorofkings_cn | **REVIEW** | CANDIDATE | 1 | snap-honorofkings_cn-6ca30c9dd7548b0ceb1c9482 |
| honorofkings_global | **REVIEW** | CANDIDATE | 2 | snap-honorofkings_global-93adcb6eadecef0136b16c7d |
| huggingface | **REVIEW** | CANDIDATE | 3 | snap-huggingface-c41977bf6c8dade8b423273a |
| icloud | **VERIFIED** | CANDIDATE | 58 | snap-icloud-838b1fbabbc13b04097f7eb1 |
| messenger | **REVIEW** | CANDIDATE | 4 | snap-messenger-0a0d45654f4b394bb85deabf |
| neteasemail | **REVIEW** | CANDIDATE | 3 | snap-neteasemail-817c44ccb4b6b36d7b108a88 |
| neteasemusic | **VERIFIED** | CANDIDATE | 10 | snap-neteasemusic-e44060214727df2dca508867 |
| netflix | **VERIFIED** | CANDIDATE | 31 | snap-netflix-7b3e54dbc15daa952dcaef2f |
| onedrive | **VERIFIED** | CANDIDATE | 13 | snap-onedrive-b589d8dadd9f13403d7ae305 |
| openai | **VERIFIED** | CANDIDATE | 31 | snap-openai-3daa3b2eaf413566b57c5538 |
| perplexity | **REVIEW** | CANDIDATE | 4 | snap-perplexity-5843c1ce73203b9d968be9fc |
| qq | **REVIEW** | REVIEW | 1 | snap-qq-73cd58e3f219de9a16769f91 |
| qqmail | **PRODUCTION** | CANDIDATE | 1 | snap-qqmail-6b294a6a56c74356d45a8983 |
| qqmusic | **PRODUCTION** | CANDIDATE | 1 | snap-qqmusic-144f8b8b6ac75b2d1e5cd045 |
| roblox | **REVIEW** | CANDIDATE | 47 | snap-roblox-36d3732a073e69dc0d883708 |
| signal | **REVIEW** | CANDIDATE | 8 | snap-signal-82644ff2cbaddc4da87ede48 |
| siri | **REVIEW** | CANDIDATE | 1 | snap-siri-47e2e3f224b653abe0a7da30 |
| taobao | **VERIFIED** | REVIEW | 1 | snap-taobao-9d9ea3dd71d0ef067dd7c6a1 |
| teams | **VERIFIED** | CANDIDATE | 4 | snap-teams-6aa385077c2e25e0bd158160 |
| telegram | **VERIFIED** | CANDIDATE | 24 | snap-telegram-e985d44adc6d0a592feff2e5 |
| tencentcloud | **PRODUCTION** | CANDIDATE | 1 | snap-tencentcloud-99be32d627feeda81e8555b9 |
| tencentmeeting | **REVIEW** | CANDIDATE | 3 | snap-tencentmeeting-b860ac733a4552e89e1ef88e |
| tencentvideo | **REVIEW** | CANDIDATE | 17 | snap-tencentvideo-0f255bfc922db6125299fcbf |
| testflight | **VERIFIED** | CANDIDATE | 2 | snap-testflight-29c5632a2668a3c10290338d |
| tiktok | **VERIFIED** | CANDIDATE | 29 | snap-tiktok-df0d82d481b22c2cbe3c5905 |
| tmall | **VERIFIED** | CANDIDATE | 8 | snap-tmall-e874413d8245a8df0eb4b75e |
| wechat | **VERIFIED** | CANDIDATE | 28 | snap-wechat-472d929bbfb735e852d4cb83 |
| wecom | **REVIEW** | CANDIDATE | 3 | snap-wecom-ff81022ae1599758656ebf1c |
| xbox | **REVIEW** | CANDIDATE | 42 | snap-xbox-be1a85faaec0bb69f03aae37 |
| youdao | **REVIEW** | CANDIDATE | 15 | snap-youdao-45f37817f90d1ea214d4b881 |
| youtube | **REVIEW** | CANDIDATE | 175 | snap-youtube-ea6794cdfc9366447a0922c2 |
| youtubemusic | **VERIFIED** | CANDIDATE | 1 | snap-youtubemusic-4af31e7577631d296a0eea49 |
<!-- SOURCE_STATUS:END -->
