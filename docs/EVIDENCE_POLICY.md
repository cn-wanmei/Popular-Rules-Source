# Evidence Policy

## Evidence model

Evidence is an auditable relation between an asset and an authoritative source.

Required identity dimensions:

`authority` · `source_method` · `strength` · `confidence` · `service_scope` · `content_hash` · `parser_version`.

## Production

Production-capable evidence must be official and bound to the exact service scope.

Provider, ASN, CDN and shared infrastructure evidence is not sufficient to establish Product Service ownership.

## Provenance v2

Each durable release exposes independent:

- `content_digest`
- `evidence_digest`
- `policy_digest`
- `generator_digest`
- `release_digest`

Collection verifies equality for every field before immutable acquisition.

## Negative evidence

Every exclusion decision should be explainable: shared infrastructure, external dependency, ambiguous ownership, wrong product scope or explicit policy/tombstone.

## Seed

Authoring Seed is a candidate source only. It cannot become production evidence without a valid official evidence chain.