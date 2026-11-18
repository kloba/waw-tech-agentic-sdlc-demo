---
name: Daily Repo Status
description: |
  A short daily status report for the maintainers, posted as an issue.
  This is the workflow built live in the talk (same idea as the gh-aw workshop).

on:
  schedule: daily
  workflow_dispatch:

permissions:
  contents: read
  issues: read
  pull-requests: read
  actions: read

engine: copilot
timeout-minutes: 10

network: defaults

tools:
  github:
    toolsets: [default, actions]

safe-outputs:
  create-issue:
    title-prefix: "[repo status] "
    labels: [report]
    max: 1
  noop:
    report-as-issue: false
---

# Daily Repo Status

Write a status report for the maintainers of `${{ github.repository }}` covering the **last 24 hours**, and publish it as one issue.

Use these sections, and link every item you mention:

1. **Highlights** — merged PRs and closed issues, one line each.
2. **Agents at work** — issues labeled `agent-ready` or `auto-fix`, and the PRs agents opened for them (who opened it, current state).
3. **Waiting for a human** — PRs waiting for review or approval, issues labeled `needs-info` or `needs-human`.
4. **CI health** — failed workflow runs, with the workflow name and a one-line reason if it's obvious.

Keep it under 250 words, plain and factual — no hype, no guesses. If nothing happened in the last 24 hours, say so in one sentence.
