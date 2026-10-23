# Port — Concurrency · Java
<!-- canonical_section: concurrency.core | language: java -->

## Definition

Java's concurrency is specification-grade: the Java Memory Model (JLS §17) defines happens-before precisely, and the platform offers a graduated ladder — threads and `synchronized`, the `java.util.concurrent` toolkit (locks, atomics, concurrent collections, executors), and, since Java 21, *virtual threads*: JVM-scheduled lightweight threads that restore the simple thread-per-request style at massive scale, with structured concurrency (`StructuredTaskScope`) as their companion discipline.

## Idiom mapping

- Canon "structured lifetimes" → `StructuredTaskScope`: forked subtasks are joined at scope exit, cancellation propagates, and a failure in one branch cancels siblings by policy — the canon's rule as a language feature; Executors with try-with-resources is the fallback shape.
- Canon "synchronization discipline named" → prefer the toolkit over raw `synchronized`: `ReentrantLock` (try-lock, fairness options, multiple conditions), `ReadWriteLock`, atomics (`AtomicLong`, `LongAdder` under contention), and the concurrent collections (`ConcurrentHashMap` — whose atomic methods like `computeIfAbsent` exist precisely to kill check-then-act races).
- Canon "share by communicating" → `BlockingQueue` between producer and consumer threads (bounded: backpressure is a feature), `CompletableFuture` pipelines for async composition, and virtual-thread-per-task with blocking I/O as the modern server default — blocking code, non-blocking economics.
- Canon "immutability shares freely" → records and deeply immutable objects cross threads without synchronization; `final` fields carry a memory-model guarantee (safe publication) that mutable fields do not.

## Worked example

```java
try (var scope = new StructuredTaskScope.ShutdownOnFailure()) {
    var user  = scope.fork(() -> fetchUser(id));
    var order = scope.fork(() -> fetchOrders(id));
    scope.join().throwIfFailed();          // both done, or the scope failed fast
    render(user.get(), order.get());
}                                          // no thread outlives this block
```

Thread-per-task simplicity with structured guarantees: no orphan threads, failure of either branch cancels the other, and the scope exit is the join — the canon's structure made idiomatic.

## Pitfalls

- **Double-checked locking without `volatile`**: the pre-memory-model classic — a partially constructed object published to other threads; the field must be `volatile` (or the idiom abandoned for holder patterns).
- **Synchronizing on interned/boxed objects** (`synchronized (Integer)`, string literals): locks shared with strangers across the whole JVM — lock on dedicated private objects only.
- **Thread-pool sizing by folklore**: CPU-bound pools ≈ core count; I/O-bound pools are bounded by the *downstream* capacity, not by optimism; unbounded queues in front of pools convert overload into latency and OOM.
- **Virtual-thread pinning**: a `synchronized` block (or native frame) around blocking I/O pins the carrier thread, silently negating virtual threads' scale — prefer `ReentrantLock` in blocking paths.

## Canon cross-reference

Canonical section: **concurrency.core** (Chapter 15, "Substance"). This port implements the canon for java; where the port and the canon disagree, the canon governs and the port is the bug.
