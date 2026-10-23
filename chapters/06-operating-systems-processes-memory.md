# Chapter 6 — Operating Systems, Processes, and Memory

## Principle

Every program an agent writes runs inside an operating system's abstractions: processes that pretend to own a machine, virtual memory that pretends to be infinite and private, files and sockets that pretend devices are byte streams. Bugs that look like application bugs are very often the abstractions leaking — and an agent that knows what the OS actually does can predict, recognize, and fix them.

## Substance

**Processes and threads.** A process is an isolated address space plus resources; a thread is a schedulable execution stream sharing that space. Isolation buys fault containment (a crashing process dies alone) at the price of explicit inter-process communication; threads share memory cheaply and inherit the entire concurrency problem (Chapter 15). The scheduler multiplexes more runnable threads than cores by time-slicing — which is why "it worked on my machine" and tail-latency behavior both trace back to scheduling and contention, not code logic.

**Virtual memory.** Each process sees a private, contiguous address space, translated by page tables to physical frames, paged to disk on demand. Consequences an agent must internalize: allocation is cheap until it isn't (page faults, swapping, and the OOM killer that shoots the largest process when memory runs out); stack memory is small and fixed (deep recursion overflows it — production stacks are often just a few MiB per thread — while heap structures can grow); a memory-mapped file and an in-memory array differ in everything except syntax.

**The process lifecycle and its signals:** fork/exec or spawn, exit codes (the first API every program offers — 0 success, non-zero failure, and other programs *will* parse it), signals (SIGTERM asks, SIGKILL orders, SIGPIPE arrives when your reader went away), zombies (dead children awaiting reaping), and the orphan adoption rules. A supervisor that doesn't reap, a pipeline that ignores exit codes, a server that traps no signals — each is an OS-level bug class with a name.

**File systems and I/O.** Files are persistent byte sequences with names in a hierarchy; durability is earned, not default — data written may sit in OS buffers, and only `fsync` (and its directory counterpart) promises survival of a crash. Buffering exists at every layer (application, stdio, page cache, device), and each layer trades latency against throughput and safety. Descriptors are a finite resource: leaks of open files and sockets present as the classic "too many open files" failure under load, long after the leak was written.

## Worked example

A worker processes a queue: reads a job file, computes, writes results. Under load it intermittently dies with no application error. The OS-literate diagnosis order: check exit status (137 = 128+9: SIGKILL — the OOM killer's signature; memory growth is the bug), check descriptor count trend (leak → eventual EMFILE), check whether "written" results were fsynced (a crash window explains missing outputs). Each hypothesis is a single command to test. Without the OS model, the same incident reads as "flaky" and gets retried into a bigger outage.

## Failure mode

Assuming the abstraction is the reality: recursion depth chosen as if stacks were elastic; treating `write()` returning as "the data is saved"; spawning unbounded children; leaking descriptors in error paths (the path least tested is the path that leaks). And the classic: CPU at 100% blamed on computation when the process is actually thrashing — paging, not computing.

## Rule

> **Rule.** For any long-running or load-bearing program, enumerate its OS resources — memory ceiling, descriptor budget, child processes, stack depth — and what happens at each limit. A design that cannot say how it dies at its limits will die at them anyway, undocumented.
