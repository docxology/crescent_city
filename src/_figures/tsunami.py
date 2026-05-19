"""Tsunami-event figures.

Three figures: a multi-century scatter of recorded tsunamis, a death-toll
comparison bar chart, and a schematic four-wave-sequence cross-section
for the 1964 event. The first two read from ``data/tsunami_events.csv``;
the schematic reads its four-wave factual sequence from
``data/tsunami_1964_wave_sequence.csv`` while keeping illustrative harbor
geometry in code.
"""

from __future__ import annotations

import textwrap
from pathlib import Path

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.lines import Line2D
from matplotlib.patches import Polygon, Rectangle

from ._io import save_figure
from ._style import PALETTE, add_wrapped_footer, annotate_source

_DATA_DIR = Path(__file__).resolve().parents[2] / "data"


def plot_tsunami_timeline(output_dir: Path, csv: Path | None = None) -> Path:
    """Date-vs-wave-height scatter of recorded tsunamis affecting Crescent City.

    Annotations are assigned deterministic lanes to reduce label
    collisions; categories use the project palette consistently.
    """
    csv_path = csv or _DATA_DIR / "tsunami_events.csv"
    df = pd.read_csv(csv_path)
    df["date_clean"] = pd.to_datetime(df["date"], errors="coerce")
    df = df.dropna(subset=["date_clean"]).sort_values("date_clean").reset_index(drop=True)

    fig, ax = plt.subplots(figsize=(17.5, 8.9))
    colors_map = {
        "Disaster": PALETTE["red"],
        "Geological": PALETTE["orange"],
        "Exploration": PALETTE["blue"],
        "Conflict": PALETTE["brown"],
    }
    label_plan = [
        (-26, 42),
        (26, -52),
        (0, 70),
        (-42, -76),
        (42, 28),
        (0, -34),
    ]
    label_overrides = {
        "1700_Cascadia": (-44, 42),
        "1812_Regional": (24, -56),
        "1854_Regional": (0, 52),
        "1906_SanFrancisco": (-36, -62),
        "1923_Kamchatka": (-58, 30),
        "1946_Aleutian": (-76, -18),
        "1952_Kamchatka": (-44, 62),
        "1957_Aleutian": (64, -42),
        "1960_Chile": (66, 40),
        "1964_Alaska": (-56, -66),
        "2006_Kuril": (54, 58),
        "2009_Samoa": (24, -44),
        "2010_Chile": (-52, 52),
        "2011_Tohoku": (62, -48),
        "2022_Tonga": (42, 50),
    }
    for idx, row in df.iterrows():
        cat = row["category"]
        color = colors_map.get(cat, PALETTE["gray"])
        marker = "v" if cat == "Disaster" else "o"
        size = 180 if cat == "Disaster" else 90
        ax.scatter(
            row["date_clean"],
            row["wave_height_ft"],
            s=size,
            c=color,
            marker=marker,
            zorder=3,
            edgecolors="black",
            linewidth=0.7,
        )
        offset_x, offset_y = label_overrides.get(str(row["tsunami"]).strip(), label_plan[idx % len(label_plan)])
        ax.annotate(
            textwrap.fill(str(row["tsunami"]).strip().replace("_", " "), width=14),
            (row["date_clean"], row["wave_height_ft"]),
            textcoords="offset points",
            xytext=(offset_x, offset_y),
            fontsize=10.7,
            ha="center",
            color=color,
            bbox=dict(boxstyle="round,pad=0.22", facecolor="white", edgecolor=color, alpha=0.88, linewidth=0.7),
            arrowprops=dict(arrowstyle="-", color=color, alpha=0.55, linewidth=0.7),
        )

    ax.set_xlabel("Year")
    ax.set_ylabel("Estimated peak wave height (ft above MLLW)")
    ax.set_title("Recorded Tsunamis Affecting Crescent City, 1700-2022")

    ax.xaxis.set_major_locator(mdates.YearLocator(base=50))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    ax.set_xlim(pd.Timestamp("1688-01-01"), pd.Timestamp("2035-01-01"))
    ax.set_ylim(0, df["wave_height_ft"].max() * 1.34)
    ax.grid(True, axis="y", alpha=0.30)

    legend_elements = [
        Line2D(
            [0],
            [0],
            marker="v",
            color="w",
            markerfacecolor=PALETTE["red"],
            markersize=12,
            markeredgecolor="black",
            label="Disaster (fatal / damage)",
        ),
        Line2D(
            [0],
            [0],
            marker="o",
            color="w",
            markerfacecolor=PALETTE["orange"],
            markersize=10,
            markeredgecolor="black",
            label="Geological / proxy",
        ),
        Line2D(
            [0],
            [0],
            marker="o",
            color="w",
            markerfacecolor=PALETTE["blue"],
            markersize=10,
            markeredgecolor="black",
            label="Historic report",
        ),
    ]
    ax.legend(
        handles=legend_elements,
        loc="upper center",
        bbox_to_anchor=(0.5, -0.15),
        ncol=3,
        framealpha=0.95,
        fontsize=11.5,
    )
    add_wrapped_footer(
        fig,
        "Sources: NOAA NCEI Hazard Runup DB; Atwater (2005) on 1700 orphan tsunami; "
        "Goldfinger (2012) paleoseismic correlation; Lipton (1965).",
        y=0.024,
        width=124,
        fontsize=10.1,
    )

    fig.autofmt_xdate()
    fig.tight_layout(rect=(0, 0.10, 1, 1))
    return save_figure(fig, "tsunami_timeline", output_dir)


