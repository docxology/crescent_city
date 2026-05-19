"""Figure-generation tests — registry contract, signatures, determinism."""

from __future__ import annotations

import hashlib
import inspect
import json
import os
import re
import subprocess
import sys
from pathlib import Path

import pytest

_PROJECT_DIR = Path(__file__).resolve().parent.parent
_REPO_ROOT = _PROJECT_DIR.parent.parent
SCRIPT_FIGURE_TIMEOUT_SECONDS = 300


def _python_for_project_scripts() -> Path:
    venv_py = _PROJECT_DIR / ".venv" / "bin" / "python"
    return venv_py if venv_py.exists() else Path(sys.executable)


class TestFigures:
    """Validate generated figures exist and are non-trivial."""

    EXPECTED = [
        "section_word_counts.png",
        "readability_metrics.png",
        "citation_density.png",
        "nested_systems_map.png",
        "population_trend.png",
        "economic_sectors.png",
        "tsunami_timeline.png",
        "disaster_impact.png",
        "tsunami_inundation_diagram.png",
        "historical_timeline.png",
        "regional_map.png",
        "tolowa_villages_map.png",
        "redwood_decline_chart.png",
        "cascadia_paleoseismology.png",
        "jefferson_map.png",
        "climograph.png",
        "harbor_timeline.png",
        "currents_timeline.png",
        "sea_level_scenarios.png",
        "smith_river_protection.png",
        "housing_pipeline.png",
        "last_chance_grade_profile.png",
        "archaeology_evidence_ladder.png",
        "rural_health_access_network.png",
    ]

    def test_figure_count(self, pipeline_artifacts, figures_dir: Path) -> None:
        pngs = sorted(figures_dir.glob("*.png"))
        assert len(pngs) == len(self.EXPECTED), f"Expected {len(self.EXPECTED)} figures, got {len(pngs)}"

    @pytest.mark.parametrize("name", EXPECTED)
    def test_figure_exists(self, pipeline_artifacts, figures_dir: Path, name: str) -> None:
        assert (figures_dir / name).exists(), f"Missing: {name}"

    @pytest.mark.parametrize("name", EXPECTED)
    def test_figure_non_trivial(self, pipeline_artifacts, figures_dir: Path, name: str) -> None:
        p = figures_dir / name
        assert p.exists(), f"Missing: {name}"
        assert p.stat().st_size > 5_000, f"Too small ({p.stat().st_size}B): {name}"

    def test_all_pngs_have_svg(self, pipeline_artifacts, figures_dir: Path) -> None:
        for png in figures_dir.glob("*.png"):
            assert png.with_suffix(".svg").exists(), f"No SVG for {png.name}"

    def test_png_svg_contract_count(self, pipeline_artifacts, figures_dir: Path) -> None:
        pngs = sorted(figures_dir.glob("*.png"))
        svgs = sorted(figures_dir.glob("*.svg"))
        assert len(pngs) == 24
        assert len(svgs) == 24
        assert {p.stem for p in pngs} == {p.stem for p in svgs}

    def test_figure_manifest_records_sources_and_hashes(self, pipeline_artifacts, figures_dir: Path) -> None:
        manifest_path = figures_dir / "figure_manifest.json"
        assert manifest_path.exists()
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        assert manifest["figure_count"] == 24
        records = manifest["figures"]
        assert [record["name"] for record in records] == [name.removesuffix(".png") for name in self.EXPECTED]
        by_name = {record["name"]: record for record in records}
        assert by_name["population_trend"]["data_inputs"] == [
            {"argument": "pop_csv", "path": "data/population_data.csv"}
        ]
        assert "current_event_chronology" in by_name["currents_timeline"]["evidence_classes"]
        assert "uscb2020census" in by_name["historical_timeline"]["source_keys"]
        assert "crescentcity_housing_update2025" in by_name["housing_pipeline"]["source_keys"]
        assert "delnorte_cha2024" in by_name["rural_health_access_network"]["source_keys"]
        provenance_fields = {
            "source_freshness",
            "source_type",
            "last_checked",
            "visual_evidence_mode",
            "reader_risk",
            "long_description",
            "provenance_notes",
        }
        for record in records:
            assert "source_keys" in record
            assert provenance_fields <= set(record), record["name"]
            assert record["source_freshness"]
            assert record["source_type"]
            assert record["last_checked"]
            assert record["visual_evidence_mode"]
            assert record["reader_risk"] in {"low", "medium", "high"}
            assert len(record["long_description"].split()) >= 18
            outputs = record["outputs"]
            assert len(outputs["png"]["sha256"]) == 64
            assert len(outputs["svg"]["sha256"]) == 64
            png_path = figures_dir / outputs["png"]["path"]
            svg_path = figures_dir / outputs["svg"]["path"]
            assert png_path.exists()
            assert svg_path.exists()
            assert hashlib.sha256(png_path.read_bytes()).hexdigest() == outputs["png"]["sha256"]
            assert hashlib.sha256(svg_path.read_bytes()).hexdigest() == outputs["svg"]["sha256"]

    def test_figure_manifest_source_keys_resolve(
        self, pipeline_artifacts, figures_dir: Path, manuscript_dir: Path
    ) -> None:
        bib = (manuscript_dir / "references.bib").read_text(encoding="utf-8")
        bib_keys = set(re.findall(r"@\w+\{([^,\s]+),", bib))
        manifest = json.loads((figures_dir / "figure_manifest.json").read_text(encoding="utf-8"))
        source_keys = {
            key
            for record in manifest["figures"]
            for key in record.get("source_keys", [])
        }
        assert source_keys
        assert source_keys <= bib_keys

    def test_manuscript_figure_captions_state_audit_contract(self, manuscript_dir: Path) -> None:
        """Every embedded figure caption should name source, evidence, limit, and claim."""
        caption_re = re.compile(r"!\[(.*?)\]\((.*?)\)\{#fig:([^}\s]+)", re.S)
        source_re = re.compile(
            r"Source basis|Data:|plotted from|drawn from|generated from|computed from|Source:",
            re.I,
        )
        limitation_re = re.compile(
            r"limitation|not a|not an|does not|rather than|not official|not final|not survey|schematic",
            re.I,
        )
        missing: list[str] = []
        captions_found = 0
        for path in sorted(manuscript_dir.glob("*.md")):
            for match in caption_re.finditer(path.read_text(encoding="utf-8")):
                captions_found += 1
                caption = " ".join(match.group(1).split())
                checks = {
                    "source": bool(source_re.search(caption)),
                    "evidence class": "evidence class" in caption.lower(),
                    "limitation": bool(limitation_re.search(caption)),
                    "interpretive claim": "interpretive claim" in caption.lower(),
                }
                failed = [name for name, passed in checks.items() if not passed]
                if failed:
                    missing.append(f"{path.name}#{match.group(3)} missing {', '.join(failed)}")

        assert captions_found == len(self.EXPECTED)
        assert not missing, "Figure caption audit contract failures: " + "; ".join(missing)

    def test_no_stray_figures_outside_figures_dir(self, pipeline_artifacts, output_dir: Path) -> None:
        """Figures must live only under ``output/figures/``."""
        stray = sorted(output_dir.glob("*.png")) + sorted(output_dir.glob("*.svg"))
        assert not stray, f"Stray figure outputs at output/ root: {[p.name for p in stray]}"


