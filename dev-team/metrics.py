#!/usr/bin/env python3
"""
Dev team observability metrics.

Reports:
  - repeated-mistake rate (same lesson class appearing 2+ times)
  - agent activity from observability log
  - open vs fixed bug ratio per project

Usage: python3 metrics.py
Reads: ~/workspaces/.observability/agents.log
       ~/workspaces/*/docs/lessons.md

No external dependencies.
"""
import re
from collections import Counter, defaultdict
from pathlib import Path

HOME = Path.home()
LOG_PATH = HOME / "workspaces/.observability/agents.log"
WORKSPACES = HOME / "workspaces"


def agent_activity():
    if not LOG_PATH.exists():
        return {}
    counts = Counter()
    for line in LOG_PATH.read_text().splitlines():
        m = re.search(r"agent=(\S+)", line)
        if m:
            counts[m.group(1)] += 1
    return dict(counts.most_common())


def parse_lessons(path: Path):
    lessons = []
    current = {}
    for line in path.read_text().splitlines():
        if line.startswith("### BUG-") or line.startswith("### "):
            if current:
                lessons.append(current)
            current = {"title": line.lstrip("# ").strip(), "file": str(path)}
        elif line.startswith("- Status:"):
            current["status"] = line.split(":", 1)[1].strip()
        elif line.startswith("- found_by:"):
            current["found_by"] = line.split(":", 1)[1].strip()
        elif line.startswith("- Lesson:"):
            current["lesson"] = line.split(":", 1)[1].strip()
    if current:
        lessons.append(current)
    return lessons


def lessons_report():
    all_lessons = []
    for md in WORKSPACES.glob("*/docs/lessons.md"):
        project = md.parts[-3]
        for l in parse_lessons(md):
            l["project"] = project
            all_lessons.append(l)

    if not all_lessons:
        return {"total": 0}

    keyword_map = defaultdict(list)
    for l in all_lessons:
        words = set(re.findall(r"\w{4,}", (l.get("lesson") or "").lower()))
        for w in words:
            keyword_map[w].append(l["title"])

    repeated = {w: titles for w, titles in keyword_map.items() if len(titles) >= 2}

    by_project = defaultdict(lambda: {"open": 0, "fixed": 0})
    for l in all_lessons:
        project = l.get("project", "unknown")
        status = l.get("status", "open")
        by_project[project][status] += 1

    return {
        "total": len(all_lessons),
        "repeated_mistake_keywords": {k: v for k, v in sorted(repeated.items())},
        "by_project": dict(by_project),
    }


def main():
    print("=" * 60)
    print("DEV TEAM METRICS")
    print("=" * 60)

    activity = agent_activity()
    if activity:
        print("\n── Agent activity (total runs) ──")
        for agent, count in activity.items():
            print(f"  {agent:<20} {count}")
    else:
        print("\n── Agent activity: no log found ──")

    lr = lessons_report()
    print(f"\n── Lessons & bugs (total: {lr['total']}) ──")

    if lr.get("by_project"):
        for proj, counts in lr["by_project"].items():
            total = counts["open"] + counts["fixed"]
            fix_rate = counts["fixed"] / total * 100 if total else 0
            print(f"  {proj}: {total} bugs, {counts['open']} open, "
                  f"{counts['fixed']} fixed ({fix_rate:.0f}% fix rate)")

    repeated = lr.get("repeated_mistake_keywords", {})
    if repeated:
        print(f"\n── Repeated mistake keywords ({len(repeated)} found) ──")
        for kw, titles in list(repeated.items())[:10]:
            print(f"  '{kw}' appears in {len(titles)} lessons:")
            for t in titles[:3]:
                print(f"    · {t}")
    else:
        print("\n── No repeated mistakes detected ✓ ──")

    print()


if __name__ == "__main__":
    main()
