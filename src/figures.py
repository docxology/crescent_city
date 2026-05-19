"""Public figure-generation API for the Crescent City project.

This module is the single entry point for every figure in the manuscript.
Implementations live in the :mod:`src._figures` subpackage, organized by
topic (manuscript metrics, demographics, tsunami, history, cartography,
conservation, geophysics, political geography, climate, ecology, harbor
history, systems, community systems, and recent events). This module:

* applies the project's shared matplotlib style (via :mod:`src._figures._style`),
* re-exports every plotting function so existing callers like
  ``from src.figures import plot_section_word_counts`` keep working,
* registers all plotters in :data:`FIGURE_REGISTRY` so the pipeline
  can iterate over them generically, and
* exposes :func:`generate_all_figures` as the single batched generator
  invoked by ``scripts/y_generate_history_figures.py`` and the test suite.

The figure suite is documented in the manuscript Appendix
(``manuscript/A1_figure_catalogue.md``) — each entry there names the
generator function and lists the data sources, so reproducing a figure
is always a one-line script call.
"""

from __future__ import annotations

import csv
import hashlib
import json
import sys
from pathlib import Path
from typing import Callable

# When invoked directly as a script (``python src/figures.py``), ``src`` is
# not yet on sys.path. Self-bootstrap so the same module file works both
# as ``import src.figures`` and as a direct script entry point — the latter
# is exercised by the project's reproducibility test suite.
if __name__ == "__main__" and __package__ in (None, ""):  # pragma: no cover
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

# Importing _style applies the shared rcParams as a side effect.
from src._figures import _style  # noqa: E402,F401  (side-effect import)
import matplotlib.pyplot as plt  # noqa: E402  (after _style sets the Agg backend)
from src._figures._io import save_figure  # noqa: E402
from src._figures._style import PALETTE  # noqa: E402
from src._figures.cartography import plot_regional_map, plot_tolowa_villages_map  # noqa: E402
from src._figures.climate import plot_climograph, plot_sea_level_scenarios  # noqa: E402
from src._figures.community_systems import (  # noqa: E402
    plot_archaeology_evidence_ladder,
    plot_housing_pipeline,
    plot_last_chance_grade_profile,
    plot_rural_health_access_network,
)
from src._figures.conservation import plot_redwood_decline_chart  # noqa: E402
from src._figures.currents import plot_currents_timeline  # noqa: E402
from src._figures.demographics import plot_economic_sectors, plot_population_trend  # noqa: E402
from src._figures.ecology import plot_smith_river_protection  # noqa: E402
from src._figures.geophysics import plot_cascadia_paleoseismology  # noqa: E402
from src._figures.harbor_history import plot_harbor_timeline  # noqa: E402
from src._figures.history import plot_historical_timeline  # noqa: E402
from src._figures.political_geography import plot_jefferson_map  # noqa: E402
from src._figures.systems import plot_nested_systems_map  # noqa: E402
from src._figures.manuscript_metrics import (  # noqa: E402
    plot_citation_density,
    plot_readability_metrics,
    plot_section_word_counts,
)
from src._figures.tsunami import (  # noqa: E402
    plot_disaster_impact,
    plot_tsunami_inundation_diagram,
    plot_tsunami_timeline,
)

DEFAULT_OUTPUT_DIR = Path(__file__).resolve().parents[1] / "output" / "figures"
"""Default output directory for figures when no override is provided."""

DEFAULT_DATA_DIR = Path(__file__).resolve().parents[1] / "data"
"""Default data directory for source-keyed figure inputs."""

FIGURE_MANIFEST_NAME = "figure_manifest.json"
"""Machine-readable provenance manifest written beside generated figures."""

FIGURE_PROVENANCE_NAME = "figure_provenance.csv"
"""Checked-in figure provenance and accessibility metadata table."""


