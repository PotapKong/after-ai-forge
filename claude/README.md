# Claude Code adapter

This adapter is the native after-ai-forge setup for Claude Code.

Claude Code gets real named departments from `claude/agents/*.md`. The main
Claude Code session acts as the orchestrator, delegates to the six specialists,
and uses the shared workspace contract in `workspaces/`.

## Install

```bash
mkdir -p ~/.claude/agents
cp claude/agents/*.md ~/.claude/agents/
cat claude/CLAUDE.md >> ~/.claude/CLAUDE.md

mkdir -p ~/workspaces
cp workspaces/CLAUDE.md ~/workspaces/CLAUDE.md
cp workspaces/AGENTS.md ~/workspaces/AGENTS.md
cp -r workspaces/_template ~/workspaces/_template
```

Merge `claude/settings.json` into `~/.claude/settings.json` if you want the
SubagentStop observability hook.

## Departments

- `ui-designer`: UX/UI specs and design system.
- `frontend`: components, client logic, and frontend tests.
- `backend`: API, database, server logic, and contracts.
- `tester`: tests and systematic bug hunting.
- `security`: read-only STRIDE-style audit.
- `verifier`: independent acceptance with PASS or FAIL.
