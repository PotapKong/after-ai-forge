# Codex adapter

This adapter turns after-ai-forge into a Codex-friendly coding team.

Codex does not need Claude-style named agent files. The main Codex session acts
as the orchestrator. When the runtime exposes parallel worker/explorer agents,
the orchestrator delegates bounded work with the role cards in
`codex/role-cards/`. When parallel agents are unavailable, it runs the same
roles as staged modes in one session.

## Install

```bash
mkdir -p ~/workspaces
cp codex/AGENTS.md ~/workspaces/AGENTS.md
cp -r workspaces/_template ~/workspaces/_template

mkdir -p ~/workspaces/dev-team/codex
cp -r codex/role-cards ~/workspaces/dev-team/codex/role-cards
```

Open a project under `~/workspaces/<project>` with Codex. The local
`AGENTS.md` should make Codex behave as the orchestrator.

## Delegation pattern

- Use `ui-designer` for UX, screen structure, states, and design specs.
- Use `frontend` for components, styling, browser behavior, accessibility, and
  client tests.
- Use `backend` for API, database, server logic, integrations, and contracts.
- Use `tester` for coverage gaps, bug hunts, and regression reports.
- Use `security` for read-only threat review, secrets, auth, data safety, and
  dependency risks.
- Use `verifier` for independent end-to-end acceptance with PASS or FAIL.

Parallel work is allowed only when write ownership is disjoint. The orchestrator
keeps the final responsibility for integration and verification.
