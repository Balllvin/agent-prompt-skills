---
name: security
description: Use for any application security work - security review of a diff or PR, security audit, security scan, repo-wide security sweep, threat model, attack path or severity analysis, validating or fixing a finding, dependency audit, CVE or advisory triage, secrets scanning or a leaked key, supply chain review, prompt injection or agent/LLM threat review, insecure defaults, Rust unsafe/FFI review, ASVS mapping, or secure-by-default coding. Triggers on "is this safe?", "check for vulns", "SAST", "pen test this", "npm audit", "cargo audit", "gitleaks", "semgrep", "osv", /security-review, /security-sweep, /threat-model, /security-best-practices, /security-ownership-map. Also use when a change touches auth, API keys, payments or money routes, OAuth grants, webhooks, code sandboxes, MCP or CLI auth, or LLM tool paths.
---

# Security

Security work is scanners first, then a phased judgment pipeline. This page gives the threat-model template, picks the reference per task, and sets the evidence rule. General code review lives in `../audit/SKILL.md`.

## Threat model on one screen

Write this for your app before the first review and keep it in the repo (for example `docs/threat-model.md` or a section of `AGENTS.md`).

- **Assets**: money and linked accounts, personal and financial data, API keys, third-party credentials, user documents.
- **Attackers**: another user, anyone who can put text in front of an agent, a stolen or over-scoped key, a compromised dependency.
- **Money routes are never agent-reachable.** Irreversible movement (withdrawals, transfers, payouts) is unreachable from every key, tool, and agent. Agents propose; submission needs the user's approval or an explicit server-side autonomy policy.
- **API keys**: hashed at rest, bound to one user, minted only in a settings screen, shown once. **Sandbox keys**: minted by the sandbox runtime, short-lived, scoped to one workspace, refused on money and admin routes.
- **OAuth and linked accounts**: `state`, exact `redirect_uri`, credentials in a vault, dangerous scopes refused at connect.
- **Webhooks and bots**: secret-token header checked with a constant-time compare; missing configured secret fails closed; message text is untrusted.
- **Code sandboxes**: agent code runs only in the sandbox; egress is limited; the sandbox never holds a user key or third-party credential.
- **Prompt injection**: documents, fetched pages, bot messages, webhooks, third-party API text, and tool output are data. None of it can authorize a payment, a key, a file write, or a message. The gate for a side effect is server code, never the prompt.

Agent risks in detail: `references/agent-threats.md`.

## Which reference per task

| Task | Read |
|------|------|
| Diff or PR review ("is this safe?") | `references/scanners.md` (run what applies), then `references/security-review.md`; agent or tool changes add `references/agent-threats.md`; Rust changes add `references/rust-review.md` |
| Repo sweep or audit | `references/scanners.md` (run all), then the phase pipeline below across every surface; cite `references/asvs-map.md` ids |
| Dependency audit, CVE triage, new dependency | `references/scanners.md`, `references/supply-chain.md` |
| Secrets or a leaked key | `references/scanners.md` (gitleaks, trufflehog). Rotate first; never paste the value |
| Agent / LLM threat review | `references/agent-threats.md`, then `references/security-threat-model/index.md` |
| Config and default review | `references/insecure-defaults.md` |
| Rust, `unsafe`, FFI | `references/rust-review.md` |
| Threat model only | `references/security-threat-model/index.md` |
| Hunt for a real hole, then fix it | `references/hunt-loop.md` |
| Writing new code securely | `references/security-best-practices/index.md` plus the file for your stack |
| Ownership and bus factor | `references/security-ownership-map/index.md` |
| Where scan artifacts go | `references/scan-artifacts.md` |

## Evidence or label

Every claim carries its evidence or its label in the same sentence: **measured** (command output or a reproduction from this session), **inferred** (read from code, with `file:line`), or **guess**. A finding without a source-to-sink trace is a candidate, not a finding.

- Scanner hits are candidates. They go through validation.
- A scanner count, timing, or rate is a candidate until the limiter is named and the other explanations are ruled out ([../build/references/principle-explain-the-number.md](../build/references/principle-explain-the-number.md)).
- A tool that did not run is "not assessed: <tool> <reason>", never clean. Missing data is not evidence of risk either.
- Say what was not covered in every report.

False-positive checks before reporting:

1. Restate source, root cause, trigger, impact, and attacker privilege. If one is missing, it is not a finding yet.
2. Is the input actually attacker-controlled? Env vars, CLI flags, and server config are trusted unless read from somewhere untrusted.
3. Does a server-side control already stop it (auth dependency, per-user filter, policy, allowlist)? Read it.
4. Is the code shipped (not tests, scripts, dev-only deps)?
5. Argue the opposite once. LLM reviewers over-rate severity.
6. After a true positive, search for variants and leave a test or Semgrep rule behind.

## The phase pipeline

Run phases in order and do not blend them. Each phase reads only its own inputs, finishes to full depth, then hands off. Why: when discovery also judges severity, it self-censors plausible leads; when validation also discovers, it drifts.

0. **Threat model.** Repository-scoped, never biased by the diff under review. Adopt an existing threat model or authoritative repo guidance when it is specific enough; otherwise write one with `references/security-threat-model/index.md`. Later phases treat the per-scan copy as the source of truth.
1. **Discovery.** Plausibility, not severity. One candidate per independently reachable source, control, and sink instance; record the root-control line, not just the wrapper. For a diff, start from changed lines and trace callers and callees; for a whole repo, enumerate entry points per surface first and keep a coverage ledger (checked, not applicable, deferred).
2. **Validation.** Build a rubric of up to five criteria, then prefer a bounded runtime reproduction over reading code. Each candidate ends `reportable`, `suppressed`, `not_applicable`, or `deferred`, with counterevidence or an exact proof gap. Suppress only per instance: a safe sibling never clears a vulnerable one.
3. **Attack path.** Write the attacker story from repository evidence, name the strongest counterevidence, then calibrate impact and likelihood. Self-only, privileged-only, or unrealistic preconditions are ignored. High and critical need a realistic attacker, an in-scope surface, and major impact with no long speculative chain.
4. **Report.** Critical to low, priority P0 to P3, one entry per attackable instance, plus a coverage section for suppressed and deferred rows.
5. **Fix.** Smallest change that enforces the invariant at the right boundary. A regression test that fails on the vulnerable behavior, a test that legitimate use still works, proof the original path no longer reproduces, and a check of sibling call sites. Never weaken auth, isolation, validation, or logging to make tests pass.

