# Chapter 12 — Debugging Method

## Principle

Debugging is the scientific method applied to a misbehaving artifact: observe, hypothesize, predict, experiment, conclude. The skill is not intuition — it is discipline under frustration: change one variable at a time, believe the evidence over the theory, and treat every "impossible" observation as information about your model of the system, not about the system's sanity.

## Substance

**The loop:** (1) *Reproduce* — a bug you cannot reproduce you cannot fix, only chase; build the smallest reliable reproduction before touching the code (the repro is also the regression test, Chapter 11). (2) *Reduce* — bisect the input, the configuration, the history, until the reproducer is minimal; `git bisect` automates this against history (the first bad commit is a fact, not a suspicion). (3) *Hypothesize* — name a mechanism, not a location: "the cache returns the stale entry because the key omits the locale" predicts specific observations; "something's wrong in caching" predicts nothing. (4) *Experiment* — instrumentation over staring: logs, assertions, debugger breakpoints, sanitizers; design the experiment so both outcomes are informative. (5) *Conclude and generalize* — after the fix, ask what class this bug belongs to and where else the class lives.

**The canonical tactics** (the tradition runs from Kernighan & Pike, *The Practice of Programming*, through Zeller, *Why Programs Fail*): divide and conquer; work backwards from the failure; check the plug (the embarrassing basics — wrong environment, stale build, wrong file — are statistically the most common causes); rubber-duck explanation (articulating the expected behavior precisely exposes the wrong assumption); printf's honest cousin, the structured log with timestamps and correlation ids; and the differential method — find two environments/inputs/versions that differ in outcome and interrogate the difference.

**Heisenbugs and the observer effect:** bugs that vanish under observation (races, timing, uninitialized memory) demand recording over inspection — flight recorders, core dumps, deterministic replay, sanitizers — because the instrument must not change the phenomenon.

## Worked example

Intermittent failure: one request in a thousand returns the previous user's data. Hypotheses ranked by mechanism: shared mutable state across requests (a module-level cache keyed badly); connection-pool object reuse; a race in session lookup. The discriminating experiment is not reading the code harder — it is adding the user id and the serving object id to the response log for an hour and correlating: failures sharing an object id with the previous request convict the pool; failures sharing a key convict the cache. One hour of data beats a week of code reading, because the bug is *intermittent* and code reading samples the same distribution the bug hides in.

## Failure mode

Shotgun debugging (multiple simultaneous changes — when it "works," nobody knows why, and one change is usually a regression in waiting); fixing the symptom at the observation point (retrying, catching-and-ignoring, sleeping 100ms "to let it settle"); anchoring on the first plausible theory and explaining away contrary evidence; and the sunk-cost loop — the third hour on a hypothesis the data rejected in the first.

## Rule

> **Rule.** No fix without a reproduction; no conclusion without an experiment whose outcome could have changed your mind. If two consecutive experiments fail to discriminate, widen the observation (more logging, a sanitizer, a bisect) instead of deepening the theory — the deficit is data, not cleverness.
