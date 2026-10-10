# Efficient systems: the data-systems doctrine

Reference for `/radical-simplification` ("Fast by design"). Load it when you build or review a hot route, read model, queue, stream, cache, or first-paint path. The laws and the latency order live in `../index.md` and the build hub `SKILL.md`; this file holds the reasoning and the patterns behind them.

Theory: Martin Kleppmann, *Designing Data-Intensive Applications* (DDIA). Worked example: a mobile web app speed overhaul (read models, one client store, deleted bootstrap path). Method: `/ponytail`, `/performance-profiler`, `/silent-failure-hunter`, `/thermos`.

## Data-Systems Doctrine (DDIA applied to a web app)

### Know your load parameters, then choose where the work runs (ch. 1)

Describe load with the few numbers that actually drive cost: requests per
second per route, read/write ratio, rows per screen, symbols per user, fan-out
per event. Kleppmann's Twitter example is the canonical trade: home-timeline
reads outnumbered tweet writes by two orders of magnitude, so Twitter moved
the join to write time — fan out each tweet into per-follower timeline caches
— and accepted expensive writes to make reads cheap. Snapshot hydration
workers in a market-data app are the same decision: market reads dominate provider
writes, so workers assemble read models ahead of time and requests only read.
The corollary also transfers: extreme hot keys (celebrity accounts; in a
market app, index-level symbols every user watches) may deserve a hybrid path rather than
forcing one strategy everywhere.

### Measure percentiles, not averages (ch. 1)

The mean tells you nothing about how many users experienced a delay; use p50,
p95, p99. High percentiles matter disproportionately because the slowest
requests often belong to the heaviest users, and because of **tail latency
amplification**: when one page issues many backend calls, the chance that a
user waits on at least one slow call rises with every call — a screen that
fans out to 10 endpoints at p99 makes roughly one in ten page loads slow.
Queueing delay dominates high percentiles (head-of-line blocking), which is
why bounded concurrency and per-section deadlines beat raw speed. When
load-testing, keep sending requests independently of responses; waiting for
each response before sending the next artificially shortens observed queues.

### Separate systems of record from derived data (part III)

Every dataset is either the authoritative source of truth or derived from
one. In a typical web app, user, account, and document rows in PostgreSQL are
systems of record; snapshots, read models, provider caches, client stores, and search
mirrors are derived data — redundant, denormalized, and **rebuildable from
the source**. This distinction is what makes aggressive caching safe: losing
derived data may cost a rebuild, never truth. Two hard rules follow. First,
never let a derived store quietly become a source of truth (no user edits
into caches, no snapshot fields that exist nowhere else). Second, avoid dual
writes: an application writing the same fact to two stores in parallel will
eventually leave them disagreeing after a partial failure. Give each payload
scope one durable owner and derive the rest. Collapsing an offline cache and
a boot-time IndexedDB double-write into one store is this rule.

### Derived views trade write cost for read speed — justify the ratio (ch. 3)

Indexes, materialized views, and read models all speed reads by adding write
work and storage. Well-chosen ones are the single biggest lever on read-heavy
paths; speculative ones are pure write tax. Add them where a measured hot
read exists, and remove them when the read pattern goes away. Time-window and
ranking queries need composite indexes matched to the actual sort.

### Freshness classes set cache policy

Data is fresh when its age — measured from event time, not fetch time — is
within the tolerance where a decision based on it is still correct. That
tolerance is a product requirement per data type, not a technical constant,
and it directly determines what you can cache and for how long. The
controlling insight: **cacheability is the inverse of change rate, and
immutable data is infinitely cacheable.**

The freshness ladder for this domain:

| Data type | Required freshness | Cache policy |
|---|---|---|
| Live quotes, market open | Seconds (the 30/60/300s SLAs) | Do not cache — stream; HTTP fallback with soft-stale revalidation |
| Quotes, market closed | Static until next session | Cache until the session boundary, session-aware invalidation |
| Intraday bars | 30–60s | Short TTL plus single-flight |
| Completed daily OHLC | Immutable once the session closes | Cache indefinitely, version/content-keyed |
| News | Minutes, aged from publication time | Short TTL, event-time deadlines |
| Earnings calendar | Hours–days | Long TTL; reconcile priority names per-symbol |
| Fundamentals/filings | Quarterly change | Days–weeks; invalidate on filing events |
| Company profile | Rarely changes | Weeks |
| User holdings/watchlist | Read-your-writes — correctness, not TTL | Cache freely, invalidate synchronously in the mutation path |
| Auth/session | Correctness-bound | Never trade for speed |

Three rules follow. Age everything from provider/event timestamps — a stale
row fetched one second ago is still stale (the quote-frame liveness rule).
Every cached read carries freshness metadata and distinguishes
stale-but-usable (serve, revalidate in background) from stale-unusable (hard
expiry, honest degraded state). And hunt for hidden immutability: "closed
sessions never change" is the single biggest cache lever in a market-data
app.

