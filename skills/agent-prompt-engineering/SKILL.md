---
name: agent-prompt-engineering
description: Write, cut, and iterate prompts, skills, rules, and agent workflows. Use when designing agents, writing SKILL.md or rules, architecting workflows, refining anti-slop or taste skills, or making prompt language direct and cheap. Unslop every prompt this skill ships. Point at pstack unslop when the agent can load skills. Bake the Unslop writing rules when it cannot. Do not invent a shorter anti-slop list. Do not require ASD-STE100.
---

# Agent prompt engineering

Use this skill to design or rewrite agent prompts, skills, and rules.

Write instructions in the imperative and the active voice. One instruction per sentence. One term per concept. Use "must" and "do not". Unslop the skill's own prose and every prompt it produces.

## Core principles

- Start simple. One augmented LLM call or a fixed workflow before a free-roaming agent.
- Workflows are predefined paths. Agents pick tools and next steps from feedback.
- Keep the design small. Make the plan visible. Document and test the agent-computer interface.
- Tokens rot. Keep the smallest high-signal set.
- Measure. Iterate on failures. Write a check the agent can run itself before you write the prompt.
- Right altitude. Specific enough to guide, loose enough for heuristics. No brittle if-else scripts. No "do the right thing".
- Persona labels alone do not change output. Give docs, examples, and do/don'ts instead.

## Prompt language

- Active imperative. "Read the file", not "the file should be read".
- Condition before action. Warning before the step it protects.
- Numbered or bulleted list for more than two steps.
- One topic per paragraph.
- One word, one meaning. Do not rotate "plan", "roadmap", and "strategy" for the same object.
- Short verbs. "Use", not "utilize". "Start", not "initiate". "Check", not "validate against expectations".
- Keep articles. Telegraphic fragments parse wrong.
- No all-caps threats. No fake stakes.
- A rule must be checkable from the output. "Be concise" is not. "No preamble" is.
- If a rule needs a long justification, the rule is wrong. Cut it until it is obvious.

Slop: "Additionally, it's important to ensure that you thoroughly explore the codebase in order to gain a comprehensive understanding before you consider making any changes."

Direct: "Before you edit, read the files that own the behavior you change. List their callers."

Slop: "You may want to leverage the available testing utilities to validate your implementation where possible."

Direct: "Run the test suite after each change. If a test fails, fix the code before you continue."

### Token economy

No waste. Not minimum tokens. If a cut costs clarity, keep the words.

Condense the prompt:

- State each rule once, in the section that owns it. No later "reminder".
- Give paths and names. Do not paste content the agent can fetch.
- Delete role fluff.
- Merge overlapping rules.
- Hard problems are the exception. Then add "take your time", "read all related code", "form hypotheses before you change anything".

Put an output contract in the prompt:

- Answer first. No preamble, no restated question, no closing summary.
- Length matches the answer. One sentence if that covers it.
- No numeric caps unless a machine parses the output or a skim channel displays it.
- Smallest format that carries the content. Paths and line refs, not pasted files.
- A take, not a hedge. If options are real, still name a pick.
- Keep full sentences. Do not ask for cryptic fragments.

When a response is off, correct the delta only. Do not re-prompt from scratch.

```
# Output format
- Unslop. Point at pstack/unslop/SKILL.md, or bake the full Unslop writing rules. Do not invent a shorter list.
- Answer first. Length matches the answer.
- Evidence as paths and line refs.
- No preamble, no restated instructions, no closing summary.
- Commit to a recommendation.
```

## Unslop

Must always apply to this skill's output and to every prompt, skill, or rule it produces.

### Bake or point

1. Point. Tell the agent to read and apply `pstack/unslop/SKILL.md` or `.agents/skills/pstack/unslop/SKILL.md` (`/unslop`). Use this when the agent can load repo skills.
2. Bake. Paste the Unslop writing rules from that file into the prompt. Use this when the agent cannot load skills.

If unsure, bake. Do not invent a shorter list.

### Process

1. Scan for Unslop patterns.
2. Rewrite. Keep meaning. Match intended tone.
3. Add soul. Opinions, varied rhythm, specific detail. Sterile voice is also a tell.
4. Self-audit. "What makes this obviously AI generated?" Fix those tells.

### Prompt-only extras

Unslop does not name these. Delete them in prompts:

- Marketing adjectives with no test. "Robust", "seamless", "comprehensive", "cutting-edge", "powerful", "world-class".
- Hedges that hide a requirement. "Perhaps", "ideally", "where possible", "as appropriate", "if feasible". State the condition or make the instruction unconditional.
- Empty intensifiers. "Very", "truly", "incredibly", "extremely".
- Restating the instruction as a benefit. The instruction is enough.

## Pstack house notes

When the repo has `.agents/skills/pstack/`:

- Read `HOUSE.md` before poteto-mode. House overrides win.
- Unslop PR text and commit messages with `unslop/SKILL.md`.
- Radical simplification still applies. Ask "can I delete this?"
- For Marauder coding agents, model mapping lives in `.cursor/rules/pstack-models.mdc`. Default is Grok 4.6, no fast, effort high.
- Skip as defaults. Arena, swarm, orchestrate-program, autopilot, hillclimb.

