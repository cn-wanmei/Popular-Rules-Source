# P1/P2 下一批服务树执行记录 — 2026-09-26

本记录对应正式执行基线：
P1/P2 下一批服务树 → 独立子服务发现 → 自建 Source → immutable release → Collection materialization。

执行分组：
- P1: huawei-cloud, mi-cloud, jd-cloud, kugou, kuwo, quanmin-k-ge
- P2: amazonmusic, audible, goodreads, messenger, adobe-firefly, adobe-stock, adobe-fonts, openai-api, openai-platform, chatgpt, anthropic-claude, anthropic-platform, xai-grok, stripe-dashboard, venmo

发现与来源策略：
- 21 个服务在 config/p1_p2_self_built_official_wave.yaml 中具有已核验的官方入口与 exact host。
- 21 个服务在 config/self_built_services.yaml 中 upstream_binding 均为 null。
- config/source_adapters.yaml 将 21 个服务统一绑定到 self_built adapter。
- 当前 self_built/*/domains.list 均已存在；本次执行不得把 candidate 自动视为 production。
- 已存在的历史 snapshot/release 不覆盖、不改写；新 identity 必须从当前 head 产生。

本次执行目标：
1. 在专用 branch feat/service-completion-p0-p2-20260926 上运行既有 completion gate。
2. 对列出的 P1/P2 服务生成 candidate snapshot。
3. 为非历史服务建立 durable immutable release；既有 messenger 历史 release 保持不变。
4. 通过 PR 回 Main，由 Collection Source Auto Handoff 消费 durable seal。
5. 后续由 Collection Source Gate / Canary / Production 流程决定最终消费状态。

状态语义：
candidate_only != production。
review / candidate snapshot 均可保留为 durable audit evidence，但不得跳过 Collection promotion gates。
