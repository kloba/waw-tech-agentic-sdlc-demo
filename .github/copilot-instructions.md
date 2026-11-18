# Copilot instructions for this repository

This repo is a small demo app for the talk "Assign & Forget? GitHub tools for an agentic SDLC".
Agents (Copilot cloud agent and the agentic workflows in `.github/workflows/*.md`) change it, so keep changes boring and easy to review.

## The project

- `src/agenda/` — a stdlib-only Python package that loads a conference agenda (`data/agenda.json`) and answers questions: next talk, talks in a room, overlapping talks.
- `tests/` — pytest tests. `tests/conftest.py` has the `talks` fixture and the `make_talk()` helper.
- CLI: `PYTHONPATH=src python -m agenda list|next|conflicts`.

## Rules

- Every bug fix starts with a failing test that reproduces the issue, then the smallest fix.
- Runtime code uses the standard library only. Don't add dependencies.
- Keep functions small and pure; type-hint public functions.
- Don't edit `.github/` (workflows, rulesets, agent config) in a feature or bug-fix PR.
- Before you finish: `python -m pytest -q` and `ruff check . && ruff format --check .` must pass.
- PR description: what was wrong, what changed, which test proves it, and `Fixes #<issue>`.
