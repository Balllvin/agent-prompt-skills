---
name: build
description: >-
  Use on any coding task, even when no skill is named: writing, fixing,
  refactoring, debugging, designing, or verifying code. Load it before the
  first edit. Triggers: "fix this bug", "why is this failing", "debug this",
  "be lazy", "simplest solution", "yagni", "verify this", "prove it works",
  "what could this break", "grill me", "how does X work", "why is X like
  this", "design this", "remove slop", "write a failing test first", and the
  old names /ponytail, /radical-simplification, /deslop, /tdd, /no-comments,
  /blast-radius, /grilling, /grill-me, /how, /why, /architect, /interrogate,
  /poteto-mode, /verify-this, /teach, /reflect, /recall, /figure-it-out,
  /show-me-your-work, /systematic-debugging.
---

# Build

The single skill for how code gets written here. `AGENTS.md` wins on workflow, git, routing, and file-size gates. This file wins on how you shape the code itself. The rules below come first because only the top of this file survives context compaction.

It covers the build ladder, one remaining way, fast-by-design hot paths, the pstack principles, debugging, TDD and revert-proof tests, verification, deslop and comments, planning, and working style for long runs.

## 0. Always-on rules (pstack)

These change behavior on every task, so they live here and not only in a reference. Source: pstack by Lauren Tan (poteto), MIT, https://github.com/cursor/plugins/tree/main/pstack.

- **Evidence or label.** Every claim carries its evidence or its label in the same sentence: measured, inferred, or guess. "Tests pass (ran `pytest tests/x`, 12 passed)" or "Probably a stale cache (guess)". Never hand the human a check you could run.
- **Try it instead of asking.** Before asking the user, classify the fork. If running something (a script, a repro, a prototype, a grep) could answer it, run it. Only product direction and irreversible actions go to the user.
- **Copy playbook steps verbatim.** When a playbook or checklist applies, copy its steps into the todo list word for word. A skipped step stays listed as `skip: <reason>`. Never drop one silently.
- **No is an acceptable answer.** Say no to scope that does not earn its place, and disagree with a wrong suggestion with the technical reason. No performative agreement.
- **Cut what does not change behavior.** In code, prompts, and skill text, delete any instruction, guard, or line whose removal changes nothing. Keep a line only if you can name what goes wrong without it.

## 1. The build ladder

For a fresh worktree, read the repo's pinned runtime versions (for example a `RUNTIME_VERSIONS.md`, `.tool-versions`, or `rust-toolchain.toml`) before build commands. Run Cargo from the crate workspace so rustup reads its pin. Build every native library required by the selected tests before collection; another worktree's library is not setup proof.

Keep npm installs in the current worktree. Before `npm ci`, unlink only its own `node_modules` symlink if it targets shared dependencies. Never reinstall into another chat's dependency tree.

Read the task and trace the real flow end to end first. The ladder shortens the solution, never the reading. A small diff in the wrong place is a second bug, not laziness.

Then stop at the first rung that holds:

1. **Does it need to exist?** Speculative need means skip it and say so in one line.
2. **Is it already in the codebase?** Reuse the helper, type, or pattern a few files over. Re-implementing what exists is the most common slop.
3. **Does the stdlib do it?** Use it.
4. **Does the platform do it?** `<input type="date">`, CSS over JS, a DB constraint over app code.
5. **Does an installed dependency do it?** Use it. Do not add a dependency for a few lines.
6. **Can it be one line?** Then one line.
7. **Only then** write the minimum code that works.

Two rungs work: take the higher one. Two stdlib options of the same size: take the one correct on edge cases. Lazy means less code, not a flimsier algorithm.

**Bug fix means root cause.** Grep every caller of the function before you edit it. One guard in the shared function is a smaller diff than one per caller, and patching only the path the ticket names leaves the siblings broken.

**Never simplify away** trust-boundary validation, error handling that prevents data loss, security, accessibility basics, or anything explicitly requested. If the user insists on the full version, build it without re-arguing.

Preserve accepted inputs and error behavior when cutting work. A byte or count metric does not authorize a new rejection threshold. If a real resource constraint requires a boundary change, measure it, justify the threshold, and record the contract change.

