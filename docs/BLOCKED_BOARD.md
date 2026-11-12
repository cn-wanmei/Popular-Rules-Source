# Source 阻塞看板（自动生成）

> generated_at: `2026-11-12T17:02:08Z`

权威：`config/source_canary_state.yaml` + `reports/generated/lifecycle.json`。

## BLOCKED

| Service | Lifecycle | Release | Domains |
|---|---|---|---:|
| — | — | — | — |

## domains = 0

| Service | Lifecycle | Release | Domains |
|---|---|---|---:|
| — | — | — | — |

## 处理原则

1. 禁止用空结果覆盖 Last Known Good。
2. BLOCKED / domains=0 必须先修 adapter 或明确策略，再谈晋升。
3. Collection Source health 与本表交叉核对。
