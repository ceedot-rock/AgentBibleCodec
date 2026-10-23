# Port — Concurrency · Rust
<!-- canonical_section: concurrency.core | language: rust -->

## Definition

Rust moves concurrency correctness into the type system (Chapter 5's port): the `Send` trait marks types safe to transfer between threads, `Sync` marks types safe to share by reference, and the ownership rules that govern single-threaded memory govern multithreaded access too — a data race is unrepresentable in safe code. "Fearless concurrency" is the community's name for the consequence: the compiler rejects the race before the schedule can find it.

## Idiom mapping

- Canon "shared mutable state names its discipline" → the type *is* the name: `Mutex<T>` (shared ownership via `Arc<Mutex<T>>`), `RwLock<T>` (many readers / one writer), atomics with explicit `Ordering` for lock-free state, ownership transfer via channels (`std::sync::mpsc`, or `tokio::sync` in async) for the communicate-by-sharing pattern.
- Canon "check-then-act is a race" → the `MutexGuard` makes the check-and-act one critical section by construction: you cannot touch the data without holding the guard, and the guard's scope is the lock's scope.
- Canon "structured lifetimes" → scoped threads (`std::thread::scope`, stable since 1.63): spawned threads borrow stack data and are guaranteed joined at scope end — structured concurrency as a library type, with the borrow checker proving the join.
- Canon "async is not parallel" → async/await with an executor (tokio and kin): futures are lazy, tasks interleave at `.await`, and `Send` bounds decide whether a task may migrate between worker threads — the canon's warning, enforced by types.

## Worked example

```rust
use std::sync::{Arc, Mutex};
use std::thread;

let counter = Arc::new(Mutex::new(0u64));
let handles: Vec<_> = (0..100).map(|_| {
    let c = Arc::clone(&counter);
    thread::spawn(move || {
        for _ in 0..1_000 { *c.lock().unwrap() += 1; }
    })
}).collect();
for h in handles { h.join().unwrap(); }
assert_eq!(*counter.lock().unwrap(), 100_000);
```

Chapter 15's worked example — the counter that returned 97,412 — cannot lose an update here: the increment is inseparable from the lock, because the integer is *inside* the mutex and unreachable otherwise.

## Pitfalls

- **Holding a guard across `.await`**: blocks an executor thread and can deadlock a single-threaded runtime; drop guards before awaiting, or scope them tightly.
- **Deadlock is still possible**: two mutexes, two orders — types prevent *races*, not *wait cycles*; the canon's lock-ordering discipline still applies in full.
- **`Ordering::Relaxed` by default**: atomics without a reasoned memory ordering are data races in a trench coat; Acquire/Release is the usual correct pair for flag-plus-data patterns.
- **Unbounded channels**: memory grows silently under a slow consumer — the backpressure lesson of Chapter 7 applies verbatim; prefer bounded.

## Canon cross-reference

Canonical section: **concurrency.core** (Chapter 15, "Substance"). This port implements the canon for rust; where the port and the canon disagree, the canon governs and the port is the bug.
