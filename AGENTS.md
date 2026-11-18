# AGENTS.md

Instructions for any coding agent working in this repository (Copilot, Claude, Codex, …).
The full rules are in `.github/copilot-instructions.md`; this is the short version.

## Setup

```bash
python -m venv .venv && . .venv/bin/activate
pip install -r requirements-dev.txt
```

## Check your work

```bash
python -m pytest -q
ruff check . && ruff format --check .
```

## Conventions

- Bug fix = failing test first, then the smallest change in `src/agenda/`.
- Standard library only at runtime; no new dependencies.
- Don't touch `.github/` in a code PR.
- Put `Fixes #<issue>` in the PR description.
