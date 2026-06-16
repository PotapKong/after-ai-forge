# Installation Guide

## Prerequisites

- Claude Code CLI installed and authenticated, or Codex / an AGENTS.md-aware coding agent
- Docker + docker compose
- Python 3.10+
- git

---

## Agent-driven install

If you want your coding agent to do the setup, give it this repository and ask:

```text
Read BOOTSTRAP.md, detect your runtime, install the matching after-ai-forge
adapter, create the workspace template, configure optional memory if possible,
and verify the result.
```

Use the manual sections below when you want to do the setup yourself.

---

## Claude Code adapter

### Step 1 — Agent definitions

```bash
mkdir -p ~/.claude/agents
cp claude/agents/*.md ~/.claude/agents/
```

### Step 2 — Global CLAUDE.md

If you already have `~/.claude/CLAUDE.md`, append the dev-team section:

```bash
cat claude/CLAUDE.md >> ~/.claude/CLAUDE.md
```

If you don't have one yet:

```bash
cp claude/CLAUDE.md ~/.claude/CLAUDE.md
# Edit the User and "How to communicate" sections
```

### Step 3 — Settings (merge into ~/.claude/settings.json)

Add the hooks section from `claude/settings.json`:

```json
{
  "permissionMode": "auto",
  "hooks": {
    "SubagentStop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "bash ~/workspaces/dev-team/hooks/log-agent.sh",
            "timeout": 5
          }
        ]
      }
    ]
  }
}
```

### Step 4 — Workspaces

```bash
mkdir -p ~/workspaces
cp workspaces/CLAUDE.md ~/workspaces/CLAUDE.md
cp workspaces/AGENTS.md ~/workspaces/AGENTS.md
cp -r workspaces/_template ~/workspaces/_template
```

---

## Codex adapter

Codex uses `AGENTS.md` as the workspace contract. If parallel worker/explorer
agents are available, the orchestrator uses the role cards. Otherwise it runs
the same departments as staged modes in one session.

### Step 1 — Workspace instructions

```bash
mkdir -p ~/workspaces
cp codex/AGENTS.md ~/workspaces/AGENTS.md
```

If `~/workspaces/AGENTS.md` already exists, merge the Codex dev-team sections
instead of overwriting local rules.

### Step 2 — Template and role cards

```bash
cp -r workspaces/_template ~/workspaces/_template
mkdir -p ~/workspaces/dev-team/codex
cp -r codex/role-cards ~/workspaces/dev-team/codex/role-cards
```

Start Codex inside `~/workspaces/<project>`. The main session is the
orchestrator; specialist departments are delegated to workers when the runtime
supports it and emulated as staged modes otherwise.

---

## Shared dev-team tooling

### Step 1 — Copy tooling

```bash
mkdir -p ~/workspaces/dev-team
cp -r dev-team/hooks ~/workspaces/dev-team/hooks
cp dev-team/metrics.py ~/workspaces/dev-team/metrics.py
cp -r dev-team/memory-store ~/workspaces/dev-team/memory-store
cp -r dev-team/systemd ~/workspaces/dev-team/systemd

chmod +x ~/workspaces/dev-team/hooks/log-agent.sh
chmod +x ~/workspaces/dev-team/memory-store/mem
```

### Step 2 — Memory database

```bash
cd ~/workspaces/dev-team/memory-store
cp .env.example .env
# Edit .env — set POSTGRES_PASSWORD and DAEMON_SECRET

docker compose up -d

python3 -m venv .venv
.venv/bin/pip install "psycopg[binary]" fastembed
```

### Step 3 — Memory daemon autostart

### Linux / WSL

```bash
mkdir -p ~/.config/systemd/user
cp ~/workspaces/dev-team/systemd/dev-team-memory.service.template \
   ~/.config/systemd/user/dev-team-memory.service
# Edit the file: replace YOUR_USER with your actual username

systemctl --user daemon-reload
systemctl --user enable --now dev-team-memory
```

### macOS (launchd)

Create `~/Library/LaunchAgents/dev-team-memory.plist`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
  "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key><string>dev-team-memory</string>
  <key>ProgramArguments</key>
  <array>
    <string>/Users/YOUR_USER/workspaces/dev-team/memory-store/.venv/bin/python</string>
    <string>/Users/YOUR_USER/workspaces/dev-team/memory-store/memory_daemon.py</string>
  </array>
  <key>RunAtLoad</key><true/>
  <key>KeepAlive</key><true/>
</dict>
</plist>
```

```bash
launchctl load ~/Library/LaunchAgents/dev-team-memory.plist
```

### Windows (manual or Task Scheduler)

```powershell
# Start in background (run once per session)
Start-Process python -ArgumentList "C:\Users\YOUR_USER\workspaces\dev-team\memory-store\memory_daemon.py" -WindowStyle Hidden
```

## Verify

```bash
~/workspaces/dev-team/memory-store/mem health
# Expected: {"ok": true}
```

Also verify the workspace contract:

```bash
test -f ~/workspaces/AGENTS.md || test -f ~/workspaces/CLAUDE.md
test -f ~/workspaces/_template/docs/lessons.md
```

## New project

```bash
cp -r ~/workspaces/_template ~/workspaces/my-project
# Edit ~/workspaces/my-project/CLAUDE.md or local project instructions:
# fill in stack, commands, conventions, and acceptance checks.

cd ~/workspaces/my-project
# Start Claude Code or Codex here. The team is ready.
```

---

## Troubleshooting

**Daemon not starting:** Check Docker is running and `.env` has passwords set.

**`mem health` connection error:** Daemon not running. Check:
```bash
systemctl --user status dev-team-memory
journalctl --user -u dev-team-memory -n 50
```

**Agents not in Claude Code:** Verify `~/.claude/agents/*.md` exist and restart Claude Code.

**Codex is not using the team:** Verify the active workspace has an `AGENTS.md`
that includes the Codex dev-team instructions, then restart the Codex session in
that workspace.
