---
name: audit
description: >-
  Use whenever code needs review or an audit, even when no skill is named: a
  diff, branch, PR, or the whole repo, your own diff before calling a coding
  task done, and replies to review comments. Triggers: "review this PR",
  "code review", "audit the repo", "what can we delete", "is this
  over-engineered", "why is this slow", "are these tests any good", "find
  swallowed errors", "find similar bugs", "are there other places like this",
  "thermos", "review waves", "weekly audit", a pasted PR URL, and the old
  names /thermos, /thermo-nuclear-review, /thermo-nuclear-code-quality-review,
  /review-waves, /ponytail-audit, /ponytail-review, /silent-failure-hunter,
  /performance-profiler, /test-audit, /code-review,
  /pr-test-analyzer, /type-design-analyzer, /receiving-code-review,
  /requesting-code-review, /make-pr-easy-to-review, /pr-review-canvas,
  /differential-review, /variant-analysis.
---

# Audit

One home for every review lens. Pick a mode, run the lenses that fit, fan
out critics when the diff is big, verify every finding yourself, then report.
Each lens has a full reference file under `references/`; this page carries
the load-bearing rules so a reviewer can work from it alone and open the
reference only for depth.

**Evidence or label.** Every finding carries its evidence (the `path:line`, the command and its output, the measurement) or a label in the same sentence: measured, inferred, or guess. A guess is never reported at high or critical severity. (pstack, Lauren Tan, MIT.)

**Measured number.** A speed, coverage, or error-rate number in a review is not evidence until the Evidence line names the limiter and a run rules out errors, skipped or cached work, an untuned side, noise, and work that never ran. Reading the code is not that run. See [Explain the number](../build/references/principle-explain-the-number.md) and [Benchmark checklist](../build/references/benchmark-checklist.md). (pstack 0.15.15.)

Security-specific scans (threat models, validation, attack paths) live in
the `security` hub. This hub's bug lens catches security regressions in a
diff; a real security scan goes to `../security/SKILL.md`.

## 1. Pick the mode

| Mode | When | Shape |
|------|------|-------|
| Diff review | A branch, PR, or local diff | Lenses over `git diff origin/main...HEAD` or `gh pr diff <n>`. Report only added or changed lines, plus old code the diff now depends on. |
| Thermos | "thermos", "double thermo", structural diffs, files near 500 lines | Two critics in parallel: bug lens and structure lens. Synthesize yourself. |
| Review waves | A long PR is done and about to ship | Up to five parallel critics, parent verifies and fixes between waves. At most three waves. Wave 2+ re-runs only critics that had real findings (plus UI/UX when fixes touched UI). |
| Repo audit | "audit the repo", "find bloat", test-suite pruning, perf hunt | Scope by app path, never the repo root. Rank biggest cut or biggest cost first. One-shot report, applies nothing unless asked. |
| Weekly audit | A scheduled weekly sweep | Three proposal reviews (pstack, ponytail, thermos) on latest `origin/main`, each read-only, then one consolidator PR with the findings two reviews agree on, then the owner's merge gate. |
| Differential review | A security-relevant or risky diff, however small | Triage by what the code touches, not size. See `references/differential-review.md`. |
| Variant analysis | A bug was just confirmed | Hunt its siblings before closing. See `references/differential-review.md`. |
| PR review reply | Review comments arrived on your PR | Verify each comment against the code before changing anything. One summary: implemented, not implemented on purpose, checks. Resolve threads. |
| Reviewer handoff | Making a PR easy to read, or dispatching a reviewer | Tidy description, separate mechanical from core files, or render a walkthrough page. |

Why the wave cap: wave 1 finds, wave 2 confirms fixes and catches
regressions, wave 3 exists only if wave 2 still found real bugs. Past that,
critics start restating themselves and the cost outruns the signal. A clean
critic is not re-run for ceremony.

For a repository audit, the review-wave cap does not cap coverage. Track inventoried, semantically read, generated/vendor and unreviewed paths separately. A signatures/AST census is not semantic review. Reopen uncovered families or missing cache identities; a lean verdict names the paths and rejected cuts that support it.

For schema/index coverage, compare model declarations, explicit bootstrap registration, migration history and actual registered metadata. Transitive API imports can hide missing registration; fixture metadata is not proof of the full live schema. Verify unique-constraint backing before treating a paired index as duplicate.

