---
name: Issue Fixer
description: |
  Factory lane. When a maintainer labels an issue auto-fix, the agent fixes it,
  adds a regression test and opens a PR labeled awaiting-review for the PR Reviewer gate.
  Adapted from github.com/kloba/github-agentic-workflows-demo.

on:
  issues:
    types: [labeled]
    names: [auto-fix]
  workflow_dispatch:
    inputs:
      issue_number:
        description: Issue to fix (used by the rework loop)
        required: true
        type: string

permissions:
  contents: read
  issues: read
  pull-requests: read

engine: copilot
timeout-minutes: 20

concurrency:
  group: issue-fixer-${{ github.event.issue.number || inputs.issue_number }}
  cancel-in-progress: false
  job-discriminator: ${{ github.event.issue.number || inputs.issue_number }}

network:
  allowed: [defaults, python]

steps:
  - name: Checkout repository
    uses: actions/checkout@v7
    with:
      persist-credentials: false
  - name: Set up Python
    uses: actions/setup-python@v7
    with:
      python-version: "3.12"
  - name: Install dev dependencies
    run: pip install -r requirements-dev.txt

tools:
  github:
    toolsets: [default]
  edit:
  bash:
    - "python -m pytest *"
    - "ruff *"
    - "git diff *"
    - "git status"
    - "cat *"
    - "grep *"
    - "ls *"
    - "head *"
    - "sed -n *"

safe-outputs:
  create-pull-request:
    title-prefix: "[fix] "
    labels: [automated-fix, awaiting-review]
    draft: false
    allowed-branches: ["fix/*"]
    max: 1
  add-comment:
    target: "*"
    max: 1
  noop:
    report-as-issue: false
---

# Issue Fixer

A maintainer asked you to fix issue **#${{ github.event.issue.number || inputs.issue_number }}** in `${{ github.repository }}` without further help. The **PR Reviewer** workflow will review your PR and either label it `ready-to-merge` (then it merges automatically once CI is green) or `needs-rework` (then you get one more try).

## 1. Check that you should act

Read the issue (title, body, labels, comments) with the GitHub tools. Call `noop` with a one-line reason and stop if any of these is true:

- the issue is closed;
- it has a label `do-not-fix`, `wontfix`, `needs-info` or `needs-human`;
- an open pull request already references it;
- it asks for something you can't verify with a test (design, docs-only wording, "it feels slow").

## 2. Fix it

1. Read `AGENTS.md` and `.github/copilot-instructions.md` first and follow them.
2. Reproduce the problem with a **new failing test** in `tests/` that describes the expected behaviour from the issue.
3. Make the smallest change in `src/agenda/` that makes the test pass. Don't refactor unrelated code, don't add dependencies, don't touch `.github/`.
4. Run `python -m pytest -q` and `ruff check .` — both must pass.

## 3. Open the pull request

Create one pull request from a branch named `fix/issue-${{ github.event.issue.number || inputs.issue_number }}`:

- Title: a short imperative summary (the `[fix]` prefix is added for you).
- Body: what was wrong, what you changed, which test proves it, and the line `Fixes #${{ github.event.issue.number || inputs.issue_number }}`.

Then add one comment on the issue: "Opened a fix PR; the PR Reviewer gate decides if it merges."

If you could not produce a passing fix, don't open a PR: comment on the issue with what you tried and what's blocking you.
