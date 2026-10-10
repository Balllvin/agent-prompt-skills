---
name: fmp-integration
description: Use when adding or changing access to Financial Modeling Prep (FMP) or any similar byte- or call-billed market-data API in an app - HTTP calls, quote or price-history stores, statement, ratio, or key-metric caches, agent or CLI tools that read market data, field renames and endpoint migrations, market-data contract tests, cache TTLs or freshness, scheduled jobs that read market data for many users, worker counts on provider paths - or when provider usage, bandwidth, 429s, or over-limit errors show up. Triggers include /fmp-integration, "FMP", "Financial Modeling Prep", "market data", "quote cache", "price history".
---
# FMP integration

FMP bills bandwidth, so every avoidable fetch costs money, and provider cost must grow with distinct symbols, never with users, screens, or workers. Give each concern one owner, reuse cached rows, and keep failures honest. The same rules fit any metered market-data API.

## One owner per concern

| Concern | One owner |
|---|---|
| HTTP | One transport module with a shared client pool, the provider's rate limit, and an honest result type (`ok` / `empty` / `failed` with status). Callers use a **strict** getter (raise) or a **meta** getter (branch on `source_status`). |
| Live quotes | One quote store (cached per symbol, locked so concurrent readers make one request) |
| Daily bars | One durable price-history table |
| Agent tool catalog | One tool layer that reads the same caches as the screens |
| Statement, ratio, key-metric cache | One row per `(namespace, symbol, period)` at a canonical row count; readers slice |
| Stable vs legacy field names | One normalizer that adds legacy aliases |

Hard constraints:

- **No ad hoc HTTP clients.** No second pool, no second global budget. Import through the transport.
- **Apps are snapshot-first.** Screens paint from cached snapshots plus a websocket or bounded API, with freshness metadata. No browser calls to the provider. No on-request provider fetch for a screen that already paints.
- **Market data stays out of LLM system prompts.** Live quotes, calendars, and tool JSON go in user or tool turns, never `role=system`, so prompt caches keep hitting.
- **Durable cache in Postgres.** Do not use Redis or a document store as the system of record for provider data.
- **Cache writes only on success.** A timeout, 429, or 5xx is not an empty result. Missing OHLC is not `0.0`. A successful empty answer gets a short TTL, and a cache-only read of an empty row queues a refresh instead of painting a blank screen.
- **Page size is not cache identity.** Statements, ratios, and key metrics share one canonical row per `(symbol, period)`; `limit` never enters the key. Every app and worker reads that row and slices locally.
- **Background hydration never forces a refresh.** Only a user-visible stale read may queue one. Do not widen `limit`, symbol lists, or date windows past what the screen shows.
- **Unavailable is not clean.** A missing or failed measurement is never evidence of an empty or healthy result. Say the data is unavailable.
- **Stable renames get aliases.** When the provider renames a field, add the legacy alias in the normalizer; do not patch one screen's fallback key list.

## Scale rules

- **One fact, one row, for everyone.** Cache identity is `(provider, namespace, symbol, key_parts)`. Never put a user, portfolio, API key, page size, `limit`, `strict` flag, or a moving `to` date in `key_parts`. Check: two callers that differ only in those values write one row.
- **Prove a filter before you loop on it.** Before calling an endpoint once per entity (per holder, per position, per fund), confirm in the official docs that the filter parameter exists, then record one real response and check its row count and size. Providers often ignore unknown parameters and return the whole page. Match rows by their own id field (`cik`, `symbol`), never by "first row".
- **Jobs collect symbols first.** A scheduled job that walks users builds `symbol -> recipients`, fetches each symbol once through a cached owner, then fans results out. Share only symbol-level facts; anything computed from one user's position, settings, or entitlement runs per recipient. Check: N users holding one ticker make the same request count as one user, and two users with different share counts get their own numbers.
- **A closed market is not a cache miss.** A quote aged from its trade time is expired the moment it is written outside the session, so every read refetches. Gate on the exchange calendar before reading quotes in a job, and never re-apply the last session's change during closed hours.
- **Every data family has a freshness class.** Pick the class before the TTL (table below). A closed period (past bar, past quarter, past filing, past transcript) is immutable: no background job refetches it.
- **Agent paths read app caches first.** Agent and CLI tools get the same rows the screens read. A read-only public market-data tool result may be shared across users. Never cache an error result or anything user-scoped.
- **No self-imposed caps.** Do not add a fixed worker count, byte budget, or page cap. A limit is either the provider's real answer (a 429, its published per-minute rate) or measured at startup (CPU count, Postgres `max_connections`). Stay under the allowance by reusing data, not by pausing work.
- **Process memory is not shared state.** Single-flight locks, 429 cooldowns, rolling-minute counters, and byte meters that must hold across processes or restarts live in Postgres (advisory locks, a shared row). Share the provider's limit across processes; never divide it by a worker count.
- **Measure wire bytes per caller before you claim a saving.** Fewer app requests or smaller app JSON do not prove fewer provider bytes. Count real HTTP attempts and bytes at the transport, per caller label, before and after.
- **Read-path speed is Python (or your runtime) first.** For cached reads, remove generic encoders, ORM object construction, and per-client re-encoding (orjson, column tuples, encode once per message) before proposing another language or service.
- **A freshness or latency number is not a result** until you name the limiter and rule out another explanation with a run. See [Explain the number](../build/references/principle-explain-the-number.md).

