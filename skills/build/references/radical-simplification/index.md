---
name: radical-simplification
description: >
  Use for new work, review, audit, two parts that serve one job,
  "how should I build this," "what should quality be," "Can I
  simplify this?", and any hot route, read model, queue, stream,
  cache, first paint, or "make this faster / cheaper" task. Name one
  remaining thorough way. Make the tree match it, even if that means
  ripping architecture. Do not use to wrap two lives, keep a second
  home, drop a real failure state, or invent a thinner wrong path.
---

# Radical Simplification

The simplest approach that still does the thorough job. Never simplify by
dropping a real failure state or inventing a thinner wrong path.

This is not ponytail. Ponytail is the smallest thing that works. This skill
is one way to do the job, even if you rip the house.

## The job

Name the ending with Musk's algorithm. Order matters.
1. Question the requirement. Who asked. Do we need this job at all.
2. Delete parts and steps you can. You will add some back.
3. Then simplify. Do not simplify something that should not exist.
4. Automate last.

Then: one sentence (one way, one name, one owner). Make the tree match it.
Do not keep a split because it already exists. That is analogy. Name the
constraints, then the tree.

Take the easy path only when the ending is the same. If easy leaves two
homes, two names, or a facade, it is not the same ending. Do the harder
delete.

## When

1. Default: apply. Make the tree match the ending.
2. If nothing exists yet, name the ending and the architecture in one
   sentence before you write. Then ask whether that architecture is
   already the one way.
3. If asked only to review or audit, write one line per finding. Rank
   them. Apply nothing. Tag each finding `second-home`, `wrapper`,
   `silent-path`, `type-home`, or `quality-drop`.

## Rules

1. Ending first. If you cannot name the one remaining way in one sentence, stop.
2. If two modules, paths, or types exist for one job, integrate or delete.
   Delete the wrapper, the layer, pass-through helpers, and
   single-implementation interfaces. Do not keep both plus a switch.
3. If the split is the complexity, change the architecture. A new folder
   must replace the old ones in the same PR.
4. Deleted code must leave the tree: imports, tests, dead files, and flags
   that preserve the split.
5. Distinct failure states stay distinct (`401`, `503`, `user_id: 0`, empty
   last-good). Distinct implementations of the same job do not. Delete
   try/catch on trusted paths, null guards that cannot fire, and optional
   fields that hide the boundary. Catch-log-and-continue and
   return-null-on-error are a second, silent path. Delete them.
6. Leave the test that hits the remaining implementation. A test that only
   asserts a mock was called does not prove one path.
7. If you cannot pick or integrate into one survivor, stop. Do not invent a
   third home.
8. Do not fabricate evidence on the surviving path. Chained `as` casts,
   widen-then-assert, `unknown`/`object` parameters, and empty-object
   spreads that hide a field are a second type-home. Fix the real type.

## Forbidden

- This file and `references/efficient-systems.md` are the rules. Do not hand the job to another skill.
- Wrap, facade, adapter, pass-through helper, single-implementation
  interface, or `getX()` over two lives.
- A worker, cache, queue, or flag that papers over two homes is not automation.
- A ten-line patch in the survivor while the second part still exists.
- Rename-as-simplify, comment-as-delete, or `deprecated` without removal.
- A module named `radical-simplification`.
- "Too risky to change architecture" as the default. Risk sequences the
  delete. It does not keep two ways.

## Fail / pass

Fail: two auth (or fetch, or error) paths stay; a new `getX()` maps every
miss to one flag. Fail: a thin wrapper over two lives. Fail: a test that
only asserts a mock was called. Fail: a thinner wrong path that drops a
real failure state. Fail: reviewed, left two homes.

Pass: one remaining path owns the job; the other is gone from the tree;
the miss is fixed there; a test proves callers hit only that path.

## Fast by design

Speed and cost follow the same rule: the fastest work never runs, the next fastest already ran before the request arrived. Read `references/efficient-systems.md` before you build or review a hot route, read model, queue, stream, cache, or first-paint path.

Latency is trips × distance + work per trip. Attack in that order:

1. Eliminate trips. A read model or one aggregate endpoint, not ten calls.
2. Shorten trips. Memory, client store, Postgres, then provider.
3. Move work to write time when reads dominate.
4. Only then make the work cheaper: algorithm first, language last.

Classify and measure the actual cost before choosing a tool. Generic provider, SQL or framework latency ranges are not evidence. I/O wait does not get faster in Rust. Move hot CPU or memory work across a language boundary only when equal-behavior profiling shows a gain that earns it; small confirmed gains remain in scope. Prefer existing SQL aggregation and native-backed libraries first. Read [reuse and work budgets](../reuse-and-budgets.md) for actual caller/cache identities and count proofs.

Measure resident memory and idle work alongside trips. Profile queue polling, boot imports, unbounded provider-payload retention and forced refresh. Remove repeated work while preserving the consumer's latency, freshness, cancellation and failure contracts.

The five laws:

1. Serve first paint from a bounded read model, never a provider fan-out. Enqueue refresh; return freshness metadata.
2. Scope every cost to the visible screen: the rows shown, the symbols shown, a disclosed cap.
3. Bound everything: deadlines per section, pool size, payload size, finite retries.
4. Never trade honesty for speed. A cache hit is not a live tick; a degraded section is not empty; a 429 is not an empty history.
5. Measure before and after, then leave the test that fails if the slow path returns (request or query counts, deadline, N+1 guard).

Freshness is a product rule per data type. Closed-session and completed-bar reuse follows the owning correction/adjustment policy; finished data is not automatically immutable. User writes need read-your-writes, not a TTL. The full ladder is in the reference.

## UI chrome

Working-product chrome is a job. Name one remaining visual way. ui-ux owns the shared grammar. The app UI architecture doc owns tokens, shells, routes, and the owner's feedback log. Do not copy the skill into the architect file. Do not grow the architect file with shared "one heading / five states" doctrine.

A chat composer is one cluster: oval well plus any focus, quote, or attachment chips, overlaying the transcript. A hairline footer plus that oval plus a chip plate is three homes. Keep the oval. Delete the band and the plate. Do not extract a shared `ChatComposer` package. Each app's live composer file is the owner.

Ponytail still picks the smallest code. This skill still picks the one remaining way even when that means ripping a dock that already exists.

Tag UI audit findings with the same labels: `second-home` (band plus oval), `wrapper` (plate around chips), `silent-path` (composer that drops failed send), `quality-drop` (thinner oval that hides send).

