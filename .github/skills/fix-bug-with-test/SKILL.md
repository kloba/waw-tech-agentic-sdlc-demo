---
name: fix-bug-with-test
description: Fix a reported bug in this repo the safe way — reproduce it with a failing pytest test, make the smallest fix, verify, and write the PR description. Use for any issue labeled bug.
---

# Fix a bug with a regression test

1. **Reproduce.** Turn the issue's steps into a pytest test in `tests/` (use `make_talk()` from `tests/conftest.py` and fixed times). Run `python -m pytest -q` and confirm the new test fails for the reason described in the issue. If it passes, stop and comment that you can't reproduce it.
2. **Fix.** Change the smallest amount of code in `src/agenda/`. No refactoring, no new dependencies.
3. **Verify.** `python -m pytest -q` and `ruff check . && ruff format --check .` both pass.
4. **Describe.** PR body with four short parts: *Problem*, *Fix*, *Test*, and `Fixes #<issue>`.
