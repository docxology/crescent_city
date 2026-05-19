"""Community, infrastructure, archaeology, and healthcare system figures."""

from __future__ import annotations

import textwrap
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import pandas as pd
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Patch

from ._io import save_figure
from ._style import PALETTE, add_wrapped_footer

_DATA_DIR = Path(__file__).resolve().parents[2] / "data"


def _wrap(value: object, width: int) -> str:
    return textwrap.fill(str(value), width=width)


def plot_housing_pipeline(output_dir: Path, projects_csv: Path | None = None) -> Path:
    """Horizontal quantity/status chart for Crescent City's 2024-2026 housing pipeline."""
    csv = projects_csv or _DATA_DIR / "housing_pipeline_projects.csv"
    df = pd.read_csv(csv)
    df["quantity"] = pd.to_numeric(df["quantity"], errors="raise")
    df = df.iloc[::-1].reset_index(drop=True)

    type_colors = {
        "planned_units": PALETTE["blue"],
        "committed_vouchers": PALETTE["green"],
        "funding_millions": PALETTE["orange"],
    }
    fig, ax = plt.subplots(figsize=(15.5, 8.2))
    y = range(len(df))
    colors = [type_colors.get(t, PALETTE["gray"]) for t in df["quantity_type"]]
    bars = ax.barh(y, df["quantity"], color=colors, edgecolor="white", linewidth=1.2, height=0.62)

    for bar, row in zip(bars, df.itertuples(index=False)):
        qty = int(row.quantity) if float(row.quantity).is_integer() else row.quantity
        suffix = {"planned_units": "units", "committed_vouchers": "vouchers", "funding_millions": "$M"}.get(
            row.quantity_type, row.quantity_type
        )
        label = f"{qty:g} {suffix}\n{row.status.replace('_', ' ')}"
        ax.text(
            bar.get_width() + 4,
            bar.get_y() + bar.get_height() / 2,
            label,
            va="center",
            ha="left",
            fontsize=11.8,
            color=PALETTE["dark"],
            fontweight="semibold",
        )

    ax.set_yticks(list(y))
    ax.set_yticklabels([_wrap(p, 31) for p in df["project"]], fontsize=12.5, fontweight="semibold")
    ax.set_xlabel("Quantity (bar labels identify unit type)", fontsize=13.0, fontweight="bold")
    ax.set_title("Crescent City Affordable-Housing Pipeline (2024-2026): Status and Scale")
    ax.set_xlim(0, max(df["quantity"]) * 1.55)
    ax.xaxis.set_major_locator(ticker.MaxNLocator(6))
    ax.grid(True, axis="x", alpha=0.25)
    ax.grid(False, axis="y")

    handles = [
        plt.Line2D([0], [0], color=color, linewidth=8, label=label)
        for label, color in (
            ("planned units", type_colors["planned_units"]),
            ("committed vouchers", type_colors["committed_vouchers"]),
            ("funding in millions", type_colors["funding_millions"]),
        )
    ]
    ax.legend(handles=handles, loc="lower right", framealpha=0.96, fontsize=11.5)
    add_wrapped_footer(
        fig,
        "Data: data/housing_pipeline_projects.csv. Bars deliberately mix physical units, vouchers, and funding awards; "
        "labels identify the unit type so pipeline status is not mistaken for delivered housing inventory.",
        y=0.026,
        width=136,
        fontsize=10.8,
    )
    fig.tight_layout(rect=(0, 0.105, 1, 0.98))
    return save_figure(fig, "housing_pipeline", output_dir)


