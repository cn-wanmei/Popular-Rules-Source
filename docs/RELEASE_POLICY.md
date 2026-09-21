# Release Policy

## Release states

`CANDIDATE` → `PUBLISHED` is valid only for a fully evidenced immutable snapshot.
`REVIEW` and `BLOCKED` never enter the durable release.

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