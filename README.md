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
| 1688 | **PRODUCTION** | CANDIDATE | 2 | snap-1688-13aa949cc89ef847a156ab0a |
| adobe-firefly | **REVIEW** | CANDIDATE | 1 | snap-adobe-firefly-278e98581b6f8e62e261931a |
| adobe-fonts | **REVIEW** | CANDIDATE | 1 | snap-adobe-fonts-0cfd6c78ffb842903de0152c |
| adobe-stock | **REVIEW** | CANDIDATE | 1 | snap-adobe-stock-fb5983c8b0ef609fde49e4e0 |
| alibabacloud | **REVIEW** | CANDIDATE | 12 | snap-alibabacloud-461ca160d076aaffa913407c |
| amazonmusic | **REVIEW** | CANDIDATE | 1 | snap-amazonmusic-8f36e1717aca94afda1ee0d0 |
| anthropic-claude | **REVIEW** | CANDIDATE | 1 | snap-anthropic-claude-57b3b3b1999c5d83d8f322a5 |
| anthropic-platform | **REVIEW** | CANDIDATE | 1 | snap-anthropic-platform-7bf2ee650853808906839699 |
| applebooks | **REVIEW** | NO_SNAPSHOT | 0 | none |
| appledev | **VERIFIED** | CANDIDATE | 38 | snap-appledev-69881d2207a1d8d4377f2166 |
| applemaps | **REVIEW** | NO_SNAPSHOT | 0 | none |
| applemedia | **VERIFIED** | CANDIDATE | 52 | snap-applemedia-5042d174723b9a5737d6f038 |
| applemusic | **VERIFIED** | CANDIDATE | 9 | snap-applemusic-4ee97f97c6f22ef5c36b6c8a |
| applenews | **VERIFIED** | CANDIDATE | 2 | snap-applenews-5b92e365d4fca996fc468b19 |
| applepodcasts | **REVIEW** | NO_SNAPSHOT | 0 | none |
| appletv | **REVIEW** | CANDIDATE | 7 | snap-appletv-b983ca24d850eeada428f1da |
| appstore | **VERIFIED** | CANDIDATE | 2 | snap-appstore-4d616cf91c8481511685c580 |
| audible | **REVIEW** | CANDIDATE | 1 | snap-audible-2ae1b9d59ebdc6174db597b1 |
| azure | **VERIFIED** | CANDIDATE | 149 | snap-azure-b3a73e93d99fb11dc21e4888 |
| baidu | **VERIFIED** | CANDIDATE | 251 | snap-baidu-584ae9eeb87fa1dabd00d11f |
| baidu-zhidao | **REVIEW** | NO_SNAPSHOT | 0 | none |
| baidumaps | **REVIEW** | NO_SNAPSHOT | 0 | none |
| baidunetdisk | **REVIEW** | CANDIDATE | 2 | snap-baidunetdisk-2030ef27118ea52d548a5667 |
| baidutieba | **VERIFIED** | CANDIDATE | 32 | snap-baidutieba-8b4d600c509ceac6efde41b2 |
| baiduwenku | **REVIEW** | NO_SNAPSHOT | 0 | none |
| bing | **VERIFIED** | CANDIDATE | 9 | snap-bing-3f36698777489885ba7fdbfd |
| cainiao | **PRODUCTION** | CANDIDATE | 1 | snap-cainiao-4031d28314b225751617ffbd |
| chatgpt | **REVIEW** | CANDIDATE | 1 | snap-chatgpt-cc1e48c936f2293870e7e2c0 |
| claude | **VERIFIED** | CANDIDATE | 3 | snap-claude-4aec84cea09e5629117513fa |
| copilot | **VERIFIED** | CANDIDATE | 45 | snap-copilot-9f6da111d1453ad19fc927d2 |
| deepseek | **REVIEW** | CANDIDATE | 2 | snap-deepseek-e74c191a25236d73593d589b |
| dingding | **PRODUCTION** | CANDIDATE | 3 | snap-dingding-09ae1ecd000f1688f61e99a0 |
| discord | **VERIFIED** | CANDIDATE | 28 | snap-discord-e5a47c19f5c45c25c613f6f6 |
| doubao | **REVIEW** | CANDIDATE | 4 | snap-doubao-d7cf468883541cf0629f8972 |
| douyin | **VERIFIED** | CANDIDATE | 13 | snap-douyin-3780b3c2b6ee1a9abdccf245 |
| feishu | **VERIFIED** | CANDIDATE | 43 | snap-feishu-dd8e2cd8a4ac32fa8b355226 |
| findmy | **VERIFIED** | CANDIDATE | 3 | snap-findmy-5dbfa7a125855e4ee11e3daf |
| firebase | **REVIEW** | CANDIDATE | 2 | snap-firebase-7d453ef3aa923747422290a6 |
| gemini | **VERIFIED** | CANDIDATE | 9 | snap-gemini-9e01a42e8140aafccd75f9ea |
| github | **REVIEW** | CANDIDATE | 29 | snap-github-293b2b0db400e778bcfe88a7 |
| gmail | **REVIEW** | NO_SNAPSHOT | 0 | none |
| goodreads | **REVIEW** | CANDIDATE | 1 | snap-goodreads-eb7a2c816de0efe942519ac8 |
| google-calendar | **REVIEW** | NO_SNAPSHOT | 0 | none |
| google-chat | **REVIEW** | NO_SNAPSHOT | 0 | none |
| google-contacts | **REVIEW** | NO_SNAPSHOT | 0 | none |
| google-docs | **REVIEW** | NO_SNAPSHOT | 0 | none |
| google-earth | **REVIEW** | NO_SNAPSHOT | 0 | none |
| google-forms | **REVIEW** | NO_SNAPSHOT | 0 | none |
| google-groups | **REVIEW** | NO_SNAPSHOT | 0 | none |
| google-maps | **REVIEW** | NO_SNAPSHOT | 0 | none |
| google-meet | **REVIEW** | NO_SNAPSHOT | 0 | none |
| google-news | **REVIEW** | NO_SNAPSHOT | 0 | none |
| google-photos | **REVIEW** | NO_SNAPSHOT | 0 | none |
| google-play | **REVIEW** | NO_SNAPSHOT | 0 | none |
| google-sheets | **REVIEW** | NO_SNAPSHOT | 0 | none |
| google-sites | **REVIEW** | NO_SNAPSHOT | 0 | none |
| google-slides | **REVIEW** | NO_SNAPSHOT | 0 | none |
| google-vids | **REVIEW** | NO_SNAPSHOT | 0 | none |
| google-voice | **REVIEW** | NO_SNAPSHOT | 0 | none |
| google-workspace-studio | **REVIEW** | NO_SNAPSHOT | 0 | none |
| googlecloud | **REVIEW** | CANDIDATE | 5 | snap-googlecloud-9d8b487a6027d62cad21ad43 |
| googledrive | **VERIFIED** | CANDIDATE | 4 | snap-googledrive-cee3bfde150a7392cd48a8d2 |
| googlefcm | **REVIEW** | CANDIDATE | 13 | snap-googlefcm-d2649b705a9906c0296cdbaf |
| groq | **REVIEW** | CANDIDATE | 1 | snap-groq-c073c7adcd8f0db5ebe9a92a |
| honorofkings_cn | **REVIEW** | CANDIDATE | 1 | snap-honorofkings_cn-a804aed53545aac4f58d34d8 |
| honorofkings_global | **REVIEW** | CANDIDATE | 2 | snap-honorofkings_global-9271ce0b7c8d6b9d6d1836fa |
| huawei-appgallery | **REVIEW** | NO_SNAPSHOT | 0 | none |
| huawei-cloud | **REVIEW** | CANDIDATE | 1 | snap-huawei-cloud-baad7d83f4093ace2f04705c |
| huggingface | **REVIEW** | CANDIDATE | 3 | snap-huggingface-c41977bf6c8dade8b423273a |
| icloud | **VERIFIED** | CANDIDATE | 58 | snap-icloud-838b1fbabbc13b04097f7eb1 |
| jd-cloud | **REVIEW** | CANDIDATE | 1 | snap-jd-cloud-7364b0a4c509c49727621c40 |
| kuaishou | **REVIEW** | NO_SNAPSHOT | 0 | none |
| kuaishou-open | **REVIEW** | NO_SNAPSHOT | 0 | none |
| kugou | **REVIEW** | CANDIDATE | 1 | snap-kugou-bd7700e11c8ff2c07e7b9321 |
| kuwo | **REVIEW** | CANDIDATE | 1 | snap-kuwo-c36f7d9497fdd5e0b0806d93 |
| messenger | **REVIEW** | CANDIDATE | 4 | snap-messenger-b3b52c8322960d4f19279550 |
| mi-cloud | **REVIEW** | CANDIDATE | 1 | snap-mi-cloud-e876da13d4a50a1abf1ddb7a |
| ms365-excel | **REVIEW** | NO_SNAPSHOT | 0 | none |
| ms365-loop | **REVIEW** | NO_SNAPSHOT | 0 | none |
| ms365-mesh | **REVIEW** | NO_SNAPSHOT | 0 | none |
| ms365-onenote | **REVIEW** | NO_SNAPSHOT | 0 | none |
| ms365-planner | **REVIEW** | NO_SNAPSHOT | 0 | none |
| ms365-powerpoint | **REVIEW** | NO_SNAPSHOT | 0 | none |
| ms365-word | **REVIEW** | NO_SNAPSHOT | 0 | none |
| neteasemail | **REVIEW** | CANDIDATE | 3 | snap-neteasemail-8f25db6f713ea62f08bd565b |
| neteasemusic | **VERIFIED** | CANDIDATE | 10 | snap-neteasemusic-34efc854219f96a2aa121d84 |
| netflix | **VERIFIED** | CANDIDATE | 31 | snap-netflix-5b2876cf88dc642c06b22d35 |
| onedrive | **VERIFIED** | CANDIDATE | 13 | snap-onedrive-b589d8dadd9f13403d7ae305 |
| openai | **VERIFIED** | CANDIDATE | 31 | snap-openai-cda1ed8e109c4abd8bf521dd |
| openai-api | **REVIEW** | CANDIDATE | 1 | snap-openai-api-c8952ba8249663ca6f49098d |
| openai-platform | **REVIEW** | CANDIDATE | 1 | snap-openai-platform-769b5880b0899016f4335a85 |
| perplexity | **REVIEW** | CANDIDATE | 4 | snap-perplexity-5843c1ce73203b9d968be9fc |
| qq | **REVIEW** | REVIEW | 1 | snap-qq-e8b755c0889d871584191efb |
| qqmail | **PRODUCTION** | CANDIDATE | 1 | snap-qqmail-013babbee1bf9cf46a1741a1 |
| qqmusic | **PRODUCTION** | CANDIDATE | 1 | snap-qqmusic-421df9f4465ad7fb35ed9c06 |
| quanmin-k-ge | **REVIEW** | CANDIDATE | 1 | snap-quanmin-k-ge-00c1b63526a1b67c5f490aaf |
| roblox | **REVIEW** | CANDIDATE | 47 | snap-roblox-36d3732a073e69dc0d883708 |
| signal | **REVIEW** | CANDIDATE | 8 | snap-signal-82644ff2cbaddc4da87ede48 |
| siri | **REVIEW** | CANDIDATE | 1 | snap-siri-440b4c5a63d59b410d5e32fa |
| stripe-dashboard | **REVIEW** | CANDIDATE | 1 | snap-stripe-dashboard-e5667382cb3f12c246ad8660 |
| taobao | **VERIFIED** | REVIEW | 1 | snap-taobao-05620e1ac2b0ac7b838b0baa |
| teams | **VERIFIED** | CANDIDATE | 4 | snap-teams-6aa385077c2e25e0bd158160 |
| telegram | **VERIFIED** | CANDIDATE | 24 | snap-telegram-ae2063026508ed946661df66 |
| tencentcloud | **PRODUCTION** | CANDIDATE | 1 | snap-tencentcloud-ade52617c57ff6a0f637ff2b |
| tencentmeeting | **REVIEW** | CANDIDATE | 3 | snap-tencentmeeting-19826cb5a6a9fb912f7be3fc |
| tencentvideo | **REVIEW** | CANDIDATE | 17 | snap-tencentvideo-0bbc97349dbece8ea2628b3f |
| testflight | **VERIFIED** | CANDIDATE | 2 | snap-testflight-29c5632a2668a3c10290338d |
| tiktok | **VERIFIED** | CANDIDATE | 29 | snap-tiktok-d7c408670d9f72fda616937c |
| tmall | **VERIFIED** | CANDIDATE | 8 | snap-tmall-68de325c52bf9461941f66d5 |
| venmo | **REVIEW** | CANDIDATE | 1 | snap-venmo-ad97a6f5008ebab004dbad8a |
| wechat | **VERIFIED** | CANDIDATE | 28 | snap-wechat-472d929bbfb735e852d4cb83 |
| wecom | **REVIEW** | CANDIDATE | 3 | snap-wecom-095975531756aac155c3bd1b |
| xai-grok | **REVIEW** | CANDIDATE | 1 | snap-xai-grok-0f56662ce92c5717e8909b9d |
| xbox | **REVIEW** | CANDIDATE | 42 | snap-xbox-c056e17cbe3622251ba30c82 |
| youdao | **REVIEW** | CANDIDATE | 15 | snap-youdao-fc97f5d207d4c3358c6a4d6b |
| youtube | **REVIEW** | CANDIDATE | 175 | snap-youtube-58b8afe3b6062febd60fd519 |
| youtubemusic | **VERIFIED** | CANDIDATE | 1 | snap-youtubemusic-4af31e7577631d296a0eea49 |
<!-- SOURCE_STATUS:END -->
