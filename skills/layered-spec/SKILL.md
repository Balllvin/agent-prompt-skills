---
name: layered-spec
description: Use before multi-surface product or workflow work, to write a layered spec and plan PR instead of implementing. Load for /layered-spec, /feature-spec, /startup-pressure-test, /user-research-synthesis, "write a spec", "write a layered spec", "plan the layers", "feature spec", "PRD", "pressure test this idea", "synthesize this feedback", "split this into slices", or when a user-visible result spans several apps, channels (chat, bots, email), a CLI, or an API. Do not use when the user wants the feature built in this thread.
---

# Layered spec

The spec covers the problem, acceptance, surfaces, data contracts, non-goals, global constraints, review focus, and parallel homework layers of easy, easy-ui, hard, and hard-ui slices, with copy-paste tier prompts. It absorbed the old `/feature-spec`, `/startup-pressure-test`, and `/user-research-synthesis` skills; their detail is in `references/` (table under "Before the spec").

Write the spec before the product. This thread ships markdown, not formatters, nodes, UI, or jobs.

An implementer who only reads this skill plus the plan PR must know exactly how to kick a slice, where Owns live, and what they must not touch. They still choose how many layers and letters the work needs.

Unslop the spec, the PR body, the layer map, and both copy-paste prompts. Read `../ui-ux/references/writing/unslop.md`. Do not invent a shorter list.

## Done means

All of these, or the spec is not done:

- A file under `product-specs/` on a **draft** plan PR to `main`
- Spec sections Layer 0 through Layer 6 filled from live code (write `none` and why if a section does not apply)
- One remaining way, named with live paths
- Homework slices in Layer 6 named `L1A`, `L1B`, `L2A`, … each labeled easy, easy-ui, hard, or hard-ui
- Every slice in a layer runs in parallel with every other slice in that layer. Nothing inside a layer waits on anything else inside it
- File sets inside one homework layer do not overlap
- A living `layers.md` (or a slice table in the spec) for writeback
- Two short copy-paste prompts in the reply, with the plan PR URL filled
- No product code on the plan branch
- Plan PR stays draft. Nobody merges it from an implementer thread
- The spec self-review passed and a fresh reader could name each slice's owner files and done test
- The plan states the Merge-ready gate

## Load first

1. `AGENTS.md`, `README.md`, `lessons.md`
2. `/build` (one remaining way, ponytail ultra)
3. `/orchestrate-subagents` (parent maps, children do not finish the spec)
4. Domain skills the live code requires (`/ui-ux`, `/fmp-integration` for metered market data, `/audit` silent failures if a result can fail quiet, `/security` for auth or money, `/provider-routing` if models)
5. Canonical shot: the best existing spec under `product-specs/`, or the nearest live owner in the tree

## Before the spec

A layered spec fixes how to build something. It cannot tell you whether to build it. Do these first when the input is an idea, a complaint pile, or a vague ask, because a clean spec for the wrong problem wastes every slice below it.

1. **Pressure-test the idea.** When the work is a new product bet, run [startup-pressure-test](references/startup-pressure-test/index.md): who has the pain, what they do today, the smallest test that proves or kills it. A weak or pivot verdict ends the spec thread; report it instead.
2. **Synthesize user feedback.** When the problem comes from user complaints, support notes, or interviews, run [user-research-synthesis](references/user-research-synthesis.md): code the notes, group themes, weight by frequency and impact. Layer 0 cites the themes, not one loud quote, so the spec solves the common case.
3. **Write acceptance like a PRD.** Use [feature-spec](references/feature-spec.md) for Layer 0 and Layer 1: problem with evidence, goals as outcomes not outputs, non-goals with reasons, and Given/When/Then acceptance criteria. Why: acceptance an implementer can test is what lets a slice say "done" without asking.

| Reference | Use for |
|---|---|
| [startup-pressure-test](references/startup-pressure-test/index.md) | Verdict on whether the idea is worth building; [playbooks](references/startup-pressure-test/references/playbooks.md) per mode. |
| [user-research-synthesis](references/user-research-synthesis.md) | Turning feedback, surveys, and interviews into ranked themes. |
| [feature-spec](references/feature-spec.md) | PRD shape, user stories, MoSCoW, success metrics, acceptance criteria, scope creep. |

## Path

Put specs in a tracked folder. If `docs/` is gitignored scratch in your repo, never put a spec there. Never stage scratch folders or `worktrees/`.

