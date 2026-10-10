---
name: railway-deployment
description: Use when deploying, configuring, verifying, or debugging apps on Railway, especially a monorepo with several services (for example `backend`, `web`, `worker`) built from one repository. Covers watch paths, CLI linking, healthchecks, migrations on boot, zero-downtime overlap, Postgres pool sizing, background-job timeouts, env vars and flags, frontend production builds, post-merge verification, failed-deploy diagnosis, and fixing forward. Load it before a merge that will deploy, after a deploy fails, or when production returns 5xx after a release.
---

# Railway deployment

A merge is not a release. A release is done when the exact commit is serving, the healthcheck is green, and the logs are clean for a few minutes. This skill is the path from "merged" to "proven live", plus the configuration that keeps that path boring.

Examples use three services from one repo: `backend` (API + migrations + in-process jobs), `web` (Next.js), `worker` (queue consumer). Replace names with yours.

## Rules

1. Prove the deploy holds your SHA. "Latest deployment is SUCCESS" proves nothing if your commit was skipped or a newer one replaced it.
2. Pass `--service` and `--environment` explicitly on every CLI call. The linked context is often a different service or project.
3. Read-only by default. Variables, redeploys, restarts, service config, domains, and deletes change shared production. Get the owner's explicit yes before each write.
4. Fix forward. A failed build or failed healthcheck leaves the old deployment serving, so you have time to fix the cause instead of reverting.
5. Speed over efficiency. When production is broken, take the fastest correct path to green: more pool, more memory, one more replica. Tune for cost later with measurements.
6. Kill every background poller and log tail you start before you finish.

## 1. Monorepo services and watch paths

Each service has a root directory and watch patterns. Railway builds a service only when a commit touches a path that matches its patterns; otherwise the deployment shows **SKIPPED**.

`backend/railway.toml`:

```toml
[build]
builder = "DOCKERFILE"
dockerfilePath = "backend/Dockerfile"   # relative to the service root
watchPatterns = ["backend/**", "shared-schema/**"]

[deploy]
preDeployCommand = "sh scripts/run-migrations.sh"
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
- If the image copies anything outside the service directory (a shared crate, a schema folder, generated files), that path must be in the build context **and** in `watchPatterns`. Otherwise a change there never redeploys the service, or the build fails with a missing file.
- A service whose Dockerfile reads repo-root folders needs `source.rootDirectory=/` and a `dockerfilePath` like `backend/Dockerfile`. Point the service's config-file setting at `/backend/railway.toml`. Moving it back to an isolated `/backend` root silently drops those folders from the context.
- A docs-only or other-service commit yields SKIPPED for this service. That is correct, not a failure. The service still serves the last SUCCESS build.
- CI path filters (`on.pull_request.paths`) follow the same logic. A check that never started is not a pass. Make sure the filters cover every path the image reads.

Check the live service config once before relying on it:

```bash
railway environment config --environment production --json \
  | jq '.services[] | {configFile, source, build: .build | {builder, dockerfilePath, watchPatterns}}'
```

## 2. Link the CLI

Install a current CLI (`npm i -g @railway/cli`); old versions lack `deployment list`. Link per directory, because each checkout or service folder keeps its own link.

```bash
railway whoami --json
cd backend && railway link --project <project> --environment production --service backend
railway status --json                     # confirm project, environment, service
cd ../web && railway link --project <project> --environment production --service web
railway service status --all --json       # every service and its current deployment state
```

Prefer explicit flags over relying on the link in scripts:

```bash
railway deployment list --service backend --environment production --limit 10 --json
railway logs --service backend --environment production --lines 200 --json            # latest deployment, runtime
railway logs <DEPLOYMENT_ID> --service backend --environment production --json        # one deployment, runtime
railway logs <DEPLOYMENT_ID> --service backend --environment production --build --json  # one deployment, build
railway logs --service backend --since 30m --filter "@level:error" --lines 400 --json
```

Always read logs per deployment ID when old and new containers overlap; "latest" can be the one that is still building.

## 3. Healthchecks

- Every service ships its own `/healthz` route in the same app, pinned in source and in `railway.toml`. A 404 on the healthcheck means the route is missing, not that the app crashed.
- `/healthz` is cheap and side-effect free. Return 200 when the process can serve; return 503 with a short reason when a required config is missing (backend URL, signing secret). Do not call slow third parties from it.
- `healthcheckTimeout` is the startup grace period. Railway keeps probing until it passes or the timeout ends, then marks the deploy FAILED and keeps the old one serving. Size it to real cold start: a backend that loads models or warms caches needs minutes (300 s); a Next.js server needs about 30 s.
- A worker with no HTTP port gets no `healthcheckPath`. Prove it with a startup log line and a heartbeat instead.
- `/healthz` is a probe, not a page. Keep it out of navigation and sitemaps.

## 4. Migrations on boot

Run migrations in `preDeployCommand`, not in the start command. Pre-deploy runs once per deploy before traffic moves; the start command runs on every replica and every restart.

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
alembic heads                          # must print exactly one head
rg -n '^revision\s*=' alembic/versions | sort   # revision ids are unique
alembic upgrade head && alembic downgrade -1 && alembic upgrade head   # on a local copy
```

