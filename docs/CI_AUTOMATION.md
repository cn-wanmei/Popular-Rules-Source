# CI Automation Inventory

## Active workflows

| Workflow | Purpose | Write main? |
|---|---|---|
| validate.yml | Config + tests + snapshot schema + conflict + audit | No |
| generate.yml | Official source refresh | No; creates automation PR |
| reconcile.yml | Compare PRS state with Collection | No |
| release.yml | Manual service-level release artifact | No; artifact only |

## Removed

- audit.yml：与 validate/audit 合并，旧实现已无独立价值。
- build.yml：与 generate/release 的职责重复。
- fixture-only Mode B workflow path：已移除。

## Automation rule

Scheduled generation must never push directly to main.

The correct flow is:

~~~text
Schedule
  ↓
Official Fetch
  ↓
Generate
  ↓
Automation Branch
  ↓
Pull Request
  ↓
CI
  ↓
Human / Gate approval
  ↓
main
~~~

## Production readiness

当前四条 workflow 只证明工程链可运行，不证明任何服务已经 Production。

8 个目标服务均需经过 official-evidence-only qualification。
