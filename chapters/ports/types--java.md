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
