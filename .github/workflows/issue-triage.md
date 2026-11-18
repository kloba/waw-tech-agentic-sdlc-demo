---
name: Issue Triage
description: |
  Labels new issues and asks for missing details. It never starts an agent:
  agent-ready and auto-fix are a maintainer's decision.

on:
  issues:
    types: [opened]

permissions:
  contents: read
  issues: read
  pull-requests: read

engine: copilot
timeout-minutes: 10

network: defaults

tools:
  github:
    toolsets: [default]

safe-outputs:
  add-labels:
    allowed: [bug, enhancement, documentation, question, needs-info]
    max: 1
    max-labels: 2
  add-comment:
    max: 1
  noop:
    report-as-issue: false
---

# Issue Triage

Triage issue **#${{ github.event.issue.number }}** in `${{ github.repository }}`.

1. Read the issue and skim `README.md` and `src/agenda/` so you understand the project.
2. Add **one** type label: `bug`, `enhancement`, `documentation` or `question`.
3. If the issue lacks what someone needs to act on it (steps to reproduce, expected vs. actual behaviour, the command that was run), also add `needs-info`.
4. Post one short comment (max 5 lines): what you think the issue is, the most likely place in the code, and — only if `needs-info` — the exact details that are missing.

Do **not** add `agent-ready` or `auto-fix`: handing work to an agent is a maintainer's call. If the issue was already triaged, call `noop`.
