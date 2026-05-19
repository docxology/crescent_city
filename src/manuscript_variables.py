"""Compute manuscript-level substitution variables for crescent_city.

``scripts/z_generate_manuscript_variables.py`` calls
:func:`compute_variables` and writes the resolved copies to
``output/manuscript/`` via :func:`write_variables`.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

from infrastructure.prose import ManuscriptReport


@dataclass
class ManuscriptVariables:
    """All ``{{TOKEN}}`` values that can be injected into the manuscript."""

    config_title: str = ""
    total_words: int = 0
    total_sentences: int = 0
    total_paragraphs: int = 0
    avg_grade_level: float = 0.0
    avg_reading_ease: float = 0.0
    avg_gunning_fog: float = 0.0
    citation_count: int = 0
    files_analyzed: int = 0
    longest_section_words: int = 0
    shortest_section_words: int = 0

    def to_dict(self) -> dict[str, object]:
        return {
            "CONFIG_TITLE": self.config_title,
            "TOTAL_WORDS": self.total_words,
            "TOTAL_SENTENCES": self.total_sentences,
            "TOTAL_PARAGRAPHS": self.total_paragraphs,
            "AVG_GRADE_LEVEL": round(self.avg_grade_level, 2),
            "AVG_READING_EASE": round(self.avg_reading_ease, 2),
            "AVG_GUNNING_FOG": round(self.avg_gunning_fog, 2),
            "CITATION_COUNT": self.citation_count,
            "FILES_ANALYZED": self.files_analyzed,
            "LONGEST_SECTION_WORDS": self.longest_section_words,
            "SHORTEST_SECTION_WORDS": self.shortest_section_words,
        }


def compute_variables(report: ManuscriptReport, config_title: str = "") -> ManuscriptVariables:
    """Derive every substitution token from a :class:`ManuscriptReport`."""
    word_counts = [f.metrics.word_count for f in report.files]
    longest = max(word_counts, default=0)
    shortest = min(word_counts, default=0)

    return ManuscriptVariables(
        config_title=config_title,
        total_words=report.total_words,
        total_sentences=report.total_sentences,
        total_paragraphs=report.total_paragraphs,
        avg_grade_level=report.avg_flesch_kincaid_grade,
        avg_reading_ease=report.avg_flesch_reading_ease,
        avg_gunning_fog=report.avg_gunning_fog,
        citation_count=len(report.citation_keys),
        files_analyzed=len(report.files),
        longest_section_words=longest,
        shortest_section_words=shortest,
    )


_TOKEN_RE = re.compile(r"\{\{([A-Z_]+)\}\}")


def substitute_in_text(text: str, variables: ManuscriptVariables) -> str:
    """Replace every ``{{TOKEN}}`` in *text* with its computed value."""
    lookup = variables.to_dict()

    def _replacer(m: re.Match[str]) -> str:
        key = m.group(1)
        val = lookup.get(key)
        if val is None:
            # Leave unknown tokens untouched so typos are visible.
            return str(m.group(0))
        return str(val)

    return _TOKEN_RE.sub(_replacer, text)


def write_variables(
    variables: ManuscriptVariables,
    manuscript_dir: Path | str,
    output_dir: Path | str,
) -> list[Path]:
    """Write substituted copies of every ``.md`` in *manuscript_dir*
    into *output_dir/manuscript/*, and refresh renderer support files.

    Returns the list of output file paths.
    """
    manuscript_path = Path(manuscript_dir)
    out_path = Path(output_dir) / "manuscript"
    out_path.mkdir(parents=True, exist_ok=True)

    skip = {"SYNTAX.md", "AGENTS.md", "README.md", "config.yaml", "preamble.md"}
    written: list[Path] = []
    expected_names = {src.name for src in manuscript_path.glob("*.md") if src.name not in skip}

    for stale in out_path.glob("*.md"):
        if stale.name not in expected_names:
            stale.unlink()

    for src in sorted(manuscript_path.glob("*.md")):
        if src.name in skip:
            continue
        content = src.read_text(encoding="utf-8")
        resolved = substitute_in_text(content, variables)
        dst = out_path / src.name
        dst.write_text(resolved, encoding="utf-8")
        written.append(dst)

    for support_name in ("references.bib", "config.yaml", "preamble.md"):
        src = manuscript_path / support_name
        if src.exists():
            (out_path / support_name).write_bytes(src.read_bytes())

    return written