- Two heads (two branches each added a migration) fail `upgrade head`. Merge the heads in the same PR with `alembic merge heads -m "merge heads"`.
- Parent every new revision on the current live head. Keep revision ids short if your `alembic_version` column is `VARCHAR(32)`.
- Rehearse on a production-shaped database (schema built, then stamped, then upgraded), not an empty one. An empty-DB upgrade proves little.
- Migrations must be compatible with the old code still serving during overlap: add columns nullable or with defaults, backfill, switch readers, then drop in a later release.
- Use `NullPool` (or no pool) for the migration process so it holds no idle connections.

## 5. Zero-downtime deploys

With `overlapSeconds` and `drainingSeconds`, Railway starts the new container, waits for its healthcheck, routes traffic to it, keeps the old one alive for the overlap, then sends SIGTERM and allows the drain window.

- Old and new code run at the same time for up to `overlapSeconds`. API, database schema, cookies, and queued job payloads must work for both versions.
- Handle SIGTERM: stop taking new jobs, finish or requeue in-flight work, close the pool. For uvicorn, `--timeout-graceful-shutdown` below `drainingSeconds` (for example 25 vs 30).
- Jobs claimed by a container that was killed must be recoverable: leases with expiry, and a startup sweep that requeues or fails orphans.
- Session secrets and signing keys must accept both old and new values across a deploy, or every user is signed out.
- Do not merge right before a time-critical scheduled job. A redeploy restarts in-process schedulers.

## 6. Database connection pool sizing

Every process opens its own pool. Size each process to its fair share of the server's connections, minus headroom:

```
usable   = max_connections - superuser_reserved_connections - reserved_connections - headroom
per_proc = usable // (replicas * worker_processes_per_replica)
pool_size = per_proc,  max_overflow = small (0-2)
```

- Read `max_connections` and the reserved settings from Postgres at startup rather than hardcoding them:

  ```sql
  SELECT current_setting('max_connections')::int,
         current_setting('superuser_reserved_connections')::int
         + COALESCE(current_setting('reserved_connections', true), '0')::int;
  ```

- `headroom` (about 5) covers migrations, admin shells, and other services sharing the database.
- Count worker processes from the launcher (`WEB_CONCURRENCY`, your `--workers` value), not from the CPU count.
- **Never cap the pool low.** A process that also runs in-process background dispatchers, schedulers, or queue drains lets them hold connections. With a small cap, those tasks take every slot, request handlers wait for `pool_timeout`, and every request returns 500 with `QueuePool limit of size N overflow M reached, connection timed out`. Take the full fair share. A floor is a warning threshold for an undersized database, not a cap.
- Set `pool_timeout` below the proxy request timeout, so a starved request fails with a clear error instead of a gateway timeout. Turn on `pool_pre_ping` and a `pool_recycle` (for example 1800 s).
- Pools open lazily, so the overlap window rarely doubles real usage. If it does, raise `max_connections` or headroom; do not shrink pools.
- Log the computed size at startup (`db_pool_sized max_connections=… processes=… pool_size=…`) so a 500 storm can be checked against it in one log search.
- Never share one session or connection across concurrent tasks, and never hold a transaction open across a slow external call.

## 7. Per-job timeouts

A single-instance queue or scheduler runs jobs one after another. One job that never returns freezes everything behind it until the process restarts.