Write `product-specs/<slug>.md`. Split by responsibility if the file would cross 500 lines. Link parts from that folder. Keep a `layers.md` next to the spec for slice status.

## Two numberings

Do not mix them.

| Name | What it is | Example |
|---|---|---|
| Spec sections | How the plan is written | Layer 0 Problem, Layer 1 Acceptance, … Layer 6 Ship slices |
| Homework waves | How the product ships later | `L1` is a parallel wave. `L1A` is part A. `L2` starts after every `L1*` PR has merged |

The user kicks a slice by typing `Implement L1A: ` and pasting the easy, easy-ui, hard, or hard-ui prompt **after the colon**. The paste does not bake the slice id. The implementer reads the plan PR, finds that id, and owns that part.

## This thread (spec parent)

This is a feature-spec plus a ship map. It is not feature-dev implementation.

From feature-spec: problem, goals, non-goals, testable acceptance, who is served, open questions, cuts that prevent scope creep.

From feature-dev: understand live code before designing, ask underspecified questions before locking Layer 6, name the remaining way as architecture. Stop before implementation. Do not wait for a second approval to write the spec. Do wait for answers to **blocking** questions before writing homework slices.

From orchestrate-subagents: the spec parent owns the spec files, the remaining way, and the layer map. Children do not write the spec, do not git, and cannot finish the user request alone.

Spec markdown only. Draft PR to `main`. No product code, no migration, no UI, no armed job, no production or hosting change.

Each homework slice is a later PR from fetched `origin/main`, not from this plan branch. Do not `gh pr checkout` the plan PR to implement.

## Remaining way

Before Layer 4, write one sentence per job: the live object that owns it, or skip.

If two homes already exist, name the survivor and forbid growing the other. Do not add a third.

Workflow work (when that is the job): name the one file or table that is the graph's source of truth, the one component that binds schedule and delivery, and the one walker that runs it. An agent runtime is a node, not a second DAG engine. User-facing copy comes from a deterministic cleaner, not an LLM. An LLM rewrite may polish already-cleaned text. It must not be the formatter.

UI chrome work (when that is the job): the `ui-ux` skill owns the shared grammar. Each app's live file owns the surface. Do not extract a shared kit.

Other work: name the live owner the same way. One object, one path.

## Orchestrate while writing the spec

Parent maps first with path-scoped `rg`. At most two read-only explorers, and only for surfaces the parent has not opened.

Every child prompt: one bounded map, Allowed paths, Forbidden = the spec files the parent will write, a done test, inherit parent model, no git. Abort the spawn if the child's Goal restates the full user request or if one Allowed set could finish the plan PR alone.

Do not maximize explorers. Do not hand Layer 6 construction to a child. Parent writes the spec.

## Spec sections

Write them in order. A later section must not contradict an earlier one. Skip a heading only when you write `none` and why. If any required box below is empty, the spec is not done.

### Layer 0. Problem

Who saw it, on which surface, what they were trying to do, what they got instead. Cite live files.

Not a problem: "we should add a layer", "improve UX", "make it nicer".

Ground it. A screenshot, a URL, a run id, a quoted chrome class.

### Layer 1. Acceptance

Testable checks. A command, a golden string, or a UI assertion. Cover the failure path.

Each criterion says what must appear and what must not.

Human surfaces must never present JSON. CLI and MCP stay compact JSON.

If the work is UI, say which chrome stays and which chrome goes.

### Layer 2. Surfaces

Table every place a person (or machine) can see the result. Live owner. Human or machine. Duty.

A slice that "fixes the bot message" and leaves the in-app report dumping extras has a missing row here.

### Layer 3. Data contracts / cleaners

The structured result and the one deterministic formatter, or `none` and why.

Same inputs, same output. Golden tests, not prompt vibe.

### Layer 4. Platform capabilities

If the work is a workflow, fill this table against live owners. Propose only what the remaining way can grow.

| Concern | Ask |
|---|---|
| Nodes | Which types exist. Which new type is a real job. |
| Edges | Directed DAG today. Branching only if the walker can fail loud on a fork. |
| Schedules | Scheduler cron / time of day / timezone. Not a DAG node. |
| Inputs | Graph input fields plus scheduler inputs. Missing inputs abort. |
| Delivery | Scheduler-owned channel summary and in-app packet. Notify is not a node. |
| Retries | Walker is fail-first. |
| Observability | `run_id`, traces, node error `kind`. No second run store. |
| Templates | The repo's example workflow files. |

