# Scanners

Deterministic scanners run before judgment. A scanner hit is a discovery candidate, never a finding: it goes through validation like any other lead. Wrap the tools below in one script (for example `scripts/security/refresh.sh`) that runs every installed tool, fingerprints the results, and diffs them against a committed baseline (`tool rule-id path package@version` lines).

## Install

```bash
brew install osv-scanner pip-audit cargo-audit cargo-deny gitleaks trufflehog semgrep zizmor
```

`npm audit` ships with Node. The refresh script never installs tools. Write raw JSON outside the repo (for example `~/.cache/security-scans/<date>/`).

## Per tool

| Tool | Command (from repo root) | Read the output | Not assessed when |
|------|--------------------------|-----------------|-------------------|
| osv-scanner | `osv-scanner scan source --format json -L web/package-lock.json -L crates/Cargo.lock -L requirements.txt:backend/requirements.txt` (one `-L` per lockfile) | `.results[].packages[].vulnerabilities[].id` per `package@version`. `GHSA-`, `PYSEC-`, `RUSTSEC-` ids. Check `affected` ranges against the installed version, and whether the vulnerable function is reached. | Missing, offline, or a lockfile it cannot parse (it says so on stderr). A `requirements.txt` with ranges describes the resolved floor, not what installs. |
| pip-audit | `pip-audit -r backend/requirements.txt --format json` (or the venv's `pip-audit` with no `-r` to audit what is installed) | `.dependencies[].vulns[]` with `id` and `fix_versions`. Empty `fix_versions` means no patched release yet. | Missing, or resolution failed (it resolves ranges live, so two runs can differ). |
| npm audit | per app: `cd <app> && npm audit --json --package-lock-only` | `.vulnerabilities{}`: `severity`, `range`, `via`, `fixAvailable`. Entries whose `via` is only strings are transitive; the root advisory is elsewhere in the list. Dev-only tooling rarely reaches production; say so. | Offline or no lockfile. Print a `NOT-ASSESSED <app>` line. |
| cargo audit | `cargo audit --file crates/Cargo.lock --json` | `.vulnerabilities.list[]` (real advisories) and `.warnings` (`unmaintained`, `yanked`, `unsound`). `unsound` in a crate called through FFI is worth a look. | Missing, or it could not fetch the RustSec DB. |
| cargo deny | `cargo deny --manifest-path crates/Cargo.toml check advisories bans sources licenses` | Diagnostics with a code (`vulnerability`, `banned`, `license-not-encountered`, `source-not-allowed`). | Missing, or no `deny.toml` (see `supply-chain.md`). |
| gitleaks | `gitleaks git . --redact --report-format json --report-path <out>` | `RuleID`, `File`, `Commit`, `StartLine`. `--redact` keeps the value out of the report. Rotate first, then decide on history rewrite. Obvious fake fixtures go in `.gitleaksignore` by fingerprint. | Missing. A shallow clone limits history coverage. |
| trufflehog | `trufflehog git file://$PWD --only-verified --json --no-update` | `DetectorName`, file, commit. `--only-verified` means the credential worked against the live provider: treat as an incident. Never paste the `Raw` field anywhere. | Missing, or offline (verification needs network). |
| semgrep | `semgrep scan --metrics=off --json --config p/python --config p/typescript --config p/react --config p/nextjs --config p/secrets --config p/rust <source dirs>` | `.results[]`: `check_id`, `path`, `start.line`, `extra.severity`. `.errors[]` lists skipped files; those are not assessed. | Missing, or registry download failed (offline). |
| zizmor | `zizmor --format json .github/workflows` | `ident` (for example `template-injection`, `excessive-permissions`, `unpinned-uses`) and the workflow path. | Missing. |

## What counts as "not assessed"

- The tool is missing, crashed, or printed nothing parseable.
- It ran offline when it needs a live database (osv, npm, pip-audit, trufflehog, semgrep registry).
- A lockfile or path was skipped (osv stderr, semgrep `.errors`).
- It scanned a moving target (unpinned requirements) and you report it as the deployed state.

Report each as "not assessed: <tool> <reason>". Never as clean. An absent measurement is not a pass, and missing data is not evidence of risk either.

## Triage a new fingerprint

1. Is the package or file shipped to production? (dev dependency, test fixture, script)
2. Is the vulnerable function or pattern reached from an untrusted input?
3. Is there a fixed version, and does upgrading break a pinned contract?
4. Fix, or accept into the baseline with a one-line reason in the PR body.
