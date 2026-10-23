# Chapter 21 — Verification and Selection

## Principle

An agent's outputs are claims. A patch claims to fix the issue without breaking its neighbors; an analysis claims a root cause; a summary claims fidelity to its source. Verification is the discipline of converting claims into evidence *by execution*: the patch is run against the enumerated tests; the root cause is probed by a reproduction; the summary is checked against the text. Nothing is believed because it is plausible — and in agentic systems plausibility is the failure mode, because fluent output is the model's native product.

## Substance

**Enumerate the targets before the work.** For a coding task the target set is explicit: the tests that must turn green (fail-to-pass) and the tests that must stay green (pass-to-pass). Work without a named target set cannot be verified, only admired. The reproduction comes first: a failing test or minimal script that demonstrates the defect *before* any edit — it proves the defect is understood, gives the fix a finish line, and becomes the regression test afterward (Chapter 11).

**Executed proof or it doesn't count.** The selection rule for agent outputs: when multiple candidate solutions exist, keep the one *verified by execution* — not the first, not the most confident, not the most elegant. This operates at three scales: within a run (candidate patches executed against target tests, selection by outcome); across runs (the best *verified* checkpoint is what submits when budget expires); and in training data (Chapter 23: only trajectories with executed proof are admitted). The rule's strength is its indifference to source: a candidate from a weak model that passes outranks a candidate from a strong model that wasn't run.

**Verify the path, not a model of the path.** A recurring verification failure is testing a *representation* of the system — a probe, a reimplementation, a generic version of the library — and reporting the result as a fact about the production system. Versions differ in caps, defaults, and edge behavior; a result about the generic path is a hypothesis about the production path. Where the two can diverge, the divergence must be checked, and claims must name the exact artifact, version, and path they were measured on. A claim found to describe the wrong path is withdrawn, not footnoted — because downstream decisions priced it as true.

**Distrust status channels.** Wrappers lie politely: a job runner reporting "success" for a cell whose subprocess died; a submission system whose confirmation regex matches the page's own marketing text; a monitor that reports a component's *silence* as a pass. Verification means reading the artifact (the output, the exit code, the produced file, the live state) — never the summary of the artifact. A sensor that did not run reports *absent*, not *fine*.

## Worked example

Candidate selection on a bug-fix task: the agent generates three candidate patches from three ranked hypotheses. Candidate 1 is the model's favorite — clean, minimal, confident. Executed: it fails one target test. Candidate 2 is uglier — an extra guard clause — and passes all targets with no regressions. Candidate 3 was never run because budget remained for only two evaluations. The executed-proof rule submits candidate 2 and logs candidate 1's failure as information (the favored hypothesis was wrong — exactly the kind of fact that must survive into the record, because it corrects the *next* task's priors). A workflow that ships candidate 1 on confidence has replaced verification with vibes at the exact point where verification was cheapest.

## Failure mode

Verification theater: running tests that are not the target tests; reporting "tests pass" from a run that executed a stale build; accepting a status field instead of the artifact; verifying a model of the system and reporting it as the system; and the selection failure — keeping the first adequate-looking candidate and never executing the comparison that would have ranked it last.

## Rule

> **Rule.** Every claim an agent emits carries its executed evidence: the exact command or test set, the exact target list, and the observed result, on the exact artifact and version claimed. A claim whose evidence was gathered on a different path than the claim describes is withdrawn in the same document that carried it.
