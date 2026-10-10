# Hunt loop

Use this when a review is looking for a real hole, not when a scanner already named a dependency. It sits in front of the phase pipeline. It does not replace it.

Only on repositories you own or are authorized to test. Do not write or run an attack script. A failing test calls the production function.

## Loop

1. Start from an entry the caller controls. Trace it forward to the sink. A safe sibling does not clear another path.
2. Try to disprove the candidate. If a control you opened stops it, drop it. An unread helper is not a control.
3. Keep it only when the caller gains an outcome they did not already have.
4. The fix is a test that fails on the old behavior, then the smallest change at the boundary that already owns the decision.
5. A second reader checks the diff. The author's claim is not evidence.

## Do not

- Add a second skill, a scanner runtime, or a nightly job for this loop.
- Copy an outside scanner's scripts or phase files into this repo.
- Treat a scanner hit as a finding before the disprove step.
- Log a secret, token, cookie, or request body while tracing the path.