### Expect staleness anomalies and pick guarantees deliberately (ch. 5)

Any system with asynchronous copies — replicas, caches, client snapshot
stores, service workers — has replication lag, and "eventually consistent"
hides specific user-visible anomalies. The two worth engineering for here:
**read-your-writes** (after a user mutates data, their next read must reflect
it — invalidate or overwrite the client/cache copy in the mutation path, do
not wait for the next hydration cycle) and **monotonic reads** (a user must
not see data move backwards in time — version snapshots and refuse to render
an older generation over a newer one). Also make "eventual" quantifiable:
freshness metadata on every derived read, and staleness monitoring instead of
hoping.

### Let PostgreSQL enforce the invariants (ch. 7)

Application-level read-then-write checks race under concurrency; the database
already ships the tools that do not. Unique constraints as the final
publication invariant, `ON CONFLICT` upserts for idempotent writes,
compare-and-set `UPDATE ... WHERE` for state transitions, and transactions
that commit related changes atomically (invalidation + enqueue in one
transaction, never separately). Recover races through the constraint rather
than preventing them with app locks.

### Distrust clocks, leases, and your own liveness (ch. 8)

In a distributed system the only failure detector is a timeout, a paused
process does not know it was paused, and clocks skew. A worker that claimed a
job can lose its lease during a GC pause or slow provider call and then wake
up still believing it owns the resource. The defense is a **fencing token**:
a monotonically increasing token issued with each lease, checked at the write
boundary, so a zombie's stale-token write is rejected no matter what the
zombie believes. A lease-token compare-and-set on a hydration queue is exactly
this: every worker-owned writer verifies the claimed token immediately
before the publication commit. Never decide ordering or expiry by comparing
wall-clock timestamps from different machines; last-write-wins by timestamp
silently drops writes under clock skew.

### Idempotence is end-to-end, or it is not there (ch. 8, 12)

A lost response is indistinguishable from a lost request, so every retry can
duplicate its effect unless the operation is idempotent. Transport-level
dedup (TCP, one queue hop) does not survive the whole path — the end-to-end
argument says dedup must be owned by the endpoints. Practically: the client
mints one operation id per logical action and the terminal write upserts on
it. Activity beacons are the pattern: one client `visit_id` per
landing, bare beacon immediately, enrichment later under the same id, backend
upsert on `(user_id, visit_id)` so cross-worker races cannot duplicate rows.
Any new retryable mutation gets the same treatment before it gets a retry.

### Streams: liveness comes from events, ordering comes from the log (ch. 11)

Event time and processing time are different clocks; conflating them
fabricates data. A quote's age comes from its provider timestamp, not from
when our process handled it — which is why feed liveness is owned only by
quote frames, never heartbeats or side-channel messages, and why stale cache
rows must not be relabeled as live ticks. Consumers of ordered change streams
must be idempotent, because redelivery after a crash is the normal recovery
path, not an edge case. And partition consumption is per-consumer state:
track what each client was actually delivered, not what the system globally
knows (the WebSocket snapshot-cache scoping lesson).

### Hot spots do not average out (ch. 6)

Load skew concentrates: a handful of symbols, one user's giant portfolio, one
route. Hashing and pooling spread average load but cannot fix a single hot
key — that needs its own treatment: single-flight loaders so N concurrent
callers share one request, per-scope caches with latest-per-scope reads, or a
dedicated precomputed path for the few keys everyone reads. Scatter/gather
across many partitions or providers is tail-latency amplification by
construction; bound the fanout and degrade per-section.

## Design Workflow

### 1. Trace before you touch (/ponytail)

Read the real flow end to end — screen hook, client, proxy, route, service,
provider, worker — before choosing a fix. The lazy fix is the root-cause fix:
one guard in the shared function beats a patch in every caller. Then climb the
ladder: delete the work, reuse an existing read model or helper, use a native
mechanism (DB constraint, ETag, `Retry-After`), and only then write new code.

Most "slow" reports are architectural, not micro: work running on the wrong
side of the request boundary, unbounded scope, or serialized independence.
Check those three before profiling loops.

### 2. Locate the cost (/performance-profiler)

When runtime profiling is unavailable, inspect code paths and state findings
as evidence-backed hypotheses with confidence levels — never invent measured
numbers. Priority surfaces and smells:

- **Backend:** N+1 queries in loops, missing pagination, synchronous provider
  fanout in handlers, refresh work awaited on read paths, over-serialization,
  missing composite indexes for time-window or ranking queries.
- **Frontend:** unwindowed lists, expensive render-path computation, unstable
  props causing broad rerenders, markdown-heavy pages, large blobs in state,
  eager prefetch of the whole app, duplicate durable stores for one payload.
- **Payloads:** base64 fields in list endpoints, nested objects where
  summaries suffice, duplicated per-item metadata. Prefer summary/detail
  splits and strict pagination.