def plot_last_chance_grade_profile(output_dir: Path, metrics_csv: Path | None = None) -> Path:
    """Card-style profile of Last Chance Grade risk and Alternative F metrics."""
    csv = metrics_csv or _DATA_DIR / "last_chance_grade_metrics.csv"
    df = pd.read_csv(csv)
    order = [
        "active_landslide_segment",
        "repair_cost_since_1997",
        "preferred_alternative_year",
        "tunnel_length",
        "construction_duration",
        "construction_cost_2026",
    ]
    rows = df.set_index("metric_id").loc[order].reset_index()

    fig, ax = plt.subplots(figsize=(15.5, 8.4))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    ax.text(
        0.5,
        0.95,
        "Last Chance Grade: From Chronic Repair to Tunnel Alternative",
        ha="center",
        va="top",
        fontsize=20,
        fontweight="bold",
        color=PALETTE["dark"],
    )
    ax.text(
        0.5,
        0.90,
        "Agency planning metrics are shown as measured history, official decision, or planning estimate.",
        ha="center",
        va="top",
        fontsize=12.5,
        color="#444444",
    )

    positions = [(0.06, 0.60), (0.37, 0.60), (0.68, 0.60), (0.06, 0.25), (0.37, 0.25), (0.68, 0.25)]
    class_colors = {
        "agency_project_description": PALETTE["blue"],
        "official_decision": PALETTE["green"],
        "planning_estimate": PALETTE["orange"],
    }
    for (x, y), row in zip(positions, rows.itertuples(index=False)):
        color = class_colors.get(row.evidence_class, PALETTE["gray"])
        card = FancyBboxPatch(
            (x, y),
            0.26,
            0.23,
            boxstyle="round,pad=0.018,rounding_size=0.018",
            facecolor="white",
            edgecolor=color,
            linewidth=2,
        )
        ax.add_patch(card)
        ax.text(
            x + 0.13,
            y + 0.155,
            row.display_value,
            ha="center",
            va="center",
            fontsize=24,
            fontweight="bold",
            color=color,
        )
        ax.text(
            x + 0.13, y + 0.086, _wrap(row.label, 25), ha="center", va="center", fontsize=12.5, fontweight="semibold"
        )
        ax.text(
            x + 0.13,
            y + 0.032,
            row.evidence_class.replace("_", " "),
            ha="center",
            va="center",
            fontsize=10.5,
            color="#555555",
            style="italic",
        )

    ax.add_patch(
        FancyArrowPatch((0.19, 0.56), (0.50, 0.56), arrowstyle="-|>", mutation_scale=18, lw=1.6, color=PALETTE["dark"])
    )
    ax.add_patch(
        FancyArrowPatch((0.50, 0.56), (0.81, 0.56), arrowstyle="-|>", mutation_scale=18, lw=1.6, color=PALETTE["dark"])
    )
    ax.text(
        0.5,
        0.50,
        "maintenance burden -> preferred alternative -> cost and schedule exposure",
        ha="center",
        fontsize=12.2,
        style="italic",
    )
    add_wrapped_footer(
        fig,
        "Data: data/last_chance_grade_metrics.csv. Costs and schedule are Caltrans planning estimates tied to Alternative F, not final bids.",
        y=0.025,
        width=132,
        fontsize=10.8,
    )
    fig.tight_layout(rect=(0, 0.055, 1, 1))
    return save_figure(fig, "last_chance_grade_profile", output_dir)


def plot_archaeology_evidence_ladder(output_dir: Path, layers_csv: Path | None = None) -> Path:
    """Timeline ladder of public evidence classes for the archaeology chapter."""
    csv = layers_csv or _DATA_DIR / "archaeology_evidence_layers.csv"
    df = pd.read_csv(csv)
    df["year_start"] = pd.to_numeric(df["year_start"], errors="raise")
    df["year_end"] = pd.to_numeric(df["year_end"], errors="raise")
    df = df.sort_values("year_start")

    colors = {
        "tribal_cultural_record": PALETTE["green"],
        "archaeological_material": PALETTE["brown"],
        "published_archaeology": PALETTE["blue"],
        "interpretive_method": PALETTE["cyan"],
        "legal_protection": PALETTE["purple"],
        "tribal_governance": PALETTE["orange"],
    }
    fig, ax = plt.subplots(figsize=(15.8, 8.9))
    y = range(len(df))
    for yi, row in zip(y, df.itertuples(index=False)):
        color = colors.get(row.evidence_class, PALETTE["gray"])
        ax.barh(
            yi,
            row.year_end - row.year_start,
            left=row.year_start,
            height=0.52,
            color=color,
            edgecolor="white",
            linewidth=1.2,
        )
        ax.text(
            min(row.year_end + 34, 2048),
            yi,
            row.public_detail_level.replace("_", " "),
            va="center",
            fontsize=8.0,
            color="#555555",
            bbox=dict(facecolor="white", edgecolor="none", alpha=0.78, boxstyle="round,pad=0.12"),
        )

    ax.set_yticks(list(y))
    ax.set_yticklabels([_wrap(label, 28) for label in df["label"]], fontsize=8.8, fontweight="semibold")
    ax.set_xlim(-1200, 2140)
    ax.set_ylim(-0.72, len(df) - 0.24)
    ax.set_xlabel("Approximate calendar year", fontsize=10.2, labelpad=5)
    ax.tick_params(axis="x", labelsize=10)
    ax.set_title(
        "Smith River Archaeology: Public Evidence Classes, Not Site Disclosure",
        fontsize=13.8,
        fontweight="bold",
        pad=12,
    )
    ax.grid(True, axis="x", alpha=0.25)
    ax.grid(False, axis="y")
    ax.axvline(1775, color=PALETTE["dark"], linestyle="--", linewidth=1.2, alpha=0.7)
    ax.text(
        1812,
        len(df) - 0.45,
        "1775 contact-era boundary",
        rotation=0,
        va="top",
        ha="left",
        fontsize=8.2,
        color=PALETTE["dark"],
        bbox=dict(facecolor="white", edgecolor=PALETTE["dark"], alpha=0.88, boxstyle="round,pad=0.18"),
    )
    legend_handles = [
        Patch(facecolor=color, edgecolor="white", label=label.replace("_", " "))
        for label, color in colors.items()
        if label in set(df["evidence_class"])
    ]
    ax.legend(
        handles=legend_handles,
        loc="upper left",
        bbox_to_anchor=(0.012, 0.988),
        ncol=2,
        fontsize=7.8,
        framealpha=0.95,
        title="Evidence class",
        title_fontsize=8.6,
    )
    add_wrapped_footer(
        fig,
        "Data: data/archaeology_evidence_layers.csv. The figure summarizes evidence classes and legal protections; "
        "it intentionally omits protected site coordinates and sensitive cultural-resource locations.",
        y=0.024,
        width=138,
        fontsize=9.8,
    )
    fig.tight_layout(rect=(0, 0.095, 1, 0.965))
    return save_figure(fig, "archaeology_evidence_ladder", output_dir)


