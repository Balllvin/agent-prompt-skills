---
name: ui-ux
description: Use for product screens, navigation, settings, motion, UI states, copy, messages and notifications, landings, visual assets, documents, and rendered UI verification. Dense data apps (tables, finance, research) especially.
---

# UI and UX

Make the app a clear, comfortable tool for research and decisions. Lead with the user's evidence or task. Give chrome less attention.

## Authority and context

- Follow `AGENTS.md` for workflow, contracts, validation, and file-size gates.
- Read the app's UI architecture doc, if any for tokens, navigation, and platform behavior.
- Read `CRAFT.md` for interaction values. App architecture docs own explicit platform exceptions.
- Read `references/writing.md` for prose and `references/design.md` for landings, brand, and media.
- Explicit user direction wins over style defaults. Filters prevent careless defaults; they do not prescribe a terminal aesthetic.
- Keep app-specific rules in the architect. Record concrete user feedback there, newest first.

## Start with the page's job

Before editing, name the app, the object, the user's next decision, and the evidence needed for that decision.

Example: "Portfolio. Show holdings and today's change so the person can choose what to inspect."

1. Inventory every reachable route, tab, sheet, menu, and settings panel in scope.
2. Trace the real data and actions before changing their presentation.
3. Inspect loading, populated, empty, failed, stale, partial, and unauthorized states.
4. Find the shared owner before fixing the same defect on several pages.
5. Render the current screen. Diagnose it before adding styling.

For a large browse table (a watchlist, inbox, or catalog):
1. Make list selection, view selection, filtering, and the virtualized table the initial screen. Mount research or ranking work when the person opens that workflow.
2. Compare paint rows with the selected list's total from that same response. Keep a partial preview visible while one scoped read loads the complete table, and expose loading or failure beside it.
3. Keep the table in a `flex min-h-0 min-w-0` chain to the viewport. Give columns minimum readable widths and flex growth so short presets fill wide screens while narrow screens scroll inside the grid.
4. Check a list of several hundred rows, a 30-row preview, a list whose count grows or shrinks during switching, a pending switch, and a failed refresh. Assert complete settled row identity, zero automatic research/ranking requests, and preservation of only the selected list's last-good rows. Inspect grid bounds and keyboard sorting at 1440x900 and 390x844.

## Data first

- Put the useful value, document, result, conversation, or next action in the first viewport.
- Keep page titles small and subordinate. Omit a visible title when navigation, columns, or the object already identify the content.
- Keep accessible names and document structure when deleting visible headings.
- Name units, periods, currency, provenance, and freshness where they change interpretation.
- Use tabular figures for comparable numbers. Reserve monospace for code, identifiers, and compact numeric columns.
- Use readable sans-serif text for names, explanations, settings, navigation, and actions.
- Keep missing values as `--`. Never substitute zero, sample data, or a neutral verdict for unavailable evidence. Hide a metric group when every value in it is missing.
- Say each label once per row. Never print a raw enum and its humanized copy together, or repeat one label down many rows; group identical rows with a count.
- Separate what the user owns from ideas and watchlists, and name each section in plain words.
- Apply gain/loss color to the displayed rounded value. A displayed zero is neutral.
- Put controls beside the data they change. A detail pane adds evidence the adjacent table does not already show.
- Keep dense tables useful on desktop. On phones, prioritize essential columns and contain horizontal scrolling inside the table.

## App comfort and visual craft

- Reuse each app's tokens, typography, controls, skeletons, and formatters.
- Build hierarchy with spacing, readable type, alignment, and selective emphasis.
- Keep one canvas. Use dividers only where they clarify groups, rows, or pane boundaries.
- Fewer layers, never ambiguous controls. Removing plates and lines must not remove affordance: every button keeps a border or fill, a hover state, and a focus state, so it never reads as plain text.
- Prefer black, white, and neutral gray. Primary data such as identifiers and names uses the normal text color, never an accent or off-gray tint.
- Use quiet rounded controls and native grouping where they improve recognition and touch comfort.
- Keep numeric grids precise. Do not make every screen a square terminal or a grid of decorative cards.
- Use cards for separate objects or contained interactions. Avoid cards inside cards and duplicate surrounding plates.
- Keep radii consistent by role. Nested visible corners follow outer radius = inner radius + inset.
- Use the app's existing overlay fill and shadow to distinguish menus and sheets from content.
- Keep semantic color meaningful. Do not introduce a new palette, font, or component library for polish alone.
- Keep body and secondary text at WCAG AA contrast. Small text needs more care than large values.
- Show hover, pressed, selected, disabled, and keyboard focus as distinct states.
- Gate hover effects to `hover: hover` and `pointer: fine`. Touch must not depend on hover.
- Use at least 44px touch targets and 16px phone text inputs. Respect zoom, safe areas, and the software keyboard.
- Preserve user text selection. Apply `touch-action: manipulation` to tap controls, not gesture canvases or scroll containers.

