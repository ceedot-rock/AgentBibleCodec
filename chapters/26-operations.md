# Chapter 26 — Operations: Running Agents in Production

## Principle

An agent in production is a system with economics, failure domains, and a human organization around it. Operations is where the craft meets reality: quotas, costs, monitoring, escalation, and the discipline of *how work is launched* — which determines whether the system's output is a stream of verified results or a bonfire of compute.

## Substance

**Batch over interactive.** Long agent work belongs in committed, self-terminating batch jobs that run server-side to a defined end state — not in interactive sessions that die when a tab closes, a connection drops, or a human looks away. A batch job has a contract: inputs fixed at launch, an expected output artifact, a timeout, and a log that survives it. Interactive sessions are for exploration and steering; the moment work matters, it gets a batch definition. The economic corollary: never babysit — human attention is the scarcest resource in the system, and a workflow that needs a human watching a spinner has misallocated it.

**Quota and cost economics.** Compute arrives in quotas (hours per week, calls per day, tokens per month) and every program of work is a portfolio allocation against them. Price experiments *before* running them from measured unit costs (seconds per attempt × attempts; tokens per task × tasks) — a generation or evaluation batch whose expected yield doesn't justify its quota share doesn't run, or runs smaller first (a pilot that measures the unit cost precisely). Sequencing matters: cheap decisive experiments before expensive confirmatory ones; and a shared quota silently couples projects that believe themselves independent — account for the coupling explicitly rather than discovering it as a mysteriously exhausted budget.

**Monitoring and the posture of oversight.** The operational stance that scales is: the system watches itself and batches its reports; the human is interrupted only for (a) decisions that are genuinely theirs — identity, payment, legal attestation, irreversible publication — and (b) forks where their judgment is the input. Everything else is a digest. Monitoring must distinguish *absent* from *fine*: a sensor that failed to run is a gap in coverage, reported as unknown — a dashboard that renders silence as green is manufacturing confidence.

**Human gates, designed.** Some steps are the human's by nature, not by system weakness: creating accounts, passing identity verification, providing payment instruments, signing, and final approval of irreversible external acts. Design the workflow so these arrive *consolidated and prepared* — everything fillable already filled, the exact decision stated in one line, the consequence of each option priced. The system's throughput is often bounded by this queue (in honest operational records, the majority of stalled work stalls at human-only gates, not at execution); respect it by never adding a preventable item to it, and never re-asking an item already answered.

**Stop and scope discipline.** A human's stop is final and thread-specific: stopped lines of work are not re-prompted, re-packaged, or resumed under a new name. Before spending effort on any external opportunity, venue, or target, verify it exists, is in scope, and is eligible *first* — the cheapest failure is the one prevented by a five-minute check before five hours of work.

## Worked example

A research program plans a data-generation batch: 400 attempts estimated from a measured 174 s/attempt ≈ 19 hours — two-thirds of the weekly compute quota, for an expected yield computed from the measured success rate. Priced in advance, the decision changes shape: run a 200-attempt pilot (~9.5 h) first; if the yield tracks the estimate, the second half is justified by data; if the success rate has moved (because the sampler improved), the pilot's own output may already suffice. The alternative history — launching the full batch blind — spends the same quota to learn the same facts later and worse. Operations is arithmetic performed *before* the spend, not narrative performed after it.

## Failure mode

Interactive-session dependence (work dying with tabs); unpriced launches (quota discovered exhausted mid-program); alert fatigue (so many low-grade notifications that the real one is missed — batching is a safety feature, not a courtesy); re-litigating settled stops; and shadow coupling (two "independent" programs contending for one quota, one GPU pool, or one human's attention, each planned as if alone).

## Rule

> **Rule.** Every unit of agent work launches with: a priced budget (unit cost × volume, from measurements), a defined end state and output artifact, a timeout, and a named human-gate list (what will need the human, stated up front). Work launched without a price is reported as unpriced in the operations record — and unpriced work does not get to be surprised by its bill.
