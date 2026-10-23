# Chapter 25 — Failure Modes of Agentic Systems

## Principle

Agentic systems fail in characteristic ways — not randomly, but along the seams of the loop: observation, state, mechanism, measurement, and communication with the human. A named taxonomy turns post-mortems from storytelling into pattern-matching: when a failure has a name, the next occurrence is recognized in minutes instead of diagnosed in days, and its prescribed countermeasure is already written down.

## Substance

**Failures of observation and state.** *Open-loop drift* — acting on the initial plan while the environment diverges from it. *State loss* (context rot, Chapter 20) — decisive early facts forgotten, re-derived contradictorily. *Phantom success* — an error result read as a success observation, then built upon. *Stale-artifact work* — editing, testing, or verifying a version of the artifact that is not the current one (the diff moved; the evidence didn't).

**Failures of mechanism.** *Silent non-engagement* — a discipline, gate, or sampler that exists in the design and never fires in traces (Chapter 19); its runs are indistinguishable from the mechanism's absence, except in cost. *Choreography mistaken for enforcement* — compliance expected from prose. *Budget cliff* — no defined behavior at exhaustion, so the run's product is lost instead of submitted at its best verified state. *Thrash* — repeated near-identical failed actions (the loop's tell: same call, same error, no new information between attempts) and its twin, *premature convergence* — submitting the first plausible artifact without the verification that would have killed it.

**Failures of measurement and belief.** *Overstated status* — the modal class in every honest incident record: a success state claimed before the artifact was read back (an estimate reported as a measurement; a wrapper's "success" trusted over the crashed subprocess; a document reported complete that was never read to its end). *Verification of a model* — measuring a probe or generic path and reporting it as the production path (Chapter 21). *Contaminated evaluation* — tuning on the holdout, leaking the bench into training (Chapters 22–23). *Referent misread* — executing confidently on the wrong target because a pronoun, a name, or a "submit" had two live referents; the countermeasure is mechanical: name the referent back before any irreversible act.

**Failures of the human interface.** *Approval noise* — asking the human so often, so repetitively, or so indistinguishably that approvals stop meaning anything (the human rubber-stamps; the system's real gate dissolves). *Unbatched interruption* — many small asks where one consolidated decision would do. *Gate misplacement* — asking the human about matters the system can verify itself, while *not* stopping at the irreversible ones (identity, payment, publication) that are genuinely theirs. *Silent waiting* — a run blocked on a human input that was never clearly requested, discovered hours later.

## Worked example

A workflow reports a submission "confirmed" — its checker matched a success phrase in the target page's own marketing copy ("thank you for considering…"), present whether or not anything was submitted. The submission had in fact been rejected for missing fields. Classify before fixing: this is *overstated status* via a *status channel that was never the artifact*. The countermeasure is class-shaped, not instance-shaped: confirmations are read from system state (the submission appears in the system's own list, with an identifier), never from page prose — a rule that then protects every other workflow using the same checker, not just this one. That last step — generalize the fix to the class — is what separates a taxonomy from a pile of anecdotes.

## Failure mode (of failure analysis itself)

Blame-shaped post-mortems ("the model was careless") that name no mechanism and therefore prevent nothing; single-cause stories for multi-cause events; and the most corrosive — quietly editing the record (relabeling a failure as a success, deleting the trace) which destroys the dataset every future improvement depends on. The failure record is training data for both humans and models; falsifying it is falsifying the curriculum.

## Rule

> **Rule.** Every failure is recorded under a taxonomy name with its detection method (how it was caught) and its class-level countermeasure. A post-mortem that names no mechanism, or whose fix addresses only the instance, is returned as incomplete — the class is still at large.
