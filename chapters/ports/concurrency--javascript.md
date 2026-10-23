# Port — Concurrency · JavaScript
<!-- canonical_section: concurrency.core | language: javascript -->

## Definition

JavaScript runs a single-threaded event loop per realm: code executes run-to-completion between await points, and "concurrency" means interleaving asynchronous operations, not parallel execution. Parallelism exists at the edges — Web Workers (browser) and worker_threads (Node) — as separate event loops communicating by message passing, with no shared heap by default (Node's `SharedArrayBuffer` + Atomics being the deliberate exception). The model eliminates data races on ordinary objects and replaces them with interleaving hazards at every `await`.

## Idiom mapping

- Canon "async is not parallel" → this port *is* that section: promises and async/await structure concurrency; CPU-bound work on the loop freezes all of it (a 200 ms computation is a 200 ms outage for every in-flight request) and belongs in a worker.
- Canon "share by communicating" → the only native pattern: `postMessage` between loops, structured-clone semantics (data is copied, not shared — ownership transfer is physical, hence safe by construction).
- Canon "structured lifetimes" → `AbortController`/`AbortSignal` as the cancellation currency: operations accept a signal, parents abort children, and frameworks increasingly enforce the pattern; un-abortable fire-and-forget promises are the leak shape.
- Canon "check-then-act is a race" → identical force, one thread: `if (!cache.has(k)) cache.set(k, await load(k))` races with itself across the `await`; the fix is the same — make the sequence atomic (store the in-flight promise, not just the value).

## Worked example

```js
const inflight = new Map();
async function loadOnce(key, loader) {
  if (!inflight.has(key)) {
    inflight.set(key, loader(key).finally(() => inflight.delete(key)));
  }
  return inflight.get(key); // every concurrent caller shares ONE load
}
```

The check-then-act gap (two callers both loading) is closed by caching the *promise* synchronously, before any await: interleaving can only occur at awaits, and there is none between the check and the set.

## Pitfalls

- **Blocking the loop**: synchronous JSON parsing of a huge payload, a regex with catastrophic backtracking, or a long loop — the entire realm stalls; measure with event-loop-lag metrics, not hope.
- **Unhandled rejections**: a promise that rejects with no handler is a silent failure in old code and a crash in modern Node defaults; every promise chain ends in a `catch` or a `return` to a caller who has one.
- **Fire-and-forget without tracking**: starting async work nobody awaits — errors vanish, ordering inverts, process exit truncates writes. Track it, await it, or queue it deliberately.
- **Assuming timer precision**: `setTimeout` is a lower bound under load, never a scheduling guarantee; time-critical logic belongs to clocks and deadlines, not sleeps.

## Canon cross-reference

Canonical section: **concurrency.core** (Chapter 15, "Substance"). This port implements the canon for javascript; where the port and the canon disagree, the canon governs and the port is the bug.
