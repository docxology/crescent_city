"""Conceptual systems-architecture figure for the manuscript.

The plot is pure code: it translates the manuscript's organizing frame
into a reproducible diagram rather than reading an external dataset.
"""

from __future__ import annotations

import textwrap
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

from ._io import save_figure
from ._style import PALETTE, annotate_source


def _box(
    ax: plt.Axes,
    *,
    x: float,
    y: float,
    width: float,
    height: float,
    text: str,
    facecolor: str,
    edgecolor: str,
    fontsize: float = 12.0,
    weight: str = "normal",
    alpha: float = 0.96,
    wrap_width: int = 24,
) -> None:
    patch = FancyBboxPatch(
        (x, y),
        width,
        height,
        boxstyle="round,pad=0.014,rounding_size=0.018",
        facecolor=facecolor,
        edgecolor=edgecolor,
        linewidth=1.4,
        alpha=alpha,
    )
    ax.add_patch(patch)
    ax.text(
        x + width / 2,
        y + height / 2,
        textwrap.fill(text, width=wrap_width),
        ha="center",
        va="center",
        fontsize=fontsize,
        fontweight=weight,
        color=PALETTE["dark"],
        linespacing=1.15,
    )


def plot_nested_systems_map(output_dir: Path, **_: object) -> Path:
    """Draw the manuscript's Space-Time-People-Ideas organizing frame."""
    fig, ax = plt.subplots(figsize=(16, 11.5))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    columns = [
        (
            "SPACE",
            PALETTE["blue"],
            [
                "Earth system",
                "Pacific basin",
                "North America",
                "Cascadia margin",
                "Klamath-Smith watersheds",
                "Crescent City harbor and townsite",
            ],
        ),
        (
            "TIME",
            PALETTE["orange"],
            [
                "Geologic deep time",
                "Indigenous continuity",
                "Contact and conquest",
                "Industrial extraction",
                "Tsunami reconstruction",
                "Climate-adaptation present",
            ],
        ),
        (
            "PEOPLE",
            PALETTE["green"],
            [
                "Tolowa Dee-ni' Nation",
                "Yurok, Hupa, Karuk neighbors",
                "Settlers and immigrant workers",
                "Civic, tribal, state, federal institutions",
                "Fishers, loggers, nurses, teachers, visitors",
                "Press, mutual aid, families",
            ],
        ),
        (
            "IDEAS",
            PALETTE["purple"],
            [
                "World renewal and stewardship",
                "Sovereignty, termination, restoration",
                "Extraction, conservation, co-management",
                "Jefferson and rural autonomy",
                "Redwood sacredness and folklore",
                "Reproducible public evidence",
            ],
        ),
    ]

    ax.text(
        0.5,
        0.965,
        "Nested Systems of Crescent City History",
        ha="center",
        va="top",
        fontsize=20,
        fontweight="bold",
        color=PALETTE["dark"],
    )
    ax.text(
        0.5,
        0.925,
        "The manuscript preserves historical sequence, but each chapter also sits inside interacting spatial, temporal, social, and interpretive systems.",
        ha="center",
        va="top",
        fontsize=12.5,
        color="#444444",
    )

    col_width = 0.21
    gap = 0.025
    x0 = 0.045
    top = 0.84
    row_h = 0.064
    row_gap = 0.014

    for col_idx, (heading, color, levels) in enumerate(columns):
        x = x0 + col_idx * (col_width + gap)
        _box(
            ax,
            x=x,
            y=top,
            width=col_width,
            height=0.06,
            text=heading,
            facecolor=color,
            edgecolor=color,
            fontsize=15.5,
            weight="bold",
            alpha=0.18,
        )
        for row_idx, level in enumerate(levels):
            y = top - 0.08 - row_idx * (row_h + row_gap)
            _box(
                ax,
                x=x,
                y=y,
                width=col_width,
                height=row_h,
                text=level,
                facecolor="white",
                edgecolor=color,
                fontsize=11.6,
                weight="semibold" if row_idx in (0, len(levels) - 1) else "normal",
            )
            if row_idx < len(levels) - 1:
                cx = x + col_width / 2
                ax.add_patch(
                    FancyArrowPatch(
                        (cx, y - 0.004),
                        (cx, y - row_gap - 0.006),
                        arrowstyle="-|>",
                        mutation_scale=12,
                        linewidth=1.1,
                        color=color,
                        alpha=0.72,
                    )
                )

    emergence_box = (0.14, 0.055, 0.72, 0.12)
    _box(
        ax,
        x=emergence_box[0],
        y=emergence_box[1],
        width=emergence_box[2],
        height=emergence_box[3],
        text="Emergent object of study: a small coastal city whose history is produced by interactions among coast, forest, river, institutions, memory, and repeated shocks",
        facecolor="#F7F7F7",
        edgecolor=PALETTE["dark"],
        fontsize=12.4,
        weight="semibold",
        wrap_width=72,
    )

    for col_idx, (_heading, color, _levels) in enumerate(columns):
        x = x0 + col_idx * (col_width + gap) + col_width / 2
        ax.add_patch(
            FancyArrowPatch(
                (x, 0.225),
                (0.5, emergence_box[1] + emergence_box[3] + 0.01),
                arrowstyle="-|>",
                mutation_scale=18,
                linewidth=1.9,
                color=color,
                alpha=0.72,
                connectionstyle="arc3,rad=0.08",
            )
        )

    interaction_y = 0.225
    ax.add_patch(
        FancyArrowPatch(
            (0.105, interaction_y),
            (0.895, interaction_y),
            arrowstyle="<->",
            mutation_scale=18,
            linewidth=1.8,
            color=PALETTE["dark"],
            alpha=0.68,
        )
    )
    ax.text(
        0.5,
        interaction_y + 0.02,
        "feedbacks: hazard -> rebuilding -> governance -> memory -> adaptation",
        ha="center",
        va="bottom",
        fontsize=12.2,
        color=PALETTE["dark"],
        bbox=dict(facecolor="white", edgecolor="#cccccc", alpha=0.92, boxstyle="round,pad=0.25"),
    )

    annotate_source(
        ax,
        "Conceptual synthesis: hierarchy theory, CHANS, SES, and panarchy; local layers from manuscript sections.",
        loc="lower right",
    )

    fig.tight_layout()
    return save_figure(fig, "nested_systems_map", output_dir)
