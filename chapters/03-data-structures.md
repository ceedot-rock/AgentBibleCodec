# Chapter 3 — Data Structures

## Principle

Programs are algorithms plus data structures (Wirth's title says it exactly: *Algorithms + Data Structures = Programs*, 1976). The structure chosen determines which operations are cheap, which are ruinous, and — less obviously — which bugs are even possible. Most "algorithm problems" in production code are actually data-structure selection problems wearing a disguise.

## Substance

**The core inventory and their honest costs:**

- **Arrays / lists:** O(1) indexed access, O(n) insertion in the middle, cache-friendly. The default; deviate only for a reason.
- **Linked lists:** O(1) insertion at a held node, O(n) access, cache-hostile. Rarely the right answer on modern hardware despite textbook nostalgia.
- **Hash tables:** expected O(1) lookup/insert/delete; the cost is hash quality, load factor, and worst-case degradation. Iteration order is not a contract unless the implementation makes it one.
- **Balanced search trees** (red-black, AVL, B-trees): guaranteed O(log n) operations and *ordered* traversal. B-trees' wide fanout is why they own disk-based indexing (Chapter 8): one node per block read.
- **Heaps / priority queues:** O(log n) insert and extract-min; the engine inside Dijkstra, schedulers, top-k problems, and event simulations.
- **Stacks and queues:** LIFO/FIFO disciplines — call stacks, undo histories, BFS frontiers, work queues, backpressure buffers.
- **Graphs:** adjacency list (sparse) vs adjacency matrix (dense); the representation choice changes every operation's cost and memory by orders of magnitude.
- **Tries, bloom filters, disjoint-set (union-find), ring buffers:** specialized structures that each turn a specific expensive question into a cheap one — prefix lookup, probable membership with one-sided error, connectivity, fixed-size recent history.

**The selection method** is operational: list the operations the workload actually performs, their frequencies, and the size regime; then choose the structure whose cost profile matches. "We need fast lookup by id, occasional range scans by time, 10⁸ entries, mostly appends" selects a B-tree-family structure; "fast lookup only, 10⁴ entries, in memory" selects a hash map. Requirements first, nostalgia never.

**Invariants.** Every structure maintains invariants (heap property, BST ordering, red-black balance rules), and every bug in a structure is an invariant broken at one operation and discovered at another. Correct implementations state the invariant and check it in tests; concurrent structures add the question of *when* the invariant is observable (Chapter 15).

## Worked example

Implementing an LRU cache: requirements — get and put in O(1), evict least-recently-used. A hash map alone gives O(1) lookup but no recency order; a list alone gives order but O(n) lookup. The composition — hash map from key to node in a doubly linked list ordered by recency — gives both operations O(1) and eviction at the tail. This pattern (compose two simple structures so each covers the other's weakness) is the most reusable design move in the chapter.

## Failure mode

The default-container trap: reaching for the language's list/map for every shape of data, then discovering O(n) scans inside hot loops, or hash-map iteration order leaking into output and making tests flaky. And the exotic trap: implementing a sophisticated structure where a sorted array and binary search would be faster, smaller, and provably correct.

## Rule

> **Rule.** For every non-trivial collection in a design, name the three most frequent operations and their required bounds; the chosen structure must meet all three on paper before it is coded. If it cannot, compose structures or change the access pattern — do not hope the workload stays small.
