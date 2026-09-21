# Operations

## Standard repair

    python -m source_engine gap --service taobao
    python -m source_engine repair --service taobao
    python -m source_engine generate --service taobao
    python -m source_engine schema-validate
    python -m source_engine release --service taobao

Use Gap output before repair. Repair must attach official evidence; it must never insert an unexplained domain directly into a Release.

## Verification

    python -m source_engine health
    python -m source_engine candidate-audit
    python -m source_engine conflict
    python -m source_engine reconcile
    python -m source_engine qualify

## Immutable seal

After a successful Source main change, Durable Bridge produces a persistent 8/8 service seal. Collection Auto Handoff then compares the seal against `sources/immutable_registry.yaml` and opens a normal Collection PR when the immutable identity changes.

## State

Do not maintain a second lifecycle database. Edit `config/source_canary_state.yaml` only; generated completion reports are derived evidence.