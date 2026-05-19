"""Political-geography figures — proposed State of Jefferson territory.

One figure: a schematic map of the proposed State of Jefferson and the
California / Oregon counties that have voted to join the modern revival
movement, with Crescent City marked as a participating county seat.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D
from matplotlib.patches import Polygon, Rectangle

from ._io import save_figure
from ._style import PALETTE, add_wrapped_footer

# Approximate centroids and stylized polygons for the participating counties.
# Coordinates are illustrative — not survey-grade.
# Counties whose Boards of Supervisors or voters formally engaged with the
# 2013-2015 modern Jefferson revival. Status decoded as ("joined" / "declined").
# Sources: Ballotpedia, Sacramento Bee, JPR, BoS minutes 2013-2015.
_CALIF_COUNTIES = [
    # (name, centroid_lon, centroid_lat, year, status, polygon)
    (
        "Del Norte",
        -123.95,
        41.75,
        2014,
        "declined",
        [(-124.4, 41.40), (-123.50, 41.40), (-123.50, 42.00), (-124.4, 42.00)],
    ),
    (
        "Siskiyou",
        -122.50,
        41.60,
        2013,
        "joined",
        [(-123.50, 41.18), (-121.45, 41.18), (-121.45, 42.00), (-123.50, 42.00)],
    ),
    ("Modoc", -120.70, 41.55, 2013, "joined", [(-121.45, 41.18), (-119.99, 41.18), (-119.99, 42.00), (-121.45, 42.00)]),
    (
        "Lassen",
        -120.65,
        40.65,
        2015,
        "joined",
        [(-121.30, 40.15), (-119.99, 40.15), (-119.99, 41.18), (-121.30, 41.18)],
    ),
    (
        "Tehama",
        -122.20,
        40.05,
        2014,
        "joined",
        [(-123.05, 39.80), (-121.55, 39.80), (-121.55, 40.45), (-123.05, 40.45)],
    ),
    ("Glenn", -122.40, 39.55, 2014, "joined", [(-122.95, 39.30), (-122.00, 39.30), (-122.00, 39.80), (-122.95, 39.80)]),
    ("Yuba", -121.40, 39.25, 2014, "joined", [(-121.65, 39.05), (-121.10, 39.05), (-121.10, 39.45), (-121.65, 39.45)]),
    (
        "Sutter",
        -121.70,
        39.00,
        2014,
        "joined",
        [(-122.00, 38.85), (-121.40, 38.85), (-121.40, 39.20), (-122.00, 39.20)],
    ),
    ("Lake", -122.85, 39.10, 2015, "joined", [(-123.10, 38.85), (-122.50, 38.85), (-122.50, 39.40), (-123.10, 39.40)]),
]
_OR_COUNTIES = [
    ("Curry", -124.30, 42.40, None, [(-124.50, 42.005), (-124.05, 42.005), (-124.05, 42.85), (-124.50, 42.85)]),
    ("Josephine", -123.50, 42.40, None, [(-123.85, 42.005), (-123.10, 42.005), (-123.10, 42.85), (-123.85, 42.85)]),
    ("Jackson", -122.80, 42.40, None, [(-123.10, 42.005), (-122.30, 42.005), (-122.30, 42.85), (-123.10, 42.85)]),
    ("Klamath", -121.65, 42.40, None, [(-122.30, 42.005), (-120.50, 42.005), (-120.50, 43.10), (-122.30, 43.10)]),
]


def plot_jefferson_map(output_dir: Path, **_kwargs: object) -> Path:
    """Schematic of the proposed State of Jefferson territory.

    Stylized — not survey-grade. Counties are drawn as approximate
    rectangles; the exact boundaries are not the figure's claim.
    The Yreka declaration site is marked, as is Crescent City as a
    participating county seat.
    """
    fig, ax = plt.subplots(figsize=(15, 12))

    LON_MIN, LON_MAX = -124.8, -119.5
    LAT_MIN, LAT_MAX = 38.6, 43.2

    # Pacific
    ax.add_patch(
        Rectangle((LON_MIN, LAT_MIN), LON_MAX - LON_MIN, LAT_MAX - LAT_MIN, facecolor=PALETTE["water"], zorder=0)
    )

    # Approximate land mask — straight-line CA/OR coast and east margin
    land = np.array(
        [
            (-124.40, LAT_MIN),
            (-124.40, 41.50),
            (-124.20, 41.75),
            (-124.20, 42.00),
            (-124.50, 42.20),
            (-124.40, 42.85),
            (-124.10, 42.85),
            (LON_MAX, 42.85),
            (LON_MAX, LAT_MIN),
        ]
    )
    ax.add_patch(
        Polygon(land, closed=True, facecolor=PALETTE["land"], edgecolor=PALETTE["dark"], linewidth=1.0, zorder=1)
    )

    # CA counties — green if joined, red-hatched if declined
    for name, cx, cy, year, status, poly in _CALIF_COUNTIES:
        if status == "joined":
            ax.add_patch(
                Polygon(
                    poly,
                    closed=True,
                    facecolor=PALETTE["green"],
                    alpha=0.32,
                    edgecolor=PALETTE["green"],
                    linewidth=1.4,
                    zorder=2,
                )
            )
            label = f"{name}\n{year}"
        else:
            ax.add_patch(
                Polygon(
                    poly,
                    closed=True,
                    facecolor=PALETTE["red"],
                    alpha=0.20,
                    edgecolor=PALETTE["red"],
                    linewidth=1.4,
                    hatch="//",
                    zorder=2,
                )
            )
            label = f"{name}\n{year} no"
        ax.text(cx, cy, label, ha="center", va="center", fontsize=8.7, fontweight="bold", color=PALETTE["dark"])

    # OR sympathetic counties (un-voted but historically aligned)
    for name, cx, cy, _, poly in _OR_COUNTIES:
        ax.add_patch(
            Polygon(
                poly,
                closed=True,
                facecolor=PALETTE["orange"],
                alpha=0.22,
                edgecolor=PALETTE["orange"],
                linewidth=1.4,
                linestyle="--",
                zorder=2,
            )
        )
        ax.text(cx, cy, name, ha="center", va="center", fontsize=8.7, color=PALETTE["dark"])

    # CA / OR border
    ax.axhline(42.005, color=PALETTE["dark"], linewidth=2.2, zorder=4)
    ax.text(LON_MIN + 0.08, 42.06, "California — Oregon border", fontsize=10, style="italic", color=PALETTE["dark"])

    # Key cities and historic sites
    sites = [
        ("Yreka, CA", -122.63, 41.74, "1941 declaration"),
        ("Crescent City", -124.20, 41.755, "Del Norte seat"),
        ("Port Orford, OR", -124.50, 42.74, "Oregon anchor"),
        ("Redding, CA", -122.39, 40.59, "regional hub"),
    ]
    site_offsets = {
        "Yreka, CA": (22, 22),
        "Crescent City": (36, -44),
        "Port Orford, OR": (38, -12),
        "Redding, CA": (28, -26),
    }
    for name, lon, lat, role in sites:
        ax.scatter(lon, lat, marker="*", s=350, color=PALETTE["red"], edgecolor="white", linewidth=1.5, zorder=6)
        ax.annotate(
            f"{name}\n{role}",
            xy=(lon, lat),
            xytext=site_offsets[name],
            textcoords="offset points",
            fontsize=8.9,
            fontweight="bold",
            color=PALETTE["red"],
            bbox=dict(facecolor="white", edgecolor=PALETTE["red"], boxstyle="round,pad=0.3", alpha=0.92),
            zorder=7,
        )

    # Ocean watermark
    ax.text(
        LON_MIN + 0.15,
        41.0,
        "PACIFIC\nOCEAN",
        fontsize=15,
        fontweight="bold",
        color=PALETTE["blue"],
        style="italic",
        alpha=0.7,
    )

    # Legend
    legend_items = [
        mpatches.Patch(
            facecolor=PALETTE["green"],
            alpha=0.32,
            edgecolor=PALETTE["green"],
            label="CA county whose Board voted to join",
        ),
        mpatches.Patch(
            facecolor=PALETTE["red"],
            alpha=0.20,
            edgecolor=PALETTE["red"],
            hatch="//",
            label="CA county whose voters declined (Measure A)",
        ),
        mpatches.Patch(
            facecolor=PALETTE["orange"],
            alpha=0.22,
            edgecolor=PALETTE["orange"],
            linestyle="--",
            label="Sympathetic OR county (no formal vote)",
        ),
        Line2D(
            [0],
            [0],
            marker="*",
            color="w",
            markerfacecolor=PALETTE["red"],
            markersize=14,
            label="Historic site or county seat",
        ),
    ]
    ax.legend(
        handles=legend_items,
        loc="upper center",
        bbox_to_anchor=(0.5, -0.08),
        ncol=2,
        fontsize=9.6,
        framealpha=0.95,
    )

    ax.set_xlim(LON_MIN, LON_MAX)
    ax.set_ylim(LAT_MIN, LAT_MAX)
    ax.set_xlabel("Longitude (°W)")
    ax.set_ylabel("Latitude (°N)")
    ax.set_title(
        "The State of Jefferson — Proposed Secession Territory and Participating Counties",
        fontsize=16,
        fontweight="bold",
    )
    ax.set_aspect(1 / np.cos(np.deg2rad(40.5)))
    ax.grid(True, alpha=0.25, linestyle="--")

    add_wrapped_footer(
        fig,
        "Stylized, not survey-grade: approximate county rectangles show political geography, not legal boundaries. "
        "Jefferson was first proclaimed at Yreka on 27 Nov 1941; Del Norte voters declined Measure A in 2014.",
        y=0.04,
        width=132,
        fontsize=9.8,
    )
    fig.subplots_adjust(bottom=0.17)
    return save_figure(fig, "jefferson_map", output_dir)
