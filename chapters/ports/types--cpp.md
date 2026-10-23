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
