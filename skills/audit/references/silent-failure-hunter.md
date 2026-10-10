---
name: silent-failure-hunter
description: Find errors that the app swallows, hides, or reports as success, and fix them so users see an honest state and the logs show what failed. Use on any diff or audit that touches error handling, catch blocks, fallbacks, retries, caches, background tasks, or empty, loading, stale, and failed UI states, and before calling such work done.
---

# Silent failure hunter

A failure the user cannot see and the logs cannot explain is a bug, even when nothing crashes. Hunt those, then fix them at the owner.

## What counts as silent

- **Swallowed:** `except Exception: pass`, `contextlib.suppress(Exception)`, JS `.catch(() => {})`, empty `catch {}`, Swift `try?` on a user path, Rust `.ok()` or `unwrap_or_default()` on I/O that matters.
- **Failure sold as success:** returning `[]`, `None`, `0.0`, or `{"ok": true}` when a provider failed. A 429 cached as empty price history. A background write reported as recorded when it was skipped.
- **Failure sold as a different failure:** a catch-all that turns a runner crash into "Could not update the automation", a 401 shown as "Try again" forever, a failed load shown as "No runs yet".
- **Lost:** `asyncio.create_task` whose exception nobody reads, a Swift `Task {}` whose error is dropped, a cleanup error that replaces the original error.
- **Mislabelled:** a real failure logged at `info`, an expected skip logged at `error`, an error state rendered with `role="status"`.
- **Unbounded:** a retry loop or cooldown with no cap that turns one bad response into an outage (for example trusting any `Retry-After`).

## Rules the fix must meet

- Backend logs go through one structured logging config (for example structlog). Put ids on the event as fields: `request_id`, `run_id`, `job`, `tool`, `user_id` when safe, and a `failure_class`. Log at start, decision, failure, and done.
- `error` means a real failure. An expected skip is `warning` or `info`.
- Catch and continue only with a bounded `warning` that names what was skipped and why it is safe.
- Third-party provider error text goes through a sanitizer before logging or display (it can echo keys or URLs with keys). Never log secrets, tokens, cookies, auth headers, or request bodies.
- Browser proxies log `<app>_api_proxy_failed` with `failure_class`, method, redacted path, and the backend `X-Request-Id`.
- UI keeps loading, empty, stale, degraded, and failed as distinct states. Failed has a retry when a retry can work, and uses `role="alert"`.
- A fallback is explicit (`stale`, `degraded`, `offline-cache`, `reconnecting`) and visible, never a quiet substitute the user mistakes for live data.

## Process

1. List every error path in scope: try/except, catch, `try?`, `.ok()`, `?.` that skips work, default values on failure, retries, background tasks, fallbacks.
2. For each, ask: what exceptions can reach it, including ones the author did not expect? What does the user see? What does the log say, with which ids? Would someone debugging from production logs in six months find it?
3. Narrow the catch to the expected errors. Let the rest propagate to a handler that logs and shows an honest state.
4. Check the tests: a test must drive the failure and assert the visible state and the log event. A test that only covers the happy path does not prove the handler.

## Output

One entry per finding, ranked by user impact:

```
<severity: critical | high | medium> file:line
Swallows: what fails and what hides it
User sees: the wrong state, or nothing
Logs: what the production logs show today
Fix: the narrowed handler, the state, and the log event with its fields
```

Critical: data loss, a wrong number shown as right, a security check that fails open, or a user path that fails with no state and no log. High: a misleading message or an unjustified fallback. Medium: missing ids or wrong level.

In a diff review, report only lines the diff adds or changes, plus old handlers the diff now depends on.
