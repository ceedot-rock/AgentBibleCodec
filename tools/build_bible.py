#!/usr/bin/env python3
"""Build bible.md, bible.jsonl, and bible-index.json from chapters/.

Stdlib only. Chapter metadata (part, domains) lives in CHAPTER_META below;
ports declare their own metadata in a header comment:
    <!-- canonical_section: types.core | language: python -->
Canonical section ids for port targets:
    types.core       -> chapter 05, section "Substance"
    concurrency.core -> chapter 15, section "Substance"
"""
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CH = ROOT / "chapters"

CHAPTER_META = {
    "01-computation-and-computability": ("Part I — The Foundations of Coding", ["computation", "theory"]),
    "02-algorithms-and-complexity": ("Part I — The Foundations of Coding", ["algorithms", "complexity"]),
    "03-data-structures": ("Part I — The Foundations of Coding", ["data-structures", "algorithms"]),
    "04-paradigms-and-language-design": ("Part I — The Foundations of Coding", ["paradigms", "language-design"]),
    "05-types-and-formal-semantics": ("Part I — The Foundations of Coding", ["types", "semantics"]),
    "06-operating-systems-processes-memory": ("Part I — The Foundations of Coding", ["operating-systems", "memory", "processes"]),
    "07-networking-and-distributed-systems": ("Part I — The Foundations of Coding", ["networking", "distributed-systems"]),
    "08-databases-and-storage": ("Part I — The Foundations of Coding", ["databases", "storage"]),
    "09-compilers-interpreters-runtimes": ("Part I — The Foundations of Coding", ["compilers", "runtimes"]),
    "10-software-design-and-architecture": ("Part II — The Craft", ["design", "architecture"]),
    "11-testing-and-verification": ("Part II — The Craft", ["testing", "verification"]),
    "12-debugging-method": ("Part II — The Craft", ["debugging", "method"]),
    "13-security": ("Part II — The Craft", ["security"]),
    "14-performance-and-optimization": ("Part II — The Craft", ["performance", "optimization"]),
    "15-concurrency": ("Part II — The Craft", ["concurrency"]),
    "16-version-control-and-collaboration": ("Part II — The Craft", ["version-control", "collaboration"]),
    "17-documentation-and-readability": ("Part II — The Craft", ["documentation", "readability"]),
    "18-agent-loops-and-tool-use": ("Part III — The Agentic Layer", ["agent-loops", "tool-use"]),
    "19-harness-design": ("Part III — The Agentic Layer", ["harness-design"]),
    "20-context-engineering": ("Part III — The Agentic Layer", ["context-engineering"]),
    "21-verification-and-selection": ("Part III — The Agentic Layer", ["verification", "selection"]),
    "22-evaluation-and-measurement": ("Part III — The Agentic Layer", ["evaluation", "measurement"]),
    "23-training-agents": ("Part III — The Agentic Layer", ["training", "fine-tuning"]),
    "24-mandates-receipts-accountability": ("Part III — The Agentic Layer", ["accountability", "mandates", "receipts"]),
    "25-failure-modes": ("Part III — The Agentic Layer", ["failure-modes", "reliability"]),
    "26-operations": ("Part III — The Agentic Layer", ["operations", "production"]),
    "27-principles-of-practice": ("Closing", ["principles", "practice"]),
    "28-appendix-a-errata-exercises": ("Appendices", ["critique", "errata"]),
    "29-appendix-b-canon": ("Appendices", ["canon", "bibliography"]),
}

CANONICAL = {
    "types.core": {"chapter": "05-types-and-formal-semantics", "section": "Substance"},
    "concurrency.core": {"chapter": "15-concurrency", "section": "Substance"},
}


def words(text):
    return len(re.findall(r"\S+", text))


def split_sections(md):
    """Split markdown on '## ' headings. Returns [(section_name, body)]."""
    parts = re.split(r"(?m)^## ", md)
    out = []
    head = parts[0]
    # strip the leading '# Title' line from the pre-section head
    head_body = re.sub(r"(?m)^# .*\n", "", head, count=1).strip()
    if head_body:
        out.append(("(intro)", head_body))
    for p in parts[1:]:
        name, _, body = p.partition("\n")
        out.append((name.strip(), body.strip()))
    return out


