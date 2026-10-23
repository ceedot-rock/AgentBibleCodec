# Chapter 1 — Computation and Computability

## Principle

Before an agent writes code, it must know what code *is*: a finite description of a mechanical procedure, executed by a machine that follows rules without understanding them. Programming is possible because computation has a precise mathematical definition — and it has hard limits that no cleverness, scale, or model size removes. An agent that knows the limits stops early and honestly; an agent that doesn't will happily burn its entire budget on a problem that is provably undecidable or intractable.

## Substance

**The Church–Turing thesis.** Any function computable by any effective procedure is computable by a Turing machine — a finite control, an unbounded tape, and a handful of operations (after Turing, *On Computable Numbers*, 1936). Every programming language in practical use is Turing-complete: given unbounded time and memory it can compute anything any other can. Languages differ not in *what* they can compute but in *how expressively, safely, and efficiently* they let a programmer say it. This is why "can language X do Y?" is almost always the wrong question; the right questions are cost, clarity, and error surface.

**Decidability and the halting problem.** Turing proved no program can decide, for every program and input, whether that program halts. This is not an engineering gap; it is a theorem. Its corollaries (Rice's theorem) say *every* non-trivial semantic property of programs is undecidable in general: whether a program is correct, whether two programs are equivalent, whether a variable is ever used, whether this code contains a virus. Practical tools therefore choose a side: static analyzers are *sound* (no false negatives, some false alarms), *complete* (no false alarms, some misses), or neither — never both fully. When a tool claims certainty about program behavior, ask which side it errs on.

**Information.** Shannon's mathematical theory of communication (Shannon, 1948) defines information quantitatively: a message's information content is its surprisal, and entropy bounds how far any lossless encoding can compress a source. Compression limits, error-correcting codes, and channel capacity all descend from this. The working consequence for an agent: redundancy is the only thing compression removes; already-random data does not compress, and a "compression result" beating entropy bounds is a measurement error, not a breakthrough.

**Self-reference.** Programs can read, generate, and modify programs — compilers compile compilers, agents write agents. Diagonal arguments (the engine behind the halting proof and Gödel's incompleteness theorems) recur wherever a system reasons about itself: an agent evaluating its own output inherits the limits of any self-referential checker, which is one reason external verification (Chapter 21) is structurally necessary rather than merely prudent.

## Worked example

A user asks for a tool that "checks whether any submitted program will loop forever, so we can reject bad ones." The computability-literate response: the general tool cannot exist; build instead a *partial* checker — timeouts during execution, loop-fuel limits, detection of known non-terminating patterns — and document which cases it decides, which it rejects on suspicion, and which it passes in ignorance. That is how every real system (sandboxed runtimes, smart-contract gas, CI timeouts) answers an undecidable question: bound the resource, not the logic.

## Failure mode

Treating limits as engineering challenges: attempting exhaustive verification of arbitrary code, expecting a static tool to settle behavioral questions exactly, or trusting a claimed result that violates an information-theoretic bound. The failure presents as endless work on an impossible specification — the most expensive failure an autonomous agent can have, because nothing in the loop pushes back.

## Rule

> **Rule.** When a task requires deciding a semantic property of arbitrary programs, restate it as a bounded, decidable approximation (resource limits, pattern classes, sound-but-incomplete analysis) and state explicitly which cases the approximation errs on. A plan that requires an exact general solution to an undecidable problem is rejected before the first tool call.
