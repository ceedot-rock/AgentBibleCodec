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
