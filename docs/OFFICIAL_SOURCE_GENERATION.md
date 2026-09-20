# Official Source Generation

## Goal

The first-class capability of this repository is to derive service-domain sources from official upstream material.

## Supported input classes

- Official machine-readable lists
- Official APIs returning structured data
- Official JSON/YAML/configuration
- Official documentation
- Official web pages

The current implementation includes a safe web/JSON extractor. Additional structured adapters are added only when a service has a fixture and a contract test.

## Trust boundary

A domain found on an official page is only a candidate. The service allow policy is applied before materialization, so third-party analytics, provider infrastructure, and unrelated dependencies are not silently promoted.

## Release safety

- HTTP failures never replace a known-good source with an empty list.
- Large removals and growth bursts enter review.
- Snapshot directories are immutable once a candidate exists.
- Generated domains carry asset IDs and evidence IDs.
- Raw upstream content is stored locally for audit during generation and is intentionally not committed by default.

## Reproducibility

The stable identity of a snapshot is derived from service ID plus normalized domain content. Runtime timestamps are metadata and must not change the content identity.

## Future adapters

The adapter interface is intentionally narrow:

1. fetch
2. parse
3. extract
4. produce evidence

Client-specific rule generation stays in Popular-Rules-Collection.

## Mode B fixtures (v0.3.1)

Each first-wave service has:

```text
tests/fixtures/<service>/mode_b/official_endpoints_v1.json
tests/fixtures/<service>/mode_b/official_endpoints_v1.expected.txt
```

Parser: `adapters/official_json/mode_b.py`

Contract tests: `tests/test_mode_b.py`

Build merges Mode B fixture domains into materialization (allow-policy filtered).

## Publish

```bash
python -m source_engine generate --service taobao
python -m source_engine publish --service taobao
# → snapshots/<id>/publish.json + generated/published/taobao.json
# release_state → PUBLISHED
```
