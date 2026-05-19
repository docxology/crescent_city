"""Custom hand-drawn-style cartographic and place-relationship figures.

The regional reference map is a stylized latitude/longitude orientation
figure. The Tolowa Dee-ni' place-relationship figure is deliberately
non-coordinate and omits protected-location detail.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D
from matplotlib.patches import Ellipse, FancyArrowPatch, FancyBboxPatch, Polygon, Rectangle

from ._io import save_figure
from ._style import PALETTE, add_north_arrow, add_scale_bar, add_wrapped_footer

# ═══════════════════════════════════════════════════════════════════════
# Figure — Regional reference map
# ═══════════════════════════════════════════════════════════════════════


def plot_regional_map(output_dir: Path, **_: object) -> Path:
    """Reference map of the Crescent City / Del Norte County region.

    Stylized — not survey-grade. Coordinates approximate spatial
    relationships only. Layout choices move the legend off the Cascadia
    annotation, tighten label positioning around Pelican Bay and Lake Earl,
    and route the Highway 199 polyline through the Smith River drainage.
    """
    fig, ax = plt.subplots(figsize=(14, 13))
    LON_MIN, LON_MAX = -124.50, -123.40
    LAT_MIN, LAT_MAX = 41.40, 42.12

    # Pacific Ocean background
    ax.add_patch(
        Rectangle(
            (LON_MIN, LAT_MIN),
            LON_MAX - LON_MIN,
            LAT_MAX - LAT_MIN,
            facecolor=PALETTE["water"],
            edgecolor="none",
            zorder=0,
        )
    )

    # Stylized coastline
    coast = np.array(
        [
            (-124.20, LAT_MIN),
            (-124.18, 41.50),
            (-124.17, 41.55),
            (-124.18, 41.60),
            (-124.21, 41.65),
            (-124.20, 41.72),
            (-124.235, 41.745),
            (-124.255, 41.78),
            (-124.20, 41.83),
            (-124.18, 41.90),
            (-124.21, 41.95),
            (-124.20, 42.00),
            (-124.16, 42.005),
            (LON_MAX, 42.005),
            (LON_MAX, LAT_MIN),
        ]
    )
    ax.add_patch(
        Polygon(coast, closed=True, facecolor=PALETTE["land"], edgecolor=PALETTE["dark"], linewidth=1.2, zorder=1)
    )

    # Forested upland shading
    forest = np.array([(-124.10, LAT_MIN), (LON_MAX, LAT_MIN), (LON_MAX, 41.99), (-124.10, 41.99)])
    ax.add_patch(Polygon(forest, closed=True, facecolor=PALETTE["forest"], alpha=0.18, edgecolor="none", zorder=1))

    # Tolowa Dee-ni' traditional-territory overlay
    tolowa = np.array(
        [
            (-124.27, 41.78),
            (-124.18, 41.78),
            (-124.10, 41.85),
            (-124.05, 41.95),
            (-124.05, 42.005),
            (-123.85, 42.005),
            (-123.85, 41.85),
            (-124.10, 41.75),
        ]
    )
    ax.add_patch(
        Polygon(
            tolowa,
            closed=True,
            facecolor=PALETTE["orange"],
            alpha=0.18,
            edgecolor=PALETTE["orange"],
            linestyle="--",
            linewidth=1.3,
            zorder=2,
        )
    )

    # Smith River drainage (Hwy 199 follows this)
    smith_x = np.array([-123.50, -123.65, -123.80, -123.95, -124.05, -124.12, -124.18, -124.20])
    smith_y = np.array([41.85, 41.86, 41.88, 41.92, 41.97, 41.985, 41.99, 42.00])
    ax.plot(smith_x, smith_y, color=PALETTE["blue"], linewidth=2.2, zorder=3)

    # Klamath River
    ax.plot(
        [-123.50, -123.75, -124.00, -124.05],
        [41.60, 41.55, 41.55, 41.55],
        color=PALETTE["blue"],
        linewidth=2.2,
        zorder=3,
    )

    # Lake Earl / Lake Talawa lagoon
    ax.add_patch(
        Ellipse(
            (-124.21, 41.83),
            0.045,
            0.065,
            facecolor=PALETTE["water"],
            edgecolor=PALETTE["blue"],
            linewidth=1.4,
            zorder=3,
        )
    )

    # US Highway 101 (coastal spine)
    ax.plot(
        [-124.21, -124.20, -124.20, -124.05, -124.03],
        [41.45, 41.55, 41.72, 41.55, 42.005],
        color=PALETTE["red"],
        linewidth=2.4,
        zorder=4,
    )
    # US Highway 199 (interior to Oregon, runs along the Smith)
    ax.plot(
        [-124.20, -124.18, -124.05, -123.80, -123.50, -123.40],
        [41.72, 41.85, 41.95, 41.92, 41.97, 42.00],
        color=PALETTE["orange"],
        linewidth=2.0,
        zorder=4,
    )

    # CA/OR border
    ax.axhline(42.005, color=PALETTE["dark"], linewidth=1.6, linestyle=":", zorder=5)
    ax.text(
        LON_MIN + 0.02, 42.025, "CALIFORNIA — OREGON state border", fontsize=11, style="italic", color=PALETTE["dark"]
    )

    # Point database: (label, lon, lat, kind, label_dx, label_dy)
    points = [
        ("Crescent City", -124.20, 41.755, "city", 10, 4),
        ("Smith River", -124.15, 41.95, "town", 8, 4),
        ("Klamath", -124.04, 41.54, "town", 8, 4),
        ("Gasquet", -123.97, 41.85, "town", 8, 4),
        ("Battery Pt. Lt.", -124.245, 41.745, "landmark", -85, -6),
        ("Point St. George", -124.265, 41.78, "landmark", -90, 4),
        ("Pelican Bay State Prison", -124.19, 41.88, "prison", 8, 4),
        ("Last Chance Grade", -124.06, 41.62, "hazard", 8, 4),
        ("Jedediah Smith Redwoods SP", -123.92, 41.80, "park", 8, 4),
        ("Del Norte Coast Redwoods SP", -124.08, 41.65, "park", 8, -10),
        ("Prairie Creek Redwoods SP", -124.05, 41.42, "park", 8, 4),
        ("Redwood National Park", -123.92, 41.50, "park", 8, 4),
        ("Lake Earl / Talawa", -124.165, 41.83, "lagoon", 0, 0),
    ]
    # Marker, color, size, fontweight, fontsize — typed explicitly so mypy
    # can see scatter() receives the right kinds (matplotlib's overloads are
    # picky: marker must be ``str|Path|MarkerStyle|None``; ``s`` must be a
    # numeric scalar, not ``object``).
    style_map: dict[str, tuple[str, str, float, str, int]] = {
        "city": ("*", PALETTE["red"], 380.0, "bold", 13),
        "town": ("o", PALETTE["dark"], 80.0, "normal", 11),
        "landmark": ("^", PALETTE["purple"], 110.0, "normal", 10),
        "tribal": ("s", PALETTE["orange"], 120.0, "bold", 11),
        "prison": ("P", PALETTE["dark"], 140.0, "normal", 10),
        "hazard": ("X", PALETTE["red"], 140.0, "bold", 10),
        "park": ("o", PALETTE["green"], 70.0, "normal", 10),
        "lagoon": ("", PALETTE["blue"], 0.0, "normal", 10),
    }
    individual_labels = {
        "Crescent City",
        "Smith River",
        "Klamath",
        "Gasquet",
        "Battery Pt. Lt.",
        "Point St. George",
        "Pelican Bay State Prison",
        "Last Chance Grade",
        "Lake Earl / Talawa",
    }
    for label, lon, lat, kind, dx, dy in points:
        marker, color, size, weight, fs = style_map[kind]
        if marker:
            ax.scatter(
                lon,
                lat,
                marker=marker,
                color=color,
                s=size,
                zorder=6,
                edgecolors="black",
                linewidths=0.6,
            )
        if label in individual_labels:
            ax.annotate(
                label,
                (lon, lat),
                textcoords="offset points",
                xytext=(dx, dy),
                fontsize=fs,
                fontweight=weight,
                color=color,
                zorder=7,
            )

    ax.text(
        -123.74,
        41.58,
        "Redwood parks\ncorridor",
        fontsize=11.2,
        fontweight="bold",
        color=PALETTE["green"],
        style="italic",
        ha="center",
        bbox=dict(facecolor="white", edgecolor=PALETTE["green"], boxstyle="round,pad=0.25", alpha=0.84),
        zorder=7,
    )

    # Cascadia subduction zone — moved to top-left, well clear of legend
    ax.annotate(
        "CASCADIA\nSUBDUCTION ZONE\n(offshore, ~100 km west)",
        xy=(-124.42, 41.95),
        ha="center",
        va="center",
        fontsize=12,
        fontweight="bold",
        color=PALETTE["red"],
        style="italic",
        bbox=dict(facecolor="white", edgecolor=PALETTE["red"], boxstyle="round,pad=0.4", alpha=0.92),
        zorder=8,
    )
    ax.add_patch(
        FancyArrowPatch(
            (-124.42, 41.90),
            (-124.28, 41.80),
            arrowstyle="->",
            mutation_scale=18,
            color=PALETTE["red"],
            linewidth=2,
            zorder=8,
        )
    )

    # Pacific Ocean watermark — clear of all annotations
    ax.text(
        -124.45,
        41.55,
        "PACIFIC\nOCEAN",
        fontsize=16,
        fontweight="bold",
        color=PALETTE["blue"],
        style="italic",
        alpha=0.7,
        ha="center",
    )

    # Six Rivers NF label — clear of road / Hwy 199 line
    ax.text(
        -123.55,
        41.70,
        "Six Rivers\nNational Forest",
        fontsize=12,
        fontweight="bold",
        color=PALETTE["forest"],
        style="italic",
        alpha=0.85,
        ha="center",
    )

    # Legend — moved to bottom-left, smaller, no overlap with subduction box
    legend_items = [
        mpatches.Patch(
            facecolor=PALETTE["orange"],
            alpha=0.18,
            edgecolor=PALETTE["orange"],
            linestyle="--",
            label="Tolowa Dee-ni' traditional territory",
        ),
        mpatches.Patch(facecolor=PALETTE["forest"], alpha=0.18, label="Forested uplands"),
        mpatches.Patch(facecolor=PALETTE["water"], label="Open water / lagoons"),
        Line2D([0], [0], color=PALETTE["red"], linewidth=2.4, label="US Hwy 101"),
        Line2D([0], [0], color=PALETTE["orange"], linewidth=2.0, label="US Hwy 199"),
        Line2D([0], [0], color=PALETTE["blue"], linewidth=2.0, label="Smith / Klamath rivers"),
        Line2D([0], [0], marker="*", color="w", markerfacecolor=PALETTE["red"], markersize=14, label="County seat"),
        Line2D(
            [0],
            [0],
            marker="o",
            color="w",
            markerfacecolor=PALETTE["green"],
            markersize=10,
            label="State / national park corridor",
        ),
        Line2D(
            [0],
            [0],
            marker="s",
            color="w",
            markerfacecolor=PALETTE["orange"],
            markersize=10,
            label="Tolowa cultural site",
        ),
    ]
    ax.legend(handles=legend_items, loc="lower right", fontsize=10.5, framealpha=0.95, ncol=1, borderpad=0.6)

    ax.set_xlim(LON_MIN, LON_MAX)
    ax.set_ylim(LAT_MIN, LAT_MAX)
    ax.set_xlabel("Longitude (°W)")
    ax.set_ylabel("Latitude (°N)")
    ax.set_title("Crescent City and Del Norte County — Regional Reference Map")
    ax.set_aspect(1 / np.cos(np.deg2rad(41.75)))
    ax.grid(True, alpha=0.25, linestyle="--")

    add_scale_bar(ax, length_km=10.0, lat_center=41.75)
    add_north_arrow(ax)
    add_wrapped_footer(
        fig,
        "Source basis: stylized reference map from public geographic coordinates and local GIS context. Points, road lines, "
        "territory overlays, and the offshore Cascadia arrow are approximate and not survey-grade.",
        y=0.018,
        width=124,
        fontsize=9.8,
    )
    fig.subplots_adjust(bottom=0.075, top=0.92)

    return save_figure(fig, "regional_map", output_dir)


# ═══════════════════════════════════════════════════════════════════════
# Figure — Tolowa Dee-ni' public place relationships
# ═══════════════════════════════════════════════════════════════════════


def plot_tolowa_villages_map(output_dir: Path, **_: object) -> Path:
    """Generalized Tolowa Dee-ni' place relationships without coordinates."""
    fig, ax = plt.subplots(figsize=(13.2, 10.6))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis("off")

    ax.add_patch(Rectangle((0, 0), 2.0, 10, facecolor=PALETTE["water"], edgecolor="none", zorder=0))
    ax.add_patch(Rectangle((2.0, 0), 8.0, 10, facecolor=PALETTE["land"], edgecolor="none", zorder=0))
    ax.add_patch(
        Polygon(
            [(1.85, 0.2), (2.25, 1.2), (2.0, 2.8), (2.35, 4.4), (2.08, 6.0), (2.32, 8.4), (2.0, 9.8)],
            closed=False,
            fill=False,
            edgecolor=PALETTE["dark"],
            linewidth=2.2,
            zorder=2,
        )
    )
    ax.plot([2.2, 3.0, 4.2, 5.6, 7.3, 8.8], [7.2, 7.65, 8.0, 8.25, 8.45, 8.65], color=PALETTE["blue"], lw=3)
    ax.text(5.35, 8.62, "Smith River relationship", color=PALETTE["blue"], fontsize=12.5, fontweight="bold")
    ax.add_patch(Ellipse((2.7, 5.6), 0.9, 1.45, facecolor=PALETTE["water"], edgecolor=PALETTE["blue"], lw=1.8))
    ax.text(2.8, 4.65, "Lake Earl / Talawa\nlagoon context", ha="center", fontsize=10.4, color=PALETTE["blue"])
    ax.axhline(9.25, color=PALETTE["dark"], lw=1.5, ls=":")
    ax.text(2.25, 9.38, "present CA-OR state line", fontsize=10.5, style="italic", color=PALETTE["dark"])

    territory = FancyBboxPatch(
        (2.35, 1.05),
        6.95,
        7.85,
        boxstyle="round,pad=0.25,rounding_size=0.28",
        facecolor=PALETTE["orange"],
        edgecolor=PALETTE["orange"],
        alpha=0.12,
        linewidth=1.8,
        linestyle="--",
    )
    ax.add_patch(territory)
    ax.text(
        7.55,
        1.55,
        "Tolowa Dee-ni'\npublic cultural-geography frame",
        fontsize=14,
        color=PALETTE["orange"],
        fontweight="bold",
        ha="center",
        style="italic",
    )
    ax.text(0.65, 4.9, "PACIFIC\nOCEAN", fontsize=15, fontweight="bold", color=PALETTE["blue"], ha="center")

    cards = [
        (
            4.0,
            7.35,
            "Smith River estuary",
            "Public names include Yontocket,\nHowonquet, and Tepashne.",
        ),
        (
            3.75,
            5.45,
            "Lagoon and coastal villages",
            "Public names include How-On-Quer,\nEtchulet, and related lake/coast references.",
        ),
        (
            3.75,
            3.45,
            "Headlands and town overlay",
            "Public place references include Tatitun\nand Point St. George.",
        ),
        (
            6.95,
            6.25,
            "River, trail, and language relations",
            "Pacific Coast Athabaskan context links\nTolowa with neighboring Chetco, Tututni,\nHupa, and Yurok histories.",
        ),
        (
            6.75,
            4.0,
            "Klamath boundary context",
            "Shown as a relationship zone only,\nnot a site-location claim.",
        ),
    ]
    for x, y, title, body in cards:
        ax.add_patch(
            FancyBboxPatch(
                (x - 1.35, y - 0.58),
                2.7,
                1.16,
                boxstyle="round,pad=0.18,rounding_size=0.12",
                facecolor="white",
                edgecolor=PALETTE["orange"],
                linewidth=1.5,
                alpha=0.96,
                zorder=5,
            )
        )
        ax.text(x, y + 0.22, title, ha="center", va="center", fontsize=10.6, fontweight="bold", color=PALETTE["dark"], zorder=6)
        ax.text(x, y - 0.25, body, ha="center", va="center", fontsize=8.9, color=PALETTE["dark"], zorder=6)

    arrows = [
        ((4.65, 7.0), (5.95, 6.45)),
        ((4.6, 5.42), (5.45, 5.72)),
        ((4.55, 3.55), (5.55, 3.9)),
        ((6.6, 5.65), (6.65, 4.62)),
    ]
    for start, end in arrows:
        ax.annotate("", xy=end, xytext=start, arrowprops=dict(arrowstyle="->", color=PALETTE["brown"], lw=1.4))

    ax.set_title("Tolowa Dee-ni' Public Place Relationships", fontsize=18, fontweight="bold", pad=18)
    ax.text(
        0.5,
        0.055,
        "Generalized schematic: no latitude/longitude axes, point coordinates, parcel references, site IDs, or protected-location detail.",
        transform=ax.transAxes,
        ha="center",
        fontsize=10.6,
        color=PALETTE["dark"],
        bbox=dict(facecolor="white", edgecolor=PALETTE["dark"], boxstyle="round,pad=0.3", alpha=0.92),
    )
    add_wrapped_footer(
        fig,
        "Source basis: public tribal-history and ethnographic synthesis. The drawing preserves relative relationships among coast, river, "
        "lagoon, headlands, and language neighbors without publishing archaeological coordinates or sensitive cultural-resource identifiers.",
        y=0.012,
        width=130,
        fontsize=9.6,
    )
    fig.subplots_adjust(bottom=0.09, top=0.9, left=0.04, right=0.98)
    return save_figure(fig, "tolowa_villages_map", output_dir)
