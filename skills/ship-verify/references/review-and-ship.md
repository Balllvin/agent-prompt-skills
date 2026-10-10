---
name: review-and-ship
description: Review the current branch for bugs, intent fit, and test coverage; run or write tests; commit focused work; open or update a PR.
---

# Review and ship

## Trigger

Reviewing changes before shipping. Close key issues, verify behavior, and open or update a PR.

## Workflow

1. Gather context: diff against base branch, uncommitted changes, recent commits, changed files, and user intent from recent relevant chats if useful.
2. Run targeted tests for changed behavior. If no focused tests exist, decide whether to add them or document the gap.
3. Review for correctness, regressions, security, and intent fit. Use parallel subagents for larger diffs.
4. Fix critical issues before finalizing and re-run affected tests.
5. Commit selective files with a concise message.
6. Push branch and open or update a PR.

## Suggested Checks

```bash
git fetch origin main
git diff origin/main...HEAD
git status
```

Run the focused tests for the files you changed. Follow the repo's CI rule (`ci.md`); do not run a slow full local CI script unless the owner asks.

## Guardrails

- Prioritize correctness, security, and regressions over style-only comments.
- Keep commits focused and avoid unrelated file changes.
- If pre-commit checks fail, fix the issues rather than bypassing hooks.
- Judge readiness from the tests you ran, not from checks that may not run (see `ci.md`).

## Output

- Findings summary (critical, warning, note)
- Tests run and outcomes
- PR URL