## Flows and settings

- Show the common path first. Put advanced inspection one level deeper.
- One object per page. Switch objects from one compact header dropdown, never a stacked list of every object as page chrome.
- Split a crowded page into a few plainly named views with an obvious switcher instead of one long scroll.
- Never put an always-visible text input beside every row. Use an explicit button such as "Add note" that reveals the input.
- Use one primary action per task. Remove duplicate controls and unnecessary steps.
- Autosave ordinary edits quietly. Keep drafts after failure and preserve both versions on conflict.
- Scope busy and failed state to the item it belongs to. One row's request or one bad item must not freeze or fail the whole list or panel.
- Keep a confirmed snapshot for optimistic updates. Roll back or reconcile failed writes visibly.
- Confirm destructive or irreversible actions. Give reversible actions direct manipulation or undo.
- Keep settings names, groups, defaults, and persisted meaning aligned across clients using the same account.
- Explain device-only settings at the relevant control. Do not offer inert substitutes for keychain, updates, or folder access.
- Keep deep links, selected navigation, tabs, and route state consistent.
- Give icon controls accessible names. Keep primary and recovery actions reachable by keyboard and touch.
- Menus use the app's existing popover owner (for example Floating UI) on web and the system menu on native.
- Check Esc, outside click, focus return, viewport edges, and submenu travel.

## Honest state and perceived speed

- Skeleton only the first blocking load. Match the geometry of the loaded content.
- Keep populated content visible during refresh. Mark the affected region busy and show a short refresh status.
- Show empty copy only after a successful settled read.
- Put failure and Retry beside the affected content. Never describe failure as absence.
- Show routine cache age quietly. A timestamp is not a failed request. Reserve warning and Retry for a completed failure; keep partial-data facts local and unresolved write errors visible.
- Clear busy state after failed streams. Preserve the prompt and saved trail.
- Hold private chrome behind a confirmed session. Unavailable auth shows recovery; confirmed sign-out goes to login.
- First paint uses bounded reads. Defer hidden tabs and expensive secondary requests.
- Check unbounded lists, request waterfalls, oversized payloads, and unstable live renders on hot routes.
- Keep chart geometry stable across loading, failure, and range changes.
- Do not swallow errors or announce success before a write is confirmed.

For screen switches, hidden panels, live progress or imports, read [reuse and work budgets](../build/references/reuse-and-budgets.md). Verify first paint, focus, interval, unmount, next-hop reuse and ten rapid switches. CSS hiding does not stop effects; a healthy stream must gate equivalent fallback polling without weakening recovery.

## Motion with a purpose

Use motion to explain a press, open a temporary layer, connect related states, or prevent a jarring change.

- Give frequent actions immediate feedback. Keyboard shortcuts and data commits must never wait for motion.
- Use the durations, easing, and scale values in `CRAFT.md`.
- Use interruptible CSS transitions for toggles and presses. Use native platform transitions in native apps.
- Animate exact properties, usually transform and opacity. Never use `transition: all`.
- Anchor menus to their trigger and keep dialogs centered. Scale only small press controls.
- Keep live data (prices, counters) immediately legible. Do not stagger values or animate every page title.
- Add modest motion to occasional sheets, menus, and meaningful state changes. Do not treat all animation as decoration.
- Honor reduced motion at the same selector specificity. Remove movement; retain static feedback and brief fades when useful.
- Stop persistent decorative loops. Never disable input until an animation finishes.
- Do not add pointer-tracking state, scroll hijacking, ambient motion, or a new animation dependency for simple polish.

## Web and native parity, chat surfaces

- Match web and native capabilities, labels, persisted settings, state handling, and recovery for shared jobs.
- Adapt layout and controls to the platform. Folder access, keychain, and auto-update remain device capabilities.
- Keep one floating oval composer. Context chips share its overlay without a surrounding footer plate or divider.
- Show the reply directly. Keep traces and sources in message overflow; keep artifacts and run cards in the reply.
- Traces open a viewport-contained overlay on web and native inspection in native apps. Show full reasoning, named tools, and child receipts.
- Render stored content as readable documents, including tables, lists, quotes, code, and links.
- Preserve source content and drafts when changing presentation. Failed, processing, empty, and stale sources remain distinct.
- Test one source of each supported kind, including failed imports and long table content.

## Precise words

- Read `references/writing/unslop.md`. Keep that source catalog unchanged.
- Use sentence case and short concrete verbs. Explain the failure and the next useful action.
- Delete repeated titles, route descriptions, marketing claims, and internal implementation jargon.
- Do not remove necessary units, permission consequences, financial risk, or recovery instructions to shorten copy.
- Use no decorative emojis, em dashes, or en dashes in new product copy.
- Fix poor AI-written content in its producing prompt. Lead with the answer and cite evidence inline.

## Verify and critique

