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