# ── Figure type and registry ───────────────────────────────────────────
FigurePlotter = Callable[..., Path]
"""Type alias for every plotting function in the suite. All accept either
``(manuscript_dir, output_dir)`` (the three manuscript-metric plotters) or
``(output_dir, **kwargs)`` (everything else), and return the PNG path."""


class FigureSpec:
    """Lightweight registration record for a figure.

    Attributes:
        name: Short stable identifier, also used as the PNG/SVG basename.
        plotter: The function that produces the figure.
        needs_manuscript: ``True`` when the plotter needs the manuscript
            directory (the three section-metric plotters); ``False``
            otherwise.
        description: One-line summary used by the manuscript Figure
            Catalog and by :func:`generate_all_figures` print output.
        data_inputs: Optional ``(argument_name, filename)`` pairs. When
            :func:`generate_all_figures` receives ``data_dir``, these pairs
            are resolved against that directory and passed to the plotter.
        primary_section: Section anchor where the figure is primarily embedded.
        evidence_classes: Evidence types encoded by the figure.
        source_freshness: Refresh cadence or volatility class.
        source_type: Dominant source class used by the figure.
        last_checked: ISO date when the figure source basis was last audited.
        visual_evidence_mode: Visual genre used to encode the evidence.
        reader_risk: Risk that the figure could be overread without caption
            calibration.
        long_description: Accessibility-oriented description of the figure.
        provenance_notes: Short maintenance note for source refresh.
    """

    __slots__ = (
        "name",
        "plotter",
        "needs_manuscript",
        "description",
        "data_inputs",
        "primary_section",
        "evidence_classes",
        "source_freshness",
        "source_type",
        "last_checked",
        "visual_evidence_mode",
        "reader_risk",
        "long_description",
        "provenance_notes",
    )

    def __init__(
        self,
        name: str,
        plotter: FigurePlotter,
        needs_manuscript: bool,
        description: str,
        data_inputs: tuple[tuple[str, str], ...] = (),
        primary_section: str = "sec:figure_catalogue",
        evidence_classes: tuple[str, ...] = ("unspecified",),
        source_freshness: str = "",
        source_type: str = "",
        last_checked: str = "",
        visual_evidence_mode: str = "",
        reader_risk: str = "",
        long_description: str = "",
        provenance_notes: str = "",
    ) -> None:
        self.name = name
        self.plotter = plotter
        self.needs_manuscript = needs_manuscript
        self.description = description
        self.data_inputs = data_inputs
        self.primary_section = primary_section
        self.evidence_classes = evidence_classes
        self.source_freshness = source_freshness
        self.source_type = source_type
        self.last_checked = last_checked
        self.visual_evidence_mode = visual_evidence_mode
        self.reader_risk = reader_risk
        self.long_description = long_description
        self.provenance_notes = provenance_notes