**Non-trivial logic leaves one runnable check** (a branch, loop, parser, money or security path). One small test or assert-based self-check. Trivial one-liners need none.

**Mark deliberate shortcuts** with `ponytail: <ceiling>, <upgrade path>` (`# ponytail: global lock, per-account locks if throughput matters`). The marker makes simplicity read as intent, and `/ponytail-debt` harvests them.

**Output:** code first, then at most three short lines: what was skipped and when to add it. A paragraph defending a simplification is complexity smuggled back in as prose. Requested explanations are not debt.

Intensity: `lite` builds what was asked and names the lazier option, `full` (default) enforces the ladder, `ultra` challenges the requirement in the same breath.

### One remaining way (radical simplification)

Ponytail picks the smallest code. Radical simplification picks one way to do the job, even if that means ripping architecture.

- Run it in order: question the requirement, delete parts, then simplify, then automate. Do not simplify something that should not exist.
- Name the ending in one sentence: one way, one name, one owner. If you cannot, stop.
- Two modules, paths, or types for one job: integrate or delete. No wrapper, facade, pass-through helper, single-implementation interface, `getX()` over two lives, or switch that keeps both.
- A new folder replaces the old ones in the same PR. Deleted code leaves the tree with its imports, tests, flags, and dead files.
- Distinct failure states stay distinct (`401`, `503`, empty last-good). Catch-log-and-continue and return-null-on-error are a silent second path. Delete them.
- Do not fabricate evidence on the surviving path: chained `as` casts, `unknown` params, or spreads that hide a field are a second type-home.
- "Too risky" sequences the delete. It does not justify keeping two ways.
- Review mode: one line per finding, ranked, tagged `second-home`, `wrapper`, `silent-path`, `type-home`, or `quality-drop`. Apply nothing.

### Fast by design

The fastest work never runs. The next fastest already ran before the request arrived. Latency is trips × distance + work per trip, so attack in that order:

1. Eliminate trips: a read model or one aggregate endpoint, not ten calls.
2. Shorten trips: memory, client store, Postgres, then provider.
3. Move work to write time when reads dominate.
4. Only then make the work cheaper: algorithm first, language last.

Classify and measure the actual cost. Do not substitute generic provider, SQL or Python latency ranges for evidence. I/O wait does not get faster in Rust. Move work to a native (for example Rust) crate only when a profile shows hot CPU or memory, equal behavior, and a measured gain that earns the language boundary. Small confirmed hot-path gains remain in scope. Measure resident memory and idle work as well as request counts. Profile boot imports, idle polling, payload retention and forced refresh; remove repeated work only while preserving its consumer and freshness contracts.

For a hot route, list, cache, import, stream or switchable screen, read [reuse and work budgets](references/reuse-and-budgets.md). Trace the next caller, reuse existing facts, and leave a count proof; first-paint success alone does not close siblings.

The five laws:

1. First paint comes from a bounded read model, never a provider fan-out. Enqueue refresh and return freshness metadata.
2. Scope every cost to the visible screen.
3. Bound everything: per-section deadlines, pool size, payload size, finite retries.
4. Never trade honesty for speed. A cache hit is not a live tick, a degraded section is not empty, a 429 is not an empty history.
5. Measure before and after, then leave the test that fails if the slow path returns.

Freshness is a product rule per data type. Closed-session and daily-bar reuse follows the owning correction/adjustment policy; finished data is not automatically immutable. User writes need read-your-writes. Details: `references/radical-simplification/references/efficient-systems.md`. For algorithmic hotspots (nested scans, N+1, O(n²)), use `references/complexity-optimizer/index.md` and its scanner.

## 2. Principles

One line each. Read the leaf in `references/principle-<name>.md` when a principle shapes a real decision, and name the choice it changed. A citation with no decision behind it is decoration.

