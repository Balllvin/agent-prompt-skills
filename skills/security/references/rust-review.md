# Rust review (unsafe, FFI, local servers)

Use for Rust crates that take untrusted input: agent tool runners, FFI libraries loaded by another runtime, local HTTP servers, and CLIs that spawn processes. Themes drawn from Trail of Bits' Rust review guidance (CC-BY-SA-4.0; our own words).

## Where to look

| Area | Risk |
|-------|------|
| `ffi.rs` and any `extern "C"` entry point | `unsafe` FFI: null and lifetime handling, lengths, UTF-8, panics across the boundary |
| File tools, path helpers, stores | Path traversal and symlink escape from granted roots; file writes |
| Local HTTP server | Bind address, origin and CSRF checks, auth on localhost |
| Process spawning | Child processes, signal handling, env leakage |
| Provider HTTP clients | TLS, timeouts, secret handling, error text |
| Tool, MCP, and scheduler code | Untrusted tool output, retries, resource bounds |

## Checks

- **unsafe**: `rg -n 'unsafe' crates/`. Each block needs a `SAFETY:` reason that holds for every caller. FFI entry points wrap work in `catch_unwind`; a panic unwinding into C is undefined behavior.
- **Panics as DoS**: `unwrap`, `expect`, indexing, and `as` casts on untrusted input (tool args, HTTP bodies, model output) crash a request or the server. Prefer `?` and `get`.
- **Integer handling**: lengths and offsets from input use `checked_*` or `try_from`, not `as`.
- **Paths**: canonicalize, then check `starts_with(root)`; re-check after following symlinks; reject `..` before join, not after.
- **Processes**: `Command` with argv, never `sh -c` with model text. Clear or allowlist env so provider keys do not leak to children.
- **Local server**: binds `127.0.0.1` only; rejects foreign `Origin`/`Host` (DNS rebinding); no CORS wildcard.
- **Secrets**: keys never in `Debug` output, logs, or error strings sent to a model.
- **Deps**: `cargo audit` and `cargo deny` (see `supply-chain.md`); `--locked` builds.
