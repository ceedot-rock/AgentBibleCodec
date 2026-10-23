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
