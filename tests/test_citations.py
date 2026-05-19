"""Citation and bibliography consistency tests."""

from __future__ import annotations

import re
from pathlib import Path

import yaml


def _bib_keys(manuscript_dir: Path) -> set[str]:
    bib = (manuscript_dir / "references.bib").read_text(encoding="utf-8")
    return set(re.findall(r"@\w+\{([^,\s]+),", bib))


def _manuscript_citation_keys(manuscript_dir: Path, bib_keys: set[str]) -> set[str]:
    cited: set[str] = set()
    for path in sorted(manuscript_dir.glob("*.md")):
        if path.name.startswith("99_"):
            continue
        cited.update(
            key for key in re.findall(r"@([A-Za-z0-9_]+)", path.read_text(encoding="utf-8")) if key in bib_keys
        )
    return cited


def _reserve_keys(manuscript_dir: Path) -> set[str]:
    config = yaml.safe_load((manuscript_dir / "config.yaml").read_text(encoding="utf-8"))
    return set(config["bibliography"].get("reserve_keys", []))


class TestCitations:
    """Validate citation–bibliography consistency and density."""

    def test_bib_exists(self, manuscript_dir: Path) -> None:
        assert (manuscript_dir / "references.bib").exists()

    def test_bib_has_minimum_entries(self, manuscript_dir: Path) -> None:
        bib = (manuscript_dir / "references.bib").read_text()
        entries = re.findall(r"@\w+\{", bib)
        assert len(entries) >= 50, f"Expected >=50 bib entries, got {len(entries)}"

    def test_citation_keys_match_bib(self, manuscript_dir: Path) -> None:
        bib = (manuscript_dir / "references.bib").read_text()
        bib_keys = set(re.findall(r"@\w+\{(\w+)", bib))

        cited_keys = set()
        for f in sorted(manuscript_dir.glob("*.md")):
            if f.name.startswith("99_"):
                continue
            for m in re.findall(r"\[@(\w+)\]", f.read_text()):
                cited_keys.add(m)

        skip = {"key", "sec", "cite", "citep", "citet", "citeyear", "citation", "citation_key"}
        cited_keys -= skip

        missing = cited_keys - bib_keys
        assert not missing, f"Cited keys missing from bib: {sorted(missing)}"

    def test_citation_density_above_floor(self, manuscript_dir: Path) -> None:
        total_words = 0
        total_cites = 0
        for f in sorted(manuscript_dir.glob("*.md")):
            if f.name.startswith("99_"):
                continue
            text = f.read_text()
            words = max(len(text.split()), 1)
            cites = len(re.findall(r"\[@\w+\]", text))
            total_words += words
            total_cites += cites
        density = (total_cites / total_words) * 1000
        assert density >= 3.0, f"Density {density:.2f} below 3.0/1 000 words"

    def test_unique_citation_count(self, manuscript_dir: Path) -> None:
        keys = set()
        for f in sorted(manuscript_dir.glob("*.md")):
            if f.name.startswith("99_"):
                continue
            for m in re.findall(r"\[@(\w+)\]", f.read_text()):
                keys.add(m)
        assert len(keys) >= 40, f"Only {len(keys)} unique citation keys"

    def test_unreserved_bibliography_entries_are_cited(self, manuscript_dir: Path) -> None:
        bib_keys = _bib_keys(manuscript_dir)
        reserve_keys = _reserve_keys(manuscript_dir)
        cited_keys = _manuscript_citation_keys(manuscript_dir, bib_keys)

        unknown_reserve_keys = reserve_keys - bib_keys
        assert not unknown_reserve_keys, f"Reserve keys missing from bib: {sorted(unknown_reserve_keys)}"

        unreserved_unused = bib_keys - cited_keys - reserve_keys
        assert not unreserved_unused, "Uncited non-reserve BibTeX keys: " + ", ".join(sorted(unreserved_unused))

    def test_reserve_bibliography_audit_is_documented(self, project_root: Path, manuscript_dir: Path) -> None:
        reserve_keys = _reserve_keys(manuscript_dir)
        ledger = (project_root / "docs" / "claim_ledger.md").read_text(encoding="utf-8")

        assert "## Reserve Bibliography Audit" in ledger
        assert "Unused non-reserve entries | 0 | none" in ledger
        for key in reserve_keys:
            assert f"`{key}`" in ledger
