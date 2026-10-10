---
name: deslop
description: Remove AI-generated code slop and clean up code style. Use when cleaning a branch diff, reviewing freshly generated code, or the user says deslop / remove slop / clean up AI code.
---

# Remove AI code slop

Check the diff against main and remove AI-generated slop introduced in the branch. Prefer the file's existing voice over a new house style.

This is a **filter**, not a rewrite mandate. Adaptive: keep intentional comments, guards, and structure the surrounding code already uses. If the user or another skill (ponytail, thermo-nuclear) asks for a deeper structural change, do that instead of cosmetic cleanup alone.

## Focus Areas

### Comments and narration
- Extra comments that restate the next line, narrate "what" instead of "why", or are inconsistent with local style
- Section banners (`// ===== Helpers =====`), emoji in comments, and changelog comments left in code
- Docstrings that duplicate the function name without adding contracts, units, or failure modes

### Defensive theater
- Defensive checks or try/catch blocks that are abnormal for trusted / already-validated code paths
- Catch-log-and-continue that swallows errors the caller should see (hand off real silence bugs to `silent-failure-hunter`)
- Null/empty guards that cannot fire given upstream types or invariants

### Types and indirection
- Casts to `any` / `as unknown as` used only to bypass type issues
- Thin wrappers, pass-through helpers, or single-implementation interfaces added "for clarity"
- Optional fields and silent fallbacks that paper over an unclear boundary

### Structure and style
- Deeply nested code that should be simplified with early returns
- Speculative abstractions, feature flags, or config for values that never change
- Verbose names that fight local conventions (`dataValueResult`, `handleClickEventHandler`)
- Import or formatting churn unrelated to the change
- Other patterns inconsistent with the file and surrounding codebase

### Tests and fixtures
- Tests that only assert mocks were called, with no behavior contract
- Fixtures full of `"John Doe"`, `"Acme"`, `99.99%`, or emoji unless the product surface truly needs them
- Snapshot or golden updates that bury accidental copy/UI slop instead of fixing the source

## Guardrails

- Keep behavior unchanged unless fixing a clear bug.
- Prefer minimal, focused edits over broad rewrites. Deletion over reformatting.
- Do not restyle unrelated files or "while I'm here" cleanup outside the diff.
- If a structural code-judo move is obvious and in-scope, prefer it; otherwise leave a short note and stop.
- Keep the final summary concise (1-3 sentences): what slop was removed, what was left on purpose.

## See also

- `ponytail` when the slop is speculative abstraction or a re-implement of an existing helper.
- `thermo-nuclear-code-quality-review` when the slop is spaghetti growth, thin wrappers, or file-size gate violations.
- `silent-failure-hunter` when the slop is swallowed errors or success-looking failure paths.
- `ui-ux` / `taste-skill` when the diff is UI chrome, not code style.
