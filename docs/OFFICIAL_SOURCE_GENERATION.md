# Official Source Generation

## Adapter priority

    official machine-readable
          ↓
    official API / structured JSON
          ↓
    official manifest / SDK
          ↓
    official documentation
          ↓
    controlled browser/JS extraction
          ↓
    auxiliary external cross-check

Only explicitly configured official origins can produce production evidence.

## Adapter contract

Each adapter must declare:

- source URL/origin;
- extraction or field-path contract;
- parser implementation;
- fixture and regression coverage;
- evidence mapping;
- deterministic output semantics.

Supported contract families include `official_web`, `official_json`, `official_api`, `official_manifest`, `official_sdk` and `official_browser`.

## Browser adapter

Browser execution is a controlled source adapter for JS-rendered official pages. It is not general crawling.

Network requests, embedded JSON and DOM values are admissible only when they resolve within the configured official boundary and can be tied to deterministic evidence metadata.

## Seed

Authoring seed is a candidate anchor only. A seed-only domain remains non-production until supported by official evidence.