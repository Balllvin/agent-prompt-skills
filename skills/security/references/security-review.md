---
name: security-review
description: >
  Conduct security-focused code reviews to identify high-confidence vulnerabilities
  with real exploitation potential. Supports two modes: (1) reviewing pending changes
  on the current git branch, and (2) reviewing a GitHub pull request by number.
  Use this skill whenever the user asks to review code for security issues, audit
  a PR for vulnerabilities, run a security scan, check for injection flaws, find
  hardcoded secrets, or do any kind of security-focused code analysis. Also trigger
  when users say things like "is this safe?", "any security concerns?", "check for
  vulns", "SAST", "security audit", or "pen test this code". This skill should be
  used even for quick security checks — it ensures consistent, high-quality analysis
  with minimal false positives.
---

# Security Code Review

A focused security review methodology for identifying vulnerabilities in code changes. Designed to catch real exploitable issues while keeping noise manageable.

## Modes of Operation

### Mode 1: Branch Review (Local Changes)

Use when the user wants to review pending changes on the current branch.

**Steps:**
1. Run `git status` and `git diff --name-only origin/HEAD...` to identify changes
2. Run `git log --no-decorate origin/HEAD...` to see commits
3. Run `git diff --merge-base origin/HEAD` to get the full diff
4. Identify which languages are involved and load the relevant checklists below
5. Analyze the diff using the methodology below

### Mode 2: PR Review

Use when the user references a specific PR number or asks to review a pull request.

**Steps:**
1. Use `gh pr view <number> --json files,title,body,additions,deletions` to get PR metadata
2. Use `gh pr diff <number>` to get the complete diff
3. Identify which languages are involved and load the relevant checklists below
4. Analyze the diff using the methodology below

---

## Analysis Methodology

### Phase 1 — Repository Context Research

Before analyzing changes, understand the security posture of the codebase:

- Identify existing security frameworks and libraries in use
- Look for established secure coding patterns (e.g., parameterized queries, input sanitization helpers)
- Examine existing validation and sanitization patterns
- Understand the project's security model and threat boundaries
- Check for security-related configuration (CSP headers, CORS policies, auth middleware)

### Phase 2 — Comparative Analysis

Compare the new changes against what already exists:

- Does new code deviate from established secure patterns?
- Are there inconsistent security implementations?
- Does the change introduce new attack surfaces?
- Are existing security controls being bypassed or weakened?
- Are new dependencies introduced that expand the attack surface?

### Phase 3 — Vulnerability Assessment

Examine each modified file for security implications:

- Trace data flow from user inputs to sensitive operations
- Look for privilege boundaries being crossed unsafely
- Identify injection points and unsafe deserialization
- Check for hardcoded secrets and weak cryptography
- Verify that error handling doesn't leak sensitive information

---

## Security Categories to Examine

**Input Validation Vulnerabilities:**
- SQL injection via unsanitized user input
- Command injection in system calls or subprocesses
- XXE injection in XML parsing
- Template injection in templating engines
- NoSQL injection in database queries
- Path traversal in file operations
- HTTP header injection
- LDAP injection
- XPath injection

**Authentication & Authorization Issues:**
- Authentication bypass logic
- Privilege escalation paths
- Session management flaws
- JWT token vulnerabilities (weak signing, missing expiry, algorithm confusion)
- Authorization logic bypasses
- Insecure direct object references (IDOR)
- Missing authentication on sensitive endpoints

**Crypto & Secrets Management:**
- Hardcoded API keys, passwords, or tokens
- Weak cryptographic algorithms or implementations (MD5, SHA1 for security, DES, RC4)
- Improper key storage or management
- Cryptographic randomness issues (using `math.random` for security tokens)
- Certificate validation bypasses
- Weak password hashing (unsalted, low iterations)

**Injection & Code Execution:**
- Remote code execution via deserialization
- Pickle injection in Python
- YAML deserialization vulnerabilities
- Eval injection in dynamic code execution
- XSS vulnerabilities (reflected, stored, DOM-based)
- Server-Side Template Injection (SSTI)
- Prototype pollution (in contexts with security impact)

**Data Exposure:**
- Sensitive data in logs (credentials, tokens, PII)
- API endpoint data leakage
- Debug information exposure in production
- Verbose error messages exposing internals
- Sensitive data in URL parameters
- Missing encryption for data in transit

---

## Language-Specific Checklists

Apply the relevant checklist(s) based on which languages appear in the changes.

### Python
- [ ] `eval()`, `exec()`, `compile()` with user input
- [ ] `pickle.loads()` / `pickle.load()` on untrusted data
- [ ] `yaml.load()` without `Loader=SafeLoader` (use `yaml.safe_load()`)
- [ ] `subprocess.run()` / `os.system()` / `Popen` with `shell=True` and user input
- [ ] f-strings or `.format()` in SQL queries instead of parameterized queries
- [ ] `__import__()` or `importlib` with user-controlled module names
- [ ] `marshal.loads()` on untrusted data
- [ ] `tempfile.mktemp()` (use `mkstemp()` instead — TOCTOU race)
- [ ] `hashlib.md5()` / `hashlib.sha1()` for password hashing (use `bcrypt`, `argon2`, or `scrypt`)
- [ ] `random` module for security-sensitive values (use `secrets` module)
- [ ] `xml.etree.ElementTree` without defusedxml (XXE risk)
- [ ] Django `mark_safe()` / `|safe` template filter with user input
- [ ] Flask `render_template_string()` with user input (SSTI)
- [ ] `jwt.decode()` with `algorithms` not specified or `verify=False`

