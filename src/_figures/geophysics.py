"""Geophysics figures — Cascadia paleoseismology.

One figure: a stick-event chronology of inferred Cascadia margin
earthquakes over the last ~10,000 years, derived from the Goldfinger
et al. (2012) USGS Professional Paper 1661-F turbidite-correlation
record.
"""

from __future__ import annotations

import csv
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

from ._io import save_figure
from ._style import PALETTE, add_wrapped_footer

_DATA_DIR = Path(__file__).resolve().parents[2] / "data"
_EVENTS_CSV = _DATA_DIR / "cascadia_paleoseismic_events.csv"
_STATS_CSV = _DATA_DIR / "cascadia_summary_stats.csv"


def _load_events(path: Path) -> list[tuple[str, int, str]]:
    with path.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    return [(row["label"], int(row["age_yr_bp"]), row["segment"]) for row in rows]


def _load_summary_stats(path: Path) -> str:
    with path.open(newline="", encoding="utf-8") as f:
        rows = sorted(csv.DictReader(f), key=lambda row: int(row["sort_order"]))
    lines = ["Goldfinger et al. (2012) summary statistics"]
    lines.extend(f"  - {row['label']}:  {row['value']}" for row in rows)
    return "\n".join(lines)


def plot_cascadia_paleoseismology(
    output_dir: Path,
    events_csv: Path | None = None,
    stats_csv: Path | None = None,
    **_: object,
) -> Path:
    """Stick-event chronology of inferred Cascadia margin earthquakes.

    Vertical sticks at each turbidite-derived event age, colored by
    inferred rupture segment. The two used segments — full-margin and
    southern — are placed on horizontal lanes for visual separation;
    labels are staggered across four offsets to minimize overlap on
    closely-spaced events.
    """
    events = _load_events(events_csv or _EVENTS_CSV)
    stats = _load_summary_stats(stats_csv or _STATS_CSV)

    fig, ax = plt.subplots(figsize=(16.8, 7.2))

    seg_colors = {
        "full": PALETTE["red"],
        "south": PALETTE["orange"],
    }
    seg_y = {"full": 1.0, "south": 0.55}

    # Lane background bands for visual separation.
    for label, y, color in [
        ("Full-margin rupture", seg_y["full"], PALETTE["red"]),
        ("Southern-segment rupture", seg_y["south"], PALETTE["orange"]),
    ]:
        ax.axhspan(y - 0.04, y + 0.04, color=color, alpha=0.05, zorder=1)
        ax.text(9450, y, label, fontsize=13, color=color, va="center", ha="right", style="italic")

    # Four-level label staggering to handle dense clusters.
    label_offsets = [0.07, 0.14, 0.21, 0.28]
    for i, (label, age, seg) in enumerate(events):
        if seg not in seg_y:
            continue
        y = seg_y[seg]
        color = seg_colors[seg]
        ax.plot([age, age], [0, y], color=color, linewidth=2.2, zorder=3)
        ax.scatter(age, y, s=80, color=color, edgecolor="black", linewidth=0.7, zorder=4)
        dy = label_offsets[i % len(label_offsets)]
        ax.text(age, y + dy, label, ha="center", fontsize=11.3, fontweight="semibold", color=color)

    # Highlight T1 (AD 1700) as "the ancestor"
    ax.annotate(
        "T1 — 26 January 1700\nMw 8.7–9.2 (orphan-tsunami\nrecord; Atwater 2005)",
        xy=(320, 1.0),
        xytext=(1700, 1.45),
        fontsize=13,
        fontweight="semibold",
        color=PALETTE["red"],
        bbox=dict(facecolor="white", edgecolor=PALETTE["red"], boxstyle="round,pad=0.35", alpha=0.95),
        arrowprops=dict(arrowstyle="->", color=PALETTE["red"], lw=1.5),
        zorder=6,
    )

    # Recurrence statistics box: model summaries, not deterministic forecasts.
    ax.text(
        0.985,
        0.02,
        stats,
        transform=ax.transAxes,
        ha="right",
        va="bottom",
        fontsize=12,
        color=PALETTE["dark"],
        bbox=dict(facecolor="white", edgecolor=PALETTE["dark"], boxstyle="round,pad=0.45", alpha=0.95),
    )

    ax.set_xlim(-200, 9500)
    ax.set_ylim(0, 1.85)
    ax.invert_xaxis()  # past on the right, present on the left
    ax.set_xlabel("Years before present (BP)")
    ax.set_yticks([])
    ax.set_title("Cascadia Subduction Zone: 10,000-Year Paleoseismic Record")

    legend_elements = [
        Line2D([0], [0], color=PALETTE["red"], linewidth=4, label="Full-margin rupture (Mw >= 8.7)"),
        Line2D([0], [0], color=PALETTE["orange"], linewidth=4, label="Southern-segment rupture (Mw 8.0–8.7)"),
    ]
    ax.legend(handles=legend_elements, loc="upper right")

    ax.text(
        0.005,
        0.92,
        "PRESENT →",
        transform=ax.transAxes,
        fontsize=12,
        fontweight="semibold",
        color=PALETTE["dark"],
        style="italic",
    )
    ax.text(
        0.985,
        0.92,
        "← DEEP PAST",
        transform=ax.transAxes,
        ha="right",
        fontsize=12,
        fontweight="semibold",
        color=PALETTE["dark"],
        style="italic",
    )

    ax.grid(True, axis="x", alpha=0.25)
    add_wrapped_footer(
        fig,
        "Data: data/cascadia_paleoseismic_events.csv and "
        "data/cascadia_summary_stats.csv. Event ages are approximate "
        "turbidite-correlation medians rounded for display; probabilities "
        "are model outputs.",
        y=0.018,
        width=132,
        fontsize=10.5,
    )
    fig.tight_layout(rect=(0, 0.06, 1, 1))
    return save_figure(fig, "cascadia_paleoseismology", output_dir)
