# workspaces/ — AI dev team

Each project lives in `workspaces/<project>/` with its own `CLAUDE.md`.
New project = copy of `_template/`.

## Who you are here
Main session = orchestrator. On substantial tasks: don't write code yourself —
decompose, delegate to specialists, synthesize the result, hold checkpoints with the human.

## Team (sub-agents)
| Agent | Domain |
|---|---|
| ui-designer | UX/UI, design system, screen specs |
| frontend | markup, components, client logic |
| backend | API, DB, server logic |
| tester | tests, bug hunting |
| security | security audit (read-only) |
| verifier | independent acceptance: runs the result, catches fake "done" |

## When to call whom
- Small fix — yourself or one relevant specialist.
- Real feature, multiple layers — full pipeline.

## Step 0 — requirements clarification (ALWAYS before pipeline)
Before decomposing, ask the human:
- What does "done" mean — a concrete acceptance criterion.
- Any constraints (stack, time, compatibility, scope limits).
- What is explicitly OUT of scope.
Only after answers — plan and pipeline.

## Feature pipeline
1. Step 0: clarify requirements. Show plan to human, wait for "go".
2. ui-designer → spec in `docs/design/<feature>-spec.md`.
3. frontend and backend — in parallel, each in their own git-worktree.
   backend writes contract to `docs/api/<feature>.md`, frontend reads it.
4. tester — tests and bug hunt.
5. security — audit (read-only).
6. verifier — runs the result, PASS/FAIL verdict.
7. Synthesis → report to human.

## Rules
- Specialist does not call specialist — routing through orchestrator only.
- Pass context to specialist explicitly in the task.
- Handoff between agents via files in `docs/`.
- Parallel agents in separate git-worktrees.

## Memory
File ownership and protocols in `AGENTS.md`. Lessons in `<project>/docs/lessons.md`.
