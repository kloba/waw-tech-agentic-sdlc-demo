---
applyTo: "tests/**"
---

# Test conventions

- Use pytest functions, not classes. One behaviour per test; name it after the behaviour (`test_next_talk_returns_talk_starting_now`).
- Build small talks with `make_talk()` from `tests/conftest.py`; use the `talks` fixture only when the real agenda data matters.
- Use fixed times (`2026-11-26T10:00`), never `datetime.now()`.
- A regression test for a bug must fail on the old code. Mention the issue number in a comment above it.
