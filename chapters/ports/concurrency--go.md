# Port — Concurrency · Go
<!-- canonical_section: concurrency.core | language: go -->

## Definition

Go's concurrency is built in at the language level: goroutines (lightweight, runtime-scheduled threads, thousands are routine), channels (typed conduits for values *and* synchronization), and `select` (waiting on multiple channels). The runtime scheduler multiplexes goroutines onto OS threads with work stealing, and the race detector (`-race`) is a first-class, production-grade instrument — the canon's demand for adversarial testing of concurrency ships with the toolchain.

## Idiom mapping

- Canon "share by communicating" → Go's founding proverb *is* the canon's: "Don't communicate by sharing memory; share memory by communicating." A value sent on a channel transfers ownership by convention; the receiver owns it now.
- Canon "structured lifetimes" → goroutines have no built-in parent; structure is imposed by `sync.WaitGroup`, `errgroup`, and above all `context.Context` — cancellation and deadlines propagate down the call tree, and a goroutine that ignores its context is a leak by definition.
- Canon "synchronization discipline named" → channels first; `sync.Mutex` for protecting small shared structures where a channel would contort the design (state-with-guard is a legitimate Go shape); `sync/atomic` for counters and flags.
- Canon "deadlock prevention" → no lock ordering needed where there are no locks; the channel-era equivalents are unbuffered-channel cycles and senders with no receivers — the runtime detects total deadlock ("all goroutines are asleep") and panics, but partial deadlock (one stuck pipeline) hangs silently.

## Worked example

```go
jobs := make(chan Job)
var wg sync.WaitGroup
for i := 0; i < 8; i++ {
    wg.Add(1)
    go func() {
        defer wg.Done()
        for j := range jobs { process(j) } // ends when jobs closes
    }()
}
for _, j := range allJobs { jobs <- j }
close(jobs)   // the close is the termination signal
wg.Wait()
```

The worker pool is a dozen lines: ownership flows through the channel, termination is the close, completion is the WaitGroup — each canon element visible in the idiom itself.

## Pitfalls

- **Goroutine leaks**: a goroutine blocked forever on a send nobody receives, holding its stack and everything it captured. Every spawned goroutine needs a provable exit path (context, close, or a receiver that cannot leave).
- **Loop variable capture** (pre-1.22 semantics survive in old code): goroutines closing over the loop variable all see its final value.
- **Data races despite the idiom**: channels don't protect a shared map touched on both sides of the channel; `-race` in tests is not optional hygiene, it is the test.
- **Buffered channel as a crutch**: a huge buffer converts backpressure into memory growth and hides the overload it was meant to signal (Chapter 7).

## Canon cross-reference

Canonical section: **concurrency.core** (Chapter 15, "Substance"). This port implements the canon for go; where the port and the canon disagree, the canon governs and the port is the bug.
