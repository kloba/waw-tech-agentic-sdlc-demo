---
name: CI Doctor
description: |
  When the CI workflow fails, investigates the logs and explains the likely
  root cause on the pull request (or in an issue for failures on main).

on:
  workflow_run:
    workflows: ["CI"]
    types: [completed]
    branches: [main, "fix/**", "copilot/**"]

if: ${{ github.event.workflow_run.conclusion == 'failure' }}

permissions:
  actions: read
  contents: read
  issues: read
  pull-requests: read

engine: copilot
timeout-minutes: 10

network: defaults

tools:
  github:
    toolsets: [default, actions]

safe-outputs:
  add-comment:
    target: "*"
    max: 1
  create-issue:
    title-prefix: "[ci-doctor] "
    labels: [ci-failure]
    max: 1
  noop:
    report-as-issue: false
---

# CI Doctor

The **CI** run ${{ github.event.workflow_run.html_url }} failed on commit `${{ github.event.workflow_run.head_sha }}`.

1. List the jobs of run ${{ github.event.workflow_run.id }} and read the logs of the failed steps.
2. Find the **first real error** (a failing test, a lint error, an install problem) and the file and line it points to.
3. If the run belongs to an open pull request, add one comment on that PR. Otherwise open one issue. In both cases write:
   - **Failing step:** name of the job and step
   - **Root cause:** 1–3 sentences, quoting the key log line
   - **Suggested fix:** the smallest change that should make CI green

Only state what the logs show. If the failure looks like a flaky runner or network problem, say so and suggest a re-run.
