# Appendix A — Errata Exercises: Claims, Flaws, Corrections

**About this appendix.** Every entry below is a **constructed teaching exercise**: an invented claim of the kind commonly made about agentic coding and computing, followed by its flaw, its correction, and the evidence or reasoning that settles it. These are not reports of real incidents; they are training material for the *motion* of correction — read a confident claim, find the mechanism of its wrongness, state the true claim crisply, and name the evidence. A reader (human or model) who can perform this motion on unseen claims has learned the book's master skill.

---

## Exercise 1 — "Our fine-tune ran five epochs, so the model learned the task."

**Claim.** A training run completed its schedule; therefore the model was trained.

**Flaw.** Completion of a schedule proves only that steps were *executed*, not that weights *changed*. If the training precision cannot represent the updates — in pure float16, an AdamW update near learning rate 2×10⁻⁵ is smaller than the spacing between representable values near typical weight magnitudes, and rounds back to the identical stored value — the model after five epochs is bit-for-bit the model before them. Loss logs print normally throughout, because the loss is computed from the (unchanged) model.

**Correction.** A run trains a model only if its weights measurably change. Establish this with a one-step census (one optimizer step; count changed weights — ≈all in fp32, a small fraction in broken fp16) and with end-to-end evidence (an evaluation delta against the untrained control). Correct precision practice: fp32 master weights and optimizer state, lower-precision arithmetic only inside autocast.

**Evidence.** The census is decisive and cheap: identical batch, identical loss in both precisions, and a changed-weight fraction that differs by an order of magnitude between them. A flat metric at exactly chance across every epoch is the field signature of the frozen case.

## Exercise 2 — "The submission was confirmed — the page said 'Thank you.'"

**Claim.** An automated submitter reports success because the result page contained a success phrase.

**Flaw.** The phrase matched was part of the form's own static copy, present on the page whether the submission succeeded, failed validation, or was never sent. A confirmation detector that scans page prose measures the page's marketing, not the transaction's outcome.

**Correction.** A submission is confirmed only by system state: the submission appears in the system's own records (a submissions list, an identifier, a status field) read back after the fact. Outcomes that cannot be so verified are reported as *clicked–unverified* — a distinct, honest state.

**Evidence.** Read-back: query the system's record of submissions. If the item is absent, the prose was lying by coincidence; if present with an identifier, the confirmation is real. The two states are distinguishable in every case — the exercise's claim survives only where nobody looked.

## Exercise 3 — "The gate blocks unverified patches."

**Claim.** A pre-submit gate implemented as a tool the agent is instructed to call "blocks" patches that lack test evidence.

**Flaw.** A tool the model chooses to invoke cannot block anything. The model can omit the call, call it after submitting, or call it and proceed despite its verdict. What exists is a *request*, enforced by nothing; calling it a block mistakes choreography for mechanism.

**Correction.** Blocking requires enforcement outside the model's control: the submission action itself refuses until the precondition is verifiably met (test evidence bound to the current artifact's hash). Where the platform offers no such hook, the honest description is "a cooperative protocol, mitigated by artifact-binding" — and the system's guarantees must be restated at that level.

**Evidence.** One completed run whose trace shows a submission with no preceding gate verdict falsifies the claim as stated — regardless of that run's outcome.

## Exercise 4 — "The benchmark improved 50% after our change."

**Claim.** Resolution rose from 2 to 3 tasks on a 20-task benchmark — "a 50% improvement."

**Flaw.** Two compounding misstatements: the relative framing of a tiny base (1 task = 5 points absolute, 50% relative), and the treatment of a one-task flip as signal when run-to-run variance at n=20 routinely flips individual tasks. The claim is arithmetic wearing a lab coat.

**Correction.** Report absolute numbers with denominators (2/20 → 3/20), state the pre-registered signal threshold for the bench size (≥2 tasks at n=20), and record sub-threshold differences as *no detectable effect* pending a powered comparison.

**Evidence.** Re-run the control under the identical configuration: if its score also moves by a task between repeats, the noise floor is measured, and the claim's "improvement" is inside it.

## Exercise 5 — "Hash-chained receipts prove what the agent did."

**Claim.** Because each receipt commits to its predecessor's hash and the final seal binds the artifact, the ledger *proves* the agent's conduct.

**Flaw.** An unsigned chain proves internal consistency only. An attacker able to rewrite the ledger can recompute every link and the seal; the verifier accepts the rewritten history because every check it can perform is a check the rewrite satisfies. The claim omits its attacker model — the word "proves" is doing unlicensed work.

**Correction.** The chain detects *partial* tampering (edits, deletions, reordering, truncation) by parties who cannot or do not rewrite the whole. Authenticity requires a signature from a key the agent cannot hold, or an external anchor (periodically published ledger heads) that makes total rewrite publicly evident. State both the guarantee and the undetectable rewrite, or the claim is oversold.

