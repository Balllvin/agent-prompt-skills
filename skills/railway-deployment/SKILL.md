---
name: railway-deployment
description: Use when standing up, deploying, configuring, securing, verifying, or debugging an app on Railway, especially a monorepo with several services (for example `backend`, `web`, `worker`) plus Postgres and Redis. Covers project setup, env vars and secrets, database and pool sizing, cache, backend and frontend services, security, post-merge verification, and failed-deploy diagnosis. Load it before a merge that will deploy, when adding a service, after a deploy fails, or when production returns 5xx after a release. For the full Railway CLI and API reference, load the companion `use-railway` skill.
---

# Railway deployment

How to run a full stack on Railway well. A merge is not a release: a release is done when the exact commit is serving, the healthcheck is green, and the logs are clean for a few minutes.

Examples use one repo with three app services, `backend` (API), `web` (Next.js), `worker` (queue consumer), plus `Postgres` and `Redis`. Replace names with yours. Commands match Railway CLI 5.x (`railway --version`). For anything not covered here (buckets, IaC files, metrics, tracing, the GraphQL API, database analysis), use the companion skill [`use-railway`](../use-railway/SKILL.md).

## Rules

1. Prove the deploy holds your SHA. "Latest deployment is SUCCESS" proves nothing if your commit was SKIPPED or a newer one replaced it.
2. Pass `--service` and `--environment` explicitly. The linked context is often a different service or project.
3. Read-only by default on shared environments. Variables, redeploys, restarts, service config, domains, scaling, and deletes change production. Get the owner's explicit yes for each write.
4. Fix forward. A failed build or failed healthcheck leaves the old deployment serving, so you have time to fix the cause instead of reverting.
5. Speed over efficiency. When production is broken, take the fastest correct path to green: a bigger pool, more memory, one more replica. Tune for cost later, with measurements.
6. Never print secret values. `variable list --json`, `--kv`, `railway run env` and `printenv` all show raw values.
7. Kill every background poller and log stream you start before you finish.

## Contents

