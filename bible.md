# The Agentic Coding Bible

**AgentBibleCodec** — a codec for coding knowledge: everything encoded in, your selection decoded out.

v1 · 2026-10-22

This book is modular and filterable. The full text is the default; `tools/filter_bible.py` decodes the selection you ask for (languages, domains). See `MANIFEST.md` for structure, `PORTING.md` for the language-port protocol, and `NOTATION.md` for the study-book layer.



---

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


---

# Chapter 2 — Algorithms and Complexity

## Principle

Correctness says a program produces the right answer. Complexity says whether it produces it before the heat death of the project. An agent must reason about growth — how time and memory scale with input size — before choosing an approach, because the difference between O(n log n) and O(n²) is invisible on test data and catastrophic on production data.

## Substance

**Asymptotic analysis** (the canon is Cormen, Leiserson, Rivest & Stein, *Introduction to Algorithms* — "CLRS") describes growth rates ignoring constant factors: O(1), O(log n), O(n), O(n log n), O(n²), O(2ⁿ). The discipline is in the ignoring: asymptotics predict *scaling*, and scaling is what kills systems. A nested loop over 10⁶ records is ~10¹² operations — no constant-factor optimization, faster language, or bigger machine rescues a wrong complexity class; the input only has to grow modestly to defeat any of them.

