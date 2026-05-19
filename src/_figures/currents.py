"""Currents (2024–2026) figure — recent-events timeline.

Renders the verified events in ``data/historical_events.json`` for the
2024–2026 window as a category-stratified scatter, suitable for the
manuscript's current-events chapter. Reads the same canonical data file the
broader historical timeline uses, so future event additions are picked up
automatically.
"""

from __future__ import annotations

import json
from datetime import date
from pathlib import Path
from typing import Iterable

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import yaml

from ._io import save_figure
from ._style import PALETTE, add_wrapped_footer

_DATA_DIR = Path(__file__).resolve().parents[2] / "data"
_CATEGORIES_YAML = _DATA_DIR / "currents_categories.yaml"


def _fractional_year(dt: date) -> float:
    start = date(dt.year, 1, 1)
    end = date(dt.year + 1, 1, 1)
    return dt.year + ((dt - start).days / (end - start).days)


def _load_category_lanes(
    path: Path | None = None,
) -> dict[str, tuple[str, str, float, str]]:
    """Load Currents lane definitions from YAML.

    Reads ``data/currents_categories.yaml`` and returns a mapping from
    category key → ``(color, marker, y_lane, label)`` — the same shape the
    plotter consumed when the lanes were hard-coded. Centralizing the
    declaration in YAML means adding a new manuscript domain is a data
    edit, not a code change.
    """
    src = path or _CATEGORIES_YAML
    raw = yaml.safe_load(src.read_text(encoding="utf-8"))
    lanes = {}
    for entry in raw["lanes"]:
        lanes[entry["key"]] = (
            PALETTE[entry["palette_key"]],
            entry["marker"],
            float(entry["y_lane"]),
            entry["label"],
        )
    return lanes


# Loaded eagerly at import time for direct single-plot calls. The batched
# generator passes an explicit project-local YAML path so isolated project
# roots use their own data directory.
_CATEGORY_LANES = _load_category_lanes()

_EVENT_LABEL_OFFSETS: dict[str, tuple[int, int]] = {
    "2025-cdfw-sets-limited-california-ocean-salmon-recreational-season-after-2023-2024-closures": (-160, -78),
    "2025-cdfw-reports-widespread-klamath-salmon-reoccupation-one-year-after-dam-removal": (-185, -66),
    "2026-cdfw-announces-commercial-ocean-salmon-return-after-three-year-closure": (-160, -82),
    "2026-battery-point-apartments-100m-affordable-housing-project-resumes-construction-af": (178, 34),
    "2026-crescent-city-council-opens-prop-218-protest-process-for-proposed-water-and-sewe": (-150, -72),
    "2026-crescent-city-fire-rescue-opens-fire-chief-recruitment-5-may-applications-close-": (118, 52),
    "2026-pelican-bay-state-prison-homicide-investigation-opens-gabriel-otero-10-march": (-130, 46),
    "2026-maiden-lane-homicide-three-charged-after-fatal-altercation-killing-41-year-old-m": (125, -54),
    "2026-tolowa-dee-ni-nation-awarded-200-000-for-elk-habitat-restoration": (-165, 58),
    "2026-mw-4-8-offshore-gorda-plate-earthquake-89-km-wsw-of-crescent-city-9-may-no-tsuna": (10, 42),
    "2026-crescent-city-named-americas-favorite-small-towns-finalist-by-parade-magazine-an": (148, 48),
}


def _source_tier_style(source_tier: str, color: str) -> dict[str, object]:
    """Return marker fill/outline style for current-event source quality."""
    if source_tier == "official_primary":
        return {"facecolors": color, "edgecolors": "black", "linewidths": 0.85, "alpha": 1.0}
    if source_tier in {"official_plus_local_journalism", "official_plus_reference"}:
        return {"facecolors": color, "edgecolors": PALETTE["dark"], "linewidths": 1.9, "alpha": 0.96}
    if source_tier == "local_journalism_current_status":
        return {"facecolors": "white", "edgecolors": color, "linewidths": 2.15, "alpha": 0.96}
    if source_tier == "local_journalism_pending_official_record":
        return {"facecolors": "white", "edgecolors": PALETTE["red"], "linewidths": 2.4, "alpha": 0.96}
    if source_tier == "commercial_publication":
        return {"facecolors": "#F7F7F7", "edgecolors": color, "linewidths": 1.75, "alpha": 0.82}
    if source_tier == "tribal_press_release_republished":
        return {"facecolors": color, "edgecolors": PALETTE["forest"], "linewidths": 2.55, "alpha": 0.98}
    return {"facecolors": color, "edgecolors": "black", "linewidths": 0.85, "alpha": 1.0}