1. [Setup](#1-setup): project, services, builds, domains, PR environments, regions, volumes
2. [Env and secrets](#2-env-and-secrets)
3. [DB](#3-db-postgres): Postgres, URLs, pool sizing, migrations, backups, `max_connections`
4. [Cache](#4-cache-redis): Redis, eviction, queues and locks
5. [Backend](#5-backend): API, workers, cron, healthchecks, replicas, graceful shutdown, job timeouts
6. [Frontend](#6-frontend): Next.js builds, build-time env, domains, CORS
7. [Security](#7-security)
8. [Deploy and verify](#8-deploy-and-verify)
9. [Troubleshooting](#9-troubleshooting)
10. [Checklist](#10-checklist)

## 1. Setup

### Install, sign in, link

```bash
npm i -g @railway/cli            # or: railway upgrade --yes
railway login                    # browser, or device code on headless machines
railway whoami --json
```

New project, or link an existing one. Links are per directory, so link each service folder you work from.

```bash
railway init --name myapp --json                       # creates the project and links this directory
# or
railway link --project myapp --environment production --service backend
railway status --json                                  # confirm project, environment, service
railway service list --json
railway service status --all --json                    # every service and its deployment state
```

### Add services

```bash
railway add --database postgres --json
railway add --database redis --json
railway add --repo owner/repo --branch main --service backend --json   # GitHub autodeploy
railway add --repo owner/repo --branch main --service web --json
railway add --repo owner/repo --branch main --service worker --json
railway add --service scratch --json && railway up --service scratch --detach -m "first deploy"   # deploy from local files instead
railway service source connect --repo owner/repo --branch main --service scratch                  # switch a local-upload service to GitHub
```

In the GitHub service settings, turn on "Wait for CI" so a push deploys only after checks pass.

### Monorepo: root directory and watch paths

Each service gets a root directory, a config file, and watch patterns. Railway builds a service only when a commit touches a path matching its patterns; otherwise the deployment is **SKIPPED**.

```bash
railway environment edit --environment production --service-config web source.rootDirectory "/web"
railway environment edit --environment production --service-config web build.watchPatterns '["web/**"]'
railway environment config --environment production --json \
  | jq '.services[] | {configFile, source, build: (.build | {builder, dockerfilePath, watchPatterns})}'
```

Keep the config in the repo instead. `backend/railway.toml`:

```toml
[build]
builder = "DOCKERFILE"
dockerfilePath = "backend/Dockerfile"
watchPatterns = ["backend/**", "shared-schema/**"]

[deploy]
preDeployCommand = "sh scripts/run-migrations.sh"
startCommand = "sh scripts/start-api.sh"
healthcheckPath = "/healthz"
healthcheckTimeout = 300
overlapSeconds = 20
drainingSeconds = 30
restartPolicyType = "ON_FAILURE"
restartPolicyMaxRetries = 3
```

`web/railway.toml`:

```toml
[build]
builder = "DOCKERFILE"
dockerfilePath = "Dockerfile"
watchPatterns = ["web/**"]

[deploy]
healthcheckPath = "/healthz"
healthcheckTimeout = 30
overlapSeconds = 20
drainingSeconds = 30
restartPolicyType = "ON_FAILURE"
restartPolicyMaxRetries = 3
```

- Watch patterns are gitignore-style globs matched against repo-root paths.
- If the image reads anything outside the service directory (a shared package, schema folder, generated files), that path must be in the build context **and** in `watchPatterns`. Otherwise a change there never redeploys the service, or the build fails with a missing file.
- A Dockerfile that copies repo-root folders needs `source.rootDirectory` `/` with `dockerfilePath` `backend/Dockerfile`, and the service's config-file path set to `/backend/railway.toml`. Moving it back to an isolated `/backend` root silently drops those folders from the context.
- SKIPPED for a docs-only or other-service commit is correct. The service keeps serving its last SUCCESS build.
- CI path filters (`on.pull_request.paths`) follow the same logic. A check that never started is not a pass.

### Build: Dockerfile or Railpack

- **Railpack** (default builder; Nixpacks is the legacy one) detects the language and builds without a Dockerfile. Good for a plain Node, Python, Go, or static app. Set `build.buildCommand` and `deploy.startCommand` when detection guesses wrong.
- **Dockerfile** when you need system packages, multi-stage builds, a compiled toolchain, or the exact same image locally and in production. A `Dockerfile` at the service root is picked up automatically; elsewhere set `dockerfilePath`.
- Pin base images by version (and digest if you can). Run as a non-root user.
- Railway Metal requires cache mount ids of the form `id=s/<service-id>-<target>` for `RUN --mount=type=cache`. Without the prefix the build fails.
- Listen on `$PORT`, bound to `::` (all interfaces, IPv4 and IPv6) so both the public proxy and private networking reach it.

### Domains

```bash
railway domain --service web --json                                  # generate a *.up.railway.app domain
railway domain app.example.com --service web --port 3000 --json      # custom domain; prints the DNS records
railway domain status app.example.com --service web --json           # DNS and certificate state
railway domain list --service web --json
```

Add the CNAME (and verification TXT) it prints at your DNS provider. Apex domains need a provider with CNAME flattening or ALIAS records. Railway issues the TLS certificate once DNS resolves; `domain status` shows progress. Give public domains only to services browsers must reach (section 7).

### Environments and PR previews

```bash
railway environment list --json
railway environment new staging --duplicate production --json
railway environment list --ephemeral --json      # PR environments
```

Turn on PR environments in the project settings. Each PR gets a copy of the base environment's services, with its own databases. Check that preview variables do not point at production data, payment keys, or outbound email.

### Regions, replicas, volumes

```bash
railway scale --service backend --environment production us-west=2       # replicas per region
railway volume add --service backend --mount-path /data --json
railway volume list --json
```

- Replicas must be stateless: no local files that matter, no in-memory sessions, and in-process schedulers must be leader-elected (a Postgres advisory lock or a Redis lock) or moved to a single `worker`.
- A service with a volume runs one replica, and redeploys briefly unmount the volume. Put durable data in Postgres or object storage; use volumes for databases and caches you can rebuild.
- Put the app in the same region as its database. Cross-region queries add latency to every request.

## 2. Env and secrets

```bash
railway variable list --service backend --environment production          # table; values are sensitive
railway variable set LOG_LEVEL=info --service backend --environment production
printf '%s' "$NEW_KEY" | railway variable set API_KEY --stdin --service backend --environment production
railway variable set A=1 B=2 --service backend --environment production --skip-deploys   # batch, deploy once later
railway variable delete OLD_FLAG --service backend --environment production
railway variable edit --service backend --environment production          # bulk edit with a reviewed diff
```

- **Service variables** belong to one service in one environment. **Shared variables** are defined once per environment in project settings and referenced as `${{shared.KEY}}`. Use shared variables for values several services need (an `APP_ENV`, a public base URL), not for secrets only one service should hold.
- **Reference variables** keep values in one place and follow rotations:

  ```
  DATABASE_URL=${{Postgres.DATABASE_URL}}          # private network URL
  REDIS_URL=${{Redis.REDIS_URL}}                   # private network URL
  BACKEND_INTERNAL_URL=http://${{backend.RAILWAY_PRIVATE_DOMAIN}}:${{backend.PORT}}
  PUBLIC_WEB_ORIGIN=https://${{web.RAILWAY_PUBLIC_DOMAIN}}
  ```

  Service names in references are case-sensitive.
- Setting or deleting a variable triggers a redeploy of that service unless you pass `--skip-deploys`. With `--skip-deploys`, apply later with `railway redeploy --service backend --environment production --yes`. `railway restart` does **not** pick up build-time values; it reuses the built image.
- **Sealed variables** are write-only: nobody can read them back, and `variable list` shows the name with no value. A sealed key with a null value already exists; do not recreate it. Seal every credential.
- Railway injects `RAILWAY_*` variables at runtime (`RAILWAY_ENVIRONMENT_NAME`, `RAILWAY_SERVICE_NAME`, `RAILWAY_GIT_COMMIT_SHA`, `RAILWAY_PRIVATE_DOMAIN`, `RAILWAY_PUBLIC_DOMAIN`). Log the commit SHA at startup.
- Validate required config at boot and fail with a clear message, or report it as 503 from `/healthz`. Reject unsafe values in deployed environments: a non-Postgres `DATABASE_URL`, `*` CORS origins, non-HTTPS origins.

### Run locally with production-shaped variables

```bash
railway run --service backend --environment staging -- python -m app.check_config
railway run --service backend --environment staging -- npm run dev
railway shell --service backend --environment staging       # subshell with variables loaded
railway connect postgres --environment staging              # psql over SSH or the TCP proxy
```

Put Railway flags before `--`. Prefer a staging environment; run against production only for read-only checks the owner approved. Private hostnames (`*.railway.internal`) do not resolve on your laptop, so a local process needs the public URL or `railway connect ... --tunnel-only`.

### Job feature flags

A flag that defaults off is a trap: the code ships, nobody sets the variable in production, and the job silently never runs.

- For each new flag, either default it on where the job should run, or set the variable in production as part of the release.
- Log every flag's state at startup (`job_disabled job=digest flag=DIGEST_ENABLED`) and check it after deploy.
- One owner per flag. Do not let an old or legacy flag disable a job a newer setting turned on.

## 3. DB (Postgres)

### URLs

- `${{Postgres.DATABASE_URL}}` is the **private** URL (`postgres.railway.internal`). Use it for every service in the project: no egress cost, never exposed to the internet.
- `${{Postgres.DATABASE_PUBLIC_URL}}` goes through a TCP proxy. Use it only for local tools, and prefer `railway connect postgres` (SSH tunnel) over leaving a proxy open.
- SQLAlchemy async needs the driver in the scheme: rewrite `postgresql://` to `postgresql+asyncpg://` in code, not by copying the value.
- Private networking is available at runtime only, not during the build. Do not query the database in a build step.

### Migrations on deploy

Run migrations in `preDeployCommand`, not in the start command. Pre-deploy runs once per deploy, before traffic moves, with the service's variables and private network; the start command runs on every replica and every restart.

`backend/scripts/run-migrations.sh`:

```sh
#!/bin/sh
set -eu
cd "$(dirname "$0")/.."
current="$(alembic current 2>&1 | tail -n 1)" || { echo "alembic current failed" >&2; exit 1; }
echo "Migration phase: alembic upgrade head (current=$current)"
if ! out="$(alembic upgrade head 2>&1)"; then
  printf '%s\n' "$out" >&2
  failing="$(printf '%s\n' "$out" | sed -nE 's/.*Running upgrade [^ ]+ -> ([^, ]+).*/\1/p' | tail -n 1)"
  echo "Alembic upgrade failed: current=$current failing=${failing:-unknown}" >&2
  exit 1
fi
echo "Migration phase: import the app once"
python -c "import app.main"
echo "Migration phase complete"
```

Before merging any migration:

```bash
cd backend
alembic heads                                              # exactly one head
rg -n '^revision\s*=' alembic/versions | sort              # unique revision ids
alembic upgrade head && alembic downgrade -1 && alembic upgrade head   # on a local copy
```

- Two branches that each added a migration produce two heads, and `upgrade head` fails in pre-deploy. Merge them in the same PR: `alembic merge heads -m "merge heads"`.
- Parent each new revision on the current live head. Keep revision ids short if `alembic_version.version_num` is `VARCHAR(32)`.
- Rehearse on a production-shaped database (schema built, stamped, then upgraded), not only an empty one.
- Old code keeps serving during the deploy overlap. Add columns nullable or with a default, backfill, switch readers, and drop in a later release.
- The migration process uses no pool (`NullPool`) so it holds no idle connections.

### Pool sizing and `max_connections`

Railway Postgres starts with the Postgres default `max_connections` (usually 100). Every process opens its own pool. Size each process to its fair share minus headroom:

```
usable    = max_connections - superuser_reserved_connections - reserved_connections - headroom
per_proc  = usable // (replicas * worker_processes_per_replica, summed over every service using the DB)
pool_size = per_proc;  max_overflow = 0..2
```

```sql
SELECT current_setting('max_connections')::int AS max_connections,
       current_setting('superuser_reserved_connections')::int
       + COALESCE(current_setting('reserved_connections', true), '0')::int AS reserved;
SELECT application_name, state, count(*) FROM pg_stat_activity GROUP BY 1, 2 ORDER BY 3 DESC;
```

- Read these at startup instead of hardcoding. Count processes from the launcher (`WEB_CONCURRENCY`, your `--workers`), not the CPU count.
- `headroom` (about 5) covers migrations, `railway connect` sessions, and other services.
- **Never cap the pool low.** A process that runs in-process dispatchers, schedulers, or queue drains lets them hold connections. With a small cap they take every slot, request handlers wait for `pool_timeout`, and every request returns 500 with `QueuePool limit of size N overflow M reached, connection timed out`. Take the full fair share; treat a floor as a warning for an undersized database, not a cap.
- Set `pool_timeout` below the proxy request timeout, turn on `pool_pre_ping`, and set `pool_recycle` (for example 1800 s).
- Set `application_name` per service and role so `pg_stat_activity` shows who holds connections.
- Log the computed size at startup (`db_pool_sized max_connections=… processes=… pool_size=…`).
- Need more? Raise `max_connections` (`ALTER SYSTEM SET max_connections = 200;` via `railway connect postgres`, then restart the Postgres service, owner approval) and give the database more memory, or add PgBouncer: `railway postgres pgbouncer add --service Postgres --pool-mode transaction`. Transaction mode breaks server-side prepared statements; for asyncpg set `statement_cache_size=0`.
- Never share one session across concurrent tasks, and never hold a transaction open across a slow external call.

### Backups and volumes

Postgres data lives on the database service's volume. Turn on backups before you need them.

```bash
railway postgres pitr status --service Postgres --json
railway postgres pitr enable --service Postgres                       # continuous backups (owner approval)
railway postgres pitr backup create --service Postgres --name pre-migration
railway postgres pitr backup list --service Postgres --json
```

- Take an on-demand backup before any destructive migration or bulk data fix.
- `pitr restore` restores into a **new** service; `pitr backup restore` overwrites the current data. Restore drills go to a new service, never over production.
- Without PITR, use scheduled backups from the database service's Backups tab, and test a restore once.

## 4. Cache (Redis)

```bash
railway add --database redis --json
railway variable set 'REDIS_URL=${{Redis.REDIS_URL}}' --service backend --environment production
railway connect redis --environment staging
```

- Use the private `REDIS_URL`. Do not add a TCP proxy to Redis.
- **Eviction policy.** Check it with `CONFIG GET maxmemory-policy`.
  - Pure cache: `allkeys-lru`, every key has a TTL, and the app treats a miss or an unreachable Redis as "go to the source".
  - Queues, locks, rate limits, sessions: `noeviction`. Eviction silently deletes jobs and releases locks.
  - Different needs, different instances: one Redis for cache (`allkeys-lru`), one for queues (`noeviction`).
  - `CONFIG SET` does not survive a restart. Put the policy in the Redis service's start command (for example `redis-server --maxmemory-policy noeviction`) so it persists.
- **Queues.** Use a library with acknowledgement and retry (a list plus a processing list, Streams with consumer groups, or a job framework built on them). Jobs must be idempotent: a worker killed mid-job will see it again.
- **Locks.** `SET lock:<name> <token> NX PX <ttl_ms>`; release with a compare-and-delete script so you never delete someone else's lock; always set a TTL longer than the job's timeout. Use a lock to elect one scheduler across replicas.
- Namespace keys (`app:env:purpose:id`) so environments sharing an instance never collide.
- Redis is not the database. Anything you cannot lose goes to Postgres.

## 5. Backend

### Service layout

- `backend`: HTTP API. Public domain only if browsers or third parties call it directly; otherwise `web` calls it over the private network.
- `worker`: same repo and image, different start command (`deploy.startCommand "python -m app.worker"`), no domain, no healthcheck path. Prove it with a startup log line and a heartbeat.
- Cron: a service with `deploy.cronSchedule` (for example `"*/15 * * * *"`, UTC) and `restartPolicyType = "NEVER"`. The process must do its work and **exit**. A run that never exits blocks the next one ("maximum number of running instances reached").
- If jobs run in-process in the API instead, size the DB pool for both (section 3) and elect one scheduler when there are replicas.

### Healthchecks

- Each HTTP service ships `/healthz` in the same app and pins it in `railway.toml`. A 404 on the healthcheck means the route is missing, not that the app crashed.
- `/healthz` is cheap and side-effect free: 200 when the process can serve, 503 with a short reason when required config is missing. Do not call slow third parties from it.
- `healthcheckTimeout` is the startup grace period. Railway probes until it passes or the timeout ends, then marks the deploy FAILED and keeps the old one serving. Size it to the real cold start: minutes for a backend that loads models or warms caches, about 30 s for a Next.js server.
- `/healthz` is a probe, not a page. Keep it out of navigation and sitemaps.

### Zero-downtime deploys and graceful shutdown

With `overlapSeconds` and `drainingSeconds`, Railway starts the new container, waits for its healthcheck, moves traffic, keeps the old one for the overlap, then sends SIGTERM and waits the drain window before killing it.

- Old and new code run together. API shapes, schema, cookies, and queued job payloads must work for both versions.
- On SIGTERM: stop accepting work, finish or requeue in-flight jobs, close pools. For uvicorn, `--timeout-graceful-shutdown 25` with `drainingSeconds = 30`.
- Jobs a killed container had claimed must be recoverable: leases that expire, and a startup sweep that requeues or fails orphans.
- Signing keys must accept old and new values across a deploy, or users are signed out.
- Do not merge right before a time-critical scheduled job; a redeploy restarts in-process schedulers.

### Per-job timeouts

A single-consumer queue runs jobs one after another. One job that never returns freezes everything behind it until the process restarts.

- Wrap every job type, and its finalize step, in a hang timeout (`asyncio.wait_for(run(job), timeout=JOB_TIMEOUT_S)`, a thread with a deadline, or the job framework's timeout).
- Bound every outbound call with a request timeout and capped retries, so the job timeout is a backstop.
- On timeout: log `job`, `run_id`, `duration_ms`; mark the job failed or retryable; release its lease; continue.
- Prevent overlapping ticks: a scheduled job still running must not start again.
- Test it: a worker test with a job that never returns must still let the next job run.

### Logging

Log JSON with ids as fields (`request_id`, `job`, `run_id`), at boundaries (start, decision, failure, done). Keep levels honest. Keep routine per-item logs low; Railway rate-limits very chatty services (around 500 lines per second). Never log secrets, tokens, cookies, auth headers, or request bodies.

## 6. Frontend

### Next.js builds

`next build` type-checks the whole app, including `*.test.ts` files in the `tsconfig` include. Unit test runners do not type-check. Green tests plus a red build is common. Before merging any change to `web/`:

```bash
cd web && npm ci && npx tsc --noEmit && npm run build
docker build -f web/Dockerfile web/          # same context as the service root, to reproduce Railway exactly
```

- Use `output: "standalone"` with `CMD ["node", "server.js"]`, and copy `.next/static` and `public/` into the runner stage.
- Make `.next/cache` writable by the runtime user; standalone still writes ISR entries there.
- Use relative imports in `next.config.ts`; path aliases may not resolve when the config loads.
- Static sites (Vite, plain HTML): build, then serve the output with a small static server bound to `$PORT`, or use Railpack's static detection.

### Build-time vs runtime variables

- `NEXT_PUBLIC_*` (and Vite's `VITE_*`) are **inlined at build time**. Changing one needs a rebuild (`railway redeploy --from-source` or a new commit), not a restart. With a Dockerfile, declare them as `ARG` in the build stage; Railway passes service variables as build args.
- Never put a secret in a `NEXT_PUBLIC_*` variable; it ships to every browser.
- Server-only values (`BACKEND_INTERNAL_URL`, signing secrets) are read at runtime in server code and route handlers, so they can change per environment without rebuilding.
- The browser cannot reach `*.railway.internal`. Either proxy API calls through Next.js route handlers (server to `backend` over the private network) or give `backend` a public domain and call it with CORS.

### Domains and CORS

- Prefer `app.example.com` (web) and `api.example.com` (backend) under one registrable domain, so cookies can be first-party with `SameSite=Lax`.
- Backend CORS: an explicit allowlist of HTTPS origins (`https://app.example.com`, plus preview origins if needed), never `*` with credentials. Build it from a variable, for example `CORS_ORIGINS=https://${{web.RAILWAY_PUBLIC_DOMAIN}},https://app.example.com`.
- Cookies: `Secure`, `HttpOnly` for sessions, explicit `Domain` only when subdomains must share them.
- Check the custom domain, not the `*.up.railway.app` host, when users reach the app through the custom domain.

## 7. Security

### Secrets

- Secrets live only in Railway variables, sealed. Never in the repo, the Dockerfile, image layers, build logs, PR text, or chat. `.env` files are gitignored and in `.dockerignore`; commit only a `.env.example` with names and no values.
- Scope each secret to the one service and environment that needs it. Staging and PR environments get their own keys, never production keys.
- Rotate: add the new key alongside the old, deploy code that accepts both, switch signers to the new key, remove the old key after sessions or tokens signed with it expire. Rotate immediately if a value was printed, committed, or pasted.
- Do not paste `variable list --json`, `--kv`, `railway run env`, or `printenv` output anywhere.

### Encryption in transit

- Public domains terminate TLS at Railway's edge with managed certificates. Redirect HTTP to HTTPS in the app and set HSTS once the custom domain is stable.
- Service to service and service to database: the private network (`*.railway.internal`), which is isolated per project and environment and is encrypted between hosts. Do not route internal traffic through public domains.
- Postgres over the public TCP proxy (local tools, external services) must use TLS: `sslmode=require` (libpq) or `ssl="require"` (asyncpg). Prefer `railway connect postgres` over SSH.

### Encryption at rest

- Database and service data sit on Railway volumes. Check Railway's current security documentation for its disk-encryption guarantees and do not rely on them alone for sensitive fields.
- Encrypt sensitive columns in the app (OAuth tokens, API keys users give you, personal data) with an authenticated cipher (AES-GCM or Fernet) and a key from a sealed variable (`FIELD_ENCRYPTION_KEY`). Store a key version with each value so you can rotate (decrypt with any known key, encrypt with the newest).
- Backups contain the same data. Restrict who can restore or download them.

### Least-privilege tokens

- CI deploys use a **project token** (`RAILWAY_TOKEN`), created in project settings and scoped to one project and environment. Store it as a CI secret.
- An **account or workspace token** (`RAILWAY_API_TOKEN`) can touch every project you can. Use it only where you must manage several projects, never in a single app's CI.
- Remove workspace members and tokens you no longer use.

### Keep internal services private

- Only services browsers or third parties must reach get a public domain. `worker`, cron, internal APIs, Postgres, and Redis get none.
- Audit and remove stray exposure:

  ```bash
  railway domain list --service worker --json
  railway domain delete worker-production.up.railway.app --service worker --yes
  railway tcp-proxy list --service Postgres --json
  railway tcp-proxy delete <tcp-proxy-id> --service Postgres --yes
  ```

- An internal API that must stay reachable from `web` still authenticates requests (a shared secret header or signed token); the private network is not authorization.
- Admin surfaces get their own service or origin, their own login, and no shared cookies with the main app.

## 8. Deploy and verify

### Deploy

- GitHub-connected services deploy on push to their branch (after CI, if "Wait for CI" is on).
- Local upload: `railway up --service backend --environment staging --detach -m "summary"`. It returns before the deployment is healthy; verify as below.
- Rebuild the current source: `railway redeploy --service web --environment production --from-source --yes`. Same image again: `railway redeploy --service web --environment production --yes`. No rebuild: `railway restart --service web --environment production --yes`.

### Verify after merge

Run this for every service whose watch paths the merge touched.

```bash
SHA=$(git rev-parse origin/main)            # or the merge commit
SVC=backend; ENV=production; URL=https://api.example.com

railway deployment list --service "$SVC" --environment "$ENV" --limit 1 --json | jq '.[0]'   # see the field names once

# 1. Wait for a SUCCESS deployment holding SHA or a descendant of it.
DEPLOY_ID=""
for i in $(seq 1 60); do
  railway deployment list --service "$SVC" --environment "$ENV" --limit 10 --json \
    | jq -r '.[] | [.id, .status, (.meta.commitHash // .commitHash // "")] | @tsv' > /tmp/deploys.tsv
  while IFS=$'\t' read -r id status commit; do
    [ "$status" = SUCCESS ] && [ -n "$commit" ] || continue
    if [ "$commit" = "$SHA" ] || git merge-base --is-ancestor "$SHA" "$commit" 2>/dev/null; then
      DEPLOY_ID=$id; break
    fi
  done < /tmp/deploys.tsv
  [ -n "$DEPLOY_ID" ] && break
  head -n 3 /tmp/deploys.tsv
  sleep 20
done
echo "serving deployment: ${DEPLOY_ID:-none}"

# 2. Healthcheck through the public domain.
curl -sS -o /dev/null -w '%{http_code}\n' --max-time 20 "$URL/healthz"

# 3. Scan the new deployment for 2-3 minutes.
railway logs "$DEPLOY_ID" --service "$SVC" --environment "$ENV" --since 3m --lines 1000 --json \
  | grep -E -i 'QueuePool|timed out|Traceback|"level":"error"' | head -50
railway logs --http --service "$SVC" --environment "$ENV" --status 500..599 --since 3m --lines 100
```

Repeat step 3 after another two minutes; bounded `--since/--lines` queries return instead of streaming.

- Newest row SKIPPED: your commit did not touch this service's watch paths. Confirm with `git diff --name-only <prev>..$SHA`; the SUCCESS row before it is what serves.
- A newer commit already deployed: SUCCESS on a descendant counts.
- Join the serving deployment id to its build log and healthcheck result. The newest status alone may not be the process taking traffic.
- Then exercise the changed route or screen on the live URL. A green healthcheck does not prove the feature.
- Nothing SUCCESS after the wait: go to section 9. Never report "deployed" from the merge time.

### Fix forward

- A failed build or healthcheck does not replace the serving deployment, so users keep the previous release while you fix the cause.
- A revert drops the good parts of the change too, a migration revert means a downgrade on production data, and reverts tend to be re-landed with the same bug.
- Revert only when the broken release is serving, users are hurt now, and the fix is not minutes away. Then re-land with the fix and a test that would have caught it.
- For an immediate rollback without a commit, redeploy the last good deployment from the dashboard (owner approval), then fix forward on top.

### Clean up

```bash
jobs -l                                   # shell jobs you started
pgrep -af 'railway (logs|deployment)'     # long-running CLI calls
kill <pid>                                # only processes you started
rm -f /tmp/deploys.tsv
```

Prefer bounded loops and `--since/--lines` over streaming `railway logs`. Delete one-shot scheduled checks after they report.

## 9. Troubleshooting

```bash
railway deployment list --service backend --environment production --limit 5 --json | jq '.[] | {id, status}'
railway logs <DEPLOYMENT_ID> --service backend --environment production --build --lines 300
railway logs <DEPLOYMENT_ID> --service backend --environment production --lines 300
railway logs --latest --service backend --environment production --lines 300      # even if failed or building
```

Read the first real error, not the last line. Reproduce locally with the same command Railway ran (the Docker build, `npm run build`, or the pre-deploy script) before pushing the fix.

| Symptom | Cause | Fix |
|---|---|---|
| `Type error:` in `next build` / `tsc` | Type error in app or test files | `npx tsc --noEmit && npm run build` locally, fix, push |
| `COPY failed` / file not found | Path outside the service build context | Fix root directory or `dockerfilePath`; add the path to `watchPatterns` |
| Cache mount error on Metal | Mount id lacks `s/<service-id>-` | Prefix the mount id |
| Build cannot reach the database | Private network is runtime-only | Move DB work to `preDeployCommand` or startup |
| `Multiple head revisions` in pre-deploy | Two Alembic heads | `alembic merge heads`, push |
| Pre-deploy fails on a migration | Bad migration, or non-nullable column on existing rows | Fix the migration; add a default or backfill |
| Healthcheck fails, 404 on `/healthz` | Route missing or wrong path | Add the route; match `healthcheckPath` |
| Healthcheck fails, 503 | Missing required variable | Set it (with approval); it redeploys |
| Healthcheck times out while booting | Startup slower than `healthcheckTimeout`, or not listening on `$PORT` | Raise the timeout, bind `::` on `$PORT`, move warmup off startup |
| `ImportError` / circular import at boot | Import-order bug | Fix; add `python -c "import app.main"` to pre-deploy |
| SUCCESS, then `CRASHED` | Runtime error on first request or job | Runtime logs for that deployment id |
| Every request 500, `QueuePool limit … timed out` | Pool too small for in-process jobs plus requests | Section 3: take the fair share |
| `too many connections` / `remaining connection slots are reserved` | Sum of pools above `max_connections` | Recompute shares, raise `max_connections`, or add PgBouncer |
| `ENOTFOUND` / `getaddrinfo` on `*.railway.internal` | Calling the private host from the browser, the build, or a laptop; or app not bound to `::` | Server-side calls only, at runtime; bind `::` |
| Queue stops, no job summaries | A job hung | Section 5: per-job timeout |
| Jobs or locks vanish under memory pressure | Redis eviction policy | `noeviction` for queues and locks |
| Frontend shows an old API URL | `NEXT_PUBLIC_*` baked at build | Rebuild (`redeploy --from-source`) |
| CORS error in the browser | Origin not in the allowlist, or `http` vs `https` | Add the exact HTTPS origin |
| Custom domain has no certificate | DNS record missing or proxied | `railway domain status <domain>`; fix DNS |
| Deploy shows SKIPPED | Commit outside watch paths | Expected; or widen `watchPatterns` |

## 10. Checklist

Setup:

- [ ] Each service has a root directory, config file, `watchPatterns`, and a pinned builder.
- [ ] App services listen on `::` and `$PORT`; every HTTP service has `/healthz` and a `healthcheckTimeout` above its real cold start.
- [ ] Only browser-facing services have public domains; databases have no TCP proxy.
- [ ] Database backups (PITR or scheduled) are on, and one restore was tested into a new service.

Before merge:

- [ ] Every path the image reads is in the build context and in `watchPatterns`.
- [ ] `alembic heads` prints one head; the migration works with old code still serving.
- [ ] Frontend: `npx tsc --noEmit && npm run build` passed locally.
- [ ] New variables and job flags are set in production (with approval), sealed if secret.
- [ ] New background jobs have a per-job timeout and log their flag state at startup.
- [ ] Pool size per process equals its fair share of `max_connections`.

After merge:

- [ ] For each touched service, a SUCCESS deployment holds the merge SHA or a descendant.
- [ ] `/healthz` on the public domain returns 200.
- [ ] Two to three minutes of the new deployment's logs show no 5xx, pool timeouts, or tracebacks.
- [ ] The changed route or screen works on the live URL.
- [ ] Failures were fixed forward, with a test for the cause.
- [ ] Every poller and log stream you started is stopped.
