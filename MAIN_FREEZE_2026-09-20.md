# Main Freeze — 2026-09-20

Popular-Rules-Source main is frozen for Phase 2.

Scheduled / manual production writers are disabled on main. Validation may continue on branches and PRs.

## Development

All implementation goes to phase2/* branches and returns through Pull Request.

## Activation

Main can resume Source generation only after:

1. live official Source is verified
2. seed-only assets = 0 for promoted services
3. Evidence and Boundary gates pass
4. Snapshot determinism passes
5. Collection reconciliation passes
6. production activation is explicitly approved

## Repository protection

The current connected GitHub interface cannot mutate branch-protection/ruleset administration settings. Therefore workflow writers are frozen, but real branch protection still needs to be enabled in GitHub repository settings.
