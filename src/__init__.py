"""crescent_city — domain logic for Crescent City history.

All business logic for the project lives here; scripts/ are thin
orchestrators.

* :mod:`src.config` — typed YAML loader.
* :mod:`src.pipeline` — pure orchestration: read manuscript, run prose
  analysis, validate citation keys against the bibliography, write the
  prose report.
* :mod:`src.figures` — matplotlib renderers for the readability
  dashboard, per-section word counts, citation density, systems map,
  population trends, economic sectors, tsunami timeline, disaster impact,
  and historical timeline.
* :mod:`src.manuscript_variables` — substitution variables for the
  abstract.
* :mod:`src.report` — assembles the final review report (markdown).
"""

from __future__ import annotations

from .config import ProjectConfig, load_project_config
from .figures import (
    generate_all_figures,
    plot_citation_density,
    plot_disaster_impact,
    plot_economic_sectors,
    plot_historical_timeline,
    plot_nested_systems_map,
    plot_population_trend,
    plot_readability_metrics,
    plot_section_word_counts,
    plot_tsunami_timeline,
)
from .manuscript_variables import (
    ManuscriptVariables,
    compute_variables,
    substitute_in_text,
    write_variables,
)
from .pipeline import CheckResult, run_pipeline
from .report import write_review_report

__all__ = [
    # Config
    "ProjectConfig",
    "load_project_config",
    # Pipeline
    "CheckResult",
    "run_pipeline",
    # Figures
    "generate_all_figures",
    "plot_section_word_counts",
    "plot_readability_metrics",
    "plot_citation_density",
    "plot_population_trend",
    "plot_economic_sectors",
    "plot_tsunami_timeline",
    "plot_disaster_impact",
    "plot_historical_timeline",
    "plot_nested_systems_map",
    # Manuscript variables
    "ManuscriptVariables",
    "compute_variables",
    "substitute_in_text",
    "write_variables",
    # Report
    "write_review_report",
]