**Evidence.** Perform the rewrite in a test: alter a receipt-level fact, recompute the chain and seal, and present it to the verifier. Acceptance is the measured limit of the unsigned mechanism — demonstrable in an afternoon, decisive forever.

## Exercise 6 — "We measured the library: recursion to depth 20,000 overflows the stack."

**Claim.** A probe program using the library's serialization API recursively overflows at depth 20,000, so deeply nested values are a crash risk for stored data.

**Flaw.** The probe measured a *generic* path — raw recursion in the probe's own code — not the library's production path, which enforces a container-depth cap (returning clean errors) at a far lower depth. Values beyond the cap cannot be constructed through the production API at all, so the claimed stored-data scenario cannot occur. The measurement was real; its subject was a different system than the one claimed.

**Correction.** Behavioral claims bind to the exact path measured: library version, entry point, and enforcement points on that path. When a production cap intervenes, the claim must be restated to whatever survives the cap (e.g., in-execution consumers without the cap, if any exist and are demonstrated) — or withdrawn.

**Evidence.** Trace the production call path and find the enforcement; demonstrate construction of a beyond-cap value *through the production API* or concede it cannot be built. The cap's presence in the shipped source settles which.

## Exercise 7 — "Adding the discipline prompts didn't help, so discipline doesn't work."

**Claim.** An agent given explicit discipline instructions (verify before submitting, enumerate targets, self-examine) scored no better than baseline; discipline is therefore ineffective for agents.

**Flaw.** The experiment varied the *delivery channel* (prompt text) and concluded about the *concept*. Discipline-as-exhortation is one implementation; discipline-as-harness-enforcement was never in the trial. Additionally, at small n the result is "no detectable effect," not "proven zero" — the conclusion overclaims in two directions at once.

**Correction.** Scope conclusions to the implementation measured: "discipline delivered as prompt text showed no detectable effect at n=20 on this model." The harness-enforced variant is a separate, untested hypothesis until a trial installs enforcement outside the model's discretion and measures engagement in traces.

**Evidence.** In the trial's own traces, check whether the instructed behaviors occurred (targets enumerated? self-exams present?). If the behaviors are absent from the traces, the trial measured instruction-following, not discipline — and the trace check, not the score, is what reveals it.

## Exercise 8 — "Compression beat the entropy bound on our corpus."

**Claim.** A new codec compresses a test corpus to fewer bits than the source's estimated entropy — "beyond Shannon."

**Flaw.** Lossless compression of a source below its true entropy is impossible (Shannon, 1948); an apparent violation means the entropy was misestimated (usually: the estimator assumed independence, or the "corpus" was generated by a process with learnable structure the estimator ignored) — or the codec smuggled information (a dictionary trained on the test set, uncounted headers, the decompressor containing the data).

**Correction.** Count *everything* needed to decode: model, dictionary, headers, parameters. Estimate entropy with the strongest available model of the source, and treat "beating entropy" as a bug report against the accounting, never as a result.

**Evidence.** Decode the compressed artifact in a clean environment containing only the counted material. If decoding requires anything uncounted, the claim collapses to arithmetic. Entropy accounting that survives clean-room decoding is the only kind there is.

## Exercise 9 — "The agent fixed the bug — all tests pass."

**Claim.** After the agent's edit, the test suite is green; the bug is fixed.

**Flaw.** "All tests" may exclude the test that demonstrates the bug (it may never have been written), include it only in a form the edit gamed (test modified, assertion weakened, fixture altered), or pass because the bug's trigger wasn't exercised in this configuration. A green suite is evidence about the suite, and about the bug only to the extent the suite's relationship to the bug is established.

**Correction.** The claim requires: a reproduction that failed *before* the edit and passes *after* (same test, unmodified), plus the pre-existing suite green (no regressions), plus protected-file discipline — tests and test configuration were not altered to achieve the pass, or any alteration is declared and justified as a specification change.

**Evidence.** The before/after pair on the identical test is the evidence; a bare after-state is an anecdote. If no failing-before test exists, the honest claim is "the suite passes and the reported symptom is unaddressed by any test" — which is a statement about remaining risk, not about a fix.

## Exercise 10 — "Retries are safe — the API usually processes each request once."

**Claim.** A client retries timed-out requests freely, since duplicates are rare in practice.

**Flaw.** A timeout means the response was lost, not that the request failed — the request may have executed fully. "Usually processed once" under retries means *sometimes processed twice*, and for non-idempotent effects (charges, sends, allocations) the rare case is the catastrophic one. The claim mistakes a frequency statement for a safety property.

**Correction.** Non-idempotent operations carry idempotency keys; the server deduplicates on the key, stored transactionally with the effect. Retries then become safe *by construction*, at any frequency — safety is a property of the mechanism, not of the observed duplicate rate.

**Evidence.** Fault-injection: kill the response path after the server commits but before the client hears, then retry. Count effects. One duplicate falsifies "safe" for the un-keyed design; the keyed design survives the same test by construction.
