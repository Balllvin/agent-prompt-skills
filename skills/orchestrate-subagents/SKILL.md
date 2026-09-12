---
name: orchestrate-subagents
description: Parent keeps the user task and primary edits. Use only to assign bounded helper work including exploration, isolated slices, review, repair, verification, docs checks, or cross-surface audits. Do not hand the full user task to one sub-agent or to a set of workers. Skip for tiny edits, one-line fixes, simple command answers, or single-owner git and release steps.
---

# Orchestrate subagents

Honor nearest repo instructions first. `AGENTS.md`, `README.md`, `lessons.md`, UI architect files, validation rules, branch and worktree policy.

The parent is the implementor and the orchestrator. Sub-agents do parts. They do not do the whole job. They do not cover every product file while the parent only integrates.

When `pstack` is present, read `HOUSE.md`. House overrides win. Unslop child prompts and parent notes. File pointers, not pasted dumps. Parent writes its own summary of child work. Fire a fresh child with consolidated scope instead of trusting a "done" resume.

## Operating model

1. Own the user task. Keep the goal, design choices, and primary product path.
2. Before any worker spawn, name the primary file(s) for that goal.
3. Keep those files out of every worker Allowed list.
4. Edit at least one primary file yourself before you treat worker diffs as done.
5. Split only independent helper parts that improve completeness or speed.
6. One child, one bounded sub-task, one file scope.
7. One writer per file or checkout at a time.
8. Pull results back. Inspect every diff or finding. Integrate, fix, validate.
9. Own the final state. Correctness, tests, docs, branch hygiene, commit, push, PR.

## Hard boundaries

Do not:

- hand the full user request, PR goal, or end-to-end implementation to one child
- ask a child to "complete the task", "implement the feature", or "finish the PR"
- let worker Allowed sets together cover every product file while you edit none
- put every product file for the goal into worker Allowed lists
- use a child as a replacement parent that re-delegates the whole job
- skip parent implementation and wait for workers
- accept work that exceeds assigned scope
- inline large files into a child prompt when a path is enough
- invent a short anti-slop list; point or bake Unslop in full

Do:

- keep the parent on design and primary edits
- explorers map, critics review, verifiers check, workers take narrow slices
- make every worker Allowed set a strict subset of the files the goal needs
- put the parent primary path in Forbidden files for every worker
- state allowed files, forbidden files, and a success check in every child prompt
- reject or trim work that drifts onto the parent path
- design the child's done test before you write the prompt

### Pre-spawn checklist

Abort the spawn if any answer is yes:

1. Does Goal restate the full user request?
2. Could one Allowed set finish the PR alone?
3. Do all worker Allowed sets cover every product file while the parent edits none?
4. Is the parent skipping primary edits and waiting on workers?
5. Would the next prompt equal the full user task?
6. Is the child prompt missing a checkable done test?
7. Are two writers about to share a file, lockfile, migration, or fixture?

## Cursor model

When running in Cursor (including Cursor Cloud) and the Task tool lets you pick a model, pass `model: "cursor-grok-4.6-high"` for every child. Do not omit it. Do not default to Claude, Opus, or Sonnet unless the user names another model for that run. Tell each child to reason at high effort before acting.

When running in Marauder house pstack, follow `.cursor/rules/pstack-models.mdc`. Default is Grok 4.6, no fast, effort high.

## When to delegate

Use a child only when a bounded part is clear:

- map unfamiliar paths, contracts, tests, or sibling surfaces
- implement one isolated slice that is a strict subset of the goal files
- compare frontend, backend, PWA, Smaug, notebook, or QuantLab contracts
- targeted review for correctness, a11y, data fidelity, security, perf, or missing tests
- focused repair after a finding or failing check, without the remaining feature
- verify docs, provider behavior, framework rules, or lessons
- audit near-duplicate surfaces so the fix lands everywhere it should

Skip:

- one-line or single-symbol edits
- small deterministic docs tweaks
- command output faster to answer directly
- git bootstrap, rebase, push, or branch flows
- migrations or release sequencing where parallel writes raise risk
- formatter-only or linter-only mechanical changes
- any case where the only useful prompt restates the full user task

Prefer fewer children. Do not maximize count. Route bulk reads to explorers so the parent window stays small.

## Agent mix

Smallest useful team.

