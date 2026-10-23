#!/usr/bin/env python3
"""annotate.py — the study book tool (see NOTATION.md). Stdlib only.

    python3 tools/annotate.py add --chapter 19-harness-design --section Substance \
        --passage "..." [--note "..."] [--kind highlight|correction|question]
    python3 tools/annotate.py list [--kind correction]
    python3 tools/annotate.py export [--out file]
"""
import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SB = ROOT / "studybook"
JSONL = SB / "notations.jsonl"
MD = SB / "studybook.md"

HEADER = ("# Study Book\n\n"
          "Personal notations routed from the Agentic Coding Bible via the notation "
          "layer (see `../NOTATION.md`). This file is generated from `notations.jsonl` "
          "by `tools/annotate.py` — it fills as the reader notates.\n")


def load():
    if not JSONL.exists():
        return []
    return [json.loads(l) for l in JSONL.read_text(encoding="utf-8").splitlines() if l.strip()]


def render(notes):
    chunks = [HEADER]
    if not notes:
        chunks.append("\n*(No notations yet.)*\n")
    by_ch = {}
    for n in notes:
        by_ch.setdefault(n["chapter"], []).append(n)
    for ch in sorted(by_ch):
        chunks.append(f"\n## {ch}\n")
        for n in by_ch[ch]:
            chunks.append(f"\n### {n['id']} · {n['section']} · {n['kind']} · {n['created']}\n")
            chunks.append(f"\n> {n['passage']}\n")
            if n.get("note"):
                chunks.append(f"\n{n['note']}\n")
            chunks.append(f"\n*tags: {', '.join(n.get('languages', []))} · "
                          f"{', '.join(n.get('domains', []))} · sha256 {n['passage_sha256'][:12]}…*\n")
    MD.write_text("\n".join(chunks), encoding="utf-8")


def main():
    ap = argparse.ArgumentParser(description="Study book (notation) tool")
    sub = ap.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("add")
    a.add_argument("--chapter", required=True)
    a.add_argument("--section", required=True)
    a.add_argument("--passage", required=True)
    a.add_argument("--note", default="")
    a.add_argument("--kind", default="highlight", choices=["highlight", "correction", "question"])
    a.add_argument("--languages", default="agnostic")
    a.add_argument("--domains", default="")
    sub.add_parser("list").add_argument("--kind", default=None)
    e = sub.add_parser("export")
    e.add_argument("--out", default=str(SB / "studybook-export.jsonl"))
    args = ap.parse_args()

    notes = load()
    if args.cmd == "add":
        entry = {
            "id": f"n-{len(notes) + 1:04d}",
            "created": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "chapter": args.chapter,
            "section": args.section,
            "passage": args.passage,
            "passage_sha256": hashlib.sha256(args.passage.encode("utf-8")).hexdigest(),
            "languages": [s for s in args.languages.split(",") if s],
            "domains": [s for s in args.domains.split(",") if s],
            "note": args.note,
            "kind": args.kind,
        }
        SB.mkdir(parents=True, exist_ok=True)
        with open(JSONL, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
        render(load())
        print(f"added {entry['id']} ({entry['kind']}) -> {JSONL}; studybook.md re-rendered")
    elif args.cmd == "list":
        for n in notes:
            if args.kind and n["kind"] != args.kind:
                continue
            print(f"{n['id']} [{n['kind']}] {n['chapter']} / {n['section']}: {n['passage'][:80]}…")
        print(f"{len(notes)} notation(s) total")
    elif args.cmd == "export":
        out = Path(args.out)
        with open(out, "w", encoding="utf-8") as f:
            for n in notes:
                e = {"chapter": n["chapter"], "section": n["section"],
                     "tier": "studybook", "kind": n["kind"],
                     "languages": n.get("languages", ["agnostic"]),
                     "domains": n.get("domains", []),
                     "text": n["passage"] + (("\n\nNote: " + n["note"]) if n.get("note") else "")}
                if n["kind"] == "correction":
                    e["mastery_gold"] = True   # human corrections: what the model must learn to produce
                f.write(json.dumps(e, ensure_ascii=False) + "\n")
        print(f"exported {len(notes)} notation(s) -> {out} "
              f"({sum(1 for n in notes if n['kind'] == 'correction')} correction(s) flagged mastery_gold)")


if __name__ == "__main__":
    main()