**Core**
- `laziness-protocol`: prefer deletion, flat call chains, one source of truth per decision, the smallest diff. Question any signal threaded through many layers.
- `subtract-before-you-add`: remove dead weight first. A reference with no novel content gets deleted, not stubbed.
- `foundational-thinking`: data shape first, scaffold (CI, tests, shared types) before features, DRY the structure not every line.
- `redesign-from-first-principles`: integrate a requirement as if it existed on day one and propagate it through every reference.
- `minimize-reader-load`: count layers to trace and state to hold. A reader should answer "where does X come from" in 30 seconds.
- `outcome-oriented-execution`: optimize for the verified end state. Planned, scoped intermediate breakage beats long-lived compatibility code.
- `experience-first`: delight over convenience. The next maintainer and the importing colleague are users too.
- `exhaust-the-design-space`: with no precedent, design it twice. A second flavor of the same shape does not count.
- `build-the-lever`: non-trivial work gets a codemod, script, or generator a reviewer can rerun. Citing this with no script in the diff means you did not apply it.
- `attack-the-premise`: after two fixes on one premise fail the same gate, write the premise down and take a census before a third fix.

**Architecture**
- `model-the-domain`: a state machine, union, table, or reducer instead of a growing if/else chain or a second boolean kept in sync.
- `boundary-discipline`: validate and narrow at system boundaries, trust types inside, keep business logic pure.
- `type-system-discipline`: illegal states unrepresentable, brand primitives, parse external data, no lying casts, exhaustive matches, derive from schemas.
- `make-operations-idempotent`: ask what happens if it runs twice or crashed halfway. Converge, or add a reconcile step.
- `migrate-callers-then-delete-legacy-apis`: migrate and delete in one wave. No permanent adapters.
- `separate-before-serializing-shared-state`: give each actor its own write target before reaching for a lock.

**Verification**
- `prove-it-works`: check the real artifact, not a proxy, a self-report, or "it compiles". Script the check when you can.
- `explain-the-number`: before you trust, report, or act on a measured number, name what bounds it and rule out other explanations with a run.
- `fix-root-causes`: reproduce, ask why until the cause, fix every instance of the pattern. Restart bugs are usually stale state.
- `sequence-verifiable-units`: each unit ends green before the next. Deliver failing test first, then the fix.
- `test-behavior-not-implementation`: see section 3.

**Delegation and meta**
- `guard-the-context-window`: route bulky output to subagents, keep summaries in the main thread, read only what you use.
- `never-block-on-the-human`: proceed on reversible work and present the result. Pause for irreversible actions and product direction.
- `encode-lessons-in-structure`: capture a confirmed miss in the matching `lessons/` topic; read `lessons.md` for routing. Prefer a type, lint, helper, or check when it can enforce the invariant. Agent workflow corrections belong in the owning skill, linked from the router.

## 3. Tests and verification

**A test must fail when the behavior breaks.** Before keeping a test, ask: would it still pass if every imported function returned `undefined`? If yes, it proves nothing. The five shapes that fail this check are weak assertions (`toBeDefined`, `not.toThrow`), mock-or-absence only (`toHaveBeenCalled`, `toEqual([])`), self-referential expected values (`expect(f(a)).toBe(f(a))`), constant pins (`expect(LIMITS.max).toBe(8)`), and fixture asserting fixture. Fix: call the subject with one concrete input and assert the literal output or observable effect. Assert the payload a mock received, not that it was called.

**Revert-proof.** A new or retargeted test must go red when the product change is reverted. Prove it at least once: revert the fix (in a copy, not a loop over the live checkout), run the test, watch it fail for the intended reason, restore. A test that stays green on revert is the "add tests that stay green if the change is reverted" failure `AGENTS.md` forbids.

**TDD on bugs with a cheap local target** (`/tdd`):
1. Name intended vs current behavior and the smallest reproduction.
2. Pick the narrowest existing test home for that codepath.
3. Write the failing test first and confirm it fails for the right reason.
4. Make the smallest production fix, rerun, then run adjacent checks.

When a failing test is impractical (broad harness, prod-only state, brittle mocks), say why before fixing and use the closest executable check: a script, a repro command, browser automation. No new test beats a bad one. Never change a test to match a wrong implementation or loosen it to go green; if the contract changed, retarget it. Report failing-before and passing-after evidence.

**Verify a claim** (`/verify-this`): restate it as condition, metric, and threshold. Capture baseline and treatment with the same command, data, and environment. Compare raw artifacts. Return exactly one verdict: `VERIFIED`, `NOT VERIFIED`, or `INCONCLUSIVE`. Inconclusive is not a pass, and a clear negative is useful. Details: `references/verify-this.md`.

