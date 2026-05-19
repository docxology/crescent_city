"""Assemble the final review report (Markdown) for crescent_city."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable

from infrastructure.prose.report import ManuscriptReport

from .checks import CheckResult


def write_review_report(
    output_path: Path | str,
    *,
    title: str,
    manuscript_report: ManuscriptReport,
    checks: Iterable[CheckResult],
    include_per_file_table: bool = True,
    include_outline: bool = True,
    include_quality_flags: bool = True,
    figures: list[Path] | None = None,
) -> Path:
    """Write a markdown review report and return its path."""
    from infrastructure.prose import render_outline

    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    checks = list(checks)
    all_passed = all(c.passed for c in checks)

    lines: list[str] = []
    lines.append(f"# {title}")
    lines.append("")
    lines.append(
        f"_Files:_ **{len(manuscript_report.files)}** · "
        f"_words:_ **{manuscript_report.total_words}** · "
        f"_sentences:_ **{manuscript_report.total_sentences}** · "
        f"_paragraphs:_ **{manuscript_report.total_paragraphs}**"
    )
    lines.append("")
    lines.append(
        f"_Avg FRE:_ {manuscript_report.avg_flesch_reading_ease} · "
        f"_avg FKGL:_ {manuscript_report.avg_flesch_kincaid_grade} · "
        f"_unique citation keys:_ {len(manuscript_report.citation_keys)}"
    )
    lines.append("")

    lines.append(f"## Checks {'✅' if all_passed else '⚠️'}")
    lines.append("")
    lines.append("| Check | Result | Detail |")
    lines.append("|---|---|---|")
    for c in checks:
        emoji = "✅" if c.passed else "❌"
        lines.append(f"| `{c.name}` | {emoji} | {c.message} |")
    lines.append("")

    if include_per_file_table and manuscript_report.files:
        lines.append("## Per-file metrics")
        lines.append("")
        lines.append("| File | Words | Sentences | FRE | FKGL | Fog | Citations |")
        lines.append("|---|---:|---:|---:|---:|---:|---:|")
        for f in manuscript_report.files:
            m = f.metrics
            lines.append(
                f"| `{f.name}` | {m.word_count} | {m.sentence_count} | "
                f"{m.flesch_reading_ease} | {m.flesch_kincaid_grade} | "
                f"{m.gunning_fog} | {len(f.quality.citation_keys)} |"
            )
        lines.append("")

    if include_outline and manuscript_report.files:
        lines.append("## Outline")
        lines.append("")
        for f in manuscript_report.files:
            lines.append(f"### `{f.name}`")
            lines.append("")
            outline_text = render_outline(f.structure)
            if outline_text:
                lines.append(outline_text)
            else:
                lines.append("_(no headings)_")
            lines.append("")

    if include_quality_flags:
        flagged = []
        for f in manuscript_report.files:
            q = f.quality
            if (q.long_sentence_count or q.passive_count or q.hedge_count) and q.word_count:
                flagged.append((f.name, q))
        if flagged:
            lines.append("## Quality flags")
            lines.append("")
            for name, q in flagged:
                lines.append(f"### `{name}`")
                lines.append("")
                if q.long_sentence_count:
                    lines.append(f"- {q.long_sentence_count} long sentence(s)")
                if q.passive_count:
                    lines.append(f"- {q.passive_count} potential passive-voice sentence(s)")
                if q.hedge_count:
                    lines.append(f"- {q.hedge_count} hedge word(s): " + ", ".join(sorted(set(q.hedge_words))[:10]))
                lines.append("")

    if figures:
        lines.append("## Figures")
        lines.append("")
        for fig_path in figures:
            lines.append(f"- `{fig_path.name}`")
        lines.append("")

    out.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    return out