def plot_disaster_impact(output_dir: Path, csv: Path | None = None) -> Path:
    """Documented tsunami deaths relevant to Crescent City, by where they fell.

    Every count comes from the project event catalog
    ``data/tsunami_events.csv`` — never from prose:

    * 1964 Alaska — 11, in Crescent City (the row's ``deaths`` column).
    * 1946 Aleutian — 0 on the contiguous-US west coast (the row's
      ``deaths`` column); its 159 fatalities fell in Hilo, Hawaii,
      recorded in that row's ``notes`` field, outside this figure's
      scope.
    * 2011 Tohoku — 1, at the Klamath River mouth, Del Norte County,
      recorded in the ``2011_Tohoku`` ``notes`` field (0 in Crescent
      City proper); guarded below so the constant cannot drift from its
      catalog source.

    The figure makes scope explicit so the Crescent City count (11) is
    never conflated with the 1964 event's wider contiguous-US west-coast
    total (16: 11 Crescent City + 4 Newport, Oregon + 1 Klamath) or with
    the 1946 Hawaii toll (159).
    """
    csv_path = csv or _DATA_DIR / "tsunami_events.csv"
    df = pd.read_csv(csv_path)

    def _row(event: str) -> "pd.Series[object]":
        sel = df.loc[df["tsunami"] == event]
        if sel.empty:
            raise ValueError(f"tsunami_events.csv missing required event: {event}")
        return sel.iloc[0]

    deaths_1964 = int(str(_row("1964_Alaska")["deaths"]).strip())
    deaths_1946_westcoast = int(str(_row("1946_Aleutian")["deaths"]).strip())
    notes_2011 = str(_row("2011_Tohoku")["notes"])
    if "1 death in Del Norte County" not in notes_2011:
        raise ValueError(
            "2011_Tohoku catalog note no longer documents the single "
            "Klamath-mouth death; update plot_disaster_impact"
        )
    deaths_2011_klamath = 1  # per tsunami_events.csv 2011_Tohoku `notes`

    events: tuple[tuple[str, int, str], ...] = (
        ("1946 Aleutian", deaths_1946_westcoast, "contiguous-US west coast\n(159 deaths in Hilo, Hawaii)"),
        ("2011 Tohoku", deaths_2011_klamath, "Klamath River mouth\n(0 in Crescent City)"),
        ("1964 Alaska", deaths_1964, "Crescent City"),
    )
    labels = [f"{name}\n{scope}" for name, _d, scope in events]
    values = [d for _n, d, _s in events]

    fig, ax = plt.subplots(figsize=(12.2, 6.6))
    colors = [PALETTE["blue"], PALETTE["orange"], PALETTE["red"]]
    bars = ax.barh(range(len(events)), values, color=colors, edgecolor="white", linewidth=1)
    ax.set_yticks(range(len(events)))
    ax.set_yticklabels(labels)
    ax.set_xlabel("Documented deaths within the figure's scope")
    ax.set_title("Documented Tsunami Deaths Relevant to Crescent City, by Where They Fell")
    for bar, val in zip(bars, values, strict=True):
        ax.text(
            bar.get_width() + 0.2,
            bar.get_y() + bar.get_height() / 2,
            f"{val:,}",
            va="center",
            fontsize=12,
            fontweight="semibold",
        )
    ax.set_xlim(0, max(values) + 4)
    ax.invert_yaxis()
    ax.grid(True, axis="x", alpha=0.25)
    annotate_source(
        ax,
        "Source basis: data/tsunami_events.csv (Dengler 2005; Ross 2012).",
        loc="lower right",
    )
    add_wrapped_footer(
        fig,
        "Scope is explicit: 11 is the Crescent City toll, not the 1964 event's wider "
        "contiguous-US west-coast total of 16 (11 Crescent City + 4 Newport, Oregon + 1 "
        "Klamath); the 1946 Aleutian tsunami's 159 deaths fell in Hilo, Hawaii, outside "
        "this figure's scope.",
        y=0.016,
        width=118,
        fontsize=10.0,
    )

    fig.tight_layout(rect=(0, 0.12, 1, 1))
    return save_figure(fig, "disaster_impact", output_dir)


