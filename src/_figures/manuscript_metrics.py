"""Per-section manuscript-metrics figures.

Three figures — section word counts, readability metrics, and citation
density — that operate over the manuscript directory rather than the
project's CSV data files. They make the manuscript reflect on itself:
the same pipeline that builds the PDF also documents the prose's
quantitative properties.
"""

from __future__ import annotations

import re
import textwrap
from dataclasses import dataclass
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np

from ._io import save_figure
from ._style import PALETTE, add_wrapped_footer

_EXCLUDED_MANUSCRIPT_FILES = {
    "99_references.md",
    "AGENTS.md",
    "README.md",
    "SYNTAX.md",
    "preamble.md",
}


@dataclass(frozen=True)
class _SectionRecord:
    """Small display record for a manuscript source section."""

    path: Path
    title: str
    short_label: str
    part: str


def _section_labels(manuscript_dir: Path) -> list[Path]:
    """Return manuscript markdown files in canonical order.

    Support and folder-documentation files are intentionally omitted: the
    metric figures should describe the manuscript readers encounter, not
    renderer preamble, syntax notes, or local agent/readme guidance that
    happen to live in the same directory.
    """
    return [
        p
        for p in sorted(manuscript_dir.glob("*.md"))
        if p.name not in _EXCLUDED_MANUSCRIPT_FILES and not p.name.startswith("99_")
    ]


