# Promotion Contract

## Direction

```text
Popular-Rules-Source Release
        →
Promotion Bridge
        →
Popular-Rules-Collection Source Registry / Collection input
```

This project never writes Canonical or client generated/ trees in Collection.

## Gate checklist before promotion

- Schema PASS
- Evidence PASS
- Ownership PASS
- Boundary PASS
- Exclusion PASS
- Duplicate PASS
- Conflict PASS
- Reconciliation PASS
- Deterministic PASS

Any FAIL → BLOCK.

## Compatibility

Source Release schema version must remain readable by Collection adapter v1.x.
Breaking field changes require MAJOR version bump and coordinated adapter update.
