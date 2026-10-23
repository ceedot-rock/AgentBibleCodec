# Port — Concurrency · Python
<!-- canonical_section: concurrency.core | language: python -->

## Definition

CPython's concurrency story is defined by the Global Interpreter Lock (GIL): in the standard interpreter, only one thread executes Python bytecode at a time, so threads parallelize *waiting* (I/O) but not *computation* (free-threaded builds are changing this, but the GIL model remains the safe assumption for portable code). True CPU parallelism comes from multiprocessing (separate interpreters, explicit data transfer) or native extensions that release the GIL. Asyncio provides cooperative concurrency on one thread: tasks interleave at `await` points.

## Idiom mapping

- Canon "share by communicating" → `queue.Queue` between threads (thread-safe by construction), `multiprocessing.Queue`/pools between processes, asyncio queues within the loop.
- Canon "check-then-act is a race" → identical in asyncio despite the single thread: any sequence split by an `await` can interleave. The GIL makes individual bytecodes atomic-ish, never sequences.
- Canon "structured lifetimes" → `asyncio.TaskGroup` (3.11+) and `concurrent.futures` context managers: children cannot outlive their scope, and exceptions propagate as a group.
- Canon "synchronization discipline named" → `threading.Lock/RLock`, `asyncio.Lock` (different objects — never mix across the boundary), and `concurrent.futures` as the preferred high-level interface.

## Worked example

```python
import asyncio

async def fetch_all(urls, client):
    async with asyncio.TaskGroup() as tg:
        tasks = [tg.create_task(client.get(u)) for u in urls]
    return [t.result() for t in tasks]  # all done, or the group raised
```

One thread, hundreds of in-flight requests, no data races on Python objects — and every shared-state hazard that remains lives exactly at the `await` seams, where the canon says to look.

## Pitfalls

- **Blocking the event loop**: one synchronous call (a `time.sleep`, a requests call, a CPU burst) inside async code stalls *every* task — the asyncio equivalent of holding a lock across I/O.
- **Threads for CPU work**: adding threads to a GIL-bound computation adds contention, not speed; profile first (Chapter 14), then reach for processes.
- **Fork surprises in multiprocessing**: children inherit state at fork; locks and connections inherited across the fork are classic corruption sources — spawn cleanly for anything stateful.
- **Daemon threads at exit**: work silently abandoned at interpreter shutdown; join or use executors.

## Canon cross-reference

Canonical section: **concurrency.core** (Chapter 15, "Substance"). This port implements the canon for python; where the port and the canon disagree, the canon governs and the port is the bug.
