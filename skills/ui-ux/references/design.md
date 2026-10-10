# Design

Expressive visuals: pages that sell, and assets that carry a brand. The old taste, landing, brand, image, and video skills now live under `design/`, a reference of the `ui-ux` skill. This file routes to them and holds the rules that apply across all of them.

## Which rules

| Surface | Rules | Why |
| --- | --- | --- |
| Signed-out landing, marketing route, welcome page, portfolio site, brand asset, image, video, game | this file | The job is persuasion or identity. Taste and variety matter. |
| Anything behind a login: data views, tables, settings, chat, admin, workspaces | `../SKILL.md` product sections | The data is the product. Taste machinery (glass, marquee, hover-scale, big type) slows decisions and hides failures. |
| Signed-out page that shows the product | both | this file owns layout and motion; the product rules' honesty, tokens, and failure states still apply. |

The app UI architecture doc wins for its app. `AGENTS.md` wins on workflow, file-size gates, and data-provider routing. Inside this reference, `taste-skill` wins visual-taste conflicts.

## Design read first

Before editing, write one line: surface, audience, the one decision the page asks for, and the proof. Example: "Reading this as: signed-out research-app landing; promise is research you can cite; decision is create account or leave; proof is an animated product mock." This stops the model reaching for the aesthetic it used last time.

Then pick dials (`taste-skill` section 1): design variance, motion intensity, visual density. Say them. A brief for a bank and a brief for a game studio should not land on the same numbers.

## Anti-slop filter

This is a filter, not a style. It says what not to ship when the model reaches for "designed" defaults. Any one tell is survivable; stacking them is what reads as AI-made on sight. If the brief explicitly asks for one, do it. Full list: `design/taste-skill.md` section 9.

- **No em-dash or en-dash as a separator anywhere visible.** It is the most common model tell and survives "use sparingly." Use a period, comma, colon, or hyphen.
- **No div-built fake product UI** on generic landings. Use a real screenshot, a generated image, or nothing. The exception is an animated HTML mock built from real component labels and real data.
- **No three equal feature cards, centered hero plus gradient blob, or AI-purple accent.** These are the model's defaults, so they are what every other generated page already looks like.
- **No Inter plus slate by default, no pure `#000`, no neon glow, no gradient headline text, no custom cursors.**
- **No filler copy:** version eyebrows (`V0.6`, `BETA`), section numbers (`001 / Capabilities`), step labels (`Step 1/2/3`), scroll cues, locale and weather strips, "Quietly trusted by", "Elevate/Seamless/Unleash". They add words without adding a fact.
- **No fake data:** "John Doe", "Acme", `99.99%`. Fake-perfect numbers read as invented. Quote real public figures from a named source or show nothing.
- **No decorative dots, hairline grids, or pills on photos** unless they carry meaning.
- **Rationed middle-dot**, at most one per metadata line.

### The five AI default looks

Adapted from Anthropic's `frontend-design` skill (Apache-2.0, see `../../THIRD_PARTY_NOTICES.md`). A generated page tends to land on one of these whole kits. Name the one you are closest to and move away from it on a landing:

1. Warm cream background, serif display face, terracotta accent.
2. Near-black background with one acid accent color.
3. Broadsheet hairline rules with zero radius. It can be a deliberate product look for dense data screens. Keep it there if chosen. Avoid it as the default on landings, where it reads as the model's editorial kit.
4. The SaaS kit of identical rounded cards with soft shadows.
5. ALL-CAPS eyebrows and middle-dot meta strings.

Two passes before you build. First write a compact plan: 4 to 6 named hex tokens, type roles, and an ASCII wireframe. Then review that plan against the brief and this list, and cut whatever is generic. Spend boldness in one place per page, not everywhere.

Pre-flight: run `taste-skill` section 14 before you call a page done.

## Scroll-film landing rules

Use these when a signed-out landing (`/login`, `/about`, a welcome route) tells the product story as a scroll-driven film.

- **Scroll is the playhead.** Motion is CSS sticky plus CSS scroll-driven animation, behind `@supports`. GSAP ScrollTrigger only when CSS cannot pin one scene. No Lenis, canvas frame sequences, Three.js, or video scrubbing. Why: CSS scroll timelines run off the main thread and degrade to a readable page when unsupported. The exception is a decorative WebGPU shader backdrop, which must still degrade to a static image.
- **Final state is the default state.** Without JavaScript, without scroll-timeline support, and under `prefers-reduced-motion`, every word and the CTA must be visible in document order. An observer that never fires must not hide the sign-up button.
- **Footage is real.** Live data comes from your own cached endpoint, never from a metered third-party API in the browser. Loading, empty, failed, stale, and ready are five distinct states. Mocks show only capabilities that exist.
- **Humans | AI toggle** on every landing, with one agent data module feeding the AI view, `/llms.txt`, and the Markdown `/login`. Agents do not click toggles.
- **Scene variety.** Adjacent cuts never share a layout family (stack, bleed, window, terminal, poster, strip, pudding, control). Left-copy/right-mock twice in a row is a fail. Name each scene's family in the PR.
- **4 to 6 beats.** Open, hold, cut, close. A beat that restates an earlier one is deleted.
- **Web vitals budget.** LCP under 2.5 s, INP under 200 ms, CLS under 0.1. Preload the hero image and use `font-display` with metric-matched fallbacks so web fonts do not shift layout.

