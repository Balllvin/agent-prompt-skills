---
name: ci
description: Fix a red check, debug a CI job, or loop until CI is green. Covers repos where CI runs and repos where it does not.
---

# CI

First learn the repo's rule: read `AGENTS.md` (or the contributing guide) for whether CI runs, which local gate exists, and whether the owner wants it run. Some repos have no working hosted CI; there, focused local tests are the gate and waiting on `gh pr checks` is wasted time.

## When hosted CI runs

1. `gh pr checks <n>` to list checks; `gh run view <run-id> --log-failed` for the failing step.
2. Reproduce the failing command locally with the same tool versions (lockfiles, `--locked`, pinned toolchains).
3. Classify: your diff broke it (fix), the contract changed (retarget the assertion), the baseline is red on `main` too (report, do not fix in this PR), or flake (rerun once; a second failure is not flake).
4. Push the fix and watch with `gh pr checks <n> --watch` or `gh run watch <run-id>`. Poll in a bounded loop and stop the poller when done.

## When hosted CI does not run

Run the focused tests for the files you changed, name the commands under checks in the PR body, and do not wait on checks that will never start. Run a full local CI script only when the owner asks; it is slow and duplicates the focused run.

## Always

- Never weaken, skip, or xfail a test to go green.
- A check that never starts is not a product verdict; say so.
- Stop after the same failure survives two different fixes, and report the evidence.
