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
