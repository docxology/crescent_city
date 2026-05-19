"""Shared matplotlib style for the Crescent City figure suite.

A single source of truth for the colorblind-safe Wong (2011) palette and the
rcParams that every figure inherits. Importing this module has the side
effect of applying the rcParams so figures generated in any submodule render
consistently. Idempotent — repeated imports are safe.
"""

from __future__ import annotations

import textwrap

import matplotlib
import numpy as np

matplotlib.use("Agg")  # headless rendering — must precede pyplot import
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.axes import Axes  # noqa: E402
from matplotlib.figure import Figure  # noqa: E402

# Wong (2011) colorblind-safe palette plus a few project-specific accents.
# Keep these stable: figure captions reference colors by name (e.g. "red
# downward triangles") and downstream slides reuse the same palette.
PALETTE: dict[str, str] = {
    "blue": "#0072B2",
    "orange": "#E69F00",
    "green": "#009E73",
    "red": "#D55E00",
    "purple": "#CC79A7",
    "cyan": "#56B4E9",
    "brown": "#999999",
    "yellow": "#F0E442",
    "dark": "#333333",
    "gray": "#777777",
    "light": "#E0E0E0",
    # Project-specific accents
    "water": "#A8D5E6",
    "land": "#F5F0E5",
    "forest": "#6B8E5A",
    "redwood": "#8B4513",
}

# Decade-to-color map for time-series grouping. Keep stable: economic-sector
# figure and any future longitudinal panels read decade colors from here.
DECADE_COLORS: dict[int, str] = {
    1990: PALETTE["blue"],
    2000: PALETTE["orange"],
    2010: PALETTE["green"],
    2020: PALETTE["red"],
}


# Shared rcParams. Figure-specific overrides should be applied via
# ``plt.subplots(..., figsize=...)`` or ``ax.set_title(..., fontsize=...)``
# rather than by mutating these defaults.
#
# Sans-serif typography produces denser, more legible scientific figures at
# the 300 DPI / quarter-page print sizes used throughout the manuscript. The
# font list is portable across matplotlib installations without requiring a
# system font registration.
RCPARAMS: dict[str, object] = {
    "figure.facecolor": "white",
    "axes.facecolor": "white",
    "axes.edgecolor": "#222222",
    "axes.linewidth": 1.0,
    "axes.grid": True,
    "axes.grid.axis": "both",
    "grid.alpha": 0.30,
    "grid.linewidth": 0.7,
    "grid.linestyle": "-",
    "font.family": "sans-serif",
    "font.sans-serif": [
        "DejaVu Sans",
        "Helvetica",
        "Arial",
        "Liberation Sans",
        "sans-serif",
    ],
    # Typography hierarchy — chosen for legibility at quarter-page print
    # size and for WCAG-style readability when figures are embedded in
    # web/PDF artifacts.
    "font.size": 15,
    "axes.titlesize": 20,
    "axes.titleweight": "semibold",
    "axes.titlepad": 14,
    "axes.labelsize": 16,
    "axes.labelweight": "semibold",
    "axes.labelpad": 8,
    "xtick.labelsize": 14,
    "ytick.labelsize": 14,
    "xtick.major.size": 5,
    "ytick.major.size": 5,
    "xtick.minor.size": 3,
    "ytick.minor.size": 3,
    "xtick.color": "#222222",
    "ytick.color": "#222222",
    "legend.fontsize": 14,
    "legend.title_fontsize": 15,
    "legend.frameon": True,
    "legend.framealpha": 0.95,
    "legend.edgecolor": "#444444",
    "legend.fancybox": False,
    "figure.dpi": 300,
    "savefig.dpi": 300,
    "savefig.bbox": "tight",
    "savefig.pad_inches": 0.25,
    "lines.linewidth": 2.0,
    "lines.markersize": 8,
    "patch.linewidth": 1.0,
    # Determinism: pin the SVG ID hash salt and PNG metadata so consecutive
    # runs of the same plotter produce byte-identical output. Without these,
    # matplotlib embeds run-specific element IDs and PNG creation timestamps
    # that break the project's reproducibility contract (tests assert
    # byte-identical regeneration of every pure-code figure).
    "svg.hashsalt": "crescent_city",
    # Accessibility: keep SVG text as real text nodes instead of converting
    # labels to vector paths. This makes generated figures searchable and
    # auditable in downstream document tools.
    "svg.fonttype": "none",
}