def _source_tier_legend_handles() -> list[Line2D]:
    """Compact legend for source-tier fill/outline semantics."""
    return [
        Line2D(
            [0],
            [0],
            linestyle="",
            marker="o",
            markersize=9,
            markerfacecolor=PALETTE["gray"],
            markeredgecolor="black",
            markeredgewidth=0.85,
            label="official primary",
        ),
        Line2D(
            [0],
            [0],
            linestyle="",
            marker="o",
            markersize=9,
            markerfacecolor=PALETTE["gray"],
            markeredgecolor=PALETTE["dark"],
            markeredgewidth=1.9,
            label="official + context",
        ),
        Line2D(
            [0],
            [0],
            linestyle="",
            marker="o",
            markersize=9,
            markerfacecolor="white",
            markeredgecolor=PALETTE["gray"],
            markeredgewidth=2.15,
            label="local journalism",
        ),
        Line2D(
            [0],
            [0],
            linestyle="",
            marker="o",
            markersize=9,
            markerfacecolor="white",
            markeredgecolor=PALETTE["red"],
            markeredgewidth=2.4,
            label="pending official record",
        ),
        Line2D(
            [0],
            [0],
            linestyle="",
            marker="o",
            markersize=9,
            markerfacecolor=PALETTE["forest"],
            markeredgecolor=PALETTE["forest"],
            markeredgewidth=2.55,
            label="tribal / commercial public status",
        ),
    ]


def _parse_year(year_field: object) -> float | None:
    """Return year as a float; handles 'c.1000BCE', '2024', None, etc."""
    if year_field is None:
        return None
    s = str(year_field)
    if "BCE" in s:
        return None
    s = s.replace("c.", "")
    try:
        return float(s)
    except ValueError:
        return None


def _event_x(event: dict) -> float | None:
    """Return fractional-year x position, preferring structured dates."""
    date_iso = event.get("date_iso")
    if isinstance(date_iso, str) and date_iso:
        try:
            # Month-level strings are stored as YYYY-MM. Treat them as mid-month
            # so current-event clusters spread by evidence date instead of year.
            if len(date_iso) == 7:
                dt = date.fromisoformat(f"{date_iso}-15")
            else:
                dt = date.fromisoformat(date_iso)
            return _fractional_year(dt)
        except ValueError:
            pass
    return _parse_year(event.get("year"))


def _filter_window(events: Iterable[dict], year_min: float, year_max: float) -> list[dict]:
    out = []
    for e in events:
        y = _event_x(e)
        if y is None:
            continue
        if year_min <= y <= year_max:
            out.append(e)
    return out


def _current_event_audit_date(events: Iterable[dict]) -> date:
    """Return the latest checked-as-of date for current-event rows.

    The project data tests require 2024+ rows to carry a current
    ``checked_as_of`` value. Reading that value here keeps the figure title,
    filter window, and footer synchronized with the data ledger.
    """
    checked_dates: list[date] = []
    for event in events:
        year = _parse_year(event.get("year"))
        if year is None or year < 2024:
            continue
        checked = event.get("checked_as_of")
        if isinstance(checked, str) and checked:
            checked_dates.append(date.fromisoformat(checked))
    if not checked_dates:
        msg = "No checked_as_of values found for current-event rows"
        raise ValueError(msg)
    return max(checked_dates)


