# Source automation 分支卫生（G）

## 策略

- 前缀：`automation/source-refresh-*`
- **TTL**：合并或关闭后 **7 天** 删除远程分支
- 打开且 CI 绿的 refresh PR：优先合并；红则关闭并删分支
- 禁止长期堆积「Action required」而无审查

## 操作

```bash
gh api repos/cn-wanmei/Popular-Rules-Source/branches --paginate \
  | jq -r '.[].name' | grep '^automation/source-refresh'

gh pr list --repo cn-wanmei/Popular-Rules-Source --state open --search 'head:automation/source-refresh'
```

## 本轮

- 对打开的 automation refresh PR 执行审查或关闭，避免长期 Action required。
