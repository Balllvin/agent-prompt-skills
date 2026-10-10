---
name: principle-explain-the-number
description: "Apply before you trust, report, or act on a number you measured. Name what bounds it, and rule out other explanations with a run."
disable-model-invocation: true
---

# Explain the number

A measured number is a claim about a system. Before you trust it, report it, or change code because of it, name what bounds it. Rule out that the run measured something else.

## Why

A failed run still prints a number that looks fine. Errors, a cache that skipped the work, code that never ran, a side left on defaults, and run-to-run noise all do this. If you cannot say why the number is not twice as good, you do not know what you measured.

## Pattern

Ask why not double. Name the resource or code path that bounds the result. A core, a lock, the disk, the network, or the load generator are the usual bounds. Take that bound from a profile or from counters captured during a run. Map it to source. A guess from reading the code is not a limiter.

List what else the number could be measuring. Rule out each explanation with a run, not with a reading of the code. Check errors, skipped or cached work, an untuned side, noise, and a piece too small to matter on the path a user waits on.

Keep the evidence with the number. Record the run count, the spread, and the limiter in the notes or a linked artifact. A reader should be able to check the claim without re-running your memory.

For a performance number, follow [benchmark-checklist](benchmark-checklist.md). For an eval result, ask the same questions of the trials. Did every run do the task? Does the gap hold across trials and models? Does the scenario matter?

You skipped this when the evidence has no run count, no spread, or no named limiter. You also skipped it when the time saved is larger than the time the changed piece took.

This is not [Prove it works](principle-prove-it-works.md). That check asks whether an output is real. This check asks whether a measured number means what you say it means.

Source: cursor/plugins pstack df581122, rewritten.
