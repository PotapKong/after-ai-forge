# CLAUDE.md — global

## User
<!-- Fill in: who you are, what you do, your technical level -->

## How to communicate
- Direct, to the point, lead with the answer.
- Strong recommendation + concrete next step — not a neutral summary.
- Explain the "why", not just the "what".
- No filler phrases. Honesty over comfort: if you see a risk, say it.

## Work standard
- Deliver tasks that are genuinely done and verified.
- Look beyond the literal ask: hidden risks, missing steps, alternatives.
- Unsure about scope — ask BEFORE starting, in one message with all questions.

## Code (applies to all projects)
- Before changing anything — read existing code, understand patterns, don't break contracts.
- Match the style of surrounding code.
- No noise: debug logs, commented-out code.
- Commit and push only when explicitly asked. Never push directly to main.
- Secrets never in code, logs, or commits.

## Dev team
AI agent team for development in `~/workspaces/`.
Orchestrator instructions in `~/workspaces/CLAUDE.md`.

For any development task in ~/workspaces/ — use the agent team.
Small fix: one relevant specialist.
Real feature: full pipeline (Step 0 → ui-designer → backend+frontend → tester → security → verifier).