**Blast radius** (`/blast-radius`): listing callers is not the job. Find the one fact the change is safe because of, look where grep stops (library source, wire formats, DB columns, teardown timing, flags), and prove that fact with a script that runs real code. Rank each safety fact: said so, pointed at the line, walked the failure, ran it, reproduced in the app. Anything below "ran it" is marked unproven. Details: `references/blast-radius.md`.

**Debug before fixing** (`/systematic-debugging`, full procedure in `references/systematic-debugging.md`, from obra/superpowers, MIT). No fix before a root cause:
1. Root cause: read the whole error, reproduce it reliably, check recent changes. On a multi-component path, log what enters and leaves each boundary in one run before guessing.
2. Pattern: find a working sibling and list every difference, however small.
3. Hypothesis: write one ("X because Y"), change one variable, and form a new hypothesis if it fails. Never stack fixes.
4. Fix: failing test first, then one fix, then verify.
Two failed fixes on one premise means stop and run `attack-the-premise`; three means question the architecture. A test that passes alone and fails in the suite: bisect with `references/find-polluter.sh`.

**Compile errors:** run the repo's type and compile commands, group by file, fix highest confidence first, rerun until clean (`references/check-compiler-errors.md`).

**Toolchain upgrades:** trace every selector: app engines, lockfiles, containers, CI, local runners and documented commands. Use one test-dependency manifest across CI jobs. A clean install and compiler pass do not prove changed test discovery, packaging or runtime behavior; execute those commands on the selected version. Repair collection before judging the suite, then rerun failed or unreached jobs.

**Test audits** of an existing suite live in the audit hub: `skills/audit/references/test-audit.md`.

## 4. Deslop and comments

Run deslop on the branch diff before you call a coding change done. It is a filter, not a rewrite. Keep the file's existing voice.

Remove:
- Comments that restate the next line, narrate "what", section banners, emoji, changelog notes, docstrings that repeat the name.
- Defensive theater: try/catch on trusted paths, guards that cannot fire, catch-log-and-continue that hides errors from the caller.
- `any` and `as unknown as` used to dodge types, thin wrappers, single-implementation interfaces, optional fields papering over a boundary.
- Deep nesting that early returns fix, speculative flags and config, verbose names, unrelated import or format churn.
- Tests that only assert mocks, "John Doe" and "Acme" fixtures, snapshot updates that bury copy slop.

Keep behavior unchanged, stay inside the diff, and summarize in one to three sentences what went and what stayed on purpose.

**Comments.** Write them clean as you go, because the cleanup pass reliably misses them. Keep a comment only for a non-obvious why the code cannot show. A verify script that narrates `// Phase 1: add cards` gets the narration deleted; the assertion message is the doc. A constraint comment ("do not remove", "talk to X first") is a lesson waiting to be encoded as a type, test, or lint. Offer the encoding, then delete the comment. `/no-comments` runs an independent comment reviewer over the diff and fixes accepted findings at the root; see `references/no-comments.md`. Suppressions that hide correctness or safety are findings, not keeps.

**Complete output.** Never ship `// ...`, `// rest of code`, `TODO` stubs, or a skeleton where an implementation was asked. If output must split, stop at a clean boundary and say what remains (`references/full-output-enforcement.md`).

## 5. Planning and interrogation

**Grilling** (`/grilling`, `/grill-me`): interview the user until you share an understanding. Map decisions as a tree. Each round, ask the whole frontier (questions whose prerequisites are settled), numbered, each with your recommended answer. Look facts up yourself or through a subagent; only decisions go to the user. Done when the frontier is empty and the user confirms. Write no files.

**How** (`/how`): explain a subsystem at senior-onboarding depth: overview, key concepts, how it works, where things live, gotchas. Simple questions take one explorer pass; complex ones split into two to four parallel slices, then one synthesis. Critique mode explains first, then sends critics and sorts findings into act on, consider, noted, dismissed.

**Why** (`/why`): motivation lives outside the code. Anchor with `git blame`, `git log --follow`, and `gh pr view`, then query every available evidence source in parallel, one investigator per source. Cite everything, separate what was found from what is inferred, keep the hedges, and list null results. Never cite code as evidence for its own intent.

