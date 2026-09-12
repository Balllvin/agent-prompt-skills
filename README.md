# Agent prompt skills

Two skills for writing agents that stay useful under a tight context window.

## Skills

**agent-prompt-engineering.** Write and cut prompts, skills, and rules. Direct language. One term per concept. A checkable done test before the prompt. Lean output contracts. Point at Unslop, or bake the full catalog. Do not invent a shorter anti-slop list.

**orchestrate-subagents.** The parent keeps the user task and the primary files. Children take bounded helper work only: map, slice, review, repair, verify. Every child prompt names allowed files, forbidden files, and a done test. The parent reads the diff and writes its own summary.

## Use

Copy a folder from `skills/` into your agent skills directory.

If you have pstack, point Unslop at `pstack/unslop/SKILL.md`. If you do not, bake the full Unslop writing rules into the prompt.

## Credits

- **Poteto**, for pstack and Unslop. Named after a tuber. Ships taste like it is a root vegetable with opinions.
- **Grok**, who cut the token count, then wrote a paragraph about how short it is.
- **Balllvin ([@balllvest](https://x.com/balllvest))**, who said Unsloth, meant Unslop, and still shipped a public repo before the transcript caught up.