**The standard toolkit**, each with its canonical setting: divide and conquer (merge sort, binary search — halve the problem, pay log n levels); greedy algorithms (locally optimal choices, correct only where an exchange argument proves them — Dijkstra's shortest paths yes, coin change in arbitrary denominations no); dynamic programming (overlapping subproblems + optimal substructure: compute once, memoize — edit distance, knapsack approximations); graph algorithms (BFS/DFS as the universal traversal substrate; Dijkstra with a priority queue; Bellman–Ford where negative edges exist; union-find for connectivity); hashing (expected O(1) lookup, the workhorse of deduplication and membership).

**Hardness.** NP-complete problems (after Cook, 1971; Karp's 21 problems) admit no known polynomial algorithm and are believed to admit none. The professional response is not surrender but redirection: approximation algorithms with proven ratios, parameterized algorithms (fast when a structural parameter is small), heuristics with honest "no guarantee" labels, or problem reformulation (constraints that make the instance tractable). Recognizing NP-hardness in a requirements document is a senior-level skill: "find the best schedule/routes/assignment" is often NP-hard in disguise.

**Analysis honesty.** Worst case, average case, and amortized case are different claims. Quicksort is O(n log n) average, O(n²) worst — and the worst case is *adversarially reachable* (sorted input against a naive pivot). Hash tables are O(1) expected, O(n) under collision attack. State which case a claim uses; an agent quoting only the average case for an attacker-influenced input is writing a vulnerability (see Chapter 13).

## Worked example

Task: find duplicate records in a 50-million-row export. Naive pairwise comparison: ~1.25 × 10¹⁵ comparisons — days. Sort by key (O(n log n)) and scan adjacent rows: minutes. Or one pass with a hash set: O(n) expected, memory proportional to unique keys. The algorithmic choice, made in seconds of thought, is worth more than any amount of micro-optimization of the naive version. Conversely: the same problem at 500 rows — the naive loop is *correct engineering*, because constants dominate and simplicity is a feature. Complexity analysis informs judgment; it does not replace it.

## Failure mode

Premature asymptotics (building a balanced tree where a list of twelve items lives) and its opposite, asymptotic blindness (shipping the O(n²) join because tests had 200 rows). Also: quoting a textbook bound while ignoring memory hierarchy reality — an O(n) algorithm with random access can lose to an O(n log n) algorithm with sequential access on real hardware, because cache misses cost ~100× a cache hit (Chapter 14).

## Rule

> **Rule.** Before implementing any operation over a collection, state its expected input size and the complexity of the chosen approach in time and space, including which case (worst/average/amortized) the bound assumes. If the approach is superlinear and the input can exceed ~10⁵ elements, the burden of proof is on keeping it.


---

# Chapter 3 — Data Structures

## Principle

Programs are algorithms plus data structures (Wirth's title says it exactly: *Algorithms + Data Structures = Programs*, 1976). The structure chosen determines which operations are cheap, which are ruinous, and — less obviously — which bugs are even possible. Most "algorithm problems" in production code are actually data-structure selection problems wearing a disguise.

## Substance

**The core inventory and their honest costs:**

- **Arrays / lists:** O(1) indexed access, O(n) insertion in the middle, cache-friendly. The default; deviate only for a reason.
- **Linked lists:** O(1) insertion at a held node, O(n) access, cache-hostile. Rarely the right answer on modern hardware despite textbook nostalgia.
- **Hash tables:** expected O(1) lookup/insert/delete; the cost is hash quality, load factor, and worst-case degradation. Iteration order is not a contract unless the implementation makes it one.
- **Balanced search trees** (red-black, AVL, B-trees): guaranteed O(log n) operations and *ordered* traversal. B-trees' wide fanout is why they own disk-based indexing (Chapter 8): one node per block read.
- **Heaps / priority queues:** O(log n) insert and extract-min; the engine inside Dijkstra, schedulers, top-k problems, and event simulations.
- **Stacks and queues:** LIFO/FIFO disciplines — call stacks, undo histories, BFS frontiers, work queues, backpressure buffers.
- **Graphs:** adjacency list (sparse) vs adjacency matrix (dense); the representation choice changes every operation's cost and memory by orders of magnitude.
- **Tries, bloom filters, disjoint-set (union-find), ring buffers:** specialized structures that each turn a specific expensive question into a cheap one — prefix lookup, probable membership with one-sided error, connectivity, fixed-size recent history.

**The selection method** is operational: list the operations the workload actually performs, their frequencies, and the size regime; then choose the structure whose cost profile matches. "We need fast lookup by id, occasional range scans by time, 10⁸ entries, mostly appends" selects a B-tree-family structure; "fast lookup only, 10⁴ entries, in memory" selects a hash map. Requirements first, nostalgia never.

**Invariants.** Every structure maintains invariants (heap property, BST ordering, red-black balance rules), and every bug in a structure is an invariant broken at one operation and discovered at another. Correct implementations state the invariant and check it in tests; concurrent structures add the question of *when* the invariant is observable (Chapter 15).

## Worked example

Implementing an LRU cache: requirements — get and put in O(1), evict least-recently-used. A hash map alone gives O(1) lookup but no recency order; a list alone gives order but O(n) lookup. The composition — hash map from key to node in a doubly linked list ordered by recency — gives both operations O(1) and eviction at the tail. This pattern (compose two simple structures so each covers the other's weakness) is the most reusable design move in the chapter.

## Failure mode

The default-container trap: reaching for the language's list/map for every shape of data, then discovering O(n) scans inside hot loops, or hash-map iteration order leaking into output and making tests flaky. And the exotic trap: implementing a sophisticated structure where a sorted array and binary search would be faster, smaller, and provably correct.

## Rule

> **Rule.** For every non-trivial collection in a design, name the three most frequent operations and their required bounds; the chosen structure must meet all three on paper before it is coded. If it cannot, compose structures or change the access pattern — do not hope the workload stays small.


---

# Chapter 4 — Programming Paradigms and Language Design

## Principle

A paradigm is a stance on the two questions every program answers: *where does state live*, and *how does control flow*. Languages embody answers — imperative, object-oriented, functional, logic, concurrent — and an agent that reads code across languages must recognize which stance a codebase has taken, because the idioms, the failure modes, and the safe refactorings all differ by paradigm.

## Substance

**Imperative/procedural:** programs as sequences of statements mutating state. Direct, close to the machine, and the mental model of C, Go, and shell. Its risk scales with shared mutable state.

**Object-oriented:** state encapsulated behind interfaces; behavior via message passing and polymorphism. The durable ideas are encapsulation and substitutability (Liskov: a subtype must be usable wherever its base type is — violations are bugs by definition). The cautionary canon: inheritance hierarchies that encode taxonomy instead of behavior, and the Gang of Four patterns (*Design Patterns*, Gamma et al., 1994) used as vocabulary for recurring shapes — factory, strategy, observer — not as a checklist to apply.

**Functional:** computation as evaluation of expressions; immutable data; functions as values; side effects quarantined. Its gifts to mainstream practice — map/filter/reduce, immutability by default, pure functions that are trivially testable — now appear in every modern language. Its core discipline: *referential transparency* (an expression can be replaced by its value) is what makes reasoning, caching, and parallelization safe.

**Declarative and logic:** state *what*, not *how* — SQL queries, regular expressions, build files, constraint solvers, Prolog. The engine owns the algorithm; the author owns the specification. Agents err here by writing imperative thinking in declarative clothing (row-by-row SQL cursors, regex used as parsers).

**Language design trade-offs** recur across all languages: static vs dynamic typing (Chapter 5), manual vs garbage-collected memory (Chapter 6), expressiveness vs analyzability, notation density vs readability. There is no best point on any of these axes — only fit between the language's stance and the problem's pressures. Polyglot fluency for an agent means: given a new language, first identify its choices on these axes, then write to its grain, not against it.

## Worked example

The same task in three stances — "count word frequencies in a corpus": imperative Python (a loop and a dict, explicit mutation), functional style (`collections.Counter` over a token stream — declarative composition), SQL (`SELECT word, COUNT(*) … GROUP BY word` — the engine picks the algorithm). All correct; each invites different extensions (streaming? distributed? incremental?) and different bugs (mutation during iteration; unbounded memory; a GROUP BY over an unindexed billion rows). The paradigm is chosen — or inherited — before the first line, and the choice propagates.

## Failure mode

 paradigm imperialism: forcing one stance everywhere — inheritance where composition fits, mutation-heavy code in a functional codebase, hand-rolled loops where a declarative query exists. In existing codebases the failure is subtler: writing against the grain of *this* codebase's paradigm, producing code that works and reads as foreign — which reviewers rightly reject.

## Rule

> **Rule.** Before writing in an unfamiliar codebase, name its dominant paradigm and its stance on state (mutable-shared, encapsulated, immutable) from the existing code, and match it. Introduce a different paradigm only as a deliberate, bounded, and stated decision — never by drift.


---

# Chapter 5 — Types and Formal Semantics

## Principle

A type is a claim about a value that a machine can check. Type systems exist on a spectrum from "checks nothing until runtime" to "proves absence of whole bug classes before execution," and every point on that spectrum trades the same currencies: earlier error detection against annotation burden, expressiveness against decidability. An agent needs types at two levels: as a *user* (reading signatures as the most compressed documentation there is) and as a *reasoner* (knowing what a given system can and cannot guarantee).

## Substance

**Static vs dynamic** is really *when* the check runs — compile time or run time — and therefore *which* errors are caught before users see them. Neither is "safer" absolutely: dynamic systems defer checks to tests; static systems pay in rigidity and in the temptation to encode everything in types until the types themselves need debugging.

**The vocabulary that matters everywhere:** type inference (the checker deduces types from use — ML-family, Hindley–Milner, the theory behind Haskell/OCaml and much of TypeScript's local inference); generics/parametric polymorphism (code written once over an abstract T, with the guarantee that it cannot inspect T beyond its declared bounds); algebraic data types and pattern matching (sum types — a value is one of a closed set of cases — plus exhaustiveness checking, which turns "forgot a case" into a compile error); subtyping and variance (when is a list of dogs a list of animals? — covariant for producers, contravariant for consumers, and getting it wrong is unsound); option/nullable types (making absence explicit instead of a null pointer exception — Hoare called the null reference his "billion-dollar mistake").

**Semantics** — what programs *mean* — comes in three classical styles: operational (meaning as machine steps; how most programmers think), denotational (meaning as mathematical functions), axiomatic (meaning as logical assertions — Hoare logic, pre/postconditions, the root of design-by-contract and formal verification). An agent rarely writes denotational semantics, but it uses the axiomatic style daily: every test is an executable fragment of a specification, every assertion a small Hoare triple {P} C {Q}.

**The limits are theorems, not moods.** By Rice's theorem (Chapter 1) no type system can check *all* interesting properties; practical systems check structural properties (shape, ownership, effect discipline in advanced systems like Rust's borrow checker — a type-level proof that memory is used safely, trading programmer effort for the elimination of use-after-free and data races by construction).

## Worked example

A function signature `parse(s: str) -> Result<Date, ParseError>` (in any language with sum types) carries five facts a comment would struggle to hold: input is text; output is a date *or* a structured error; failure is part of the contract, handled by the caller; the function is total (no exceptions promised); and the compiler will force every caller to confront the error case. Compare `parse(s)` in a dynamically typed style: all five facts still exist — they live in tests, docs, and production incidents instead. Types don't create the facts; they choose where the facts live and who checks them.

## Failure mode

Type-system theater: annotations that restate the obvious while the real contract (units, ranges, ordering, ownership) lives in comments — `timeout: int` that is sometimes seconds, sometimes milliseconds. And the mirror failure: treating a dynamically typed codebase as untyped, ignoring the de-facto types carried by tests, schemas, and validators at the boundaries. Every system has types; not every system writes them down.

## Rule

> **Rule.** Treat every function signature as a specification: name what the inputs may be, what the outputs can be (including failure), and what is invariant. Where the language cannot express a contract (units, ranges, ordering), put it in the name, the validation at the boundary, or a test — somewhere a machine or a reader will actually check it.


---

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


---

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


---

# Chapter 8 — Databases and Storage

## Principle

Storage is where a system's promises become permanent. The database chapter of an agent's education is about guarantees — durability, consistency, atomicity — and their prices, because every storage bug is a broken promise discovered later, usually by a user, usually at the worst time.

## Substance

**The relational model** (after Codd, 1970): data as relations — tables of tuples — manipulated declaratively (SQL), with the engine choosing access paths. Normalization removes update anomalies by removing redundancy; controlled denormalization buys read performance at the price of re-introducing them deliberately. Keys, foreign keys, and constraints are the schema enforcing invariants the application would otherwise have to — the same "where do facts live" question as types (Chapter 5), one level down.

**Transactions and ACID:** Atomicity (all or nothing — the remedy for partial writes), Consistency (invariants hold across the transaction), Isolation (concurrent transactions don't see each other's intermediate states — at a chosen level: read committed, repeatable read, serializable; the levels are a priced menu of anomalies prevented), Durability (committed means surviving a crash — paid for with fsyncs, Chapter 6). An agent must know which isolation level its code runs under and which anomaly that level *permits* (dirty reads, non-repeatable reads, phantoms, write skew) — the default is rarely serializable.

**Indexing:** a B-tree index turns a scan into a logarithmic lookup at the cost of write amplification and storage; a hash index trades ordering away for point lookups; composite indexes serve prefix queries in column order. The query planner chooses paths from statistics; "the query is slow" is usually "the planner lacked an index or fresh statistics," and the diagnostic instrument is the query plan (EXPLAIN), not intuition.

**The alternatives, honestly placed:** key-value stores (simplicity, scale, minimal queries), document stores (flexible records, weaker cross-record invariants), wide-column and time-series stores (access-pattern-shaped), object storage (immutable blobs, eventual semantics). The NoSQL trade is consistent: give up general queries and cross-record transactions, gain horizontal scale and schema flexibility. BASE (basically available, soft state, eventual consistency) is the honest label for what replaces ACID.

**Replication and consistency models** (Chapter 7's trade-offs made concrete): single-leader, multi-leader, leaderless; strong vs eventual consistency; read-your-writes and monotonic reads as session guarantees users actually notice when violated.

## Worked example

Two concurrent transfers debit the same account. Under read-committed, both read balance 100, both subtract 80, both commit "successfully" — final balance 20 or −60 depending on write order, and an overdraft the business forbids. The fixes, in ascending strength: an atomic conditional update (`UPDATE … SET balance = balance − 80 WHERE balance ≥ 80`, checking rows affected), a uniqueness/CHECK constraint in the schema, or a serializable transaction. The lesson generalizes: *concurrency correctness belongs in the storage layer's guarantees, not in application hope* — application code reading-then-writing across a gap is a race with extra steps (Chapter 15).

## Failure mode

N+1 queries (an ORM loop issuing a query per row — invisible in tests, fatal at scale); missing transactions around multi-write operations (crash = partial state); schema migrations deployed without a rollback story; assuming eventual consistency is immediate ("I wrote it, why can't I read it?"); and indexes added by superstition until writes crawl. Each is measurable with the planner and the slow-query log before it is an incident.

## Rule

> **Rule.** For every stored invariant (non-negative balances, unique emails, referential integrity), name the mechanism that enforces it — constraint, transaction isolation level, or atomic conditional write — at the storage layer. "The application checks first" is not a mechanism under concurrency.


---

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


---

# Chapter 10 — Software Design and Architecture

## Principle

Architecture is the set of decisions that are expensive to change: module boundaries, data ownership, dependency direction, the seams where parts can be replaced. Good architecture is not the absence of structure nor its maximization — it is structure placed exactly where change is expected, bought with complexity paid only there.

## Substance

**Cohesion and coupling** are the twin measures (after Constantine; popularized by *Code Complete*, McConnell): a module should do one thing completely (high cohesion), and modules should know as little about each other as possible (low coupling). Nearly every design smell is one of these failing: the god-object (cohesion collapsed), the shotgun change (coupling so high one fix touches twelve files).

**The durable patterns of structure:** layered architectures (dependencies point one way; the domain doesn't import the database), ports-and-adapters / hexagonal design (the core speaks interfaces; infrastructure implements them — the same instinct as Chapter 8's "invariants belong in storage"), dependency inversion (high-level policy must not depend on low-level detail), and the Gang of Four vocabulary (*Design Patterns*, 1994) for object-level recurring shapes. SOLID is the widely-taught mnemonic for five of these ideas; treat it as a checklist of questions, not commandments.

**Boundaries and APIs.** A system's real architecture is its boundaries: API contracts, data schemas, module interfaces. Design them for the consumer, version them deliberately, and assume every published contract becomes permanent (Hyrum's Law: with enough users, every observable behavior — including bugs — becomes depended upon). Conway's Law completes the picture: systems mirror the communication structure of the organizations that build them, so boundaries between teams become boundaries between components whether planned or not.

**Trade-off literacy.** Architecture is the management of quality attributes that fight each other: consistency vs availability (Chapter 7), coupling vs duplication (a little duplication is cheaper than the wrong abstraction — after Sandi Metz's formulation), generality vs simplicity, build vs buy. The senior skill is naming the trade-off being made *in the decision record*, so the future reader knows what was knowingly spent.

## Worked example

A reporting feature needs user data. Options: (a) query the user service's database directly — fastest to write, couples reporting to the user schema forever, breaks when the user team migrates; ( (b) call the user service's API — a boundary, versioned, slower per call, and the reporting feature survives the migration. The architectural content is not the code (both are a dozen lines) but which future changes each option makes cheap or expensive. Architecture reviews exist to price exactly this.

## Failure mode

Resume-driven design (architectures chosen for novelty), premature abstraction (generalizing from one example — wait for the third occurrence; the rule of three), the distributed monolith (microservice boundaries with monolith coupling — both costs, neither benefit), and architecture astronautics: layers that exist to display structure while the actual data flow sneaks around them.

## Rule

> **Rule.** For every new boundary or abstraction, write down which anticipated change it makes cheaper and what it costs today. If no anticipated change can be named, build the simple thing; the abstraction can be extracted when the second concrete case exists — and not before the third demands it.


---

# Chapter 11 — Testing and Verification

## Principle

Tests are executable specifications: the part of the specification that cannot drift out of date without turning red. Their purpose is not confidence in the abstract — it is *change safety*: a suite that catches regressions lets a codebase move fast; a suite that doesn't is a ritual. Verification is broader than testing (it includes static analysis, review, and proof), and Chapter 1 sets the ceiling: for arbitrary programs, testing can show the presence of defects, never their absence (after Dijkstra's famous dictum). Tests sample behavior; the craft is in choosing the sample.

## Substance

**The pyramid:** many fast unit tests (one component, milliseconds), fewer integration tests (components together, real boundaries), few end-to-end tests (the whole system, slow and brittle). Inverting the pyramid — mostly end-to-end — yields suites that are slow, flaky, and vague about what broke.

**The working techniques:** equivalence partitioning and boundary values (errors live at edges: 0, 1, max, empty, null); property-based testing (state an invariant — reversing twice is identity, sorting preserves multiset — and let a generator hunt counterexamples; QuickCheck, after Claessen & Hughes, 2000, and its descendants); fuzzing (random/mutated inputs at scale — the most productive bug-finder in modern security history for parsers and protocols); test doubles used honestly (stubs return values, mocks verify interactions — over-mocking tests the mock, not the system); mutation testing as the suite's own quality metric (inject small faults; a suite that doesn't catch them has coverage theater, not coverage).

**Coverage** measures what executed, not what was *checked*. 100% line coverage with no assertions is 0% verification. The metrics that matter: does the suite fail when the behavior is deliberately broken (mutation), and does it cover the *requirements'* edge cases, not just the code's lines?

**Test design for agents specifically:** tests are the feedback signal the whole agentic loop steers by (Part III). A target test must be *decisive* (fails before, passes after, for the right reason), *fast* (run after every change), and *honest* (never edited to pass — a modified test is a changed specification and must be treated as a product decision, not a fix).

## Worked example

Bug report: "discount applies twice on retry." The verification-first workflow: write the failing test first — a reproduction that submits the operation, retries it, and asserts one discount — watch it fail (proving the test detects the bug), then fix, watch it pass, and check the neighboring tests still pass (the regression suite's job). The test outlives the fix: it is the bug report made executable, immune to the fix being reverted or the bug being reintroduced by an unrelated change. Fix-without-repro is the anti-pattern: no proof the bug is understood, no guard against its return.

## Failure mode

Flaky tests (order-dependence, timing, shared state — each flake trains the team to ignore red, which is the suite's death); testing implementation instead of behavior (tests that break on every refactor teach nothing and cost everything); the ice-cream-cone suite; and asserting on incidental output (timestamps, ordering, addresses) — brittleness disguised as thoroughness.

## Rule

> **Rule.** Every behavior change ships with the test that would have failed without it, and every defect fix ships with the reproduction that failed before it. A test that has never been seen to fail is assumed decorative until proven otherwise.


---

# Chapter 12 — Debugging Method

## Principle

Debugging is the scientific method applied to a misbehaving artifact: observe, hypothesize, predict, experiment, conclude. The skill is not intuition — it is discipline under frustration: change one variable at a time, believe the evidence over the theory, and treat every "impossible" observation as information about your model of the system, not about the system's sanity.

## Substance

**The loop:** (1) *Reproduce* — a bug you cannot reproduce you cannot fix, only chase; build the smallest reliable reproduction before touching the code (the repro is also the regression test, Chapter 11). (2) *Reduce* — bisect the input, the configuration, the history, until the reproducer is minimal; `git bisect` automates this against history (the first bad commit is a fact, not a suspicion). (3) *Hypothesize* — name a mechanism, not a location: "the cache returns the stale entry because the key omits the locale" predicts specific observations; "something's wrong in caching" predicts nothing. (4) *Experiment* — instrumentation over staring: logs, assertions, debugger breakpoints, sanitizers; design the experiment so both outcomes are informative. (5) *Conclude and generalize* — after the fix, ask what class this bug belongs to and where else the class lives.

**The canonical tactics** (the tradition runs from Kernighan & Pike, *The Practice of Programming*, through Zeller, *Why Programs Fail*): divide and conquer; work backwards from the failure; check the plug (the embarrassing basics — wrong environment, stale build, wrong file — are statistically the most common causes); rubber-duck explanation (articulating the expected behavior precisely exposes the wrong assumption); printf's honest cousin, the structured log with timestamps and correlation ids; and the differential method — find two environments/inputs/versions that differ in outcome and interrogate the difference.

**Heisenbugs and the observer effect:** bugs that vanish under observation (races, timing, uninitialized memory) demand recording over inspection — flight recorders, core dumps, deterministic replay, sanitizers — because the instrument must not change the phenomenon.

## Worked example

Intermittent failure: one request in a thousand returns the previous user's data. Hypotheses ranked by mechanism: shared mutable state across requests (a module-level cache keyed badly); connection-pool object reuse; a race in session lookup. The discriminating experiment is not reading the code harder — it is adding the user id and the serving object id to the response log for an hour and correlating: failures sharing an object id with the previous request convict the pool; failures sharing a key convict the cache. One hour of data beats a week of code reading, because the bug is *intermittent* and code reading samples the same distribution the bug hides in.

## Failure mode

Shotgun debugging (multiple simultaneous changes — when it "works," nobody knows why, and one change is usually a regression in waiting); fixing the symptom at the observation point (retrying, catching-and-ignoring, sleeping 100ms "to let it settle"); anchoring on the first plausible theory and explaining away contrary evidence; and the sunk-cost loop — the third hour on a hypothesis the data rejected in the first.

## Rule

> **Rule.** No fix without a reproduction; no conclusion without an experiment whose outcome could have changed your mind. If two consecutive experiments fail to discriminate, widen the observation (more logging, a sanitizer, a bisect) instead of deepening the theory — the deficit is data, not cleverness.


---

# Chapter 13 — Security

## Principle

Security is the property that a system behaves as intended *in the presence of an adversary* — an intelligent opponent who reads the code, chooses inputs maliciously, and profits from the difference between what the author assumed and what the system permits. Correctness reasoning assumes a indifferent universe; security reasoning assumes a hostile one. This changes everything about how code must be written and reviewed.

## Substance

**The foundational habits:** validate and encode at boundaries — injection (SQL, command, template) exists wherever untrusted data is concatenated into a language, and is killed by parameterization/escaping, never by blocklists; authentication (who are you) is not authorization (what may you do) — check both, server-side, on every request; least privilege (each component, token, and account gets the minimum it needs — the blast radius principle); secrets are credentials, not data — never in code, never in logs, never in version control, rotated and scoped; cryptography is used, never invented — vetted libraries, standard constructions, and paranoia about the surrounding protocol, where real-world failures actually live.

**The standard taxonomies** give the field its checklist: the OWASP Top 10 for web applications (broken access control, cryptographic failures, injection, insecure design, misconfiguration, vulnerable components, auth failures, integrity failures, logging failures, SSRF); STRIDE for threat modeling (spoofing, tampering, repudiation, information disclosure, denial of service, elevation of privilege); CWE for weakness classes. Use them as coverage instruments — a design review that walks STRIDE per component finds what ad-hoc worry misses.

**The deep principles:** defense in depth (no single control is load-bearing); fail closed (on error, deny — the default that matters is the one taken when the check itself crashes); complete mediation (check every access, not every session); the trusted computing base is everything whose compromise breaks the guarantee — keep it small and audited; and attackers think in graphs while defenders think in lists (after John Lambert): the defender patches entries, the attacker chains them.

**Supply chain** is the modern surface: dependencies are code you run with your privileges — pin them, audit them, watch their advisories; the build pipeline is part of the trusted base (reproducible builds, signed artifacts, provenance attestations are the accountability patterns of Chapter 24 applied to software itself).

## Worked example

A search feature builds a query by string concatenation: `"... WHERE name = '" + input + "'"`. Input `' OR '1'='1` returns every row; input with a UNION exfiltrates other tables. The fix is not filtering quotes (attackers encode around filters forever) but *parameterized queries*, which separate code from data structurally — the driver sends the query shape and the values on different channels, so no input can ever become syntax. The generalization: injection is a category, not an instance — SQL, shell commands, HTML (XSS), LDAP, template engines — and in every case the cure is the same shape: never let data cross into code without a structural boundary.

## Failure mode

Security by obscurity (secret URLs, hidden fields — discovered, not protected); client-side enforcement (checks in JavaScript the attacker doesn't run); rolling your own crypto or auth; logs full of credentials; and the philosophical failure — reviewing for bugs but not for abuse cases: "what would I do with this feature if I were hostile?" is a different question from "does this feature work?"

## Rule

> **Rule.** For every input boundary, name the language the data could enter (SQL, shell, HTML, path, query) and the structural mechanism that prevents it from becoming code there. For every privileged action, name the server-side authorization check. A review that finds neither named is a review that did not cover security, whatever else it covered.


---

# Chapter 14 — Performance and Optimization

## Principle

Performance work is measurement work. The universal law of optimization: *profile first* — the bottleneck is almost never where intuition points, because programmers (and models) reason about the code they wrote most recently, not the code the machine spends time in. Amdahl's Law sets the ceiling: speeding a component that consumes fraction p of runtime by any factor improves the whole by at most 1/(1−p). Optimizing a 5% component perfectly buys 5%.

## Substance

**Where time actually goes:** the memory hierarchy dominates modern performance. Registers ~1 cycle, L1 cache ~4, L2 ~12, main memory ~100+, disk/network orders beyond. An algorithm with worse asymptotics but sequential access routinely beats a "better" one with pointer-chasing random access. Data layout (arrays of structs vs structs of arrays), cache-line awareness, and avoiding allocation in hot paths are worth more than clever instruction choices. Measure with profilers (sampling for the broad picture, instrumentation for the exact one) and hardware counters where the question is microarchitectural.

**The method:** (1) measure the baseline end-to-end, with realistic data, and write the number down; (2) profile to localize; (3) form a hypothesis ("this is O(n²) over the user table"); (4) change one thing; (5) re-measure against the same harness; (6) keep or revert by the number. Benchmarks need the same rigor as experiments (Chapter 22): warm-up, variance reporting, identical conditions, and suspicion of any result too good to be true (dead-code elimination eating the benchmark is the classic).

**The common real wins,** in the order they usually matter: fix the algorithm (Chapter 2); fix the data access (index the query, batch the calls — N+1 queries and chatty APIs are the production performance bugs, Chapter 8); cache with an explicit invalidation story; remove work (the fastest code is code not run — memoization, laziness, short-circuits); parallelize only after the serial profile is understood (Chapter 15) — parallelizing an I/O-bound or lock-bound workload multiplies contention, not throughput.

**Throughput vs latency** are different objectives with different enemies: throughput loves batching and queues; latency (especially tail latency, p99) hates them. State which one the system is for before optimizing either.

## Worked example

A dashboard endpoint takes 3 seconds. Intuition says the rendering code; the profile says 2.7 s in database calls — specifically 340 queries for one page (an ORM traversing relations per row). The fix is one eager-loaded query: 3 s → 120 ms, a 25× win from *removing round trips*, zero algorithmic cleverness. The counterfactual fix — optimizing the template engine — was measured to be worth at most 8%. This distribution (one boring structural cause taking ~90% of time) is the norm, and it is invisible without the profile.

## Failure mode

Optimizing unmeasured code; micro-optimizing a cold path while the hot path allocates in a loop; caching without invalidation (trading a performance bug for a correctness bug, the worse bargain); benchmark gaming (results that exist only in the benchmark); and premature optimization as a personality trait — complexity spent where no profile asked for it, paid by every future reader.

## Rule

> **Rule.** No performance claim without a before/after measurement on the same harness with the same data, and no optimization merged whose measured end-to-end effect is inside the noise. If the profile doesn't indict a component, the component is innocent — whatever it looks like.


---

# Chapter 15 — Concurrency

## Principle

Concurrency is the discipline of correctness when events interleave. Its central difficulty: between any two operations of one thread, any number of operations of another may occur — so sequential reasoning silently stops applying, and bugs become nondeterministic, rare, and load-dependent. Parallelism (doing things at once for speed) is one motive; concurrency (structuring for independent activities) is the broader one, and it is paid for in reasoning.

## Substance

**The failure vocabulary:** a *race condition* — outcome depends on interleaving; the *data race* — unsynchronized concurrent access with at least one write (undefined behavior in low-level memory models); the *atomicity violation* — a check-then-act sequence (`if (balance >= x) withdraw(x)`) whose premise expires between check and act; *deadlock* — a cycle of threads each waiting for the next (prevented by lock ordering: acquire in a globally fixed order); *livelock and starvation* — motion without progress, and progress denied; *priority inversion*.

**The tools, in ascending power and danger:** immutable data (no sharing, no problem — share freely); message passing / actor models (share by communicating — Go's proverb: "don't communicate by sharing memory; share memory by communicating"); locks/mutexes (correct, composable poorly, deadlock-prone); lock-free structures and atomics with explicit memory orderings (expert territory — the memory model, e.g. the C++ or Java model, defines which reorderings are legal and what `volatile`/acquire/release actually promise); software transactional memory and structured concurrency (scope-bound lifetimes for tasks — the modern answer to leaked threads: a task's children cannot outlive its scope).

**Async is not parallel:** an event loop gives concurrency (many in-flight I/O operations) on one thread — no data races on the heap, but interleavings at every `await`, so check-then-act bugs survive the translation and must be reasoned about identically.

**Testing concurrency** requires adversarial instruments: stress runs, deterministic-scheduler testing (exploring interleavings systematically where the platform allows), thread sanitizers, and the humility that a passing test proves almost nothing — races hide in schedules, not in code paths, and the schedule space is astronomically larger than any test run.

## Worked example

A counter incremented by 100 threads × 1,000 increments each returns 97,412. The mechanism: `count++` is read-modify-write, not atomic — two threads read 50, both write 51, one increment is lost; thousands of collisions later, the total is short. Fixes at three levels: an atomic counter (hardware-level); a lock around the increment (correct, serializes); or restructure so threads never share (per-thread counters, summed at the end — fastest, and the design lesson: *the best synchronization is the one the architecture makes unnecessary*).

## Failure mode

Synchronizing the obvious variable while the invariant spans three; locking inconsistently ordered across code paths (deadlock under the one schedule production finds); holding locks across I/O or calls into unknown code; "fixing" a race with a sleep; and volatile-as-synchronization superstition in memory models where it doesn't mean that.

## Rule

> **Rule.** Every piece of shared mutable state in a design names its synchronization discipline (immutability, ownership by one thread, a named lock, an atomic with stated ordering) — and every check-then-act sequence over shared state is presumed a race until the discipline shows otherwise.


---

# Chapter 16 — Version Control and Collaboration

## Principle

Version control is the team's shared memory and time machine: every change recorded with its author, its moment, and — if the team writes them — its reasons. For an agent, version control is also the primary *safety instrument*: work happens in increments that can be inspected, compared, and reversed. A change that cannot be described as a diff cannot be reviewed; a change that cannot be reverted cannot be risked.

## Substance

**The model that matters** (Git, the dominant instance): commits are snapshots in a directed acyclic graph; branches are movable pointers; merging reconciles lines of development; the working tree, the index, and HEAD are three distinct states (most beginner confusion is conflating them). History is a designed artifact: atomic commits (one logical change each) make review, bisection (`git bisect`, Chapter 12), and reversion mechanical; tangled commits make all three archaeology.

**The collaboration protocol:** work on branches; propose changes as reviewable units (pull/merge requests) with a description that states intent, evidence, and risk; review is a verification activity (Chapter 11), not a style tribunal — the reviewer's questions are "is this correct, is this tested, is this the right boundary, can this be reverted"; continuous integration runs the suite on every proposal so "green" is a property of the change, not of someone's machine.

**Hygiene with teeth:** commit messages that say *why* (the what is in the diff); never commit secrets (Chapter 13 — history remembers what working trees forget, and rotation, not deletion, is the remedy); small changes over large ones (review quality collapses with size — a 1,000-line change gets a 1,000-line skim); and protected files discipline — configuration and test infrastructure changes ride in their own commits, visibly, because they alter what "passing" means for everyone.

## Worked example

A regression appears somewhere in 400 commits since the last release. `git bisect` with an automated test performs a binary search over history: ~9 test runs localize the exact introducing commit, whose diff — being atomic — shows the precise mechanism. The same hunt without atomic history is a week of suspicion. Bisectability is not a luxury feature; it is the debugging method's infrastructure, and it is purchased entirely by commit discipline exercised months earlier.

## Failure mode

The mega-commit (a feature, two fixes, and a refactor in one — unreviewable, unrevertable, unbisectable); committing generated artifacts and editor noise until the diff lies about the change; force-pushing shared history (rewriting the team's memory under their feet); and review theater — approvals without reading, which convert the safety instrument into a signature formality.

## Rule

> **Rule.** Every commit is one logical change with a message stating its reason, small enough to be reviewed in full and reverted without collateral. Any change a reviewer cannot fully read is, by definition, too large — split it before asking for review.


---

# Chapter 17 — Documentation and Readability

## Principle

Code is read far more often than it is written — by reviewers, by future maintainers, by debugging sessions at 3 a.m., and by agents, whose entire perception of a codebase is its text. Readability is therefore not aesthetics; it is the bandwidth of the channel through which every other engineering activity flows. Documentation's job is narrower than people think: record what the code *cannot say* — intent, reasons, constraints, history — and let the code say the rest.

## Substance

**Naming** is the highest-leverage readability act: names that carry the contract (units, ranges, semantics — `timeout_seconds`, not `timeout`), consistency that lets readers pattern-match across the codebase, and honesty (a function named `get` that writes is a lie told to every future reader). **Structure** follows: small functions with one level of abstraction each; code laid out so the common path reads top-to-bottom; comments that explain *why* (the constraint, the workaround's reason, the citation) rather than narrating *what* the next line plainly does — comments that duplicate code rot into falsehoods, and a stale comment is worse than none because it is believed.

**The documentation layers,** each with a distinct job: docstrings/API docs (the contract at the point of use); README (the on-ramp: what this is, how to run it, where things live); architecture records (ADR-style: decision, context, alternatives rejected and why — the institutional cure for re-litigating settled questions and for "why is it like this?" archaeology); changelogs (what changed for consumers, in their terms); and runbooks (operational knowledge for the failure case, written before it happens).

**For agent readers specifically:** machine-legible structure is a kindness with measurable returns — consistent file organization, explicit invariants stated near the code they constrain, tests that double as usage examples, and errors whose messages name the violated expectation. An agent reading a codebase samples it under a budget (Part III); documentation that front-loads architecture and invariants converts that budget from archaeology into work.

## Worked example

Two implementations of a retry helper. The first is forty lines with a comment `// retry logic`. The second is forty lines with a header: "Retries *idempotent* calls only. Backoff: exponential, base 200 ms, jitter ±50%, max 5 attempts, total budget 30 s. Non-idempotent callers must pass an idempotency key (Chapter 7). Chosen after incident review showed synchronized retries amplifying an outage." The second header prevents three distinct future bugs (retrying a payment, removing the jitter, raising attempts unboundedly) — none of which the code itself could prevent, because each bug consists of *changing the code while misunderstanding it*. That is documentation's precise function: transmitting the constraints that are invisible in the artifact.

## Failure mode

Documentation that paraphrases code and drifts; aspirational docs describing the system that was planned; README archaeology (five generations of setup instructions, one of which works); comment-to-code ratio worship; and its opposite — the "code is self-documenting" dogma applied to systems whose key facts (why this threshold, why this order, what breaks if changed) exist nowhere in the code at all.

## Rule

> **Rule.** Every non-obvious decision in code carries its reason at the point of decision — the constraint, the rejected alternative, or the citation. If a future change could be made wrongly *while reading the code correctly*, the missing fact belongs in a comment, a test name, or a decision record before the change ships.


---

# Chapter 18 — Agent Loops and Tool Use

## Principle

An agent is a loop, not a model: perceive through tools, decide, act through tools, observe the result, repeat under a budget until a stopping rule fires (this generalizes Chapter 1's foundations to the working agent). The model supplies decisions; the loop supplies everything that makes decisions *consequential and checkable* — observations, state, tools, budget, termination. When an agent fails, the failure belongs to a named loop component before it belongs to "the model."

## Substance

**The canonical loop is ReAct** (after Yao et al., 2022): reasoning and acting interleaved, each action conditioned on the observations previous actions returned. Refinements build on it: **Reflexion** (after Shinn et al., 2023) adds verbal self-feedback stored across attempts — the agent writes down what it concludes from a failure and carries the note into the next try; **plan-and-execute** separates a planner that decomposes the task from executors that run the steps (cheaper per step, weaker at recovery when the plan meets reality); **tree/search-based** agents (Tree of Thoughts, after Yao et al., 2023) explore multiple candidate paths with explicit evaluation — paying compute for decision quality where decisions are expensive to reverse.

**Tool use is an interface discipline.** Tools are functions with names, typed arguments, and structured results. What makes them usable by a model: small, composable surfaces (a read tool, an edit tool, a run tool — not forty flags on one mega-tool); results that are complete but bounded (truncated with the truncation *announced*); errors returned as structured observations the model can act on, not as crashes that end the run; and idempotency where the world allows it, because agents retry. The agent–computer interface (after SWE-agent, Yang et al., 2024) is measured to matter as much as the model: how files are presented, how edit confirmations read, how output windows are sized — these are agent-quality decisions.

**State** is what the loop remembers outside the model's head: working notes, enumerated target lists, checkpoints (a known-good state to retreat to), and the trace itself — the complete record of calls and observations, which is both the debugging instrument and, in accountable systems (Chapter 24), the audit artifact.

**Budgets are part of the architecture,** not an operational afterthought: call budgets, token budgets, wall-clock budgets — with defined behavior at exhaustion (submit the best verified state; never leave the run's product unextracted). An agent without an exhaustion behavior has a failure mode shaped like a cliff.

## Worked example

A coding agent fixing a failing test, loop by loop: observe (the test failure output, quoted exactly) → hypothesize (three ranked root-cause candidates, written down) → act (read the implicated function, not the whole file) → observe (the code contradicts hypothesis #1) → act (write a failing reproduction; run it; it fails as predicted — the hypothesis now has evidence) → edit → run the target tests → the repro passes, one neighboring test regresses → diagnose (the fix was too broad) → narrow the edit → all green → submit. Every step's observation changed the next decision; nothing was believed without a tool returning it. That trace, read afterward, is the difference between an agent and a text generator with permissions.

## Failure mode

The open-loop failure: long sequences of actions taken from the initial plan without intermediate observation (the agent "executes" a script in its head and discovers reality only at the end). Tool misuse follows: calls with hallucinated names or arguments (a symptom of a surface the model couldn't internalize), retrying a failed call verbatim (the definition of loop-thrash), and silent tool failure — treating an error result as a success observation and building on it.

## Rule

> **Rule.** Every action in an agent run must be preceded by an observation that justifies it and followed by an observation that judges it. A run whose trace contains long action sequences with no intervening observations is operating open-loop, and its outputs are unverified by construction — whatever they look like.


---

# Chapter 19 — Harness Design

## Principle

The harness is everything around the model — runner, sandbox, tool implementations, prompt assembly, budget enforcement — and it, not the model, decides which disciplines are real. The governing distinction of this chapter: **enforcement versus exhortation.** A rule the model is *asked* to follow is choreography; a rule the harness *enforces* is mechanism. Choreography can be skipped, forgotten under context pressure, or complied with in form while violated in substance — silently, every time. A check the model invokes on itself is choreography, not enforcement, no matter how sternly the prompt phrases it.

## Substance

**Three enforcement levels, named so claims can be priced:**

- **Level 0 — exhortation.** The instruction lives in the prompt. Compliance is a per-turn decision by the model. Useful for judgment (style, priorities, strategies); worthless as a guarantee for invariants.
- **Level 1 — artifact-binding.** The discipline produces inspectable artifacts (recorded test runs, hashes, structured checklists) so that non-compliance is *visible* in the trace after the fact. This deters nothing in the moment but makes evaluation honest: the checker can score whether the discipline happened.
- **Level 2 — gating.** Code outside the model's control refuses the action until preconditions hold — a submission is rejected until target-test evidence for the current artifact exists; a spend is refused until a mandate check passes. Denials are named, logged, countable events.

**Not every platform permits Level 2.** Many agent frameworks (and most competition harnesses) are declarative: the author supplies configuration and prompts; the only author code runs as tools *the model chooses to invoke*. On such a platform there may be no hook at action time — no callback at submit, no interceptor on tool calls — and any "gate" authored as a tool is Level 0 in uniform. The honest responses are: implement Level 1 and label it as such; put enforcement in whatever runner code the author *does* control (their own evaluation harness, their own production wrapper); or change platforms. The dishonest response — documenting choreography as enforcement — corrupts every downstream decision that trusts it.

**Engagement is measured or it didn't happen.** Every mechanism must emit trace evidence of its own operation (a sampling step logs its candidates; a gate logs its verdicts), and every evaluation must check engagement *before* interpreting outcomes. A mechanism that never fires produces runs that look like evidence against the idea and are actually evidence about the wiring. Instrument first; conclude second.

**Sandboxing is the harness's other half:** isolated workspaces per task, no network unless the task demands it, resource ceilings (CPU, memory, time) enforced by the platform, and a clean, reproducible initial state — because an agent evaluated in a polluted environment produces numbers about the pollution.

## Worked example

A team builds a "pre-submit verification gate" as a tool the agent should call before submitting, instructed firmly in the prompt. In evaluation, scores don't move. Trace inspection finds the gate was invoked in a minority of runs and its denials were overridden by the agent in most of those — the agent treated the gate as advice. Rebuilt as a harness rule (submission rejected unless the run record contains a passing target-test execution against the current diff), the same discipline becomes real: denials appear in traces as events, agents adapt by running tests earlier, and the mechanism's effect becomes measurable for the first time. The idea didn't change. The enforcement level did.

## Failure mode

Oversold choreography (documentation claiming guarantees the platform cannot provide); silent non-engagement (mechanisms consuming prompt budget while never firing); and gate-gaming — an agent that learns to produce the *artifacts* of compliance (a test run against a stale diff, a checklist filled pro-forma) when the gate checks artifacts rather than facts. Gates must bind to the current artifact — hash the diff the evidence claims to cover, or the evidence is decorative.

## Rule

> **Rule.** For every discipline a system claims, publish its enforcement level and the trace evidence that proves engagement. A claim of Level 2 is falsified by a single completed run that violated the discipline without a recorded denial; a mechanism with no engagement evidence in traces is reported as *not measured*, never as *working*.


---

# Chapter 20 — Context Engineering

## Principle

A language model's context window is its entire working memory: everything it can consider is what's in the window, and everything in the window competes for its attention and its budget. Context engineering is the discipline of deciding what enters, in what form, in what order, and what is deliberately kept out or externalized — the prompt is a designed artifact, not a transcript that happens to accumulate.

## Substance

**The budget is real and compositional.** System instructions, tool definitions, task statement, observations, history, and the model's own reasoning all draw from the same finite window (tens of thousands of tokens in small-model settings; more in frontier ones — the discipline is identical, only the numbers change). Serving stacks manage overflow by compaction — summarizing or dropping history — which means *the system will forget on your behalf if you do not choose what is forgotten*. Load-bearing facts (the exact failing assertion, the enumerated target list, the current plan and its status) must live in external artifacts the agent re-reads — notes, files, structured state — not only in history that compaction can take.

**Selection beats volume.** Retrieval (search by the literal error string, by symbol, by similarity) exists to put the *relevant* slice in front of the model: function-level reads rather than whole files; the failing test and its fixtures rather than the suite; neighbors of the code under change rather than the repository. Reading order matters: specification (tests) before implementation before surroundings. Every irrelevant token admitted taxes attention and evicts, eventually, a relevant one.

**Structure helps the model use what it has:** stable instruction placement (system material first, where models weight it), clear delimiters between instruction, data, and observation (untrusted content must be *formatted* as data — prompt injection is what happens when the boundary fails), summaries that preserve decisions and discard transcripts, and just-in-time loading (fetch detail when the decision needing it arrives, not speculatively at the start).

**Context failure has names:** *overflow* (the window is exceeded and the run dies or truncates mid-thought); *rot* (early decisive facts are compacted away and late behavior degrades into re-derivation and contradiction); *poisoning* (irrelevant or adversarial content crowds out the task); *lost-in-the-middle* (empirically, models underuse information buried mid-context — after Liu et al., *Lost in the Middle*, 2023 — so placement is a quality decision, not cosmetics).

## Worked example

An agent debugging a failure reads the full 1,800-line module, the full test file, and three full neighboring files "for context" — 60% of its window gone before its first hypothesis. The decisive line (the assertion in one test) sits in the middle of that mass. It then re-reads two of the files after compaction discards them, spending budget to recover what it already paid for once. The disciplined run: search the error string; read the failing test (40 lines) and its fixture; read the implicated function (60 lines) and its callers; write the hypothesis and target list to notes. Same task, a tenth of the context, and the window still holds room for the repair iterations — which are where tasks are actually won.

## Failure mode

The maximal-read anti-pattern ("include everything, to be safe"); trusting auto-compaction to preserve the one number that matters; treating retrieved text as instruction (injection); and its quiet cousin — letting tool output formats bloat (verbose JSON, repeated headers, stack traces with no signal lines) until the observation channel is mostly noise.

## Rule

> **Rule.** Every run maintains its load-bearing state — target list with current status, exact failure text, current plan — in an external artifact re-read after any compaction. A trace in which the agent re-derives or contradicts state its own earlier observations established is a context-discipline failure, charged to the harness design, not to the model's memory.


---

# Chapter 21 — Verification and Selection

## Principle

An agent's outputs are claims. A patch claims to fix the issue without breaking its neighbors; an analysis claims a root cause; a summary claims fidelity to its source. Verification is the discipline of converting claims into evidence *by execution*: the patch is run against the enumerated tests; the root cause is probed by a reproduction; the summary is checked against the text. Nothing is believed because it is plausible — and in agentic systems plausibility is the failure mode, because fluent output is the model's native product.

## Substance

**Enumerate the targets before the work.** For a coding task the target set is explicit: the tests that must turn green (fail-to-pass) and the tests that must stay green (pass-to-pass). Work without a named target set cannot be verified, only admired. The reproduction comes first: a failing test or minimal script that demonstrates the defect *before* any edit — it proves the defect is understood, gives the fix a finish line, and becomes the regression test afterward (Chapter 11).

**Executed proof or it doesn't count.** The selection rule for agent outputs: when multiple candidate solutions exist, keep the one *verified by execution* — not the first, not the most confident, not the most elegant. This operates at three scales: within a run (candidate patches executed against target tests, selection by outcome); across runs (the best *verified* checkpoint is what submits when budget expires); and in training data (Chapter 23: only trajectories with executed proof are admitted). The rule's strength is its indifference to source: a candidate from a weak model that passes outranks a candidate from a strong model that wasn't run.

**Verify the path, not a model of the path.** A recurring verification failure is testing a *representation* of the system — a probe, a reimplementation, a generic version of the library — and reporting the result as a fact about the production system. Versions differ in caps, defaults, and edge behavior; a result about the generic path is a hypothesis about the production path. Where the two can diverge, the divergence must be checked, and claims must name the exact artifact, version, and path they were measured on. A claim found to describe the wrong path is withdrawn, not footnoted — because downstream decisions priced it as true.

**Distrust status channels.** Wrappers lie politely: a job runner reporting "success" for a cell whose subprocess died; a submission system whose confirmation regex matches the page's own marketing text; a monitor that reports a component's *silence* as a pass. Verification means reading the artifact (the output, the exit code, the produced file, the live state) — never the summary of the artifact. A sensor that did not run reports *absent*, not *fine*.

## Worked example

Candidate selection on a bug-fix task: the agent generates three candidate patches from three ranked hypotheses. Candidate 1 is the model's favorite — clean, minimal, confident. Executed: it fails one target test. Candidate 2 is uglier — an extra guard clause — and passes all targets with no regressions. Candidate 3 was never run because budget remained for only two evaluations. The executed-proof rule submits candidate 2 and logs candidate 1's failure as information (the favored hypothesis was wrong — exactly the kind of fact that must survive into the record, because it corrects the *next* task's priors). A workflow that ships candidate 1 on confidence has replaced verification with vibes at the exact point where verification was cheapest.

## Failure mode

Verification theater: running tests that are not the target tests; reporting "tests pass" from a run that executed a stale build; accepting a status field instead of the artifact; verifying a model of the system and reporting it as the system; and the selection failure — keeping the first adequate-looking candidate and never executing the comparison that would have ranked it last.

## Rule

> **Rule.** Every claim an agent emits carries its executed evidence: the exact command or test set, the exact target list, and the observed result, on the exact artifact and version claimed. A claim whose evidence was gathered on a different path than the claim describes is withdrawn in the same document that carried it.


---

# Chapter 22 — Evaluation and Measurement

## Principle

Agent programs improve by measurement or merely change. Evaluation is a scientific instrument pointed at your own system, and it obeys the rules of instruments: a frozen test set, a defined metric, pre-registered comparisons, and a noise floor below which differences are not differences. Without those, "improvement" is a narrative genre.

## Substance

**The benchmark is the contract.** SWE-bench (after Jimenez et al., 2024) defined the modern shape: real repository issues, a fixed base commit, patches applied and judged by test execution — resolved if and only if the fail-to-pass set passes and the pass-to-pass set holds. Benchmarks earn trust through frozen membership, hermetic execution (fresh environment per task, no network leakage), and a resolution definition that cannot be negotiated per task. Contamination — benchmark items or their solutions leaking into training data or prompts — converts the instrument into a mirror; guarding the split (a frozen *holdout* never tuned on, reserved for confirmation reads) is an integrity rule, not a preference.

**Pre-registration for agent experiments:** before the run, write down the primary metric (usually resolution rate), the secondaries (cost per task, calls, per-task flips), the single variable being changed, and the ship criterion. One variable per comparison — two changes and one number yields two suspects. Differences must clear a **signal threshold** sized to the bench: on n=20, one task is 5 percentage points and flips by chance constantly; a working rule is ≥2 tasks before a difference is treated as signal at that scale, scaling proportionally at other n. A one-task difference is recorded as *no detectable effect* — which is a real result, distinct both from "proven zero" and from "it works."

**Cost is a metric.** Resolution at unbounded cost is a demo. Report calls, tokens, wall-time, and dollars per resolved task alongside the rate; a configuration that wins +1 task at 3× cost may be a trade, or a loss, but it is not a free win. Also report **engagement metrics** for internal mechanisms (Chapter 19): candidates sampled, gates fired, repairs attempted — the numbers that distinguish "the idea failed" from "the idea never ran."

**Variance is real:** sampling temperature, task ordering, and environment jitter make single runs anecdotes. Repeat decisive comparisons, use identical configurations for control and treatment (hash them; "identical except" must be provable), and log every tried configuration with its outcome — an unrecorded tune is a rumor the next engineer will pay to re-test.

## Worked example

A team adds a sophisticated multi-step prompt protocol and measures +1 task on their 20-task bench (10% → 15%). Headline written: "protocol improves resolution 50% (relative)." The measured truth: one flip, inside noise at n=20; the protocol also cost 30% more calls per task. The disciplined record reads: *no detectable effect; cost up; do not ship on this evidence; if the idea matters, power the comparison properly (larger bench or repeated runs).* Programs that ship on one-flip evidence accumulate a codebase of superstitions, each defended by a number that never replicated.

## Failure mode

Tuning on the holdout (it becomes training data and the final read becomes fiction); retrospective criteria (choosing the metric after seeing results); comparing across changed benches, budgets, or scorers; reporting rates without denominators ("improved 50%" of a 2-task base); and ignoring cost until the invoice teaches it.

## Rule

> **Rule.** No configuration ships on a difference below the pre-registered signal threshold for the bench size, and no improvement is claimed from a comparison in which anything but the named variable differed. A result that a same-configuration re-run cannot reproduce within threshold is reclassified as noise in the same record that reported it.


---

# Chapter 23 — Training Agents

## Principle

When configuration and prompting reach their measured ceiling, the remaining lever is the weights. Training an agent means teaching behavior from *evidence*: demonstrations and trajectories whose correctness was established by execution. The governing principle is provenance — every training example asserts "this behavior was right," and that assertion must carry the same executed proof demanded of any other claim (Chapter 21).

## Substance

**Supervised fine-tuning (SFT)** trains on (input, desired output) pairs by gradient descent on the model's own loss — teaching format, style, procedure, and, with enough verified substance, capability. **LoRA** (after Hu et al., 2021) makes this cheap: freeze the base weights, train low-rank adapter matrices on selected projections; adapters are small, swappable, and composable (different adapters for different roles — a coder, an analyzer — over one base).

**STaR and rejection sampling** (after Zelikman et al., 2022) solve the demonstrations problem: let the current model attempt tasks, keep only attempts that *verifiably succeed* (the target tests pass under independent execution), fine-tune on those, and iterate — each round's better sampler yields better data. The oracle variant builds trajectories from known-good solutions (e.g., human gold patches) and admits them only when the solution verifies and the trajectory's observations are *real* — replayed against the actual environment at the actual state, so every tool result in the record is genuine output. Synthesized observations (plausible reconstructions of what tools "would have" returned) teach the model a fictional world; the honest gates reject them or label them permanently.

**Dataset hygiene is a border checkpoint:** reject benchmark items and holdout items (by id *and* by content collision — same repo at the same commit), reject records failing the evidence gate, reject over-length records rather than truncating them into nonsense, deduplicate by solution fingerprint, cap per-task counts so one easy task can't dominate. A manifest records exactly what was admitted and why the rest was not; the dataset's claims about itself must be checkable.

**The numerics of training are part of training.** Gradient descent updates weights by amounts on the order of the learning rate (10⁻⁵–10⁻⁴). In float16, the representable spacing near a weight of magnitude ~1 is ~10⁻³ — *larger than the update* — so updates round back to the identical stored value, and the optimizer's second-moment estimates underflow below the subnormal floor. A model trained in pure fp16 at small learning rates can be *incapable of changing*, while its loss curve prints normally and its logs look like a training run. The standard cure is mixed precision done correctly: master weights and optimizer state in fp32, forward/backward compute in bf16/fp16 autocast, gradient checkpointing when memory binds. And the standard *verification*: a one-step census — take one optimizer step and count how many weights actually changed (in fp32, expect ~all; in broken fp16, a small fraction) — run *before* the expensive run, not after the puzzling flat result. Training failures are quiet: leakage inflates every later metric, wrong precision produces a perfect log of a frozen model, and a launcher that reports success for a crashed subprocess will happily confirm all of it. Verify artifacts (weights moved, adapter loads, eval delta exists), never wrappers.

## Worked example

A fine-tune completes 5 epochs; evaluation shows *exactly* chance performance, identical across epochs — the signature not of weak learning but of *no* learning. The differential diagnosis is short: (1) label alignment (are targets permuted? — check end-to-end with one hand-traced example); (2) gradient flow (does every parameter receive gradient? — one backward pass with per-module norms); (3) update survival (one optimizer step, then a census of changed weights in the training precision). Cause (3) convicts silently and is the one nobody checks first, because "the loss printed" feels like training. The census takes minutes and settles it.

## Failure mode

Training on the benchmark; training on unverified or synthesized trajectories while claiming verified data; silent precision pathologies; evaluating the trained model on data adjacent to its training set and calling the gap "capability"; and selecting the final checkpoint by vibes instead of a frozen-bench delta against the untrained control under an identical configuration hash.

## Rule

> **Rule.** A training run is reported only with three artifacts: a dataset manifest proving zero benchmark/holdout contamination and the evidence status of every admitted record; a pre-flight check that the optimizer measurably changes weights in the training precision; and a post-training delta against the untrained control on the frozen bench under identical configuration. Missing any one, the run is *unverified* — whatever its logs say.


---

# Chapter 24 — Mandates, Receipts, and Accountability Patterns

## Principle

Agents act in the world — they spend, edit, send, and delete — and someone is answerable for those acts. Accountability is an engineering pattern, not a policy document: before the act, a *mandate* bounds what the agent may do; during the act, *receipts* record what it did; after the act, a third party can *verify* the record against the mandate without trusting the agent or its operator. Identity, authorization, and audit — designed before the incident, not reconstructed after it.

## Substance

**Identity.** The agent carries a short-lived, signed credential binding it to a principal and a configuration (model, prompt hash, tool set). Short lifetimes bound the value of theft; signatures make the credential unforgeable by the agent itself; the identity record makes any later artifact attributable: *this* agent, in *this* configuration, did this.

**Mandates.** A mandate is a signed, expiring authorization with explicit bounds — the generalization of capability and spend-limit patterns across computing: allowed tools and action classes; allowed scope (paths, hosts, accounts); numeric caps (calls, tokens, money, wall-clock); expiry. Enforcement is *fail-closed and at the point of action*: a call outside the mandate is denied by the enforcing layer (Chapter 19's Level 2 — a mandate checked by the agent's own goodwill is a wish), and an exhausted or expired mandate denies by default. Mandates compose with least privilege (Chapter 13): the agent that drafts does not hold the send permission; drafting and sending are different grants, and the distance between them is the distance between a suggestion and a commitment.

**Receipts.** Every action appends a receipt to a hash-chained ledger (after Schneier & Kelsey's tamper-evident logging, 1999; the transparency-log family, RFC 6962, is the public-scale relative): each receipt commits to its predecessor's hash and records the action, its arguments hash, its result hash, resources consumed, and its mandate. At completion the final artifact (the patch, the purchase) is *sealed*: a closing record binds the artifact's hash to the ledger head and the mandate — so the artifact provably came from the run the ledger describes.

**What verification proves — and what it does not.** A checker validates: chain integrity (no receipt altered, deleted, or reordered without detection), seal binding (this artifact ↔ this ledger), and mandate compliance (every receipt inside the bounds). State the limits with equal precision: an *unsigned* chain proves internal consistency, not authenticity — an attacker who can rewrite the whole ledger can recompute the whole chain and seal, and no check on the record alone detects it. Authenticity requires a signature the agent cannot forge or an external anchor the attacker cannot rewrite (periodically publishing the ledger head to an independent medium — a public transparency log, a timestamping service, a blockchain — so history-rewriting becomes publicly evident). A second limit: receipts record what the *recording layer* saw; a compromised recorder can lie at the source. Coverage is a property of placement (harness-observed recording beats agent-self-reported recording — Chapter 19 again), and honest systems say which placement they use.

## Worked example

A purchasing agent holds a mandate: vendor allow-list, $500 cap, 20 calls, 1 hour. It buys in 14 calls and $412; each call's receipt chains to the last; the invoice is sealed against the ledger head. An auditor — trusting neither the agent nor its operator — replays the chain, checks the seal, and sums the receipts against the mandate: attribution, conduct, and integrity each answered from the record alone. Now tamper with it: edit one receipt's amount and the chain breaks at the next link; delete a receipt and the sequence gaps; truncate the tail and the seal's head mismatches. Rewrite *everything* consistently and the unsigned chain accepts it — which is exactly why the operator also anchors the head externally each hour: the rewrite would now contradict a public record. Each guarantee is stated with its attacker model; that is what makes it a guarantee rather than a slogan.

## Failure mode

Audit theater: logs the audited party can edit, receipts recorded by the agent itself with no independent observation, mandates enforced by prompt text, seals computed over artifacts that are later modified (a seal binds a hash — hash the final artifact, after final edits, or it binds a draft), and valid-but-wrong-mode credentials (a demo/test credential is cryptographically *valid*; validity checks alone do not exclude it — mode must be checked explicitly, a classic).

## Rule

> **Rule.** Every accountability claim names its placement and its attacker: who records, who can rewrite, what detects rewriting, and what the record cannot prove. A claim that a log "proves" an agent's conduct is falsified by exhibiting one undetectable rewrite the design permits — and every design must either close that rewrite or publish it as its stated limit.


---

# Chapter 25 — Failure Modes of Agentic Systems

## Principle

Agentic systems fail in characteristic ways — not randomly, but along the seams of the loop: observation, state, mechanism, measurement, and communication with the human. A named taxonomy turns post-mortems from storytelling into pattern-matching: when a failure has a name, the next occurrence is recognized in minutes instead of diagnosed in days, and its prescribed countermeasure is already written down.

## Substance

**Failures of observation and state.** *Open-loop drift* — acting on the initial plan while the environment diverges from it. *State loss* (context rot, Chapter 20) — decisive early facts forgotten, re-derived contradictorily. *Phantom success* — an error result read as a success observation, then built upon. *Stale-artifact work* — editing, testing, or verifying a version of the artifact that is not the current one (the diff moved; the evidence didn't).

**Failures of mechanism.** *Silent non-engagement* — a discipline, gate, or sampler that exists in the design and never fires in traces (Chapter 19); its runs are indistinguishable from the mechanism's absence, except in cost. *Choreography mistaken for enforcement* — compliance expected from prose. *Budget cliff* — no defined behavior at exhaustion, so the run's product is lost instead of submitted at its best verified state. *Thrash* — repeated near-identical failed actions (the loop's tell: same call, same error, no new information between attempts) and its twin, *premature convergence* — submitting the first plausible artifact without the verification that would have killed it.

**Failures of measurement and belief.** *Overstated status* — the modal class in every honest incident record: a success state claimed before the artifact was read back (an estimate reported as a measurement; a wrapper's "success" trusted over the crashed subprocess; a document reported complete that was never read to its end). *Verification of a model* — measuring a probe or generic path and reporting it as the production path (Chapter 21). *Contaminated evaluation* — tuning on the holdout, leaking the bench into training (Chapters 22–23). *Referent misread* — executing confidently on the wrong target because a pronoun, a name, or a "submit" had two live referents; the countermeasure is mechanical: name the referent back before any irreversible act.

**Failures of the human interface.** *Approval noise* — asking the human so often, so repetitively, or so indistinguishably that approvals stop meaning anything (the human rubber-stamps; the system's real gate dissolves). *Unbatched interruption* — many small asks where one consolidated decision would do. *Gate misplacement* — asking the human about matters the system can verify itself, while *not* stopping at the irreversible ones (identity, payment, publication) that are genuinely theirs. *Silent waiting* — a run blocked on a human input that was never clearly requested, discovered hours later.

## Worked example

A workflow reports a submission "confirmed" — its checker matched a success phrase in the target page's own marketing copy ("thank you for considering…"), present whether or not anything was submitted. The submission had in fact been rejected for missing fields. Classify before fixing: this is *overstated status* via a *status channel that was never the artifact*. The countermeasure is class-shaped, not instance-shaped: confirmations are read from system state (the submission appears in the system's own list, with an identifier), never from page prose — a rule that then protects every other workflow using the same checker, not just this one. That last step — generalize the fix to the class — is what separates a taxonomy from a pile of anecdotes.

## Failure mode (of failure analysis itself)

Blame-shaped post-mortems ("the model was careless") that name no mechanism and therefore prevent nothing; single-cause stories for multi-cause events; and the most corrosive — quietly editing the record (relabeling a failure as a success, deleting the trace) which destroys the dataset every future improvement depends on. The failure record is training data for both humans and models; falsifying it is falsifying the curriculum.

## Rule

> **Rule.** Every failure is recorded under a taxonomy name with its detection method (how it was caught) and its class-level countermeasure. A post-mortem that names no mechanism, or whose fix addresses only the instance, is returned as incomplete — the class is still at large.


---

# Chapter 26 — Operations: Running Agents in Production

## Principle

An agent in production is a system with economics, failure domains, and a human organization around it. Operations is where the craft meets reality: quotas, costs, monitoring, escalation, and the discipline of *how work is launched* — which determines whether the system's output is a stream of verified results or a bonfire of compute.

## Substance

**Batch over interactive.** Long agent work belongs in committed, self-terminating batch jobs that run server-side to a defined end state — not in interactive sessions that die when a tab closes, a connection drops, or a human looks away. A batch job has a contract: inputs fixed at launch, an expected output artifact, a timeout, and a log that survives it. Interactive sessions are for exploration and steering; the moment work matters, it gets a batch definition. The economic corollary: never babysit — human attention is the scarcest resource in the system, and a workflow that needs a human watching a spinner has misallocated it.

**Quota and cost economics.** Compute arrives in quotas (hours per week, calls per day, tokens per month) and every program of work is a portfolio allocation against them. Price experiments *before* running them from measured unit costs (seconds per attempt × attempts; tokens per task × tasks) — a generation or evaluation batch whose expected yield doesn't justify its quota share doesn't run, or runs smaller first (a pilot that measures the unit cost precisely). Sequencing matters: cheap decisive experiments before expensive confirmatory ones; and a shared quota silently couples projects that believe themselves independent — account for the coupling explicitly rather than discovering it as a mysteriously exhausted budget.

**Monitoring and the posture of oversight.** The operational stance that scales is: the system watches itself and batches its reports; the human is interrupted only for (a) decisions that are genuinely theirs — identity, payment, legal attestation, irreversible publication — and (b) forks where their judgment is the input. Everything else is a digest. Monitoring must distinguish *absent* from *fine*: a sensor that failed to run is a gap in coverage, reported as unknown — a dashboard that renders silence as green is manufacturing confidence.

**Human gates, designed.** Some steps are the human's by nature, not by system weakness: creating accounts, passing identity verification, providing payment instruments, signing, and final approval of irreversible external acts. Design the workflow so these arrive *consolidated and prepared* — everything fillable already filled, the exact decision stated in one line, the consequence of each option priced. The system's throughput is often bounded by this queue (in honest operational records, the majority of stalled work stalls at human-only gates, not at execution); respect it by never adding a preventable item to it, and never re-asking an item already answered.

**Stop and scope discipline.** A human's stop is final and thread-specific: stopped lines of work are not re-prompted, re-packaged, or resumed under a new name. Before spending effort on any external opportunity, venue, or target, verify it exists, is in scope, and is eligible *first* — the cheapest failure is the one prevented by a five-minute check before five hours of work.

## Worked example

A research program plans a data-generation batch: 400 attempts estimated from a measured 174 s/attempt ≈ 19 hours — two-thirds of the weekly compute quota, for an expected yield computed from the measured success rate. Priced in advance, the decision changes shape: run a 200-attempt pilot (~9.5 h) first; if the yield tracks the estimate, the second half is justified by data; if the success rate has moved (because the sampler improved), the pilot's own output may already suffice. The alternative history — launching the full batch blind — spends the same quota to learn the same facts later and worse. Operations is arithmetic performed *before* the spend, not narrative performed after it.

## Failure mode

Interactive-session dependence (work dying with tabs); unpriced launches (quota discovered exhausted mid-program); alert fatigue (so many low-grade notifications that the real one is missed — batching is a safety feature, not a courtesy); re-litigating settled stops; and shadow coupling (two "independent" programs contending for one quota, one GPU pool, or one human's attention, each planned as if alone).

## Rule

> **Rule.** Every unit of agent work launches with: a priced budget (unit cost × volume, from measurements), a defined end state and output artifact, a timeout, and a named human-gate list (what will need the human, stated up front). Work launched without a price is reported as unpriced in the operations record — and unpriced work does not get to be surprised by its bill.


---

# Chapter 27 — Principles of Practice

The closing chapter collects the book's rules as general principles of agentic coding practice. Each is stated so it can be checked — a principle that no evidence could embarrass is a slogan, and this book has tried to contain none.

## On the loop

1. **An agent is a loop, not a model.** Attribute every failure to a named component — observation, state, tool interface, budget, stopping rule — before attributing it to the model.
2. **No open-loop runs.** Every action is preceded by a justifying observation and followed by a judging one.
3. **The world is the ground truth.** Observations returned by tools outrank the model's expectations, plans, and memory, in that order, every time they conflict.

## On enforcement

4. **Choreography is not enforcement.** A check the model invokes on itself is advice. Guarantees live in code the model cannot skip.
5. **Name the enforcement level** of every claimed discipline, and show the trace evidence that it engaged. No engagement evidence, no claim.
6. **Fail closed.** When a check cannot run, the answer is denial and a report of *absent* — never a silent pass.

## On verification

7. **Executed proof or it doesn't count.** Selection — of patches, checkpoints, training data — is by measured outcome, never by confidence, order, or elegance.
8. **Name the path.** A claim covers the exact artifact, version, and code path measured. A claim found to describe a different path is withdrawn, in the same document, at the same prominence.
9. **Read the artifact, not the status.** Wrappers, summaries, and success flags are claims about evidence, not evidence.
10. **Enumerate targets before work.** What must turn green, what must stay green — named first, or verification is theater.

## On measurement

11. **Frozen benches, frozen criteria.** The test set, the metric, and the ship threshold are fixed before the run; the holdout is never tuned on.
12. **One variable per comparison,** and differences below the noise threshold are recorded as *no detectable effect* — a real result, not a failed one.
13. **Cost is a metric.** Every improvement is reported with its price in calls, tokens, time, or money.
14. **Log every tried configuration.** An unrecorded tune is an anecdote; a recorded search is an asset.

## On training

15. **Provenance or exclusion.** Training data carries executed evidence and a checkable manifest; synthesized correctness is labeled permanently or rejected.
16. **Never train on the test.** Benchmark and holdout material is excluded by identity and by content, and the exclusion is asserted, not assumed.
17. **Verify the training actually trains.** One optimizer step, one census of changed weights, before the expensive run — a frozen model with beautiful logs is still frozen.

## On accountability

18. **Mandate before action, receipt during, seal after.** Authority is bounded in advance and checked at the point of action; the record binds the artifact to the run.
19. **State every guarantee with its attacker.** What the record proves, against whom, and the rewrite it cannot detect — published, not discovered.
20. **The human's gates are the human's.** Identity, payment, legal attestation, and irreversible publication stop for the human — prepared, consolidated, and never routed around.

## On the craft itself

21. **Claims match evidence** — in code comments, in reports, in benchmarks, in training data. This is the master principle; every other rule in this chapter is its corollary in one domain.
22. **Corrections are data.** An error found, named, mechanistically explained, and converted into a class-level countermeasure is the highest-value artifact a practice produces. The appendix that follows exists to train exactly that motion.


---

# Appendix A — Errata Exercises: Claims, Flaws, Corrections

**About this appendix.** Every entry below is a **constructed teaching exercise**: an invented claim of the kind commonly made about agentic coding and computing, followed by its flaw, its correction, and the evidence or reasoning that settles it. These are not reports of real incidents; they are training material for the *motion* of correction — read a confident claim, find the mechanism of its wrongness, state the true claim crisply, and name the evidence. A reader (human or model) who can perform this motion on unseen claims has learned the book's master skill.

---

## Exercise 1 — "Our fine-tune ran five epochs, so the model learned the task."

**Claim.** A training run completed its schedule; therefore the model was trained.

**Flaw.** Completion of a schedule proves only that steps were *executed*, not that weights *changed*. If the training precision cannot represent the updates — in pure float16, an AdamW update near learning rate 2×10⁻⁵ is smaller than the spacing between representable values near typical weight magnitudes, and rounds back to the identical stored value — the model after five epochs is bit-for-bit the model before them. Loss logs print normally throughout, because the loss is computed from the (unchanged) model.

**Correction.** A run trains a model only if its weights measurably change. Establish this with a one-step census (one optimizer step; count changed weights — ≈all in fp32, a small fraction in broken fp16) and with end-to-end evidence (an evaluation delta against the untrained control). Correct precision practice: fp32 master weights and optimizer state, lower-precision arithmetic only inside autocast.

**Evidence.** The census is decisive and cheap: identical batch, identical loss in both precisions, and a changed-weight fraction that differs by an order of magnitude between them. A flat metric at exactly chance across every epoch is the field signature of the frozen case.

## Exercise 2 — "The submission was confirmed — the page said 'Thank you.'"

**Claim.** An automated submitter reports success because the result page contained a success phrase.

**Flaw.** The phrase matched was part of the form's own static copy, present on the page whether the submission succeeded, failed validation, or was never sent. A confirmation detector that scans page prose measures the page's marketing, not the transaction's outcome.

**Correction.** A submission is confirmed only by system state: the submission appears in the system's own records (a submissions list, an identifier, a status field) read back after the fact. Outcomes that cannot be so verified are reported as *clicked–unverified* — a distinct, honest state.

**Evidence.** Read-back: query the system's record of submissions. If the item is absent, the prose was lying by coincidence; if present with an identifier, the confirmation is real. The two states are distinguishable in every case — the exercise's claim survives only where nobody looked.

## Exercise 3 — "The gate blocks unverified patches."

**Claim.** A pre-submit gate implemented as a tool the agent is instructed to call "blocks" patches that lack test evidence.

**Flaw.** A tool the model chooses to invoke cannot block anything. The model can omit the call, call it after submitting, or call it and proceed despite its verdict. What exists is a *request*, enforced by nothing; calling it a block mistakes choreography for mechanism.

**Correction.** Blocking requires enforcement outside the model's control: the submission action itself refuses until the precondition is verifiably met (test evidence bound to the current artifact's hash). Where the platform offers no such hook, the honest description is "a cooperative protocol, mitigated by artifact-binding" — and the system's guarantees must be restated at that level.

**Evidence.** One completed run whose trace shows a submission with no preceding gate verdict falsifies the claim as stated — regardless of that run's outcome.

## Exercise 4 — "The benchmark improved 50% after our change."

**Claim.** Resolution rose from 2 to 3 tasks on a 20-task benchmark — "a 50% improvement."

**Flaw.** Two compounding misstatements: the relative framing of a tiny base (1 task = 5 points absolute, 50% relative), and the treatment of a one-task flip as signal when run-to-run variance at n=20 routinely flips individual tasks. The claim is arithmetic wearing a lab coat.

**Correction.** Report absolute numbers with denominators (2/20 → 3/20), state the pre-registered signal threshold for the bench size (≥2 tasks at n=20), and record sub-threshold differences as *no detectable effect* pending a powered comparison.

**Evidence.** Re-run the control under the identical configuration: if its score also moves by a task between repeats, the noise floor is measured, and the claim's "improvement" is inside it.

## Exercise 5 — "Hash-chained receipts prove what the agent did."

**Claim.** Because each receipt commits to its predecessor's hash and the final seal binds the artifact, the ledger *proves* the agent's conduct.

**Flaw.** An unsigned chain proves internal consistency only. An attacker able to rewrite the ledger can recompute every link and the seal; the verifier accepts the rewritten history because every check it can perform is a check the rewrite satisfies. The claim omits its attacker model — the word "proves" is doing unlicensed work.

**Correction.** The chain detects *partial* tampering (edits, deletions, reordering, truncation) by parties who cannot or do not rewrite the whole. Authenticity requires a signature from a key the agent cannot hold, or an external anchor (periodically published ledger heads) that makes total rewrite publicly evident. State both the guarantee and the undetectable rewrite, or the claim is oversold.

**Evidence.** Perform the rewrite in a test: alter a receipt-level fact, recompute the chain and seal, and present it to the verifier. Acceptance is the measured limit of the unsigned mechanism — demonstrable in an afternoon, decisive forever.

## Exercise 6 — "We measured the library: recursion to depth 20,000 overflows the stack."

**Claim.** A probe program using the library's serialization API recursively overflows at depth 20,000, so deeply nested values are a crash risk for stored data.

**Flaw.** The probe measured a *generic* path — raw recursion in the probe's own code — not the library's production path, which enforces a container-depth cap (returning clean errors) at a far lower depth. Values beyond the cap cannot be constructed through the production API at all, so the claimed stored-data scenario cannot occur. The measurement was real; its subject was a different system than the one claimed.

**Correction.** Behavioral claims bind to the exact path measured: library version, entry point, and enforcement points on that path. When a production cap intervenes, the claim must be restated to whatever survives the cap (e.g., in-execution consumers without the cap, if any exist and are demonstrated) — or withdrawn.

**Evidence.** Trace the production call path and find the enforcement; demonstrate construction of a beyond-cap value *through the production API* or concede it cannot be built. The cap's presence in the shipped source settles which.

## Exercise 7 — "Adding the discipline prompts didn't help, so discipline doesn't work."

**Claim.** An agent given explicit discipline instructions (verify before submitting, enumerate targets, self-examine) scored no better than baseline; discipline is therefore ineffective for agents.

**Flaw.** The experiment varied the *delivery channel* (prompt text) and concluded about the *concept*. Discipline-as-exhortation is one implementation; discipline-as-harness-enforcement was never in the trial. Additionally, at small n the result is "no detectable effect," not "proven zero" — the conclusion overclaims in two directions at once.

**Correction.** Scope conclusions to the implementation measured: "discipline delivered as prompt text showed no detectable effect at n=20 on this model." The harness-enforced variant is a separate, untested hypothesis until a trial installs enforcement outside the model's discretion and measures engagement in traces.

**Evidence.** In the trial's own traces, check whether the instructed behaviors occurred (targets enumerated? self-exams present?). If the behaviors are absent from the traces, the trial measured instruction-following, not discipline — and the trace check, not the score, is what reveals it.

## Exercise 8 — "Compression beat the entropy bound on our corpus."

**Claim.** A new codec compresses a test corpus to fewer bits than the source's estimated entropy — "beyond Shannon."

**Flaw.** Lossless compression of a source below its true entropy is impossible (Shannon, 1948); an apparent violation means the entropy was misestimated (usually: the estimator assumed independence, or the "corpus" was generated by a process with learnable structure the estimator ignored) — or the codec smuggled information (a dictionary trained on the test set, uncounted headers, the decompressor containing the data).

**Correction.** Count *everything* needed to decode: model, dictionary, headers, parameters. Estimate entropy with the strongest available model of the source, and treat "beating entropy" as a bug report against the accounting, never as a result.

**Evidence.** Decode the compressed artifact in a clean environment containing only the counted material. If decoding requires anything uncounted, the claim collapses to arithmetic. Entropy accounting that survives clean-room decoding is the only kind there is.

## Exercise 9 — "The agent fixed the bug — all tests pass."

**Claim.** After the agent's edit, the test suite is green; the bug is fixed.

**Flaw.** "All tests" may exclude the test that demonstrates the bug (it may never have been written), include it only in a form the edit gamed (test modified, assertion weakened, fixture altered), or pass because the bug's trigger wasn't exercised in this configuration. A green suite is evidence about the suite, and about the bug only to the extent the suite's relationship to the bug is established.

**Correction.** The claim requires: a reproduction that failed *before* the edit and passes *after* (same test, unmodified), plus the pre-existing suite green (no regressions), plus protected-file discipline — tests and test configuration were not altered to achieve the pass, or any alteration is declared and justified as a specification change.

**Evidence.** The before/after pair on the identical test is the evidence; a bare after-state is an anecdote. If no failing-before test exists, the honest claim is "the suite passes and the reported symptom is unaddressed by any test" — which is a statement about remaining risk, not about a fix.

## Exercise 10 — "Retries are safe — the API usually processes each request once."

**Claim.** A client retries timed-out requests freely, since duplicates are rare in practice.

**Flaw.** A timeout means the response was lost, not that the request failed — the request may have executed fully. "Usually processed once" under retries means *sometimes processed twice*, and for non-idempotent effects (charges, sends, allocations) the rare case is the catastrophic one. The claim mistakes a frequency statement for a safety property.

**Correction.** Non-idempotent operations carry idempotency keys; the server deduplicates on the key, stored transactionally with the effect. Retries then become safe *by construction*, at any frequency — safety is a property of the mechanism, not of the observed duplicate rate.

**Evidence.** Fault-injection: kill the response path after the server commits but before the client hears, then retry. Count effects. One duplicate falsifies "safe" for the un-keyed design; the keyed design survives the same test by construction.


---

# Appendix B — The Canon: Definitive Sources by Domain

No single book contains the craft. This appendix is the map: for each domain, the public works an agent (or its trainer) should treat as ground truth — the texts against which claims in this Bible, and anywhere else, are checked. Listing is by the part of this book they ground.

## Part I — Foundations

- **Computation & computability** — Turing, *On Computable Numbers* (1936); Sipser, *Introduction to the Theory of Computation*; Hopcroft & Ullman, *Introduction to Automata Theory, Languages, and Computation*.
- **Information theory** — Shannon, *A Mathematical Theory of Communication* (1948); Cover & Thomas, *Elements of Information Theory*.
- **Algorithms & complexity** — Cormen, Leiserson, Rivest & Stein, *Introduction to Algorithms* (CLRS); Knuth, *The Art of Computer Programming* (TAOCP); Garey & Johnson, *Computers and Intractability* (NP-completeness).
- **Data structures** — CLRS (above); Knuth, TAOCP vols. 1 & 3; Sedgewick & Wayne, *Algorithms*.
- **Programming languages & paradigms** — Abelson & Sussman, *Structure and Interpretation of Computer Programs* (SICP); Pierce, *Types and Programming Languages*; Friedman & Wand, *Essentials of Programming Languages*.
- **Types & semantics** — Pierce (above); Winskel, *The Formal Semantics of Programming Languages*; Hoare, *An Axiomatic Basis for Computer Programming* (1969).
- **Operating systems** — Tanenbaum & Bos, *Modern Operating Systems*; Arpaci-Dusseau & Arpaci-Dusseau, *Operating Systems: Three Easy Pieces* (OSTEP); Bryant & O'Hallaron, *Computer Systems: A Programmer's Perspective* (CS:APP).
- **Networking & distributed systems** — Tanenbaum & Wetherall, *Computer Networks*; Kleppmann, *Designing Data-Intensive Applications*; Brewer, *CAP Theorem* (2000) and Gilbert & Lynch's proof (2002); Lamport, *Time, Clocks, and the Ordering of Events* (1978).
- **Databases** — Codd, *A Relational Model of Data for Large Shared Data Banks* (1970); Garcia-Molina, Ullman & Widom, *Database Systems: The Complete Book*; Kleppmann (above) for the modern storage landscape.
- **Compilers** — Aho, Lam, Sethi & Ullman, *Compilers: Principles, Techniques, and Tools* (the Dragon Book); Appel, *Modern Compiler Implementation*; Cooper & Torczon, *Engineering a Compiler*.

## Part II — The Craft

- **Design & architecture** — Gamma, Helm, Johnson & Vlissides, *Design Patterns* (1994); Evans, *Domain-Driven Design*; Martin, *Clean Architecture*; McConnell, *Code Complete*; Brooks, *The Mythical Man-Month*.
- **Testing & verification** — Claessen & Hughes, *QuickCheck* (2000) for property-based testing; Zeller, *Why Programs Fail* (also the debugging canon); the fuzzing literature via AFL (Zalewski) and its successors.
- **Debugging** — Zeller (above); Kernighan & Pike, *The Practice of Programming*; Agans, *Debugging: The 9 Indispensable Rules*.
- **Security** — OWASP Top 10 and ASVS; Anderson, *Security Engineering*; Schneier, *Applied Cryptography* (concepts) with Ferguson, Schneier & Kohno, *Cryptography Engineering* (practice); Microsoft's STRIDE threat-modeling literature.
- **Performance** — Amdahl (1967); Hennessy & Patterson, *Computer Architecture: A Quantitative Approach*; Gregg, *Systems Performance*; the `perf`/profiling literature of the relevant platform.
- **Concurrency** — Herlihy & Shavit, *The Art of Multiprocessor Programming*; the Java and C++ memory-model specifications (JLS §17; ISO C++ [atomics]); Go's concurrency writings (Pike, *Go Proverbs*; the Go memory model document).
- **Collaboration & version control** — the Git book (Chacon & Straub, *Pro Git*); Humble & Farley, *Continuous Delivery*.
- **Readability & documentation** — Kernighan & Pike (above); McConnell (above); Google's engineering practices documentation (public) for review culture.

## Part III — The Agentic Layer

- **Agent loops** — Yao et al., *ReAct* (2022); Shinn et al., *Reflexion* (2023); Yao et al., *Tree of Thoughts* (2023).
- **Coding agents & benchmarks** — Jimenez et al., *SWE-bench* (2024); Yang et al., *SWE-agent* (2024); the SWE-bench family of follow-on benchmarks.
- **Context** — Liu et al., *Lost in the Middle* (2023); Anthropic's public engineering writings on context engineering and tool design for agents.
- **Training** — Hu et al., *LoRA* (2021); Zelikman et al., *STaR* (2022); the rejection-sampling/fine-tuning literature descended from them; Micikevicius et al., *Mixed Precision Training* (2018) for the numerics.
- **Accountability** — Schneier & Kelsey, *Secure Audit Logs* (1999); RFC 6962 (Certificate Transparency) for transparency logs; RFC 7519 (JWT) for signed credentials; the capability-security literature (Miller, *Robust Composition*, 2006) for mandates and least authority.

*Currency note.* The foundations canon is stable across decades. The agentic layer is young and moving; its entries are the founding works as of this writing (2026), and a serious reader re-derives the frontier from the current literature rather than trusting any frozen list — including this one.


---

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


---

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


---

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


---

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


---

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


---

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


---

# Port — Types · C++
<!-- canonical_section: types.core | language: cpp -->

## Definition

C++ is statically and strongly typed with a pragmatic escape hatch culture: types are checked at compile time, conversions are governed by a detailed standard, and the type system is the primary tool for encoding invariants (RAII ties resource lifetime to object lifetime — a type-level property). Templates provide parametric polymorphism resolved at compile time; since C++20, *concepts* constrain templates with named requirements, bringing error messages and intent closer to the ML-family ideal.

## Idiom mapping

- Canon "make absence explicit" → `std::optional<T>`: a value or a checked absence; dereferencing an empty optional is UB-by-contract, so `has_value()`/`value()` discipline replaces null-pointer roulette. Raw pointers conventionally mean *non-owning, possibly null*.
- Canon "sum types" → `std::variant<Ts...>` with `std::visit` and the overloaded-lambda idiom approximating pattern matching; exhaustiveness is partial (the visitor must cover all alternatives, enforced by overload resolution).
- Canon "failure in the signature" → exceptions, `std::expected<T,E>` (C++23), or error-code out-parameters in performance/ABI-constrained code — one style per codebase, stated.
- Canon "ownership as type" → `unique_ptr` (exclusive), `shared_ptr` (shared), references/views (non-owning): ownership is literally part of the type since C++11.

## Worked example

```cpp
std::optional<double> parse_timeout(std::string_view raw) {
    if (raw.empty()) return std::nullopt;          // absence is a value
    double v{};
    auto [ptr, ec] = std::from_chars(raw.data(), raw.data() + raw.size(), v);
    if (ec != std::errc{}) return std::nullopt;    // failure, not exception
    return v;
}
```

The signature alone — text view in, `optional<double>` out — states the Chapter 5 contract: total function, explicit absence, no hidden throw.

## Pitfalls

- **Undefined behavior is not a type error**: signed overflow, dangling views (`string_view` outliving its string), and iterator invalidation compile cleanly and detonate later.
- **Implicit conversions**: narrowing, sign conversions (`-1 < 1u` is false), and user-defined conversion operators create values no one wrote.
- **Slicing**: assigning a derived object to a base-typed variable silently amputates it — pass polymorphic objects by pointer/reference.
- **`auto` overuse**: deduction hides exactly the types the canon says carry the contract; use it for the obvious, spell the load-bearing ones.

## Canon cross-reference

Canonical section: **types.core** (Chapter 5, "Substance"). This port implements the canon for cpp; where the port and the canon disagree, the canon governs and the port is the bug.


---

# Port — Types · Go
<!-- canonical_section: types.core | language: go -->

## Definition

Go is statically typed with deliberately modest type machinery: no inheritance, no generics until 1.18 (and restrained since), and *structural* interfaces — a type satisfies an interface by having its methods, without declaring the intent. The design stance is explicitness over expressiveness: the type system carries shapes and contracts; cleverness is expected to live in the code, not the types.

## Idiom mapping

- Canon "make absence explicit" → Go's honest weakness: `nil` exists for pointers, interfaces, maps, slices, channels, and function values, and a typed nil inside an interface is *not* `== nil` (the famous two-word interface value: type + value; a nil `*T` wrapped in an interface is a non-nil interface). Absence is modeled by convention: zero values, presence booleans (`v, ok := m[k]`), or explicit pointer semantics — and the convention must be stated per API.
- Canon "failure in the signature" → the multi-return `(T, error)` idiom is the culture's spine: errors are values, checked explicitly, wrapped with context (`fmt.Errorf("...: %w", err)`). The canon's demand that failure be un-ignorable is approximated socially (linters flag unchecked errors) rather than by the compiler.
- Canon "sum types" → approximated by an interface with unexported marker methods plus a type switch; exhaustiveness is *not* compiler-checked — the port's known gap, compensated by a default-case panic in switches over closed sets.
- Canon "composition over inheritance" → embedding: a struct gains another's methods by containing it — delegation with the hazards of a flattened namespace.

## Worked example

```go
func parseTimeout(raw string) (float64, bool) {
    raw = strings.TrimSpace(raw)
    if raw == "" {
        return 0, false // absent: explicit, per the (value, ok) idiom
    }
    v, err := strconv.ParseFloat(raw, 64)
    if err != nil {
        return 0, false
    }
    return v, true
}
```

The `(value, ok)` shape is the signature carrying the contract, in the idiom a Go reader pattern-matches instantly.

## Pitfalls

- **The typed-nil interface trap** (above): returning a nil `*MyError` as an `error` yields a non-nil error that "isn't nil" in the caller — a contract bug that compiles forever.
- **Zero-value ambiguity**: `0`, `""`, and `false` are both valid values and Go's "unset" markers; APIs must say which, or use pointers/`ok` forms.
- **Unchecked errors**: the compiler permits ignoring a returned `error`; code review and `errcheck` are the enforcement — choreography, by the standards of Chapter 19, and treated as such.
- **Shadowing with `:=`** inside blocks, most dangerously shadowing an `err` being checked outside.

## Canon cross-reference

Canonical section: **types.core** (Chapter 5, "Substance"). This port implements the canon for go; where the port and the canon disagree, the canon governs and the port is the bug.


---

# Port — Types · Java
<!-- canonical_section: types.core | language: java -->

## Definition

Java is statically, nominally typed: subtyping is by declared relationship (`extends`/`implements`), checked at compile time, with a managed runtime (the JVM) enforcing memory safety — no dangling pointers, no buffer overflows, at the price of `NullPointerException`, the language's endemic failure. Generics (since Java 5) are implemented by *erasure*: type arguments exist at compile time and are removed at runtime, a compatibility decision whose consequences still shape daily practice.

## Idiom mapping

- Canon "make absence explicit" → `Optional<T>` for return values (its designed use) plus nullability annotations (`@Nullable`/`@NonNull`, checked by tools) — because bare references are nullable by default, the discipline is annotation-and-convention, and APIs must state their null contract.
- Canon "sum types" → sealed classes/interfaces (Java 17) with pattern matching in `switch`: the compiler checks exhaustiveness over the permitted subclasses — the canon's ideal, native and modern.
- Canon "failure in the signature" → exceptions split by philosophy: *checked* exceptions are part of the signature (the compiler enforces handling — the canon's un-ignorable failure, at real ergonomic cost), *unchecked* for programming errors. Streams and lambdas handle checked exceptions so poorly that wrapping conventions grew around them.
- Canon "records as data" → `record` types (Java 16): immutable carriers with generated equality — algebraic *product* types, pairing with sealed types for full ADTs.

## Worked example

```java
sealed interface TimeoutParse {
    record Parsed(double seconds) implements TimeoutParse {}
    record Absent() implements TimeoutParse {}
    record Invalid(String raw) implements TimeoutParse {}
}

static TimeoutParse parse(String raw) {
    if (raw == null || raw.isBlank()) return new Absent();
    try { return new Parsed(Double.parseDouble(raw.trim())); }
    catch (NumberFormatException e) { return new Invalid(raw); }
}
```

Callers switch over `TimeoutParse` with compiler-checked exhaustiveness: add a fourth case and every consumer must confront it — the canon's sum-type discipline in full.

## Pitfalls

- **Erasure consequences**: no `new T()`, no `instanceof List<String>`, overloading on generic parameters collides — errors that baffle until erasure is understood.
- **`==` on boxed types and strings**: identity vs equality; `Integer` caching makes small values accidentally `==`-equal — a bug that passes tests and fails in production ranges. Always `.equals`.
- **Raw types**: legacy compatibility hatch that disables generic checking for the whole expression — treat in review as unchecked code.
- **Null as the default absence**: any unannotated reference may be null; defensive `NullPointerException`-driven development is the tax for skipping the `Optional`/annotation discipline above.

## Canon cross-reference

Canonical section: **types.core** (Chapter 5, "Substance"). This port implements the canon for java; where the port and the canon disagree, the canon governs and the port is the bug.


---

# Port — Types · JavaScript / TypeScript
<!-- canonical_section: types.core | language: javascript -->

## Definition

JavaScript is dynamically typed with pervasive implicit conversion ("coercion") and a prototype-based object model; every value is one of a small set of runtime types, and `typeof` itself has famous seams (`typeof null === "object"`). TypeScript layers a *structural, gradually-adopted* static type system on top: types are checked at compile time and fully erased at runtime — they describe the program to tools and readers, and constrain nothing the running code does with unvalidated external data.

## Idiom mapping

- Canon "make absence explicit" → fight the two-headed absence: `null` *and* `undefined` both exist; disciplined code picks one (usually `undefined` for "absent," `null` only where an API demands it) and models optionality as `T | undefined` with strict null checks on.
- Canon "sum types" → discriminated unions: object literals with a literal `kind`/`type` tag, switched exhaustively (the `never` check pattern gives exhaustiveness the compiler can verify).
- Canon "failure in the signature" → exceptions for the exceptional; `Promise` rejection as the async error channel; Result-style unions in codebases that choose them. Unhandled rejections are the silent killer — they are errors that chose the path nobody watches.
- Canon "contracts at boundaries" → because types erase, *runtime validation* (schema validators — zod and kin) at every trust boundary is the port of the canon's static guarantee: types for the inside, schemas for the edges.

## Worked example

```ts
type ParseResult =
  | { kind: "ok"; seconds: number }
  | { kind: "absent" }
  | { kind: "invalid"; raw: string };

function parseTimeout(raw: string): ParseResult {
  const t = raw.trim();
  if (t === "") return { kind: "absent" };
  const v = Number(t);
  return Number.isFinite(v) ? { kind: "ok", seconds: v } : { kind: "invalid", raw };
}
```

The union makes the three outcomes distinct and exhaustively switchable — the canon's sum-type discipline expressed in the language's native idiom.

## Pitfalls

- **Coercion traps**: `==` performs type conversion (`"" == 0`, `null == undefined`); use `===` and treat `==` in a diff as a finding.
- **`any` leakage**: one `any` at a boundary silently disables checking downstream; prefer `unknown` + validation.
- **Erasures trusted as walls**: casting a JSON response `as User` asserts a fact nothing checked. Validate, don't cast.
- **Number is a double**: integers above 2⁵³ lose precision; ids and money need strings or `bigint`.

## Canon cross-reference

Canonical section: **types.core** (Chapter 5, "Substance"). This port implements the canon for javascript (TypeScript idioms where they differ from plain JavaScript); where the port and the canon disagree, the canon governs and the port is the bug.


---

# Port — Types · Python
<!-- canonical_section: types.core | language: python -->

## Definition

Python's types are dynamic and strong: every value has a type at runtime, checked at the moment of use, and implicit conversions between unrelated types are refused (`"1" + 1` is an error, not `2` or `"11"`). Variables are names bound to objects; assignment rebinds a name, it never copies or converts the object. Type *annotations* (PEP 484) are a parallel, gradual layer: they are not enforced by the interpreter and exist for checkers (mypy, pyright), editors, and readers.

## Idiom mapping

- Canon "make absence explicit" → `Optional[T]` / `T | None`, and the discipline of checking for `None` at boundaries rather than discovering it in a traceback.
- Canon "sum types + exhaustiveness" → approximated by `typing.Union` with `match` statements (3.10+) and by dataclasses/enums; true exhaustiveness checking comes only from an external checker with strict settings.
- Canon "code against the contract" → duck typing and `typing.Protocol` (structural subtyping): a type is what it *does*. Contracts are conventionally documented in docstrings and enforced by tests.
- Error contract → exceptions, or explicit result-style returns (`tuple[T, None]`, result libraries) where the codebase chooses that style; mixing both in one API is the smell.

## Worked example

```python
def parse_timeout(raw: str) -> float | None:
    """Seconds, or None if unspecified — never raises on bad input."""
    raw = raw.strip()
    return float(raw) if raw else None
```

The annotation states the full contract the canon demands (Chapter 5): text in; seconds or explicit absence out; failure folded into the return. A checker verifies callers handle the `None`; the runtime would have let them forget.

## Pitfalls

- **Mutable default arguments**: `def f(x=[])` shares one list across all calls — the canonical Python type/lifetime trap.
- **Annotations trusted as enforcement**: they are not checked at runtime; untrusted input still needs validation (dataclasses with validators, pydantic, or manual checks at the boundary).
- **`==` vs `is`**: identity vs equality; `is` is for `None` and sentinels, not for values.
- **Late binding closures**: lambdas in loops capture the variable, not its value.
- **Bool is an int**: `True + 1 == 2` — type checks with `isinstance(x, int)` silently accept booleans.

## Canon cross-reference

Canonical section: **types.core** (Chapter 5, "Substance"). This port implements the canon for python; where the port and the canon disagree, the canon governs and the port is the bug.


---

# Port — Types · Rust
<!-- canonical_section: types.core | language: rust -->

## Definition

Rust is statically typed with local inference and a type system extended by *ownership*: every value has exactly one owner, moves transfer ownership, and borrows are checked at compile time against lifetimes. The borrow checker is a type-level proof system for memory safety — use-after-free, double-free, and data races are compile errors, not runtime events — purchased with programmer effort and occasional fights with the checker that are, on inspection, the checker being right.

## Idiom mapping

- Canon "make absence explicit" → `Option<T>`: there is no null. `Some`/`None` are exhaustive in `match`; absence cannot be dereferenced by accident.
- Canon "failure in the signature" → `Result<T, E>` everywhere fallibility exists; the `?` operator propagates errors explicitly, and unhandled Results warn (a `#[must_use]` type).
- Canon "sum types" → `enum` with data-carrying variants plus exhaustive `match` — the canon's full ideal, native: add a variant and every match site in the program fails to compile until handled.
- Canon "parametric polymorphism" → generics with trait bounds (monomorphized, zero-cost); trait objects (`dyn Trait`) where dynamic dispatch is actually wanted.
- Canon "newtype discipline" → the newtype pattern (a struct wrapping a primitive) makes units and domains distinct types at zero runtime cost.

## Worked example

```rust
fn parse_timeout(raw: &str) -> Option<f64> {
    let raw = raw.trim();
    if raw.is_empty() { None } else { raw.parse().ok() }
}
```

No null, no exception, no unhandled case: the type `Option<f64>` is the whole contract, and callers cannot use the value without confronting the `None` case in a `match` or combinator.

## Pitfalls

- **`unwrap()`/`expect()` in production paths**: converts a checked absence into a panic — the type system offered a contract and the code declined it.
- **`clone()` to appease the borrow checker**: silences the ownership design the checker was defending; repeated clones signal a wrong ownership shape.
- **Fighting lifetimes with `'static` and leaks** (`Box::leak`): compiles, and quietly reintroduces the memory bugs the system exists to prevent.
- **Over-general generics**: trait-bound towers that serve one call site — the canon's rule-of-three applies to abstractions in types as elsewhere.

## Canon cross-reference

Canonical section: **types.core** (Chapter 5, "Substance"). This port implements the canon for rust; where the port and the canon disagree, the canon governs and the port is the bug.