def plot_currents_timeline(
    output_dir: Path,
    json_path: Path | None = None,
    lanes_yaml: Path | None = None,
) -> Path:
    """Plot 2024–2026 events as a domain-stratified scatter timeline."""
    json_file = json_path or _DATA_DIR / "historical_events.json"
    category_lanes = _load_category_lanes(lanes_yaml) if lanes_yaml is not None else _CATEGORY_LANES
    events = json.loads(json_file.read_text(encoding="utf-8"))
    audit_date = _current_event_audit_date(events)
    audit_label = f"{audit_date.day} {audit_date:%B %Y}"
    recent = _filter_window(events, 2024, _fractional_year(audit_date))
    # Sort by parsed year then by event text length to keep deterministic
    recent.sort(key=lambda e: (_event_x(e) or 0, e["event"][:30]))

    fig, ax = plt.subplots(figsize=(18.2, 9.6))

    # Lane background bands for visual separation
    for cat, (color, marker, y_lane, label) in category_lanes.items():
        ax.axhspan(y_lane - 0.04, y_lane + 0.04, color=color, alpha=0.05, zorder=1)
        ax.text(
            2026.88,
            y_lane,
            label,
            fontsize=13.5,
            color=color,
            va="center",
            ha="left",
            style="italic",
            fontweight="semibold",
        )

    # Plot events
    plotted_categories: set[str] = set()
    label_offsets = {
        "Environment": [(-118, -62), (118, -52)],
        "Infrastructure": [(-140, -46), (130, 36)],
        "Governance": [(-178, 44), (0, 60), (178, 44)],
        "Culture": [(-125, -40), (-125, -54), (150, 36)],
        "Conservation": [(-158, 36)],
        "Geological": [(0, 24)],
        "Conflict": [(-108, 34), (108, 34)],
    }
    label_counts: dict[str, int] = {}
    for i, e in enumerate(recent):
        cat = e.get("category", "")
        if cat not in category_lanes:
            continue
        color, marker, y_lane, label = category_lanes[cat]
        year = _event_x(e)
        if year is None:
            continue
        # Slight horizontal jitter inside the year for clarity when multiple
        # events share a year (deterministic, not random)
        same_year = [j for j, ev in enumerate(recent) if _event_x(ev) == year and ev.get("category") == cat]
        offset = 0.0
        if len(same_year) > 1:
            order = same_year.index(i)
            offset = (order - (len(same_year) - 1) / 2) * 0.055
        x = year + offset
        tier_style = _source_tier_style(str(e.get("source_tier", "")), color)
        ax.scatter(
            x,
            y_lane,
            s=210 if cat == "Geological" else 150,
            marker=marker,
            zorder=4,
            label=cat if cat not in plotted_categories else None,
            **tier_style,
        )
        plotted_categories.add(cat)
        short = e.get("label") or e["event"][:44] + ("…" if len(e["event"]) > 44 else "")
        offsets = label_offsets.get(cat, [(0, 22), (0, -28)])
        label_index = label_counts.get(cat, 0)
        label_counts[cat] = label_index + 1
        x_offset, y_offset = _EVENT_LABEL_OFFSETS.get(str(e.get("id", "")), offsets[label_index % len(offsets)])
        ax.annotate(
            short,
            (x, y_lane),
            textcoords="offset points",
            xytext=(x_offset, y_offset),
            fontsize=10.5,
            ha="center",
            color=color,
            bbox=dict(boxstyle="round,pad=0.26", facecolor="white", edgecolor=color, alpha=0.92, linewidth=0.9),
            arrowprops=dict(arrowstyle="-", color=color, alpha=0.58, linewidth=0.9),
            annotation_clip=False,
        )

    source_tier_legend = ax.legend(
        handles=_source_tier_legend_handles(),
        loc="upper center",
        bbox_to_anchor=(0.5, -0.115),
        ncol=5,
        title="Source tier marker fill / outline",
        framealpha=0.97,
        fontsize=8.8,
        title_fontsize=9.2,
        handletextpad=0.35,
        columnspacing=0.82,
        borderpad=0.42,
    )
    ax.add_artist(source_tier_legend)

    ax.set_xlim(2023.68, 2027.55)
    ax.set_ylim(-0.15, 1.15)
    ax.set_xticks([2024, 2025, 2026])
    ax.set_xticklabels(["2024", "2025", "2026"])
    ax.set_yticks([])
    ax.set_title(
        f"Currents: Crescent City and Del Norte County, 2024-{audit_label}",
        fontsize=19.2,
        fontweight="bold",
    )
    ax.grid(True, axis="x", alpha=0.25)
    for spine in ("top", "right", "left"):
        ax.spines[spine].set_visible(False)

    source_note = (
        "Sources: Caltrans, City of Crescent City, CCHD, KRRC, NOAA/CDFW, USGS, CDCR, IJPR, "
        "Redwood Voice, Wild Coast Compass, SFGATE, and ASCE. Marker fill/outline encodes source tier; "
        f"data checked {audit_label}."
    )
    add_wrapped_footer(fig, source_note, y=0.012, width=150, fontsize=10.1)

    fig.tight_layout(rect=(0, 0.105, 1, 1))
    return save_figure(fig, "currents_timeline", output_dir)