1. Run the app and inspect the rendered change before calling it done.
2. Check responsive web changes at 390x844 and 1440x900; use supported window sizes for Native. Include states affected by the change.
3. Stress with long names, long URLs, large counts, missing values, narrow screens, zoom, and awkward tables.
4. Drive real keyboard and touch paths. Check focus, names, contrast, dialogs, scrolling, and reduced motion.
5. Reproduce bugs before fixing them. Keep behavior tests that fail when the fix is reverted.
6. Render Native views offscreen with test data. Do not inspect the owner's running app or credentials.
7. For a changed shared job or setting, check its web and native contracts. Record intentional platform differences explicitly.
8. Iterate with focused checks, then run the affected final gate required by `AGENTS.md`.
9. Give a fresh critic the integrated diff. The parent reviews every finding and owns the final decision.
10. Record route coverage, screenshot paths, commands, failures, and unavailable checks. A source audit does not prove a rendered screen.

Report polish findings as `Severity | Location | Before | After | Why`. Block on broken interactions, misleading data, inaccessible recovery, or lost drafts.

## References


Files over 600 lines are catalogs: search them for the section you need.

| Reference | Read when |
| --- | --- |
| `CRAFT.md` | Reviewing nested surfaces, icons, press/hover, or motion values. |
| `MESSAGES.md` | Writing messages or question cards to the person. |
| `references/writing.md` | Any prose: full Unslop, technical writing, reader test, PR bodies, document formats. |
| `references/writing/unslop.md` | The source Unslop catalog. Tests read it; keep it byte-identical. |
| `references/writing/technical-writing.md` | Docs, RFCs, READMEs: Diataxis modes, style, review checklist. |
| `references/writing/pdf.md` | Creating, editing, and rendering PDFs. |
| `references/design.md` | Any landing, brand, image, or video work; routes to everything under `references/design/`. |
| `references/design/taste-skill.md` | Landing, portfolio, or redesign taste: dials, AI tells, pre-flight. |
| `references/design/high-end-visual-design.md`, `gpt-taste.md`, `industrial-brutalist-ui.md`, `stitch-design-taste.md`, `ui-ux-pro-max.md` | Style catalogs for a specific landing brief (restrained, premium, GSAP editorial, brutalist, Stitch `DESIGN.md`, palette and font catalog). |
| `references/design/image-taste-frontend.md`, `image-taste-art-direction.md`, `imagegen-frontend-web.md`, `imagegen-frontend-mobile.md` | Image-first comps before building web or mobile screens. |
| `references/design/imagegen/index.md` | Generating or editing images. Extras in `references/`: `cli`, `image-api`, `prompting`, `sample-prompts`, `codex-network`. |
| `references/design/brandkit.md` | Brand boards and logo systems as images. |
| `references/design/banner-design/index.md` | Banners. Extra: `references/design/banner-design/references/banner-sizes-and-styles.md`. |
| `references/design/design-kit/index.md` | Logos, CIP, icons, social photos, HTML slides. Extras in `references/`: `design-routing`, `logo-design`, `logo-style-guide`, `logo-color-psychology`, `logo-prompt-engineering`, `cip-design`, `cip-style-guide`, `cip-deliverable-guide`, `cip-prompt-engineering`, `icon-design`, `social-photos-design`, `banner-sizes-and-styles`, `slides`, `slides-create`, `slides-strategies`, `slides-layout-patterns`, `slides-copywriting-formulas`, `slides-html-template`. |
| `references/design/design-system/index.md` | Brand token architecture. Extras in `references/`: `token-architecture`, `primitive-tokens`, `semantic-tokens`, `component-tokens`, `component-specs`, `states-and-variants`, `tailwind-integration`. |
| `references/design/hatch-pet/index.md` | Animated Codex pets. Extras in `references/`: `animation-rows`, `codex-pet-contract`, `qa-rubric`, `scripts/`, `LICENSE.txt`. |
| `references/playwright/index.md` | Driving a real browser. Extras in `references/`: `cli`, `workflows`. |
| `references/playwright-interactive.md` | Iterative UI debugging with a persistent browser or Electron session. |
| `references/webapp-testing.md` | Starting servers before a Playwright run and picking selectors. |
| `references/react-performance.md` | Hot routes, shared clients, lists that re-render on live data. |
| `references/screenshot.md` | The user asks for a desktop, window, or region screenshot. |
| `references/control-ui.md`, `control-cli.md` | Local harnesses for web/Electron UI or CLI/TUI checks. |
| `references/ui-styling/index.md` | shadcn/ui and Tailwind. Extras in `references/`: `shadcn-components`, `shadcn-theming`, `shadcn-accessibility`, `tailwind-utilities`, `tailwind-responsive`, `tailwind-customization`, `canvas-design-system`. App tokens win. |
| `references/redesign-existing-projects.md` | Auditing an existing surface before a redesign; use its audit, not its premium styling. |