### Freshness classes

| Class | Means | Fresh window | Who refreshes |
|---|---|---|---|
| `LIVE` | The number is the product while the market is open | about 30 s in session; last close when closed | On read, through the quote store |
| `INTRADAY` | Changes through the day; minutes are fine | 60 s to 15 min by resolution | On read |
| `DAILY` | Changes at most once a day | Until the next session close, at most 24 h | On read past the window; jobs only for demanded symbols |
| `EVENT` | Changes when something happens: earnings print, filing, release | 24 h by default, cut to the event | A known event for that symbol and period marks the row due |
| `IMMUTABLE` | A closed period | Long (for example 365 days) | Never by a background job; only explicit refresh or a correction |

A successful empty answer gets its own short window: at most 15 minutes for slow reference data, at most 60 seconds near a live event. A failure is never stored as empty.

Typical mapping: quotes `LIVE`; intraday bars `INTRADAY` (closed sessions `IMMUTABLE`); daily bars `DAILY` for the latest session, `IMMUTABLE` before; profile `DAILY`; statements, ratios, key metrics `EVENT` (closed fiscal periods `IMMUTABLE`); estimates `DAILY`; earnings calendar `DAILY`, `EVENT` on print day; transcripts `EVENT` dates and `IMMUTABLE` text; news `INTRADAY`; 13F holdings `EVENT` in the filing window, closed quarters `IMMUTABLE`.

### Cost model

Bytes per day ≈ F + b_s·S + b_u·U: fixed work, plus a per-symbol term over distinct symbols S, plus a per-user term over users U. Only the per-user term is a scaling bug. It almost always comes from a scheduled job that loops over users and calls an uncached getter inside the loop. Convert it with "jobs collect symbols first".

| Path | Upstream calls for N same-minute readers |
|---|---|
| Quote store with per-symbol lock and a Postgres advisory lock | 1 |
| Cached getter with an in-process lock | 1 per process |
| Uncached getter, raw HTTP, hosted MCP tool | N |

## Workflow

1. Search for existing owners first (`rg -n "quote|price_history|fmp|get_with_meta|get_strict" <backend>`). Search every live caller app, not retired folders or the repo root.
2. Trace the actual caller to its cache and transport, not only the named facade. A raw getter beside a cached getter does not inherit its cache. Route to the owner in the table above; do not add a parallel wrapper for the same upstream contract.
   - Assign each `(provider, namespace, symbol, key_parts)` one cache owner. Read the getter before using it as a cache loader.
   - Test ownership through the real getter and cache with a stub at the HTTP boundary. Exercise missing, expired, fresh, and failed-then-recovered rows. Assert one wire fetch per cold or expired identity, then zero on a fresh read. Run the same check through each route and snapshot builder that uses the fact.
3. Verify uncertain params, paths, shapes, and pagination against the current official docs (`site:site.financialmodelingprep.com/developer/docs ...`). Prefer primary docs over blog posts, stale repo notes, or memory. A code vs docs disagreement becomes a migration question plus a focused contract test.
4. Prefer stable endpoints when current and complete; keep legacy ones only as a documented fallback.
5. Decide failure semantics before coding:
   - **strict** when the data is primary to the surface (raise)
   - **meta** when the caller must branch on `source_status`
   - **optional/degraded** only for true enrichment; still thread `source_status` and never mint `[]` from a failed fetch
   - explicit partial success for batch and multi-entity payloads
6. Test the normalization and the failure path users will see.
7. Short quote rows: batch endpoints (forex, commodities, index lists) may return only `symbol, price, change, volume`. Derive previous close from what the row has (`previousClose = price - change`) before any backfill call. Curl the endpoint once and confirm which fields come back before trusting a field name.

Optional: keep a `references/endpoints.json` with one entry per endpoint you call (path, owner module, doc URL, stable or legacy, `last_verified`). A PR that touches an endpoint updates its date; a monthly pass re-checks entries older than 90 days.

## Verification checklist

- Cold, warm, and stale paths checked against [reuse and work budgets](../build/references/reuse-and-budgets.md); helper calls distinguished from wire bytes.
- No new ad hoc HTTP client, no second cache for an existing fact.
- Owner matches the table (transport, quote store, price history, tool layer).
- Official docs checked when behavior was uncertain.
- Primary vs optional failure semantics encoded; missing, empty, partial, stale, and malformed stay distinct.
- No fake zeros, fake empty arrays, or success-shaped failures; cache writes only on success.
- Cache identity excludes user, page size, `limit`, `strict`, and moving windows; a per-entity loop has a recorded response proving its filter works.
- Stable-renamed fields carry legacy aliases, verified by a normalizer test.
- Apps stay snapshot-first; no market data in LLM system prompts.
- Tests cover at least one real provider-shaped fixture and one failure or partial path.
- Jobs and agent tools fetch per distinct symbol; a test with several users on one ticker proves the request count.
- The family's freshness class is named in the PR, and closed periods are never refetched by a background job.
- Nothing that must hold across processes relies on process memory, and no new fixed cap was added.
