# Source 阻塞看板（自动生成）

> generated_at: `2026-11-12T17:50:08Z`

权威：`config/source_canary_state.yaml` + `reports/generated/lifecycle.json`。

## BLOCKED

| Service | Lifecycle | Release | Domains |
|---|---|---|---:|
| — | — | — | — |

## domains = 0

| Service | Lifecycle | Release | Domains |
|---|---|---|---:|
| huawei-dns-api | REVIEW | NO_SNAPSHOT | 0 |
| huawei-ecs-api | REVIEW | NO_SNAPSHOT | 0 |
| huawei-evs-api | REVIEW | NO_SNAPSHOT | 0 |
| huawei-iam-api | REVIEW | NO_SNAPSHOT | 0 |
| huawei-ims-api | REVIEW | NO_SNAPSHOT | 0 |
| huawei-obs-api | REVIEW | NO_SNAPSHOT | 0 |
| huawei-vpc-api | REVIEW | NO_SNAPSHOT | 0 |

## 处理原则

1. 禁止用空结果覆盖 Last Known Good。
2. BLOCKED / domains=0 必须先修 adapter 或明确策略，再谈晋升。
3. Collection Source health 与本表交叉核对。
