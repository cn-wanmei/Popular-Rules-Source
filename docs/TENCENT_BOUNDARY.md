# Tencent Boundary Model

## First-wave related services

- tencentcloud
- qqmail
- qqmusic
- dingding (DingTalk; Alibaba-owned product, historically listed with enterprise messaging — treated under its own ecosystem key `alibaba` in config but audited against Tencent overlap for QQ-family only)

## Rules

1. `Tencent ASN` ≠ `tencentcloud` product scope.
2. Shared static CDN (`gtimg.com`) excluded from product lists.
3. QQ Mail uses exact hosts (imap/smtp/pop/mail); do not expand to all `qq.com`.
4. QQ Music limited to `y.qq.com` family unless official evidence for additional music endpoints.
5. Tencent Cloud: audit Collection registry first; supplement rather than duplicate.
