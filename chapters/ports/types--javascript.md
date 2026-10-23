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