def plot_tsunami_inundation_diagram(output_dir: Path, waves_csv: Path | None = None, **_: object) -> Path:
    """Schematic four-wave sequence of the 1964 Alaska tsunami at Crescent City.

    Data-backed wave sequence. The wave timings/elevations are stored in
    CSV with source keys; the harbor cross-section remains schematic and
    is not intended as a bathymetric model.
    """
    waves = pd.read_csv(waves_csv or _DATA_DIR / "tsunami_1964_wave_sequence.csv")
    fig, ax = plt.subplots(figsize=(16, 9))
    ax.set_xlim(0, 110)
    ax.set_ylim(-8, 24)

    ax.add_patch(Rectangle((0, 0), 110, 24, facecolor="#FAFAFA", edgecolor="none", zorder=0))
    ax.add_patch(Rectangle((0, -8), 110, 8, facecolor=PALETTE["water"], edgecolor="none", zorder=0))
    ax.axhline(0, color=PALETTE["dark"], linewidth=1.4, linestyle=":", zorder=1)
    ax.text(0.5, 0.4, "Mean Lower-Low Water (MLLW)", fontsize=12, color=PALETTE["dark"], style="italic")

    # Shoreline profile and buildings
    land_x = np.array([90, 95, 100, 105, 110])
    land_y_top = np.array([0, 3, 5, 6.5, 7])
    ax.fill_between(land_x, -8, land_y_top, color=PALETTE["land"], edgecolor=PALETTE["dark"], linewidth=1.2, zorder=2)
    # Breakwater
    bw_x = np.array([80, 82, 84, 82, 80])
    bw_y = np.array([0, 4, 0, -4, -8])
    ax.add_patch(
        Polygon(
            np.column_stack((bw_x, bw_y)),
            closed=True,
            facecolor="#888888",
            edgecolor=PALETTE["dark"],
            linewidth=1.2,
            zorder=3,
        )
    )
    ax.text(
        82,
        5.2,
        "Breakwater\n(38-metric-ton dolos units,\ninstalled 1980s)",
        fontsize=12,
        ha="center",
        color=PALETTE["dark"],
        fontweight="bold",
    )
    for x0, w, h in [(96, 3, 4), (100, 2.5, 3.5), (104, 3, 5)]:
        ax.add_patch(
            Rectangle((x0, 7), w, h, facecolor=PALETTE["brown"], edgecolor=PALETTE["dark"], linewidth=1.0, zorder=4)
        )
    ax.text(
        101,
        13,
        "Front Street commercial district\n(destroyed 1964)",
        fontsize=12,
        ha="center",
        fontweight="bold",
        color=PALETTE["red"],
    )

    # Four-wave sequence. Timings and amplitudes are data-backed; the
    # Gaussian shapes are illustrative pulses for legible comparison.
    for row in waves.itertuples(index=False):
        label = str(row.label).replace("|", "\n")
        t0 = float(row.time_position)
        amp = float(row.amplitude_m)
        color = PALETTE[str(row.color_key)]
        t = np.linspace(t0 - 10, t0 + 10, 100)
        y = amp * np.exp(-((t - t0) ** 2) / 18)
        ax.plot(t, y, color=color, linewidth=3.5, zorder=5)
        ax.fill_between(t, np.minimum(y, 0), y, color=color, alpha=0.25, zorder=3)
        ax.scatter(t0, amp, s=200, marker="o", facecolor="white", edgecolor=color, linewidth=2.5, zorder=6)
        ax.annotate(
            label,
            xy=(t0, amp),
            xytext=(t0, amp + float(row.label_y_offset)),
            ha="center",
            fontsize=12.5,
            fontweight="bold",
            color=color,
            bbox=dict(facecolor="white", edgecolor=color, boxstyle="round,pad=0.35", alpha=0.95),
            zorder=7,
        )

    ax.set_xticks([float(v) for v in waves["time_position"]])
    ax.set_xticklabels([str(v).replace("|", "\n") for v in waves["tick_label"]], fontsize=12)
    ax.set_xlabel("Time (local PST, Good Friday 1964)", fontsize=16, fontweight="bold")
    ax.set_ylabel("Water Elevation above MLLW (m)", fontsize=16, fontweight="bold")
    ax.set_title("The 1964 Alaska Tsunami at Crescent City — Four-Wave Sequence", fontsize=20, fontweight="bold")
    add_wrapped_footer(
        fig,
        "Data: data/tsunami_1964_wave_sequence.csv, derived from tide-gauge records "
        "and post-event eyewitness reconstructions (Lipton/Magoon, Dengler & Magoon, "
        "Bernardi). Earthquake: Mw 9.2 Aleutian-Alaska megathrust, 27 Mar 1964 "
        "17:36 AKST. Schematic - not to true horizontal scale.",
        y=0.018,
        width=130,
    )
    ax.grid(True, axis="y", alpha=0.25)

    fig.tight_layout(rect=(0, 0.07, 1, 1))
    return save_figure(fig, "tsunami_inundation_diagram", output_dir)
