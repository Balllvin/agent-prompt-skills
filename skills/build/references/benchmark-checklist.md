---
name: benchmark-checklist
description: "Vet a performance measurement before you report it or act on it. Use when you run a benchmark or report a speedup or regression you measured."
disable-model-invocation: true
---

# Benchmark checklist

Use this when you produce a performance number. A pull request before and after, a regression claim, a hillclimb loop, or a library or config choice all count. [Explain the number](principle-explain-the-number.md) says why. Answer each question below with evidence from a run. A guess about the code is not an answer.

For a quick ballpark the user asked for, one run is enough. Still check questions 4 and 7. Say that it is one run. Skip the rest unless that run looks wrong. A choice between options is never a ballpark.

## Before you run anything

Write the claim you expect to ship, in the words you would ship. The questions test that sentence.

Read the measurement script. Note what it times, what it counts, and what it ignores.

Check the load average with `uptime`. Check the core count with `sysctl -n hw.ncpu` on macOS, or `nproc` on Linux. If the machine is busy, find what is running. If you cannot stop it, alternate the sides so both see the same noise. Say so in the report.

## The questions

1. Why not double? Name the limiter. Profile in a run you do not report. Profilers and tracers slow the work down. Watch CPU per process with `top`. Use a profiler for that runtime. On Linux, `perf` and `strace -c` show cycles and syscall counts. On macOS, sample the process. Then map the hot spot to source. Watch the load generator too. If it saturates first, you measured the load generator. If a change did not move the number, the limiter explains why. Find it before you call the change useless.
2. Was it tuned? Run every side the way production runs it. Use release builds, production flags, production env, and the same versions and data. Match batching, transaction settings, connection pools, and cache warmth to production. If one side runs on defaults, you compared configurations, not implementations. A limiter that is a setting means that side is untuned. A commit per row, a debug build, and a missing index are settings. Tune it and measure again before you pick a winner. If you cannot tune it, do not pick a winner from that run. Narrowing the claim to today's settings does not fix this when the user is choosing what to adopt. They adopt the option, not today's settings.
3. Did it break limits? Do the arithmetic. Compare bytes per second with disk and network bandwidth. Compare operations per second, times the cost per operation, with the cores you have. Compare the time saved with the time the changed piece took. A piece that takes 10% of the run can make the run at most about 11% faster if you remove it. A result past a limit means the run measured something other than the work. A cache, a no-op, or a bug are the usual causes.
4. Did it error? Count failures and non-success responses. Check that the outputs are correct, not only present. Errors are not successes. Rejections are often fast. Timeouts and retries are slow. If the script does not count errors, add the count.
5. Does it reproduce? Run each side at least 5 times. Alternate the sides so warmup, lazy init, caches, and drift do not favor one side. Report the median and the range. Treat a gap smaller than the run-to-run variation as no measurable difference. When the call is close, use a rank-sum test or the script's own statistics.
6. Does it matter? Next to any micro result, measure the end-to-end path a user waits on. Use realistic data sizes and concurrency. Report the micro result as a share of the whole. A helper that takes 1% of a request can make the request at most 1% faster, however fast the helper gets.
7. Did it even happen? Confirm the work ran inside the timed region. The request reached the server. The rows were written. The bytes were read. The code used the result. Lazy code and timeouts both print numbers for work that never happened. Generators nobody iterates, promises nobody awaits, and results a JIT can discard are lazy code.

## Report

Lead with the verdict. Use faster, slower, no measurable difference, or inconclusive.

Give the number with its unit, the run count, the range, and the limiter. For example, p50 moved from 41 ms to 33 ms, median of 7 runs per side, range 32 to 35 ms after, bound by JSON parsing on one core.

Call the verdict inconclusive when you claim a difference but cannot name the limiter. Call it inconclusive when a side ran untuned. Call it inconclusive when you could not check questions 4 and 7. Name the gap.

Keep one primary number in the pull request body. [Opening a PR](poteto-mode/playbooks/opening-a-pr.md) owns that briefing. Put the runs, the range, and the limiter evidence in a linked artifact or a notes file.

## Where this sits

[Perf issue](poteto-mode/playbooks/perf-issue.md) finds and fixes slowness. Run this checklist on its baseline before that playbook plans from the baseline. Run it on every number after that.

[Hillclimb](poteto-mode/playbooks/hillclimb.md) loops on one metric. Run this checklist on its measurement script before the script is frozen. After that, the script should print error counts and work counts, so each keep-or-revert checks questions 4 and 7.

Source: cursor/plugins pstack df581122, rewritten.
