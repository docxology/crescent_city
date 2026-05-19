"""Conservation-history figures.

One figure: the loss of old-growth coast redwood from 1850 to 2025,
with the principal conservation milestones annotated. Annotation
positions are deliberately staggered above and below the curve to
keep the dense milestone labels legible.
"""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import numpy as np

from ._io import save_figure
from ._style import PALETTE, add_wrapped_footer

_DATA_DIR = Path(__file__).resolve().parents[2] / "data"
_ACREAGE_CSV = _DATA_DIR / "redwood_old_growth_acreage.csv"
_MILESTONES_CSV = _DATA_DIR / "redwood_conservation_milestones.csv"


def _load_acreage(path: Path) -> tuple[np.ndarray, np.ndarray]:
    with path.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    years = np.array([int(row["year"]) for row in rows])
    acres = np.array([int(row["acres"]) for row in rows])
    order = np.argsort(years)
    return years[order], acres[order]


def _load_milestones(path: Path) -> list[dict[str, Any]]:
    with path.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    out: list[dict[str, Any]] = []
    for row in rows:
        out.append(
            {
                "year": int(row["year"]),
                "label": row["label"].replace("|", "\n"),
                "label_x": float(row["label_x"]),
                "label_y": float(row["label_y"]),
            }
        )
    return sorted(out, key=lambda r: int(r["year"]))


def plot_redwood_decline_chart(
    output_dir: Path,
    acreage_csv: Path | None = None,
    milestones_csv: Path | None = None,
    **_: object,
) -> Path:
    """Old-growth coast-redwood acreage decline, 1850-2025.

    Data-backed figure. Acreage points and milestone label positions live
    in checked-in CSV files so the historical estimates and source keys can
    be audited separately from the plotting geometry.
    """
    years, acres = _load_acreage(acreage_csv or _ACREAGE_CSV)
    milestones = _load_milestones(milestones_csv or _MILESTONES_CSV)

    fig, ax = plt.subplots(figsize=(16.5, 9.6))

    ax.fill_between(years, 0, acres, color=PALETTE["redwood"], alpha=0.25, zorder=2)
    ax.plot(
        years,
        acres,
        color=PALETTE["redwood"],
        linewidth=3.5,
        marker="o",
        markersize=10,
        markerfacecolor=PALETTE["redwood"],
        markeredgecolor="white",
        zorder=3,
    )

    for milestone in milestones:
        yr = int(milestone["year"])
        label = str(milestone["label"])
        y_at = float(np.interp(yr, years, acres))
        ax.axvline(yr, color=PALETTE["dark"], linestyle=":", alpha=0.35, zorder=1)
        ax.annotate(
            label,
            xy=(yr, y_at),
            xytext=(float(milestone["label_x"]), float(milestone["label_y"])),
            fontsize=11.2,
            fontweight="bold",
            color=PALETTE["dark"],
            ha="center",
            bbox=dict(facecolor="white", edgecolor=PALETTE["green"], boxstyle="round,pad=0.3", alpha=0.95),
            arrowprops=dict(arrowstyle="->", color=PALETTE["green"], lw=1.5),
            zorder=5,
        )

    # 2025 endpoint annotation
    current_year = int(years[-1])
    current_acres = int(acres[-1])
    ax.scatter(
        [current_year],
        [current_acres],
        s=260,
        marker="*",
        color=PALETTE["red"],
        edgecolor="white",
        linewidth=1.5,
        zorder=6,
    )
    ax.annotate(
        "~110,000 acres remaining\n(about 5% of original)\n— about 45% in RNSP —",
        xy=(current_year, current_acres),
        xytext=(2013, 790_000),
        fontsize=12.2,
        fontweight="bold",
        color=PALETTE["red"],
        bbox=dict(facecolor="white", edgecolor=PALETTE["red"], boxstyle="round,pad=0.5", alpha=0.96),
        arrowprops=dict(arrowstyle="->", color=PALETTE["red"], lw=2),
        zorder=6,
    )

    # Origin annotation
    ax.annotate(
        "~2.2 million acres\noriginal coast-redwood extent\n(pre-American settlement)",
        xy=(int(years[0]), int(acres[0])),
        xytext=(1859, 1_500_000),
        fontsize=12.2,
        fontweight="bold",
        color=PALETTE["redwood"],
        bbox=dict(facecolor="white", edgecolor=PALETTE["redwood"], boxstyle="round,pad=0.4", alpha=0.95),
        arrowprops=dict(arrowstyle="->", color=PALETTE["redwood"], lw=1.5),
        zorder=6,
    )

    ax.set_xlim(1845, 2035)
    ax.set_ylim(0, 2_500_000)
    ax.set_xlabel("Year", fontsize=16, fontweight="bold")
    ax.set_ylabel("Old-Growth Coast Redwood (acres)", fontsize=16, fontweight="bold")
    ax.set_title("Old-Growth Coast Redwood Forest — Decline and Protection, 1850–2025", fontsize=20, fontweight="bold")
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"{int(x / 1000):,}k"))
    ax.grid(True, alpha=0.3)

    add_wrapped_footer(
        fig,
        "Data: data/redwood_old_growth_acreage.csv and "
        "data/redwood_conservation_milestones.csv. Acreage points are rounded "
        "cited estimates, not a parcel-level inventory; milestone dates are "
        "statutory or administrative dates where available.",
        y=0.018,
        width=132,
    )

    fig.tight_layout(rect=(0, 0.075, 1, 1))
    return save_figure(fig, "redwood_decline_chart", output_dir)
