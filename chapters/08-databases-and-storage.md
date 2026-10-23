# Chapter 8 — Databases and Storage

## Principle

Storage is where a system's promises become permanent. The database chapter of an agent's education is about guarantees — durability, consistency, atomicity — and their prices, because every storage bug is a broken promise discovered later, usually by a user, usually at the worst time.

## Substance

**The relational model** (after Codd, 1970): data as relations — tables of tuples — manipulated declaratively (SQL), with the engine choosing access paths. Normalization removes update anomalies by removing redundancy; controlled denormalization buys read performance at the price of re-introducing them deliberately. Keys, foreign keys, and constraints are the schema enforcing invariants the application would otherwise have to — the same "where do facts live" question as types (Chapter 5), one level down.

**Transactions and ACID:** Atomicity (all or nothing — the remedy for partial writes), Consistency (invariants hold across the transaction), Isolation (concurrent transactions don't see each other's intermediate states — at a chosen level: read committed, repeatable read, serializable; the levels are a priced menu of anomalies prevented), Durability (committed means surviving a crash — paid for with fsyncs, Chapter 6). An agent must know which isolation level its code runs under and which anomaly that level *permits* (dirty reads, non-repeatable reads, phantoms, write skew) — the default is rarely serializable.

**Indexing:** a B-tree index turns a scan into a logarithmic lookup at the cost of write amplification and storage; a hash index trades ordering away for point lookups; composite indexes serve prefix queries in column order. The query planner chooses paths from statistics; "the query is slow" is usually "the planner lacked an index or fresh statistics," and the diagnostic instrument is the query plan (EXPLAIN), not intuition.

**The alternatives, honestly placed:** key-value stores (simplicity, scale, minimal queries), document stores (flexible records, weaker cross-record invariants), wide-column and time-series stores (access-pattern-shaped), object storage (immutable blobs, eventual semantics). The NoSQL trade is consistent: give up general queries and cross-record transactions, gain horizontal scale and schema flexibility. BASE (basically available, soft state, eventual consistency) is the honest label for what replaces ACID.

**Replication and consistency models** (Chapter 7's trade-offs made concrete): single-leader, multi-leader, leaderless; strong vs eventual consistency; read-your-writes and monotonic reads as session guarantees users actually notice when violated.

## Worked example

Two concurrent transfers debit the same account. Under read-committed, both read balance 100, both subtract 80, both commit "successfully" — final balance 20 or −60 depending on write order, and an overdraft the business forbids. The fixes, in ascending strength: an atomic conditional update (`UPDATE … SET balance = balance − 80 WHERE balance ≥ 80`, checking rows affected), a uniqueness/CHECK constraint in the schema, or a serializable transaction. The lesson generalizes: *concurrency correctness belongs in the storage layer's guarantees, not in application hope* — application code reading-then-writing across a gap is a race with extra steps (Chapter 15).

## Failure mode

N+1 queries (an ORM loop issuing a query per row — invisible in tests, fatal at scale); missing transactions around multi-write operations (crash = partial state); schema migrations deployed without a rollback story; assuming eventual consistency is immediate ("I wrote it, why can't I read it?"); and indexes added by superstition until writes crawl. Each is measurable with the planner and the slow-query log before it is an incident.

## Rule

> **Rule.** For every stored invariant (non-negative balances, unique emails, referential integrity), name the mechanism that enforces it — constraint, transaction isolation level, or atomic conditional write — at the storage layer. "The application checks first" is not a mechanism under concurrency.
