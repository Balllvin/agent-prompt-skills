---
name: review-waves
description: Multi-wave PR review with parallel critic subagents (ponytail-audit, bugs, code quality, UI/UX, reuse), parent verify-and-fix between waves, implementor workers for large finding lists, at most three waves, later waves re-run only the critics that found something. Use after a long PR is done, before ship.
---

# Review waves

Repeated passes of parallel critics over a branch diff, with the parent
verifying every finding and implementing the fixes between waves. Wave 1
finds problems. Wave 2 confirms the fixes and catches regressions. Wave 3
runs only if wave 2 still found real bugs. Never more than three. Reviewers never write code;
implementor workers only touch their assigned disjoint slice.

## Trigger

A non-trivial diff is ready for review and the author wants more than one
pair of eyes: a structural change, a cross-boundary fix, a poll/retry/logging
change, or anything touching hot routes, shared clients, or user-visible
states. For tiny diffs use `review-and-ship` instead.

## Roles

- Parent: owns the task, the primary files, synthesis, integration, checks,
  commits, push, and PR. Implements primary-path fixes itself.
- Critics: read-only reviewers, one lens each, launched in parallel. They
  return findings. They do not edit, commit, or push.
- Implementors: isolated-write workers the parent spawns only when a wave
  leaves a large finding list. Each owns one disjoint file set that is not
  the parent primary path. They do not commit or push.

Follow `orchestrate-subagents` throughout: parent names primary files first,
keeps them out of worker scope (critics get no write scope at all), omits
Task `model` so children inherit the parent model, and never hands the full
task to a child.

## Wave 1: find problems

Launch all five critics in one message against the same diff
(`gh pr diff <n>` or `git diff origin/main...HEAD`). Every critic prompt
states: read-only, no edits, no git writes, file paths not pasted dumps,
findings with `path:line` evidence, one-line verdict.

1. Ponytail-audit critic. Skill: `ponytail-audit`. Diff-only
   over-engineering hunt: duplicate owners for one concept, single-use
   abstractions, parallel constants, hand-rolled sleeps/parsers the new code
   could share. Output one line per finding, biggest cut first.
2. Bug critic. Skills: `thermo-nuclear-review`, plus
   `silent-failure-hunter` when the diff touches error handling, catch
   blocks, fallbacks, or empty/failed/stale UI. Correctness only: broken
   parsing vs the real server body shape, unbounded loops, hammering,
   abort/unmount paths, behavior changes for non-target errors, weakened
   tests, log demotions that hide real failures.
3. Code-quality critic. Skill: `thermo-nuclear-code-quality-review`.
   Maintainability only: file-size gate pressure (350 healthy, 500 hard
   split), parallel homes, copy-pasted waits/retries needing one shared
   owner, comment quality, reusable vs incident-log lessons entries.
4. UI/UX critic. Skills: `ui-ux`, plus the app
   UI architecture doc for every app touched. Runs in every wave.
   Design-read line first (app, surface kind, object, decision it supports).
   Checks: failed vs empty vs stale vs partial stay distinct, retry near the
   failure, no swallowed errors, no copy churn, no new visuals smuggled into
   a behavior fix, loading shells stable.
5. Reuse critic. Skills: pick per concern (`radical-simplification` "Fast by design" on hot
   routes, `provider-routing` on LLM paths, `fmp-integration` on metered
   market data), otherwise a data-reuse audit. Question: does the DB already hold
   what this diff refetches, repolls, or recomputes? Name the existing
   rows/caches, the code path that could serve them, and honest blockers
   (staleness policy, scope keys, per-user vs shared rows).

## Parent: verify, then implement

Do not implement findings straight from summaries.

1. Verify each finding against the live code (`verify-this` lens:
   restate falsifiably, check the file, keep what reproduces, drop what
   does not). Write your own synthesis; overlapping findings across critics
   weigh more. Record what you accept, what you reject and why.
2. Implement accepted fixes with `ponytail` (smallest diff that holds, one
   shared owner over N copies). The parent always implements the primary
   path itself. When the accepted list is large, the parent may spawn
   implementor workers for disjoint helper slices: one worker, one file
   set, strict Allowed/Forbidden lists, isolated-write, no commits. Two
   writers must never share a file, lockfile, migration, or fixture.
   Parent reviews every worker diff before accepting it. UI touches go
   through `ui-ux`. Retargeted test assertions must track the new
   contract, never loosen to go green (`tdd` lens). Run `deslop` before
   calling the diff done.
3. Run the smallest relevant checks (focused tests, `tsc --noEmit`,
   backend tests for touched areas, route-drift script when shared clients
   moved). Commit the fixes as checkpoints.

## Wave 2 and beyond: confirm fixes

Re-spawn only the critics that returned real findings last wave, against
the updated diff plus their prior finding list. Ask each: confirm your
findings are addressed, and report any regression the fix introduced. The
UI/UX critic reruns whenever the fixes touched UI. A critic that only
re-states the previous wave without reading the new diff is not done;
narrow and re-prompt.

Stop when the rerun critics come back clean, or after wave 3. List anything
still open in the PR under "Not done", with the reason. If critic subagents
are unavailable (usage limit, tool missing), run `/thermos` yourself and say
so in the PR.

Parent verifies wave output the same way every round. When a wave is
clean, ship: rebase onto `origin/main`, push, open or update the PR.

## Guardrails

- Critics are read-only. No edits, branches, commits, pushes, or PRs from
  children. Implementors write only their assigned disjoint slice, never
  the parent primary path. One writer per file.
- If a finding needs a bigger behavior change (new serving path, new
  telemetry, GET-path writes), split it into a follow-up. Say so in the PR.
- At most three waves. A wave with no real findings ends the loop; do not
  re-run a clean critic for ceremony.
- Keep the PR body honest: what broke, what changed for users, what this
  does not do, checks run and their limits.

## Output

- Wave-1 synthesis: accepted, rejected (with reason), checks.
- Final wave verdict: clean or the delta fixed.
- PR URL.
