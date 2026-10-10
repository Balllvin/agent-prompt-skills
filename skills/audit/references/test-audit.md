---
name: test-audit
description: Keep tests worth their cost. Use whenever you write, change, review, or retarget a test (authoring gate), before calling a coding task done, and when asked to audit, prune, or speed up a test suite (audit mode). Rejects tests that restate source, duplicate stronger proof, couple to implementation, or keep test-only production seams alive.
---

# Test audit

A test earns its place by catching a credible regression that nothing stronger already catches. Two modes share one bar. Idea credit: openclaw's `test-audit` skill.

## Authoring gate

Before you add or change a test, answer all four. A missing answer means do not add it yet.

1. **Contract.** What behavior, invariant, or independent contract does it protect? Name it in the test name.
2. **Regression.** What real change makes it fail? Revert your fix and watch it fail for that reason (see `/tdd`, and `revert-proof` in `lessons.md`). A test that never failed proves the mock.
3. **Owner.** Why does existing coverage miss it? Each contract has one primary test at the strongest boundary: the route through the test client, the service with a real session, the component through user events, the Rust crate through its public API. Extend a table case or shared fixture before you add a near-copy.
4. **Seam.** Does it need an export, flag, `*ForTests` helper, or injection hook that production does not use? Then move the test to the real boundary instead.

Then check it against the junk list. A match fails the gate unless the retention list names the contract it guards.

A test your change breaks is yours to fix, wherever it lives. If the contract changed, retarget the assertion. If the product is wrong, fix the product. Never skip, xfail, loosen, or delete it to go green.

Before retargeting a transport fixture, verify its auth mode against the real backend boundary. A bearer-only client cannot fabricate a successful cookie-only identity response. Preserve denial, error and secret-redaction assertions.

Read-only and bootstrap checks need cold identities: run each public read alone, then in sequence, with both existing and missing state. A warm process cache can conceal the initializer's first-write path. Assert returned state and durable mutations separately; preserve explicit initialization and stale-work recovery contracts.

For structured-log assertions, establish the capture before binding the logger, or observe the configured sink. Check both cold logging and a logger bound before logging is reconfigured. A cached logger can retain its old processor chain and bypass `capture_logs()`. If the event appears in the real sink but not the capture, repair capture isolation. Keep event fields and domain assertions strict; do not change product behavior or add a baseline to hide a capture failure.

For concurrency proofs, synchronize independent starts at the transport boundary. Short sleeps do not establish exact overlap under scheduler load. Keep the concurrency limits, values, request counts and result order strict. Reverting the concurrent path must fail the proof.

Persistent history proofs include missing-all rows, a missing tail and valid JSON of the wrong shape. Exercise the actual downgrade transaction: preserve unchanged legacy bytes and roll back before dropping incomplete history. Drive failure delivery through its public consumer; typed integrity failure in a best-effort reason loader must still reach the generic failure copy while database errors and cancellation propagate.

For PostgreSQL isolation proofs, leave the active schema empty and put legacy tables in a later `search_path` schema. Exercise upgrade, runtime repair, backfill and downgrade. Assert both schemas and their rows stay unchanged. Two populated schemas miss fallback mutation.

Operation budgets must compose across owners. Observe real SQL inside the assigned read boundary, assert its exact count and public output, and report broader totals separately. Before retargeting a failed total, identify the downstream change and show that reverting the assigned cut still fails. A smaller global total is not by itself a regression. For cluster-wide WAL measurements, use a dedicated quiet server and record its identity, clients and interval boundaries. Interleave baseline and treatment. Retain every sample and declare warmup policy and percentile calculation; use nearest-rank p95 or name another method explicitly. Lower WAL does not excuse a material latency regression. A helper parity test does not prove its caller stopped repeating work. Exercise the actual caller lifecycle and measure the operation there; distinguish offscreen mounted behavior from desktop input and visual checks.

When a test checks time since a state transition, take the reference after that transition completes or use its persisted event timestamp. Match the store’s timestamp precision. A reference captured before a disable/re-enable commit can undercount a full day across a second boundary. Preserve the strict duration and unlock assertions; reproduce the real boundary without replacing clocks or lengthening deadlines.

For Native Undo/Redo, mount the production window, root and command wiring with isolated storage. Verify the focused history owner, menu availability, single-step keyboard Undo/Redo and persisted output. Exercise focus changes and read-only or empty history. A draft history unit test does not prove shipping command routing. A host that omits production focus or scene wiring cannot establish shortcut acceptance.

## Junk list

- No assertion, or an assertion that cannot fail (self-comparison, expected value produced by the code under test).
- Reads source files as text and greps names, imports, or class strings. Survives real regressions, breaks on renames.
- Copies of a shared test into every app that ships the same generated file. The generator's `--check` already proves the bytes match.
- Monkeypatches a private helper (`_utcnow`, `_resolve_user_id`) so any refactor breaks it. Patch the clock or the boundary instead.
- A mock or fake that implements the behavior the test asserts, or a fake session missing the methods the real path calls.
- Fixtures that hand the code the ordering, receipt, or callback it should produce itself.
- The same scenario replayed at every layer it passes through.
- A negative test that passes for an unrelated reason (a different guard refuses it).
- A name that promises more than the input exercises.
- A timeout raised to hide a slow or hung test (15 s per test, a 30 s suite default).
- A test that targets code or routes that no longer exist.

## Retention list

Keep a test that independently guards a public API, route contract, CLI output, migration, storage format, security boundary, generated cross-language catalog, prompt bytes, Dockerfile or deploy output, or observable ordering. A source-reading test stays only when it is the cheapest guard of a user-facing key, byte, or path and survives an identifier rename. A kept test that fails on `main` is a possible product bug: reproduce it and fix the owner.

## Before you say done

- New and changed tests passed the gate.
- Each main change has a test that fails when the change is reverted. You saw it fail.
- No test was skipped, xfailed, loosened, deleted to pass, or given a longer timeout to pass.
- No new test-only export or production seam. Conditional proof flags, counters and fixtures in product source are seams even when release builds exclude them. Use actual compiler profiles or a standalone black-box harness; retain its runner, source hashes and raw baseline/treatment/reversion artifacts before removing a worktree.
- The focused tests for the change passed, and you named the commands. Do not run `scripts/ci/local.sh` or GitHub CI unless the owner asked.

## Audit mode

Read-only discovery first; report evidence before editing.

1. Read `AGENTS.md`, `lessons.md`, the test, its production owner, callers, sibling tests, and how `scripts/ci/local.sh` routes it.
2. Hunt the junk list by lane: backend tests, each web app's `src`, native crates or app test targets, and `scripts/` checks.
3. For each candidate record: test id and path; what failure it can detect; production callers of any seam it keeps alive; the stronger test that remains; why it exists (`git log -L` or blame); what deletion it unlocks; the validation command.
4. Group candidates into one coherent PR per owner boundary. Prefer fewer high-confidence batches over a long speculative list.
5. Edit: delete dead seams with the tests, move kept regressions to their owner, merge near-duplicates into one table test. Report production and test line counts separately (`git diff --numstat`).

Slow or static is not a reason to delete. A test that looks like implementation may still be the only guard of a contract; prove otherwise first.

## Campaign mode

To prune one subsystem's whole test surface: record a baseline pass/fail per file at a pinned `main` SHA; split the tests into lanes by production owner; give each lane a read-only ledger that marks every test Retain, Fix, Consolidate (into which keeper), or Delete (with the proof that remains); then pick the keeper suite per contract and edit lane by lane. Baseline failures go on their own list and are treated as product bugs until shown otherwise.
