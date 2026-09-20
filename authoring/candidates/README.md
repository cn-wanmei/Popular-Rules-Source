# Discovery Candidate Ledger

该目录只保存缺失规则补全候选，不是 Production Source。

规则：

- candidate 不等于 production。
- promoted 必须携带 evidence_ids。
- 候选可以来自官方 Discovery、官方文档/API/SDK、Runtime Observation 或外部交叉验证。
- 正式 Materialization 仍必须经过 Source Engine。
- 不得把第三方规则集直接当作官方 Evidence。
- 每个服务使用一个 <service>.jsonl，每行一个 JSON Candidate。
