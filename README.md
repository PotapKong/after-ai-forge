# after-ai-forge 🔥

**AI dev team with persistent memory — run by Claude Code.**

An orchestrator + 6 specialized sub-agents + 3-level memory system that learns across projects.

```
Orchestrator (main session)
├── ui-designer   — UX/UI specs, design system
├── frontend      — components, client logic         ← TDD-first
├── backend       — API, DB, server logic             ← TDD-first
├── tester        — tests, bug hunting                ← systematic debug protocol
├── security      — read-only STRIDE audit
└── verifier      — independent acceptance (PASS/FAIL)

Memory
├── Level 1 — personal per-agent (Claude Code native)
├── Level 2 — project docs/ under git
└── Level 3 — central cross-project Postgres + pgvector (semantic search)
```

## Why this beats generic agent setups

| Feature | Generic | after-ai-forge |
|---|---|---|
| Domain specialists | ❌ | ✅ 6 agents |
| Cross-project memory | ❌ | ✅ pgvector semantic |
| File handoff protocol | ❌ | ✅ docs/ contracts |
| Bug tracking + lessons | ❌ | ✅ lessons.md |
| Security audit | ❌ | ✅ STRIDE |
| Independent acceptance | ❌ | ✅ verifier |
| Observability | ❌ | ✅ hooks + metrics |
| TDD enforcement | ❌ | ✅ RED→GREEN→REFACTOR |
| Requirements before pipeline | ❌ | ✅ Step 0 |

## Quick start

```bash
git clone https://github.com/PotapKong/after-ai-forge
cd after-ai-forge

# 1. Copy agent definitions
cp -r claude/agents ~/.claude/agents

# 2. Merge claude/CLAUDE.md into your ~/.claude/CLAUDE.md

# 3. Set up workspaces
mkdir -p ~/workspaces
cp workspaces/CLAUDE.md ~/workspaces/CLAUDE.md
cp workspaces/AGENTS.md ~/workspaces/AGENTS.md
cp -r workspaces/_template ~/workspaces/_template

# 4. Start memory (requires Docker)
cd dev-team/memory-store
cp .env.example .env          # fill in your passwords
docker compose up -d
python3 -m venv .venv
.venv/bin/pip install "psycopg[binary]" fastembed
chmod +x mem

# 5. Enable systemd service (Linux/WSL)
cp dev-team/systemd/dev-team-memory.service.template \
   ~/.config/systemd/user/dev-team-memory.service
# edit ExecStart path, then:
systemctl --user daemon-reload
systemctl --user enable --now dev-team-memory

# 6. Verify
./dev-team/memory-store/mem health   # {"ok": true}
```

See [INSTALL.md](INSTALL.md) for detailed per-OS instructions.

## Architecture

```
~/workspaces/
  CLAUDE.md          orchestrator instructions + Step 0 protocol
  AGENTS.md          ownership contracts + handoff protocols
  _template/         new project skeleton
  <project>/
    CLAUDE.md        project stack + conventions
    docs/
      design/        ui-designer output
      api/           backend contracts
      test-report/   tester reports
      security/      STRIDE audits
      verify/        PASS/FAIL verdicts
      lessons.md     bug log + lessons learned

~/.claude/
  CLAUDE.md          global profile + standards
  agents/            6 agent definitions
  settings.json      permissionMode + observability hook

~/workspaces/dev-team/
  memory-store/      Postgres + pgvector + daemon + client
  hooks/             SubagentStop log hook
  metrics.py         repeated-mistake rate + activity metrics
```

## Feature pipeline

```
Step 0: requirements clarification
  └─► ui-designer → docs/design/<feature>-spec.md
       ├─► backend  (worktree-A) → docs/api/<feature>.md
       └─► frontend (worktree-B) reads spec + contract
            └─► tester: coverage + bug hunt
                 └─► security: STRIDE audit (read-only)
                      └─► verifier: PASS/FAIL
                           └─► orchestrator: synthesis report
```

## Memory protocol

Every agent, before each task:
```bash
mem recall "<task summary>" [--project <name>]
```

Every agent, after each task:
```bash
echo '{"kind":"lesson","project":"<name>","title":"...","lesson":"..."}' | mem save
```

## Requirements

- Claude Code CLI with agent support
- Docker + docker compose
- Python 3.10+
- ~2 GB disk

## License

MIT
