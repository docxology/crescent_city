"""Data-file schema and integrity tests."""

from __future__ import annotations

import csv
from datetime import date
import json
import re
from pathlib import Path

CURRENT_EVENT_AUDIT_DATE = date(2026, 5, 19)
CURRENT_EVENT_MAX_AUDIT_AGE_DAYS = 45
CURRENT_EVENT_SOURCE_TIERS = {
    "commercial_publication",
    "local_journalism_current_status",
    "local_journalism_pending_official_record",
    "official_plus_local_journalism",
    "official_plus_reference",
    "official_primary",
    "tribal_press_release_republished",
}
FIGURE_SOURCE_FRESHNESS = {"static", "low_change", "periodic", "current_status", "volatile"}
FIGURE_SOURCE_TYPES = {
    "conceptual_synthesis",
    "manuscript_metric",
    "mixed_public_data",
    "official_data",
    "official_project_status",
    "schematic_public_context",
    "sensitive_public_summary",
}
FIGURE_VISUAL_MODES = {
    "chart",
    "computed_metric",
    "evidence_ladder",
    "network",
    "scenario_comparison",
    "schematic_diagram",
    "schematic_map",
    "timeline",
}
FIGURE_READER_RISKS = {"low", "medium", "high"}


def _bib_keys(manuscript_dir: Path) -> set[str]:
    bib_text = (manuscript_dir / "references.bib").read_text(encoding="utf-8")
    return set(re.findall(r"@\w+\{([^,]+),", bib_text))


def _source_keys(raw: str) -> list[str]:
    return [key.strip() for key in raw.split(";") if key.strip()]


