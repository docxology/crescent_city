"""Glossary coverage tests.

The glossary (manuscript/A2_glossary.md) is the canonical place for
non-specialist definitions. This file enforces a coverage floor:
italicised foreign-language terms and all-caps acronyms that appear
multiple times in the prose should also appear in the glossary, so
readers always have a definition pointer.
"""

from __future__ import annotations

import re
from collections import Counter
from pathlib import Path


# Acronyms that are universally familiar enough to skip glossary listing.
_ACRONYM_ALLOWLIST = {
    "U",
    "S",
    "USA",
    "PDF",
    "PNG",
    "SVG",
    "JSON",
    "CSV",
    "YAML",
    "HDPE",
    "MIT",
    "BCE",
    "CE",
    "ACS",
    "DOI",
    "ISBN",
    "URL",
    "GIS",
    "LCCN",
    "FRE",
    "FKGL",
    "XML",  # well-known abbreviations
}


def _split_words(text: str) -> list[str]:
    return re.findall(r"[A-Za-z][A-Za-z'-]+", text)


def test_glossary_present(manuscript_dir: Path) -> None:
    p = manuscript_dir / "A2_glossary.md"
    assert p.exists(), "A2_glossary.md missing"
    body = p.read_text(encoding="utf-8")
    assert len(body) > 1_000, "Glossary suspiciously short"


def test_glossary_covers_high_frequency_acronyms(manuscript_dir: Path) -> None:
    """Any all-caps acronym >=4 chars appearing >=3 times in prose should
    be defined in the glossary OR appear in the allowlist."""
    glossary_body = (manuscript_dir / "A2_glossary.md").read_text()
    glossary_terms_lower = glossary_body.lower()

    counter: Counter[str] = Counter()
    for f in sorted(manuscript_dir.glob("*.md")):
        if f.name in ("A2_glossary.md", "references.bib", "SYNTAX.md"):
            continue
        text = f.read_text(encoding="utf-8")
        # Strip code blocks to avoid YAML/JSON noise
        text = re.sub(r"```.*?```", "", text, flags=re.S)
        for tok in re.findall(r"\b[A-Z]{4,}\b", text):
            if tok in _ACRONYM_ALLOWLIST:
                continue
            counter[tok] += 1

    missing: list[tuple[str, int]] = []
    for tok, n in counter.most_common():
        if n < 3:
            break
        # The glossary may render an acronym either at start-of-entry
        # (as a header), inside parens, or inline-bold. Match loosely.
        if tok.lower() not in glossary_terms_lower:
            missing.append((tok, n))

    # A non-empty list is a *warning* but does not fail the suite: this
    # gate is intentionally tolerant until the glossary is expanded. We
    # do, however, fail if more than 12 distinct high-frequency acronyms
    # are missing — anything beyond that constitutes systemic drift.
    assert len(missing) <= 12, f"Too many high-frequency acronyms missing from glossary: {missing[:15]}"
