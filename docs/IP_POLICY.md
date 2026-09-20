# IP Policy

IP and Domain tracks are separate.

## Attribution chain (required)

```text
ASN → Provider Ownership → Network Scope → Product Attribution → Evidence
```

Forbidden: `ASN → Company → Product` direct mapping.

## Scope types

- `service` — only when Service-owned, Verified, Stable, Attributable
- `provider` / `infrastructure` / `country` / `carrier` — default for ranges

Examples:

- Tencent ASN ≠ Tencent Cloud product
- Alibaba ASN ≠ 1688 product
- Cloudflare range ≠ Cloudflare-hosted product service

Current phase focuses on **domain** materialization. IP/CIDR materialization is deferred until verified service-owned ranges exist with evidence.
