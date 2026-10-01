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
| 1688 | **PRODUCTION** | CANDIDATE | 2 | snap-1688-222302f3a20ecb7c08c72ed0 |
| 37games | **REVIEW** | CANDIDATE | 2 | snap-37games-8a465d1cde5472566a14998b |
| adobe-firefly | **REVIEW** | CANDIDATE | 1 | snap-adobe-firefly-278e98581b6f8e62e261931a |
| adobe-fonts | **REVIEW** | CANDIDATE | 1 | snap-adobe-fonts-0cfd6c78ffb842903de0152c |
| adobe-stock | **REVIEW** | CANDIDATE | 1 | snap-adobe-stock-fb5983c8b0ef609fde49e4e0 |
| alibabacloud | **REVIEW** | CANDIDATE | 12 | snap-alibabacloud-c121379a018839c4e2c1ad91 |
| aliexpress | **REVIEW** | CANDIDATE | 2 | snap-aliexpress-96471da327814186bdb36a68 |
| alipay | **REVIEW** | CANDIDATE | 2 | snap-alipay-7e39ca630ab553d1bd55c414 |
| amap | **REVIEW** | CANDIDATE | 2 | snap-amap-e135e4fdc9f54e283658b727 |
| amazonmusic | **REVIEW** | CANDIDATE | 1 | snap-amazonmusic-8f36e1717aca94afda1ee0d0 |
| amd | **REVIEW** | CANDIDATE | 2 | snap-amd-d39c5ad3a11f464cc588c7f6 |
| anjuke | **REVIEW** | CANDIDATE | 2 | snap-anjuke-0e1ad2a9baadd35c14c4008a |
| anker | **REVIEW** | CANDIDATE | 2 | snap-anker-9a9b06e7d8a0555ff7d6aedc |
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
| arista | **REVIEW** | CANDIDATE | 2 | snap-arista-840df54358b90619c408e5f4 |
| arm | **REVIEW** | CANDIDATE | 2 | snap-arm-09d5469ad7bdd751fb9b70ea |
| asml | **REVIEW** | CANDIDATE | 2 | snap-asml-5c02ccc337a824804f8d06c3 |
| atlassian | **REVIEW** | CANDIDATE | 2 | snap-atlassian-b7b664182b05e06d3e50139e |
| atour | **REVIEW** | CANDIDATE | 2 | snap-atour-48582d816984996f87f1adf8 |
| audible | **REVIEW** | CANDIDATE | 1 | snap-audible-2ae1b9d59ebdc6174db597b1 |
| autodesk | **REVIEW** | CANDIDATE | 2 | snap-autodesk-ec9852888af1e9f52eadafd2 |
| autohome | **REVIEW** | CANDIDATE | 2 | snap-autohome-119d2c8be99debed50fda277 |
| azure | **VERIFIED** | CANDIDATE | 149 | snap-azure-b3a73e93d99fb11dc21e4888 |
| baichuan | **REVIEW** | CANDIDATE | 2 | snap-baichuan-e2d81430dd580b43da427a5d |
| baidu | **VERIFIED** | CANDIDATE | 251 | snap-baidu-584ae9eeb87fa1dabd00d11f |
| baidu-zhidao | **REVIEW** | CANDIDATE | 1 | snap-baidu-zhidao-22bb74edb99604a53226a40a |
| baidumaps | **REVIEW** | CANDIDATE | 1 | snap-baidumaps-8867eda7f9ffa6e53540fd3e |
| baidunetdisk | **REVIEW** | CANDIDATE | 2 | snap-baidunetdisk-2030ef27118ea52d548a5667 |
| baidutieba | **VERIFIED** | CANDIDATE | 32 | snap-baidutieba-9badf818529f1807c7959832 |
| baiduwenku | **REVIEW** | CANDIDATE | 1 | snap-baiduwenku-57c72c17e64bf2eacf87141d |
| beike | **REVIEW** | CANDIDATE | 2 | snap-beike-ae0847a06f68cb6ccc9b1d93 |
| bing | **VERIFIED** | CANDIDATE | 9 | snap-bing-3f36698777489885ba7fdbfd |
| birentech | **REVIEW** | CANDIDATE | 2 | snap-birentech-794172d42ff5ff0de1bf0533 |
| block | **REVIEW** | CANDIDATE | 2 | snap-block-cb6da11205c0a980ace1edc2 |
| boss | **REVIEW** | CANDIDATE | 2 | snap-boss-b8731077f1f1142b7d25a49d |
| broadcom | **REVIEW** | CANDIDATE | 2 | snap-broadcom-ac0fc70c68986ce443e28b2e |
| byd | **REVIEW** | CANDIDATE | 2 | snap-byd-372c75d54b5df2d6a71260d7 |
| cadence | **REVIEW** | CANDIDATE | 2 | snap-cadence-bf842312e32dcf5a9ebf321b |
| cainiao | **PRODUCTION** | CANDIDATE | 1 | snap-cainiao-a8a898392298ebaa644a783e |
| cambricon | **REVIEW** | CANDIDATE | 2 | snap-cambricon-d21f4caa20bc6d2bb1874893 |
| caocao | **REVIEW** | CANDIDATE | 2 | snap-caocao-3bbf9c257b72eeb1e63eeb54 |
| capcut | **REVIEW** | CANDIDATE | 2 | snap-capcut-467bf7a873d3f21cf1d2dd12 |
| chatgpt | **REVIEW** | CANDIDATE | 1 | snap-chatgpt-cc1e48c936f2293870e7e2c0 |
| cisco | **REVIEW** | CANDIDATE | 2 | snap-cisco-9a3aaeb43d6d3a0a5e07a015 |
| claude | **VERIFIED** | CANDIDATE | 3 | snap-claude-4aec84cea09e5629117513fa |
| cloudflare | **REVIEW** | NO_SNAPSHOT | 0 | none |
| coinbase | **REVIEW** | CANDIDATE | 2 | snap-coinbase-428453f560b2b36a037ae4a8 |
| copilot | **VERIFIED** | CANDIDATE | 45 | snap-copilot-9f6da111d1453ad19fc927d2 |
| coupang | **REVIEW** | CANDIDATE | 2 | snap-coupang-95e69a8ae18aaaaeed2b0c26 |
| crowdstrike | **REVIEW** | CANDIDATE | 2 | snap-crowdstrike-93425b240aa10465a1666359 |
| ctyun | **REVIEW** | CANDIDATE | 2 | snap-ctyun-4274fec1e04159015436e52f |
| dahua | **REVIEW** | CANDIDATE | 2 | snap-dahua-bf8000a4d702228a37044d1a |
| dassault | **REVIEW** | CANDIDATE | 2 | snap-dassault-ddd455ea2301cc82ea31bd00 |
| databricks | **REVIEW** | CANDIDATE | 2 | snap-databricks-d612a4dc8584d5154f905273 |
| datadog | **REVIEW** | CANDIDATE | 2 | snap-datadog-507e01df7ff9a667069ba1fd |
| deepseek | **REVIEW** | CANDIDATE | 2 | snap-deepseek-0c14562b294e2ad50feadc74 |
| dell | **REVIEW** | CANDIDATE | 2 | snap-dell-38841c4b161c8f903f219bcc |
| dingding | **PRODUCTION** | CANDIDATE | 3 | snap-dingding-09ae1ecd000f1688f61e99a0 |
| discord | **VERIFIED** | CANDIDATE | 28 | snap-discord-e5a47c19f5c45c25c613f6f6 |
| dji | **REVIEW** | CANDIDATE | 2 | snap-dji-91217fbce3ff00d9c9cf090e |
| doubao | **REVIEW** | CANDIDATE | 4 | snap-doubao-5396a151dcae37583b6bd589 |
| douyin | **VERIFIED** | CANDIDATE | 13 | snap-douyin-3780b3c2b6ee1a9abdccf245 |
| dreame | **REVIEW** | CANDIDATE | 2 | snap-dreame-bed5113970f4051c281f1664 |
| ea | **REVIEW** | CANDIDATE | 2 | snap-ea-e0d2eb677f682743dd48cf3d |
| eastmoney | **REVIEW** | CANDIDATE | 2 | snap-eastmoney-1aebbd7125a8244e9014e3ff |
| eleme | **REVIEW** | CANDIDATE | 2 | snap-eleme-8452b1a92a8c2c3d7503cf0e |
| epicgames | **REVIEW** | CANDIDATE | 3 | snap-epicgames-f438fd86b26ddbc65fa37dfa |
| equinix | **REVIEW** | CANDIDATE | 2 | snap-equinix-2316b82548e279bd0ff99e56 |
| ericsson | **REVIEW** | CANDIDATE | 2 | snap-ericsson-75e2c108606fe72e56369e2a |
| feishu | **VERIFIED** | CANDIDATE | 43 | snap-feishu-dd8e2cd8a4ac32fa8b355226 |
| findmy | **VERIFIED** | CANDIDATE | 3 | snap-findmy-5dbfa7a125855e4ee11e3daf |
| firebase | **REVIEW** | CANDIDATE | 2 | snap-firebase-7161fac5d50d09fc4a2605be |
| fliggy | **REVIEW** | CANDIDATE | 2 | snap-fliggy-1d25258037024c0da23217a3 |
| fortinet | **REVIEW** | CANDIDATE | 2 | snap-fortinet-a088ad8c0dcb6f363911a3ab |
| fujitsu | **REVIEW** | CANDIDATE | 2 | snap-fujitsu-ce2d7e601c70496da9f4590f |
| gemini | **VERIFIED** | CANDIDATE | 9 | snap-gemini-9e01a42e8140aafccd75f9ea |
| getapps | **REVIEW** | CANDIDATE | 1 | snap-getapps-6eb3c67a2267c1e2d1684dd5 |
| github | **REVIEW** | CANDIDATE | 29 | snap-github-293b2b0db400e778bcfe88a7 |
| globalfoundries | **REVIEW** | CANDIDATE | 2 | snap-globalfoundries-17db302f7b18defdd35ba751 |
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
| googlecloud | **REVIEW** | CANDIDATE | 5 | snap-googlecloud-b6d12a6bdc42f9c4ae1d0b74 |
| googledrive | **VERIFIED** | CANDIDATE | 4 | snap-googledrive-a3f033b61b8bc0b99e39f7ca |
| googlefcm | **REVIEW** | CANDIDATE | 13 | snap-googlefcm-d2649b705a9906c0296cdbaf |
| grab | **REVIEW** | CANDIDATE | 2 | snap-grab-df7ca87a00ca3902947bf0e4 |
| groq | **REVIEW** | CANDIDATE | 1 | snap-groq-3f8b97712755dd76acdc77ab |
| haier | **REVIEW** | CANDIDATE | 2 | snap-haier-1d11d592bffb5709f2455f4f |
| hellobike | **REVIEW** | CANDIDATE | 2 | snap-hellobike-2f40b385c128e7087ab9bcbe |
| heytap | **REVIEW** | CANDIDATE | 2 | snap-heytap-c0fad031b445f1ba2e0df58f |
| hikvision | **REVIEW** | CANDIDATE | 2 | snap-hikvision-48addd781bb964a4f72692f1 |
| hitachi | **REVIEW** | CANDIDATE | 2 | snap-hitachi-1e6851042c68c063a98be11b |
| honor | **REVIEW** | CANDIDATE | 2 | snap-honor-aa063550b6daa7a8994cc454 |
| honorofkings_cn | **REVIEW** | CANDIDATE | 1 | snap-honorofkings_cn-a804aed53545aac4f58d34d8 |
| honorofkings_global | **REVIEW** | CANDIDATE | 2 | snap-honorofkings_global-9271ce0b7c8d6b9d6d1836fa |
| hpe | **REVIEW** | CANDIDATE | 2 | snap-hpe-7cfb13d56eca4924255a598a |
| huawei-appgallery | **REVIEW** | CANDIDATE | 1 | snap-huawei-appgallery-c9ac2197b482ac3a9910d1e1 |
| huawei-cloud | **REVIEW** | CANDIDATE | 1 | snap-huawei-cloud-baad7d83f4093ace2f04705c |
| hubspot | **REVIEW** | CANDIDATE | 2 | snap-hubspot-0fa3424c1491866458aefa94 |
| huggingface | **REVIEW** | CANDIDATE | 3 | snap-huggingface-226053190707e71c9f66141c |
| huolala | **REVIEW** | CANDIDATE | 2 | snap-huolala-13fa7bcccc08372345ff0dad |
| ibm | **REVIEW** | CANDIDATE | 2 | snap-ibm-37965a10aeb0c5a5dcbd06cc |
| icloud | **VERIFIED** | CANDIDATE | 58 | snap-icloud-d3bceca16ccfbb5fe06c64f6 |
| iflytek | **REVIEW** | CANDIDATE | 2 | snap-iflytek-4efe816c7539950150d3efde |
| intel | **REVIEW** | CANDIDATE | 2 | snap-intel-ae6db8931e41867ab2c9ce5d |
| internlm | **REVIEW** | CANDIDATE | 1 | snap-internlm-5012fe6fb6f7f401aaa09c07 |
| intuit | **REVIEW** | CANDIDATE | 2 | snap-intuit-89bf1839c3bf60c58b5e6c65 |
| jd-cloud | **REVIEW** | CANDIDATE | 1 | snap-jd-cloud-7364b0a4c509c49727621c40 |
| jdcloud | **REVIEW** | CANDIDATE | 2 | snap-jdcloud-0249ba9080d754056cd6a446 |
| jianying | **REVIEW** | CANDIDATE | 2 | snap-jianying-34e07211430e783cee781fb1 |
| kakao | **REVIEW** | CANDIDATE | 2 | snap-kakao-6653968a2323e837dd09ce60 |
| kingdee | **REVIEW** | CANDIDATE | 2 | snap-kingdee-42ceda0ada5607414b5eea3f |
| kla | **REVIEW** | CANDIDATE | 2 | snap-kla-1ba9c282fa51eb3b77b7384d |
| kuaishou | **REVIEW** | CANDIDATE | 1 | snap-kuaishou-fc5e356125b8d4a98b6162b8 |
| kuaishou-open | **REVIEW** | CANDIDATE | 1 | snap-kuaishou-open-a37b0a3c3d40ccfaa1207456 |
| kugou | **REVIEW** | CANDIDATE | 1 | snap-kugou-bd7700e11c8ff2c07e7b9321 |
| kunlunxin | **REVIEW** | CANDIDATE | 2 | snap-kunlunxin-9fde1b492b2230d9e4248208 |
| kuwo | **REVIEW** | CANDIDATE | 1 | snap-kuwo-c36f7d9497fdd5e0b0806d93 |
| lamresearch | **REVIEW** | CANDIDATE | 2 | snap-lamresearch-ff551d8ce98b44de573d829c |
| lark | **REVIEW** | CANDIDATE | 2 | snap-lark-0cd1d2b00d1ebd7917aee675 |
| lazada | **REVIEW** | CANDIDATE | 2 | snap-lazada-afca946398e6ec1cb9830db0 |
| lenovo | **REVIEW** | CANDIDATE | 2 | snap-lenovo-c8d84c550ab4949633bcea79 |
| lg | **REVIEW** | CANDIDATE | 2 | snap-lg-1d42e32c240053ac7978daba |
| linecorp | **REVIEW** | CANDIDATE | 2 | snap-linecorp-0e2c59bbc6e835b157fe80da |
| linkedin | **REVIEW** | CANDIDATE | 2 | snap-linkedin-454eb7556f0cd23a8662a2c1 |
| lufax | **REVIEW** | CANDIDATE | 2 | snap-lufax-86bfaf82bd01f21101af7538 |
| manbang | **REVIEW** | CANDIDATE | 2 | snap-manbang-8f6bf55c006138879b3f0539 |
| mediatek | **REVIEW** | CANDIDATE | 2 | snap-mediatek-6399d2c36b7c1d9a23813629 |
| mercadolibre | **REVIEW** | CANDIDATE | 2 | snap-mercadolibre-9b4cbfb954c830ddca6177eb |
| messenger | **REVIEW** | CANDIDATE | 4 | snap-messenger-b3b52c8322960d4f19279550 |
| mgtv | **REVIEW** | CANDIDATE | 2 | snap-mgtv-ffd1b433e2f0ebb7e775204b |
| mi-cloud | **REVIEW** | CANDIDATE | 1 | snap-mi-cloud-e876da13d4a50a1abf1ddb7a |
| micron | **REVIEW** | CANDIDATE | 2 | snap-micron-dd7274ef12250bff1c9bbafc |
| migu | **REVIEW** | CANDIDATE | 2 | snap-migu-2c130d2595cc59d07fca2f2c |
| mihome | **REVIEW** | CANDIDATE | 1 | snap-mihome-6a615841d6d3845cee26ffcb |
| minimax | **REVIEW** | CANDIDATE | 2 | snap-minimax-c9a118b15225676be85a7e13 |
| mongodb | **REVIEW** | CANDIDATE | 2 | snap-mongodb-f2f9a87cf8d835b8983e37f3 |
| moonshot | **REVIEW** | CANDIDATE | 2 | snap-moonshot-caaddf9c7a19a0dffbd811fd |
| ms365-excel | **REVIEW** | CANDIDATE | 1 | snap-ms365-excel-84491a426ae08f1b75786d09 |
| ms365-loop | **REVIEW** | CANDIDATE | 1 | snap-ms365-loop-65886fc777a8ed550f93fb60 |
| ms365-mesh | **REVIEW** | CANDIDATE | 1 | snap-ms365-mesh-cb11ed05173e638e4642ab11 |
| ms365-onenote | **REVIEW** | CANDIDATE | 1 | snap-ms365-onenote-5115ce5bb375c71660f5b78f |
| ms365-planner | **REVIEW** | CANDIDATE | 1 | snap-ms365-planner-c6ee135c73112ab31f5132b3 |
| ms365-powerpoint | **REVIEW** | CANDIDATE | 1 | snap-ms365-powerpoint-0e7ea85ee45bd767f51ac6b6 |
| ms365-word | **REVIEW** | CANDIDATE | 1 | snap-ms365-word-0eb9e29c143572c255507c67 |
| nec | **REVIEW** | CANDIDATE | 2 | snap-nec-f169c670ad5d484535541e84 |
| netapp | **REVIEW** | CANDIDATE | 2 | snap-netapp-b83dd36a0f68d478ef9dbb9e |
| neteasemail | **REVIEW** | CANDIDATE | 3 | snap-neteasemail-8f25db6f713ea62f08bd565b |
| neteasemusic | **VERIFIED** | CANDIDATE | 10 | snap-neteasemusic-34efc854219f96a2aa121d84 |
| netflix | **VERIFIED** | CANDIDATE | 31 | snap-netflix-5b2876cf88dc642c06b22d35 |
| nintendo | **REVIEW** | CANDIDATE | 2 | snap-nintendo-6da83899f6599b760c92b015 |
| nokia | **REVIEW** | CANDIDATE | 2 | snap-nokia-ea294874821737755659ccce |
| nvidia | **REVIEW** | CANDIDATE | 3 | snap-nvidia-a6059abb14e07ee76462cbe5 |
| office | **REVIEW** | CANDIDATE | 2 | snap-office-16c488c0914d570060921459 |
| okta | **REVIEW** | CANDIDATE | 2 | snap-okta-eacf3a9a634e3b2ac73a25b0 |
| onedrive | **VERIFIED** | CANDIDATE | 13 | snap-onedrive-241ab9a1831b3f0a3affb85a |
| openai | **VERIFIED** | CANDIDATE | 31 | snap-openai-cda1ed8e109c4abd8bf521dd |
| openai-api | **REVIEW** | CANDIDATE | 1 | snap-openai-api-c8952ba8249663ca6f49098d |
| openai-platform | **REVIEW** | CANDIDATE | 1 | snap-openai-platform-769b5880b0899016f4335a85 |
| outlook | **REVIEW** | CANDIDATE | 4 | snap-outlook-5b6d555db235bd3f501eae14 |
| palantir | **REVIEW** | CANDIDATE | 2 | snap-palantir-491431496aa1b899bd134242 |
| paloalto | **REVIEW** | CANDIDATE | 2 | snap-paloalto-702c7b333bc5db2f86137c57 |
| panasonic | **REVIEW** | CANDIDATE | 2 | snap-panasonic-7b363977355149a7d0243f6f |
| perfectworld | **REVIEW** | CANDIDATE | 2 | snap-perfectworld-eb0720d237073dafc615e47d |
| perplexity | **REVIEW** | CANDIDATE | 4 | snap-perplexity-ada0cc4943c05a38442ca859 |
| pingan | **REVIEW** | CANDIDATE | 2 | snap-pingan-2dcbbc6369fb1b3faff8522e |
| powerbi | **REVIEW** | CANDIDATE | 2 | snap-powerbi-4a7b12792a8bd819db4df285 |
| qihoo360 | **REVIEW** | CANDIDATE | 2 | snap-qihoo360-74e11f09fbd29db005e57f0b |
| qq | **REVIEW** | REVIEW | 1 | snap-qq-e8b755c0889d871584191efb |
| qqbrowser | **REVIEW** | CANDIDATE | 1 | snap-qqbrowser-ebac3c840c0e682c1defa4ee |
| qqdoc | **REVIEW** | CANDIDATE | 1 | snap-qqdoc-8da6e91061793ca4fd4dd281 |
| qqmail | **PRODUCTION** | CANDIDATE | 1 | snap-qqmail-013babbee1bf9cf46a1741a1 |
| qqmusic | **PRODUCTION** | CANDIDATE | 1 | snap-qqmusic-421df9f4465ad7fb35ed9c06 |
| qualcomm | **REVIEW** | CANDIDATE | 2 | snap-qualcomm-cd7555bc47c58157a10b7850 |
| quanmin-k-ge | **REVIEW** | CANDIDATE | 1 | snap-quanmin-k-ge-00c1b63526a1b67c5f490aaf |
| qunar | **REVIEW** | CANDIDATE | 2 | snap-qunar-88bfe5677a93332e63577a9c |
| rakuten | **REVIEW** | CANDIDATE | 2 | snap-rakuten-3078fc149868c00c2f497fa6 |
| roblox | **REVIEW** | CANDIDATE | 47 | snap-roblox-7ab801cc1c6d8e5d601d0289 |
| roborock | **REVIEW** | CANDIDATE | 2 | snap-roborock-4c2f9467d9b68fa5db780449 |
| salesforce | **REVIEW** | CANDIDATE | 2 | snap-salesforce-31ea38c4cef525d27776ca23 |
| samsung | **REVIEW** | CANDIDATE | 2 | snap-samsung-2145c8ff882fa86961ad29d9 |
| sangfor | **REVIEW** | CANDIDATE | 2 | snap-sangfor-853e2291a329729bcd847e1b |
| sap | **REVIEW** | CANDIDATE | 2 | snap-sap-f44a3acab908f192ae52c5ac |
| schneider | **REVIEW** | CANDIDATE | 2 | snap-schneider-753e5f73a86a6a7e5779b601 |
| sensetime | **REVIEW** | CANDIDATE | 2 | snap-sensetime-31421a06db6acc2a63cfe2fc |
| servicenow | **REVIEW** | CANDIDATE | 2 | snap-servicenow-dc940e97f6e01e0e05161baf |
| sfexpress | **REVIEW** | CANDIDATE | 2 | snap-sfexpress-a5cd2546c841102ce8e7b4d2 |
| sharepoint | **REVIEW** | CANDIDATE | 2 | snap-sharepoint-7ac4887e7cccbafc954801e2 |
| shiji | **REVIEW** | CANDIDATE | 2 | snap-shiji-87063a5991e518f0494da16a |
| shimo | **REVIEW** | CANDIDATE | 1 | snap-shimo-88a8b1eb120cde0c758e15b8 |
| shopee | **REVIEW** | CANDIDATE | 2 | snap-shopee-9d2b627864e500861228f164 |
| siemens | **REVIEW** | CANDIDATE | 2 | snap-siemens-205eb9b8fc9c01544c9c6dec |
| signal | **REVIEW** | CANDIDATE | 8 | snap-signal-ab3deea2dbc34fa008c60d6c |
| siri | **REVIEW** | CANDIDATE | 1 | snap-siri-440b4c5a63d59b410d5e32fa |
| skhynix | **REVIEW** | CANDIDATE | 2 | snap-skhynix-9c713c945c8629f7aa5b27a5 |
| snowflake | **REVIEW** | CANDIDATE | 2 | snap-snowflake-5e58fc10ac5e533519bfa88c |
| sony | **REVIEW** | CANDIDATE | 2 | snap-sony-382278062b14392df186ceec |
| spacex | **REVIEW** | CANDIDATE | 2 | snap-spacex-5d404d39dedfc8686cc2046f |
| starlink | **REVIEW** | CANDIDATE | 2 | snap-starlink-45649164d15006f9cffe9d8c |
| stripe-dashboard | **REVIEW** | CANDIDATE | 1 | snap-stripe-dashboard-e5667382cb3f12c246ad8660 |
| supermicro | **REVIEW** | CANDIDATE | 2 | snap-supermicro-b18020358a7546e1a2002884 |
| synopsys | **REVIEW** | CANDIDATE | 2 | snap-synopsys-be7ea0d5d5e8875d848a88ca |
| t3go | **REVIEW** | CANDIDATE | 2 | snap-t3go-fa13548a022580221f9418af |
| take2 | **REVIEW** | CANDIDATE | 2 | snap-take2-10f50ebbc0a4ce855c4c44ac |
| taobao | **PRODUCTION** | REVIEW | 1 | snap-taobao-834d549e8982036ce1438963 |
| teams | **VERIFIED** | CANDIDATE | 4 | snap-teams-b7790f52024c56ece9273ef3 |
| telegram | **VERIFIED** | CANDIDATE | 24 | snap-telegram-ae2063026508ed946661df66 |
| temu | **REVIEW** | CANDIDATE | 2 | snap-temu-755cb28a74f87d97853dc205 |
| tencentcloud | **PRODUCTION** | CANDIDATE | 1 | snap-tencentcloud-e55bc8c508e839813ae20cd0 |
| tencentdocs | **REVIEW** | CANDIDATE | 1 | snap-tencentdocs-7e4c7db2344d088c45437ab1 |
| tencentmeeting | **REVIEW** | CANDIDATE | 3 | snap-tencentmeeting-19826cb5a6a9fb912f7be3fc |
| tencentvideo | **REVIEW** | CANDIDATE | 17 | snap-tencentvideo-0bbc97349dbece8ea2628b3f |
| tesla | **REVIEW** | CANDIDATE | 2 | snap-tesla-314c9a27dfa03ba8ee211f51 |
| testflight | **VERIFIED** | CANDIDATE | 2 | snap-testflight-922accff387fa39f172c3c41 |
| ti | **REVIEW** | CANDIDATE | 2 | snap-ti-c2efd8979ef9c9fa827d3336 |
| tiktok | **VERIFIED** | CANDIDATE | 29 | snap-tiktok-d7c408670d9f72fda616937c |
| tmall | **CANARY** | CANDIDATE | 8 | snap-tmall-17de7049e2f7bf67cb88c785 |
| tongcheng | **REVIEW** | CANDIDATE | 2 | snap-tongcheng-8926afa783b32fc0d24a826c |
| tonghuashun | **REVIEW** | CANDIDATE | 2 | snap-tonghuashun-ef5a12156bca60bed5aeaa00 |
| toutiao | **REVIEW** | CANDIDATE | 2 | snap-toutiao-583bb5fa98024c20171de812 |
| transsion | **REVIEW** | CANDIDATE | 2 | snap-transsion-83d84ccfb55af29785728db0 |
| tsmc | **REVIEW** | CANDIDATE | 2 | snap-tsmc-98385619ef65a81e411bd03f |
| tuya | **REVIEW** | CANDIDATE | 2 | snap-tuya-f5f9d68b1213e64622f35273 |
| twilio | **REVIEW** | CANDIDATE | 2 | snap-twilio-f7887186eddfb1d28d9fd50b |
| umc | **REVIEW** | CANDIDATE | 2 | snap-umc-827b766e6b65335456d3c796 |
| unity | **REVIEW** | CANDIDATE | 2 | snap-unity-45474e84bdd8fae20df1487a |
| venmo | **REVIEW** | CANDIDATE | 1 | snap-venmo-ad97a6f5008ebab004dbad8a |
| vipshop | **REVIEW** | CANDIDATE | 2 | snap-vipshop-73e31c6722deb6afbde50474 |
| volcengine | **REVIEW** | CANDIDATE | 2 | snap-volcengine-85d9246bf3b4a723cd3da58f |
| wangsu | **REVIEW** | CANDIDATE | 2 | snap-wangsu-36acbd26b22f7d205cc839e4 |
| wanmei | **REVIEW** | CANDIDATE | 2 | snap-wanmei-3130e157694aecca69c95383 |
| wechat | **VERIFIED** | CANDIDATE | 28 | snap-wechat-84a8d3ac3ff682614f4d7470 |
| wecom | **REVIEW** | CANDIDATE | 3 | snap-wecom-019997bd4957a3511ce1304b |
| wegame | **REVIEW** | CANDIDATE | 2 | snap-wegame-6a0efc1d4cb7e25448a923b0 |
| wetv | **REVIEW** | CANDIDATE | 2 | snap-wetv-46ca72cdff558797584c76c6 |
| workday | **REVIEW** | CANDIDATE | 2 | snap-workday-34d88e04018a5134c661c17a |
| woyun | **REVIEW** | CANDIDATE | 2 | snap-woyun-6e17d0575f55223467583fc2 |
| wps | **REVIEW** | CANDIDATE | 2 | snap-wps-861720e326a9c4914d78ecb1 |
| wuba | **REVIEW** | CANDIDATE | 2 | snap-wuba-68050641d750e38cb952057a |
| xai-grok | **REVIEW** | CANDIDATE | 1 | snap-xai-grok-0f56662ce92c5717e8909b9d |
| xbox | **REVIEW** | CANDIDATE | 42 | snap-xbox-c056e17cbe3622251ba30c82 |
| xgimi | **REVIEW** | CANDIDATE | 2 | snap-xgimi-a1305ef56fa5eead04e3b818 |
| xianyu | **REVIEW** | CANDIDATE | 2 | snap-xianyu-9c17d7cdd33a5e0cc0f5930d |
| xigua | **REVIEW** | CANDIDATE | 2 | snap-xigua-2b53bc5f66746fd60b9ab31c |
| xunlei | **REVIEW** | CANDIDATE | 2 | snap-xunlei-44fbe977943e79cd5112f682 |
| yi | **REVIEW** | CANDIDATE | 2 | snap-yi-dd113b63488e1986dceb98e6 |
| yonyou | **REVIEW** | CANDIDATE | 2 | snap-yonyou-86528b8d7bffa51440d11b83 |
| youdao | **REVIEW** | CANDIDATE | 15 | snap-youdao-fc97f5d207d4c3358c6a4d6b |
| youku | **REVIEW** | CANDIDATE | 2 | snap-youku-0bb384a769720979e5455877 |
| youtube | **REVIEW** | CANDIDATE | 175 | snap-youtube-58b8afe3b6062febd60fd519 |
| youtubemusic | **VERIFIED** | CANDIDATE | 1 | snap-youtubemusic-0e39136672e2e05e52470bd5 |
| zhaopin | **REVIEW** | CANDIDATE | 2 | snap-zhaopin-2459988d6c7729cae68826d0 |
| zhipin | **REVIEW** | CANDIDATE | 2 | snap-zhipin-7fb74eecaa4a447df440a8e2 |
| zhipu | **REVIEW** | CANDIDATE | 3 | snap-zhipu-b777d801e25dcde103be6414 |
| zte | **REVIEW** | CANDIDATE | 2 | snap-zte-95b5ec6396a3b58bdced15f1 |
<!-- SOURCE_STATUS:END -->
