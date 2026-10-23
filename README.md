# AgentBibleCodec (ABC)

**The Agentic Coding Bible** — a universal compendium of coding knowledge, written for agents to learn from and practitioners to build on: Part I, the foundations of coding (computation, algorithms, data structures, paradigms, types, systems, networks, databases, compilers); Part II, the craft (design, testing, debugging, security, performance, concurrency, collaboration, documentation); Part III, the agentic layer (agent loops, tool use, harnesses, context engineering, verification, evaluation, training, accountability, failure modes, operations) — plus a canon appendix naming the definitive public source for every domain, and an errata appendix of constructed exercises in finding and correcting flawed claims.

AgentBibleCodec is a codec for coding knowledge: the complete body of material is encoded in — every language, every domain, the full text — and the filter system decodes out exactly the selection a given reader or training run needs, nothing more. What goes in is everything; what comes out is yours.

## The filter system

The book is fully modular. Every section carries metadata — `languages` (`agnostic`, or `cpp`, `python`, `rust`, `javascript`, `go`, `java`, …) and `domains` — and language-specific material always lives in its own tagged sections, never buried in untagged prose. The default is **all coding**: the full text ships complete, and you eliminate what you don't need.

```bash
python3 tools/filter_bible.py                          # the full Bible
python3 tools/filter_bible.py --languages cpp,python   # canon + C++/Python ports
python3 tools/filter_bible.py --languages rust --domains testing,security --with-studybook
```

Filtering emits a pruned `bible.md` + `bible.jsonl` with a generated preface stating what was included and excluded. Language-agnostic (canonical) material is always included — a selection narrows the ports, never the canon.

## Languages: the canonical-spec + verified-ports method

Concepts that vary by language have **one canonical master section** — the spec: definition, semantics, invariants, pitfalls-in-general. Each language's treatment is a **port** of that canon with an identical skeleton (definition, idiom mapping, worked example, pitfalls, canon cross-reference) and metadata (`port_of`) linking it to its canon. Adding a language means porting the canon, section by section, per the protocol in **PORTING.md** — which is what makes "all coding languages" an extensible property of the project rather than a claim about any single edition. `tools/check_ports.py` verifies every port's skeleton against its canon and reports missing ports as **ABSENT**, never as passed. v1 ships ports for C++, Python, Rust, JavaScript/TypeScript, Go, and Java for the concepts designated canonical-with-ports; `bible-index.json` carries the full canonical↔port mapping.

## The notation layer and the study book

Reading is meant to be active. Per **NOTATION.md**, a reader can select any passage and **Notate** it: the selection is routed to a personal study book (`studybook/`) with full provenance — part/chapter/section, the passage verbatim, a passage hash, the section's language/domain tags, a timestamp, and the reader's own note. `tools/annotate.py` manages the study book (`add`, `list`, `export`); notations of kind `correction` — a reader catching the text being wrong — are first-class training material, flagged as such on export. The study book respects the same filter system (`--with-studybook`).

## Files

- `chapters/` — the 29 chapter files (plus `chapters/ports/` for language ports)
- `bible.md` — the full book, assembled
- `bible.jsonl` — training-ready sections with tags (`chapter`, `section`, `tier`, `languages`, `domains`, `text`)
- `bible-index.json` — the full structure: parts, chapters, sections, tags, word counts, canonical↔port mapping
- `tools/` — `filter_bible.py`, `annotate.py`, `check_ports.py`, `build_bible.py` (all stdlib-only Python)
- `PORTING.md`, `NOTATION.md`, `MANIFEST.md` — the port protocol, the notation contract, and the book's provenance/scope record
- `studybook/` — seeded empty; fills as you notate

## License

Dual-licensed, by kind: the **code** (everything under `tools/` and any other software in this repository) is under the **MIT License** — see `LICENSE`. The **text** of the Bible (the chapters, `bible.md`, `bible.jsonl`, and the study-book material) is under the **Creative Commons Attribution 4.0 International License (CC BY 4.0)** — see `LICENSE-TEXT.md`.
