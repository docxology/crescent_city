"""Population and employment figures drawn from project CSV data.

Both figures read from ``projects/crescent_city/data/``; callers can
override the CSV path for tests and isolated reproductions.
"""

from __future__ import annotations

import textwrap
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import pandas as pd

from ._io import save_figure
from ._style import DECADE_COLORS, PALETTE, add_wrapped_footer, annotate_source

_DATA_DIR = Path(__file__).resolve().parents[2] / "data"


def plot_population_trend(output_dir: Path, pop_csv: Path | None = None) -> Path:
    """Line chart of Crescent City population by historical census/estimate year.

    The shaded blue band emphasizes the official city-enumeration
    trajectory. The peak annotation marks the Census high point, which is
    driven by group-quarters enumeration rather than a simple residential
    boom.
    """
    csv = pop_csv or _DATA_DIR / "population_data.csv"
    df = pd.read_csv(csv)
    df["decade"] = pd.to_numeric(df["decade"], errors="coerce")
    df = df.dropna(subset=["decade"])
    df["decade"] = df["decade"].astype(int)

    # Drop the 1850 zero point — it represents "no American settlement yet",
    # not a measured zero population, and plotting it produces a misleading
    # ramp from the x-axis.
    plot_df = df[df["population_estimate"] > 0].copy()

    fig, ax = plt.subplots(figsize=(12.5, 6.8))
    ax.plot(
        plot_df["decade"],
        plot_df["population_estimate"],
        color=PALETTE["blue"],
        marker="o",
        linewidth=2.4,
        markersize=8,
        zorder=3,
        label="Population estimate",
    )
    ax.fill_between(plot_df["decade"], plot_df["population_estimate"], alpha=0.12, color=PALETTE["blue"])

    peak = plot_df.loc[plot_df["population_estimate"].idxmax()]
    ax.annotate(
        f"Peak\n{int(peak['population_estimate']):,} ({int(peak['decade'])})",
        xy=(peak["decade"], peak["population_estimate"]),
        xytext=(peak["decade"] + 18, peak["population_estimate"] + 850),
        arrowprops=dict(arrowstyle="->", color=PALETTE["red"], lw=1.5),
        fontsize=13,
        color=PALETTE["red"],
        fontweight="bold",
        ha="center",
    )

    ax.set_xlabel("Census or estimate year", fontsize=12.5, fontweight="bold")
    ax.set_ylabel("Population (persons)", fontsize=12.5, fontweight="bold")
    ax.set_title(
        "Crescent City Population Trend (1860–2026, Official City Enumeration)", fontsize=15, fontweight="bold"
    )
    ax.set_xticks(np.arange(1860, 2030, 20))
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f"{int(x):,}"))
    ax.set_xlim(1855, 2030)
    ax.set_ylim(0, plot_df["population_estimate"].max() * 1.25)
    ax.grid(True, axis="y", alpha=0.30)
    ax.tick_params(axis="both", labelsize=11)
    ax.legend(loc="upper right", fontsize=11)
    annotate_source(
        ax,
        "U.S. Census 1860–2020; ACS 2023; CA DOF E-5 2026. Counts include Pelican Bay group quarters.",
        loc="lower left",
    )

    fig.tight_layout()
    return save_figure(fig, "population_trend", output_dir)