FIGURE_REGISTRY: tuple[FigureSpec, ...] = (
    FigureSpec(
        "section_word_counts",
        plot_section_word_counts,
        True,
        "Bar chart of word count per manuscript section.",
        primary_section="sec:methodology",
        evidence_classes=("manuscript_metric",),
    ),
    FigureSpec(
        "readability_metrics",
        plot_readability_metrics,
        True,
        "Flesch Reading Ease and Flesch-Kincaid Grade Level per section.",
        primary_section="sec:methodology",
        evidence_classes=("manuscript_metric",),
    ),
    FigureSpec(
        "citation_density",
        plot_citation_density,
        True,
        "Citations per 1,000 words by section, with the configured floor.",
        primary_section="sec:methodology",
        evidence_classes=("manuscript_metric", "citation_audit"),
    ),
    FigureSpec(
        "nested_systems_map",
        plot_nested_systems_map,
        False,
        "Conceptual Space-Time-People-Ideas systems map.",
        primary_section="sec:introduction",
        evidence_classes=("conceptual_synthesis",),
    ),
    FigureSpec(
        "population_trend",
        plot_population_trend,
        False,
        "Crescent City population by census/estimate year, 1850-2026.",
        (("pop_csv", "population_data.csv"),),
        primary_section="sec:demographics",
        evidence_classes=("decennial_census", "acs_estimate", "dof_estimate"),
    ),
    FigureSpec(
        "economic_sectors",
        plot_economic_sectors,
        False,
        "Employment by economic sector, 1990-2020.",
        (("econ_csv", "economic_sectors.csv"),),
        primary_section="sec:economic_history",
        evidence_classes=("employment_estimate", "sector_gdp_estimate"),
    ),
    FigureSpec(
        "tsunami_timeline",
        plot_tsunami_timeline,
        False,
        "Recorded tsunamis affecting Crescent City, 1700-2022.",
        (("csv", "tsunami_events.csv"),),
        primary_section="sec:tsunami",
        evidence_classes=("measured", "historical_report", "geological_proxy"),
    ),
    FigureSpec(
        "disaster_impact",
        plot_disaster_impact,
        False,
        "Death-toll comparison across major tsunami events.",
        (("csv", "tsunami_events.csv"),),
        primary_section="sec:tsunami",
        evidence_classes=("reported_fatality_count",),
    ),
    FigureSpec(
        "tsunami_inundation_diagram",
        plot_tsunami_inundation_diagram,
        False,
        "Schematic four-wave sequence of the 1964 Alaska tsunami.",
        (("waves_csv", "tsunami_1964_wave_sequence.csv"),),
        primary_section="sec:tsunami",
        evidence_classes=("schematic", "reconstructed_wave_sequence"),
    ),
    FigureSpec(
        "historical_timeline",
        plot_historical_timeline,
        False,
        "Two-century Gantt-style chronology of dated events.",
        (("json_path", "historical_events.json"),),
        primary_section="sec:timeline",
        evidence_classes=("chronology", "mixed_evidence"),
    ),
    FigureSpec(
        "regional_map",
        plot_regional_map,
        False,
        "Stylized Del Norte County reference map.",
        primary_section="sec:environment",
        evidence_classes=("schematic_cartography",),
    ),
    FigureSpec(
        "tolowa_villages_map",
        plot_tolowa_villages_map,
        False,
        "Non-coordinate Tolowa Dee-ni' public place-relationship schematic.",
        primary_section="sec:indigenous",
        evidence_classes=("non_coordinate_schematic", "tribal_ethnographic_record"),
    ),
    FigureSpec(
        "redwood_decline_chart",
        plot_redwood_decline_chart,
        False,
        "Old-growth coast-redwood acreage decline, 1850-2025.",
        (
            ("acreage_csv", "redwood_old_growth_acreage.csv"),
            ("milestones_csv", "redwood_conservation_milestones.csv"),
        ),
        primary_section="sec:redwood_parks",
        evidence_classes=("cited_estimate", "conservation_chronology"),
    ),
    FigureSpec(
        "cascadia_paleoseismology",
        plot_cascadia_paleoseismology,
        False,
        "10,000-year Cascadia paleoseismic event chronology (Goldfinger 2012).",
        (
            ("events_csv", "cascadia_paleoseismic_events.csv"),
            ("stats_csv", "cascadia_summary_stats.csv"),
        ),
        primary_section="sec:cascadia",
        evidence_classes=("paleoseismic_reconstruction", "model_summary"),
    ),
    FigureSpec(
        "jefferson_map",
        plot_jefferson_map,
        False,
        "Proposed State of Jefferson territory and participating counties.",
        primary_section="sec:jefferson",
        evidence_classes=("schematic_political_geography",),
    ),
    FigureSpec(
        "climograph",
        plot_climograph,
        False,
        "Crescent City monthly temperature, precipitation, and wet-day normals.",
        (("climate_csv", "climate_normals_1991_2020.csv"),),
        primary_section="sec:environment",
        evidence_classes=("station_normal",),
    ),
    FigureSpec(
        "harbor_timeline",
        plot_harbor_timeline,
        False,
        "Crescent City harbor engineering and disaster timeline, 1856-2024.",
        (("events_csv", "harbor_timeline_events.csv"),),
        primary_section="sec:seawall_engineering",
        evidence_classes=("engineering_chronology",),
    ),
    FigureSpec(
        "currents_timeline",
        plot_currents_timeline,
        False,
        "Currents: domain-stratified scatter of 2024–2026 Crescent City events.",
        (
            ("json_path", "historical_events.json"),
            ("lanes_yaml", "currents_categories.yaml"),
        ),
        primary_section="sec:currents",
        evidence_classes=("current_event_chronology", "verified_public_record"),
    ),
    FigureSpec(
        "sea_level_scenarios",
        plot_sea_level_scenarios,
        False,
        "Measured, projected, and modeled Crescent City sea-level scenarios.",
        (("scenarios_csv", "sea_level_scenarios.csv"),),
        primary_section="sec:sea_level_rise",
        evidence_classes=("measured", "projection", "modeled_hazard"),
    ),
    FigureSpec(
        "smith_river_protection",
        plot_smith_river_protection,
        False,
        "Smith River Wild and Scenic designation miles plus watershed context.",
        (("protection_csv", "smith_river_protection.csv"),),
        primary_section="sec:smith_river_ecology",
        evidence_classes=("legal_designation", "cited_estimate"),
    ),
    FigureSpec(
        "housing_pipeline",
        plot_housing_pipeline,
        False,
        "Crescent City 2024-2026 affordable-housing pipeline quantities and status.",
        (("projects_csv", "housing_pipeline_projects.csv"),),
        primary_section="sec:housing",
        evidence_classes=("official_project_status",),
    ),
    FigureSpec(
        "last_chance_grade_profile",
        plot_last_chance_grade_profile,
        False,
        "Last Chance Grade repair burden and Alternative F planning metrics.",
        (("metrics_csv", "last_chance_grade_metrics.csv"),),
        primary_section="sec:transportation",
        evidence_classes=("agency_project_description", "planning_estimate"),
    ),
    FigureSpec(
        "archaeology_evidence_ladder",
        plot_archaeology_evidence_ladder,
        False,
        "Public evidence classes for Smith River archaeology without site disclosure.",
        (("layers_csv", "archaeology_evidence_layers.csv"),),
        primary_section="sec:archaeology",
        evidence_classes=("archaeological_material", "tribal_cultural_record", "legal_protection"),
    ),
    FigureSpec(
        "rural_health_access_network",
        plot_rural_health_access_network,
        False,
        "Rural healthcare, transfer, and social-service access network.",
        (
            ("nodes_csv", "healthcare_access_nodes.csv"),
            ("edges_csv", "healthcare_access_edges.csv"),
        ),
        primary_section="sec:healthcare",
        evidence_classes=("service_network", "licensed_capacity", "care_pathway"),
    ),
)
"""Canonical, ordered registry of every figure in the suite.

Iteration order is the order in which :func:`generate_all_figures`
produces files and the order the manuscript Appendix documents them.
Adding a figure means adding one :class:`FigureSpec` entry here plus
the plot function in the appropriate ``_figures/`` submodule.
"""


