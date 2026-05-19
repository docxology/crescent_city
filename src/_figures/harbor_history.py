"""Harbor-history figure — Crescent City harbor reconstruction timeline.

One figure: a chronological band-chart of the harbor's engineering
history from the 1856 Battery Point Lighthouse through the 2014
tsunami-resistant Inner Boat Basin and the 2022 PIDP grant. The
figure makes visible the cyclical reconstruction pattern that the
prose argues is the defining feature of the working waterfront.
"""

from __future__ import annotations

import csv
import textwrap
from pathlib import Path

import matplotlib.pyplot as plt

from ._io import save_figure
from ._style import PALETTE, add_wrapped_footer

_DATA_DIR = Path(__file__).resolve().parents[2] / "data"
_EVENTS_CSV = _DATA_DIR / "harbor_timeline_events.csv"

_CATEGORIES = [
    ("disaster", "Disaster"),
    ("breakwater", "Breakwater / seawall"),
    ("dock", "Dock / basin"),
    ("rail/wharf", "Rail / wharf"),
    ("navigation", "Navigation aid"),
    ("governance", "Governance"),
    ("ecological", "Ecological"),
]
_CAT_Y = {c[0]: i for i, c in enumerate(_CATEGORIES)}

_LABEL_OFFSETS = {
    1856: (0, 20),
    1903: (0, -30),
    1911: (-10, 24),
    1931: (0, -30),
    1964: (-24, 32),
    1965: (36, -34),
    1974: (0, 24),
    1980: (0, -34),
    2011: (-20, 34),
    2014: (36, -34),
    2022: (-14, 24),
    2024: (28, -34),
}


def _load_events(path: Path) -> list[tuple[int, str, str, str]]:
    with path.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    return [
        (int(row["year"]), row["label"], row["category"], row["color_key"])
        for row in sorted(rows, key=lambda r: int(r["year"]))
    ]


def plot_harbor_timeline(output_dir: Path, events_csv: Path | None = None, **_: object) -> Path:
    """Chronological scatter of harbor-engineering and harbor-impacting events,
    1856–2024."""
    events = _load_events(events_csv or _EVENTS_CSV)
    fig, ax = plt.subplots(figsize=(17.2, 8.6))

    # Background era bands for context
    eras = [
        (1856, 1930, "Pre-modern wharf era", "#fff8e7"),
        (1930, 1964, "Harbor District / pre-tsunami", "#e9f1ff"),
        (1964, 2011, "Post-1964 reconstruction era", "#ffe8e8"),
        (2011, 2025, "Tsunami-resistant era", "#e8ffe8"),
    ]
    for y0, y1, label, color in eras:
        ax.axvspan(y0, y1, facecolor=color, alpha=0.6, zorder=0)
        ax.text(
            (y0 + y1) / 2,
            len(_CATEGORIES) - 0.2,
            label,
            ha="center",
            va="top",
            fontsize=11.3,
            style="italic",
            color=PALETTE["dark"],
        )

    for year, label, cat, color_key in events:
        y = _CAT_Y[cat]
        color = PALETTE[color_key]
        marker = "X" if cat == "disaster" else "o"
        size = 280 if cat == "disaster" else 180
        ax.scatter(year, y, s=size, c=color, marker=marker, edgecolor="black", linewidth=0.9, zorder=4)
        dx, dy = _LABEL_OFFSETS.get(year, (0, 20))
        ax.annotate(
            textwrap.fill(label, width=24),
            xy=(year, y),
            xytext=(dx, dy),
            textcoords="offset points",
            ha="center",
            fontsize=10.5,
            fontweight="bold",
            color=PALETTE["dark"],
            bbox=dict(facecolor="white", edgecolor=color, boxstyle="round,pad=0.33", alpha=0.95),
            arrowprops=dict(arrowstyle="-", color=color, alpha=0.55, linewidth=0.8),
            zorder=5,
        )

    ax.set_yticks(list(range(len(_CATEGORIES))))
    ax.set_yticklabels([c[1] for c in _CATEGORIES], fontsize=13, fontweight="bold")
    ax.set_xlabel("Year", fontsize=15, fontweight="bold")
    ax.set_xlim(1850, 2030)
    ax.set_ylim(-0.7, len(_CATEGORIES) + 0.1)
    ax.set_title("Crescent City Harbor: Engineering and Disaster Timeline (1856-2024)", fontsize=19, fontweight="bold")
    ax.grid(True, axis="x", alpha=0.3)

    add_wrapped_footer(
        fig,
        "Data: data/harbor_timeline_events.csv. Markers are dated event anchors, "
        "not a full inventory of harbor maintenance, permits, or minor repairs.",
        y=0.018,
        width=124,
        fontsize=10.5,
    )

    fig.tight_layout(rect=(0, 0.065, 1, 1))
    return save_figure(fig, "harbor_timeline", output_dir)
