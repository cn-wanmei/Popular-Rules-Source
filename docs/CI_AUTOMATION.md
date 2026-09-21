# CI Automation

| Workflow | Role | Production authority |
|---|---|---|
| `validate.yml` | configuration, schema, tests and snapshot checks | source correctness |
| `generate.yml` | scheduled/manual official refresh PR | candidate refresh |
| `release.yml` | explicit service Release Gate | Source Release |
| `durable-source-bridge.yml` | 8-service immutable durable seal | immutable Source identity |
| `reconcile.yml` | Collection registration reconciliation | handoff evidence |
| `phase2-gate.yml` | combined Source Gate / qualification | Source-side readiness |

## Ownership

Source owns its own durable seal.

Collection owns the cross-repository handoff PR, so Source does not need a cross-repository write Secret.

## Refresh contract

    scheduled official refresh
        ↓
    generated/snapshot candidate
        ↓
    CI / Source Gate
        ↓
    merge to Source main
        ↓
    Durable Bridge
        ↓
    immutable seal
        ↓
    Collection Auto Handoff

Maintenance-only workflow changes are excluded from the Durable Bridge trigger to prevent self-triggered persistence.

## Fail closed

Release and handoff stop on missing artifacts, incomplete evidence, provenance mismatch, non-determinism, unresolved conflict or degraded replacement.