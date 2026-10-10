# Reuse and work budgets

Read this when changing a hot route, list, cache, import, poller, stream, or screen that a person switches away from and back to. `/fmp-integration` owns provider policy; `/audit` owns evidence and test retention.

## Trace what the next caller pays

State the visible job and follow its real caller through auth, service, cache, SQL, provider, serialization and render. Then trace the next page, second symbol, second app and repeat visit. Name the existing writer, reader, identity and freshness rule for shared facts. Reuse them before adding a request, helper or cache. A skill naming an owner does not prove that the caller uses it.

Check siblings after a fix. A warm summary read does not prove its enrichment or builder siblings are bounded. Record cold, warm, stale, empty and failure paths separately. Distinguish helper calls from wire calls suppressed by lower caches or single-flight.

## Make the owner do less

- Pass a validated identity, built document, decoded policy or decorated holdings through the current request instead of fetching, building or decoding it again. Keep independent security and mutation checks fresh.
- Read the saved result before resolving optional provider input when the saved identity and freshness are already known. Preserve the miss, stale and explicit-refresh behavior.
- Reuse successful shared inputs without memoizing a fetch failure across callers unless the existing owner defines that policy. Preserve a later caller's recovery after the first fetch fails; prove failure-then-success at the transport boundary alongside the successful request-count budget.
- For a new write-time projection, trace every source writer and release overlap before enabling stored reads. Recheck writers added during integration, including direct transfer and mirror paths. Preserve caller transactions and old-reader compatibility; repair stale derived values through a sequenced additive migration after old writers drain.
- For a schema repair, qualify inspection and every read, write and downgrade to the same resolved schema. Prove that an empty active schema leaves visible fallback tables unchanged. Follow your repo's durable-state migration rules.
- For lists, select the columns the response actually uses. Keep full content on detail/explicit opt-in paths. Compute readiness as a scalar when the serializer only needs presence. Prove that a projection does not trigger lazy loads, `MissingGreenlet`, or an extra query.
- Put scope, filter, stable order and per-entity selection before LIMIT. A capped broad scan can still omit the requested latest row. Keep complete aggregation separate from bounded screen reads.
- Batch independent SQL on the existing session. Never gather operations concurrently on one AsyncSession. Use bounded concurrency only for detached work or tasks with independent sessions; retain transaction, lease and cancellation order.
- A concurrent pair must own both tasks until they finish. On failure or caller cancellation, cancel and await unfinished siblings before releasing its lock, lease or session boundary. A fail-fast gather alone leaves work running. Prove an immediate failure with a blocked sibling and an overlapping retry; assert cleanup, no duplicate cold-flight work, unchanged error precedence and cancellation propagation. A barrier that releases both tasks together misses this case.
- Use sets, indexes and one-pass projections for repeated membership/search work. Preserve tie order, Unicode, timestamps, error precedence and formula semantics. Benchmark engine-dependent allocation claims before proposing a new implementation.
- Check a duplicate import before provider fetch when its identity is known. Keep the locked post-fetch/CAS recheck for races and identities resolved only by the provider.

## Keep one observation owner

- When a healthy SSE/WebSocket already supplies the same progress, gate fallback polling. Preserve the existing disconnect, resume, terminal and cancellation latency; a slower interval is a product change, not a free optimization.
- Share an observer for the same scoped run. Stop it at terminal state or last unsubscribe. A CSS-hidden component remains mounted: check its fetches, workers and projections explicitly.
- A settled promise is not a freshness cache. Keep concurrent-flight dedupe separate from the snapshot/ETag/owner-generation store; purge private state on account change and logout.
- Coalesce high-frequency UI updates with a final flush on semantic transitions and unmount. Do not omit current facts merely to stabilize a signature.
- Bound temporary buffers while reading, not after buffering the full response. Release object URLs and observers at their last consumer. Preserve active consumers and exact output bytes.

## Budget the observable operation

Choose a fixture for one item, the actual visible list, ten times that list, rapid switches and concurrent sessions. Count requests, SQL, selected rows/columns, provider bytes, payload bytes, repeated builds or retained resources as appropriate. Preserve the public result and failure state.

A lower operation count does not justify a material time or memory regression. Measure the same increasing-size fixture before accepting a wider projection or batch. If the existing public owner cannot supply a narrow batch, give the parent a minimal prerequisite and serialize its ownership; do not add a second query owner or bypass private methods. Keep each group's original date intersection, freshness and retry semantics when sharing inputs.

For a slice budget, assert exact work at its named owner and report whole-operation totals separately. A whole-flow SQL total includes other owners: a valid downstream read removal must not invalidate an unrelated slice. Keep strict result, transaction and reversion assertions; do not replace exact budgets with permissive ranges.

Count selected rows and columns at the real driver fetch or stream boundary. A private helper returning a mapping can make its length mean symbols rather than rows. Retarget the measurement with exact result/reversion keepers; do not retain a production wrapper or counter solely to preserve a benchmark seam.

Use the smallest proof that fails when the repeated work returns. A counting request/repository boundary is valid for an operation budget; it does not prove production latency. Keep baseline and treatment on the same input and environment. Report timing/bytes as unmeasured until captured. Do not trade full history, undo, statistical evidence, unacknowledged work or freshness for a count reduction.

A stream's connection or global receipt time does not prove the selected record is fresh. Before suppressing fallback work, test an old selected-symbol payload while another symbol advances feed liveness. Require receipt or version evidence for the same identity; unknown age retains the normal fallback and honest stale state.

## Delete with a survivor

Before deleting a workflow node, trace edge outputs into the next handler's actual input. Unused node metadata does not make its upstream producer dead. Replay the same graph fixture at the consumer boundary and preserve its exact input.

Check routing before optimizing a page body. A permanent redirect can shadow a live-looking file. Enumerate every deleted module and its tests, prove the redirect/destination or public keeper, then remove both together. Do not delete an API or shared helper just because one UI caller disappeared.

Deduplicate removal estimates by exact file/range. Report production and test LOC separately. Gross removable current lines are not net savings when replacement code is needed. Full owner/file size is not a deletion estimate. Historical migrations, deployed data and public crate APIs require their own compatibility evidence.