Tiny diffs (a few lines, one owner) skip fan-out: run the bug lens yourself.

## 2. The lenses

Every lens reports only what it can tie to a `path:line`. Every lens stays
in its lane so critics do not duplicate each other; route off-lane findings
to the right lens in one line.

### Bugs, breakage, security (reads `references/thermo-nuclear-review.md`)

Critic: `thermo-nuclear-review-subagent`, `wave-bug-critic`.

- Scope: code added or modified in the diff. Pre-existing issues are out
  unless the diff makes them worse.
- Trace side effects across packages; simple edits break distant callers.
  Check the real server body shape against the parser, abort and unmount
  paths, unbounded loops and retries, behavior changes for non-target
  errors.
- Devex breakage: renamed or new env vars, moved secrets, remapped ports,
  new required setup steps.
- Feature-flag and internal-only leaks. They are subtle; trace every gate.
- Security in the diff: auth and ownership checks, `User.id` scoping,
  Agent-key scope, order and money routes staying unreachable, secrets in
  logs. Deep security work goes to the `security` hub.
- Intended breakage the author clearly meant, with tight scope, is not a
  finding. "Delete the database" still is.
- Never present unfinished research ("fine if the backend handles it") when
  you can read the backend. Never inflate priority; one false High costs
  trust in every later report.
- Read PR discussion (BugBot, humans) only after your own pass, so your
  eyes stay fresh. Flag which findings came from them.

### Structure and the 1k-line gate (reads `references/thermo-nuclear-code-quality-review.md`)

Critic: `thermo-nuclear-code-quality-review-subagent`, `wave-quality-critic`.

- Be ambitious. Look for the "code judo" move that deletes whole branches,
  modes, or layers instead of rearranging them.
- File size, per AGENTS.md: 350 healthy, 500 is the hard split line, 1000 is
  stop. A diff that pushes a file past 1000 is a presumptive blocker. Past
  500, ask for a split by responsibility.
- Spaghetti growth: new ad-hoc `if`s in unrelated flows, one-off booleans,
  nullable modes, feature logic leaking into shared code.
- Thin wrappers, identity abstractions, casts, `any`, needless optionality
  that hide the real invariant.
- Logic in the wrong layer: routes orchestrate, services decide, clients
  transport, components render. Reuse the canonical helper over a
  near-duplicate.
- Needlessly serial independent work; updates that can leave state half
  applied.
- Few high-conviction comments beat a list of nits. "It works" is not the
  approval bar.

### Over-engineering (reads `references/ponytail-review.md` for diffs, `references/ponytail-audit.md` repo-wide)

Critic: `wave-ponytail-critic`. The design rules behind the tags live in
`../build/references/ponytail.md` and `../build/references/radical-simplification/index.md`.

One line per finding, biggest cut first:
`<file>:L<line>: <tag> <what to cut>. <replacement>.`

- `delete:` dead code, unused flexibility, speculative feature.
- `stdlib:` hand-rolled thing the standard library ships. Name it.
- `native:` dependency or code doing what the platform already does.
- `yagni:` one-implementation interface, config nobody sets, one-caller layer.
- `shrink:` same logic, fewer lines. Show the shorter form.

Deletion estimates deduplicate exact file/ranges and separate production/test gross removal from net replacement estimates. Do not sum aliases, whole Owns sets or the sizes of files that merely need editing.

Also hunt two parts doing one job (duplicate owners, parallel constants,
copy-pasted waits or retries). End with a deduplicated quantified subtotal and mark unknown net replacement as unmeasured, or
`Lean already. Ship.` A single smoke test or `assert` self-check is the
minimum, never bloat. Bugs, security, and speed are out of this lane.

### Silent failures (reads `references/silent-failure-hunter.md`)

Critic: part of `wave-bug-critic` whenever the diff touches error handling.

A failure the user cannot see and the logs cannot explain is a bug even when
nothing crashes. Hunt:

- Swallowed: `except Exception: pass`, `.catch(() => {})`, Swift `try?` on a
  user path, Rust `.ok()` on I/O that matters.
- Failure sold as success: `[]`, `None`, `0.0`, `{"ok": true}` after a
  provider failed; a 429 cached as empty history.
