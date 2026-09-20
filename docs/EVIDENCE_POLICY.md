# Evidence Policy

## Evidence grades

| Grade | Examples |
| ----- | -------- |
| S0 | Official docs, API, SDK, product page, official config/repo |
| S1 | Official technical endpoints, network docs, client config |
| S2 | High-quality external cross-check |
| S3 | Discovery-only (blogs, forums, single third-party lists) — never promote alone |

## Required fields

- evidence_id
- service_id
- asset / asset_type
- source_type / source_url
- retrieved_at
- content_hash
- confidence
- status

Large third-party document bodies are **not** mirrored permanently; store URL, title, hash, summary, and conclusion.

## Positive and negative evidence

Both must be supported:

- Why an asset belongs to the service
- Why an asset does **not** belong (shared infra, external dependency, ambiguous)

## Authority vs method vs strength

These are independent dimensions:

```yaml
source:
  authority: official
  method: official_document_extraction
evidence:
  strength: S1
generation:
  mode: extracted
```

Official authority does **not** imply every domain on the page is service-owned.
