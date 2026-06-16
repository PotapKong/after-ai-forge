# Repository agent instructions

This repository packages an AI development team that can be adapted to multiple
coding-agent runtimes.

When a user asks you to install, adapt, or apply this repo to another workspace:

1. Read `BOOTSTRAP.md` first.
2. Detect the target runtime:
   - Claude Code: use `claude/` plus `workspaces/CLAUDE.md`.
   - Codex or any AGENTS.md-aware coding agent: use `codex/` plus
     `workspaces/AGENTS.md`.
   - Unknown runtime: install the workspace docs and role cards, then explain
     which runtime-specific hooks could not be applied.
3. Keep the platform adapters separate. Do not make Claude instructions depend
   on Codex-only behavior, and do not make Codex instructions depend on
   Claude-only named agents.
4. Preserve the shared contract: orchestrator, six specialist roles, docs-based
   handoffs, memory recall/save where available, tests, security audit, and
   independent verification.
5. Do not commit or push unless the user explicitly asks.

When editing this repository:

- Keep `README.md` high level and human-facing.
- Keep `INSTALL.md` command-oriented.
- Keep `BOOTSTRAP.md` agent-facing and runtime-agnostic.
- Put Claude-specific material under `claude/`.
- Put Codex-specific material under `codex/`.
- Shared workspace contracts belong under `workspaces/`.
- Do not commit secrets, `.env` files, local logs, or generated memory data.