_PROVENANCE_FIELDS = (
    "source_freshness",
    "source_type",
    "last_checked",
    "visual_evidence_mode",
    "reader_risk",
    "long_description",
    "provenance_notes",
)


def _read_figure_provenance(path: Path) -> dict[str, dict[str, str]]:
    """Read checked-in figure provenance metadata keyed by figure name."""
    if not path.exists():
        return {}
    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return {
            row["figure_name"]: {
                "source_freshness": row.get("source_freshness", ""),
                "source_type": row.get("source_type", ""),
                "last_checked": row.get("last_checked", ""),
                "visual_evidence_mode": row.get("visual_evidence_mode", ""),
                "reader_risk": row.get("reader_risk", ""),
                "long_description": row.get("long_description", ""),
                "provenance_notes": row.get("notes", ""),
            }
            for row in reader
        }


def _apply_figure_provenance(
    registry: tuple[FigureSpec, ...],
    provenance_path: Path = DEFAULT_DATA_DIR / FIGURE_PROVENANCE_NAME,
) -> None:
    """Populate registry records from the checked-in provenance table."""
    provenance = _read_figure_provenance(provenance_path)
    if not provenance:
        return
    for spec in registry:
        row = provenance.get(spec.name, {})
        for field in _PROVENANCE_FIELDS:
            setattr(spec, field, row.get(field, ""))


