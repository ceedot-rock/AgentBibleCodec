# Chapter 20 — Context Engineering

## Principle

A language model's context window is its entire working memory: everything it can consider is what's in the window, and everything in the window competes for its attention and its budget. Context engineering is the discipline of deciding what enters, in what form, in what order, and what is deliberately kept out or externalized — the prompt is a designed artifact, not a transcript that happens to accumulate.

## Substance

**The budget is real and compositional.** System instructions, tool definitions, task statement, observations, history, and the model's own reasoning all draw from the same finite window (tens of thousands of tokens in small-model settings; more in frontier ones — the discipline is identical, only the numbers change). Serving stacks manage overflow by compaction — summarizing or dropping history — which means *the system will forget on your behalf if you do not choose what is forgotten*. Load-bearing facts (the exact failing assertion, the enumerated target list, the current plan and its status) must live in external artifacts the agent re-reads — notes, files, structured state — not only in history that compaction can take.

**Selection beats volume.** Retrieval (search by the literal error string, by symbol, by similarity) exists to put the *relevant* slice in front of the model: function-level reads rather than whole files; the failing test and its fixtures rather than the suite; neighbors of the code under change rather than the repository. Reading order matters: specification (tests) before implementation before surroundings. Every irrelevant token admitted taxes attention and evicts, eventually, a relevant one.

**Structure helps the model use what it has:** stable instruction placement (system material first, where models weight it), clear delimiters between instruction, data, and observation (untrusted content must be *formatted* as data — prompt injection is what happens when the boundary fails), summaries that preserve decisions and discard transcripts, and just-in-time loading (fetch detail when the decision needing it arrives, not speculatively at the start).

**Context failure has names:** *overflow* (the window is exceeded and the run dies or truncates mid-thought); *rot* (early decisive facts are compacted away and late behavior degrades into re-derivation and contradiction); *poisoning* (irrelevant or adversarial content crowds out the task); *lost-in-the-middle* (empirically, models underuse information buried mid-context — after Liu et al., *Lost in the Middle*, 2023 — so placement is a quality decision, not cosmetics).

## Worked example

An agent debugging a failure reads the full 1,800-line module, the full test file, and three full neighboring files "for context" — 60% of its window gone before its first hypothesis. The decisive line (the assertion in one test) sits in the middle of that mass. It then re-reads two of the files after compaction discards them, spending budget to recover what it already paid for once. The disciplined run: search the error string; read the failing test (40 lines) and its fixture; read the implicated function (60 lines) and its callers; write the hypothesis and target list to notes. Same task, a tenth of the context, and the window still holds room for the repair iterations — which are where tasks are actually won.

## Failure mode

The maximal-read anti-pattern ("include everything, to be safe"); trusting auto-compaction to preserve the one number that matters; treating retrieved text as instruction (injection); and its quiet cousin — letting tool output formats bloat (verbose JSON, repeated headers, stack traces with no signal lines) until the observation channel is mostly noise.

## Rule

> **Rule.** Every run maintains its load-bearing state — target list with current status, exact failure text, current plan — in an external artifact re-read after any compaction. A trace in which the agent re-derives or contradicts state its own earlier observations established is a context-discipline failure, charged to the harness design, not to the model's memory.
