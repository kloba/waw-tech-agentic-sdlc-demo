---
name: Issue Triage
description: |
  Entry point of the autonomous factory. Labels each new issue and routes it:
  auto-fix (the factory fixes, reviews and merges it), agent-ready (the Copilot cloud
  agent opens a draft PR for a human) or needs-info. gh-aw only runs it for people with
  write access, so issues from strangers never reach a coding agent.

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
    allowed: [bug, enhancement, documentation, question, needs-info, auto-fix, agent-ready]
    max: 1
    max-labels: 2
  add-comment:
    max: 1
  noop:
    report-as-issue: false
---

# Issue Triage

Triage issue **#${{ github.event.issue.number }}** in `${{ github.repository }}` and route it. Nobody checks your decision before an agent starts work, so be conservative.

## 1. Skip what isn't a work item

Call `noop` with a one-line reason and stop if the issue:

- is a status report (label `report` or a title starting with `[repo status]`);
- already has `auto-fix`, `agent-ready`, `needs-info`, `needs-human` or `do-not-fix`;
- is referenced by an open pull request.

## 2. Understand it

Read the issue, `README.md`, `AGENTS.md` and the code in `src/agenda/` and `tests/`.

## 3. Label and route — one add-labels call with two labels

1. **Type:** `bug`, `enhancement`, `documentation` or `question`.
2. **Route** — exactly one:
   - `auto-fix` — a defect or small behaviour change in `src/agenda/` where the expected behaviour is stated or obvious, a unit test can pin it, and the fix is a few lines. A `[ci-doctor]` issue qualifies when the root cause is in `src/` or `tests/`, not a flaky runner or network.
   - `agent-ready` — a clear feature or documentation change that is bigger than a one-line fix (a new CLI option, README examples) but needs no further questions.
   - `needs-info` — anything else: unclear expected behaviour, missing steps to reproduce, something a test can't check ("it feels slow"), a design decision, or changes to `.github/`, CI, dependencies or secrets.

## 4. Comment

Post one comment (max 5 lines): what the issue is, the most likely place in the code, and which lane you chose and why. For `needs-info`, list exactly what is missing.
