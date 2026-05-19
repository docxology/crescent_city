"""Climate figures — Crescent City monthly climograph.

One figure: a climograph combining monthly mean temperature, precipitation,
and wet-day frequency from NOAA NCEI 1991-2020 monthly normals for Crescent
City McNamara Airport (USW00024286).
"""

from __future__ import annotations

import textwrap
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import pandas as pd

from ._io import save_figure
from ._style import PALETTE, add_wrapped_footer

_DATA_DIR = Path(__file__).resolve().parents[2] / "data"


def plot_climograph(output_dir: Path, climate_csv: Path | None = None) -> Path:
    """Crescent City monthly climograph from NOAA NCEI monthly normals.

    The figure uses only fields available from the station normals table:
    mean monthly temperature, precipitation, and the average number of days
    with at least 0.01 inch of precipitation.
    """
    csv = climate_csv or _DATA_DIR / "climate_normals_1991_2020.csv"
    df = pd.read_csv(csv)
    months = df["month_name"].tolist()
    x = df["month"].to_numpy() - 1

    fig, ax1 = plt.subplots(figsize=(14, 8))

    # Precipitation bars (left axis)
    bars = ax1.bar(
        x,
        df["prcp_in"],
        color=PALETTE["blue"],
        alpha=0.7,
        edgecolor=PALETTE["dark"],
        linewidth=0.7,
        width=0.7,
        label="Mean precipitation (in)",
        zorder=2,
    )
    for b, v in zip(bars, df["prcp_in"]):
        ax1.text(
            b.get_x() + b.get_width() / 2,
            b.get_height() + 0.3,
            f"{v:.1f}",
            ha="center",
            fontsize=10,
            color=PALETTE["blue"],
            fontweight="bold",
        )
    ax1.set_xlabel("Month")
    ax1.set_ylabel("Precipitation (inches per month)", color=PALETTE["blue"])
    ax1.tick_params(axis="y", labelcolor=PALETTE["blue"])
    ax1.set_ylim(0, 16)
    ax1.set_xticks(x)
    ax1.set_xticklabels(months)

    # Temperature line (right axis 1)
    ax2 = ax1.twinx()
    ax2.plot(
        x,
        df["tavg_f"],
        color=PALETTE["red"],
        marker="o",
        linewidth=3,
        markersize=10,
        zorder=4,
        label="Mean temperature (°F)",
    )
    ax2.set_ylabel("Temperature (°F)", color=PALETTE["red"])
    ax2.tick_params(axis="y", labelcolor=PALETTE["red"])
    ax2.set_ylim(40, 70)

    # Wet days as secondary overlay from the same NOAA normals table.
    ax3 = ax1.twinx()
    ax3.spines["right"].set_position(("outward", 60))
    ax3.plot(
        x,
        df["wet_days_ge_0_01_in"],
        color=PALETTE["gray"],
        marker="s",
        linewidth=2,
        linestyle="--",
        markersize=8,
        zorder=3,
        label="Wet days (>=0.01 in)",
    )
    ax3.set_ylabel("Wet days per month", color=PALETTE["gray"])
    ax3.tick_params(axis="y", labelcolor=PALETTE["gray"])
    ax3.set_ylim(0, 28)

    ax1.set_title("Crescent City Climate Normals (1991–2020): Temperature, Precipitation, and Wet Days")

    # Combined legend
    lines1, lbl1 = ax1.get_legend_handles_labels()
    lines2, lbl2 = ax2.get_legend_handles_labels()
    lines3, lbl3 = ax3.get_legend_handles_labels()
    ax1.legend(lines1 + lines2 + lines3, lbl1 + lbl2 + lbl3, loc="upper center", ncol=3)

    ax1.grid(True, axis="y", alpha=0.3)
    add_wrapped_footer(
        fig,
        "NOAA NCEI normals-monthly-1991-2020, Crescent City McNamara Airport (USW00024286).",
        y=0.012,
        width=112,
    )
    fig.tight_layout(rect=(0, 0.04, 1, 1))
    return save_figure(fig, "climograph", output_dir)


def plot_sea_level_scenarios(output_dir: Path, scenarios_csv: Path | None = None) -> Path:
    """Compare measured, projected, and modeled Crescent City water-level shifts."""
    csv = scenarios_csv or _DATA_DIR / "sea_level_scenarios.csv"
    df = pd.read_csv(csv)
    df = df.copy()
    for col in ("value_min_ft", "value_mid_ft", "value_max_ft"):
        df[col] = pd.to_numeric(df[col], errors="raise")

    class_colors = {
        "measured": PALETTE["blue"],
        "projection": PALETTE["cyan"],
        "scenario_projection": PALETTE["green"],
        "low_probability_high_impact": PALETTE["orange"],
        "modeled_hazard": PALETTE["red"],
    }

    fig, ax = plt.subplots(figsize=(14.8, 8.4))
    y_positions = list(range(len(df)))
    for y, row in zip(y_positions, df.itertuples(index=False)):
        color = class_colors.get(row.evidence_class, PALETTE["dark"])
        ax.plot([row.value_min_ft, row.value_max_ft], [y, y], color=color, linewidth=7, solid_capstyle="round")
        ax.scatter(row.value_mid_ft, y, s=150, color="white", edgecolor=color, linewidth=2.2, zorder=4)
        if row.value_min_ft == row.value_max_ft:
            ax.scatter(row.value_mid_ft, y, s=230, color=color, edgecolor="black", linewidth=0.8, zorder=5)
        label = f"{row.value_mid_ft:g} ft"
        if row.value_min_ft != row.value_max_ft:
            label = f"{row.value_min_ft:g}-{row.value_max_ft:g} ft; midpoint {row.value_mid_ft:g}"
        ax.text(
            row.value_max_ft + 0.16,
            y,
            label,
            va="center",
            ha="left",
            fontsize=12.2,
            color=PALETTE["dark"],
            fontweight="semibold",
        )

    ax.axvline(0, color=PALETTE["dark"], linewidth=1.2, alpha=0.8)
    ax.set_yticks(y_positions)
    ax.set_yticklabels([textwrap.fill(label, 34) for label in df["label"]], fontsize=12.6)
    ax.invert_yaxis()
    ax.set_xlabel("Relative water-level shift in feet")
    ax.set_title("Crescent City Sea-Level Scenarios: Measured, Projected, and Modeled Shifts")
    ax.set_xlim(-0.8, 7.35)
    ax.xaxis.set_major_locator(ticker.MultipleLocator(1.0))
    ax.grid(True, axis="x", alpha=0.28)
    ax.grid(False, axis="y")

    legend_lines = []
    legend_labels = []
    for evidence_class, color in class_colors.items():
        if evidence_class in set(df["evidence_class"]):
            legend_lines.append(plt.Line2D([0], [0], color=color, linewidth=6))
            legend_labels.append(evidence_class.replace("_", " "))
    ax.legend(
        legend_lines,
        legend_labels,
        loc="lower right",
        title="Evidence class",
        framealpha=0.96,
        fontsize=11.5,
        title_fontsize=12.5,
    )
    add_wrapped_footer(
        fig,
        "Data: data/sea_level_scenarios.csv. Values mix measured local relative trend, "
        "planning projections, high-end scenario stress tests, and modeled coseismic subsidence; "
        "the unknown Cascadia event is not a calendar forecast.",
        y=0.018,
        width=132,
    )
    fig.tight_layout(rect=(0, 0.065, 1, 1))
    return save_figure(fig, "sea_level_scenarios", output_dir)