If the work is not a workflow, fill the same table with that product's equivalent owners, or write `none` and why.

### Layer 5. Non-goals

Cuts. One reason each. "Second engine", "would dump JSON at a human", and "second kit" are reasons.

Do not park work under Later, nice, or maybe. If a live owner already has the data, put it on a slice. If it needs a new engine or a new channel, cut it.

This is the scope fence. A later slice must not quietly do a non-goal.

### Global constraints

Project-wide values every slice must honor, copied verbatim from the spec, `AGENTS.md`, or the live code: exact version pins, limits, names, route shapes, copy strings, privacy rules. A slice prompt points here instead of restating them. Why: a value paraphrased in six slices drifts into six values. Adapted from obra/superpowers `writing-plans` (MIT).

### Review focus

The three to five inputs or failure modes the spec implies but no slice's Done-when tests yet. Pair each with the test that pins it and the slice that owns that test. Reviewers read this list first. Why: acceptance covers the happy path the author pictured; review focus names what the author did not. Adapted from obra/superpowers `writing-plans` (MIT).

### Layer 6. Ship slices

Read [slice ownership and effort](references/slice-review.md). Classify the actual decision and state risk; keywords and file size are not a tier rubric. List contiguous easy, easy-ui, hard, hard-ui blocks in each layer and assign letters in that order. Keep evidence rank separate from parallel dispatch order.

Homework waves. You choose how many layers and how many letters. The constraints are the freedom.

**A layer (`L1`, `L2`)** is a set of slices that all start from the same fetched `origin/main`. They run in parallel. File sets inside a layer must not overlap. Shared control files are never a slice: `AGENTS.md`, `lessons.md`, lockfiles, CI, the model-routing core, migration heads other slices also need.

**A slice (`L1A`, `L1B`)** is one implementer thread, one worktree, one branch, one draft PR to `main`. Label it **easy**, **easy-ui**, **hard**, or **hard-ui**. Do not label every slice the same tier.

**A slice is a verifiable unit.** End it in a check. Do not add a compatibility shim to keep an intermediate state smooth. [Sequence verifiable units](../build/references/principle-sequence-verifiable-units.md). [Outcome-oriented execution](../build/references/principle-outcome-oriented-execution.md).

**The parallel rule is absolute.** Every slice in a layer starts at the same time, from the same `origin/main`, and none of them waits for another. Never write "L3B after L3A", "step 3.1 then 3.2", or a `Depends` that names a slice in the same layer. If B needs A's merged code, B goes in the next layer. One feature may span two, three or four layers. That is normal and good. A layer is a batch of parallel work, not a feature. A layer that ends with a feature half-built is fine, as long as each slice leaves a stub that fails loud. This rule overrides anything else in this skill and any later request to "just do A first". If ordering is needed, add a layer.

**hard-ui:** the person reads or taps this slice, and the work is a screen or several screens, or a UI flow with backend glue. Empty, loading, stale, and failed states, phone and desktop screenshots, and `/audit` review waves (at most three). Give it to the strongest agents.

**easy-ui:** the person reads or taps this slice, and the target is clear: copy, a state the screen is missing, a field render, a small fix in named components. The agent may make small choices inside its files. No new layout and no new flow. Do not run `/audit` review waves.

**hard:** mainly backend, runtime, security, data, packaging, or a failure path that can go quiet. It needs tracing or design. A few lines of frontend glue are fine. Never a screen. `/audit` review waves, at most three.

**easy:** a clear target in named files with no design: deletions, moves, import rewrites, dead code, test retargets, a bounded bug fix whose fix is stated, config, docs. The agent traces callers and makes the small choices inside its files itself. Do not run `/audit` review waves; run `/build` deslop. An easy or easy-ui slice lists:
- the files, or an `rg` that produces the file list
- the change, stated as a rule or an end state ("every `from x import y` imports from `z`", "the 429 path raises `FmpRateLimited` with the ticker")
- the commands that prove it, and what they print when done

Default up. When a slice is mechanical once its target is stated, state the target and make it easy. Reserve hard for work that needs a design choice the spec cannot make in advance.