class TestSupportingModulesUnderCoverage:
    """Exercise figures module APIs."""

    def test_generate_all_figures_writes_registry_pngs(self, manuscript_dir: Path, tmp_path: Path) -> None:
        from src import figures as fig_module

        out = tmp_path / "fig_bundle"
        paths = fig_module.generate_all_figures(manuscript_dir, out)
        assert len(paths) == len(fig_module.FIGURE_REGISTRY)
        assert all(Path(p).stat().st_size > 5_000 for p in paths)
        assert (out / fig_module.FIGURE_MANIFEST_NAME).exists()
        for p in paths:
            assert Path(p).with_suffix(".svg").exists(), f"missing SVG sibling for {p}"

    def test_generate_all_figures_uses_explicit_data_dir(self, manuscript_dir: Path, tmp_path: Path) -> None:
        """A bad explicit data_dir must fail instead of silently reading project defaults."""
        from src import figures as fig_module

        with pytest.raises(FileNotFoundError):
            fig_module.generate_all_figures(manuscript_dir, tmp_path / "figs", data_dir=tmp_path / "empty_data")

    def test_registry_data_inputs_exist(self, data_dir: Path) -> None:
        from src import figures as fig_module

        missing = []
        for spec in fig_module.FIGURE_REGISTRY:
            for _arg, filename in spec.data_inputs:
                if not (data_dir / filename).exists():
                    missing.append(f"{spec.name}: {filename}")
        assert not missing, "FigureSpec data_inputs missing files: " + ", ".join(missing)

    def test_figure_registry_matches_generate_all(self) -> None:
        from src import figures as fig_module

        names = [spec.name for spec in fig_module.FIGURE_REGISTRY]
        assert len(names) == len(set(names)), "duplicate figure names in registry"
        for required in (
            "section_word_counts",
            "nested_systems_map",
            "regional_map",
            "tolowa_villages_map",
            "redwood_decline_chart",
            "tsunami_inundation_diagram",
            "cascadia_paleoseismology",
            "jefferson_map",
            "climograph",
            "harbor_timeline",
            "currents_timeline",
            "sea_level_scenarios",
            "smith_river_protection",
            "housing_pipeline",
            "last_chance_grade_profile",
            "archaeology_evidence_ladder",
            "rural_health_access_network",
        ):
            assert required in names, f"{required} missing from FIGURE_REGISTRY"

    def test_figure_registry_metadata_populated(self) -> None:
        from src import figures as fig_module

        for spec in fig_module.FIGURE_REGISTRY:
            assert spec.primary_section.startswith("sec:"), spec.name
            assert spec.evidence_classes and spec.evidence_classes != ("unspecified",), spec.name
            assert spec.source_freshness, spec.name
            assert spec.source_type, spec.name
            assert spec.last_checked, spec.name
            assert spec.visual_evidence_mode, spec.name
            assert spec.reader_risk in {"low", "medium", "high"}, spec.name
            assert len(spec.long_description.split()) >= 18, spec.name

    def test_pure_code_figures_are_deterministic(self, tmp_path: Path) -> None:
        """Pure-code (no-file-input) plotters must produce byte-identical SVG."""
        from src import figures as fig_module

        pure_code_plotters = [
            ("regional_map", fig_module.plot_regional_map),
            ("nested_systems_map", fig_module.plot_nested_systems_map),
            ("tolowa_villages_map", fig_module.plot_tolowa_villages_map),
            ("jefferson_map", fig_module.plot_jefferson_map),
        ]
        for name, plot_fn in pure_code_plotters:
            out1 = tmp_path / f"{name}_run1"
            out2 = tmp_path / f"{name}_run2"
            plot_fn(output_dir=out1)
            plot_fn(output_dir=out2)
            svg1 = (out1 / f"{name}.svg").read_bytes()
            svg2 = (out2 / f"{name}.svg").read_bytes()
            assert hashlib.sha256(svg1).hexdigest() == hashlib.sha256(svg2).hexdigest(), (
                f"{name}.svg is non-deterministic across runs"
            )

    def test_data_driven_figures_are_deterministic(self, tmp_path: Path, manuscript_dir: Path) -> None:
        """Plotters that read CSV/JSON inputs are deterministic when their
        inputs are fixed — this is the second half of the reproducibility
        contract, complementing the pure-code suite."""
        from src import figures as fig_module

        data_plotters = [
            ("population_trend", fig_module.plot_population_trend, ()),
            ("economic_sectors", fig_module.plot_economic_sectors, ()),
            ("tsunami_timeline", fig_module.plot_tsunami_timeline, ()),
            ("disaster_impact", fig_module.plot_disaster_impact, ()),
            ("tsunami_inundation_diagram", fig_module.plot_tsunami_inundation_diagram, ()),
            ("historical_timeline", fig_module.plot_historical_timeline, ()),
            ("redwood_decline_chart", fig_module.plot_redwood_decline_chart, ()),
            ("cascadia_paleoseismology", fig_module.plot_cascadia_paleoseismology, ()),
            ("climograph", fig_module.plot_climograph, ()),
            ("harbor_timeline", fig_module.plot_harbor_timeline, ()),
            ("currents_timeline", fig_module.plot_currents_timeline, ()),
            ("sea_level_scenarios", fig_module.plot_sea_level_scenarios, ()),
            ("smith_river_protection", fig_module.plot_smith_river_protection, ()),
            ("housing_pipeline", fig_module.plot_housing_pipeline, ()),
            ("last_chance_grade_profile", fig_module.plot_last_chance_grade_profile, ()),
            ("archaeology_evidence_ladder", fig_module.plot_archaeology_evidence_ladder, ()),
            ("rural_health_access_network", fig_module.plot_rural_health_access_network, ()),
        ]
        for name, plot_fn, extra in data_plotters:
            out1 = tmp_path / f"{name}_d1"
            out2 = tmp_path / f"{name}_d2"
            plot_fn(out1, *extra)
            plot_fn(out2, *extra)
            svg1 = (out1 / f"{name}.svg").read_bytes()
            svg2 = (out2 / f"{name}.svg").read_bytes()
            assert hashlib.sha256(svg1).hexdigest() == hashlib.sha256(svg2).hexdigest(), (
                f"{name}.svg is non-deterministic across two consecutive runs"
            )

    def test_manuscript_metric_figures_are_deterministic(self, tmp_path: Path, manuscript_dir: Path) -> None:
        """Three section-metric plotters reading the manuscript tree."""
        from src import figures as fig_module

        manuscript_plotters = [
            ("section_word_counts", fig_module.plot_section_word_counts),
            ("readability_metrics", fig_module.plot_readability_metrics),
            ("citation_density", fig_module.plot_citation_density),
        ]
        for name, plot_fn in manuscript_plotters:
            out1 = tmp_path / f"{name}_m1"
            out2 = tmp_path / f"{name}_m2"
            plot_fn(manuscript_dir, out1)
            plot_fn(manuscript_dir, out2)
            svg1 = (out1 / f"{name}.svg").read_bytes()
            svg2 = (out2 / f"{name}.svg").read_bytes()
            assert hashlib.sha256(svg1).hexdigest() == hashlib.sha256(svg2).hexdigest(), (
                f"{name}.svg is non-deterministic across runs"
            )

    def test_manuscript_metric_figures_exclude_folder_docs(self, manuscript_dir: Path) -> None:
        from src._figures.manuscript_metrics import _section_labels

        names = {p.name for p in _section_labels(manuscript_dir)}
        assert "README.md" not in names
        assert "AGENTS.md" not in names
        assert "SYNTAX.md" not in names

    def test_svg_preserves_key_text_for_accessibility(self, pipeline_artifacts, figures_dir: Path) -> None:
        checks = {
            "currents_timeline.svg": "Currents: Crescent City",
            "redwood_decline_chart.svg": "Old-Growth Coast Redwood",
            "tsunami_inundation_diagram.svg": "The 1964 Alaska Tsunami",
            "sea_level_scenarios.svg": "Crescent City Sea-Level Scenarios",
            "last_chance_grade_profile.svg": "Last Chance Grade",
            "rural_health_access_network.svg": "Rural Health Access Network",
            "section_word_counts.svg": "Section Word Counts by Part",
            "citation_density.svg": "Citation Density by Source Section",
            "readability_metrics.svg": "Readability by Manuscript Part",
        }
        for name, expected_text in checks.items():
            svg = (figures_dir / name).read_text(encoding="utf-8")
            assert "<text" in svg, f"{name} does not preserve SVG text nodes"
            assert expected_text in svg, f"{name} missing searchable text: {expected_text}"
        currents_svg = (figures_dir / "currents_timeline.svg").read_text(encoding="utf-8")
        assert "Source tier marker fill" in currents_svg
        assert "pending official record" in currents_svg
        tolowa_svg = (figures_dir / "tolowa_villages_map.svg").read_text(encoding="utf-8")
        assert "Tolowa Dee-ni' Public Place Relationships" in tolowa_svg
        for forbidden in ("Latitude", "Longitude", "Yontocket Cemetery", "scale bar"):
            assert forbidden not in tolowa_svg

    def test_metric_svg_preserves_part_group_labels(self, pipeline_artifacts, figures_dir: Path) -> None:
        for name in ("section_word_counts.svg", "citation_density.svg", "readability_metrics.svg"):
            svg = (figures_dir / name).read_text(encoding="utf-8")
            for label in ("Space", "Time", "People", "Ideas"):
                assert label in svg, f"{name} missing manuscript-part label {label}"

    def test_crowded_figures_have_safe_outer_margins(self, pipeline_artifacts, figures_dir: Path) -> None:
        import numpy as np
        from PIL import Image

        def nonwhite_fraction(crop: Image.Image) -> float:
            arr = np.asarray(crop.convert("RGB"))
            nonwhite = np.any(arr != 255, axis=2).sum()
            return float(nonwhite / (arr.shape[0] * arr.shape[1]))

        for name in (
            "currents_timeline.png",
            "redwood_decline_chart.png",
            "tsunami_inundation_diagram.png",
            "historical_timeline.png",
            "citation_density.png",
            "section_word_counts.png",
            "readability_metrics.png",
            "economic_sectors.png",
            "tsunami_timeline.png",
            "regional_map.png",
            "tolowa_villages_map.png",
            "jefferson_map.png",
            "sea_level_scenarios.png",
            "housing_pipeline.png",
            "last_chance_grade_profile.png",
            "archaeology_evidence_ladder.png",
            "rural_health_access_network.png",
        ):
            img = Image.open(figures_dir / name)
            width, height = img.size
            assert width >= 3000 and height >= 1800, f"{name} rendered too small: {width}x{height}"
            edge = 3
            borders = (
                img.crop((0, 0, width, edge)),
                img.crop((0, height - edge, width, height)),
                img.crop((0, 0, edge, height)),
                img.crop((width - edge, 0, width, height)),
            )
            assert max(nonwhite_fraction(border) for border in borders) < 0.02, f"{name} content is clipped at edge"

    def test_individual_plotter_signatures(self) -> None:
        from src import figures as fig_module

        for spec in fig_module.FIGURE_REGISTRY:
            sig = inspect.signature(spec.plotter)
            params = list(sig.parameters)
            if spec.needs_manuscript:
                assert params[0] == "manuscript_dir", spec.name
                assert params[1] == "output_dir", spec.name
            else:
                assert "output_dir" in params, spec.name

    def test_figures_module_invoked_as_script(self) -> None:
        exe = _python_for_project_scripts()
        env = {**os.environ, "PYTHONPATH": f"{_REPO_ROOT}{os.pathsep}{_PROJECT_DIR / 'src'}"}
        r = subprocess.run(
            [str(exe), str(_PROJECT_DIR / "src" / "figures.py")],
            cwd=str(_PROJECT_DIR),
            capture_output=True,
            text=True,
            timeout=SCRIPT_FIGURE_TIMEOUT_SECONDS,
            env=env,
        )
        assert r.returncode == 0, r.stderr[-500:]
