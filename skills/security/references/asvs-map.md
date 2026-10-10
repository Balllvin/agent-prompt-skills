# ASVS 5.0 map

OWASP ASVS 5.0.0 (May 2025, 17 chapters, https://owasp.org/www-project-application-security-verification-standard/). Target Level 2. Cite requirement ids as `v5.0.0-<chapter>.<section>.<req>` so findings stay comparable across reviews. Verify chapter titles against the release before citing; the ids are authoritative, the titles here are short labels.

Fill the owner column for your repo once (a path or module per chapter) and keep it current. Chapters with no owner are listed as out of scope in a report, not silently dropped.

| ASVS chapter | Typical owner | What to verify first |
|--------------|----------------|----------------------|
| V1 Encoding and sanitization | API layer, UI renderers | Parameterized SQL only; model or user markdown sanitized before render |
| V2 Validation and business logic | Money, order, quota, and approval services | Limits, approval flow, and money rules enforced server-side |
| V3 Web frontend security | Each web app | CSP, no token in `localStorage` where a cookie fits, proxy header handling |
| V4 API and web service | Routers, MCP endpoint, browser proxies | Auth on every route, method checks, mass assignment |
| V5 File handling | Uploads, file tools | Size and type limits, path confinement |
| V6 Authentication | Auth module, admin login | Password storage, rate limits, admin on a separate origin |
| V7 Session management | Session cookies, refresh tokens | Expiry, revocation, cookie flags |
| V8 Authorization | Every per-user filter; API key scopes | Object-level checks, key scope, money routes unreachable from keys |
| V9 Self-contained tokens | JWT handling | Pinned algorithms, audience, expiry |
| V10 OAuth and OIDC | Third-party account connects | `state`, exact `redirect_uri`, PKCE, scope refusal at connect |
| V11 Cryptography | Secrets vault, key hashing | Hash API keys; encrypt stored credentials; constant-time compares |
| V12 Secure communication | Provider clients, hosting | TLS verify on, no plaintext hops to third parties |
| V13 Configuration | Env config, `.env.example`, Dockerfiles | No fallback secrets, boot-time config checks, debug off |
| V14 Data protection | Personal and financial data, LLM provider policy | Zero-retention provider policy, log redaction, retention |
| V15 Secure coding and architecture | Dependencies, native code | Lockfiles, `unsafe` review, see `supply-chain.md` and `rust-review.md` |
| V16 Security logging and error handling | Logging config, proxy logs | Ids as fields, no secrets or bodies, errors not swallowed |
| V17 WebRTC | Voice or live media, if any | Out of scope unless it ships |