- `explorer`. Read-heavy mapping, evidence, file inventories, contract diffs, docs lookup. Read-only.
- `worker`. Isolated implementation or repair in an assigned file set that is not the primary path.
- `critic`. Bugs, regressions, missing tests, maintainability, UI, data contracts, a11y, security, perf.
- `verifier`. Focused checks, inspect failures, name the smallest repair.

Default for a moderate feature:

1. Parent implements the primary path.
2. One explorer if the file graph is unknown.
3. One worker per disjoint helper slice the parent cannot own at the same time.
4. One critic after the parent integrates the first coherent change.
5. One verifier when checks fail or coverage is unclear.

One-page UI. Parent implements. One critic. A worker only for a disjoint helper surface.

High-risk backend or provider work. Parent implements the router or service core. Add a verifier or a data-contract critic.

## Child prompt

Write Goal so the child cannot finish the user task alone. If it can, do not send the prompt.

Apply agent-prompt-engineering here. Right altitude. One term per concept. Each rule once. Paths, not pastes. Unslop the prompt. Embed an output contract. Done test the child can run.

```text
Task in /absolute/path/to/worktree.
Role: explorer | worker | critic | verifier.
Parent owns: the main task, primary path files <list>, integration, git, and PR.
Your job: <one bounded sub-task>. Part of the main task, not the whole task.
Do not: take the full user goal; expand scope; create branches, commits, pushes, or PRs.
Goal: <deliverable that cannot finish the user task alone>.
Scope: <subsystem, route, component, service, or concern>.
Allowed files: <exact files or directories>.
Forbidden files: <parent primary path and anything else off limits>.
Write mode: read-only | isolated-write.
Boundaries: Do not touch files outside Allowed. Do not take parent-owned primary files unless listed in Allowed.
Verification: <checks to run>. Done means: <checkable exit>.
Context: use paths and search. Do not ask the parent to paste file bodies.
Writing: point at pstack/unslop/SKILL.md or .agents/skills/pstack/unslop/SKILL.md, or bake the full Unslop writing rules. Do not invent a shorter list.
Expected output:
- Answer first. Unslop. No preamble, no restated instructions, no closing summary.
- Changed files or findings with paths and symbols.
- Commands run, with pass or fail.
- Risks and the next repair.
- A recommendation, not a hedge.
Ownership: Parent owns integration, conflicts, final verification, git, and PR.
```

`read-only` for mapping or critique. `isolated-write` for one disjoint implementation or repair. A critic gets `isolated-write` only when the parent asks it to fix one narrow issue it found.

## Write safety

- Stay in the parent worktree unless the parent provisioned another one.
- Never let two agents write the same file, directory, generated artifact, lockfile, migration chain, or fixture at the same time.
- Children do not create branches, worktrees, commits, pushes, PRs, stashes, or index changes.
- One writer for shared control surfaces. `AGENTS.md`, `README.md`, `lessons.md`, `.agents`, `.codex`, `.cursor`, migrations, CI, release scripts, manifests, lockfiles, provider routing.
- Review every child diff before accepting it. Reject, revise, or reassign.
- If a worker finishes the parent-owned primary change, that is scope failure. Rework under parent ownership.
- Repair and verify agents do not receive the remaining full feature. Parent does the first repair on the primary path.

## Loop

1. Explore. Map different surfaces when the file graph is unclear.
2. Implement. Parent edits the primary path. Workers only on independent helper parts.
3. Integrate. Reconcile assumptions. Run focused checks.
4. Review. Critics against the integrated diff.
5. Repair. Parent first when the path is single-threaded. Else a narrow repair.
6. Verify. Tests. A verifier for failures or coverage gaps.
7. Repeat until the checks pass.

Stop delegating when remaining work is one blocking path, agents would fight over the same files, local execution is faster, or the next prompt would equal the full user task.

## Parent review

Do not pass through a child's summary. Read the diff or findings. Write your own.

A vague child result is not done. Narrow the next pass or inspect the work yourself.

Correct the delta only when a child is close. Do not re-prompt the whole task.

After integrate, ask whether the output meets the done test. If not, name the miss and the smallest fix.

## Anti-patterns

- Child Goal that restates the user task.
- Allowed set that can ship the PR alone.
- Pasting whole files into the child prompt.
- Hedged child instructions. "Consider", "where possible".
- No done test.
- Maximizing worker count for coverage theater.
- Treating critic output as merge-ready without parent edits.
