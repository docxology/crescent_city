"""Manuscript-structure and content tests (no pipeline run required)."""

from __future__ import annotations

import re
from pathlib import Path


class TestManuscriptStructure:
    """Validate overall manuscript structure and heading hierarchy."""

    def test_section_count(self, manuscript_dir: Path) -> None:
        """At least 45 manuscript sections (00–45+)."""
        md_files = sorted(p for p in manuscript_dir.glob("*.md") if not p.name.startswith("99_"))
        assert len(md_files) >= 45, f"Expected >=45 sections, found {len(md_files)}"

    def test_every_section_starts_with_part_or_chapter_heading(self, manuscript_dir: Path) -> None:
        """Every .md file (except 99_*) starts with H1 (parts/appendices) or H2 (chapter fragments)."""
        heading = re.compile(r"^#{1,2}\s+", re.M)
        for f in sorted(manuscript_dir.glob("*.md")):
            if f.name.startswith("99_"):
                continue
            text = f.read_text()
            first = text.lstrip().split("\n", 1)[0]
            assert heading.match(first), f"{f.name} does not start with H1 or H2: {first[:80]!r}"

    def test_no_skipped_heading_levels(self, manuscript_dir: Path) -> None:
        """No file uses H4 without H3, etc."""
        for f in sorted(manuscript_dir.glob("*.md")):
            if f.name.startswith("99_"):
                continue
            text = f.read_text()
            levels = {h.count("#") for h in re.findall(r"^(#{1,6})\s", text, re.M)}
            if not levels:
                continue
            sorted_levels = sorted(levels)
            for i in range(len(sorted_levels) - 1):
                lo, hi = sorted_levels[i], sorted_levels[i + 1]
                assert hi - lo == 1, f"{f.name} skips heading level between H{lo} and H{hi}"

    def test_abstract_exists(self, manuscript_dir: Path) -> None:
        p = manuscript_dir / "00_abstract.md"
        assert p.exists(), "00_abstract.md missing"
        text = p.read_text()
        assert "Crescent City" in text
        assert "Keywords:" in text

    def test_timeline_section_has_table(self, manuscript_dir: Path) -> None:
        p = manuscript_dir / "71_timeline.md"
        assert p.exists()
        text = p.read_text()
        assert "|" in text, "Timeline should contain a table"


class TestContent:
    """Validate substantive content in key manuscript sections."""

    def test_tsunami_section_mentions_1964(self, manuscript_dir: Path) -> None:
        sec = (manuscript_dir / "31_tsunami.md").read_text()
        assert "1964" in sec
        assert "tsunami" in sec.lower()

    def test_indigenous_names_tribe(self, manuscript_dir: Path) -> None:
        sec = (manuscript_dir / "41_indigenous.md").read_text()
        assert "Tolowa" in sec
        assert "Dee-ni'" in sec

    def test_archaeology_section(self, manuscript_dir: Path) -> None:
        sec = (manuscript_dir / "21_archaeology.md").read_text()
        assert len(sec) > 100
        assert "archaeol" in sec.lower() or "shell midden" in sec.lower()

    def test_tohoku_section(self, manuscript_dir: Path) -> None:
        sec = (manuscript_dir / "33_tohoku.md").read_text()
        assert "2011" in sec
        assert "Tōhoku" in sec or "Tohoku" in sec

    def test_wwii_section(self, manuscript_dir: Path) -> None:
        sec = (manuscript_dir / "48_world_war_ii.md").read_text()
        assert "World War" in sec or "WWII" in sec

    def test_seawall_mentions_seawall(self, manuscript_dir: Path) -> None:
        sec = (manuscript_dir / "09_seawall_engineering.md").read_text()
        assert "seawall" in sec.lower()

    def test_oil_spill_mentions_oil(self, manuscript_dir: Path) -> None:
        sec = (manuscript_dir / "08_oil_spill.md").read_text()
        assert "oil" in sec.lower()

    def test_gold_rush_mentions_gold(self, manuscript_dir: Path) -> None:
        sec = (manuscript_dir / "24_gold_rush.md").read_text()
        assert "gold" in sec.lower()

    def test_methodology_section(self, manuscript_dir: Path) -> None:
        sec = (manuscript_dir / "72_methodology.md").read_text()
        assert len(sec) > 300

    def test_reproducibility_section(self, manuscript_dir: Path) -> None:
        sec = (manuscript_dir / "73_reproducibility.md").read_text()
        assert "uv run" in sec or "reproduc" in sec.lower()

    def test_sea_level_rise_section(self, manuscript_dir: Path) -> None:
        sec = (manuscript_dir / "05_sea_level_rise.md").read_text()
        assert "sea" in sec.lower()
        assert "rise" in sec.lower()


