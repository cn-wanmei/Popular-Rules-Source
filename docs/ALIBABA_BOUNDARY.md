# Alibaba Boundary Model

## Services in first wave

- 1688
- taobao
- tmall
- cainiao

## Rules

1. Ecosystem membership ≠ product ownership.
2. Shared CDN (`alicdn.com`, `tbcdn.cn`, …) never enters a single-service domain list.
3. Parent hosts (`alibaba.com`) stay outside product materialization unless service-specific evidence exists.
4. Cross-candidates among 1688 / taobao / tmall / cainiao → `CONFLICT` until resolved with evidence.
5. Cainiao logistics endpoints must not be attributed to Taobao/1688 solely by corporate ownership.

## 1688 sample scope (Phase 3)

In-scope suffixes: `*.1688.com` after official evidence + allow policy.
Out-of-scope: Alibaba CDN, generic Alibaba login/gateway without 1688 product context.