Put in Owns every test file the change will break (callers' tests, fixtures, fakes). A slice whose Owns leave out its callers' tests cannot go green, and its agent will either stop or merge red.

For generated mirrors, inspect the generator manifest before assigning Owns. Reserve the canonical source and affected mirrors, or schedule the canonical change first. Keep the manifest parent-owned.

Trace each acceptance target through its client and server boundaries. Assign every required contract change and its public proof. If another owner must deliver it first, schedule that prerequisite explicitly. Do not publish an AND acceptance whose required server change is forbidden by Owns.

Split the decision from the screen when their files do not overlap. The earlier layer owns the rules and the packet. The UI slice in the next layer only reads that packet. Do not put a ranker and a screen in one slice when a later layer can render the result. A user-facing string with no layout judgment is its own easy-ui slice. It does not ride inside a hard backend slice, and it is not labeled easy.

Pack the layer. Several features in `L1` is normal if Owns cannot overlap. Start depth in `L1`, finish it in `L2` when the next part must import merged code or when two jobs share a file.

`L2` starts after **every** `L1*` homework PR has merged. Same for later layers. Rebase onto that `main`. Inside `L2`, all slices again start together.

Do not serialize one feature per layer when other features' files are free. Do not split two edits that share a file into parallel slices. Merge those into one slice. Pick the tier from the main job.

If two skins implement the same contract and their Owns cannot overlap, they may be parallel in the same layer. The spec is the contract. Do not invent a second remaining way.

Inspect `origin/<agent>/<slice-id>` before assigning a branch. If that name is leftover unrelated work, the spec names a unique prefix. Put the branch name on the slice.

The label after the id is easy, easy-ui, hard, or hard-ui.

```markdown
### L1A hard. <one-line job>
Branch: <agent>/<unique-id>
Owns: <paths>
Forbidden: <shared files, plus every other slice in this layer>
Depends: none inside this layer (all earlier layers merged)
Done when: <command that goes red if this slice is reverted>
Skills: <extra skills beyond the paste>
```

`L2A` Depends: all `L1*` merged. Never another `L2*` slice.

Files already near 500 lines: the slice extracts or reuses. It does not grow them.

Match each Done-when proof to AGENTS test policy. Use public results, real operation counts, compiled contracts or measured workloads. Do not offer source-text deletion or syntax checks as behavior proof.

Migrations (for example Alembic): the parent serializes revisions against the current single head. A slice may propose its schema change, but cannot create a competing head or rewrite a sibling revision. Rebase the assigned revision at integration and run the repo's single-head check on the merged tree.

Grant a baseline exception only with its exact test ID, immutable main SHA, reproduction evidence and owning fix. Link that list from the affected slice, or say no per-slice exceptions are granted. Unrun tests are not evidence of a clean base.

`layers.md` starts with every slice `planned` and an empty PR cell. Implementers fill only their row.

## Merge-ready gate

State this in the plan: the owner merges only homework PRs whose plan-PR report says `Merge-ready: yes`. `Merge-ready: yes` means every Done-when line has its proof, the repo gate is green apart from exact documented baseline exceptions, and nothing sits under Needs owner. Anything else is `Merge-ready: no` with the reason. A layer starts only when every slice of the layer before it merged under this gate.

## Spec self-review

Run this before you push the plan PR, and again after any edit to Layer 6. Fix what fails; do not publish around it.

1. **Owns are complete.** Every slice's Owns include the tests of its callers, fixtures, and fakes the change breaks (`rg -l "<module>"` under the test dirs). Match every Expected/Verify target to an owned live boundary or a scheduled prerequisite. Check projections, schemas and transport-byte proofs, not just client callers.
2. **Zero overlap per layer.** Run `python3 <skills-dir>/layered-spec/scripts/check-slices.py <slice-parts...>` and inspect shared controls. Include reserved paths and every deletion target; evidence-only paths stay read-only.
3. **Every Done-when line is checkable.** A command with its expected output, a golden string, or a UI assertion. "Works", "looks right", and "is clean" fail.
4. **Baseline exceptions are explicit.** Exact test IDs, immutable main SHA and reproduction evidence are linked, or no exception is granted. A generic known-red phrase fails.
5. **No placeholders or contradictions.** Tier blocks and letters are ordered; changed published IDs have a complete remap. Gross removal and net replacement estimates are distinct. No `TBD`, `<fill>`, or two sections that disagree about an owner or a value.
6. **Reader test.** Give the spec path to a fresh sub-agent with no context and ask it to name, for three slices, the owner files, the forbidden files, and the done test. Every miss is a spec bug. See the reader test in `/ui-ux` ("Words users see").

## Blocking questions

After the live map, list underspecified behavior. Tag each blocking or not.

Blocking: do not write Layer 6 until the user answers.

Non-blocking: record in the spec. A slice can start.

If the user says "whatever you think", state the pick in the spec and proceed.

## Copy-paste prompts

Owns, Forbidden, Done when, and extra skills live in the spec. The paste carries only what every slice of a tier shares. The implementer reads the plan after `Implement L1A: `. Replace `<SPEC_PR_URL>` and `<SPEC_PATH>` once the plan PR exists. Never bake a slice id into the paste.

Every prompt starts with the common block, then its tier block.

### Common block

```text
Read AGENTS.md. Your slice id is the token after "Implement", before the colon. Find it in <SPEC_PATH> on the plan branch (plan PR <SPEC_PR_URL>), with its exact baseline exceptions, if any. Never build on or merge the plan branch.
Setup: git fetch origin main --prune, then a new worktree on the branch the slice names from that origin/main. Follow AGENTS.md "Fresh worktree setup".
Finish the slice. Do not end your turn with a question: decide reversible things, note the choice under "Changed from the spec", and keep going. Only secrets, money, production, hosting, keychains, or a product decision the slice leaves open go under "Needs owner"; do the rest around them.
Files: build inside Owns and own every regression your change causes. If repair needs another path, give the parent its exact path and failing test so ownership can be updated before repair. Never edit a sibling's file or infer permission from a source citation.
Skills: /build on every slice; /ui-ux for the PR body and the report (words people read); /ship-verify for the gate, rebase, and PR.
Checks: iterate with focused tests, including every test file for the modules you change. After the final rebase run the repo gate once and rerun only failed jobs. A red test is yours unless an exact documented baseline exception applies or you reproduced it on the immutable origin/main SHA. Never skip, xfail, loosen, or lengthen a timeout on a test. New and changed tests pass the /audit test gate, and the main change has a test that fails when reverted.
Hygiene: commit after each finished step. Wait only on your own processes. Before your final message stop your servers and watchers and drop scratch databases. Evidence goes in the PR body.
Report: draft PR to main linking <SPEC_PR_URL>. One comment on the plan PR, edited in place, never a second: Slice / PR / Merge-ready: yes or no, and why / Implemented (each Done-when line with its proof) / Not implemented (reason in your words) / Changed from the spec / Found / Needs owner / Checks. Then update only your row in layers.md on the plan branch. Do not merge.
```

### Easy block

```text
This slice is easy: a clear target in named files, no design. Trace callers and make the small choices inside your files yourself. If the slice text is wrong (a file, symbol, or command does not match), take the obvious reading, post "Found:" on the plan PR, and continue; if there is no obvious reading, skip only that step. No screen changes. Do not run /audit review waves; run /build deslop on your diff.
```

### Easy-ui block

```text
This slice is easy-ui: a clear target on a screen. Load /ui-ux and the UI architecture doc of each app you touch, if any. Change the strings, fields, and states the slice names; keep the layout. Trace callers and make the small choices yourself. If the slice text is wrong, take the obvious reading, post "Found:", and continue. Screenshot each changed screen at 390x844 and desktop (or an offscreen native render from a test) and embed them in the PR. Do not run /audit review waves; run /build deslop.
```

### Hard block

```text
This slice is hard. Read README.md, lessons.md, and the spec files the slice names. Trace the real flow and list every caller before you edit. Load the slice's Skills; run the /build blast-radius check before cross-cutting edits, and /security when the slice touches auth, keys, money, or untrusted input. Name the one remaining way in a sentence and make the tree match it. Where a later layer fills a slot, leave a stub that fails loud. /audit review waves (max 3): wave 1 runs all five critics; later waves re-run only critics that found something, after you fix it. If critics are unavailable, run the /audit thermos pass yourself and say so. Post "Found:" for bugs or spec errors anywhere; fix them when the file is yours or unowned.
```

### Hard-ui block

```text
This slice is hard-ui. Read README.md, lessons.md, /ui-ux, the UI architecture doc of each app you touch, and the spec files the slice names. Walk the current screens first and keep recent UI work unless it is buggy. Ship end to end on every surface the slice names, with empty, loading, stale, and failed states and tests that fail if reverted. Reuse the shared kit; split files that would pass 500 lines. Prove the flows with Playwright against a running app; screenshots at 390x844 and desktop, plus a native window or an offscreen render (never sign in with the owner's Keychain). /audit review waves (max 3) as in the hard block; /security as in the hard block. Post "Found:" for bugs anywhere; fix them when the file is yours or unowned.
```

## Write back

The implementer's single plan-PR comment (common block) is the write-back. Then spec-only on the plan branch: that row in `layers.md`. Rebase if a sibling already updated the map. No app source.

## Process

1. Restate the failure in Layer 0. Cuts in Layer 5.
2. Map live owners. Parent first. At most two read-only explorers.
3. Ask blocking questions if the remaining way is still a guess.
4. Fill spec sections 1 through 5, Global constraints, and Review focus. Name the remaining way.
5. Split Layer 6. You pick the count. Every slice in a layer runs in parallel: no order inside a layer, ever. Zero file overlap inside a layer. Label each slice easy, easy-ui, hard, or hard-ui. Put rules in a backend slice and screens in a UI slice when the files allow it. Anything that needs another slice's merged code goes in the next layer.
6. Run the spec self-review. Fix every miss.
7. Write on `<agent>/<task>` from latest `origin/main`. Push a draft plan PR. Never merge it.
8. Reply with the plan PR URL, the slice table, the four prompts with the URL filled, and cuts.

## Reply shape

1. Plan PR URL
2. Spec path
3. Slice table: id, tier, one-line job
4. The four short prompts, URL already filled. User types `Implement L1A: ` then the matching paste after the colon.
5. Cuts you skipped

## Completeness gate

Tick before you open the plan PR:

- [ ] Layer 0 names a user-visible failure with a path
- [ ] Layer 1 is testable, including a failure path
- [ ] Layer 2 lists every human surface that can show the result
- [ ] Remaining way is one sentence per job, with a live owner
- [ ] Layer 5 has cuts with reasons
- [ ] Every Layer 6 slice has Owns, Forbidden, Done when, one of easy / easy-ui / hard / hard-ui, and a branch
- [ ] No two slices in the same homework layer share a file
- [ ] No slice depends on another slice in its own layer, and no layer has steps or an internal order
- [ ] Every easy and easy-ui slice lists exact files, exact edits, exact commands, and the exact Done-when output
- [ ] `L2*` Depends names merged `L1*`
- [ ] `layers.md` exists
- [ ] Easy, easy-ui, hard, and hard-ui pastes are in the reply, plan PR URL filled, no baked slice id
- [ ] Global constraints and Review focus are filled
- [ ] Spec self-review passed, including the fresh-reader test
- [ ] The Merge-ready gate is stated in the plan
- [ ] Plan PR is draft. No product code

## Examples

Good Layer 0: the user's bot trial of the weekday portfolio-review workflow dumped the walk as raw JSON. The decision model's answer and the source rows were in the blob. Run id `workflow-<id>`. The content was a useful review. The presentation was a stack dump.

Bad Layer 0: "Improve workflow UX across surfaces."

Good Layer 1: a unit test feeds a walk result and asserts a golden string with no `{` and no `"verdicts"`.

Bad Layer 1: "Make the bot message nicer."

Good Layer 6: `L1A` hard owns the packet. `L2A` hard-ui owns the web screen. `L2B` hard-ui owns the mobile screen. The screens share the packet. They do not share a file. An exact label change is easy-ui, not hard-ui.

Bad Layer 6: two parallel slices both edit `globals.css`.

## Do not

- Implement the product in the spec thread
- Merge the plan PR
- Bake a slice id into the paste
- Tag unrelated PRs in this skill
- Accept JSON as the user-visible shape in bot messages, cards, reports, or agent results
- Use an LLM as the only formatter
- Invent a second DAG engine or a shared UI kit for one job
- Arm a production job or edit hosting config
- Put specs in `docs/`
- Split two edits that share a file into parallel slices
- Put an order inside a layer ("A then B", "step 1.1 / 1.2", Depends on a same-layer slice). Add a layer instead
- Write an easy or easy-ui slice that needs a judgment call
- Label a screen as easy, or a backend ranker as hard-ui
- Put a ranker and a screen in one slice when their files can live in two layers
- One feature per layer when other features' files are free
- Hand the full spec to one explorer
- Let children git, PR, or write the spec
