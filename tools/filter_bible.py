#!/usr/bin/env python3
"""filter_bible.py — decode a selection of the Bible.

Usage:
    python3 tools/filter_bible.py [--languages cpp,python] [--domains testing,security]
                                  [--with-studybook] [--out-dir DIR]

Rules:
  * No selection at all  -> the full Bible, unchanged.
  * Language-AGNOSTIC sections are ALWAYS included (the canon ships whole).
  * Language-specific sections (ports) are included only when their language
    is selected; when --domains is also given, a port must additionally match
    a selected domain (ports currently carry no domains, so a domain filter
    prunes ports unless the port is tagged for it).
  * Domain filtering never removes agnostic material (see preface in output).
  * --with-studybook also includes study book entries (studybook/notations.jsonl)
    that pass the same language/domain test, rendered after the Bible text.

Outputs <out-dir>/bible.md and <out-dir>/bible.jsonl (default: ./filtered/).
Stdlib only.
"""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def passes(entry, langs, domains):
    el = entry.get("languages", ["agnostic"])
    if "agnostic" in el:
        return True                      # canon always ships
    if langs is not None and not (set(el) & langs):
        return False
    if domains is not None:
        ed = set(entry.get("domains", []))
        if ed and not (ed & domains):
            return False
    return True


def main():
    ap = argparse.ArgumentParser(description="Decode a selection of the Agentic Coding Bible.")
    ap.add_argument("--languages", help="comma list, e.g. cpp,python")
    ap.add_argument("--domains", help="comma list, e.g. testing,security")
    ap.add_argument("--with-studybook", action="store_true",
                    help="also include matching study book entries")
    ap.add_argument("--out-dir", default=str(ROOT / "filtered"))
    args = ap.parse_args()

    langs = set(args.languages.split(",")) if args.languages else None
    domains = set(args.domains.split(",")) if args.domains else None

    entries = [json.loads(l) for l in (ROOT / "bible.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
    kept = [e for e in entries if passes(e, langs, domains)]

    out = Path(args.out_dir)
    out.mkdir(parents=True, exist_ok=True)
    with open(out / "bible.jsonl", "w", encoding="utf-8") as f:
        for e in kept:
            f.write(json.dumps(e, ensure_ascii=False) + "\n")

    def wcount(es):
        return sum(len(e["text"].split()) for e in es)

    preface = [
        "# The Agentic Coding Bible — decoded selection\n",
        f"Selection: languages={sorted(langs) if langs else 'ALL'}, "
        f"domains={sorted(domains) if domains else 'ALL'}, studybook={args.with_studybook}.",
        f"Included: {len(kept)} of {len(entries)} sections, ~{wcount(kept)} of ~{wcount(entries)} words.",
        "All language-agnostic (canonical) material is always included. "
        "Excluded: language-specific sections whose language was not selected"
        + ("; sections outside the selected domains where tagged." if domains else "."),
        "",
    ]
    chunks = ["\n".join(preface)]
    for e in kept:
        chunks.append(f"\n\n## [{e['chapter']}] {e['section']}\n\n{e['text']}")

    sb_notes = []
    if args.with_studybook:
        sb = ROOT / "studybook" / "notations.jsonl"
        if sb.exists():
            for line in sb.read_text(encoding="utf-8").splitlines():
                if not line.strip():
                    continue
                n = json.loads(line)
                probe = {"languages": n.get("languages", ["agnostic"]),
                         "domains": n.get("domains", [])}
                if passes(probe, langs, domains):
                    sb_notes.append(n)
        chunks.append("\n\n---\n\n# Study Book (notations matching this selection)\n")
        if not sb_notes:
            chunks.append("\n*(No notations match this selection, or the study book is empty.)*")
        for n in sb_notes:
            chunks.append(f"\n\n### [{n['chapter']}] {n['section']} — {n['kind']}\n\n> {n['passage']}\n\n{n.get('note','')}")

    (out / "bible.md").write_text("\n".join(chunks) + "\n", encoding="utf-8")
    print(f"kept {len(kept)}/{len(entries)} sections, ~{wcount(kept)}/{wcount(entries)} words "
          f"-> {out}/bible.md, {out}/bible.jsonl; studybook entries included: {len(sb_notes)}")


if __name__ == "__main__":
    main()