def chapter_title(md):
    m = re.search(r"(?m)^# (.+)$", md)
    return m.group(1).strip() if m else ""


def build():
    entries = []          # bible.jsonl entries
    index = {"title": "The Agentic Coding Bible", "project": "AgentBibleCodec",
             "version": "v1", "date": "2026-10-22", "parts": [], "canonical": {}, "ports": []}
    parts_map = {}
    md_chunks = [
        "# The Agentic Coding Bible\n\n"
        "**AgentBibleCodec** — a codec for coding knowledge: everything encoded in, your selection decoded out.\n\n"
        "v1 · 2026-10-22\n\n"
        "This book is modular and filterable. The full text is the default; "
        "`tools/filter_bible.py` decodes the selection you ask for (languages, domains). "
        "See `MANIFEST.md` for structure, `PORTING.md` for the language-port protocol, "
        "and `NOTATION.md` for the study-book layer.\n"
    ]

    chapter_files = sorted(CH.glob("*.md"))
    total_words = 0
    for cf in chapter_files:
        cid = cf.stem
        md = cf.read_text(encoding="utf-8")
        part, domains = CHAPTER_META.get(cid, ("Unfiled", []))
        title = chapter_title(md)
        secs = split_sections(md)
        ch_rec = {"id": cid, "title": title, "part": part, "domains": domains,
                  "words": words(md), "sections": []}
        for sname, body in secs:
            e = {"chapter": cid, "section": sname, "tier": "bible",
                 "part": part, "languages": ["agnostic"], "domains": domains,
                 "text": body}
            entries.append(e)
            ch_rec["sections"].append({"name": sname, "words": words(body),
                                       "languages": ["agnostic"], "domains": domains})
        total_words += ch_rec["words"]
        parts_map.setdefault(part, []).append(ch_rec)
        md_chunks.append("\n\n---\n\n" + md.strip())

    # ports
    port_files = sorted((CH / "ports").glob("*.md"))
    for pf in port_files:
        md = pf.read_text(encoding="utf-8")
        m = re.search(r"canonical_section:\s*([\w.]+)\s*\|\s*language:\s*([\w+]+)", md)
        canon_id, lang = (m.group(1), m.group(2)) if m else (None, None)
        pid = f"port/{pf.stem}"
        title = chapter_title(md)
        secs = split_sections(md)
        rec = {"id": pid, "title": title, "port_of": canon_id, "language": lang,
               "words": words(md), "sections": []}
        for sname, body in secs:
            e = {"chapter": pid, "section": sname, "tier": "bible",
                 "part": "Ports", "languages": [lang], "domains": [],
                 "port_of": canon_id, "text": body}
            entries.append(e)
            rec["sections"].append({"name": sname, "words": words(body),
                                    "languages": [lang], "domains": [],
                                    "port_of": canon_id})
        total_words += rec["words"]
        index["ports"].append(rec)
        md_chunks.append("\n\n---\n\n" + md.strip())

    for part, chs in parts_map.items():
        index["parts"].append({"part": part, "chapters": chs})
    for canon_id, tgt in CANONICAL.items():
        ports = [p["id"] for p in index["ports"] if p["port_of"] == canon_id]
        index["canonical"][canon_id] = {**tgt, "ports": ports}
    index["total_words"] = total_words
    index["section_count"] = len(entries)

    (ROOT / "bible.md").write_text("\n".join(md_chunks) + "\n", encoding="utf-8")
    with open(ROOT / "bible.jsonl", "w", encoding="utf-8") as f:
        for e in entries:
            f.write(json.dumps(e, ensure_ascii=False) + "\n")
    with open(ROOT / "bible-index.json", "w", encoding="utf-8") as f:
        json.dump(index, f, indent=2, ensure_ascii=False)
    print(f"chapters={len(chapter_files)} ports={len(port_files)} "
          f"sections={len(entries)} total_words={total_words}")


if __name__ == "__main__":
    build()
