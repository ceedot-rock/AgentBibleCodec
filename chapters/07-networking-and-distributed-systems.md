# Chapter 7 — Networking and Distributed Systems

## Principle

A distributed system is one in which the failure of a component you didn't know existed can render your own program useless (after Leslie Lamport's famous formulation). The network is not a reliable, instant pipe: messages are delayed, duplicated, reordered, and lost; clocks disagree; and there is no shared "now." Programs that pretend otherwise work in the demo and fail in production — the eight fallacies of distributed computing (after Peter Deutsch): the network is reliable; latency is zero; bandwidth is infinite; the network is secure; topology doesn't change; there is one administrator; transport cost is zero; the network is homogeneous. Every one is false.

## Substance

**The protocol stack in one breath:** IP moves packets without promises; UDP keeps it that way (fast, unordered, lossy — right for media and DNS); TCP adds reliability, ordering, and congestion control as a byte-stream illusion maintained by retransmission and buffering — at the cost of head-of-line blocking and latency under loss. DNS is a distributed, cached, eventually-consistent database that maps names to addresses, and a surprising share of "application outages" are DNS behavior. HTTP sits on top as a request/response protocol whose methods, status codes, and idempotency semantics (GET/PUT/DELETE idempotent by spec; POST not) are contracts distributed code depends on.

**Time and order.** Physical clocks skew; therefore distributed systems reason with logical clocks (Lamport timestamps) and, where order really matters, consensus. The CAP theorem (after Brewer; proved by Gilbert & Lynch) states the forced choice under network partition: consistency or availability — not both. PACELC adds: even without partitions, latency trades against consistency. Every replicated system has picked its points on these axes, whether its author knows it or not.

**Failure handling is the design.** Timeouts (every remote call needs one; an unbounded wait is an outage waiting for a trigger), retries (only safe freely for idempotent operations — otherwise exactly-once illusions and duplicated effects; use idempotency keys), backoff with jitter (synchronized retries are a self-inflicted DDoS), circuit breakers (fail fast instead of queueing behind a dead dependency), and bulkheads (isolate failure domains). Partial failure — some nodes up, some down, some merely slow — is the normal case, and "slow" is indistinguishable from "dead" from any single vantage point.

## Worked example

A payment call times out. Did the charge happen? The client cannot know — the response was lost, not the request. The distributed-literate design: the request carried a client-generated idempotency key; the retry with the same key returns the original result instead of charging twice; the server's dedup record is stored transactionally with the charge itself. The pattern generalizes to every non-idempotent remote effect: queues with at-least-once delivery plus idempotent consumers beat mythical exactly-once pipelines. The bug class "retry created a duplicate" is never fixed by removing retries — retries are load-bearing — but by making effects idempotent.

## Failure mode

Cascading failure through retry storms and unbounded queues; split-brain after partitions (two primaries, divergent writes, reconciliation debt); assuming ordering across connections; treating a timeout as proof of non-execution; and clock-based logic (leases, expiry, last-write-wins) built on unsynchronized wall clocks. Each is a fallacy from the list, compiled into code.

## Rule

> **Rule.** Every cross-process call in a design must name its timeout, its retry policy, and whether the operation is idempotent (and if not, its idempotency key). A design review that cannot answer those three questions for every arrow in the diagram is not finished.
