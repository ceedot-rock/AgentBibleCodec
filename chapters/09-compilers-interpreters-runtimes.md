# Chapter 9 — Compilers, Interpreters, and Runtimes

## Principle

Between source code and execution stands a translation pipeline, and knowing its stages turns "the program misbehaves" into a localizable question: was it lexed, parsed, analyzed, optimized, or executed wrongly? An agent that understands the pipeline reads error messages as stage reports, predicts what optimizations can and cannot do, and never fights the wrong layer.

## Substance

**The classical pipeline:** lexing (characters → tokens), parsing (tokens → syntax tree, per the language's grammar), semantic analysis (names resolved, types checked, scopes built — the phase that produces most beginner-facing errors), intermediate representation (a machine-ish, language-neutral form where most optimization lives), code generation (IR → target machine code, register allocation included). Interpreters execute the tree or a bytecode directly; just-in-time (JIT) compilers observe a running program and compile its hot paths natively, trading startup cost for peak speed — the engine model of modern JavaScript and JVM/.NET ecosystems. Ahead-of-time compilation pays the cost before execution and starts instantly.

**Optimization is semantics-preserving transformation** — that qualifier is the whole game. Constant folding, dead-code elimination, inlining, loop-invariant motion, vectorization: each is valid only because it provably doesn't change observable behavior. Two consequences: a compiler bug or an over-eager optimization flag is a real (if rare) suspect when optimized builds misbehave and debug builds don't; and undefined behavior in languages like C/C++ is the compiler's license to assume the impossible never happens — programs that rely on UB are not "working," they are un-diagnosed.

**Runtimes** are the code that ships with the program: garbage collectors (tracing vs reference counting; generational hypotheses; pause-time vs throughput trade-offs), exception machinery, dynamic dispatch, concurrency schedulers (green threads, async executors). The runtime is why "the same algorithm" performs differently across languages, and why memory bugs in managed languages are leaks of *reachable* objects rather than dangling pointers.

**Build systems and linking** belong to this chapter because they are the pipeline's social layer: static vs dynamic linking, dependency resolution, incremental builds, and reproducibility (same inputs → bit-identical outputs, the property that makes build artifacts auditable).

## Worked example

A release build crashes; the debug build passes. Pipeline thinking orders the suspects: (1) undefined behavior the optimizer exploits (most likely — run sanitizers: ASan/UBSan catch the class directly); (2) a race the slower debug timing hides (Chapter 15 — run a thread sanitizer); (3) an actual optimizer bug (rare; bisect optimization levels to confirm before claiming it). Each suspect has an instrument. Without the pipeline model, the incident is "flaky release build" and the fix attempted is superstition — rebuild, reorder, hope.

## Failure mode

Blaming the compiler first (it is almost never the compiler — but "almost" is why sanitizer evidence, not confidence, settles it); assuming source-level reasoning transfers naively to optimized code (variables optimized away in the debugger are a feature); and bytecode/IL illiteracy — refusing to read the layer where the actual behavior is defined.

## Rule

> **Rule.** For any misbehavior that differs between build configurations or languages, localize it to a pipeline stage with an instrument (sanitizer, IR dump, disassembly, runtime trace) before proposing a fix. "The compiler is wrong" requires a minimal reproducer at reduced optimization, or it is not yet a claim.
