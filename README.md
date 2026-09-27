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
| 1688 | **PRODUCTION** | CANDIDATE | 2 | snap-1688-4152b558b34476df1a55a8d8 |
| adobe-firefly | **REVIEW** | CANDIDATE | 1 | snap-adobe-firefly-278e98581b6f8e62e261931a |
| adobe-fonts | **REVIEW** | CANDIDATE | 1 | snap-adobe-fonts-0cfd6c78ffb842903de0152c |
| adobe-stock | **REVIEW** | CANDIDATE | 1 | snap-adobe-stock-fb5983c8b0ef609fde49e4e0 |
| alibabacloud | **REVIEW** | CANDIDATE | 12 | snap-alibabacloud-c121379a018839c4e2c1ad91 |
| amazonmusic | **REVIEW** | CANDIDATE | 1 | snap-amazonmusic-8f36e1717aca94afda1ee0d0 |
| amd | **REVIEW** | NO_SNAPSHOT | 0 | none |
| anthropic-claude | **REVIEW** | CANDIDATE | 1 | snap-anthropic-claude-57b3b3b1999c5d83d8f322a5 |
| anthropic-platform | **REVIEW** | CANDIDATE | 1 | snap-anthropic-platform-7bf2ee650853808906839699 |
| applebooks | **REVIEW** | CANDIDATE | 1 | snap-applebooks-1a82b91eb9b4c8feecb94c8a |
| appledev | **VERIFIED** | CANDIDATE | 38 | snap-appledev-69881d2207a1d8d4377f2166 |
| applemaps | **REVIEW** | CANDIDATE | 1 | snap-applemaps-71a1a34ed238b4cf742e293e |
| applemedia | **VERIFIED** | CANDIDATE | 52 | snap-applemedia-5042d174723b9a5737d6f038 |
| applemusic | **VERIFIED** | CANDIDATE | 9 | snap-applemusic-da04320590fe88862d5e36fb |
| applenews | **VERIFIED** | CANDIDATE | 2 | snap-applenews-5b92e365d4fca996fc468b19 |
| applepodcasts | **REVIEW** | CANDIDATE | 1 | snap-applepodcasts-4bfb9ca6b27a141e7aa9fa0c |
| appletv | **REVIEW** | CANDIDATE | 7 | snap-appletv-b983ca24d850eeada428f1da |
| appstore | **VERIFIED** | CANDIDATE | 2 | snap-appstore-d141bbc12b271c916f41990c |
| audible | **REVIEW** | CANDIDATE | 1 | snap-audible-2ae1b9d59ebdc6174db597b1 |
| autohome | **REVIEW** | NO_SNAPSHOT | 0 | none |
| azure | **VERIFIED** | CANDIDATE | 149 | snap-azure-b3a73e93d99fb11dc21e4888 |
| baidu | **VERIFIED** | CANDIDATE | 251 | snap-baidu-584ae9eeb87fa1dabd00d11f |
| baidu-zhidao | **REVIEW** | NO_SNAPSHOT | 0 | none |
| baidumaps | **REVIEW** | NO_SNAPSHOT | 0 | none |
| baidunetdisk | **REVIEW** | CANDIDATE | 2 | snap-baidunetdisk-2030ef27118ea52d548a5667 |
| baidutieba | **VERIFIED** | CANDIDATE | 32 | snap-baidutieba-9badf818529f1807c7959832 |
| baiduwenku | **REVIEW** | NO_SNAPSHOT | 0 | none |
| bing | **VERIFIED** | CANDIDATE | 9 | snap-bing-3f36698777489885ba7fdbfd |
| byd | **REVIEW** | NO_SNAPSHOT | 0 | none |
| cainiao | **PRODUCTION** | CANDIDATE | 1 | snap-cainiao-179bcd0d35e42488cc41692b |
| chatgpt | **REVIEW** | CANDIDATE | 1 | snap-chatgpt-cc1e48c936f2293870e7e2c0 |
| cisco | **REVIEW** | NO_SNAPSHOT | 0 | none |
| claude | **VERIFIED** | CANDIDATE | 3 | snap-claude-4aec84cea09e5629117513fa |
| cloudflare | **REVIEW** | NO_SNAPSHOT | 0 | none |
| copilot | **VERIFIED** | CANDIDATE | 45 | snap-copilot-9f6da111d1453ad19fc927d2 |
| datadog | **REVIEW** | NO_SNAPSHOT | 0 | none |
| deepseek | **REVIEW** | CANDIDATE | 2 | snap-deepseek-0c14562b294e2ad50feadc74 |
| dingding | **PRODUCTION** | CANDIDATE | 3 | snap-dingding-09ae1ecd000f1688f61e99a0 |
| discord | **VERIFIED** | CANDIDATE | 28 | snap-discord-e5a47c19f5c45c25c613f6f6 |
| doubao | **REVIEW** | CANDIDATE | 4 | snap-doubao-9f9124c0c24b39a949792104 |
| douyin | **VERIFIED** | CANDIDATE | 13 | snap-douyin-3780b3c2b6ee1a9abdccf245 |
| eastmoney | **REVIEW** | NO_SNAPSHOT | 0 | none |
| feishu | **VERIFIED** | CANDIDATE | 43 | snap-feishu-dd8e2cd8a4ac32fa8b355226 |
| findmy | **VERIFIED** | CANDIDATE | 3 | snap-findmy-5dbfa7a125855e4ee11e3daf |
| firebase | **REVIEW** | CANDIDATE | 2 | snap-firebase-a5574fd6cc7df4f1b8b30508 |
| gemini | **VERIFIED** | CANDIDATE | 9 | snap-gemini-9e01a42e8140aafccd75f9ea |
| github | **REVIEW** | CANDIDATE | 29 | snap-github-293b2b0db400e778bcfe88a7 |
| gmail | **REVIEW** | CANDIDATE | 1 | snap-gmail-c3a855e07fa2cf45651ae3a4 |
| goodreads | **REVIEW** | CANDIDATE | 1 | snap-goodreads-eb7a2c816de0efe942519ac8 |
| google-calendar | **REVIEW** | CANDIDATE | 1 | snap-google-calendar-1b852f9159dd62fdc2bbde01 |
| google-chat | **REVIEW** | CANDIDATE | 1 | snap-google-chat-25e1acd75e54a275f491a913 |
| google-contacts | **REVIEW** | CANDIDATE | 1 | snap-google-contacts-3ad5c7ecb05956597c4ae5ca |
| google-docs | **REVIEW** | CANDIDATE | 1 | snap-google-docs-373a011368bfd8cccaccc4dd |
| google-earth | **REVIEW** | CANDIDATE | 1 | snap-google-earth-d9b76bf3506634dccd2b96e2 |
| google-forms | **REVIEW** | CANDIDATE | 1 | snap-google-forms-559aea19004e62de9eb7175d |
| google-groups | **REVIEW** | CANDIDATE | 1 | snap-google-groups-ee345194168348f5b9b4cad2 |
| google-maps | **REVIEW** | CANDIDATE | 1 | snap-google-maps-ad2f1a8bcd3a536fca6b3dac |
| google-meet | **REVIEW** | CANDIDATE | 1 | snap-google-meet-c4280ce1e242a4dd7b758342 |
| google-news | **REVIEW** | CANDIDATE | 1 | snap-google-news-78c4526fe0a249e933aed4ff |
| google-photos | **REVIEW** | CANDIDATE | 1 | snap-google-photos-c2fe7615ea4cf011cdbc31de |
| google-play | **REVIEW** | CANDIDATE | 1 | snap-google-play-8521d59544a0decf823e859c |
| google-sheets | **REVIEW** | CANDIDATE | 1 | snap-google-sheets-6de01de6e87331067661ad92 |
| google-sites | **REVIEW** | CANDIDATE | 1 | snap-google-sites-8110ded44cc74b3e78e32ecc |
| google-slides | **REVIEW** | CANDIDATE | 1 | snap-google-slides-4b5f8f5fff72ee076ba11416 |
| google-vids | **REVIEW** | CANDIDATE | 1 | snap-google-vids-e595a5032f87e5544cb3874e |
| google-voice | **REVIEW** | CANDIDATE | 1 | snap-google-voice-d823134be8c59031aa5055d8 |
| google-workspace-studio | **REVIEW** | CANDIDATE | 1 | snap-google-workspace-studio-a936fad5df9362c828fb9d68 |
| googlecloud | **REVIEW** | CANDIDATE | 5 | snap-googlecloud-c6f2f1a871af186052767530 |
| googledrive | **VERIFIED** | CANDIDATE | 4 | snap-googledrive-a3f033b61b8bc0b99e39f7ca |
| googlefcm | **REVIEW** | CANDIDATE | 13 | snap-googlefcm-d2649b705a9906c0296cdbaf |
| groq | **REVIEW** | CANDIDATE | 1 | snap-groq-c073c7adcd8f0db5ebe9a92a |
| honor | **REVIEW** | NO_SNAPSHOT | 0 | none |
| honorofkings_cn | **REVIEW** | CANDIDATE | 1 | snap-honorofkings_cn-a804aed53545aac4f58d34d8 |
| honorofkings_global | **REVIEW** | CANDIDATE | 2 | snap-honorofkings_global-9271ce0b7c8d6b9d6d1836fa |
| huawei-appgallery | **REVIEW** | NO_SNAPSHOT | 0 | none |
| huawei-cloud | **REVIEW** | CANDIDATE | 1 | snap-huawei-cloud-baad7d83f4093ace2f04705c |
| huggingface | **REVIEW** | CANDIDATE | 3 | snap-huggingface-c41977bf6c8dade8b423273a |
| ibm | **REVIEW** | NO_SNAPSHOT | 0 | none |
| icloud | **VERIFIED** | CANDIDATE | 58 | snap-icloud-d3bceca16ccfbb5fe06c64f6 |
| iflytek | **REVIEW** | NO_SNAPSHOT | 0 | none |
| intel | **REVIEW** | NO_SNAPSHOT | 0 | none |
| jd-cloud | **REVIEW** | CANDIDATE | 1 | snap-jd-cloud-7364b0a4c509c49727621c40 |
| kuaishou | **REVIEW** | NO_SNAPSHOT | 0 | none |
| kuaishou-open | **REVIEW** | NO_SNAPSHOT | 0 | none |
| kugou | **REVIEW** | CANDIDATE | 1 | snap-kugou-bd7700e11c8ff2c07e7b9321 |
| kuwo | **REVIEW** | CANDIDATE | 1 | snap-kuwo-c36f7d9497fdd5e0b0806d93 |
| lenovo | **REVIEW** | NO_SNAPSHOT | 0 | none |
| messenger | **REVIEW** | CANDIDATE | 4 | snap-messenger-b3b52c8322960d4f19279550 |
| mgtv | **REVIEW** | NO_SNAPSHOT | 0 | none |
| mi-cloud | **REVIEW** | CANDIDATE | 1 | snap-mi-cloud-e876da13d4a50a1abf1ddb7a |
| mongodb | **REVIEW** | NO_SNAPSHOT | 0 | none |
| ms365-excel | **REVIEW** | CANDIDATE | 1 | snap-ms365-excel-84491a426ae08f1b75786d09 |
| ms365-loop | **REVIEW** | CANDIDATE | 1 | snap-ms365-loop-65886fc777a8ed550f93fb60 |
| ms365-mesh | **REVIEW** | CANDIDATE | 1 | snap-ms365-mesh-cb11ed05173e638e4642ab11 |
| ms365-onenote | **REVIEW** | CANDIDATE | 1 | snap-ms365-onenote-5115ce5bb375c71660f5b78f |
| ms365-planner | **REVIEW** | CANDIDATE | 1 | snap-ms365-planner-c6ee135c73112ab31f5132b3 |
| ms365-powerpoint | **REVIEW** | CANDIDATE | 1 | snap-ms365-powerpoint-0e7ea85ee45bd767f51ac6b6 |
| ms365-word | **REVIEW** | CANDIDATE | 1 | snap-ms365-word-0eb9e29c143572c255507c67 |
| neteasemail | **REVIEW** | CANDIDATE | 3 | snap-neteasemail-8f25db6f713ea62f08bd565b |
| neteasemusic | **VERIFIED** | CANDIDATE | 10 | snap-neteasemusic-34efc854219f96a2aa121d84 |
| netflix | **VERIFIED** | CANDIDATE | 31 | snap-netflix-5b2876cf88dc642c06b22d35 |
| nvidia | **REVIEW** | NO_SNAPSHOT | 0 | none |
| onedrive | **VERIFIED** | CANDIDATE | 13 | snap-onedrive-241ab9a1831b3f0a3affb85a |
| openai | **VERIFIED** | CANDIDATE | 31 | snap-openai-cda1ed8e109c4abd8bf521dd |
| openai-api | **REVIEW** | CANDIDATE | 1 | snap-openai-api-c8952ba8249663ca6f49098d |
| openai-platform | **REVIEW** | CANDIDATE | 1 | snap-openai-platform-769b5880b0899016f4335a85 |
| perplexity | **REVIEW** | CANDIDATE | 4 | snap-perplexity-ada0cc4943c05a38442ca859 |
| qihoo360 | **REVIEW** | NO_SNAPSHOT | 0 | none |
| qq | **REVIEW** | REVIEW | 1 | snap-qq-e8b755c0889d871584191efb |
| qqmail | **PRODUCTION** | CANDIDATE | 1 | snap-qqmail-013babbee1bf9cf46a1741a1 |
| qqmusic | **PRODUCTION** | CANDIDATE | 1 | snap-qqmusic-421df9f4465ad7fb35ed9c06 |
| quanmin-k-ge | **REVIEW** | CANDIDATE | 1 | snap-quanmin-k-ge-00c1b63526a1b67c5f490aaf |
| qunar | **REVIEW** | NO_SNAPSHOT | 0 | none |
| roblox | **REVIEW** | CANDIDATE | 47 | snap-roblox-36d3732a073e69dc0d883708 |
| salesforce | **REVIEW** | NO_SNAPSHOT | 0 | none |
| samsung | **REVIEW** | NO_SNAPSHOT | 0 | none |
| shimo | **REVIEW** | NO_SNAPSHOT | 0 | none |
| signal | **REVIEW** | CANDIDATE | 8 | snap-signal-ab3deea2dbc34fa008c60d6c |
| siri | **REVIEW** | CANDIDATE | 1 | snap-siri-440b4c5a63d59b410d5e32fa |
| stripe-dashboard | **REVIEW** | CANDIDATE | 1 | snap-stripe-dashboard-e5667382cb3f12c246ad8660 |
| taobao | **VERIFIED** | REVIEW | 1 | snap-taobao-50646cfa0e93b38a8153bf8d |
| teams | **VERIFIED** | CANDIDATE | 4 | snap-teams-b7790f52024c56ece9273ef3 |
| telegram | **VERIFIED** | CANDIDATE | 24 | snap-telegram-ae2063026508ed946661df66 |
| tencentcloud | **PRODUCTION** | CANDIDATE | 1 | snap-tencentcloud-11f2a09f18218925500878fc |
| tencentmeeting | **REVIEW** | CANDIDATE | 3 | snap-tencentmeeting-19826cb5a6a9fb912f7be3fc |
| tencentvideo | **REVIEW** | CANDIDATE | 17 | snap-tencentvideo-0bbc97349dbece8ea2628b3f |
| tesla | **REVIEW** | NO_SNAPSHOT | 0 | none |
| testflight | **VERIFIED** | CANDIDATE | 2 | snap-testflight-922accff387fa39f172c3c41 |
| tiktok | **VERIFIED** | CANDIDATE | 29 | snap-tiktok-d7c408670d9f72fda616937c |
| tmall | **VERIFIED** | CANDIDATE | 8 | snap-tmall-ea8c65fe854188e13fb67584 |
| venmo | **REVIEW** | CANDIDATE | 1 | snap-venmo-ad97a6f5008ebab004dbad8a |
| wechat | **VERIFIED** | CANDIDATE | 28 | snap-wechat-84a8d3ac3ff682614f4d7470 |
| wecom | **REVIEW** | CANDIDATE | 3 | snap-wecom-c6975c7fa31bc2c96407e444 |
| wps | **REVIEW** | NO_SNAPSHOT | 0 | none |
| xai-grok | **REVIEW** | CANDIDATE | 1 | snap-xai-grok-0f56662ce92c5717e8909b9d |
| xbox | **REVIEW** | CANDIDATE | 42 | snap-xbox-c056e17cbe3622251ba30c82 |
| xunlei | **REVIEW** | NO_SNAPSHOT | 0 | none |
| youdao | **REVIEW** | CANDIDATE | 15 | snap-youdao-fc97f5d207d4c3358c6a4d6b |
| youtube | **REVIEW** | CANDIDATE | 175 | snap-youtube-58b8afe3b6062febd60fd519 |
| youtubemusic | **VERIFIED** | CANDIDATE | 1 | snap-youtubemusic-0e39136672e2e05e52470bd5 |
| zhipin | **REVIEW** | NO_SNAPSHOT | 0 | none |
| zte | **REVIEW** | NO_SNAPSHOT | 0 | none |
<!-- SOURCE_STATUS:END -->