**Teach** (`/teach`): run `how` and `why`, then explain plainly at the person's pace. Smallest complete answer first, diagrams built up one part at a time, no pacing theater. `/bro` restates the last message without jargon.

**Architect** (`/architect`): for work crossing a function or package boundary. Ground with `how` (and `why` if ownership moves). Write the caller's usage first, then types and signatures with unimplemented bodies. Design at least two structurally different shapes, screen them against `references/architect/references/design-red-flags.md` (shallow modules, leakage, temporal decomposition, pass-throughs), prefer the deeper interface. Implement against the sketch and surface deviations. Repeated friction of the same shape means scrap and redesign smaller.

**Interrogate** (`/interrogate`): state the intent in one paragraph, send the same diff and rubric to several independent reviewers, weight consensus findings highest, then judge as the lead: act on, consider, noted, dismissed. Never auto-apply.

**Figure it out** (`/figure-it-out`): when no playbook fits a large or unattended task, design one first. Falsifiable definition of done, quantified scope, rigor biased high, verification harness and baseline before the work, riskiest unknown first, a decision trail throughout.

Multi-surface product work gets a spec first through `/layered-spec`. Parallel helpers follow `/orchestrate-subagents`.

## 6. Working style for long runs

**Poteto mode** (`/poteto-mode`): a rigor mode. Start multi-step tasks with a todo list, match the task to a playbook in `references/poteto-mode/playbooks/`, and copy its steps in verbatim; skipped steps stay listed with `skip: <reason>`. Name the data shape before any code. Classify an empirical fork before asking the user: if running something could answer it, prototype instead. Say no when scope does not earn its place. House rules win: read the repo's `AGENTS.md` overrides first, never merge unless the owner asks, and do not match Hillclimb, Orchestrate, or Autopilot playbooks, arena, or swarm unless named.

**Reply style:** evidence or label on every claim (section 0), short declarative sentences, no em dashes, no mid-sentence colons, impact for the user and the next maintainer first, never a fabricated link. Prose follows `/unslop` (`skills/ui-ux/references/writing/unslop.md`).

**Show me your work** (`/show-me-your-work`): long, autonomous, or step-away runs keep one append-only TSV decision log (`ts, phase, decision, why, evidence, result`) via `references/show-me-your-work/scripts/log.sh`. Evidence is a pointer, never a paragraph. Log forks, completed units, pivots, and blockers. Audit it against the transcript before handing back, and end with an Attention section from a reviewer on a different model. Local by default; commit only when the reviewer needs the trail.

**Recall** (`/recall`): before resuming, rebuild context from recent chats and the shared record (PRs, tickets, errors), verify against live `git` and `gh`, and return a capsule, tagged thread statuses, recurring problems, and one next move.

**Reflect** (`/reflect`): after a long run, three reviewers (judgment, tooling, divergent) mine the transcript, a synthesizer sorts accepted, rejected, and backlog. Move anything a lint or script can enforce to backlog. Get approval before editing any skill.

**Trust artifacts, not summaries.** Inspect a delegate's diff and output yourself. A second opinion is the same prompt on a different model.

## 7. Old skill → where it lives now

Every file under `references/` is listed. Read the file when the "Read when" column matches; the sections above carry the rules that change behavior.

