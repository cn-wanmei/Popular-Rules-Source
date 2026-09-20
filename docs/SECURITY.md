# Security / Supply Chain

- Default GitHub Actions permissions: `contents: read`
- Write only on isolated release/generate jobs
- Pin action versions (prefer SHA where practical)
- Pin Python dependencies
- Secrets only via Actions secrets; never in repo or artifacts
- External sources: read data only; never execute third-party scripts
- Source artifacts must not contain tokens, cookies, or private response bodies
- Artifact checksums required on every snapshot/release
