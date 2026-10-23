# Chapter 15 — Concurrency

## Principle

Concurrency is the discipline of correctness when events interleave. Its central difficulty: between any two operations of one thread, any number of operations of another may occur — so sequential reasoning silently stops applying, and bugs become nondeterministic, rare, and load-dependent. Parallelism (doing things at once for speed) is one motive; concurrency (structuring for independent activities) is the broader one, and it is paid for in reasoning.

## Substance

**The failure vocabulary:** a *race condition* — outcome depends on interleaving; the *data race* — unsynchronized concurrent access with at least one write (undefined behavior in low-level memory models); the *atomicity violation* — a check-then-act sequence (`if (balance >= x) withdraw(x)`) whose premise expires between check and act; *deadlock* — a cycle of threads each waiting for the next (prevented by lock ordering: acquire in a globally fixed order); *livelock and starvation* — motion without progress, and progress denied; *priority inversion*.

**The tools, in ascending power and danger:** immutable data (no sharing, no problem — share freely); message passing / actor models (share by communicating — Go's proverb: "don't communicate by sharing memory; share memory by communicating"); locks/mutexes (correct, composable poorly, deadlock-prone); lock-free structures and atomics with explicit memory orderings (expert territory — the memory model, e.g. the C++ or Java model, defines which reorderings are legal and what `volatile`/acquire/release actually promise); software transactional memory and structured concurrency (scope-bound lifetimes for tasks — the modern answer to leaked threads: a task's children cannot outlive its scope).

**Async is not parallel:** an event loop gives concurrency (many in-flight I/O operations) on one thread — no data races on the heap, but interleavings at every `await`, so check-then-act bugs survive the translation and must be reasoned about identically.

**Testing concurrency** requires adversarial instruments: stress runs, deterministic-scheduler testing (exploring interleavings systematically where the platform allows), thread sanitizers, and the humility that a passing test proves almost nothing — races hide in schedules, not in code paths, and the schedule space is astronomically larger than any test run.

## Worked example

A counter incremented by 100 threads × 1,000 increments each returns 97,412. The mechanism: `count++` is read-modify-write, not atomic — two threads read 50, both write 51, one increment is lost; thousands of collisions later, the total is short. Fixes at three levels: an atomic counter (hardware-level); a lock around the increment (correct, serializes); or restructure so threads never share (per-thread counters, summed at the end — fastest, and the design lesson: *the best synchronization is the one the architecture makes unnecessary*).

## Failure mode

Synchronizing the obvious variable while the invariant spans three; locking inconsistently ordered across code paths (deadlock under the one schedule production finds); holding locks across I/O or calls into unknown code; "fixing" a race with a sleep; and volatile-as-synchronization superstition in memory models where it doesn't mean that.

## Rule

> **Rule.** Every piece of shared mutable state in a design names its synchronization discipline (immutability, ownership by one thread, a named lock, an atomic with stated ordering) — and every check-then-act sequence over shared state is presumed a race until the discipline shows otherwise.