### JavaScript / TypeScript
- [ ] `eval()`, `Function()`, `setTimeout(string)`, `setInterval(string)` with user input
- [ ] `dangerouslySetInnerHTML` in React with unsanitized content
- [ ] `innerHTML`, `outerHTML`, `document.write()` with user input
- [ ] `child_process.exec()` with string concatenation (use `execFile` or `spawn` with arrays)
- [ ] Template literals in SQL queries instead of parameterized queries
- [ ] `JSON.parse()` on untrusted input without try/catch (can crash server)
- [ ] Missing or weak CORS configuration (`Access-Control-Allow-Origin: *` on authenticated endpoints)
- [ ] `require()` or dynamic `import()` with user-controlled paths
- [ ] `vm.runInNewContext()` / `vm.Script` for sandboxing (easily escapable)
- [ ] `new RegExp(userInput)` without escaping (ReDoS in server-side with timeout implications)
- [ ] `Object.assign()` / spread with user-controlled keys into sensitive objects (prototype pollution with impact)
- [ ] Express `res.redirect()` with unvalidated user input
- [ ] Missing `httpOnly`, `secure`, `sameSite` flags on session cookies
- [ ] `bypassSecurityTrustHtml` / `bypassSecurityTrustScript` in Angular

### Go
- [ ] `fmt.Sprintf()` in SQL queries instead of parameterized queries
- [ ] `os/exec.Command()` with unsanitized user input
- [ ] `html/template` vs `text/template` confusion (text/template does NOT escape HTML)
- [ ] `net/http` handlers missing authentication middleware
- [ ] Unchecked `err` returns on security-critical operations (e.g., auth checks, crypto)
- [ ] `crypto/rand` vs `math/rand` confusion (math/rand is predictable)
- [ ] `filepath.Join()` with user input without cleaning `..` sequences
- [ ] `ioutil.ReadAll()` / `io.ReadAll()` on untrusted HTTP responses without size limits
- [ ] Missing TLS verification (`InsecureSkipVerify: true`)
- [ ] `reflect` package with user-controlled type names
- [ ] CORS middleware configured with wildcard origins on authenticated routes

### Java / Kotlin
- [ ] String concatenation in SQL/JPQL/HQL queries (use PreparedStatement or JPA parameters)
- [ ] `Runtime.exec()` / `ProcessBuilder` with user input
- [ ] `ObjectInputStream.readObject()` on untrusted data (deserialization RCE)
- [ ] `XMLInputFactory` / `DocumentBuilderFactory` without disabling external entities (XXE)
- [ ] `ScriptEngine.eval()` with user input
- [ ] `Class.forName()` with user-controlled class names
- [ ] Spring `@RequestMapping` without method restriction (allows unintended HTTP methods)
- [ ] Missing `@PreAuthorize` / `@Secured` on sensitive Spring endpoints
- [ ] `MessageDigest.getInstance("MD5")` for password hashing
- [ ] JNDI lookups with user-controlled names (Log4Shell pattern)
- [ ] Thymeleaf `th:utext` with user input (unescaped HTML)
- [ ] `SecureRandom` not used where `Random` is used for tokens/secrets

### Ruby
- [ ] String interpolation in SQL queries (use ActiveRecord parameterized queries)
- [ ] `system()`, backticks, `exec()`, `%x{}` with user input
- [ ] `send()` / `public_send()` with user-controlled method names
- [ ] `ERB.new(user_input).result` (SSTI)
- [ ] `YAML.load()` on untrusted data (use `YAML.safe_load()`)
- [ ] `Marshal.load()` on untrusted data
- [ ] `constantize` with user-controlled strings
- [ ] `html_safe` on user-provided content in Rails
- [ ] `render inline:` with user input in Rails (code execution)
- [ ] Weak `before_action` / `skip_before_action` patterns that bypass auth

### Rust
- [ ] `unsafe` blocks — review for soundness (memory safety issues ARE valid in unsafe Rust)
- [ ] `.unwrap()` on user-controlled input in server code (panic = crash)
- [ ] Raw SQL via string formatting instead of query builders
- [ ] `Command::new()` with user-controlled arguments
- [ ] FFI (`extern "C"`) boundary issues — memory safety not guaranteed across FFI
- [ ] `std::mem::transmute` with incorrect types
- [ ] Missing bounds checking in `unsafe` pointer arithmetic

