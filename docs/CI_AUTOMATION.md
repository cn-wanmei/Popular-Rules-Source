# CI Automation

> **Status: Current**  
> Workflow inventory must match `.github/workflows/*.yml` on `main`.

| Workflow | Role | Production authority |
|---|---|---|
| `validate.yml` (`CI`) | configuration, schema, tests, snapshot checks | source correctness |
| `generate.yml` | scheduled/manual official refresh PR | candidate refresh |
| `release.yml` | explicit single-service Release Gate | Source Release |
| `durable-source-bridge.yml` | durable processing batch (policy-driven matrix + selective execution) | immutable Source identity (best-effort batch; see completeness) |
| `reconcile.yml` | Collection registration reconciliation | handoff evidence |
| `status.yml` | generated lifecycle report refresh | observability |
| `restore-canary-state.yml` | emergency canary SSOT restore | ops recovery |

## Terminology

| Term | Meaning |
|------|--------|
| **Production cohort** | Lifecycle production + Collection binding (SSOT: `config/source_canary_state.yaml`) |
| **Durable processing batch** | Services in `config/durable_release_policy.yaml` `default_processing_batch` |
| **Selective execution** | `workflow_dispatch.services` comma list overrides matrix |

Do **not** use the obsolete label “8-service durable seal” for the bridge matrix size.

## Ownership

Source owns its own durable seal.

Collection owns the cross-repository handoff PR, so Source does not need a cross-repository write Secret.

## Refresh contract

```text
scheduled official refresh
    ↓
generated/snapshot candidate
    ↓
CI / Source Gate
    ↓
merge to Source main
    ↓
Durable Bridge (COMPLETE | PARTIAL | FAILED)
    ↓
immutable seal artifacts
    ↓
Collection Auto Handoff
```

Maintenance-only workflow path changes are excluded from the Durable Bridge push trigger where configured.

## Durable batch completeness

| Status | Meaning |
|--------|--------|
| `COMPLETE` | All planned matrix services `PERSISTED` |
| `PARTIAL` | At least one `PERSISTED`, some incomplete/blocked |
| `FAILED` | Zero services persisted (fail-closed) |

## Fail closed

Release and handoff stop on missing artifacts, incomplete evidence, provenance mismatch, non-determinism, unresolved conflict or degraded replacement.
