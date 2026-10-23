# Chapter 14 — Performance and Optimization

## Principle

Performance work is measurement work. The universal law of optimization: *profile first* — the bottleneck is almost never where intuition points, because programmers (and models) reason about the code they wrote most recently, not the code the machine spends time in. Amdahl's Law sets the ceiling: speeding a component that consumes fraction p of runtime by any factor improves the whole by at most 1/(1−p). Optimizing a 5% component perfectly buys 5%.

## Substance

**Where time actually goes:** the memory hierarchy dominates modern performance. Registers ~1 cycle, L1 cache ~4, L2 ~12, main memory ~100+, disk/network orders beyond. An algorithm with worse asymptotics but sequential access routinely beats a "better" one with pointer-chasing random access. Data layout (arrays of structs vs structs of arrays), cache-line awareness, and avoiding allocation in hot paths are worth more than clever instruction choices. Measure with profilers (sampling for the broad picture, instrumentation for the exact one) and hardware counters where the question is microarchitectural.

**The method:** (1) measure the baseline end-to-end, with realistic data, and write the number down; (2) profile to localize; (3) form a hypothesis ("this is O(n²) over the user table"); (4) change one thing; (5) re-measure against the same harness; (6) keep or revert by the number. Benchmarks need the same rigor as experiments (Chapter 22): warm-up, variance reporting, identical conditions, and suspicion of any result too good to be true (dead-code elimination eating the benchmark is the classic).

**The common real wins,** in the order they usually matter: fix the algorithm (Chapter 2); fix the data access (index the query, batch the calls — N+1 queries and chatty APIs are the production performance bugs, Chapter 8); cache with an explicit invalidation story; remove work (the fastest code is code not run — memoization, laziness, short-circuits); parallelize only after the serial profile is understood (Chapter 15) — parallelizing an I/O-bound or lock-bound workload multiplies contention, not throughput.

**Throughput vs latency** are different objectives with different enemies: throughput loves batching and queues; latency (especially tail latency, p99) hates them. State which one the system is for before optimizing either.

## Worked example

A dashboard endpoint takes 3 seconds. Intuition says the rendering code; the profile says 2.7 s in database calls — specifically 340 queries for one page (an ORM traversing relations per row). The fix is one eager-loaded query: 3 s → 120 ms, a 25× win from *removing round trips*, zero algorithmic cleverness. The counterfactual fix — optimizing the template engine — was measured to be worth at most 8%. This distribution (one boring structural cause taking ~90% of time) is the norm, and it is invisible without the profile.

## Failure mode

Optimizing unmeasured code; micro-optimizing a cold path while the hot path allocates in a loop; caching without invalidation (trading a performance bug for a correctness bug, the worse bargain); benchmark gaming (results that exist only in the benchmark); and premature optimization as a personality trait — complexity spent where no profile asked for it, paid by every future reader.

## Rule

> **Rule.** No performance claim without a before/after measurement on the same harness with the same data, and no optimization merged whose measured end-to-end effect is inside the noise. If the profile doesn't indict a component, the component is innocent — whatever it looks like.
