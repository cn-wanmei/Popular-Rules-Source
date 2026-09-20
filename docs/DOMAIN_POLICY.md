# Domain Policy

## Normalization

统一进行：

- lower-case
- strip scheme/path/query/fragment
- strip trailing dot
- IDNA / Punycode
- reject IP literals
- reject malformed labels
- reject example / localhost

## Allow Policy

每个 Service 至少定义：

- allowed_host_exact
- allowed_host_suffixes

Candidate 提取以后再执行 Allow Policy。

## Classification

| Classification | Service List |
|---|---|
| service | Yes |
| shared | No |
| external_dependency | No |
| provider | No |
| infrastructure | No |
| candidate | Review only |
| unknown | No |

## Wildcard

只有源数据明确表达 wildcard 才保留 wildcard 语义。

绝不从 apex 自动扩大为 wildcard。

## Override

Override 必须有 reason 或 evidence，并重新经过 Service Allow Policy、Exclusion 和 Tombstone。

## Removal

~~~text
Official removed
   ↓
REMOVAL_CANDIDATE
   ↓
Secondary Verification
   ↓
Explicit Revoke
   ↓
Tombstone
~~~