def plot_economic_sectors(output_dir: Path, econ_csv: Path | None = None) -> Path:
    """Grouped bar chart of employment by sector across four decades.

    Uses the project's :data:`DECADE_COLORS` map so the four decade-colored
    bar groups follow a consistent visual encoding (1990 blue → 2020 red).
    """
    csv = econ_csv or _DATA_DIR / "economic_sectors.csv"
    df = pd.read_csv(csv)
    sectors = df["sector"].values
    decades = [1990, 2000, 2010, 2020]
    cols = [f"{d}_employment" for d in decades]

    x = np.arange(len(sectors))
    width = 0.20

    fig, ax = plt.subplots(figsize=(16.8, 8.4))
    for i, (decade, col) in enumerate(zip(decades, cols)):
        bars = ax.bar(
            x + (i - 1.5) * width,
            df[col],
            width,
            label=str(decade),
            color=DECADE_COLORS[decade],
            edgecolor="white",
            linewidth=0.6,
        )
        for bar, val in zip(bars, df[col]):
            if decade == 2020 and val > 50:
                ax.text(
                    bar.get_x() + bar.get_width() / 2,
                    bar.get_height() + 6,
                    f"{int(val):,}",
                    ha="center",
                    va="bottom",
                    fontsize=11.5,
                    rotation=0,
                    color="#333333",
                )

    gdp = pd.to_numeric(df["sector_gdp_2020_millions"], errors="coerce")
    ax2 = ax.twinx()
    ax2.scatter(
        x,
        gdp,
        color=PALETTE["dark"],
        marker="D",
        s=90,
        label="2020 sector GDP",
        zorder=5,
    )
    for x_i, val in zip(x, gdp):
        ax2.text(
            float(x_i),
            val + 2,
            f"${int(val)}M",
            ha="center",
            va="bottom",
            fontsize=11,
            color=PALETTE["dark"],
            fontweight="semibold",
        )
    ax2.set_ylabel("2020 sector GDP (millions USD)", fontsize=14, fontweight="bold", color=PALETTE["dark"])
    ax2.tick_params(axis="y", labelcolor=PALETTE["dark"], labelsize=12)
    ax2.yaxis.set_major_formatter(ticker.FuncFormatter(lambda v, _: f"${int(v):,}M"))
    ax2.set_ylim(0, max(gdp) * 1.22)
    ax2.grid(False)

    ax.set_xlabel("Economic sector", fontsize=14, fontweight="bold")
    ax.set_ylabel("Employment (estimated persons)", fontsize=14, fontweight="bold")
    ax.set_title("Crescent City: Employment by Sector and 2020 GDP Context (1990-2020)", fontsize=18, fontweight="bold")
    ax.set_xticks(x)
    ax.set_xticklabels([textwrap.fill(str(s), width=16) for s in sectors], rotation=0, ha="center", fontsize=12)
    ax.tick_params(axis="y", labelsize=12)
    ax.grid(True, axis="y", alpha=0.25)
    bars_handles, bars_labels = ax.get_legend_handles_labels()
    line_handles, line_labels = ax2.get_legend_handles_labels()
    ax.legend(
        bars_handles + line_handles,
        bars_labels + line_labels,
        title="Measure",
        loc="upper center",
        bbox_to_anchor=(0.5, 1.02),
        ncol=5,
        fontsize=12,
        title_fontsize=13,
    )
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda v, _: f"{int(v):,}"))
    add_wrapped_footer(
        fig,
        "Sources: California EDD QCEW; BLS LAUS; local 2020 sector-GDP estimates in data/economic_sectors.csv.",
        y=0.015,
        width=128,
        fontsize=11.5,
    )

    fig.tight_layout(rect=(0, 0.045, 1, 0.96))
    return save_figure(fig, "economic_sectors", output_dir)


def plot_extraction_decline(output_dir: Path, econ_history_csv: Path | None = None) -> Path:
    """Line chart of lumber and fishing employment estimates, 1880-2020.

    Reads ``data/economic_history.csv`` so the long extraction-cycle
    narrative in ``29_economic_history.md`` has a visible series instead of
    prose-only estimates. Values are historical estimates (source keys on
    each row), not official payroll series — the caption must say so.
    """
    csv = econ_history_csv or _DATA_DIR / "economic_history.csv"
    df = pd.read_csv(csv)
    df["year"] = pd.to_numeric(df["year"], errors="coerce")
    df = df.dropna(subset=["year"])
    df["year"] = df["year"].astype(int)

    fig, ax = plt.subplots(figsize=(12.5, 6.8))
    for col, label, color in (
        ("lumber_jobs_estimate", "Lumber jobs (estimate)", PALETTE["green"]),
        ("fishing_jobs_estimate", "Fishing jobs (estimate)", PALETTE["blue"]),
    ):
        series = df.dropna(subset=[col])
        ax.plot(
            series["year"],
            series[col],
            marker="o",
            linewidth=2.4,
            markersize=7,
            color=color,
            label=label,
            zorder=3,
        )

    peak = df.loc[df["lumber_jobs_estimate"].idxmax()]
    ax.annotate(
        f"Peak lumber employment\n~{int(peak['lumber_jobs_estimate']):,} ({int(peak['year'])})",
        xy=(peak["year"], peak["lumber_jobs_estimate"]),
        xytext=(peak["year"] + 14, peak["lumber_jobs_estimate"] + 120),
        arrowprops=dict(arrowstyle="->", color=PALETTE["red"], lw=1.5),
        fontsize=12,
        color="#333333",
    )
    ax.annotate(
        "2020: ~2 lumber jobs, ~60 fishing jobs\n(post-extraction maintenance economy)",
        xy=(2020, 2),
        xytext=(1952, 900),
        arrowprops=dict(arrowstyle="->", color=PALETTE["red"], lw=1.5),
        fontsize=12,
        color="#333333",
    )

    ax.set_xlabel("Year", fontsize=14, fontweight="bold")
    ax.set_ylabel("Estimated jobs", fontsize=14, fontweight="bold")
    ax.set_title("The Extraction Decline: Lumber and Fishing Employment, 1880-2020", fontsize=18, fontweight="bold")
    ax.tick_params(labelsize=12)
    ax.grid(True, alpha=0.25)
    ax.legend(fontsize=12, loc="upper right")
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda v, _: f"{int(v):,}"))
    ax.set_ylim(0, 2600)
    add_wrapped_footer(
        fig,
        "Sources: local historical estimates synthesized in data/economic_history.csv (source_keys: economic_history); not an official payroll series.",
        y=0.015,
        width=128,
        fontsize=11.5,
    )

    fig.tight_layout(rect=(0, 0.045, 1, 0.96))
    return save_figure(fig, "extraction_decline", output_dir)
