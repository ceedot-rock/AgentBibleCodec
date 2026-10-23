# Chapter 22 — Evaluation and Measurement

## Principle

Agent programs improve by measurement or merely change. Evaluation is a scientific instrument pointed at your own system, and it obeys the rules of instruments: a frozen test set, a defined metric, pre-registered comparisons, and a noise floor below which differences are not differences. Without those, "improvement" is a narrative genre.

## Substance

**The benchmark is the contract.** SWE-bench (after Jimenez et al., 2024) defined the modern shape: real repository issues, a fixed base commit, patches applied and judged by test execution — resolved if and only if the fail-to-pass set passes and the pass-to-pass set holds. Benchmarks earn trust through frozen membership, hermetic execution (fresh environment per task, no network leakage), and a resolution definition that cannot be negotiated per task. Contamination — benchmark items or their solutions leaking into training data or prompts — converts the instrument into a mirror; guarding the split (a frozen *holdout* never tuned on, reserved for confirmation reads) is an integrity rule, not a preference.

**Pre-registration for agent experiments:** before the run, write down the primary metric (usually resolution rate), the secondaries (cost per task, calls, per-task flips), the single variable being changed, and the ship criterion. One variable per comparison — two changes and one number yields two suspects. Differences must clear a **signal threshold** sized to the bench: on n=20, one task is 5 percentage points and flips by chance constantly; a working rule is ≥2 tasks before a difference is treated as signal at that scale, scaling proportionally at other n. A one-task difference is recorded as *no detectable effect* — which is a real result, distinct both from "proven zero" and from "it works."

**Cost is a metric.** Resolution at unbounded cost is a demo. Report calls, tokens, wall-time, and dollars per resolved task alongside the rate; a configuration that wins +1 task at 3× cost may be a trade, or a loss, but it is not a free win. Also report **engagement metrics** for internal mechanisms (Chapter 19): candidates sampled, gates fired, repairs attempted — the numbers that distinguish "the idea failed" from "the idea never ran."

**Variance is real:** sampling temperature, task ordering, and environment jitter make single runs anecdotes. Repeat decisive comparisons, use identical configurations for control and treatment (hash them; "identical except" must be provable), and log every tried configuration with its outcome — an unrecorded tune is a rumor the next engineer will pay to re-test.

## Worked example

A team adds a sophisticated multi-step prompt protocol and measures +1 task on their 20-task bench (10% → 15%). Headline written: "protocol improves resolution 50% (relative)." The measured truth: one flip, inside noise at n=20; the protocol also cost 30% more calls per task. The disciplined record reads: *no detectable effect; cost up; do not ship on this evidence; if the idea matters, power the comparison properly (larger bench or repeated runs).* Programs that ship on one-flip evidence accumulate a codebase of superstitions, each defended by a number that never replicated.

## Failure mode

Tuning on the holdout (it becomes training data and the final read becomes fiction); retrospective criteria (choosing the metric after seeing results); comparing across changed benches, budgets, or scorers; reporting rates without denominators ("improved 50%" of a 2-task base); and ignoring cost until the invoice teaches it.

## Rule

> **Rule.** No configuration ships on a difference below the pre-registered signal threshold for the bench size, and no improvement is claimed from a comparison in which anything but the named variable differed. A result that a same-configuration re-run cannot reproduce within threshold is reclassified as noise in the same record that reported it.
