# Release Policy

## Release states

`CANDIDATE` → Qualified Durable Release (handoff-eligible to Collection) is valid only for a fully evidenced immutable snapshot.

| State | Written under `releases/` | Collection handoff |
|-------|---------------------------|--------------------|
| `CANDIDATE` | Yes — Qualified Durable Release | Eligible (`handoff_eligible=true`) |
| `REVIEW` | Yes — **audit archive only** | **Not eligible** (`handoff_eligible=false`) |
| `BLOCKED` | No — fail-closed at release layer | Not eligible |

`REVIEW` snapshots may be retained as durable audit evidence so that incomplete or in-review candidates are not discarded. They must not be treated as promotable releases for Collection binding. `BLOCKED` is always rejected by `create_release`.

## Release identity v2

The release identity is derived from:

- content digest
- evidence digest
- policy digest
- generator digest

and is sealed as `release_digest`.

The Source persistence commit is the immutable transport identity used by Collection. It is intentionally distinct from the verified input commit used to prove the Source Gate.

## Hard blocks

- schema or contract failure;
- unresolved conflict;
- missing or incomplete official evidence;
- empty or unsafe replacement;
- non-deterministic output;
- seed-only output presented as production;
- provenance equality failure;
- missing durable artifacts.

## Rollback

Rollback changes the Collection binding to a previously verified immutable Source release. Historical Source snapshots are never rewritten.