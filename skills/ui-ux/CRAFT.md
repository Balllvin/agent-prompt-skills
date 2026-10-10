# Craft polish

Use with `SKILL.md` and the app architect. The architect owns app tokens and platform behavior. These values guide interaction; they do not require terminal chrome.

Adapted from Jakub Krehel's better-ui and Emil Kowalski's design-engineering guidance.

- https://www.skills.sh/jakubkrehel/skills/better-ui
- https://github.com/emilkowalski/skills

MIT. Copyright (c) 2026 Jakub Krehel. Copyright (c) 2026 Emil Kowalski.

## Shape and hierarchy

Use the app's existing radius scale by role. Keep reading and data areas calm. Use rounded controls and recognizable native groups when they improve comfort. A square panel is not a quality requirement.

Close nested corners follow outer radius = inner radius + inset. Prefer removing the extra shell when it adds no meaning. At more than 24px inset, treat the layers independently.

Align names, values, and actions across rows. Use optical alignment for asymmetric icons. Start icon-label padding 2px smaller on the icon side, then inspect it.

Match icons to adjacent text: 1.5px for regular and 2px for semibold. Use one glyph with `currentColor`, sized on 16, 20, or 24px grids. Flip direction-sensitive icons for RTL only.

## Motion decision

Name the feedback or state relationship the motion explains. Skip motion that delays frequent work or obscures data.

| Interaction | Default |
| --- | --- |
| Keyboard shortcut, ticker commit, live value | Immediate; never wait for a transition |
| Small control press | 100-160ms, scale around 0.97 |
| Hover or selected state | Immediate or 100-150ms color/opacity |
| Tooltip or small menu | 125-200ms, anchored at its trigger |
| Sheet or dialog | 200-280ms, clear entry and faster return |

Use `cubic-bezier(0.23, 1, 0.32, 1)` for entry. Move reversible layers along the same path. Keep dialogs centered and popovers anchored. Start scale near 0.97, never zero.

Use interruptible CSS transitions for presses and toggles. Native uses SwiftUI or AppKit behavior. Prefer transform and opacity for movement. Name exact properties; never `transition: all`. Do not animate layout dimensions for routine polish.

Do not scale data rows, navigation, tables, or reading content. Do not stagger financial values, charts, or evidence. Occasional menus and sheets can move modestly while content remains legible.

Keep subsequent toolbar tooltips immediate after the first one opens. Keep input available throughout transitions. Avoid mount-state flags and new dependencies when CSS expresses the behavior.

Honor reduced motion at the animated selector's specificity. Remove movement, overshoot, and loops. Keep a static state cue or brief fade. Theme changes must not trail through several color transitions.

Gate hover with `@media (hover: hover) and (pointer: fine)`. Disabled controls do not press or hover. Use at least 44px touch targets. Never hide the only action behind hover.

## Layers and depth

Use dividers where they clarify rows or panes. Use whitespace where it already explains grouping. Do not surround every module with a border.

Floating layers use the app's existing overlay fill and shadow. They must stay distinguishable from the page, including increased contrast settings. Keep charts and documents opaque.

Native system materials are platform behavior. Do not import decorative glass or build a second shadow system.

## Stress and inspect

Render long names, long URLs, large values, empty content, stale data, and failed requests. Check narrow screens and zoom. Slow an occasional transition to inspect its origin, interruption, and final state. Verify reduced motion separately.

A screenshot proves only the state shown. Record viewport, data state, route, and artifact path. Source inspection alone is not visual verification.

Report findings as `Severity | Location | Before | After | Why`. Block on broken interactions, misleading data, inaccessible recovery, or lost drafts. Name unverified states explicitly.
