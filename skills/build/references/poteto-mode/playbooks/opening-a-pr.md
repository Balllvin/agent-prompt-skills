### Opening a PR

Invoked at the end of every other playbook.

**Worktree.** Work from a git worktree off main; subagents inherit it. Multiple `Task` calls on the same branch each get their own worktree, or `git fetch && git reset --hard origin/<branch>` between them. Dirty branch with unrelated work: patch out, fresh worktree, apply. Snarled worktree: reset from main, redo minimally.

**Commits.** Commit liberally; rebase into small, ordered commits before opening PRs. Each commit is a future PR: landable, ordered to tell the story. Amend when the fix belongs in a just-made commit; new commit when separable.

**PRs.** `/deslop` the diff before commit; `/no-comments` the diff before review; apply the **unslop** skill to the PR description and commit bodies. Small PRs, 5 narrow over 1 fat; stack follow-ups, branch off main only for genuinely independent work. For stacked PRs, use whatever stacking tool your team uses; the principle is small, ordered slices with the stack visible to reviewers. `gh pr view <number>` before referencing PR status. Rebase on `main` before substantial stack work. No `## Summary` / `## Test plan` boilerplate on small PRs; commit bodies don't restate the subject. A performance change reports one primary number in the body and puts the rest in an artifact. Do not babysit each PR while a stack is still being built. Push back when feedback drifts from intent.

**Briefing.** Write the PR body as a briefing a reviewer can read in under a minute. Say why the change exists, what it leaves out, what it could break, and how you proved it. Use short sentences and few identifiers. The squash commit body is the PR body. Cut the body once it would push that squash commit past about 40 lines. Put each section under a `##` heading, not a bold lead-in. Do not list SHAs or rebase genealogy. Do not add a preamble that says the branch is based on main. `AGENTS.md` owns the five heading names. Follow [ship-verify](../../../../ship-verify/SKILL.md) for those headings and the ship steps. Do not invent a second heading set in this playbook.

A subagent that opens a PR runs `interrogate`, `/deslop`, and `/no-comments`, returns the URL, and does NOT babysit. Return to the parent.