def _section_title(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    for line in text.splitlines():
        if line.startswith("#"):
            title = line.lstrip("#").strip()
            title = re.sub(r"\s*\{#[^}]+\}\s*$", "", title)
            return title or path.stem
    return path.stem.replace("_", " ").title()


def _part_label(path: Path, title: str, current: str) -> str:
    if path.name.startswith("A"):
        return "Appendix"
    if title.startswith("Part "):
        if "—" in title:
            after_dash = title.split("—", 1)[1].strip()
            return after_dash.split(":", 1)[0].strip()
        return title.split(":", 1)[0].strip()
    return current


def _section_records(manuscript_dir: Path) -> list[_SectionRecord]:
    records: list[_SectionRecord] = []
    current_part = "Front"
    for path in _section_labels(manuscript_dir):
        title = _section_title(path)
        part = _part_label(path, title, current_part)
        if part != "Appendix":
            current_part = part
        stem = path.stem
        prefix = stem.split("_", 1)[0]
        if prefix.isdigit():
            label = f"{int(prefix):02d}. {textwrap.shorten(title, width=31, placeholder='...')}"
        else:
            label = f"{prefix}. {textwrap.shorten(title, width=31, placeholder='...')}"
        records.append(_SectionRecord(path=path, title=title, short_label=label, part=part))
    return records


def _part_spans(records: list[_SectionRecord]) -> list[tuple[str, int, int]]:
    spans: list[tuple[str, int, int]] = []
    if not records:
        return spans
    start = 0
    current = records[0].part
    for idx, rec in enumerate(records[1:], start=1):
        if rec.part != current:
            spans.append((current, start, idx - 1))
            current = rec.part
            start = idx
    spans.append((current, start, len(records) - 1))
    return spans


def _shade_part_spans(ax, records: list[_SectionRecord]) -> None:
    for idx, (_part, start, end) in enumerate(_part_spans(records)):
        if idx % 2:
            ax.axvspan(start - 0.5, end + 0.5, color=PALETTE["light"], alpha=0.24, zorder=0)


def _shade_part_spans_horizontal(ax, records: list[_SectionRecord]) -> None:
    for idx, (_part, start, end) in enumerate(_part_spans(records)):
        if idx % 2:
            ax.axhspan(start - 0.5, end + 0.5, color=PALETTE["light"], alpha=0.24, zorder=0)


def _label_part_spans_horizontal(ax, records: list[_SectionRecord], max_count: int) -> None:
    for part, start, end in _part_spans(records):
        if part == "Front":
            continue
        ax.text(
            max_count * 0.985,
            (start + end) / 2,
            textwrap.shorten(part, width=24, placeholder="..."),
            ha="right",
            va="center",
            fontsize=9.6,
            fontweight="semibold",
            color="#555555",
            bbox=dict(facecolor="white", edgecolor="#dddddd", alpha=0.82, boxstyle="round,pad=0.18"),
            zorder=4,
        )


def _set_part_xticks(ax, records: list[_SectionRecord]) -> None:
    spans = _part_spans(records)
    centers = [(start + end) / 2 for _part, start, end in spans]
    labels = [part.replace("Part ", "") for part, _start, _end in spans]
    ax.set_xticks(centers)
    ax.set_xticklabels(labels, fontsize=12, fontweight="semibold")


def _add_metric_footer(fig, text: str) -> None:
    """Place a consistent source and limitation note below manuscript-metric plots."""
    add_wrapped_footer(fig, text, y=0.018, width=140, fontsize=10.3)


def _part_panel_axes() -> tuple[plt.Figure, np.ndarray]:
    """Return a compact two-column grid for part-grouped metric figures."""
    fig, axes = plt.subplots(
        3,
        2,
        figsize=(17.5, 13.8),
        sharex=True,
        gridspec_kw={"hspace": 0.34, "wspace": 0.46},
    )
    return fig, axes.ravel()


def _count_syllables(word: str) -> int:
    """Approximate English syllable count for fallback readability metrics."""
    cleaned = re.sub(r"[^a-z]", "", word.lower())
    if not cleaned:
        return 0
    groups = re.findall(r"[aeiouy]+", cleaned)
    count = len(groups)
    if cleaned.endswith("e") and count > 1 and not cleaned.endswith(("le", "ye")):
        count -= 1
    return max(count, 1)


def _fallback_readability(text: str) -> tuple[float, float]:
    """Return ``(FRE, FKGL)`` when ``textstat`` is unavailable.

    The formulas match the Flesch Reading Ease and Flesch-Kincaid Grade
    Level definitions; syllables are estimated with a deterministic vowel
    group heuristic. This keeps figure generation offline and robust in
    lean test environments while preserving the same metric semantics.
    """
    words = re.findall(r"[A-Za-z]+(?:['-][A-Za-z]+)?", text)
    sentences = [s for s in re.split(r"[.!?]+", text) if s.strip()]
    word_count = max(len(words), 1)
    sentence_count = max(len(sentences), 1)
    syllables = max(sum(_count_syllables(word) for word in words), 1)
    words_per_sentence = word_count / sentence_count
    syllables_per_word = syllables / word_count
    fre = 206.835 - (1.015 * words_per_sentence) - (84.6 * syllables_per_word)
    fkgl = (0.39 * words_per_sentence) + (11.8 * syllables_per_word) - 15.59
    return fre, fkgl


def _readability_scores(text: str) -> tuple[float, float]:
    """Return Flesch Reading Ease and Flesch-Kincaid Grade Level."""
    try:
        from textstat import flesch_kincaid_grade, flesch_reading_ease
    except ModuleNotFoundError:
        return _fallback_readability(text)
    return flesch_reading_ease(text), flesch_kincaid_grade(text)


def plot_section_word_counts(manuscript_dir: Path, output_dir: Path) -> Path:
    """Bar chart of word count per manuscript section.

    Bars above the section-mean line are recolored green to highlight the
    sections that carry a disproportionate share of the narrative.
    """
    records = _section_records(manuscript_dir)
    counts = [len(r.path.read_text(encoding="utf-8").split()) for r in records]
    mean_count = float(np.mean(counts))
    max_count = max(counts)

    spans = _part_spans(records)
    fig, axes = _part_panel_axes()

    for ax, (part, start, end) in zip(axes, spans):
        subset = records[start : end + 1]
        subset_counts = counts[start : end + 1]
        y = np.arange(len(subset))
        colors = [PALETTE["green"] if count > mean_count else PALETTE["blue"] for count in subset_counts]
        bars = ax.barh(y, subset_counts, color=colors, edgecolor="white", linewidth=0.7)
        ax.set_yticks(y)
        ax.set_yticklabels(
            [textwrap.shorten(r.short_label, width=34, placeholder="...") for r in subset],
            fontsize=8.8,
        )
        ax.axvline(mean_count, color=PALETTE["red"], linestyle="--", linewidth=1.25, alpha=0.82)
        ax.set_xlim(0, max_count * 1.13)
        ax.invert_yaxis()
        ax.grid(True, axis="x", alpha=0.24)
        ax.grid(False, axis="y")
        ax.set_title(part, loc="left", fontsize=12.4, fontweight="bold", color=PALETTE["dark"], pad=4)
        for bar, count in zip(bars, subset_counts):
            ax.text(
                bar.get_width() + max_count * 0.012,
                bar.get_y() + bar.get_height() / 2,
                f"{count:,}",
                va="center",
                fontsize=8.1,
                color=PALETTE["dark"],
            )

    for ax in axes[len(spans) :]:
        ax.set_visible(False)
    for ax in axes[: len(spans)]:
        ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f"{int(x):,}"))
    fig.supxlabel("Word Count", fontsize=14, fontweight="bold", y=0.052)
    fig.suptitle("Crescent City History: Section Word Counts by Part", fontsize=18.5, fontweight="bold", y=0.975)
    axes[0].plot([], [], color=PALETTE["red"], linestyle="--", linewidth=1.25, label=f"Mean ({mean_count:.0f})")
    axes[0].legend(fontsize=9.6, loc="upper right")
    _add_metric_footer(
        fig,
        "Source basis: manuscript/*.md source sections only; folder README/AGENTS/SYNTAX/preamble files and references are excluded. "
        "Counts are computational reading aids, not measures of historical importance.",
    )

    fig.subplots_adjust(left=0.16, right=0.965, bottom=0.095, top=0.93)
    return save_figure(fig, "section_word_counts", output_dir)


