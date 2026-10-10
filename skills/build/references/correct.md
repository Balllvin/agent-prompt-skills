---
name: correct
description: "Find the mistakes agents keep repeating in this repo and make each one impossible. Try architecture, then types, then a lint whose error names the fix, then a test, and write docs last. Use for /correct."
disable-model-invocation: true
---

# Correct

The user keeps correcting agents in this repo for the same mistakes. Change the repo so the next agent cannot make them.

Assume every contributor is an agent. It sees only the files it opened. It copies the nearest example. It takes the shortest path that compiles. Design the repo so a change that looks right from one file is right for the whole repo.

## Find the mistake classes

Read recent commits, reverts, review comments, `AGENTS.md`, skill files, and comments that explain workarounds. Group the mistakes into classes. A class counts once it has happened twice.

## Fix each class at the highest level that works

Stop at the first level that makes the mistake impossible. Do not add a lower guard for a mistake a higher level already blocks.

1. Eliminate it with architecture. Give each piece of state one owner. Give each task one supported way. Hide internals so the wrong import fails. Replace a hand-synced list with one source of truth. Delete old ways and dead code an agent would copy.
2. Enforce it with types so the bad state cannot be written.
3. If bad code still compiles, add a lint or CI check. The error names the file, type, or function to use instead. If the pattern is already common, fail only when a change adds more of it.
4. Test the behavior. Fix or delete any test that would still pass if every function it calls returned nothing. See [Test behavior, not implementation](principle-test-behavior-not-implementation.md).
5. Write docs or agent rules last, and only for a judgment call. Nothing fails when an agent skips a doc.

## Fix and prove

Fix the most frequent class first. Finish its proof before the next class.

Prove each new check fails on a real past mistake. Run the same command locally and in the CI job that owns the check. An exception sits on the offending line. It names the reason, an expiry date, and who approved it.

## Keep the rule where it is enforced

Do not add a new paragraph to `AGENTS.md` for a mistake a type, a lint, or a test can already block. `AGENTS.md` owns durable policy. Put a judgment-only rule in the owning skill. Read `lessons.md` for where to record the class. See [Encode lessons in structure](principle-encode-lessons-in-structure.md).

When the user corrects you, fix this instance and add the rule at the highest level that works. If the rule was already written and nothing enforces it, that is a repeat. Fix it at the highest level in the same change. Drop a rule once its mistake cannot happen.

Reply with each class, its evidence, the level you picked, and why a higher level did not work.

Source: cursor/plugins pstack df581122, rewritten.
