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
