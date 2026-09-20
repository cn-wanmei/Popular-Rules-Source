# Domain Policy

## Normalization

- Lowercase, strip scheme/port/path, strip trailing dots
- IDNA / Punycode normalization
- Reject IP literals, localhost, example.com, private/malformed labels

## Allow policy

Each service declares:

- `allowed_host_exact`
- `allowed_host_suffixes`

A candidate domain must match allow policy **after** extraction.

## Classification

| Class | Enter service domain list? |
| ----- | -------------------------- |
| service | Yes |
| shared | No |
| external_dependency | No |
| provider | No |
| infrastructure | No |
| unknown | No |

## Wildcards

Only when official source explicitly expresses `*.example.com`.
Never promote `example.com` to `*.example.com` automatically.

## Removal

Official list removal → `REMOVAL_CANDIDATE` → secondary checks → explicit revoke / tombstone.
Never auto-delete on a single fetch anomaly.
