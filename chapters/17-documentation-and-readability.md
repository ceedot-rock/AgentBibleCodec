# Chapter 17 — Documentation and Readability

## Principle

Code is read far more often than it is written — by reviewers, by future maintainers, by debugging sessions at 3 a.m., and by agents, whose entire perception of a codebase is its text. Readability is therefore not aesthetics; it is the bandwidth of the channel through which every other engineering activity flows. Documentation's job is narrower than people think: record what the code *cannot say* — intent, reasons, constraints, history — and let the code say the rest.

## Substance

**Naming** is the highest-leverage readability act: names that carry the contract (units, ranges, semantics — `timeout_seconds`, not `timeout`), consistency that lets readers pattern-match across the codebase, and honesty (a function named `get` that writes is a lie told to every future reader). **Structure** follows: small functions with one level of abstraction each; code laid out so the common path reads top-to-bottom; comments that explain *why* (the constraint, the workaround's reason, the citation) rather than narrating *what* the next line plainly does — comments that duplicate code rot into falsehoods, and a stale comment is worse than none because it is believed.

**The documentation layers,** each with a distinct job: docstrings/API docs (the contract at the point of use); README (the on-ramp: what this is, how to run it, where things live); architecture records (ADR-style: decision, context, alternatives rejected and why — the institutional cure for re-litigating settled questions and for "why is it like this?" archaeology); changelogs (what changed for consumers, in their terms); and runbooks (operational knowledge for the failure case, written before it happens).

**For agent readers specifically:** machine-legible structure is a kindness with measurable returns — consistent file organization, explicit invariants stated near the code they constrain, tests that double as usage examples, and errors whose messages name the violated expectation. An agent reading a codebase samples it under a budget (Part III); documentation that front-loads architecture and invariants converts that budget from archaeology into work.

## Worked example

Two implementations of a retry helper. The first is forty lines with a comment `// retry logic`. The second is forty lines with a header: "Retries *idempotent* calls only. Backoff: exponential, base 200 ms, jitter ±50%, max 5 attempts, total budget 30 s. Non-idempotent callers must pass an idempotency key (Chapter 7). Chosen after incident review showed synchronized retries amplifying an outage." The second header prevents three distinct future bugs (retrying a payment, removing the jitter, raising attempts unboundedly) — none of which the code itself could prevent, because each bug consists of *changing the code while misunderstanding it*. That is documentation's precise function: transmitting the constraints that are invisible in the artifact.

## Failure mode

Documentation that paraphrases code and drifts; aspirational docs describing the system that was planned; README archaeology (five generations of setup instructions, one of which works); comment-to-code ratio worship; and its opposite — the "code is self-documenting" dogma applied to systems whose key facts (why this threshold, why this order, what breaks if changed) exist nowhere in the code at all.

## Rule

> **Rule.** Every non-obvious decision in code carries its reason at the point of decision — the constraint, the rejected alternative, or the citation. If a future change could be made wrongly *while reading the code correctly*, the missing fact belongs in a comment, a test name, or a decision record before the change ships.
