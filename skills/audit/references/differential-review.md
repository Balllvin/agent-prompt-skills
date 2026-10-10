# Differential review and variant analysis

Written in our own words from ideas in Trail of Bits' `differential-review` and `variant-analysis` skills (https://github.com/trailofbits/skills, CC-BY-SA-4.0). No text is copied; the ideas are credited here.

## Differential review

Review a change by what it touches, not by how big it is. A two-line diff in an auth check outranks a 400-line rename.

1. **Triage by risk.** Mark the diff high risk when it touches auth, money, order or trading paths, secrets, input parsing, serialization, SQL, file paths, subprocess calls, or permission checks. Everything else starts medium. A "just a refactor" stays high until you show it is behavior-preserving.
2. **Reject the shortcuts.** "Small PR, quick look", "tests pass", "it is only a rename", and "the old code did the same" are not reasons to skim. Tiny diffs have shipped the worst bugs.
3. **Check removed guards.** For every deleted or weakened check (validation, auth, rate limit, error branch), run `git log -S '<guard text>'` or `git blame` on the old line to learn why it existed. A guard removed without its reason being gone is a finding.
4. **Count the blast radius.** For each changed function, count callers with `rg` and name the count in the finding. A change with 40 callers gets a line per distinct caller shape, not a sample.
5. **Diff the contract, not the lines.** Compare inputs accepted, outputs returned, errors raised, and side effects before and after. Any widening is a finding until proven safe.
6. **Report** in the hub's report shape with evidence or label on every line.

## Variant analysis

A confirmed bug is a sample from a pattern. Find the rest before the fix lands.

1. **Name the root shape** in one sentence: the call, the missing check, and the data that reaches it.
2. **Write an exact pattern** (`rg`, ast-grep, or Semgrep) that matches only the known instance. Confirm it hits exactly that one.
3. **Generalize one element at a time**: the function name, then the argument shape, then the file scope. Rerun after each step.
4. **Stop generalizing when more than half the new matches are noise.** Step back to the last precise version.
5. **Triage every match** as vulnerable, safe (say why), or unsure. Unsure goes to a checking agent like any other finding.
6. **Fix every true variant in the same PR**, or list the rest under "Not done" with paths. Pairs with build's "grep every caller".
