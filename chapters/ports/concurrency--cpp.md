# Port — Concurrency · C++
<!-- canonical_section: concurrency.core | language: cpp -->

## Definition

C++ exposes the machine's concurrency directly: `std::thread` over OS threads, a formal memory model (since C++11) defining exactly which interleavings and reorderings are legal, and a full lattice from mutexes to lock-free atomics. The language's stance is maximal control at maximal responsibility: a data race is *undefined behavior* — not a wrong answer but a program with no meaning — and nothing in the language prevents writing one.

## Idiom mapping

- Canon "synchronization discipline named" → RAII lock guards (`std::lock_guard`, `std::unique_lock`, `std::scoped_lock`): the lock's lifetime is an object's lifetime, so early returns and exceptions cannot leak a held lock. `std::scoped_lock` on multiple mutexes uses a deadlock-avoidance algorithm — the canon's lock ordering, mechanized for the multi-lock case.
- Canon "share by communicating" → futures and promises (`std::async`, `std::future`), condition variables for wait/notify, and (C++20) coroutines plus a growing sender/receiver ecosystem; the classic hand-rolled pattern is a mutex + condition variable + queue, with the predicate-loop as a required idiom.
- Canon "structured lifetimes" → `std::jthread` (C++20): joins on destruction and carries a stop token — a joinable thread that cannot be accidentally detached into a leak, fixing `std::thread`'s terminate-on-destroy trap.
- Canon "atomics with stated ordering" → `std::atomic<T>` with explicit `memory_order` (seq_cst by default — correct and slower; acquire/release for synchronization patterns; relaxed only with a written justification).

## Worked example

```cpp
std::mutex m;
std::condition_variable cv;
std::queue<Job> q;
bool done = false;

// consumer
while (true) {
    std::unique_lock<std::mutex> lk(m);
    cv.wait(lk, [&] { return !q.empty() || done; });  // predicate loop: spurious wakeups are legal
    if (q.empty() && done) break;
    Job j = q.front(); q.pop();
    lk.unlock();
    process(j);                                        // work happens outside the lock
}
```

Every canon element is present and visible: the guarded queue, the predicate loop (a condition variable may wake without a signal — waiting without re-checking the predicate is the classic bug), and the lock released before the expensive work.

## Pitfalls

- **Data race = UB**: not "unsynchronized but probably fine" — the optimizer may assume races away. The instrument is ThreadSanitizer; the fix is a discipline, never a `volatile`.
- **Detached threads touching locals**: a detached thread outliving its function's stack frame is a use-after-free with good PR. Join, or `jthread`, or scoped ownership.
- **Locking inconsistently**: the canon's ordering rule — two mutexes taken in different orders in different functions is a deadlock awaiting its schedule.
- **`std::async`'s launch ambiguity**: the default policy may run synchronously in the calling thread; state `launch::async` when concurrency is the point.

## Canon cross-reference

Canonical section: **concurrency.core** (Chapter 15, "Substance"). This port implements the canon for cpp; where the port and the canon disagree, the canon governs and the port is the bug.
