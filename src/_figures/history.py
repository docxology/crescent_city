"""Historical-timeline Gantt-style figure.

Single figure that scatters every dated event in
``data/historical_events.json`` against a thematic category axis.
"""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.lines import Line2D

from ._io import save_figure
from ._style import PALETTE, add_wrapped_footer

_DATA_DIR = Path(__file__).resolve().parents[2] / "data"


def plot_historical_timeline(output_dir: Path, json_path: Path | None = None) -> Path:
    """Two-century scatter of categorized events from `historical_events.json`."""
    json_file = json_path or _DATA_DIR / "historical_events.json"
    with open(json_file, encoding="utf-8") as f:
        events = json.load(f)
    timed = [e for e in events if e["year"] not in ("c.1000BCE",)]

    preferred_order = [
        "Indigenous",
        "Exploration",
        "Settlement",
        "Conflict",
        "Governance",
        "Military",
        "Industry",
        "Economy",
        "Infrastructure",
        "Demographics",
        "Environment",
        "Conservation",
        "Policy",
        "Science",
        "Social",
        "Culture",
        "Geological",
        "Disaster",
    ]
    present = {e["category"] for e in timed}
    categories = [c for c in preferred_order if c in present] + sorted(present - set(preferred_order))
    cat_to_y = {c: i for i, c in enumerate(categories)}

    fig, ax = plt.subplots(figsize=(18.5, 10.4))
    cat_colors = {
        "Disaster": PALETTE["red"],
        "Economy": PALETTE["orange"],
        "Environment": PALETTE["green"],
        "Exploration": PALETTE["blue"],
        "Governance": PALETTE["purple"],
        "Indigenous": PALETTE["brown"],
        "Infrastructure": PALETTE["cyan"],
        "Military": PALETTE["yellow"],
        "Policy": "#808080",
        "Science": "#6A5ACD",
        "Social": "#FF69B4",
        "Culture": "#DAA520",
        "Demographics": "#4682B4",
        "Industry": "#CD853F",
    }

    focus_windows = [
        (1850, 1862, "Contact / conquest"),
        (1964, 1978, "Tsunami / parks"),
        (2020, 2026, "Current cluster"),
    ]
    for start, end, label in focus_windows:
        ax.axvspan(start, end, color=PALETTE["light"], alpha=0.28, zorder=0)
        ax.text(
            (start + end) / 2,
            1.01,
            label,
            transform=ax.get_xaxis_transform(),
            ha="center",
            va="bottom",
            fontsize=9.5,
            fontweight="semibold",
            color="#555555",
        )

    for e in timed:
        try:
            year = int(e["year"])
        except (ValueError, TypeError):
            continue
        y = cat_to_y[e["category"]]
        color = cat_colors.get(e["category"], PALETTE["dark"])
        marker = "X" if e["category"] == "Disaster" else "o"
        size = 220 if e["category"] == "Disaster" else 110
        if "tsunami" in e.get("tags", []) or "earthquake" in e.get("tags", []):
            size = 280
        ax.scatter(year, y, s=size, c=color, marker=marker, zorder=3, edgecolors="black", linewidth=0.8)

    ax.set_yticks(range(len(categories)))
    ax.set_yticklabels(categories, fontsize=12.5, fontweight="bold")
    ax.set_xlabel("Year", fontsize=16, fontweight="bold")
    ax.set_title("Crescent City Historical Timeline — Events by Category", fontsize=20, fontweight="bold")
    ax.xaxis.set_major_locator(ticker.MultipleLocator(25))
    ax.xaxis.set_major_formatter(ticker.FormatStrFormatter("%d"))
    ax.set_xlim(1800, 2030)
    ax.set_ylim(-0.7, len(categories) - 0.25)
    ax.grid(True, axis="x", alpha=0.3)

    legend_elements = [
        Line2D(
            [0],
            [0],
            marker="o",
            color="w",
            markerfacecolor=cat_colors.get(c, PALETTE.get("gray", "#777777")),
            markersize=12,
            label=c,
        )
        for c in categories
        if c in cat_colors
    ]
    ax.legend(
        handles=legend_elements,
        loc="upper center",
        bbox_to_anchor=(0.5, -0.085),
        ncol=6,
        fontsize=10.8,
        framealpha=0.95,
        title="Category",
        title_fontsize=12,
    )
    add_wrapped_footer(
        fig,
        "Source basis: data/historical_events.json, a curated event ledger keyed to manuscript citations. "
        "The plot encodes category and approximate event year, not magnitude, completeness, or legal status; "
        "modern clusters mark areas needing periodic re-audit.",
        y=0.024,
        width=150,
        fontsize=10.6,
    )

    fig.subplots_adjust(left=0.125, right=0.985, bottom=0.255, top=0.89)
    return save_figure(fig, "historical_timeline", output_dir)