- Failure sold as a different failure, lost task exceptions, cleanup errors
  replacing the original, wrong log level, unbounded retry or `Retry-After`.

The fix must meet these rules: a structured log event with ids as fields and
a `failure_class`; `error` only for real failures; catch-and-continue only
with a bounded `warning` naming what was skipped; loading, empty, stale,
degraded, and failed stay distinct in UI, failed uses `role="alert"`. A test
must drive the failure and assert the visible state and the log event.

### Performance (reads `references/performance-profiler.md`)

Critic: `wave-reuse-critic` covers the reuse half: does the DB or a cache
already hold what the diff refetches, repolls, or recomputes?

Label every finding with its evidence rung, strongest first:

1. Measured in production (hosting logs with `duration_ms`, metrics p50/p95/p99, metered API bytes).
2. Measured locally (benchmark, query-count fixture, import time, bundle output).
3. Read from code. Label static operation/line counts and targets as such. Timing, bytes and resource savings remain unmeasured until captured; name the metric and fixture.

Classify the cost first: trips, I/O wait, CPU, memory, bytes, or build time. Apply [reuse and work budgets](../build/references/reuse-and-budgets.md) to hot paths; inspect existing lower caches before calling an await a network trip.
Check the usual spenders: provider fan-out before first paint, N+1
queries, per-row enrichment, pollers on empty queues, `force_refresh=True`,
cache keys that include page size or date, heavy boot imports, refetch on
focus plus a short poll. A fix that hides a failure is not a speed-up. Leave
a regression guard (query count, deadline, payload cap). Hosting and
production access is read-only in an audit.

### Tests (reads `references/test-audit.md`; coverage gaps in `references/pr-test-analyzer.md`)

The authoring gate, for every added or changed test:

1. Contract: what behavior does it protect? Name it in the test name.
2. Regression: revert the fix and watch it fail for that reason.
3. Owner: one primary test per contract at the strongest boundary.
4. Seam: no test-only export, flag, or hook in production.

Junk list, each a failed gate unless it guards a named contract: no
assertion or one that cannot fail; greps source text; copies of a generated
file's test in every app; monkeypatches a private helper; a mock that
implements the asserted behavior; fixtures that hand over the answer; the
same scenario at every layer; a negative test passing for an unrelated
reason; a name that promises more than it exercises; a raised timeout; a
test of code that no longer exists.

Never skip, xfail, loosen, or delete a test to go green. For coverage
review, rate each missing test 1-10 by the regression it would catch; 8+ is
a must-add. Slow or static is not a reason to delete.

### Types (reads `references/type-design-analyzer.md`)

For each new or changed type: name its invariants, then rate 1-10 on
encapsulation, invariant expression, invariant usefulness, and enforcement.
Can an invalid instance be built? Are all mutation points guarded? Prefer
constructors and typed models that make illegal states unrepresentable over
comments and runtime checks scattered at call sites.

### UI/UX (reads `../ui-ux/SKILL.md` and the app's UI architecture doc, if any)

Critic: `wave-uiux-critic`, runs every wave. Design-read line first. Failed,
empty, stale, and partial stay distinct; retry sits near the failure; no
copy churn or new visuals smuggled into a behavior fix.

## 3. Fan out critics

Follow `../orchestrate-subagents/SKILL.md`. The parent owns the task, git,
synthesis, and every fix on the primary path.

- Launch all critics for a wave in one message. Omit `model` so children
  inherit. Each critic prompt carries only the diff or PR reference (plus
  its prior findings from wave 2 on); the critic reads this hub and its
  named reference.
- Critics are read-only: no edits, no git writes. Implementors
  (`wave-implementor`) get one disjoint file set each with Allowed and
  Forbidden lists, never the parent's primary files. Two writers never
  share a file, lockfile, migration, or fixture.
- Never let one reviewer sample a huge diff. A critic that skims 3,000
  lines returns confident noise. Slice by owner boundary (backend service,
  one app, native crate) so each critic reads every line it is given, and
  split again when a slice passes roughly 800 changed lines.
- Every synthesis ends with a coverage line so gaps are visible:
  `Coverage: <files read>/<files changed>, lenses run: <list>, skipped: <lens - reason>.`
- If critic subagents are unavailable, run thermos yourself and say so.

