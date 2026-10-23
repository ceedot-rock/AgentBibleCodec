# Chapter 27 — Principles of Practice

The closing chapter collects the book's rules as general principles of agentic coding practice. Each is stated so it can be checked — a principle that no evidence could embarrass is a slogan, and this book has tried to contain none.

## On the loop

1. **An agent is a loop, not a model.** Attribute every failure to a named component — observation, state, tool interface, budget, stopping rule — before attributing it to the model.
2. **No open-loop runs.** Every action is preceded by a justifying observation and followed by a judging one.
3. **The world is the ground truth.** Observations returned by tools outrank the model's expectations, plans, and memory, in that order, every time they conflict.

## On enforcement

4. **Choreography is not enforcement.** A check the model invokes on itself is advice. Guarantees live in code the model cannot skip.
5. **Name the enforcement level** of every claimed discipline, and show the trace evidence that it engaged. No engagement evidence, no claim.
6. **Fail closed.** When a check cannot run, the answer is denial and a report of *absent* — never a silent pass.

## On verification

7. **Executed proof or it doesn't count.** Selection — of patches, checkpoints, training data — is by measured outcome, never by confidence, order, or elegance.
8. **Name the path.** A claim covers the exact artifact, version, and code path measured. A claim found to describe a different path is withdrawn, in the same document, at the same prominence.
9. **Read the artifact, not the status.** Wrappers, summaries, and success flags are claims about evidence, not evidence.
10. **Enumerate targets before work.** What must turn green, what must stay green — named first, or verification is theater.

## On measurement

11. **Frozen benches, frozen criteria.** The test set, the metric, and the ship threshold are fixed before the run; the holdout is never tuned on.
12. **One variable per comparison,** and differences below the noise threshold are recorded as *no detectable effect* — a real result, not a failed one.
13. **Cost is a metric.** Every improvement is reported with its price in calls, tokens, time, or money.
14. **Log every tried configuration.** An unrecorded tune is an anecdote; a recorded search is an asset.

## On training

15. **Provenance or exclusion.** Training data carries executed evidence and a checkable manifest; synthesized correctness is labeled permanently or rejected.
16. **Never train on the test.** Benchmark and holdout material is excluded by identity and by content, and the exclusion is asserted, not assumed.
17. **Verify the training actually trains.** One optimizer step, one census of changed weights, before the expensive run — a frozen model with beautiful logs is still frozen.

## On accountability

18. **Mandate before action, receipt during, seal after.** Authority is bounded in advance and checked at the point of action; the record binds the artifact to the run.
19. **State every guarantee with its attacker.** What the record proves, against whom, and the rewrite it cannot detect — published, not discovered.
20. **The human's gates are the human's.** Identity, payment, legal attestation, and irreversible publication stop for the human — prepared, consolidated, and never routed around.

## On the craft itself

21. **Claims match evidence** — in code comments, in reports, in benchmarks, in training data. This is the master principle; every other rule in this chapter is its corollary in one domain.
22. **Corrections are data.** An error found, named, mechanistically explained, and converted into a class-level countermeasure is the highest-value artifact a practice produces. The appendix that follows exists to train exactly that motion.