- Wrap every job type, and the finalize step, in a hang timeout (`asyncio.wait_for(job(), timeout=…)`, a thread with a deadline, or the queue library's job timeout).
- Bound every provider call: pass a request timeout and cap retries, so the job timeout is a backstop, not the normal path.
- On timeout: log `job`, `run_id`, `duration_ms`, mark the job failed or retryable, release its lease, continue the queue.
- Prevent overlapping ticks: a scheduled job that is still running must not start again. On Railway cron services, "maximum number of running instances reached" every interval means a run never exited.
- Test it: a worker test with a job that never returns must still let the next job run.

## 8. Env vars, secrets, and job flags

```bash
railway variable list --service backend --environment production --json   # values are sensitive; do not paste them
railway variable set KEY=value --service backend --environment production  # owner approval first
```

- Secrets live only in Railway variables (or a shared variable group). Never in the repo, Dockerfile, build args that end up in image layers, logs, PR text, or chat.
- Reference other services with Railway variable references (`${{Postgres.DATABASE_URL}}`) and private networking hostnames instead of copying values.
- Validate required config at startup and fail with a clear message, or report it as a 503 from `/healthz`. Reject unsafe values in deployed environments (non-Postgres `DATABASE_URL`, `*` CORS origins, non-HTTPS origins).
- `NEXT_PUBLIC_*` values are baked in at `next build`. Changing them needs a rebuild, not a restart. Keep server-only secrets out of `NEXT_PUBLIC_*`.
- Job feature flags that default off are a trap: the code ships, the flag is never set in production, and the job silently never runs. For each new flag, either default it on where it should run, or add the variable in production as part of the release. Log the flag state at startup (`job_disabled job=… flag=…`) and check it after deploy.
- Do not let an old or legacy flag disable a job that a newer setting turned on. One owner per flag.

## 9. Building the frontend image

`next build` type-checks the whole app, including `*.test.ts` files that are in the `tsconfig` include. Unit tests (Vitest, Jest) do not type-check. Green tests plus a red build is common.

Before merging any change to `web/`:

```bash
cd web
npm ci
npx tsc --noEmit
npm run build
```

Or build the exact image Railway will build:

```bash
docker build -f web/Dockerfile web/       # use the same context as the service root
```

- Match the Next.js output mode to the start command. `output: "standalone"` needs `node server.js` plus copied `.next/static` and `public/`.
- Make `.next/cache` writable by the runtime user; standalone still writes ISR entries there.
- Use relative imports in `next.config.ts`; path aliases may not resolve at config load.
- Railway Metal requires cache mount ids of the form `id=s/<service-id>-<target>`. Without that prefix, builds with `RUN --mount=type=cache` fail.

## 10. Verify after merge

Run this for every service whose watch paths the merge touched.

```bash
SHA=$(git rev-parse origin/main)          # or the merge commit
SVC=backend; ENV=production; URL=https://api.example.com

# 1. Wait for a SUCCESS deployment that holds SHA or a descendant of it.
for i in $(seq 1 60); do
  railway deployment list --service "$SVC" --environment "$ENV" --limit 10 --json > /tmp/deploys.json
  jq -r '.[] | [.id, .status, (.meta.commitHash // .commitHash // "")] | @tsv' /tmp/deploys.json > /tmp/deploys.tsv
  DEPLOY_ID=""
  while IFS=$'\t' read -r id status commit; do
    [ "$status" = SUCCESS ] || continue
    if [ "$commit" = "$SHA" ] || git merge-base --is-ancestor "$SHA" "$commit" 2>/dev/null; then
      DEPLOY_ID=$id; break
    fi
  done < /tmp/deploys.tsv
  [ -n "$DEPLOY_ID" ] && break
  grep -q FAILED /tmp/deploys.tsv && head -n 3 /tmp/deploys.tsv
  sleep 20
done
echo "serving deployment: ${DEPLOY_ID:-none}"

# 2. Healthcheck through the public domain.
curl -sS -o /dev/null -w '%{http_code}\n' --max-time 20 "$URL/healthz"

# 3. Scan the new deployment's logs for 2-3 minutes.
timeout 180 railway logs "$DEPLOY_ID" --service "$SVC" --environment "$ENV" --json \
  | grep -E -i '" 5[0-9]{2} |status.?5[0-9]{2}|QueuePool|timed out|Traceback|error' | head -50
```

- If the newest row for your service is SKIPPED, your commit did not touch its watch paths. Confirm with `git diff --name-only <prev>..$SHA` and check that the SUCCESS row before it is the expected build.
- If a newer commit already deployed, a SUCCESS on a descendant counts: `git merge-base --is-ancestor $SHA <deployed_sha>`.
- Join the serving deployment ID to its build log and healthcheck result. Newest status alone may not be the process taking traffic.
- Check the custom domain, not the `*.up.railway.app` host, if users reach the app through the custom domain.
- Then exercise the changed route or screen on the live URL. A green healthcheck does not prove the feature.
- If nothing is SUCCESS after the wait, go to section 11. Do not report "deployed" from the merge time.

## 11. Diagnose a failed deploy

```bash
railway deployment list --service backend --environment production --limit 5 --json | jq '.[] | {id, status}'
railway logs <FAILED_ID> --service backend --environment production --build --json | tail -n 200
railway logs <FAILED_ID> --service backend --environment production --json | tail -n 200
```

Read the first real error, not the last line. Match it:

| Symptom in logs | Cause | Fix |
|---|---|---|
| `Type error:` during `next build` / `tsc` | Type error in app or test files | Run `npx tsc --noEmit && npm run build` locally, fix, push |
| `COPY failed` / file not found | Path outside the service build context | Fix root directory or Dockerfile path; add path to watch patterns |
| Cache mount error on Metal | Cache mount id lacks `s/<service-id>-` prefix | Prefix the mount id |
| `Multiple head revisions` in pre-deploy | Two Alembic heads | `alembic merge heads`, push |
| Pre-deploy fails on a migration | Bad migration or non-nullable column on existing rows | Fix the migration; add a default or backfill |
| Healthcheck fails, logs show 404 on `/healthz` | Route missing or wrong path | Add the route; match `healthcheckPath` |
| Healthcheck fails, logs show 503 | Missing required variable | Set the variable (with approval), redeploy |
| Healthcheck times out, app still booting | Startup slower than `healthcheckTimeout` | Raise the timeout or move warmup off the startup path |
| `ImportError` / circular import at boot | Import-order bug | Fix; add `python -c "import app.main"` to pre-deploy |
| Crash loop after SUCCESS, then `CRASHED` | Runtime error on first request or job | Read runtime logs for that deployment ID |
| Every request 500, `QueuePool limit … timed out` | Pool too small for in-process jobs plus requests | Section 6: take the fair share |
| Queue stops, no job summaries | A job hung | Section 7: per-job timeout |

Reproduce locally with the same command Railway ran (the Docker build, `npm run build`, or the pre-deploy script) before pushing the fix.

## 12. Fix forward

- A failed build or healthcheck does not replace the serving deployment. Users still get the previous release, so fix the cause and push.
- A revert drops the good parts of the change too, and a revert of a migration means a downgrade on production data. Reverts also tend to get re-landed with the same bug.
- Revert only when the broken release is serving, users are hurt now, and the fix is not minutes away. Then re-land with the fix and a test that would have caught it.
- If you need an immediate rollback without a new commit, redeploy the last good deployment from the dashboard or `railway redeploy` (owner approval), then fix forward on top.

## 13. Clean up

Pollers and log tails outlive the task unless you stop them.

```bash
jobs -l                                   # shell jobs you started
pgrep -af 'railway (logs|deployment)'     # long-running CLI calls
kill <pid>                                # only processes you started
```

- Prefer bounded loops (`for i in $(seq 1 60)`) and `timeout 180` on log tails, so nothing runs forever.
- Delete one-shot scheduled checks after they report.
- Remove scratch files (`/tmp/deploys.*`) you wrote.

## Checklist

Before merge:

- [ ] Every path the image reads is in the build context and in the service's `watchPatterns`.
- [ ] `alembic heads` prints one head; the migration works with old code still serving.
- [ ] Frontend: `npx tsc --noEmit && npm run build` passed locally.
- [ ] New variables and job flags are set in production, or will be as part of the release (with approval).
- [ ] New background jobs have a per-job timeout and a startup log of their flag state.
- [ ] `/healthz` exists for each HTTP service and `healthcheckTimeout` covers real cold start.

After merge:

- [ ] For each touched service, a SUCCESS deployment holds the merge SHA or a descendant.
- [ ] `/healthz` on the public domain returns 200.
- [ ] 2-3 minutes of the new deployment's logs show no 5xx, pool timeouts, or tracebacks.
- [ ] The changed route or screen works on the live URL.
- [ ] Failures were fixed forward, with a test for the cause.
- [ ] Every poller, log tail, and one-shot check you started is stopped.
