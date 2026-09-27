# applemedia hostname reconciliation (2026-09-27)

## Finding
`applemedia` is an **upstream composite** rule (blackmatrix7 AppleMedia list), not an independent product with a single official hostname family.

Generated domains already overlap:
- `applemusic.*` / music streaming hosts → covered by `applemusic`
- `applenews.*` → covered by `applenews`
- `appletv.*` → covered by `appletv`

## Decision
- **Do not** create a new brand Icon Identity or primary service tree for `applemedia`.
- Keep hierarchy node as **aggregate / legacy upstream** coverage only.
- Prefer independent services: `applemusic`, `appletv`, `applenews`, `applepodcasts`, `applebooks`.
- No durable production binding required for `applemedia` as a separate service_id for Collection rule materialization.