Steal from poteto-mode without pasting the playbooks:

- Design the verification loop before the prompt.
- File pointers, not inlined dumps.
- Parent reviews child work and writes its own summary.
- Sequence work into units that each end in a check.
- Do not block the human on reversible work. Present the result.
- Encode a repeated instruction as a lint, flag, or script, not more prose.

## Workflow patterns

Source: https://www.anthropic.com/research/building-effective-agents

Augmented LLM. Retrieval, tools, memory. Clear interfaces. MCP when it fits.

1. Prompt chaining. Fixed subtasks with gates. Outline, check, write.
2. Routing. Classify, then dispatch.
3. Parallelization. Section independent work, or vote across runs.
4. Orchestrator-workers. Parent splits unpredictable subtasks, workers run them, parent synthesizes. The parent still owns the primary path.
5. Evaluator-optimizer. Generate, score against a clear rubric, revise.

Free-roaming agents. Tool loop, plan, recover, use environment feedback. Use only when steps cannot be predicted. Stopping conditions. Human checkpoints for irreversible work. Sandbox. Cost compounds.

## Context engineering

Source: https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents

Curate tokens across turns. Prompts, history, tool results, state.

- Write. Files, scratchpads, memory. Compact history by summary.
- Select. Lightweight refs. Load on demand. Progressive disclosure. Names and folders are signals.
- Compress. Drop old tool dumps and stale thinking.
- Isolate. Separate concerns. Do not stuff one window.

System prompts. Direct language. Sections such as background, instructions, tool guidance, output format. XML or Markdown headers. Start minimal. Add examples from real failures. Few canonical shots, not every edge case.

Tools. Small set. Non-overlapping jobs. Careful descriptions. Token-cheap returns. Tolerate bad input.

History. Prune, summarize, point. Persist long state outside the window.

Hybrid. Preload the few static invariants. JIT the rest.

## Cursor practices

Source: https://cursor.com/blog/agent-best-practices

- Plan first on non-trivial work. Edit the plan. Revert and replan when the plan was wrong.
- Let the agent find context. Tag only files you already know matter.
- Fresh thread for a new feature. Continue only to iterate or debug.
- `@Past Chats` or `@Branch` instead of pasting a whole session.
- Rules are always-on. Skills load on demand. Rules for invariants and gotchas. Skills for portable how-tos. Linters own style.
- TDD when it fits. Failing test, then code. Commit often.
- Hooks for long runs. Cap iterations.
- Screenshots for visual work. MCP for external tools. Commands in `.cursor/commands/`.

## Scar tissue rules

Rules grow from real failures. Never from speculation.

- After a mistake, add one short rule.
- Do not auto-generate a rules file and ship it raw. Generic content the model already knows hurts.
- Removal test. "Would deleting this cause a mistake the agent would not otherwise make?" If no, delete it.
- Prune on model updates. Stale rules weaken the ones that still matter.

## Useful techniques

Weng. Agent = model + planning + memory + tools. CoT, Tree of Thoughts, ReAct, Reflexion, external planner. Short-term context. Long-term retrieval.

dair-ai Prompt Engineering Guide. Zero/few-shot, CoT, self-consistency, ReAct, APE. Clear structure, examples, constraints, output formats.

Common shape. Role facts + constraints + examples + format + verification loop. Structured output. Critique then revise. Compaction checkpoints. Explicit stop and done tests.

## Checklist

1. Trigger. Description says when to load.
2. Outcome and done test. Exact commands with flags early. Named tools get used far more.
3. Pick a workflow pattern.
4. Role facts, minimal background, tool rules, output contract, never-touch list.
5. One to three canonical examples.
6. Guardrails and recovery if the agent loops.
7. Context strategy. Prompt vs JIT vs summarize.
8. Exit conditions for long runs.
9. Mental fail case. Add prevention or detection.
10. Unslop pass. Point or bake the full catalog.
11. Token pass. Each rule once. Lean output contract. No waste.

### Template

```
---
name: your-agent-skill
description: Use when ... (specific triggers).
---

# Role
Facts the agent needs. No theater.

# Goal and success criteria
Done means: <a test the agent can run>

# Boundaries
Never touch: secrets, vendor dirs, prod configs, generated files

# Tools and context
What to keep in prompt. What to load. What to summarize.

# Workflow
Use [chaining | routing | orchestrator-workers | ReAct | TDD loop]
1. ...

# Output format
Unslop. Answer first. Length matches the answer. Paths, not pastes. No preamble.

# Writing rules
Point at pstack/unslop/SKILL.md, or bake the full Unslop writing rules.
Do not invent a shorter list.

# Examples
(1-2 canonical)
```

### Eval prompts

