# poc-agents-orchestration

CI updates summary:
- Feature workflow (.github/workflows/feature.yml): split into `feature-build` and `feature-unit-tests`; after successful jobs, CI creates/updates a PR from the triggering feature branch → `main` (labels/assignees inferred).
- Main workflow (.github/workflows/main.yml): runs on `main`, builds, tests and performs semantic releases (tags + GitHub Release) when conventional commits indicate a bump.

Notes:
- CI may push an updated `README.md` containing `coverage.svg` from feature branches when coverage is generated.
- Workflows use `GITHUB_TOKEN` with contents: write and pull-requests: write. If permissions are restricted, add a PAT in `secrets.PERSONAL_ACCESS_TOKEN`.

See docs/ci.md and docs/agents.md for details.
