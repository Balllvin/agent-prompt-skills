---
name: ship-verify
description: Use when shipping work - open a PR, push a branch, "ship" or "yeet" a change, fix CI or a red check, resolve a merge conflict or rebase, fetch or address PR review comments, deploy and verify a deploy, run post-deploy smoke tests, or write a weekly review or "what did I get done" summary. Triggers include /ship-verify, /yeet, /ci, /fix-ci, /loop-on-ci, /review-and-ship, /new-branch-and-pr, /fix-merge-conflicts, /get-pr-comments, /gh-address-comments, /run-smoke-tests, /weekly-review, /what-did-i-get-done, "open a PR", "fix CI", "merge conflict", "address review comments", "deploy", "ship", "weekly review". Load it even when the user names only one step. For Railway hosting, also load railway-deployment and use-railway.
---

# Ship and verify

One path from a finished diff to merged, deployed, and verified. The repo's `AGENTS.md` owns the durable rules (worktrees, branch names, PR headings, who merges); this skill is the operating manual. Never abandon a real error: iterate until every error is fixed or documented with an owner, and stop looping when the stop rule below says so.

## Index

| Need | Section / reference |
|---|---|
| Branch, worktree, commit, PR | [Branch and PR](#branch-and-pr), [new-branch-and-pr](references/new-branch-and-pr.md), [yeet](references/yeet.md) |
| Pre-ship self review | [review-and-ship](references/review-and-ship.md) |
| Red checks, CI loops | [Gate and CI](#gate-and-ci), [ci](references/ci.md) |
| Merge conflicts, rebase | [fix-merge-conflicts](references/fix-merge-conflicts.md) |
| When to stop | [When to stop iterating](#when-to-stop-iterating) |
| PR review comments | [Review comments](#review-comments), [get-pr-comments](references/get-pr-comments.md), [gh-address-comments](references/gh-address-comments.md) |
| Deploy and verify | [Deploy](#deploy), [../railway-deployment/SKILL.md](../railway-deployment/SKILL.md), [../use-railway/SKILL.md](../use-railway/SKILL.md) |
| Post-deploy smoke tests | [Smoke tests](#smoke-tests), [run-smoke-tests](references/run-smoke-tests.md) |
| Weekly or ranged work summary | [Summaries](#summaries), [weekly-review](references/weekly-review.md), [what-did-i-get-done](references/what-did-i-get-done.md) |

## Branch and PR

- Work in a dedicated worktree (for example `worktrees/<task>`) on an agent-prefixed branch (for example `agent/<task>`) cut from the latest `origin/main`. Keep local `main` a clean mirror used only to cut worktrees; editing it poisons every later worktree.
- Continue an existing PR on its exact branch; a second PR for the same work splits review history.
- Commit in checkpoints, one per finished step that still passes its checks, so reviewers can follow the history.
- Stage intended files only. Never stage scratch docs, worktrees, local databases, runtime state, or secrets. `git add -A` is wrong in a busy checkout because unrelated local edits and ignored-but-present scratch leak in.
- Rebase onto `origin/main`, push, open a draft PR to `main`. Title in everyday words. Use the repo's PR headings as `##` headings. A good default set: what was wrong, what this fixes, what you should notice, what this does not do, checks. Under checks, name the focused tests you ran.
- The body is a briefing, not a lab notebook. A reviewer who has the diff should learn the point in under a minute. No SHAs or rebase genealogy. The squash body is the PR body. Cut it if it runs past about 40 lines.
- Spawn a fresh review subagent per review. Do not resume a spent one.
- Never push directly to `main` unless the repo owner set that rule. Never merge unless the owner asked for that merge.

## Gate and CI

Learn whether hosted CI runs and what the local gate is (`AGENTS.md`). Run the focused tests for the files you changed and name those commands under checks. Details: [ci](references/ci.md).

Record the commit from your main fetch as an immutable SHA for the rebase. Another worktree can advance the shared `origin/main` ref. Before you push, compare current main with that SHA and rerun the focused tests the rebase can affect.

When tests mix a compatibility facade with direct implementation imports, trace copied dependency bindings. Facade patch teardown may leave a fake in the implementation. Real-session fixtures must bind their canonical repository and session explicitly. Replay the facade suite before the direct suite; isolated passes alone do not prove test isolation.

- Native or compiled components run their own pinned test command (for example `cargo test --locked`) when touched.
- Never weaken, skip, or xfail a test to go green. A contract change retargets the assertion; a wrong product gets fixed.
- Merge conflicts: resolve for correctness, regenerate lockfiles with the package manager, leave no markers, rerun affected checks. Rebase unpublished work; preserve published history with a normal merge when rebasing would need a force push.

## Review comments

Fetch with `gh pr view <n> --comments` and `gh api repos/<owner>/<repo>/pulls/<n>/comments --paginate`. Number each thread, fix the real ones, then post one summary: implemented, not implemented on purpose (with why), checks. Resolve the threads after the reply so the reviewer sees closure.

## When to stop iterating

Adapted from Sentry's `iterate-pr` skill (Apache-2.0, see the repo's `THIRD_PARTY_NOTICES.md`). "Never give up" means never abandon a real error. It does not mean looping forever. Stop when all of these hold:

- The focused tests for the changed files passed. Name the commands.
- Every high and medium review finding is fixed, or answered with a reason it is not implemented. Low findings (nits, style preferences) may stay open when you say so in the summary reply.
- Do not rerun those tests after a metadata-only push.

Stop and report instead of retrying when the same failure survives two different fixes, when the failure lives outside the diff (flaky baseline, provider outage, missing toolchain), or when the next step needs the owner (merge, secrets, a product decision). Name the blocker, the evidence, and the owner.

## Deploy

Read-only by default. Deployed state is shared production; a wrong variable or redeploy hits real users, so every write (variables, redeploy, restart, service config, domains, deletes) needs the owner's explicit yes first.

- Pass the target service and environment explicitly on every platform CLI call. Linked context is often some other project.
- Check the build context before a deploy: a service that builds from a subdirectory cannot see files outside it.
- Logs: filter structured logs on fields (`event`, `request_id`, `run_id`), not sentence text.
- Database-changing scripts (`ALTER SYSTEM`, `CREATE/DROP EXTENSION`, manual migrations) are owner-only: show the command, do not run it.
- On Railway: [railway-deployment](../railway-deployment/SKILL.md) owns the workflow (watch paths, SKIPPED deploys, healthchecks, migrations, verification); [use-railway](../use-railway/SKILL.md) is the CLI and API reference.

## Smoke tests

After a merge deploys, poll the platform's deployment list until the merge commit is live (on Railway a newer SKIPPED row for an unwatched path also counts; see railway-deployment), then hit health (`/healthz`) and the changed route on the real public host. The [run-smoke-tests](references/run-smoke-tests.md) commands are generic; use the target app's own Playwright or pytest smoke. Prefer deterministic waits; rerun a passing fix once to rule out flake. Stop any poller you started.

## Summaries

Use the current git user email, exclude merges, state the real date range, and describe changes functionally from commits and diffs only. Where work lands as squash merges, merged PR titles (`gh pr list --state merged --author @me`) are a better unit than raw commits.

## Record

A new bug class earns a lessons entry in the repo (problem, cause, fix, prevention). Leave the local `main` mirror on the merge commit.