def plot_readability_metrics(manuscript_dir: Path, output_dir: Path) -> Path:
    """Dual-axis plot of Flesch Reading Ease (bars) and Flesch-Kincaid Grade
    Level (line) per section.

    The metrics interpret the prose's accessibility under the standard
    Flesch-Kincaid framework. When :mod:`textstat` is unavailable, the
    plotter uses a deterministic local implementation of the same formulas.
    """
    records = _section_records(manuscript_dir)
    fre: list[float] = []
    fkgl: list[float] = []
    for rec in records:
        text = rec.path.read_text(encoding="utf-8")
        reading_ease, grade_level = _readability_scores(text)
        fre.append(reading_ease)
        fkgl.append(grade_level)

    fig, (ax1, ax2) = plt.subplots(
        2,
        1,
        figsize=(17.5, 9.4),
        sharex=True,
        gridspec_kw={"height_ratios": [1.05, 0.95], "hspace": 0.08},
    )
    x = np.arange(len(records))
    _shade_part_spans(ax1, records)
    _shade_part_spans(ax2, records)
    ax1.bar(x, fre, color=PALETTE["cyan"], alpha=0.75, label="Flesch Reading Ease", edgecolor="white", linewidth=0.6)
    ax1.set_ylabel("Reading Ease", fontsize=14, fontweight="bold", color=PALETTE["blue"])
    ax1.tick_params(axis="y", labelcolor=PALETTE["blue"], labelsize=12)
    ax1.set_ylim(0, 80)
    ax1.axhspan(0, 30, color=PALETTE["red"], alpha=0.05, zorder=0)
    ax1.set_xlim(-0.5, len(records) - 0.5)
    ax1.grid(True, axis="y", alpha=0.25)

    ax2.plot(
        x, fkgl, color=PALETTE["red"], marker="o", linewidth=2.4, markersize=5.5, label="Flesch-Kincaid Grade Level"
    )
    ax2.set_ylabel("Grade Level", fontsize=14, fontweight="bold", color=PALETTE["red"])
    ax2.tick_params(axis="y", labelcolor=PALETTE["red"], labelsize=12)
    ax2.set_ylim(8, 22)
    ax2.axhspan(12, 20, color=PALETTE["green"], alpha=0.06, zorder=0)
    ax2.grid(True, axis="y", alpha=0.25)
    _set_part_xticks(ax2, records)
    ax2.set_xlabel("Manuscript Part", fontsize=14, fontweight="bold")

    fig.suptitle("Crescent City History: Readability by Manuscript Part", fontsize=19, fontweight="bold", y=0.975)
    _add_metric_footer(
        fig,
        "Source basis: manuscript source sections only. Flesch-Kincaid formulas are mechanical readability indicators; "
        "they do not judge historical rigor, citation quality, or cultural specificity.",
    )
    lines1, lbl1 = ax1.get_legend_handles_labels()
    lines2, lbl2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, lbl1 + lbl2, loc="upper right", fontsize=11.2)

    fig.subplots_adjust(left=0.065, right=0.965, bottom=0.155, top=0.92)
    return save_figure(fig, "readability_metrics", output_dir)


