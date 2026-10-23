#!/usr/bin/env python3
"""check_ports.py — parity check for canonical ports (see PORTING.md).

Verifies, for every port in chapters/ports/:
  * its canonical section exists (chapter file + section heading);
  * its skeleton subsections are present, in the canonical order.
And reports, for each canonical concept x major language, PRESENT or ABSENT.
A missing port is ABSENT — never passed. Stdlib only.
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CH = ROOT / "chapters"

SKELETON = ["Definition", "Idiom mapping", "Worked example", "Pitfalls", "Canon cross-reference"]
CANONICAL = {
    "types.core": ("05-types-and-formal-semantics", "Substance"),
    "concurrency.core": ("15-concurrency", "Substance"),
}
MAJOR = ["cpp", "python", "rust", "javascript", "go", "java"]


def sections_of(md):
    return [m.group(1).strip() for m in re.finditer(r"(?m)^## (.+)$", md)]


def main():
    problems = []
    # canonical sections exist?
    for cid, (ch, sec) in CANONICAL.items():
        f = CH / f"{ch}.md"
        if not f.exists():
            problems.append(f"canon {cid}: chapter file missing: {f.name}")
            continue
        if sec not in sections_of(f.read_text(encoding="utf-8")):
            problems.append(f"canon {cid}: section '{sec}' not found in {f.name}")

    ports = {}
    for pf in sorted((CH / "ports").glob("*.md")):
        md = pf.read_text(encoding="utf-8")
        m = re.search(r"canonical_section:\s*([\w.]+)\s*\|\s*language:\s*([\w+]+)", md)
        if not m:
            problems.append(f"{pf.name}: missing port header comment")
            continue
        canon_id, lang = m.group(1), m.group(2)
        secs = [s for s in sections_of(md)]
        if secs != SKELETON:
            problems.append(f"{pf.name}: skeleton mismatch — found {secs}")
        ports.setdefault(canon_id, {})[lang] = pf.name

    print("PORT PARITY REPORT")
    total_present = 0
    for cid in CANONICAL:
        for lang in MAJOR:
            state = "PRESENT" if lang in ports.get(cid, {}) else "ABSENT"
            if state == "PRESENT":
                total_present += 1
            print(f"  {cid:18s} {lang:12s} {state}")
    print(f"ports present: {total_present} / {len(CANONICAL) * len(MAJOR)} "
          f"(canonical sections: {len(CANONICAL)}, major languages: {len(MAJOR)})")
    if problems:
        print("PROBLEMS:")
        for p in problems:
            print(f"  - {p}")
    else:
        print("all present ports pass the skeleton parity check")
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main())
