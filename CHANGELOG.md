# Changelog

## 0.4.0 - 2026-09-20

### Audit correction and production-boundary cleanup

- 修正“8 个服务全部 PUBLISHED”的过期状态声明。
- 明确当前 8 个首批服务均未达到 Production / Published；Tencent Cloud 保持 PARTIAL。
- 删除 fixture-only Mode B 生产接入，测试 Fixture 不再属于生产输入。
- 删除伪发布 generated/published 数据。
- 删除已废弃的 engineering / score / promotion / publish 运行路径。
- 将 Generate 改为自动创建分支并打开 PR，禁止定时任务直接修改 main。
- Snapshot / Release 改为内容寻址、不可变、幂等。
- Authoring Seed 明确为 Candidate，不再冒充官方 Evidence。
- 强化 Evidence Linkage、Override、Tombstone、Schema Validate 和变更 Gate。
- 更新 Source / Collection 双仓库边界与当前状态文档。

### Historical correction

0.3.1 曾声明“全部 8 个服务 PUBLISHED”，并将 fixture-only Mode B 合并进 Build。审计确认该路径不满足最终 Production Evidence Contract，因此这些发布资格声明已撤销。历史提交保留在 Git 历史中，当前 main 不再承认其 Production 状态。

## 0.3.x - Historical / superseded

早期版本包含 Mode B Fixture、promotion wrapper、publish wrapper 与质量评分。这些迭代已经从当前生产路径删除。