### C / C++
- [ ] Buffer overflows: `strcpy`, `strcat`, `sprintf`, `gets` (use `strncpy`, `snprintf`, `fgets`)
- [ ] Format string vulnerabilities: `printf(user_input)` (use `printf("%s", user_input)`)
- [ ] Integer overflows in size calculations before `malloc`
- [ ] Use-after-free patterns
- [ ] Double-free vulnerabilities
- [ ] Null pointer dereferences on untrusted input
- [ ] Missing bounds checks on array indexing
- [ ] `system()` with user-controlled strings
- [ ] Signed/unsigned integer comparison issues
- [ ] `alloca()` with user-controlled sizes (stack overflow)

---

## Severity Guidelines

| Severity | Criteria |
|----------|----------|
| **HIGH** | Directly exploitable vulnerabilities leading to RCE, data breach, or authentication bypass |
| **MEDIUM** | Vulnerabilities requiring specific conditions but with significant impact |
| **LOW** | Defense-in-depth issues or lower-impact vulnerabilities (report sparingly, only if noteworthy) |

Report HIGH and MEDIUM findings by default. Include LOW findings if they are concrete and actionable.

## Confidence Scoring

| Score | Meaning |
|-------|---------|
| 0.9–1.0 | Certain exploit path identified |
| 0.8–0.9 | Clear vulnerability pattern with known exploitation methods |
| 0.7–0.8 | Suspicious pattern requiring specific conditions to exploit |
| 0.5–0.7 | Possible issue worth noting — report as LOW with caveats |
| Below 0.5 | Don't report — too speculative |

Flag issues where you're **>70% confident** of exploitability. For the 50-70% range, include as LOW severity with a clear note about what conditions would make it exploitable.

---

## False Positive Filtering

Apply these rules to avoid noise, but err on the side of reporting when genuinely uncertain.

### Hard Exclusions — Do Not Report

1. **Rate limiting gaps** — missing rate limits alone is not a vulnerability
2. **Secrets on disk** managed by dedicated tooling (e.g., vault, sealed secrets)
3. **Regex injection** — injecting into regex patterns alone is not exploitable
4. **Missing hardening** that has no concrete exploit path
5. **Outdated dependencies** — managed separately by dependency scanning tools
6. **Test-only code** — findings only in test files with no production impact
7. **Markdown/documentation files** — not executable code
8. **Missing audit logs** — absence of logging is not a vulnerability

### Contextual Exclusions — Apply Judgment

These are excluded in MOST cases but should be reported if there's a concrete exploit path:

1. **DOS/resource exhaustion** — Exclude generic "this could use lots of memory" findings. Report if there's a specific amplification attack or algorithmic complexity exploit.
2. **Open redirects** — Exclude in most cases. Report if it can be chained with another vulnerability (e.g., OAuth token theft via redirect).
3. **Race conditions** — Exclude theoretical timing issues. Report if there's a concrete TOCTOU with security impact (e.g., checking permissions then acting on a different file).
4. **Memory safety in safe languages** — Buffer overflows are impossible in Rust (safe code), Python, Java, JS, Go. Report only in `unsafe` Rust, C, C++, or across FFI boundaries.
5. **Log content** — Logging URLs or generic data is fine. Report if logging passwords, tokens, API keys, PII, or request headers that likely contain credentials.
6. **GitHub Action workflows** — Most workflow issues aren't exploitable. Report only with a specific attack path involving untrusted input (e.g., `${{ github.event.pull_request.title }}` in a `run:` step).
7. **Shell script injection** — Report only if untrusted external input reaches the script (not just env vars or CLI flags from trusted sources).
8. **SSRF** — Must control host or protocol to be valid. Path-only SSRF is not a vulnerability. Client-side JS cannot perform SSRF.
9. **Client-side auth checks** — Missing permission checks in frontend code is not a vulnerability (server enforces auth). Report only if the server endpoint is also unprotected.

### Trusted Inputs

These are considered trusted and attacks requiring control of them are generally invalid:
- Environment variables
- CLI flags and arguments
- Server-side configuration files
- Kubernetes secrets / cloud provider secret managers

However, if the code explicitly reads these from an untrusted source or exposes them, that IS a finding.

---

## Output Format

Report findings in this structure:

```markdown
# Finding 1: [Category]: `file.py:line`

* **Severity:** HIGH | MEDIUM | LOW
* **Confidence:** 0.X
* **Description:** Clear description of the vulnerability
* **Exploit Scenario:** Concrete attack path an attacker could take
* **Recommendation:** Specific fix with code example if possible
```

After all findings, include a brief summary:

```markdown
## Summary

- **Files reviewed:** N
- **Findings:** X HIGH, Y MEDIUM, Z LOW
- **Languages:** Python, JavaScript, ...
```

If no vulnerabilities are found, state: **"No security vulnerabilities identified in the reviewed changes."** and still include the summary of what was reviewed.

---

## Important Notes

- Focus ONLY on security implications **newly added** by the changes under review. Do not comment on pre-existing security concerns unless the change makes them significantly worse.
- Even if something is only exploitable from the local network, it can still be HIGH severity.
- Each finding should be something a security engineer would raise in a code review.
- When genuinely uncertain, lean toward reporting with an appropriate LOW severity and confidence score rather than silently dropping it.
- Use the language-specific checklists as a scanning guide, not an exhaustive requirement. Not every item needs to be checked if it's clearly not relevant to the changes.
