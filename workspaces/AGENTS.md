# AGENTS.md — team coordination contract

## File ownership
| Agent | Owns (writes) | Does not touch |
|---|---|---|
| ui-designer | docs/design/** | code, API, tests |
| backend | server code, DB, migrations, docs/api/** | client code |
| frontend | client code, components | server code, DB |
| tester | tests | prod code |
| security | docs/security/** only — everything else read-only | any code |
| verifier | docs/verify/** only — everything else read-only + run | any code |

Two agents never edit the same file. Parallel work — in separate git-worktrees.

## Handoff protocols (via files)
- Design: ui-designer → docs/design/<feature>-spec.md → read by frontend.
- API contract: backend → docs/api/<feature>.md → read by frontend.
- Test report: tester → docs/test-report/<feature>.md.
- Audit: security → docs/security/<feature>.md.
- Verdict: verifier → docs/verify/<feature>.md (PASS/FAIL).

## Memory protocol (each agent, every task)
- Before task:
  ```bash
  ~/workspaces/dev-team/memory-store/mem recall "<task summary>" [--project <name>]
  ```
  Also read `docs/lessons.md` for the project; review personal memory.
- After task (bug found or lesson learned):
  ```bash
  echo '{"kind":"lesson","project":"<name>","title":"...","symptom":"...","lesson":"..."}' \
    | ~/workspaces/dev-team/memory-store/mem save
  # Also write to docs/lessons.md
  ```

## Never (all agents)
- Do not commit secrets or .env files.
- Do not push to main directly — branches: feat/*, fix/*, refactor/*.
- Do not touch files outside your ownership zone.
- Do not assume scope or approach — ask.
