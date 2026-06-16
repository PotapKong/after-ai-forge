# Agent bootstrap

Give this repository to a coding agent and ask it to install the dev-team setup.
This file is the agent-facing runbook.

## Goal

Configure a project workspace with:

- one orchestrator session;
- six specialist departments: `ui-designer`, `frontend`, `backend`, `tester`,
  `security`, and `verifier`;
- docs-based handoffs so parallel work does not collide;
- optional cross-project memory through `dev-team/memory-store`;
- verification habits that make "done" mean tested and accepted.

## Runtime detection

Detect the agent runtime before copying files.

| Runtime | Signal | Adapter |
|---|---|---|
| Claude Code | `~/.claude`, `CLAUDE.md`, named sub-agent support | `claude/` |
| Codex | `AGENTS.md`, Codex desktop/CLI, generic worker/explorer agents | `codex/` |
| Unknown | no clear platform files | shared `workspaces/` + role cards |

If the runtime cannot be detected, install the shared workspace contract and ask
the human which adapter-specific global config they want.

## Claude Code setup

1. Copy named agent definitions:
   ```bash
   mkdir -p ~/.claude/agents
   cp claude/agents/*.md ~/.claude/agents/
   ```
2. Merge or copy the global Claude profile:
   ```bash
   cat claude/CLAUDE.md >> ~/.claude/CLAUDE.md
   ```
3. Merge `claude/settings.json` into `~/.claude/settings.json` if hooks are
   desired.
4. Copy shared workspace files:
   ```bash
   mkdir -p ~/workspaces
   cp workspaces/CLAUDE.md ~/workspaces/CLAUDE.md
   cp workspaces/AGENTS.md ~/workspaces/AGENTS.md
   cp -r workspaces/_template ~/workspaces/_template
   ```

Claude Code gets real named departments through `~/.claude/agents/*.md`.

## Codex setup

1. Copy the Codex workspace instruction file:
   ```bash
   mkdir -p ~/workspaces
   cp codex/AGENTS.md ~/workspaces/AGENTS.md
   ```
   If `~/workspaces/AGENTS.md` already exists, merge the Codex dev-team
   sections instead of overwriting local workspace rules.
2. Copy the shared project template:
   ```bash
   cp -r workspaces/_template ~/workspaces/_template
   ```
3. Copy role cards for reusable delegation prompts:
   ```bash
   mkdir -p ~/workspaces/dev-team/codex
   cp -r codex/role-cards ~/workspaces/dev-team/codex/role-cards
   ```
4. Start Codex inside a project under `~/workspaces/<project>`. Codex should
   read `AGENTS.md` and act as the orchestrator.

Codex may not expose fixed named agents. When parallel sub-agents are available,
the orchestrator uses generic workers/explorers with the role cards. When they
are not available, the orchestrator runs the same departments as staged modes in
one session.

## Shared memory setup

Memory is optional but recommended.

```bash
mkdir -p ~/workspaces/dev-team
cp -r dev-team/hooks ~/workspaces/dev-team/hooks
cp dev-team/metrics.py ~/workspaces/dev-team/metrics.py
cp -r dev-team/memory-store ~/workspaces/dev-team/memory-store

chmod +x ~/workspaces/dev-team/hooks/log-agent.sh
chmod +x ~/workspaces/dev-team/memory-store/mem
```

Then:

```bash
cd ~/workspaces/dev-team/memory-store
cp .env.example .env
# Edit .env and set POSTGRES_PASSWORD and DAEMON_SECRET.
docker compose up -d
python3 -m venv .venv
.venv/bin/pip install "psycopg[binary]" fastembed
./mem health
```

If this fails, continue without Level 3 memory and use project docs:
`docs/lessons.md`, `docs/design/`, `docs/api/`, `docs/test-report/`,
`docs/security/`, and `docs/verify/`.

## New project setup

```bash
cp -r ~/workspaces/_template ~/workspaces/my-project
cd ~/workspaces/my-project
```

Fill the project `CLAUDE.md` or local project instructions with stack, commands,
test entry points, deploy notes, and known constraints.

## Operating model

For substantial work:

1. Orchestrator clarifies acceptance criteria.
2. `ui-designer` writes `docs/design/<feature>-spec.md`.
3. `backend` and `frontend` work in parallel when their write sets do not
   overlap; backend writes `docs/api/<feature>.md`.
4. `tester` writes or runs tests and records `docs/test-report/<feature>.md`.
5. `security` performs a read-only STRIDE-style review in
   `docs/security/<feature>.md`.
6. `verifier` runs the final acceptance flow and writes
   `docs/verify/<feature>.md` with PASS or FAIL.
7. Orchestrator integrates, fixes gaps, and reports exactly what was verified.

## Verification

The setup is ready when:

- the target workspace has an `AGENTS.md` and/or `CLAUDE.md`;
- the project template contains `docs/lessons.md`;
- role handoff folders exist or can be created under `docs/`;
- memory health returns `{"ok": true}` or the agent explicitly reports that
  memory is unavailable and project docs will be used instead.
