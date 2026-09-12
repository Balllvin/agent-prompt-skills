# Agent prompt skills

Two skills for writing agents that stay useful under a tight context window.

## Skills

**agent-prompt-engineering.** Write and cut prompts, skills, and rules. Direct language. One term per concept. A checkable done test before the prompt. Lean output contracts. Point at Unslop, or bake the full catalog. Do not invent a shorter anti-slop list.

**orchestrate-subagents.** The parent keeps the user task and the primary files. Children take bounded helper work only: map, slice, review, repair, verify. Every child prompt names allowed files, forbidden files, and a done test. The parent reads the diff and writes its own summary.

## Use

Copy a folder from `skills/` into your agent skills directory.

If you have pstack, point Unslop at `pstack/unslop/SKILL.md`. If you do not, bake the full Unslop writing rules into the prompt.

## Credits

- **Poteto**, for pstack. Unslop, poteto-mode, and the house rules these skills steal from without pasting the whole plugin. The good taste is theirs. The remaining slop is ours.
- **Grok**, for sitting in the repo, cutting tokens, and pretending that "just make the skill shorter" is a personality.
- **Alvin (@balllvest / Balllvin)**, who filed the request as a voice note, said Unsloth when he meant Unslop, then asked for a public repo like it was nothing. Tokenmaxxing in the About. Human in the loop. Sometimes the loop is a voice memo.
