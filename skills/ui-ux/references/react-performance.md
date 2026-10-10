# React performance rules for app screens

Adapted from Vercel `react-best-practices` (vercel-labs/agent-skills, MIT per its frontmatter; see `../../THIRD_PARTY_NOTICES.md`). Rewritten and cut to the tiers that decide a fast first paint (set a bar, for example 800 ms). App architect files and `AGENTS.md` win on conflict.

Priority order. Fix a higher tier before touching a lower one.

| Tier | Concern | Why it ranks here |
| --- | --- | --- |
| 1 | Request waterfalls | Each sequential await adds a full round trip before paint. |
| 2 | Bundle size | Every KB parses on the phone before anything is interactive. |
| 3 | Server work | Slow loaders and fan-out block the shell. |
| 4 | Client fetching | Duplicate or unkeyed fetches refetch data we already hold. |
| 5 | Re-render scope | Wide state updates repaint whole tables on each tick. |
| 6 | Rendering cost | Long unwindowed lists and heavy markdown hydration. |

## Tier 1: no waterfalls

- Start independent requests together (`Promise.all`), then await. An `await` inside a loop over ids is a waterfall; batch the ids into one endpoint.
- Do not let a child component start its fetch only after the parent's fetch resolves. Hoist both to the route loader or a summary endpoint.
- Start a request before the `await` that does not need it. Await late, at the point the value is used.
- Wrap slow, non-critical panels in `Suspense` so the shell paints without them.
- Prefer one read-model endpoint over N provider calls from the browser (`AGENTS.md` Database).

## Tier 2: bundle size

- Import from the module path, not a barrel `index.ts` that drags the whole package in.
- `next/dynamic` or `React.lazy` for heavy, below-the-fold, or tab-hidden widgets (charts, editors, markdown renderers).
- Load analytics and third-party scripts after hydration.
- Preload on intent (hover or focus of the link) for the next likely route, not on mount for every route.
- Check the diff for a new dependency before adding one; the platform or an existing util usually covers it.

## Tier 5: re-render scope

- Keep high-frequency state (live quotes, stream tokens, cursor position) in the smallest component that shows it. Do not lift it to a page context that every row reads.
- Split contexts by update rate. A context that changes each tick re-renders every consumer.
- Derive values during render instead of mirroring props into state with an effect.
- Stable props for memoized rows: memoize callbacks and objects passed into long lists, and key rows by id, not index.
- Use `useTransition` or `useDeferredValue` for filters over large tables so typing stays responsive.

## Tier 6: rendering

- Window lists past a few hundred rows.
- Render markdown once and cache the output; do not re-parse on each stream token.
- `content-visibility: auto` on long off-screen sections.

Report findings as `file:line  tier  rule  fix`, one per line. Do not claim a measured number you did not measure.
