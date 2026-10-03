# Security / Supply Chain

> **Status: Current**  
> Source is the Evidence Supply Layer entering Collection. Cross-repo trust: no shared secrets; Collection owns Auto Handoff.

## Controls

| Control | Implementation |
|---------|----------------|
| Default Actions permission | `contents: read` unless a job must write |
| Minimum write scope | Only jobs that commit / push |
| Actions pin | Full commit SHA only — no floating `@vN` |
| Python deps | `requirements.txt` (intent ranges) + **`requirements.lock`** (CI install) |
| Secrets | GitHub Actions Secrets only |
| Upstream fetch | Read data only; never execute third-party scripts from upstream |
| Artifacts | No tokens, cookies, or private response bodies |
| Snapshot / Release | Content digests + checksums; immutable identity |
| Scheduled generate | Opens refresh PR; does not force-push production evidence |

Pin reference (shared table): [Collection `docs/ACTIONS_SHA_PIN.md`](https://github.com/cn-wanmei/Popular-Rules-Collection/blob/main/docs/ACTIONS_SHA_PIN.md).

## Install in CI

```bash
python -m pip install -r requirements.lock
```

## Threats

```text
Malicious upstream content
Wrong service ownership attribution
Parser / schema regression
Supply-chain dependency drift
Accidental history rewrite
Legacy asset reintroduction
```

Tombstones are permanent. Snapshot / Release objects are never overwritten in place.
