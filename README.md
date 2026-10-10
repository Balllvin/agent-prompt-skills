# Agent prompt skills

Portable skills for coding agents: writing prompts, splitting work across subagents, building, reviewing, securing, shipping, and deploying. Each folder under `skills/` is one skill with a `SKILL.md` entry point and optional `references/` loaded on demand.

## Skills

| Skill | What it does |
| --- | --- |
| [agent-prompt-engineering](skills/agent-prompt-engineering/SKILL.md) | Write and cut prompts, skills, and rules: direct language, one term per concept, a checkable done test, lean output contracts. |
| [orchestrate-subagents](skills/orchestrate-subagents/SKILL.md) | The parent keeps the task and primary files; children take bounded map, slice, review, repair, and verify work with allowed files, forbidden files, and a done test. |
| [build](skills/build/SKILL.md) | How to build: the build ladder (delete, reuse, then write), fast-by-design rules, TDD, debugging, design principles, and long-run working style. |
| [audit](skills/audit/SKILL.md) | Every review lens in one place: diff review, review waves, thermos, over-engineering, silent failures, performance, tests, types, and replying to review. |
| [security](skills/security/SKILL.md) | Scanners first, then a phased pipeline (threat model, discovery, validation, attack path, report, fix) with agent/LLM threats, supply chain, and ASVS mapping. |
| [layered-spec](skills/layered-spec/SKILL.md) | Write a spec-only plan PR for multi-surface work: layers 0 to 6, parallel homework slices with zero file overlap, and copy-paste implementer prompts. |
| [ship-verify](skills/ship-verify/SKILL.md) | From finished diff to merged, deployed, and verified: branches and PRs, CI, conflicts, review comments, smoke tests, and work summaries. |
| [ui-ux](skills/ui-ux/SKILL.md) | Everything a person sees: data-first screens, honest states, motion, messages, copy (Unslop), landings, brand and image assets, and rendered verification. |
| [provider-routing](skills/provider-routing/SKILL.md) | Route LLM calls safely: live model facts, zero-data-retention gates, reasoning effort, xAI Chat vs Responses, deadlines, prompt caching, and speech. |
| [fmp-integration](skills/fmp-integration/SKILL.md) | Use a metered market-data API (Financial Modeling Prep) without blowing the budget: one owner per data class, freshness classes, cost model, and checks. |
| [railway-deployment](skills/railway-deployment/SKILL.md) | Run a full stack on Railway: setup, env and secrets, Postgres, Redis, backend, frontend, security, deploy and verify, and troubleshooting. |
| [use-railway](skills/use-railway/SKILL.md) | Railway's official agent skill (MIT): CLI and API reference for projects, services, deploys, variables, domains, and databases. |

Third-party sources and licenses: [skills/THIRD_PARTY_NOTICES.md](skills/THIRD_PARTY_NOTICES.md).

## Use

Copy a folder from `skills/` into your agent skills directory (for example `.agents/skills/`, `.cursor/skills/`, or `~/.codex/skills/`). Skills cross-link with relative paths like `../build/SKILL.md`, so copy the ones you use side by side.

Prose rules point at Unslop in `skills/ui-ux/references/writing/unslop.md`. If an agent cannot load skills, bake the full Unslop rules into its prompt.

## Credits

- **Poteto.** We put her name here so the README looks expensive. Also thanks for Unslop and Pstack.
- **Grok.** Asked to be concise. Delivered three drafts of the same sentence and kept the longest one until someone noticed.
- **The owner ([@balllvest](https://x.com/balllvest)).** Voice-noted a whole product strategy, then asked if it was already on GitHub.
