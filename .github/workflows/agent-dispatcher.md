---
name: Agent Dispatcher
description: |
  Product lane. When an issue is labeled agent-ready (by Issue Triage or a maintainer),
  check that it is specific enough and hand it to the Copilot cloud agent. Copilot opens
  a draft PR; a human still reviews and merges it.

on:
  issues:
    types: [labeled]
    names: [agent-ready]
  workflow_dispatch:
    inputs:
      issue_number:
        description: Issue to hand to the Copilot cloud agent
        required: true
        type: string

permissions:
  contents: read
  issues: read
  pull-requests: read

engine: copilot
timeout-minutes: 10

concurrency:
  group: agent-dispatcher-${{ github.event.issue.number || inputs.issue_number }}
  cancel-in-progress: false
  job-discriminator: ${{ github.event.issue.number || inputs.issue_number }}

network: defaults

tools:
  github:
    toolsets: [default]

safe-outputs:
  assign-to-agent:
    name: copilot
    target: "*"
    required-labels: [agent-ready]
    max: 1
  add-comment:
    target: "*"
    max: 1
  add-labels:
    target: "*"
    allowed: [needs-info]
    max: 1
  noop:
    report-as-issue: false
---

# Agent Dispatcher

Issue **#${{ github.event.issue.number || inputs.issue_number }}** in `${{ github.repository }}` was labeled `agent-ready`. Decide whether the Copilot cloud agent can do it without asking questions, then hand it over.

1. Read the issue (title, body, labels, comments) with the GitHub tools.
2. It is **ready** when the expected behaviour is clear enough to write a test for it and the change touches only a few files.
3. If it is ready:
   - assign the Copilot cloud agent to issue #${{ github.event.issue.number || inputs.issue_number }};
   - add one comment: "Handed to the Copilot cloud agent — expect a draft PR. A human still reviews and merges it."
4. If it is not ready: add the label `needs-info` and one comment listing what's missing (max 3 bullets). Don't assign the agent.

Never change code yourself and never touch any other issue.
