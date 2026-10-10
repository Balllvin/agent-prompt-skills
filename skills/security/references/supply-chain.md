# Supply chain

OWASP Top 10 2025 puts Software Supply Chain Failures at A03 (https://owasp.org/Top10/2025/). List your dependency surface first: every npm lockfile, Python requirements, `Cargo.lock`, Swift `Package.resolved`, Docker base images, model routes, vendored agent skills, and plugins.

## Common gaps

### Python requirements without lock pins

If every line is a range (`fastapi>=0.141,<1.0`), what production installs changes whenever upstream publishes, so an audit describes a moving target and a bad release lands without a diff.

Fix: generate a lock and install from it.

```bash
uv pip compile backend/requirements.txt -o backend/requirements.lock --generate-hashes
# Dockerfile: pip install --require-hashes -r requirements.lock
```

Keep `requirements.txt` as the human-edited input. Audit the lock (`pip-audit -r backend/requirements.lock`). Until the lock exists, report Python results as "resolved floor, not deployed state".

### No `deny.toml` for Rust

Without it `cargo deny` cannot run, so there is no policy for licenses, banned crates, duplicate versions, or unknown registries and git sources.

Fix: `cargo deny --manifest-path crates/Cargo.toml init`, then set:
- `[advisories]` default, `yanked = "deny"`;
- `[sources] unknown-registry = "deny"`, `unknown-git = "deny"`;
- `[licenses] allow = [...]` from what the tree uses today (MIT, Apache-2.0, BSD, ISC, Unicode);
- `[bans] multiple-versions = "warn"`.

Run `cargo deny check` and `cargo test --locked`.

## Review a new or bumped dependency

1. Is it needed? Prefer no new dependency.
2. Maintainer signal: repo activity, number of maintainers, recent ownership transfer, typosquat-close name.
3. Install scripts (`npm` `preinstall`/`postinstall`, Python build backends, Cargo `build.rs`).
4. Advisory history (`osv-scanner`).
5. Lockfile diff: unexpected transitive additions, registry or git source changes.

Report unavailable data as unavailable. A package with no advisory data is "not assessed", not "safe".

## Agent-facing supply chain

- Vendored skills and plugins: read every script and every instruction line before merge. Look for network calls, credential reads, and text that tells an agent to widen permissions.
- MCP tools come from your own tool definitions. A third-party MCP server is a new dependency.
- Models: pinned routes with the privacy provider object. A new provider goes through `provider-routing`.
- Licenses: Apache and MIT copies keep their notice; CC-BY-SA sources are rewritten, not copied; sources with no license are not copied.
