# MANIFEST — The Agentic Coding Bible (AgentBibleCodec, v1)

**Date:** 2026-10-22 · **Location:** `~/workspace/gemma-agent/corpus/agentic-coding-bible/` · **Repo tree:** `~/workspace/AgentBibleCodec-repo/`

## Provenance statement

This text is **original synthesis**. Every substantive claim is either (a) grounded in a named canonical public source, cited in place (list below), or (b) stated as a general principle/doctrine of the craft. **The text contains no material about any specific laboratory, company, product, person, or internal incident** — no names, measurements, or histories from any particular organization appear anywhere in it. Universal principles are stated as universals. The Errata appendix (Appendix A) consists of **constructed teaching exercises** — invented claims, explicitly labeled as such — not reports of real events.

## Structure and word counts

Word counts are whitespace-delimited words of the chapter files (headings included). Total: **24,352 words** across 29 chapters + 12 port sections; `bible.jsonl` carries **225 sections** (~23,419 words of section text).

### Part I — The Foundations of Coding (full teaching text)
| # | Chapter | Words |
|---|---------|-------|
| 01 | Computation and Computability | 638 |
| 02 | Algorithms and Complexity | 608 |
| 03 | Data Structures | 565 |
| 04 | Paradigms and Language Design | 542 |
| 05 | Types and Formal Semantics | 635 |
| 06 | Operating Systems, Processes, Memory | 609 |
| 07 | Networking and Distributed Systems | 578 |
| 08 | Databases and Storage | 594 |
| 09 | Compilers, Interpreters, Runtimes | 537 |

### Part II — The Craft (full teaching text)
| # | Chapter | Words |
|---|---------|-------|
| 10 | Software Design and Architecture | 533 |
| 11 | Testing and Verification | 556 |
| 12 | Debugging Method | 548 |
| 13 | Security | 612 |
| 14 | Performance and Optimization | 559 |
| 15 | Concurrency | 523 |
| 16 | Version Control and Collaboration | 481 |
| 17 | Documentation and Readability | 565 |

### Part III — The Agentic Layer (full teaching text)
| # | Chapter | Words |
|---|---------|-------|
| 18 | Agent Loops and Tool Use | 667 |
| 19 | Harness Design | 704 |
| 20 | Context Engineering | 635 |
| 21 | Verification and Selection | 705 |
| 22 | Evaluation and Measurement | 611 |
| 23 | Training Agents | 756 |
| 24 | Mandates, Receipts, Accountability | 801 |
| 25 | Failure Modes of Agentic Systems | 694 |
| 26 | Operations | 773 |
| 27 | Principles of Practice (closing) | 606 |

### Appendices
| # | Chapter | Words |
|---|---------|-------|
| 28 | Appendix A — Errata Exercises (constructed) | 1,820 |
| 29 | Appendix B — The Canon (bibliography by domain) | 710 |

### Ports (canonical-spec + verified-ports method; see `PORTING.md`)
| Canonical section | Language | Words | | Canonical section | Language | Words |
|---|---|---|---|---|---|---|
| types.core | cpp | 378 | | concurrency.core | cpp | 461 |
| types.core | python | 404 | | concurrency.core | python | 389 |
| types.core | rust | 392 | | concurrency.core | rust | 453 |
| types.core | javascript | 446 | | concurrency.core | javascript | 457 |
| types.core | go | 457 | | concurrency.core | go | 471 |
| types.core | java | 440 | | concurrency.core | java | 439 |

## Honest scope note

