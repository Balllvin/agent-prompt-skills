---
name: performance-profiler
description: Find what makes an app slow or expensive, prove it with code and production evidence, and turn it into ranked fixes with a number to verify. Use when a screen, route, job, or deploy is slow, when hosting or metered-API cost rises, when asked "why is this slow", "profile this", "cut cost", or when reviewing a PR that touches a hot path. Works with or without running the app.
---

# Performance profiler

Find the cost, prove it, rank it, and name the number that shows the fix worked. `/radical-simplification` ("Fast by design") owns the design rules; this skill owns the hunt.

## Evidence ladder

Use the strongest evidence you can reach. Label every finding with the rung it stands on.

1. **Measured in production.** Hosting logs and metrics, read-only:
   - Logs: for example on Railway `railway logs --service backend --environment production --since 24h --filter "<event>"`. Structured events should carry `duration_ms`, `job`, `run_id`, `request_id` as fields.
   - Metrics and HTTP: the platform's metrics (CPU, memory, request latency). Report p50/p95/p99, never averages of percentiles.
   - Metered APIs: the per-call bytes or units log and the provider's usage page. Know whether the provider bills calls, bytes, or tokens.
2. **Measured locally.** A focused benchmark or test: `time`, `python -X importtime -c "import app.main"`, a query-count fixture, `cargo bench`, a Playwright trace, `next build` bundle output.
3. **Read from code.** A hypothesis with a confidence level. Never write a number you did not measure; write the metric to capture instead.

A timing in this report is not evidence until its limiter is named. See [Explain the number](../../build/references/principle-explain-the-number.md) and [Benchmark checklist](../../build/references/benchmark-checklist.md).

## Classify first

Every cost is one of: trips (network round trips, provider calls), I/O wait (database, data providers, LLM providers, messaging APIs), CPU, memory, bytes (payload, bundle, image), or build/deploy time. Name the class before the fix. I/O wait does not get faster in Rust. CPU and memory on a hot path might; say by how much and why.

## Where apps usually spend

Check these first. They are where slowness and cost usually come from.

- **Hot routes on first paint** (web, mobile web, desktop clients): provider fan-out before first paint, per-row enrichment, N+1 queries in loops, unbounded lists, 500 KB+ payloads. A single summary endpoint can quietly grow to hundreds of provider calls and thousands of queries per request; count them.
- **Background work in the web process:** scheduler jobs that loop over every user or ticker, pollers that wake on an empty queue, hydration that passes `force_refresh=True`, refresh jobs re-queued without a success interval or failure cooldown.
- **Provider bytes:** full-history calls where a tail fetch would do, a heavy aggregate endpoint where cached pieces exist, cache keys that include page size or date so every day misses.
- **Postgres:** time-window and ranking queries without a composite index that matches the sort, JSON payload rows that are rewritten whole, tables with no retention (job rows, cache rows, events).
- **Memory:** heavy imports at boot (pandas, scipy, matplotlib), worker count, in-process caches without a bound, Chromium launches without a global cap, a whole upload read twice.
- **Clients:** refetch on every focus plus a short poll, lists without windowing, whole-library imports (d3, chart libraries) for one chart, work in render.
- **Build and deploy:** every commit rebuilding every service (no watch patterns), native code rebuilt from scratch on any edit, a large image.

Use `rg` with a path under the app you inspect. Never walk the repo root.

## Benchmark a deployed page

Use a logged-in browser automation against production, one navigation per route. Desktop pages cannot be framed (`frame-ancestors`), so navigate the tab itself and read buffered Performance entries afterwards.

- Per route record: TTFB, every `/api/*` entry's duration, `decodedBodySize`, `encodedBodySize` and `responseStatus`, the time `<main>` stops changing, and error text in `<main>` ("unavailable", "failed", "missing").
- Strip query values before returning results; the extension blocks output that carries query strings.
- Wait one second after navigation for routes that redirect, or the evaluation dies mid-navigation.
- Time clicks the same way: click, then wait for network and `<main>` to settle. Skip anything that starts a paid or side-effecting job (AI runs, sends, orders).
- Read these first, they were real: `encodedBodySize == decodedBodySize` on JSON (proxy not compressing), the same shell call on every page or twice on one page, a 5xx followed by an identical retry, one request per grid row, and a page whose data call is fast but whose text says "unavailable".
- Then join to the hosting logs (for example `railway logs --service backend --since 1h`) for scheduler `max_instances` skips, the route's 5xx with no app event (a silent failure), and job events that stop appearing after a deploy.

## Output per finding

```
<rank>. <title> — <class>, <evidence rung>
   Where: file:line (route, job, or component)
   Evidence: the log line, metric, benchmark, or code path
   Cost today: number with unit, or "unmeasured"
   Fix: the change, smallest first (delete > reuse > native > new code)
   Expected: number with unit and confidence
   Verify: the metric or test that proves it, and where to read it
```

Rank by user-visible latency and money saved, then by confidence. End with the slices: title, files it owns, done-when with a number, tier.

## Rules

- Tie every finding to a file and line.
- A fix that hides a failure is not a speed-up. Stale, degraded, and failed stay visible (`/silent-failure-hunter`).
- Leave a regression test with the fix: a query or request count, a deadline, a payload cap, an import check.
- Run the repo's performance-contract or route-drift checks, if it has them, when a hot route or shared client moves.
- Hosting access is read-only in an audit. Never change variables, redeploy, or restart.