def plot_rural_health_access_network(
    output_dir: Path,
    nodes_csv: Path | None = None,
    edges_csv: Path | None = None,
) -> Path:
    """Node-link diagram of Crescent City's rural health access system."""
    node_path = nodes_csv or _DATA_DIR / "healthcare_access_nodes.csv"
    edge_path = edges_csv or _DATA_DIR / "healthcare_access_edges.csv"
    nodes = pd.read_csv(node_path)
    edges = pd.read_csv(edge_path)
    nodes["x"] = pd.to_numeric(nodes["x"], errors="raise")
    nodes["y"] = pd.to_numeric(nodes["y"], errors="raise")
    layout = {
        "sutter_coast": (0.22, 0.55),
        "open_door": (0.41, 0.73),
        "tolowa_health": (0.41, 0.36),
        "hhsa": (0.62, 0.55),
        "air_medical": (0.71, 0.75),
        "outside_specialty": (0.82, 0.55),
        "community_support": (0.62, 0.23),
    }
    for node_id, (x, y) in layout.items():
        mask = nodes["node_id"] == node_id
        nodes.loc[mask, "x"] = x
        nodes.loc[mask, "y"] = y
    node_map = {row.node_id: row for row in nodes.itertuples(index=False)}

    type_colors = {
        "acute_care": PALETTE["red"],
        "primary_care": PALETTE["blue"],
        "tribal_health": PALETTE["green"],
        "county_services": PALETTE["purple"],
        "transport": PALETTE["orange"],
        "specialty_care": PALETTE["cyan"],
        "community_support": PALETTE["brown"],
    }
    fig, ax = plt.subplots(figsize=(15.5, 8.8))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 0.98)
    ax.axis("off")

    label_positions = {
        "primary_to_hospital": (0.31, 0.66, "primary referral"),
        "air_to_specialty": (0.78, 0.68, "regional specialty care"),
        "tribal_to_services": (0.52, 0.43, "benefits coordination"),
        "hhsa_to_support": (0.70, 0.38, "safety-net support"),
        "transport_constraint": (0.49, 0.60, "travel constraint"),
    }

    for edge in edges.itertuples(index=False):
        src = node_map[edge.source]
        tgt = node_map[edge.target]
        arrow = FancyArrowPatch(
            (src.x, src.y),
            (tgt.x, tgt.y),
            arrowstyle="-|>",
            mutation_scale=18,
            linewidth=1.5,
            color=PALETTE["dark"],
            alpha=0.48,
            connectionstyle="arc3,rad=0.08",
            zorder=1,
        )
        ax.add_patch(arrow)
        if edge.edge_id in label_positions:
            lx, ly, label = label_positions[edge.edge_id]
            ax.text(
                lx,
                ly,
                _wrap(label, 16),
                ha="center",
                va="center",
                fontsize=7.6,
                color="#555555",
                zorder=2,
                bbox=dict(facecolor="white", edgecolor="none", alpha=0.84, boxstyle="round,pad=0.10"),
            )

    for node in nodes.itertuples(index=False):
        color = type_colors.get(node.node_type, PALETTE["gray"])
        patch = FancyBboxPatch(
            (node.x - 0.075, node.y - 0.044),
            0.15,
            0.088,
            boxstyle="round,pad=0.012,rounding_size=0.018",
            facecolor="white",
            edgecolor=color,
            linewidth=2.2,
            zorder=4,
        )
        ax.add_patch(patch)
        ax.text(
            node.x,
            node.y + 0.014,
            _wrap(node.label, 20),
            ha="center",
            va="center",
            fontsize=8.9,
            fontweight="bold",
            zorder=5,
        )
        ax.text(
            node.x,
            node.y - 0.026,
            _wrap(node.capacity_label, 21),
            ha="center",
            va="center",
            fontsize=7.8,
            color=color,
            zorder=5,
        )

    ax.text(
        0.5,
        0.955,
        "Rural Health Access Network: Crescent City and Del Norte County",
        ha="center",
        va="top",
        fontsize=15.6,
        fontweight="bold",
        color=PALETTE["dark"],
    )
    ax.text(
        0.5,
        0.905,
        "Licensed beds are only one layer; routine care, tribal services, social services, transport, and regional referrals complete the system.",
        ha="center",
        va="top",
        fontsize=10.0,
        color="#444444",
    )
    add_wrapped_footer(
        fig,
        "Data: data/healthcare_access_nodes.csv and data/healthcare_access_edges.csv. "
        "Edges are care and service pathways, not patient-volume measurements.",
        y=0.025,
        width=136,
        fontsize=9.6,
    )
    fig.tight_layout(rect=(0, 0.055, 1, 1))
    return save_figure(fig, "rural_health_access_network", output_dir)
