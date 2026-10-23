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