### 3. Fix the shape, then the constants

Prefer changes that alter the workload shape over constant-factor tuning:
maps/sets over repeated linear lookups, bulk fetches over N+1 loops,
precomputed read models over request-time assembly, single-flight loaders so
concurrent callers share one request, memoized derived data over per-render
recomputation. Before any rewrite, confirm the safety checklist: data sizes
justify the change; output ordering, identity, and mutability are preserved;
caches have an invalidation story; batching preserves tenant, permission,
soft-delete, pagination, and sorting constraints.

### 4. Keep failures loud (/silent-failure-hunter)

Efficiency work creates new places to swallow errors — caches, fallbacks,
background tasks, retries. Audit every one:

- Fallbacks must be explicit states (`stale`, `degraded`, `offline-cache`,
  `reconnecting`), not silent substitutions the user mistakes for live data.
- Background and best-effort writes return an explicit committed/skipped
  result; wrappers must not log success because the helper merely returned.
- Telemetry batches are retained until a fetch succeeds or `sendBeacon`
  accepts them; dropping outage evidence to save a request destroys the only
  record of the outage.
- Catch blocks stay narrow. A broad `except` around a provider call will
  eventually hide the bug that made the path slow in the first place.

### 5. Hold the structural bar (/thermos)

A fast path that scatters special cases is a regression. Speed changes obey
the same gates as everything else: no file grown past 500 lines, no one-off
booleans threaded through unrelated flows, no second durable store for a
payload that already has one, no bespoke cache class where a read model or
single-flight helper already exists. Look for the code-judo move: the biggest speedups often come from
*deleting* a heavyweight bootstrap path, not optimizing it.

## Canonical Patterns

**Read-model serving.** Worker-owned PostgreSQL snapshots with source
versioning and freshness metadata; request paths read latest-per-scope, mask
incomplete aggregates, and show queued `503 + Retry-After` as loading, never
as failure. Missing values stay nullable — never coerce an unavailable price
to `0.0`. This is DDIA's derived-data architecture: the snapshot is
rebuildable, versioned, and never the source of truth.

**Durable queues.** Lease-token compare-and-set claims (fencing tokens),
stale-job reclaim from `started_at`, bounded worker pools with isolated
sessions, database uniqueness as the final publication invariant, and
invalidation + enqueue in one transaction. Snapshot ORM rows to immutable
scalars before any provider await that can expire the session
(`MissingGreenlet` prevention).

**Hot-route deadlines.** Per-section timeouts inside aggregate routes so one
hung provider degrades one tile; proxy deadlines strictly inside client
deadlines; the hot-path set tracks the real first-paint owner whenever routes
move.

**Live data honesty.** Liveness is owned only by real data frames (quote
ticks, not heartbeats or side-channel messages) and aged from event time;
strict reads for streaming so provider failures surface as stale/reconnect;
live overlays applied before sorting, ranking, and derived math so every
visible value describes the same tick; conversions skipped (durable snapshot
retained) when the FX rate is a sentinel or unknown.

**Bounded first render.** Small recent windows with explicit older-history
pagination; progressive settle (render the ready section, let optional
sections stream in); lazy-mount panels and sheets on open; no bulk route
prefetch; one durable client store per payload scope (no dual writes).

**Caps enforced upstream.** Request limits applied before backend enrichment
and provider fanout, not after client render; the visible scope passed into
mutation and tracking routes so hidden rows cost nothing.

**Background work off the response.** Side effects (activity records, agent
context, telemetry persistence) run behind the response via background tasks,
with end-to-end idempotence: a client-minted operation id and an
`ON CONFLICT` upsert so cross-worker races and retries cannot duplicate rows.

## Verification Contract

Every efficiency change lands with the regression that would catch its
reversal. Match the test to the mechanism:

- Route budgets: assert the response completes without awaiting broad refresh
  or per-row quote enrichment (seed sparse rows, block the refresh, count
  provider calls).
- Deadlines: include a never-finishing provider coroutine and assert partial
  data returns quickly with only that section degraded.
- Caps: assert both the request limit and the visible disclosure.
- Concurrency: prove priority start order, slow-first progress, and sibling
  success after one claim fails.
- Fencing: naturally expire a worker's lease mid-flight and prove the zombie
  cannot publish or terminalize.
- Idempotence: replay the same operation id concurrently and out of order and
  prove one row.
- Liveness: prove a non-quote message cannot flip stale→live, and a stale
  cache row is never projected as a live tick.
- Render scope: assert the initial message/row limit; record DOM and request
  counts in browser profiles when the change targets first paint.

Run the repo's performance-contract checks, if any, when touching hot
frontend routes or shared API clients. When runtime metrics become available,
capture API response times as percentiles (p50/p95/p99) by route — never
averages, and never averages of percentiles — plus DB query counts per
endpoint, staleness/lag of derived reads, and frontend long tasks. Static
analysis findings stay hypotheses until measured.
