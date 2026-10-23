# PORTING.md — Adding a Language to AgentBibleCodec

AgentBibleCodec covers every coding language by the **canonical-spec + verified-ports method**: each concept that needs language-specific treatment has exactly ONE canonical master section (the canon: definition, semantics, invariants, pitfalls-in-general — language-agnostic). Every language's treatment is a **port** of that canon. A language is *covered* for a concept when a verified port exists; otherwise its status is **ABSENT** — never "passed," never implied.

## The port skeleton (identical for every port, in this order)

1. `## Definition` — the concept as this language defines it: its model, its guarantees, its place in the type/runtime system.
2. `## Idiom mapping` — how each element of the canonical section is expressed (or consciously not expressed) in this language's native idioms. Gaps are stated as gaps, not papered over.
3. `## Worked example` — one small, complete, idiomatic example embodying the canonical contract, annotated where the canon shows through.
4. `## Pitfalls` — the language-specific failure modes of this concept: the traps a practitioner actually hits, each with its mechanism.
5. `## Canon cross-reference` — names the canonical section id and states the precedence rule: *where the port and the canon disagree, the canon governs and the port is the bug.*

Each port file carries a header comment: `<!-- canonical_section: <canon id> | language: <tag> -->`, and its JSONL/index metadata carries `port_of: <canon id>` and `languages: [<tag>]`.

## The protocol

1. **Read the canon first.** The canonical section is the spec. If the canon seems wrong, the fix goes to the canon (and every port is re-checked), never into a quiet port divergence.
2. **Port section by section**, preserving the skeleton exactly — same subsections, same order. The skeleton is what makes parity checkable by a machine instead of by taste.
3. **Write to the language's grain**: examples must be code a native practitioner would write, idioms named by their community names, pitfalls drawn from the language's real failure record.
4. **Run the parity check**: `python3 tools/check_ports.py` — it verifies each port's skeleton against its canon and lists every missing port per language as ABSENT.
5. **Register the port** by rebuilding the index (`python3 tools/build_bible.py` regenerates `bible-index.json`, which carries the canonical↔port mapping).

## Coverage states

- **PRESENT** — port exists and passes the skeleton parity check.
- **ABSENT** — no port exists. This is a normal, honest state: the canon still ships and teaches the concept; the language simply has no port yet.
- Coverage is claimed per concept per language, never globally. "All languages" is the protocol's property — any language can be added by porting — not a claim that every port exists today.
