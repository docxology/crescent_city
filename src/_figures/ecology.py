"""Ecology and river-protection figures for the Crescent City manuscript."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from ._io import save_figure
from ._style import PALETTE, add_wrapped_footer

_DATA_DIR = Path(__file__).resolve().parents[2] / "data"


def plot_smith_river_protection(output_dir: Path, protection_csv: Path | None = None) -> Path:
    """Stack Smith River Wild and Scenic corridor miles by legal designation."""
    csv = protection_csv or _DATA_DIR / "smith_river_protection.csv"
    df = pd.read_csv(csv)
    miles = df[df["unit"] == "miles"].copy()
    context = df[df["unit"] != "miles"].copy()

    order = ["wild", "scenic", "recreational"]
    colors = {"wild": PALETTE["green"], "scenic": PALETTE["cyan"], "recreational": PALETTE["blue"]}
    miles["value"] = pd.to_numeric(miles["value"], errors="raise")
    miles = miles.set_index("category").loc[order].reset_index()

    fig, ax = plt.subplots(figsize=(13.5, 7.4))
    left = 0.0
    for row in miles.itertuples(index=False):
        ax.barh(
            [0],
            [row.value],
            left=left,
            color=colors[row.category],
            edgecolor="white",
            linewidth=1.4,
            height=0.46,
            label=row.label,
        )
        ax.text(
            left + row.value / 2,
            0,
            f"{int(row.value)} mi\n{row.label.split()[0]}",
            ha="center",
            va="center",
            color="white",
            fontsize=13,
            fontweight="bold",
        )
        left += row.value

    total_miles = int(miles["value"].sum())
    watershed = context.loc[context["feature_id"] == "watershed_area", "value"].iloc[0]
    nra = context.loc[context["feature_id"] == "nra_area", "value"].iloc[0]
    ax.text(
        total_miles + 8,
        0,
        f"{total_miles} designated river miles\n{int(float(watershed))} sq mi watershed\n{int(float(nra)):,}+ acre NRA",
        va="center",
        ha="left",
        fontsize=13,
        fontweight="semibold",
        bbox=dict(facecolor="white", edgecolor=PALETTE["dark"], boxstyle="round,pad=0.4", alpha=0.95),
    )

    ax.set_xlim(0, total_miles + 130)
    ax.set_ylim(-0.65, 0.65)
    ax.set_yticks([])
    ax.set_xlabel("Designated Smith River corridor miles")
    ax.set_title("Smith River Protection: Wild, Scenic, and Recreational Miles")
    ax.legend(loc="upper center", bbox_to_anchor=(0.42, -0.05), ncol=3, framealpha=0.96)
    ax.grid(True, axis="x", alpha=0.25)
    add_wrapped_footer(
        fig,
        "Data: data/smith_river_protection.csv. Corridor miles are legal-designation counts; "
        "watershed and National Recreation Area values are context callouts, not additional river miles.",
        y=0.02,
        width=128,
    )
    fig.tight_layout(rect=(0, 0.075, 1, 1))
    return save_figure(fig, "smith_river_protection", output_dir)
