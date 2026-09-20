# Tencent Boundary Model

## Related Services

Tencent Cloud / QQ Mail / QQ Music。

DingTalk 使用 Alibaba ecosystem key，不属于 Tencent Service。

## Boundary

~~~text
Tencent ecosystem
├── Tencent Cloud
├── QQ Mail
└── QQ Music
~~~

## Rules

- Tencent ASN ≠ Tencent Cloud
- gtimg.com shared CDN 不直接归属产品
- QQ Mail 只允许明确 Mail Endpoint
- QQ Music 默认限制在官方可证明的 Music Endpoint
- Tencent Cloud 先审计 Collection 已有 Registry，再补充
- 不把其他 Tencent 产品的共享基础设施直接归给 Tencent Cloud
