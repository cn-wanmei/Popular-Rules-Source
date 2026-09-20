# Security / Supply Chain

Source Repository 是进入 Collection 的数据供应链输入。

## Controls

- GitHub Actions 默认 contents: read
- 需要写入时使用最小权限
- Actions 使用固定 SHA
- Python 依赖固定版本
- Secrets 只能通过 Actions Secrets
- 外部 Source 只读取数据，不执行第三方脚本
- Source Artifact 不包含 token、cookie、私人响应
- Snapshot / Release 使用 checksum
- Scheduled Generate 不直接写 main，只能创建刷新 PR

## Threats

重点防护：

~~~text
恶意 Source
错误归属
Parser Regression
Schema Drift
Supply-chain dependency
意外删除
历史资产回流
~~~

Tombstone 永久保留。
