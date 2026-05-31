# Installation Guide

## Prerequisites

- Claude Code CLI installed and authenticated
- Docker + docker compose
- Python 3.10+
- git

---

## Step 1 — Agent definitions

```bash
mkdir -p ~/.claude/agents
cp claude/agents/*.md ~/.claude/agents/
```

## Step 2 — Global CLAUDE.md

If you already have `~/.claude/CLAUDE.md`, append the dev-team section:

```bash
cat claude/CLAUDE.md >> ~/.claude/CLAUDE.md
```

If you don't have one yet:

```bash
cp claude/CLAUDE.md ~/.claude/CLAUDE.md
# Edit the User and "How to communicate" sections
```

## Step 3 — Settings (merge into ~/.claude/settings.json)

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

## Step 4 — Workspaces

```bash
mkdir -p ~/workspaces
cp workspaces/CLAUDE.md ~/workspaces/CLAUDE.md
cp workspaces/AGENTS.md ~/workspaces/AGENTS.md
cp -r workspaces/_template ~/workspaces/_template
```

## Step 5 — Dev team tooling

```bash
mkdir -p ~/workspaces/dev-team
cp -r dev-team/hooks ~/workspaces/dev-team/hooks
cp dev-team/metrics.py ~/workspaces/dev-team/metrics.py
cp -r dev-team/memory-store ~/workspaces/dev-team/memory-store

chmod +x ~/workspaces/dev-team/hooks/log-agent.sh
chmod +x ~/workspaces/dev-team/memory-store/mem
```

## Step 6 — Memory database

```bash
cd ~/workspaces/dev-team/memory-store
cp .env.example .env
# Edit .env — set POSTGRES_PASSWORD and DAEMON_SECRET

docker compose up -d

python3 -m venv .venv
.venv/bin/pip install "psycopg[binary]" fastembed
```

## Step 7 — Memory daemon autostart

### Linux / WSL

```bash
mkdir -p ~/.config/systemd/user
cp dev-team/systemd/dev-team-memory.service.template \
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

## Step 8 — Verify

```bash
~/workspaces/dev-team/memory-store/mem health
# Expected: {"ok": true}
```

## Step 9 — New project

```bash
cp -r ~/workspaces/_template ~/workspaces/my-project
# Edit ~/workspaces/my-project/CLAUDE.md — fill in stack, commands, conventions

cd ~/workspaces/my-project
# Start a Claude Code session — the team is ready
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
