# Release Policy

## Release states

CANDIDATE / REVIEW / BLOCKED / PUBLISHED。

当前主仓库不包含任何已验证的 PUBLISHED service release。

## Hard Block

- schema error
- evidence linkage error
- unresolved conflict
- invalid domain
- empty replacement
- determinism failure
- authoring-seed-only output被误标为 Production
- exclusion / tombstone 绕过

## Review

- source fetch degraded
- large removal
- large growth
- Last Known Good retained
- seed-only domains remain

## Snapshot

Snapshot ID 内容寻址。

~~~text
snap-<service>-<content-digest>
~~~

同一 Snapshot 重跑必须复用，不得覆写。

## Release

Release Package 对同一 Snapshot 幂等。

generated/source 只是 Source Build Output，不等于 Published。

正式 Published 必须同时经过 Source Gate 与 Collection Reconciliation。

## Rollback

只切换上游采用的 Release/Snapshot，不重写历史。