| Old skill | File | Read when |
|---|---|---|
| ponytail | `references/ponytail.md` | Intensity examples, full "when not to be lazy" text |
| ponytail-debt | `references/ponytail-debt.md` | Harvesting `ponytail:` markers into a ledger |
| ponytail-gain | `references/ponytail-gain.md` | Showing the benchmark scoreboard |
| ponytail-help | `references/ponytail-help.md` | Levels, triggers, default-mode config |
| radical-simplification | `references/radical-simplification/index.md` | Fail/pass examples, UI chrome as one way |
| reuse and work budgets | `references/reuse-and-budgets.md` | Hot route/switch, projections, shared observer, duplicate build, cache identity or deletion estimate |
| efficient-systems | `references/radical-simplification/references/efficient-systems.md` | Building or reviewing a hot route, read model, queue, stream, cache, or first paint |
| complexity-optimizer | `references/complexity-optimizer/index.md` | Algorithmic hotspot scan or report |
| (its playbook) | `references/complexity-optimizer/references/optimization-playbook.md` | O(n²) to O(n log n) transformations |
| (its template) | `references/complexity-optimizer/references/report-template.md` | Writing the complexity report |
| (its scanner) | `references/complexity-optimizer/scripts/analyze_complexity.py` | First-pass hotspot list |
| code-simplifier | `references/code-simplifier.md` | Clarity pass on freshly written code |
| deslop | `references/deslop.md` | Full slop checklist and see-also routing |
| no-comments | `references/no-comments.md` | Running the comment reviewer and its accept/reject rules |
| full-output-enforcement | `references/full-output-enforcement.md` | Long deliverables that must not be truncated |
| check-compiler-errors | `references/check-compiler-errors.md` | Compile or type-check failures block progress |
| typescript-best-practices | `references/typescript-best-practices/index.md` | Type design, or a boundary that parses external data. Not every `.ts` or `.tsx` edit |
| (its examples) | `references/typescript-best-practices/references/patterns.md` | Code examples per TS rule |
| tdd | `references/tdd.md` | Full TDD guardrails and final-report shape |
| systematic-debugging | `references/systematic-debugging.md` | Four-phase debugging, red flags, rationalizations, MIT notice |
| (its script) | `references/find-polluter.sh` | Bisecting which test pollutes shared state |
| verify-this | `references/verify-this.md` | Artifact layout and verdict rules |
| blast-radius | `references/blast-radius.md` | Full steps and hand-back shape |
| benchmark-checklist | `references/benchmark-checklist.md` | You are about to report a speedup, a regression, or another performance number |
| correct | `references/correct.md` | The same agent mistake has happened twice, or the user corrects you again |
| create-verification-skill | `references/create-verification-skill/index.md` | Repo lacks a scripted way to drive the app |
| (feature map example) | `references/create-verification-skill/references/feature-map-example/` (`README.md`, `create-note.md`, `search.md`) | Shaping a generated feature map |
| maintain-verification-skill | `references/maintain-verification-skill.md` | Keeping a verify skill's feature map honest |
| grilling, grill-me | `references/grilling.md` | Round format and frontier rules |
| how | `references/how/index.md` | Explorer split, output format, critique mode |
| (how prompts) | `references/how/references/explorer-prompt.md`, `explainer-prompt.md`, `critic-prompt.md`, `critique-rubric.md` | Spawning how explorers, explainer, or critics |
| why | `references/why/index.md` | Investigator roster, skip rules, output format |
| (why prompts) | `references/why/references/epistemics.md`, `investigator-prompt.md`, `synthesizer-prompt.md`, `source-playbook.md` | Spawning why investigators and the synthesizer |
| (why sources) | `references/why/references/sources/` (`code-archaeology.md`, `databricks.md`, `datadog.md`, `incident-postmortem.md`, `linear.md`, `notion.md`, `sentry.md`, `slack.md`) | One playbook per evidence source |
| teach | `references/teach.md` | Teaching style and diagram build-up rules |
| bro | `references/bro.md` | Restating a message plainly |
| architect | `references/architect/index.md` | Phases A to E |
| (architect refs) | `references/architect/references/design-red-flags.md`, `rationale-template.md`, `runner-prompt.md` | Screening sketches, writing rationale, briefing runners |
| interrogate | `references/interrogate/index.md` | Reviewer setup and verdict format |
| (interrogate refs) | `references/interrogate/references/reviewer-prompt.md`, `rubric.md`, `code-quality-review.md`, `lead-judgment.md` | Filling reviewer prompts and judging |
| figure-it-out | `references/figure-it-out.md` | Designing a bespoke playbook |
| poteto-mode | `references/poteto-mode/index.md` | Triggers, autonomy, playbook matching |
| (playbooks) | `references/poteto-mode/playbooks/*.md`: authoring-a-skill, autonomous-run, autopilot-full, autopilot-stack, babysit, bug-fix, eval, feature, hillclimb, investigation, multi-phase-plan, opening-a-pr, orchestrate, pause-safely, perf-issue, prototype, refactoring, runtime-forensics, session-pickup, shipping, trace-forensics, visual-parity, worktree-cleanup | The matching task shape |
| (bugbot triage) | `references/poteto-mode/references/bugbot-triage.md` | Triaging bot review comments |
| (poteto scripts) | `references/poteto-mode/scripts/` (`bootstrap.ts`, `check-plan.mjs`, `worktree-audit.sh`, `orch/`, `watch-pr/`, `package.json`, `bun.lock`) | Tools the playbooks invoke |
| show-me-your-work | `references/show-me-your-work/index.md` | Decision log rules and audit |
| (its files) | `references/show-me-your-work/references/decision-log-template.tsv`, `scripts/log.sh` | Starting and appending the log |
| recall | `references/recall.md` | Output contract for a context brief |
| reflect | `references/reflect/index.md` | Transcript review process |
| (reflect prompts) | `references/reflect/references/judgment-reviewer.md`, `tooling-reviewer.md`, `divergent-reviewer.md`, `synthesizer.md` | Spawning reflect reviewers |
| automate-me | `references/automate-me.md` | Turning a user's habits into a `-mode` skill |
| principle-attack-the-premise | `references/principle-attack-the-premise.md` | Repeated fixes fail the same gate |
| principle-boundary-discipline | `references/principle-boundary-discipline.md` | Placing validation and error handling |
| principle-build-the-lever | `references/principle-build-the-lever.md` | Non-trivial repetitive or checkable work |
| principle-encode-lessons-in-structure | `references/principle-encode-lessons-in-structure.md` | Repeating an instruction |
| principle-explain-the-number | `references/principle-explain-the-number.md` | Before you trust, report, or act on a measured number |
| principle-exhaust-the-design-space | `references/principle-exhaust-the-design-space.md` | Novel design with no precedent |
| principle-experience-first | `references/principle-experience-first.md` | Scope and UX tradeoffs |
| principle-fix-root-causes | `references/principle-fix-root-causes.md` | Debugging |
| principle-foundational-thinking | `references/principle-foundational-thinking.md` | Before writing logic; sequencing |
| principle-guard-the-context-window | `references/principle-guard-the-context-window.md` | Context filling up |
| principle-laziness-protocol | `references/principle-laziness-protocol.md` | Sizing a diff or adding layers |
| principle-make-operations-idempotent | `references/principle-make-operations-idempotent.md` | Commands and loops that retry or crash |
| principle-migrate-callers-then-delete-legacy-apis | `references/principle-migrate-callers-then-delete-legacy-apis.md` | Replacing an internal API |
| principle-minimize-reader-load | `references/principle-minimize-reader-load.md` | Code that is hard to trace |
| principle-model-the-domain | `references/principle-model-the-domain.md` | Stateful or branch-heavy logic |
| principle-never-block-on-the-human | `references/principle-never-block-on-the-human.md` | Tempted to ask about reversible work |
| principle-outcome-oriented-execution | `references/principle-outcome-oriented-execution.md` | Planned migrations and rewrites |
| principle-prove-it-works | `references/principle-prove-it-works.md` | Before declaring done |
| principle-redesign-from-first-principles | `references/principle-redesign-from-first-principles.md` | Integrating a new requirement |
| principle-separate-before-serializing-shared-state | `references/principle-separate-before-serializing-shared-state.md` | Concurrent writers |
| principle-sequence-verifiable-units | `references/principle-sequence-verifiable-units.md` | Sweeps, migrations, commit stacks |
| principle-subtract-before-you-add | `references/principle-subtract-before-you-add.md` | Sequencing an addition |
| principle-test-behavior-not-implementation | `references/principle-test-behavior-not-implementation.md` | Writing or keeping a test |
| principle-type-system-discipline | `references/principle-type-system-discipline.md` | Designing types or signatures |

Moved to other hubs: `/ponytail-review`, `/ponytail-audit`, `/thermos`, `/review-waves`, `/silent-failure-hunter`, `/performance-profiler`, and `/test-audit` live in `skills/audit/`. `/unslop`, `/technical-writing`, and everything a person reads live in `skills/ui-ux/`. `/agent-prompt-engineering` is its own skill. Parallel fan-out lives in `skills/orchestrate-subagents/`.
