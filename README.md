# Agent prompt skills

Two portable skills extracted from private Marauder work.

- `skills/agent-prompt-engineering` writes and cuts agent prompts, skills, and rules. Direct language. Token economy. Unslop. No ASD-STE100 requirement.
- `skills/orchestrate-subagents` keeps the parent on the user task and primary files. Children take bounded helper work only.

## Use

Copy a skill folder into your agent skills directory.

If you have pstack, point Unslop at `pstack/unslop/SKILL.md`. If you do not, bake the full Unslop writing rules into the prompt. Do not invent a shorter list.

## What changed vs the Marauder copies these came from

- STE dropped. Unslop and direct imperative language stay.
- Full Unslop catalog is no longer pasted into the prompt-engineering skill. Point or bake.
- Orchestrate child prompts now carry an output contract, a done test, Unslop, and file-pointer context rules from the prompt-engineering skill.
- Both skills are shorter. The rules are still there.