class TestDataFiles:
    """Validate every data file has the right shape and content."""

    def test_historical_events_json_valid(self, data_dir: Path) -> None:
        with open(data_dir / "historical_events.json") as f:
            data = json.load(f)
        assert isinstance(data, list)
        assert len(data) >= 20
        required = {
            "id",
            "year",
            "date_iso",
            "date_precision",
            "event",
            "category",
            "lat",
            "lon",
            "source_keys",
            "evidence_type",
            "verification_status",
            "checked_as_of",
        }
        for entry in data:
            assert required.issubset(entry.keys()), f"Missing fields: {entry}"
            assert entry["id"], entry
            assert entry["date_precision"], entry
            assert isinstance(entry["source_keys"], list) and entry["source_keys"], entry

    def test_historical_events_ids_and_sources_are_valid(self, data_dir: Path, manuscript_dir: Path) -> None:
        with open(data_dir / "historical_events.json") as f:
            data = json.load(f)
        ids = [entry["id"] for entry in data]
        assert len(ids) == len(set(ids)), "historical event IDs must be unique"

        bib_keys = _bib_keys(manuscript_dir)
        missing = sorted({key for entry in data for key in entry["source_keys"] if key not in bib_keys})
        assert not missing, f"historical event source_keys missing from references.bib: {missing}"

    def test_recent_historical_events_are_current_audited(self, data_dir: Path) -> None:
        with open(data_dir / "historical_events.json") as f:
            data = json.load(f)
        recent = [entry for entry in data if str(entry["year"]).isdigit() and int(entry["year"]) >= 2024]
        assert recent, "expected current-event rows in historical_events.json"
        for entry in recent:
            assert entry["verification_status"] == "checked_current_source", entry
            checked = date.fromisoformat(entry["checked_as_of"])
            assert checked == CURRENT_EVENT_AUDIT_DATE, entry
            assert (CURRENT_EVENT_AUDIT_DATE - checked).days <= CURRENT_EVENT_MAX_AUDIT_AGE_DAYS, entry
            assert entry["source_keys"], entry
            assert entry["source_tier"] in CURRENT_EVENT_SOURCE_TIERS, entry
            assert entry["refresh_trigger"], entry

    def test_recent_historical_events_have_precise_dates_or_scheduled_status(self, data_dir: Path) -> None:
        with open(data_dir / "historical_events.json") as f:
            data = json.load(f)
        recent = [entry for entry in data if str(entry["year"]).isdigit() and int(entry["year"]) >= 2024]
        for entry in recent:
            assert entry["date_iso"], entry
            event_date = date.fromisoformat(
                f"{entry['date_iso']}-15" if len(entry["date_iso"]) == 7 else entry["date_iso"]
            )
            if event_date > CURRENT_EVENT_AUDIT_DATE:
                assert entry["date_precision"] == "scheduled", entry
                assert entry["evidence_type"].startswith("scheduled "), entry
            else:
                assert entry["date_precision"] != "scheduled", entry

    def test_historical_events_have_no_duplicate_year_event_pairs(self, data_dir: Path) -> None:
        with open(data_dir / "historical_events.json") as f:
            data = json.load(f)
        pairs = [(str(entry["year"]), re.sub(r"\s+", " ", entry["event"].lower()).strip()) for entry in data]
        assert len(pairs) == len(set(pairs)), "duplicate historical timeline rows"

    def test_historical_events_coordinate_range(self, data_dir: Path) -> None:
        """Publishable event coordinates should fall within a regional anchor box."""
        with open(data_dir / "historical_events.json") as f:
            data = json.load(f)
        for e in data:
            if e["lat"] is None or e["lon"] is None:
                assert e["lat"] is None and e["lon"] is None, e
                continue
            assert 36.5 <= e["lat"] <= 49.0, f"Lat {e['lat']} out of range for '{e['event']}'"
            assert -128.0 <= e["lon"] <= -120.0, f"Lon {e['lon']} out of range for '{e['event']}'"

    def test_sensitive_indigenous_events_do_not_publish_coordinates(self, data_dir: Path) -> None:
        """Indigenous and massacre rows should not expose protected-location detail."""
        with open(data_dir / "historical_events.json") as f:
            data = json.load(f)
        sensitive_tags = {
            "forced_removal",
            "habitation",
            "imsa",
            "indigenous",
            "language",
            "massacre",
            "rancheria",
            "reservation",
            "settlement",
            "tolowa",
            "tribal_sovereignty",
        }
        sensitive_words = ("Achulet", "Howonquet", "IMSA", "Nee-dash", "Rancheria", "Tolowa", "Yontocket")
        sensitive_rows = [
            entry
            for entry in data
            if entry["category"] == "Indigenous"
            or sensitive_tags.intersection(entry.get("tags", []))
            or any(word in entry["event"] for word in sensitive_words)
        ]
        assert sensitive_rows, "expected sensitive Indigenous and archaeology-adjacent rows"
        for entry in sensitive_rows:
            assert entry["lat"] is None and entry["lon"] is None, entry

    def test_population_csv(self, data_dir: Path) -> None:
        with open(data_dir / "population_data.csv") as f:
            rows = list(csv.DictReader(f))
        assert len(rows) >= 10
        assert all(k in rows[0] for k in ("decade", "population_estimate"))

    def test_economic_sectors_csv(self, data_dir: Path) -> None:
        with open(data_dir / "economic_sectors.csv") as f:
            rows = list(csv.DictReader(f))
        assert len(rows) >= 4
        assert "sector" in rows[0]

    def test_tsunami_csv(self, data_dir: Path) -> None:
        with open(data_dir / "tsunami_events.csv") as f:
            rows = list(csv.DictReader(f))
        assert len(rows) >= 3
        years = [r["date"] for r in rows]
        assert any("1964" in y for y in years), "1964 tsunami missing"
        assert any("2011" in y for y in years), "2011 tsunami missing"

    def test_economic_history_csv(self, data_dir: Path) -> None:
        with open(data_dir / "economic_history.csv") as f:
            rows = list(csv.DictReader(f))
        assert len(rows) >= 10
        required = {"year", "estimate_type", "source_keys", "notes"}
        assert required <= set(rows[0])
        assert all(row["source_keys"] for row in rows)

    def test_csv_files_are_not_ragged(self, data_dir: Path) -> None:
        for path in sorted(data_dir.glob("*.csv")):
            with path.open(newline="", encoding="utf-8") as f:
                rows = list(csv.DictReader(f))
            bad = [idx for idx, row in enumerate(rows, start=2) if None in row or any(v is None for v in row.values())]
            assert not bad, f"{path.name} has ragged CSV row(s): {bad}"

    def test_csv_source_keys_exist_in_bibliography(self, data_dir: Path, manuscript_dir: Path) -> None:
        bib_keys = _bib_keys(manuscript_dir)
        missing: dict[str, list[str]] = {}
        for path in sorted(data_dir.glob("*.csv")):
            with path.open(newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                if "source_keys" not in (reader.fieldnames or []):
                    continue
                absent = sorted(
                    {key for row in reader for key in _source_keys(row["source_keys"]) if key not in bib_keys}
                )
                if absent:
                    missing[path.name] = absent
        assert not missing, f"CSV source_keys missing from references.bib: {missing}"

    def test_figure_provenance_csv_matches_registry(self, data_dir: Path) -> None:
        from src.figures import FIGURE_REGISTRY

        with (data_dir / "figure_provenance.csv").open(newline="", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))

        required = {
            "figure_name",
            "source_freshness",
            "source_type",
            "last_checked",
            "visual_evidence_mode",
            "reader_risk",
            "long_description",
            "notes",
        }
        assert rows
        assert required <= set(rows[0])

        registry_names = [spec.name for spec in FIGURE_REGISTRY]
        row_names = [row["figure_name"] for row in rows]
        assert row_names == registry_names
        assert len(row_names) == len(set(row_names))

        for row in rows:
            assert row["source_freshness"] in FIGURE_SOURCE_FRESHNESS, row
            assert row["source_type"] in FIGURE_SOURCE_TYPES, row
            assert row["visual_evidence_mode"] in FIGURE_VISUAL_MODES, row
            assert row["reader_risk"] in FIGURE_READER_RISKS, row
            if row["source_freshness"] != "static":
                assert date.fromisoformat(row["last_checked"]), row
            assert len(row["long_description"].split()) >= 18, row
            if row["source_type"] == "sensitive_public_summary":
                sensitive_text = f"{row['long_description']} {row['notes']}".lower()
                assert "coordinate" not in sensitive_text
                assert "site id" not in sensitive_text

    def test_figure_method_csv_ids_are_unique(self, data_dir: Path) -> None:
        for name in (
            "redwood_old_growth_acreage.csv",
            "redwood_conservation_milestones.csv",
            "cascadia_paleoseismic_events.csv",
            "cascadia_summary_stats.csv",
            "harbor_timeline_events.csv",
            "tsunami_1964_wave_sequence.csv",
            "sea_level_scenarios.csv",
            "smith_river_protection.csv",
            "housing_pipeline_projects.csv",
            "last_chance_grade_metrics.csv",
            "archaeology_evidence_layers.csv",
            "healthcare_access_nodes.csv",
            "healthcare_access_edges.csv",
        ):
            with (data_dir / name).open(newline="", encoding="utf-8") as f:
                rows = list(csv.DictReader(f))
            id_field = next(
                field
                for field in (
                    "event_id",
                    "point_id",
                    "stat_id",
                    "scenario_id",
                    "feature_id",
                    "project_id",
                    "metric_id",
                    "layer_id",
                    "node_id",
                    "edge_id",
                )
                if field in rows[0]
            )
            ids = [row[id_field] for row in rows]
            assert all(ids), f"{name} has blank IDs"
            assert len(ids) == len(set(ids)), f"{name} has duplicate IDs"

    def test_redwood_figure_method_data(self, data_dir: Path) -> None:
        with (data_dir / "redwood_old_growth_acreage.csv").open(newline="", encoding="utf-8") as f:
            acreage = list(csv.DictReader(f))
        assert {"point_id", "year", "acres", "evidence_type", "source_keys", "notes"} <= set(acreage[0])
        years = [int(row["year"]) for row in acreage]
        acres = [int(row["acres"]) for row in acreage]
        assert years == sorted(years)
        assert min(years) == 1850 and max(years) == 2025
        assert all(acres[i] >= acres[i + 1] for i in range(len(acres) - 1))
        assert acres[-1] == 110_000

        with (data_dir / "redwood_conservation_milestones.csv").open(newline="", encoding="utf-8") as f:
            milestones = list(csv.DictReader(f))
        assert {"event_id", "year", "label", "label_x", "label_y", "source_keys"} <= set(milestones[0])
        assert len(milestones) >= 7
        assert all(1850 <= int(row["year"]) <= 2025 for row in milestones)
        assert all(0 < float(row["label_y"]) < 2_500_000 for row in milestones)

    def test_cascadia_figure_method_data(self, data_dir: Path) -> None:
        with (data_dir / "cascadia_paleoseismic_events.csv").open(newline="", encoding="utf-8") as f:
            events = list(csv.DictReader(f))
        assert {"event_id", "label", "age_yr_bp", "segment", "source_keys", "notes"} <= set(events[0])
        assert len(events) >= 19
        assert {row["segment"] for row in events} <= {"full", "south"}
        assert all(int(row["age_yr_bp"]) > 0 for row in events)
        assert any(row["label"] == "T1" and int(row["age_yr_bp"]) == 320 for row in events)

        with (data_dir / "cascadia_summary_stats.csv").open(newline="", encoding="utf-8") as f:
            stats = list(csv.DictReader(f))
        assert {"stat_id", "sort_order", "label", "value", "source_keys", "notes"} <= set(stats[0])
        assert [int(row["sort_order"]) for row in stats] == sorted(int(row["sort_order"]) for row in stats)
        assert any("probability" in row["label"].lower() for row in stats)

    def test_harbor_timeline_figure_method_data(self, data_dir: Path) -> None:
        with (data_dir / "harbor_timeline_events.csv").open(newline="", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
        required = {"event_id", "year", "label", "category", "color_key", "source_keys", "notes"}
        assert required <= set(rows[0])
        years = [int(row["year"]) for row in rows]
        assert years == sorted(years)
        assert min(years) == 1856 and max(years) == 2024
        assert {"disaster", "breakwater", "dock", "governance"} <= {row["category"] for row in rows}

    def test_tsunami_wave_sequence_figure_method_data(self, data_dir: Path) -> None:
        with (data_dir / "tsunami_1964_wave_sequence.csv").open(newline="", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
        required = {
            "event_id",
            "label",
            "tick_label",
            "time_position",
            "amplitude_m",
            "color_key",
            "label_y_offset",
            "source_keys",
            "notes",
        }
        assert required <= set(rows[0])
        assert len(rows) == 4
        positions = [float(row["time_position"]) for row in rows]
        amplitudes = [float(row["amplitude_m"]) for row in rows]
        assert positions == sorted(positions)
        assert min(amplitudes) < 0
        assert max(amplitudes) == 6.4

    def test_currents_categories_yaml(self, data_dir: Path) -> None:
        import yaml

        path = data_dir / "currents_categories.yaml"
        assert path.exists(), "data-driven currents lanes missing"
        raw = yaml.safe_load(path.read_text(encoding="utf-8"))
        assert "lanes" in raw and isinstance(raw["lanes"], list)
        for entry in raw["lanes"]:
            assert {"key", "palette_key", "marker", "y_lane", "label"} <= set(entry)
            assert isinstance(entry["y_lane"], (int, float))

    def test_climate_normals_csv(self, data_dir: Path) -> None:
        with open(data_dir / "climate_normals_1991_2020.csv") as f:
            rows = list(csv.DictReader(f))
        assert len(rows) == 12
        required = {"month", "month_name", "tavg_f", "prcp_in", "wet_days_ge_0_01_in", "station"}
        assert required <= set(rows[0])
        assert {r["station"] for r in rows} == {"USW00024286"}

    def test_sea_level_scenarios_csv(self, data_dir: Path) -> None:
        with (data_dir / "sea_level_scenarios.csv").open(newline="", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
        required = {
            "scenario_id",
            "label",
            "year",
            "value_min_ft",
            "value_mid_ft",
            "value_max_ft",
            "evidence_class",
            "source_keys",
            "notes",
        }
        assert required <= set(rows[0])
        classes = {row["evidence_class"] for row in rows}
        assert {"measured", "projection", "scenario_projection", "modeled_hazard"} <= classes
        for row in rows:
            low, mid, high = (float(row["value_min_ft"]), float(row["value_mid_ft"]), float(row["value_max_ft"]))
            assert low <= mid <= high, row

    def test_smith_river_protection_csv(self, data_dir: Path) -> None:
        with (data_dir / "smith_river_protection.csv").open(newline="", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
        required = {"feature_id", "label", "value", "unit", "category", "evidence_class", "source_keys", "notes"}
        assert required <= set(rows[0])
        miles = [row for row in rows if row["unit"] == "miles"]
        assert sum(float(row["value"]) for row in miles) == 325
        assert {"wild", "scenic", "recreational"} <= {row["category"] for row in miles}

    def test_housing_pipeline_projects_csv(self, data_dir: Path) -> None:
        with (data_dir / "housing_pipeline_projects.csv").open(newline="", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
        required = {
            "project_id",
            "project",
            "quantity",
            "quantity_type",
            "status",
            "funding_millions",
            "evidence_class",
            "source_keys",
            "notes",
        }
        assert required <= set(rows[0])
        assert any(row["project_id"] == "battery_point_apartments" and float(row["quantity"]) == 162 for row in rows)
        assert {"planned_units", "committed_vouchers", "funding_millions"} <= {row["quantity_type"] for row in rows}

    def test_last_chance_grade_metrics_csv(self, data_dir: Path) -> None:
        with (data_dir / "last_chance_grade_metrics.csv").open(newline="", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
        required = {"metric_id", "label", "value", "unit", "display_value", "evidence_class", "source_keys", "notes"}
        assert required <= set(rows[0])
        by_id = {row["metric_id"]: row for row in rows}
        assert float(by_id["construction_cost_2026"]["value"]) == 2700
        assert float(by_id["tunnel_length"]["value"]) == 6000
        assert by_id["construction_duration"]["display_value"] == "6-8 yr"

    def test_archaeology_evidence_layers_csv_protects_site_locations(self, data_dir: Path) -> None:
        with (data_dir / "archaeology_evidence_layers.csv").open(newline="", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
        required = {
            "layer_id",
            "label",
            "year_start",
            "year_end",
            "evidence_class",
            "public_detail_level",
            "source_keys",
            "notes",
        }
        assert required <= set(rows[0])
        assert "lat" not in rows[0] and "lon" not in rows[0]
        assert any(row["evidence_class"] == "legal_protection" for row in rows)
        for row in rows:
            assert float(row["year_start"]) <= float(row["year_end"])
            assert row["public_detail_level"] != "specific_site_location"

    def test_healthcare_access_network_csvs(self, data_dir: Path) -> None:
        with (data_dir / "healthcare_access_nodes.csv").open(newline="", encoding="utf-8") as f:
            nodes = list(csv.DictReader(f))
        with (data_dir / "healthcare_access_edges.csv").open(newline="", encoding="utf-8") as f:
            edges = list(csv.DictReader(f))
        node_fields = {
            "node_id",
            "label",
            "node_type",
            "x",
            "y",
            "capacity_label",
            "evidence_class",
            "source_keys",
            "notes",
        }
        assert node_fields <= set(nodes[0])
        assert {"edge_id", "source", "target", "label", "evidence_class", "source_keys", "notes"} <= set(edges[0])
        node_ids = {row["node_id"] for row in nodes}
        assert {"sutter_coast", "open_door", "tolowa_health", "air_medical", "outside_specialty"} <= node_ids
        for node in nodes:
            assert 0 <= float(node["x"]) <= 1
            assert 0 <= float(node["y"]) <= 1
        for edge in edges:
            assert edge["source"] in node_ids, edge
            assert edge["target"] in node_ids, edge
