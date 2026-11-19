# Assign & Forget? — demo repo

Demo for the WAW Tech 2026 talk **"Assign & Forget? GitHub tools for an agentic SDLC"** (Taras Kloba).

The app is deliberately tiny — a Python library and CLI for a fictional conference agenda — so the interesting part is everything around it: agents taking issues to pull requests on two lanes. Open an issue and walk away: Issue Triage routes it, and on the factory lane nobody touches it until it's merged.

| | Lane 1 · product | Lane 2 · factory |
|---|---|---|
| Start | Issue Triage (or you) labels the issue `agent-ready` | Issue Triage (or you) labels the issue `auto-fix` |
| Who writes the code | Copilot cloud agent (draft PR) | `issue-fixer` agentic workflow |
| Who reviews | Copilot code review (ruleset) | `pr-reviewer` agentic workflow → `ready-to-merge` / `needs-rework` |
| Who merges | **a human** — by design | `pr-auto-merge` when the `test` check is green |

## Workflows

| File | Trigger | What it does | What it may write |
|---|---|---|---|
| `agent-dispatcher.md` | issue labeled `agent-ready` | checks the issue is specific, assigns the Copilot cloud agent | assign Copilot, 1 comment, `needs-info` |
| `issue-fixer.md` | issue labeled `auto-fix` / dispatch | failing test → fix → PR | 1 PR (`fix/*`), 1 comment |
| `pr-reviewer.md` | PR opened / updated | the gate for factory PRs | 1 comment, `ready-to-merge` or `needs-rework` |
| `pr-auto-merge.yml` | reviewer or CI finished on `fix/**` | merges labeled PRs once `test` is green | merge |
| `pr-rework.yml` | reviewer or CI finished on `fix/**` | closes `needs-rework` or red fix PRs, retries up to 2×, then `needs-human` | close PR, labels, comment, dispatch |
| `issue-triage.md` | issue opened by someone with write access | type label and route: `auto-fix`, `agent-ready` or `needs-info` | labels, 1 comment |
| `ci-doctor.md` | CI failed | explains the root cause; failures on `main` become issues that triage routes | 1 comment or 1 issue |
| `daily-repo-status.md` | daily / dispatch | status report for maintainers | 1 issue |
| `ci.yml` | push / PR | ruff + pytest (required check `test`) | — |
| `copilot-setup-steps.yml` | — | the Copilot cloud agent's environment | — |

`*.md` workflows are [GitHub Agentic Workflows](https://github.github.com/gh-aw/): edit the Markdown, then run `gh aw compile` and commit the `.lock.yml` too. The agent runs read-only; every write goes through a declared safe output.

## Secrets

| Secret | Used by | Fine-grained PAT permissions |
|---|---|---|
| `COPILOT_GITHUB_TOKEN` | all agentic workflows (Copilot engine) | Account → Copilot Requests: read |
| `GH_AW_GITHUB_TOKEN` | safe outputs (labels, comments, issues, PRs), Copilot assignment, `pr-auto-merge` | This repository only: Actions, Contents, Issues, Pull requests read & write |

GitHub doesn't start workflows for writes made with `GITHUB_TOKEN`. Writes made with `GH_AW_GITHUB_TOKEN` do, and that is what closes the loop: triage's label starts the fixer, the fixer's PR starts CI and the reviewer, the merge starts CI on `main`. Don't give that token the Workflows permission, so no agent can push changes to `.github/workflows/`. `GH_AW_AGENT_TOKEN` and `GH_AW_CI_TRIGGER_TOKEN` aren't needed when it is set.

In an organization with centralized Copilot billing you can replace `COPILOT_GITHUB_TOKEN` with `copilot-requests: write` under `permissions:` in each workflow, then recompile.

## The app

```bash
pip install -r requirements-dev.txt
PYTHONPATH=src python -m agenda list --room Main
PYTHONPATH=src python -m agenda next --now 2026-11-26T09:30
python -m pytest -q
```

The factory lane is adapted from [kloba/github-agentic-workflows-demo](https://github.com/kloba/github-agentic-workflows-demo). The agenda data is fictional.
