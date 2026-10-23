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