def annotate_source(ax: Axes, text: str, *, loc: str = "lower right") -> None:
    """Attach a small source/credit footer to an axis.

    Centralized so every figure that cites its data source uses the same
    style (italic, 9pt, near-edge placement, semi-transparent box). Pass the
    target axis and the credit text; loc accepts the same string keys as
    matplotlib legends.
    """
    if loc == "lower right":
        xy = (0.99, 0.01)
        ha, va = "right", "bottom"
    elif loc == "lower left":
        xy = (0.01, 0.01)
        ha, va = "left", "bottom"
    elif loc == "upper right":
        xy = (0.99, 0.99)
        ha, va = "right", "top"
    else:  # "upper left"
        xy = (0.01, 0.99)
        ha, va = "left", "top"
    ax.annotate(
        text,
        xy=xy,
        xycoords="axes fraction",
        ha=ha,
        va=va,
        fontsize=11,
        style="italic",
        color="#444444",
        bbox=dict(boxstyle="round,pad=0.3", facecolor="white", edgecolor="#cccccc", alpha=0.9),
    )


def add_wrapped_footer(
    fig: Figure,
    text: str,
    *,
    y: float = 0.018,
    width: int = 138,
    fontsize: float = 10.6,
    color: str = "#444444",
) -> None:
    """Place a consistent wrapped figure-level source/limitation footer.

    Use this for dense charts where an axis-level note would compete with
    data labels. It preserves source text as searchable SVG text and keeps
    the note outside the plotted data field.
    """
    fig.text(
        0.5,
        y,
        textwrap.fill(text, width=width),
        ha="center",
        va="bottom",
        fontsize=fontsize,
        color=color,
        style="italic",
    )


def add_scale_bar(
    ax: Axes,
    *,
    length_km: float = 10.0,
    lat_center: float = 41.75,
    x_frac: float = 0.05,
    y_frac: float = 0.05,
) -> None:
    """Add a horizontal scale bar to a stylized lat/lon cartographic plot.

    Converts ``length_km`` to degrees of longitude at ``lat_center`` (the
    central latitude of the map), draws a black bar at fractional axes
    position ``(x_frac, y_frac)``, and labels it underneath.
    """
    # 1 degree longitude at given latitude ≈ 111.32 km * cos(lat)
    deg_per_km = 1.0 / (111.32 * np.cos(np.deg2rad(lat_center)))
    bar_deg = length_km * deg_per_km

    xmin, xmax = ax.get_xlim()
    ymin, ymax = ax.get_ylim()
    x_lo = xmin + x_frac * (xmax - xmin)
    y_lo = ymin + y_frac * (ymax - ymin)
    ax.plot([x_lo, x_lo + bar_deg], [y_lo, y_lo], color="black", linewidth=3, solid_capstyle="butt", zorder=10)
    # End ticks
    tick_h = 0.0025 * (ymax - ymin)
    for x_end in (x_lo, x_lo + bar_deg):
        ax.plot([x_end, x_end], [y_lo - tick_h, y_lo + tick_h], color="black", linewidth=1.4, zorder=10)
    ax.text(
        x_lo + bar_deg / 2,
        y_lo - 4 * tick_h,
        f"{length_km:g} km",
        ha="center",
        va="top",
        fontsize=11,
        fontweight="semibold",
    )


def add_north_arrow(ax: Axes, *, x_frac: float = 0.92, y_frac: float = 0.92) -> None:
    """Add a simple north-arrow indicator at fractional axes position."""
    xmin, xmax = ax.get_xlim()
    ymin, ymax = ax.get_ylim()
    x = xmin + x_frac * (xmax - xmin)
    y = ymin + y_frac * (ymax - ymin)
    arrow_h = 0.04 * (ymax - ymin)
    ax.annotate(
        "N",
        xy=(x, y + arrow_h),
        xytext=(x, y - arrow_h * 0.3),
        ha="center",
        va="bottom",
        fontsize=12,
        fontweight="bold",
        arrowprops=dict(arrowstyle="-|>", color="black", lw=2, connectionstyle="arc3", mutation_scale=18),
        zorder=10,
    )


def apply() -> None:
    """Apply the shared rcParams to the current matplotlib session.

    Called eagerly at import time of :mod:`src.figures` so that *any*
    figure plotted thereafter uses the consistent style. Safe to call
    multiple times.
    """
    plt.rcParams.update(RCPARAMS)


# Apply on import so all plotters share one visual standard.
apply()
