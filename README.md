# Popular Rules Source

<p align="center">
  <img src="https://img.shields.io/badge/Layer-Evidence%20Supply-0d9488?style=for-the-badge" alt="Evidence" />
  <img src="https://img.shields.io/badge/SSOT-source_canary_state-1e293b?style=for-the-badge" alt="SSOT" />
  <img src="https://img.shields.io/badge/Seal-Immutable-6366f1?style=for-the-badge" alt="Immutable" />
  <img src="https://img.shields.io/badge/Handoff-Collection--owned-64748b?style=for-the-badge" alt="Handoff" />
</p>

<p align="center">
  <strong>官方证据 · Snapshot · Durable Release · Immutable Seal</strong><br/>
  <sub>Evidence Supply Layer for Popular-Rules-Collection</sub>
</p>

---

## 定位

**Popular Rules Source** 是 **Evidence Supply Layer**。

本仓库负责：

- 官方来源发现
- 官方 Evidence 收集
- Gap Detection / Repair
- Snapshot / Durable Release
- Immutable Seal / Provenance
- Collection Handoff

> Source **不是**用户下载仓。  
> 最终用户规则消费入口属于 **[Popular-Rules-Collection](https://github.com/cn-wanmei/Popular-Rules-Collection)**。

---

## 权威状态

| 内容 | SSOT |
|------|------|
| Source lifecycle | [`config/source_canary_state.yaml`](config/source_canary_state.yaml) |
| Static service definition | [`config/services.yaml`](config/services.yaml) |
| Durable Release | `releases/<service>/<snapshot_id>/` |
| Immutable Snapshot | `releases/<service>/<snapshot_id>/` |
| Provenance | Snapshot / Release metadata |

- `config/source_canary_state.yaml` 是**生命周期 SSOT**
- `config/services.yaml` 仅保存**静态 Service Definition**

> README **不手写**服务数量、Lifecycle 数量或 Release 数量。

---

## 状态机

```text
REVIEW ──→ VERIFIED ──→ CANARY ──→ PRODUCTION
              │             │
              └─────────────┴────→ BLOCKED
```

| 状态 | 语义 |
|------|------|
| **REVIEW** | 已建立候选，但仍需证据完善 |
| **VERIFIED** | Evidence 完整，可进入 Canary 候选 |
| **CANARY** | Source 可进行试运行 / Handoff |
| **PRODUCTION** | Durable + Collection binding 完成 |
| **BLOCKED** | 证据断流、domains=0 或策略阻塞 |

### 晋升规则

```text
REVIEW → VERIFIED → CANARY → PRODUCTION
```

**禁止跳级。** Source lifecycle 只描述 Source 自身状态，**不能**直接宣称 Collection Production。

完整规则： [Collection · SOURCE_COLLECTION_FUNNEL](https://github.com/cn-wanmei/Popular-Rules-Collection/blob/main/docs/SOURCE_COLLECTION_FUNNEL.md)

---

## 证据生产链

```text
Official Source
      ↓
Discovery
      ↓
Evidence
      ↓
Candidate
      ↓
Completeness Gate
      ↓
Snapshot
      ↓
Durable Release
      ↓
Immutable Seal
      ↓
Collection Auto Handoff
```

---

## Immutable Identity

Source Release 使用多层 provenance：

```text
content_digest
evidence_digest
policy_digest
generator_digest
```

最终 Release identity：

```text
release_digest = identity(content, evidence, policy, generator)
```

规则：

- 老 Snapshot / Release **永不覆写**
- 相同 identity 重跑必须可复用
- provenance 变化必须产生新的 immutable identity
- 不完整 Evidence **不得**进入 Release

---

## 与 Collection 的边界

| 问题 | 答案 |
|------|------|
| 用户下载规则？ | → Collection |
| 用户使用客户端规则？ | → Collection `generated/` |
| 官方来源证据？ | → Source |
| Snapshot / Durable Release？ | → Source |
| Immutable Handoff？ | → Source → Collection |
| Collection Canonical / IR？ | → Collection |

Source **不直接写**：

- Collection Canonical
- Collection IR
- Collection `generated/`
- 最终客户端目录

---

## 当前运行状态

首页不手写服务列表或 Lifecycle 数量。当前状态直接读取 SSOT / CI 生成结果。

| 状态域 | 入口 |
|--------|------|
| Lifecycle | [`config/source_canary_state.yaml`](config/source_canary_state.yaml) |
| Gap | `python -m source_engine gap --service <service>` |
| Health | `python -m source_engine health` |
| Qualification | `python -m source_engine qualify` |
| Blocked board | [`docs/BLOCKED_BOARD.md`](docs/BLOCKED_BOARD.md) |
| Reconcile | `python -m source_engine reconcile` |

---

## 关键工作流

| Workflow | 用途 | 触发 |
|----------|------|------|
| Durable Source Bridge | Durable Source 持久化 | push / dispatch |
| Release Gate | 单服务 Release 候选 | dispatch |
| Emergency Restore Canary State | 恢复 Canary SSOT | dispatch |
| Reconcile | 与 Collection 对齐报告 | schedule / dispatch |

详细工作流： [`.github/workflows/`](.github/workflows/)

---

## CLI

```bash
python -m source_engine validate
python -m source_engine gap --service taobao
python -m source_engine generate --service taobao
python -m source_engine repair --service taobao
python -m source_engine release --service taobao
python -m source_engine reconcile
python -m source_engine health
python -m source_engine qualify
pytest -q
```

---

## 生产不变量

- 官方证据优先，不猜 Service Ownership
- Provider / ASN / CDN 不能直接转化为 Product Service
- Fetch 失败不得用空结果覆盖 Last Known Good
- Candidate 无完整 Evidence 不得进入 Release
- Snapshot / Release immutable
- Collection binding 必须 exact SHA + exact provenance equality
- 跨仓库自动交接由 Collection 持有
- 不依赖跨仓库 Secret

---

## 文档

| 文档 | 用途 |
|------|------|
| [`docs/INDEX.md`](docs/INDEX.md) | 文档入口 |
| [`docs/BLOCKED_BOARD.md`](docs/BLOCKED_BOARD.md) | 阻塞看板 |
| [`source_engine/`](source_engine/) | Source Engine |
| [`config/source_canary_state.yaml`](config/source_canary_state.yaml) | Lifecycle SSOT |
| [`config/services.yaml`](config/services.yaml) | 静态服务定义 |

---

## 关联项目仓库

| 仓库 | 关系 |
|------|------|
| [Popular-Rules-Collection](https://github.com/cn-wanmei/Popular-Rules-Collection) | 最终用户规则、Canonical、客户端构建与 Production |
| [Popular-Rules-Icon](https://github.com/cn-wanmei/Popular-Rules-Icon) | Icon 资产基础设施；通过 Collection identity 间接关联 |

```text
Official Evidence
       ↓
Popular-Rules-Source
       │
       │ Immutable Seal / Handoff
       ▼
Popular-Rules-Collection
       │
       │ Canonical Identity
       ▼
Popular-Rules-Icon
```

---

<sub>README 描述制度与入口；动态数字与覆盖率以各仓 SSOT / CI 生成为准。</sub>

<!-- SOURCE_STATUS:START -->
### Source lifecycle (summary)

> 完整 per-service 表不再内嵌 README（体积与过期风险）。权威数据：
> [`config/source_canary_state.yaml`](config/source_canary_state.yaml)

生成摘要请运行：

```bash
python -m source_engine health
python -m source_engine qualify
# 或维护 scripts 生成 reports/lifecycle_summary.md 后由 CI 写入本区
```

阻塞与缺口：[`docs/BLOCKED_BOARD.md`](docs/BLOCKED_BOARD.md)

| 口径 | 入口 |
|------|------|
| Lifecycle SSOT | `config/source_canary_state.yaml` |
| Static definitions | `config/services.yaml` |
| Collection funnel | [Collection SOURCE_COLLECTION_FUNNEL](https://github.com/cn-wanmei/Popular-Rules-Collection/blob/main/docs/SOURCE_COLLECTION_FUNNEL.md) |

<!-- SOURCE_STATUS:END -->