- **Full teaching text in v1:** all 27 chapters and both appendices are complete, self-contained teaching text — principle, mechanism/substance, worked material, failure modes, and a closing falsifiable **Rule** per chapter. Chapter depth is deliberately concentrated (roughly 500–800 words per chapter): each chapter teaches the load-bearing core of its domain at the level an agent can act on, and names its canon (Appendix B) for the depth no single volume holds.
- **Reference-depth in v1:** the foundations (Part I) compress fields that fill shelves — computability, complexity, databases — into their operative cores. This is by design, not omission-by-accident: the Bible's unit of completeness is *the agent's working need*, and Appendix B is the explicit index of where the rest of human coding knowledge lives.
- **Ports:** v1 designates **2 canonical sections** for per-language treatment (`types.core`, `concurrency.core`) and ships **12 of 12** major-language ports (cpp, python, rust, javascript, go, java), all passing the skeleton parity check (`tools/check_ports.py`: **12 PRESENT / 0 problems**). All other concepts are currently **agnostic-only** — their per-language ports are **ABSENT** (not passed, not implied), to be added per the protocol in `PORTING.md`. Adding canonical concepts (error handling, memory management, async models, package ecosystems) and their ports is the v2 volume plan, together with deepening Part I chapters toward reference depth.

## Adaptability — filter verification (measured)

- Full Bible: **225 sections, ~23,419 words** (`tools/filter_bible.py` with no selection reproduces it exactly: 225/225).
- Selection `--languages cpp,python`: **177 sections, ~20,018 words**; kept ports are exactly the cpp and python ports of both canonical sections; **agnostic sections lost: 0** (verified programmatically — every canonical section of every chapter survives the filter; pruning touches only non-selected language ports).

## Notation layer / study book

Feature per `NOTATION.md`: select any passage → Notate → routed to `studybook/` with provenance (chapter/section, verbatim passage, SHA-256 passage hash, inherited language/domain tags, timestamp, reader note). Entry schema: `{id, created, chapter, section, passage, passage_sha256, languages, domains, note, kind: highlight|correction|question}`. Tooling: `tools/annotate.py` (`add`/`list`/`export`); export emits training-format JSONL with `tier: "studybook"` and flags `kind: "correction"` entries `"mastery_gold": true`. The study book is seeded empty and respects the filter system (`--with-studybook`). Tool chain verified end-to-end on a scratch copy (add → render → export, correction flagged).

## Mastery criterion (acceptance test for the trained model)

The material is mastered when a model trained on it can **correct errors in it**. Post-training acceptance is a **held-out correction test**: errors are planted in passages the model has never seen (drawn from outside the training text); the model is scored on **flag rate** (planted errors caught), **correction accuracy** (the fix is the true claim, mechanistically explained), and **false-alarm rate** (correct passages wrongly flagged). The trained adapter is compared against the **untrained baseline** on the identical test; the delta is the evidence of mastery. Appendix A's claim → flaw → correction → evidence exercises are the training-form of this test.

## Canonical citations

Turing (1936); Shannon (1948); Rice's theorem; Codd (1970); Hoare (1969, CSP 1978); Lamport (1978); Brewer CAP (2000) with Gilbert & Lynch (2002); Knuth, TAOCP; Cormen et al., CLRS; Wirth (1976); Abelson & Sussman, SICP; Pierce, TAPL; Gamma et al., Design Patterns (1994); Amdahl (1967); Claessen & Hughes, QuickCheck (2000); Zeller, Why Programs Fail; Schneier & Kelsey (1999); RFC 6962; RFC 7519; OWASP Top 10 / ASVS; Yao et al., ReAct (2022); Shinn et al., Reflexion (2023); Yao et al., Tree of Thoughts (2023); Yang et al., SWE-agent (2024); Jimenez et al., SWE-bench (2024); Liu et al., Lost in the Middle (2023); Hu et al., LoRA (2021); Zelikman et al., STaR (2022); Micikevicius et al., Mixed Precision Training (2018); Miller, capability security (2006); Herlihy & Shavit; Tanenbaum; Kleppmann, DDIA; Arpaci-Dusseau, OSTEP; Bryant & O'Hallaron, CS:APP; Aho et al., Dragon Book; Hennessy & Patterson; Brooks; Evans; Humble & Farley.

## Not grounded / flagged

- Appendix B's agentic-layer entries are dated as of 2026 in the text itself; the frontier moves and the appendix says so.
- No claim in the Bible rests on any organization's internal data; where the wider field reports contested results (e.g., exact magnitudes of position bias in long contexts), the text states the mechanism and the direction, not a borrowed number.