## Image generation

Use `design/imagegen/index.md` (OpenAI Image API through its CLI). Flow:

1. Decide generate, edit (the user gave an image or said inpaint/mask/change only X), or batch.
2. Collect prompt, verbatim text, avoid list, and inputs up front.
3. Turn the prompt into a short labeled spec. Do not invent creative requirements the user did not ask for.
4. Run, then look at the output: subject, composition, text accuracy, invariants.
5. Change one thing per iteration. Several changes at once hide which one helped.
6. Final files go under `output/imagegen/`; temp files under `tmp/imagegen/`, deleted after.

`OPENAI_API_KEY` must be set locally. Never ask the user to paste a key into chat.

For website comps before code, use `image-taste-frontend` (generate section images, analyze them, then build to match) with `image-taste-art-direction` or `imagegen-frontend-web` / `imagegen-frontend-mobile` for the prompts. One image per section beats a tiny compressed board because the build copies detail it can read.

## Video generation

Use your video model's API (check its current docs). Decide create, remix (you have a video id and want a change), status/download, or batch. Start small (for example 720p, 4 seconds); set size and seconds as API params because prose in the prompt does not change them. Poll async jobs, download assets, delete temp prompt files, and change one thing per iteration.

## Brand, banners, slides

- Premium brand boards and logo systems as images: `brandkit`.
- Logos, CIP mockups, icons, social photos, and HTML slides: `design-kit` (the older upstream `design` skill). Its `design-routing.md` picks the sub-reference.
- Banners at platform sizes: `banner-design`.
- Tokens and component specs for a brand or marketing system: `design-system`. Product tokens stay in each app's architect file.

## References

| Reference | Read when |
| --- | --- |
| `design/taste-skill.md` (1207 lines) | Any landing, portfolio, or redesign. Dials, brief-to-system map, AI tells, pre-flight. Default taste authority. |
| `design/high-end-visual-design.md` | The brief is "make it feel expensive". Fonts, spacing, shadows. |
| `design/gpt-taste.md` | GSAP-heavy editorial page with pinning and stacking. |
| `design/industrial-brutalist-ui.md` | Brief asks for a brutalist, Swiss, or terminal aesthetic. |
| `design/stitch-design-taste.md` | Writing a `DESIGN.md` for Google Stitch. |
| `design/ui-ux-pro-max.md` (658 lines) | Choosing a style, palette, or font pairing from a catalog. |
| `design/image-taste-frontend.md` (1228 lines) | Image-first web build: generate section comps, analyze, implement. Replaces the deleted `image-to-code-skill.md`. |
| `design/image-taste-art-direction.md` (686 lines) | Art-directing hero and section comp images. |
| `design/imagegen-frontend-web.md` (987 lines) | One generated image per website section. |
| `design/imagegen-frontend-mobile.md` (1465 lines) | Mobile app screen concepts and flows as images. |
| `design/imagegen/index.md` | Generating or editing any image. Extras: `references/cli.md`, `image-api.md`, `prompting.md`, `sample-prompts.md`, `codex-network.md`. |
| `design/brandkit.md` (798 lines) | Brand boards, logo systems, identity decks as images. |
| `design/banner-design/index.md` | Social, ad, hero, or print banners. Extra: `references/banner-sizes-and-styles.md`. |
| `design/design-kit/index.md` | Logos, CIP, icons, social photos, HTML slides. Extras in `references/`: `design-routing`, `logo-design`, `logo-style-guide`, `logo-color-psychology`, `logo-prompt-engineering`, `cip-design`, `cip-style-guide`, `cip-deliverable-guide`, `cip-prompt-engineering`, `icon-design`, `social-photos-design`, `banner-sizes-and-styles`, `slides`, `slides-create`, `slides-strategies`, `slides-layout-patterns`, `slides-copywriting-formulas`, `slides-html-template`. |
| `design/design-system/index.md` | Brand or marketing token architecture and component specs. Extras in `references/`: `token-architecture`, `primitive-tokens`, `semantic-tokens`, `component-tokens`, `component-specs`, `states-and-variants`, `tailwind-integration`. |
| `design/hatch-pet/index.md` | Building an animated Codex pet spritesheet. Extras: `references/animation-rows.md`, `codex-pet-contract.md`, `qa-rubric.md`, `scripts/`, `LICENSE.txt`. |

Files over 600 lines are catalogs. Search them for the section you need instead of reading end to end.