_apply_figure_provenance(FIGURE_REGISTRY)


def _sha256(path: Path) -> str:
    """Return the SHA-256 hex digest for a generated artifact."""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _split_source_keys(raw: object) -> set[str]:
    """Normalize semicolon-separated or list-style source-key fields."""
    if isinstance(raw, list):
        return {str(key).strip() for key in raw if str(key).strip()}
    if isinstance(raw, str):
        return {key.strip() for key in raw.split(";") if key.strip()}
    return set()


def _source_keys_for_file(path: Path) -> set[str]:
    """Extract BibTeX source keys declared by a data input file."""
    if not path.exists():
        return set()
    if path.suffix == ".csv":
        with path.open(newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            if "source_keys" not in (reader.fieldnames or []):
                return set()
            return {key for row in reader for key in _split_source_keys(row.get("source_keys", ""))}
    if path.suffix == ".json":
        raw = json.loads(path.read_text(encoding="utf-8"))
        rows = raw if isinstance(raw, list) else raw.values() if isinstance(raw, dict) else []
        return {
            key
            for row in rows
            if isinstance(row, dict)
            for key in _split_source_keys(row.get("source_keys", ""))
        }
    return set()


def _manifest_record(spec: FigureSpec, png_path: Path, data_dir: Path) -> dict[str, object]:
    """Build a stable manifest record for one generated figure."""
    svg_path = png_path.with_suffix(".svg")
    source_keys = sorted(
        {
            key
            for _arg, filename in spec.data_inputs
            for key in _source_keys_for_file(data_dir / filename)
        }
    )
    return {
        "name": spec.name,
        "description": spec.description,
        "primary_section": spec.primary_section,
        "evidence_classes": list(spec.evidence_classes),
        "source_freshness": spec.source_freshness,
        "source_type": spec.source_type,
        "last_checked": spec.last_checked,
        "visual_evidence_mode": spec.visual_evidence_mode,
        "reader_risk": spec.reader_risk,
        "long_description": spec.long_description,
        "provenance_notes": spec.provenance_notes,
        "source_keys": source_keys,
        "data_inputs": [
            {
                "argument": arg,
                "path": str((data_dir / filename).relative_to(data_dir.parent)),
            }
            for arg, filename in spec.data_inputs
        ],
        "outputs": {
            "png": {
                "path": png_path.name,
                "sha256": _sha256(png_path),
            },
            "svg": {
                "path": svg_path.name,
                "sha256": _sha256(svg_path),
            },
        },
    }


def write_figure_manifest(
    generated_pngs: list[str],
    output_dir: Path,
    data_dir: Path,
    manifest_name: str = FIGURE_MANIFEST_NAME,
) -> Path:
    """Write figure provenance and output checksums beside the figures.

    The manifest is deterministic and intentionally excludes timestamps.
    It gives reviewers a compact way to connect each rendered artifact to
    its registry metadata, evidence classes, declared data inputs, and
    byte-level output hashes.
    """
    records = [
        _manifest_record(spec, Path(png_path), data_dir)
        for spec, png_path in zip(FIGURE_REGISTRY, generated_pngs, strict=True)
    ]
    manifest = {
        "figure_count": len(records),
        "figures": records,
    }
    out = output_dir / manifest_name
    out.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    return out


def generate_all_figures(
    manuscript_dir: Path | None = None,
    output_dir: Path | None = None,
    data_dir: Path | None = None,
) -> list[str]:
    """Render every figure in :data:`FIGURE_REGISTRY` to ``output_dir``.

    Iterates the registry, dispatching ``needs_manuscript`` plotters with
    ``(manuscript_dir, output_dir)`` and the remainder with
    ``output_dir`` plus default kwargs. Prints the progress for each
    figure to stdout so callers using the script-orchestrator pattern
    can collect a build manifest by tailing the script output.

    Args:
        manuscript_dir: Override for the manuscript directory. Defaults
            to ``<project>/manuscript``.
        output_dir: Override for the figure output directory. Defaults
            to :data:`DEFAULT_OUTPUT_DIR` (``<project>/output/figures``).
        data_dir: Override for tabular / JSON figure inputs. Defaults
            to ``<project>/data``.

    Returns:
        List of PNG paths (one per figure, in registry order), encoded
        as strings for script manifest collection.
    """
    ms = manuscript_dir or (Path(__file__).resolve().parents[1] / "manuscript")
    out = output_dir or DEFAULT_OUTPUT_DIR
    data = data_dir or DEFAULT_DATA_DIR
    _apply_figure_provenance(FIGURE_REGISTRY, data / FIGURE_PROVENANCE_NAME)
    out.mkdir(parents=True, exist_ok=True)

    pngs: list[str] = []
    print(f"  Generating {len(FIGURE_REGISTRY)} figure(s) ...")
    for spec in FIGURE_REGISTRY:
        # Determinism: reset matplotlib global state to the pinned _style
        # baseline before every plotter so no preceding figure's rcParam or
        # pyplot-state mutation can perturb a later figure's text layout.
        # (Sub-pixel inter-figure leakage is observable only in the full
        # 24-figure pass, not in the per-plotter isolation tests; this is
        # the choke-point fix. Semantics-preserving: it only re-asserts the
        # same baseline _style already establishes at import.)
        plt.close("all")
        _style.apply()
        kwargs = {arg: data / filename for arg, filename in spec.data_inputs}
        if spec.needs_manuscript:
            p = spec.plotter(ms, out, **kwargs)
        else:
            p = spec.plotter(out, **kwargs)
        pngs.append(str(p))
        print(f"    -> {Path(p).name}  ({spec.description})")
    manifest_path = write_figure_manifest(pngs, out, data)
    print(f"  {len(pngs)} figure(s) generated.\n")
    print(f"  Figure manifest written to {manifest_path}\n")
    return pngs


__all__ = [
    "DEFAULT_DATA_DIR",
    "DEFAULT_OUTPUT_DIR",
    "FIGURE_MANIFEST_NAME",
    "FIGURE_PROVENANCE_NAME",
    "FIGURE_REGISTRY",
    "FigurePlotter",
    "FigureSpec",
    "PALETTE",
    "generate_all_figures",
    "plot_cascadia_paleoseismology",
    "plot_citation_density",
    "plot_climograph",
    "plot_archaeology_evidence_ladder",
    "plot_disaster_impact",
    "plot_economic_sectors",
    "plot_harbor_timeline",
    "plot_historical_timeline",
    "plot_housing_pipeline",
    "plot_jefferson_map",
    "plot_last_chance_grade_profile",
    "plot_nested_systems_map",
    "plot_population_trend",
    "plot_readability_metrics",
    "plot_redwood_decline_chart",
    "plot_regional_map",
    "plot_rural_health_access_network",
    "plot_sea_level_scenarios",
    "plot_section_word_counts",
    "plot_smith_river_protection",
    "plot_tolowa_villages_map",
    "plot_tsunami_inundation_diagram",
    "plot_tsunami_timeline",
    "save_figure",
    "write_figure_manifest",
]


if __name__ == "__main__":
    generate_all_figures()
