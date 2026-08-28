#!/usr/bin/env python3
"""Bidirectional glossary coverage audit.

Direction 1 (glossary -> prose): every `**term** —` entry in
`manuscript/A2_glossary.md` must appear somewhere in the manuscript prose
(case-insensitive, hyphen/space-normalized, parenthetical expansions and
slash-separated alternates allowed).

Direction 2 (prose -> glossary) is enforced separately by
`tests/test_glossary.py` (acronym coverage). This script checks direction 1
exits nonzero with a diagnostic list when a glossary term is orphaned.

Usage: uv run python scripts/audit/check_glossary_usage.py
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
MANUSCRIPT_DIR = PROJECT_ROOT / "manuscript"
GLOSSARY = MANUSCRIPT_DIR / "A2_glossary.md"

# Files whose content is meta-documentation rather than prose about the place.
EXCLUDED = {
    "A2_glossary.md",
    "99_references.md",
    "SYNTAX.md",
    "README.md",
    "AGENTS.md",
}


def _normalize(text: str) -> str:
    lowered = text.lower()
    lowered = lowered.replace("-", " ").replace("'", "")
    return re.sub(r"\s+", " ", lowered)


def _headterm_variants(term: str) -> list[str]:
    """Headterm -> acceptable prose surface forms.

    Strips a trailing parenthetical expansion, splits slash alternates, and
    normalizes hyphens/apostrophes/case so 'Double-Cross flag' matches prose
    'Double Cross flag' and back.
    """
    base = re.sub(r"\s*\([^)]*\)\s*$", "", term).strip()
    out: list[str] = []
    for part in re.split(r"\s*/\s*", base):
        part = part.strip()
        if part:
            out.append(_normalize(part))
    return out


def main() -> int:
    if not GLOSSARY.exists():
        print(f"FAIL: {GLOSSARY} missing", file=sys.stderr)
        return 2
    glossary_text = GLOSSARY.read_text(encoding="utf-8")
    terms = re.findall(r"^\*\*(.+?)\*\*\s+—", glossary_text, re.M)
    if not terms:
        print("FAIL: no glossary entries parsed", file=sys.stderr)
        return 2

    prose_files = [
        p
        for p in sorted(MANUSCRIPT_DIR.glob("*.md"))
        if p.name not in EXCLUDED
    ]
    prose = "\n".join(p.read_text(encoding="utf-8") for p in prose_files)
    prose_norm = _normalize(prose)

    orphaned: list[str] = []
    for term in terms:
        variants = _headterm_variants(term)
        if variants and not any(v in prose_norm for v in variants):
            orphaned.append(term)

    if orphaned:
        print("FAIL: glossary terms not used in manuscript prose:")
        for t in orphaned:
            print(f"  - {t}")
        return 1
    print(f"OK: all {len(terms)} glossary terms are used in the manuscript prose")
    return 0


if __name__ == "__main__":
    sys.exit(main())