class TestSectionAnchors:
    """Verify section anchors and cross-references are uniformly named."""

    def test_section_cross_references_resolve(self, manuscript_dir: Path) -> None:
        """Every `[@sec:X]` reference must match a `{#sec:X}` anchor."""
        cited: set[str] = set()
        defined: set[str] = set()
        for f in sorted(manuscript_dir.glob("*.md")):
            text = f.read_text(encoding="utf-8")
            cited.update(re.findall(r"\[@sec:([\w-]+)\]", text))
            defined.update(re.findall(r"\{#sec:([\w-]+)\}", text))
        missing = cited - defined
        assert not missing, f"Undefined section anchors: {sorted(missing)}"

    def test_no_anchor_drift_between_underscore_and_hyphen(self, manuscript_dir: Path) -> None:
        """If both `sec:foo_bar` and `sec:foo-bar` exist as anchors, that is drift.

        Pandoc-crossref treats them as different IDs; the manuscript
        should pick one convention. Today crescent_city has settled on
        underscores throughout (e.g. `sec:nee_dash`).
        """
        defined: set[str] = set()
        for f in sorted(manuscript_dir.glob("*.md")):
            defined.update(re.findall(r"\{#sec:([\w-]+)\}", f.read_text()))
        # Collapse to a canonical form and assert no collisions.
        norm: dict[str, set[str]] = {}
        for d in defined:
            norm.setdefault(d.replace("-", "_"), set()).add(d)
        collisions = {k: v for k, v in norm.items() if len(v) > 1}
        assert not collisions, f"Section anchors differ only in '_' vs '-': {sorted(collisions)} — pick one convention"

    def test_figure_cross_references_resolve(self, manuscript_dir: Path) -> None:
        """Every `[@fig:X]` cite must match a `{#fig:X}` attribute on an image."""
        cited: set[str] = set()
        defined: set[str] = set()
        for f in sorted(manuscript_dir.glob("*.md")):
            text = f.read_text(encoding="utf-8")
            cited.update(re.findall(r"\[@fig:([\w-]+)\]", text))
            defined.update(re.findall(r"#fig:([\w-]+)", text))
        missing = cited - defined
        assert not missing, f"Undefined figure anchors: {sorted(missing)}"

    def test_embedded_figure_captions_are_evidence_calibrated(self, manuscript_dir: Path) -> None:
        """Each embedded figure caption states source, evidence class, limitation, and claim."""
        caption_pattern = re.compile(r"!\[(.*?)\]\([^)]*?\)\{#fig:([\w-]+)[^}]*\}", re.S)
        captions: dict[str, str] = {}
        for f in sorted(manuscript_dir.glob("*.md")):
            for caption, fig_id in caption_pattern.findall(f.read_text(encoding="utf-8")):
                captions[fig_id] = " ".join(caption.lower().split())

        assert len(captions) == 24
        checks = {
            "source basis": ("source basis", "source:", "plotted from", "computed from", "drawn from", "generated from", "data/"),
            "evidence class": ("evidence class", "evidence classes"),
            "limitation": ("limitation", "not ", "does not", "omits", "approximate", "schematic", "rather than"),
            "interpretive claim": ("interpretive claim", "purpose", "shows", "supports", "therefore", "make visible"),
        }
        missing = []
        for fig_id, caption in captions.items():
            for label, needles in checks.items():
                if not any(needle in caption for needle in needles):
                    missing.append(f"{fig_id}: {label}")
        assert not missing, "Figure captions missing evidence-calibration language: " + ", ".join(missing)

    def test_figure_catalog_entries_are_evidence_calibrated(self, manuscript_dir: Path) -> None:
        """The appendix catalog must stay synchronized with the figure-caption contract."""
        text = (manuscript_dir / "A1_figure_catalogue.md").read_text(encoding="utf-8")
        blocks = re.findall(
            r"> Figure entry — `([^`]+)`(?: \(`[^`]+`\))?\n>\n(.*?)(?=\n> Figure entry — `|\n### |\n## |\Z)",
            text,
            flags=re.S,
        )
        assert len(blocks) == 24
        missing = []
        for basename, block in blocks:
            for label in (
                "*Data source*:",
                "*Evidence class*:",
                "*Source freshness*:",
                "*Reader risk*:",
                "*Long description*:",
                "*Encoding*:",
                "*Interpretive claim*:",
            ):
                if label not in block:
                    missing.append(f"{basename}: {label}")
        assert not missing, "Figure catalog entries missing fields: " + ", ".join(missing)