Thermos is the two-critic special case: launch
`thermo-nuclear-review-subagent` and
`thermo-nuclear-code-quality-review-subagent` in the same message against
the same scoped diff, then dedupe. Overlapping findings weigh more.

## 4. Verify each finding, then report

Do not forward critic output. Critics hallucinate lines and misread flows.

- **One checking agent per finding** on any diff that used fan-out. Give it only the finding and the `path:line`, and ask it to confirm or refute against live code (`../build/references/verify-this.md`): restate it falsifiably, open the file, reproduce. Launch them in one message. Idea from Anthropic's code-review plugin (Apache-2.0).
- **Drop anything it cannot confirm** and list it under Rejected with the reason. On a tiny diff with no fan-out, do the check yourself.
- Also drop, before checking: pre-existing issues the diff did not touch, anything a linter or type check catches, pedantic nits, and issues the code explicitly silences. Cite a rule only when you can quote it.
- **After a confirmed bug, run variant analysis** (section 1): find every sibling before the fix lands, so the fix covers all of them.

Report shape:

```
Verdict: <ship | fix first | block> - one line why.
Findings (highest severity first):
  <severity> <lens> path:line - what breaks, for whom
     Evidence: the code path, log, or measurement. A speed, coverage, or error-rate number also names its limiter and what the run ruled out, or it is not evidence.
     Fix: smallest change (delete > reuse > native > new code)
Rejected: <finding> - why it did not reproduce
Coverage: <files read>/<files changed>, lenses run, skipped with reason
Checks: commands run and results
```

Severity: critical (data loss, wrong number shown as right, auth fails
open), high (user-visible breakage, misleading state), medium (missing ids,
wrong level, maintainability blocker), low only when concrete. A lens with
nothing real says so in one line. For waves, add the accepted and rejected
lists per wave and the final wave verdict; list anything left open in the PR
under "Not done".

Receiving review: verify before implementing, ask about every unclear item
before touching any, push back with technical reasons when a suggestion is
wrong for this codebase, grep for usage before building "proper" versions of
unused code. No performative agreement or thanks; state the fix. Reply in
the inline thread, not a top-level comment.

## 5. Old skill → where it lives now

| Old skill | Now | Lens or mode |
|-----------|-----|--------------|
| `/thermos` | `references/thermos.md` | Thermos mode |
| `/thermo-nuclear-review` | `references/thermo-nuclear-review.md` | Bugs, breakage, security |
| `/thermo-nuclear-code-quality-review` | `references/thermo-nuclear-code-quality-review.md` | Structure and 1k-line gate |
| `/review-waves` | `references/review-waves.md` | Review waves mode |
| `/ponytail-audit` | `references/ponytail-audit.md` | Over-engineering, repo-wide |
| `/ponytail-review` | `references/ponytail-review.md` | Over-engineering, diff |
| `/silent-failure-hunter` | `references/silent-failure-hunter.md` | Silent failures |
| `/performance-profiler` | `references/performance-profiler.md` | Performance |
| `/test-audit` | `references/test-audit.md` | Tests: gate, junk list, audit and campaign modes |
| `/pr-test-analyzer` | `references/pr-test-analyzer.md` | Tests: coverage gaps rated 1-10 |
| `/type-design-analyzer` | `references/type-design-analyzer.md` | Types |
| `/code-review` | `references/code-review.md` | Diff review of a GitHub PR, confidence >= 80 |
| `/code-reviewer` | `references/code-reviewer.md` | Diff review against AGENTS.md, confidence >= 80 |
| `/receiving-code-review` | `references/receiving-code-review.md` | PR review reply |
| `/requesting-code-review` | `references/requesting-code-review/index.md` (prompt template: `references/requesting-code-review/code-reviewer.md`) | Reviewer handoff |
| `/make-pr-easy-to-review` | `references/make-pr-easy-to-review.md` | Reviewer handoff: description, history cleanup |
| `/differential-review`, `/variant-analysis` | `references/differential-review.md` | Differential review and variant analysis modes |
| `/pr-review-canvas` | `references/pr-review-canvas/index.md` (with `styles.css`, `renderer.js`, `template.html`) | Reviewer handoff: HTML walkthrough |

Related homes outside this hub: ponytail and radical-simplification design
rules in `../build/`, deslop and tdd in `../build/`, UI review in
`../ui-ux/`, security scans in `../security/`.