- "Does this output meet <criteria>? If not, why and how to fix?"
- "Reflect on what worked and what failed. Update the approach."
- "Grill me on these changes." / "Prove this works." / "Scrap this and implement the smaller design."

## Anti-patterns

- Stuffing context just in case.
- Vague taste lectures with no commands, paths, or Never list.
- Hardcoded if-else in the prompt when feedback would do.
- No eval loop.
- Treating rules and skills as the same thing.
- A full agent for a fixed two-step job.
- No stop condition.
- Pasting whole files.
- Overlapping tool descriptions.
- Long noisy threads instead of a fresh one plus selective refs.
- Hedged requirements. They get treated as optional.
- A homemade three-bullet anti-slop note.
- No output contract.
- Cutting past clarity.
- Passive instructions that hide the actor.
- Skip plan, then grill, then implement on non-trivial work.
- Ban lists with no adaptive override.
- Marketing bans pasted onto a working product surface.
- Style prescriptions dressed as filters.
- A second design system beside the app's tokens.

### Harness hygiene

- Keep always-on `AGENTS.md` operational and short. Nest package files for local overrides.
- Add a rule only after the same mistake repeats.
- Confirm before force-push, production migrate, public comments, shared infra. One prior yes is not a blank check.
- User-facing status in plain language. Do not `echo` at the user.
- Long goals. Plan, grill the plan, run against a done-when. Revert and replan when the plan was wrong.

### Code-slop ladder

When cleaning AI diffs, load in this order:

1. `deslop`. Comments, weird try/catch, `any` casts, nesting, Jane-Doe fixtures.
2. `ponytail`. Speculative abstractions, re-implements, YAGNI.
3. `thermo-nuclear-code-quality-review`. Spaghetti, thin wrappers, silent fallbacks, huge file growth.
4. `silent-failure-hunter`. Empty catches and failures sold as success.

## Writing anti-slop skills

### Filter, not style

- Split DON'T (tells) from DO (app tokens, shells, architect docs).
- Stacked DON'Ts are what reads as AI-made. The list does not invent a look.
- Adaptive override. If the user, architect doc, or another skill asks for a specific thing, do that.
- Keep product filters separate from marketing filters. Cross-link. Do not merge.

### Ban-list altitude

- Observable tells. `hover:scale-105` on cards, `bg-clip-text` headlines, 3-icon grids, em dash in UI copy. Not "make it premium".
- Group by failure mode so an agent can scan.
- One litmus check beats five metaphors.
- Binary only for historically ignored rules (em dash ban). Everything else stays adaptive.

### Context for design skills

- Always-on. Pointers, authority order, file-size gates.
- On-demand. Full ban lists, ladders, checklists, examples.
- JIT product truth. Architect docs and tokens via search. Do not paste the design system into the skill.
- Pre-flight checklist. Critique against the filter before ship.

### Extra for UI examples

- No filler verbs. "Elevate", "Seamless", "Unleash".
- No fake-perfect metrics unless labeled mock.
- If the explanation is longer than the rule, cut the explanation.

### Harness map

| Source | Steal | Do not paste blindly |
|---|---|---|
| Muse taste | Filter framing, scannable bans, adaptive override | Landing-page hero rules on data routes |
| Taste-skill / Antfu | Em dash ban, Jane-Doe tells, fake screenshot ban | Glass and aurora on working surfaces |
| Codex frontend-skill | Composition first, cardless default, utility-copy litmus | Full-bleed heroes inside authenticated apps |
| Grok Build / thermo-nuclear | Code judo, spaghetti ban, thin-abstraction skepticism | Generic review prompts that ignore file-size gates |
| Cursor | Rules vs skills, plan first, fresh threads | Over-tagging whole trees |

## How to use

- Invoke on agent-design tasks.
- Combine with create-skill when building a new skill.
- Combine with `/unslop` when the agent can load it. Bake when it cannot.
- Combine with orchestrate-subagents when the prompt assigns workers. Parent keeps the user task and primary files.

## References

- Anthropic. Building effective agents. Effective context engineering. Writing effective tools.
- Cursor. Agent best practices. Rules, skills, plans, hooks.
- pstack unslop. `pstack/unslop/SKILL.md` or `.agents/skills/pstack/unslop/SKILL.md`.
- Steinberger. OpenClaw `SOUL.md` brevity rule. Scar-tissue rules. Role-theater takedown.
- Cherny. Pushback prompts. "Update your rules file so you don't make that mistake again."
- Willison. Designing agentic loops. Self-verifiable done tests.
- GitHub. How to write a great agents.md. Commands early, explicit boundaries.
- ETH Zurich. Evaluating AGENTS.md. Generic auto-rules hurt. Named tools get used about 160x more.
- Cai et al. Architecture rules over style. Stale rules degrade compliance.
- Weng. LLM Powered Autonomous Agents.
- dair-ai Prompt Engineering Guide.
- Cross-harness anti-slop. Muse, Antfu, Codex frontend-skill, Grok Build. Marauder translations live in `marauder-ui-ux`, `deslop`, `thermo-nuclear-code-quality-review`.
