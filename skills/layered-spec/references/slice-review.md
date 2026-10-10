# Review slice ownership and effort

Read this before locking or changing Layer 6. `/build` owns implementation; this check makes the handoff runnable.

## Tier by the work, not its name or line count

Use `easy` for an exact mechanical target with an existing public keeper and no unresolved design. Use `easy-ui` for the same kind of change in a rendered screen. Use `hard` for semantic, cross-owner, concurrency, transaction, security, freshness or compatibility decisions. Use `hard-ui` when that work changes screen state or a user flow.

A small diff can be hard. A large mechanical deletion can be easy once caller absence, every deleted path, and the surviving contract are proved. Words such as "delete", "normalize" or "duplicate" do not determine effort. Several individually simple cuts remain hard when their state or verification is coupled. Do not bundle scopes merely to reduce the slice count.

Record the tier reason and any changed tier. Keep UI classification tied to the actual edited behavior, not a read-only component citation. Review reserved extraction/proof paths and caller tests as part of the scope.

## Make every owner executable

- For a typed result cut, trace the callback or protocol signature through every producer, consumer and direct test/fixture binding. Reserve the definition and affected bindings in Owns before dispatch; naming only the consumer leaves the change impossible inside its fence.
- Trace tests through public route, CLI and MCP dispatchers. Direct-import searches miss generic entrypoint callers. Follow compatibility facades to the live owner before assigning paths.
- When removing the last client call, retire its unused route permission. Keep strict inventory and authorization checks.
- Enumerate every file to delete, every caller test/fake that must change, and any reserved new path. A count such as "delete 32 pages" is not an Owns list.
- Keep evidence-only paths read-only. Citing a canonical cache, shared source verifier or schema does not itself authorize editing it or justify serializing every consumer.
- Put shared CI, provider core, generators, lockfiles and competing schema heads in a named parent-controlled queue. Validate actual path sets, including reserved paths, before parallel dispatch.
- Require a count, result, absence check or benchmark that fails on reversion. Existing tests passing alone does not prove an efficiency cut.
- When a helper replaces repeated work, reserve proof at the caller that invokes it. Helper-output parity proves the result, not fewer invocations. For render/effect cuts, drive the actual mounted owner through draft updates, committed changes and refresh; count executed work and fail on reversion.
- Name the exact focused command for every owned proof, including a reserved test path if created. Distinguish tests that exist on the inspected base from optional new proofs. If a reserved proof is unnecessary, its acceptance must run through a named existing boundary; do not omit the reversion target.
- Give each baseline exception its exact test ID, immutable main SHA and reproduction evidence. If no exception is granted, say so. Unrun tests do not justify a "none failing" claim.

## Recheck published assignments

Fetch current main before dispatch and integration. If another merge removed or relocated the target, inspect the surviving owner and keeper. Record the resolving PR, immutable main SHA and boundary proof. Keep the historical ID; do not widen Owns or create an empty implementation PR.

If a keeper disproves the proposed cut, withdraw the finding with its failure evidence. Do not add a feature merely to make the deletion safe. Audit withdrawals and external resolutions before advancing the layer; never count them as campaign merges.

Trace the accepted finding to its actual writer, durable model and every reader/recovery path before reserving a storage prerequisite. Similar model names do not establish the same domain or grain. If a slice needs a parent-controlled prerequisite, schedule that narrow prerequisite before the dependent work; do not place it after the layer whose completion requires it. Keep the full between-layer control separate and serialize any shared owner.

## Keep the map readable

Within each layer, list contiguous `easy`, `easy-ui`, `hard`, `hard-ui` blocks and assign letters in that order. Use A through Z, then AA onward. This is display order, not a dependency or performance rank; every slice in the layer remains parallel. Keep the evidence rank separate.

Before renumbering a published plan, check implementation status. Preserve active assignments; for unstarted slices publish the old-to-new map and update branches, anchors, finding links, tracker rows and reader-test references together. Keep stable finding identities. Run the fresh-reader test after the map changes.

Run `python3 skills/layered-spec/scripts/check-slices.py <slice-parts...>` for exact path collisions, missing contracts and tier-block order. Inspect policy-sensitive ownership yourself; a parser cannot decide whether two files share a transaction or schema head.

## Report deletion honestly

Sum exact deduplicated removal ranges, separately for production and tests. Label current gross removable lines, replacement estimates and expected net reduction separately. A file size is not a promise to delete that file. Exclude aliases, conditional findings, retained cases and line estimates that overlap. If net reduction is unmeasured, say so and give the quantified floor instead of inventing a repository-wide total.
