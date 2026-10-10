---
name: code-review
description: Review a GitHub pull request for high-confidence bugs and repository instruction compliance. Use when a user asks for @code-review, code review, PR review, or review feedback before merge.
---

# Code Review

Review the given pull request with a high signal-to-noise bar.

## Workflow

1. Confirm the PR is open, not a draft, and still needs review.
2. Identify relevant repo instructions, especially `AGENTS.md` and any path-local guidance.
3. Inspect the PR summary, changed files, and diff.
4. Review for:
   - concrete bugs and behavioral regressions
   - explicit repo-instruction violations
   - historical context that makes a changed line risky
   - comments or local docs contradicted by the change
5. Score each potential issue from 0 to 100 and report only issues with confidence at least 80.
6. Cite exact file and line evidence for every finding.

## Guardrails

- Do not report style nits, speculative concerns, pre-existing issues, or failures that CI/typecheck will catch.
- Do not assume missing context is a bug.
- Do not merge, approve, or request changes unless explicitly instructed.
- Use `gh pr view`, `gh pr diff`, and `gh api` when reviewing GitHub PRs. Do not use `gh pr checks`. GitHub CI does not run.

## Output

If issues exist, lead with findings ordered by severity. Include:

- issue summary
- confidence score
- file and line reference
- why it is a bug or instruction violation
- concrete fix suggestion

If no high-confidence issues exist, say that clearly and mention what scope was reviewed.
