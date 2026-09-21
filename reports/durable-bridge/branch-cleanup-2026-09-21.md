# Branch cleanup audit — 2026-09-21

This explicit cleanup commit triggers deletion of branches already classified as obsolete by the repository branch-cleanup roster.

The durable bridge ignores branch-cleanup workflow changes and durable-bridge reports, so this control-plane cleanup does not regenerate or reseal source snapshots.