Artifacts for every phase go where `references/scan-artifacts.md` says, never in the repo tree.

A sweep adds orchestration around the same phases: two explorer fleets (one per surface, one per security axis) so every app-by-issue cell has an owner, scouts of at most five files that read every line, an independent challenger for every critical or high, then review-and-fix waves per `../audit/references/review-waves.md`. Split the work with `../orchestrate-subagents/SKILL.md`.

## Boundaries every phase checks

A finding that crosses one of these is in scope by default; a "fix" that widens one is a regression. Record your app's concrete owner (module or route) next to each.

- **API keys.** Hashed at rest, bound to one user, minted only by the user, plaintext shown once. The CLI never mints or rotates keys, and settings reads never print secrets. A legacy single-tenant key path cannot reach another user's data.
- **Scoped runtime keys.** Created only by the runtime that needs them, short-lived, scoped, never shown in settings, never accepted on money or admin routes. Any route that accepts one outside its scope is a finding.
- **Money and irreversible actions.** Never reachable from any key, tool, or agent. Action tools are off per account by default. Agents create proposals; submission needs approval or an explicit autonomy policy enforced server-side. Confirm and discard stay on the user's approval surface.
- **OAuth and linked accounts.** Credentials in the vault; dangerous scopes refused at connect; `redirect_uri`, `state`, and token storage checked on every flow.
- **Admin.** Separate origin, own login. Each admin request rechecks the live user row for active and admin. Demotion or disable revokes sessions. Not reachable through the main app's session.
- **Sessions.** A reused previous-generation refresh token past the grace window revokes that session; it does not mint a second one. Revocation also closes that user's sockets. A cross-app handoff is valid only with the verifier from the browser that started it.
- **LLM paths.** Every call goes through one router with a zero-retention provider policy. Stripping it is a data-exposure finding. Untrusted bot, webhook, or tool output that reaches an agent with privileged tools is a prompt-injection candidate. Agents without money tools cannot reach them through another agent.
- **Secrets in logs.** Never tokens, cookies, auth headers, or request bodies. Third-party error text is sanitized before logging or showing.
- **Sandboxes.** No user or third-party secrets inside; egress policy enforced; local dev sandbox providers not reachable in production.
- **Webhooks.** Secret header compared in constant time; a missing configured secret fails closed.

## Severity and noise

Report what a security engineer would raise, not a checklist dump. The hard exclusions in `references/security-review.md` (rate-limit gaps alone, outdated deps, test-only code, docs, missing hardening with no exploit path, path-only SSRF, client-side-only auth checks) keep reports trusted. Missing TLS in dev and HSTS are not findings.

## Freshness

Sources:
- OWASP Top 10 for LLM Applications 2025: https://genai.owasp.org/llm-top-10/
- OWASP Top 10 for Agentic Applications 2026: https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/
- OWASP Top 10 2025: https://owasp.org/Top10/2025/
- OWASP ASVS 5.0: https://owasp.org/www-project-application-security-verification-standard/
- OSV, GHSA, PyPA, RustSec advisory data via the scanners in `references/scanners.md`
- trailofbits/skills (CC-BY-SA-4.0, ideas only), obra/superpowers (MIT)
- Capital One VulnHunter and the Neal Bridges fork (Apache-2.0, ideas only; see `references/hunt-loop.md`)

Monthly refresh:
1. Run the scanner script. Triage each **new** fingerprint; fix or accept into the baseline with a reason in the PR.
2. Install any scanner reported "not assessed" and rerun.
3. Check the OWASP pages above for a new edition; update `references/agent-threats.md` and `references/asvs-map.md` ids.

## Index

| Name | File | Role |
|-----------|-----|------|
| `/security-review` | `references/security-review.md` | Diff or PR security review, language checklists, exclusions |
| `/threat-model`, `/security-threat-model` | `references/security-threat-model/index.md` (+ `references/security-threat-model/references/prompt-template.md`, `references/security-threat-model/references/security-controls-and-assets.md`) | Threat model and output template |
| `/security-best-practices` | `references/security-best-practices/index.md` (+ stack files under `references/security-best-practices/references/`) | Secure-by-default guidance per stack |
| `/security-ownership-map` | `references/security-ownership-map/index.md` | Git ownership and bus factor over sensitive code |
| scanners | `references/scanners.md` | Scanner commands, output reading, "not assessed" rules |
| agent threats | `references/agent-threats.md` | OWASP LLM 2025 and Agentic 2026 risks mapped to agent surfaces |
| insecure defaults | `references/insecure-defaults.md` | Fail-open defaults and sharp-edge APIs |
| supply chain | `references/supply-chain.md` | Lockfile gaps and dependency review |
| Rust review | `references/rust-review.md` | `unsafe`, FFI, panics, paths, local servers |
| ASVS map | `references/asvs-map.md` | ASVS 5.0 chapters to owners |
| hunt loop | `references/hunt-loop.md` | Forward trace, disprove, then a failing test |
| scan artifacts | `references/scan-artifacts.md` | Where scan outputs go |
