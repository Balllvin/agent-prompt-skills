# Server-then-Playwright test pattern

Adapted from Anthropic's `webapp-testing` skill (anthropics/skills, Apache-2.0; see `../../THIRD_PARTY_NOTICES.md`). Rewritten; no upstream code is copied.

## Start the servers, then drive

1. Start every server the flow needs: the backend (for example `uvicorn` on 8000), then each web app on its own port (for example 3000). Run them in the background.
2. Wait on each port before the first page load. Poll `http://localhost:<port>` until it answers or a fixed deadline passes, then fail with the server's last log lines. Never start Playwright against a port that is still compiling.
3. Use `localhost`, not `127.0.0.1`, for frontend dev servers when the app's cookie and CORS config use it (cookie and CORS origins are keyed to it).
4. Run the Playwright script.
5. Tear every server down in a `finally`, even on failure, so the next run does not find a stale process on the port.

## Recon, then act

A dynamic page is not ready at `load`. Before choosing selectors:

1. `page.goto(url)` then `page.wait_for_load_state("networkidle")`.
2. Take a screenshot or read the DOM or accessibility tree.
3. Pick selectors from what rendered: role and accessible name first, then text, then `data-testid`. Avoid CSS paths that break on a style change.
4. Act, then assert on the next visible state, not on a timeout.

Static HTML with no server can be opened with a `file://` URL instead.

## Defaults

- Sign in with a seeded test account from the project fixtures. Never a real account.
- Capture 390x844 and 1440x900 for loaded, empty, failed, and stale states.
- Stub API routes with `page.route` for empty, 500, and slow responses.
- Collect console errors and failed requests and fail the run on unexpected ones.
