# NOTATION.md — The Notation Layer: From Reading to a Study Book

The Bible is meant to be *worked with*, not just read. The notation layer is the contract by which any reader (human, via a UI; or a program) can select any passage and route it into their personal **study book**, with provenance intact.

## The interaction

1. The reader selects/highlight any passage in any rendering of the Bible.
2. The reader invokes **Notate** and optionally attaches their own note and a *kind*.
3. The selection is appended to the study book with full provenance:
   - **part / chapter / section** the passage came from;
   - **the passage, verbatim**;
   - **a passage hash** — SHA-256 over the passage text, so the study book can later verify the passage still matches the source (and detect that the source has moved on);
   - **the section's language/domain tags**, inherited from the Bible's own metadata, so the study book filters with the same system as the Bible (see `tools/filter_bible.py --with-studybook`);
   - **a timestamp**;
   - **the reader's note**, attached verbatim.

Any reader UI that implements this contract — select → Notate → append with the fields below — is compatible with the study book format and tooling in this project. No UI is specified or required by this document; the contract is the data.

## The study book

Directory: `studybook/`

- `studybook/notations.jsonl` — the append-only record, one JSON object per notation.
- `studybook/studybook.md` — the human-readable rendering, generated from the JSONL by `tools/annotate.py`, grouped by chapter.

### Entry schema

```json
{
  "id": "n-0001",
  "created": "2026-10-22T20:15:00Z",
  "chapter": "19-harness-design",
  "section": "Substance",
  "passage": "the selected text, verbatim",
  "passage_sha256": "<sha256 hex of the passage, utf-8>",
  "languages": ["agnostic"],
  "domains": ["harness-design"],
  "note": "the reader's own note, may be empty",
  "kind": "highlight | correction | question"
}
```

Field rules: `id` is assigned sequentially by the tool (`n-0001`, …); `passage_sha256` is computed over the passage exactly as stored; `languages`/`domains` are inherited from the source section's metadata unless explicitly overridden; `kind` is one of `highlight` (worth remembering), `question` (worth resolving), `correction` (the reader asserts the passage is wrong and says why, in the note).

## Tooling

`tools/annotate.py` (stdlib only):

- `add --chapter <id> --section <name> --passage <text> [--note <text>] [--kind highlight|correction|question] [--languages a,b] [--domains a,b]` — appends to `notations.jsonl` and re-renders `studybook.md`.
- `list [--kind correction]` — prints notations.
- `export [--out file]` — emits the study book as training-format JSONL in the same shape as `bible.jsonl` entries, with `tier: "studybook"`. Entries of kind `correction` are additionally flagged `"mastery_gold": true` — a human correcting the material is demonstrating exactly the behavior the mastery criterion (see MANIFEST.md) trains and tests: error → correction, produced by a reader who understood the text deeply enough to catch it being wrong.

## Filtering

The study book respects the Bible's filter system: every notation carries its section's tags, and `tools/filter_bible.py --with-studybook` includes study book entries that match the selection (with the same inclusion rules as Bible sections), so a pruned Bible can ship with exactly the study material relevant to it.
