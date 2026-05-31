#!/usr/bin/env bash
# Log each sub-agent run. Never blocks the agent.
LOG="$HOME/workspaces/.observability/agents.log"
mkdir -p "$(dirname "$LOG")" 2>/dev/null
INPUT=$(cat 2>/dev/null)
TS=$(date -u +%Y-%m-%dT%H:%M:%SZ)
AGENT=$(printf '%s' "$INPUT" | python3 -c "
import sys, json
try:
    d = json.load(sys.stdin)
    print(d.get('agent_type') or d.get('agent_name') or 'unknown')
except Exception:
    print('unknown')
" 2>/dev/null || echo unknown)
echo "$TS  agent=$AGENT" >> "$LOG" 2>/dev/null
exit 0