def plot_citation_density(manuscript_dir: Path, output_dir: Path) -> Path:
    """Citations per 1,000 words by section, with the configured floor at 3.

    A rough proxy: counts ``[@`` tokens, which catches Pandoc-style citations
    but undercounts semicolon-separated multi-citation groups (each counted
    once per opening bracket). Good enough for trend visualization.
    """
    records = _section_records(manuscript_dir)
    densities: list[float] = []
    for rec in records:
        text = rec.path.read_text(encoding="utf-8")
        if text.startswith("[comment]:"):
            continue
        words = max(len(text.split()), 1)
        cites = max(text.count("[@"), 0)
        density = (cites / words) * 1000
        densities.append(density)

    spans = _part_spans(records)
    max_density = max(densities)
    fig, axes = _part_panel_axes()

    for ax, (part, start, end) in zip(axes, spans):
        subset = records[start : end + 1]
        subset_densities = densities[start : end + 1]
        y = np.arange(len(subset))
        colors = [PALETTE["green"] if value >= 3 else PALETTE["red"] for value in subset_densities]
        ax.barh(y, subset_densities, color=colors, alpha=0.78, edgecolor="white", linewidth=0.7)
        ax.axvline(3, color=PALETTE["red"], linestyle="--", linewidth=1.2, alpha=0.82)
        ax.set_xlim(0, max_density * 1.18)
        ax.set_yticks(y)
        ax.set_yticklabels(
            [textwrap.shorten(r.short_label, width=34, placeholder="...") for r in subset],
            fontsize=8.8,
        )
        ax.invert_yaxis()
        ax.grid(True, axis="x", alpha=0.24)
        ax.grid(False, axis="y")
        ax.set_title(part, loc="left", fontsize=12.4, fontweight="bold", color=PALETTE["dark"], pad=4)
        for yy, value in zip(y, subset_densities):
            ax.text(
                value + max_density * 0.012,
                yy,
                f"{value:.1f}",
                va="center",
                fontsize=8.1,
                color=PALETTE["dark"],
            )

    for ax in axes[len(spans) :]:
        ax.set_visible(False)
    for ax in axes[: len(spans)]:
        ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f"{x:.1f}"))
    fig.supxlabel("Citations / 1,000 Words", fontsize=14, fontweight="bold", y=0.052)
    fig.suptitle("Crescent City History: Citation Density by Source Section", fontsize=18.5, fontweight="bold", y=0.975)
    axes[0].plot([], [], color=PALETTE["red"], linestyle="--", linewidth=1.2, label="Floor: 3 / 1k")

    axes[0].legend(fontsize=9.6, loc="upper left")
    _add_metric_footer(
        fig,
        "Source basis: Pandoc-style citation tokens in manuscript source sections. Multi-source citation clusters are counted by bracket, "
        "so the plot is a conservative density check rather than a bibliography audit.",
    )

    fig.subplots_adjust(left=0.16, right=0.965, bottom=0.095, top=0.93)
    return save_figure(fig, "citation_density", output_dir)
