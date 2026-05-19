"""Tests for src.publishing — CITATION.cff / zenodo_metadata / self-citation BibTeX."""

from __future__ import annotations

import json
from pathlib import Path

import yaml


def _sample_config() -> dict:
    return {
        "paper": {
            "title": "Sample Manuscript",
            "subtitle": "A test abstract",
            "version": "0.9.1",
        },
        "publication": {
            "doi": "10.5281/zenodo.000001",
            "year": 2025,
            "repository_url": "https://github.com/docxology/crescent_city",
        },
        "authors": [
            {
                "name": "Ada Lovelace",
                "orcid": "0000-0000-0000-0001",
                "email": "ada@example.com",
                "affiliation": "Analytical Engine",
                "corresponding": True,
            },
            {"name": "Charles Babbage"},
        ],
        "keywords": ["history", "computing"],
        "metadata": {
            "license": "CC-BY-4.0",
            "code_license": "Apache-2.0",
            "data_license": "public-domain-and-open-data-by-source",
            "language": "en",
        },
    }


def test_write_citation_cff_round_trip(tmp_path: Path) -> None:
    from src.publishing import write_citation_cff

    target = tmp_path / "CITATION.cff"
    write_citation_cff(_sample_config(), target)
    parsed = yaml.safe_load(target.read_text(encoding="utf-8"))
    assert parsed["cff-version"] == "1.2.0"
    assert parsed["title"] == "Sample Manuscript"
    assert parsed["version"] == "0.9.1"
    assert parsed["doi"] == "10.5281/zenodo.000001"
    assert parsed["license"] == "CC-BY-4.0"
    assert parsed["repository-code"] == "https://github.com/docxology/crescent_city"
    assert parsed["authors"][0]["family-names"] == "Lovelace"
    assert parsed["authors"][0]["given-names"] == "Ada"
    assert parsed["authors"][0]["orcid"] == "https://orcid.org/0000-0000-0000-0001"
    assert parsed["authors"][1]["family-names"] == "Babbage"


def test_write_zenodo_metadata_shape(tmp_path: Path) -> None:
    from src.publishing import write_zenodo_metadata

    target = tmp_path / "zenodo_metadata.json"
    write_zenodo_metadata(_sample_config(), target)
    payload = json.loads(target.read_text(encoding="utf-8"))
    assert payload["metadata"]["title"] == "Sample Manuscript"
    assert payload["metadata"]["upload_type"] == "publication"
    assert payload["metadata"]["creators"][0]["name"] == "Ada Lovelace"
    assert payload["metadata"]["creators"][1]["name"] == "Charles Babbage"
    assert payload["metadata"]["doi"] == "10.5281/zenodo.000001"
    assert payload["metadata"]["license"] == "cc-by-4.0"
    assert "https://github.com/docxology/crescent_city" in payload["metadata"]["description"]


def test_write_bibtex_self_citation(tmp_path: Path) -> None:
    from src.publishing import write_bibtex_self_citation

    target = tmp_path / "self.bib"
    write_bibtex_self_citation(_sample_config(), target)
    body = target.read_text(encoding="utf-8")
    assert body.startswith("@")
    assert "Sample Manuscript" in body
    assert "CC-BY-4.0" in body
    assert "https://github.com/docxology/crescent_city" in body


def test_write_publishing_artifacts_bundle(tmp_path: Path) -> None:
    from src.publishing import write_publishing_artifacts

    artifacts = write_publishing_artifacts(_sample_config(), tmp_path)
    assert artifacts.citation_cff.exists()
    assert artifacts.zenodo_metadata.exists()
    assert artifacts.bibtex.exists()


def test_publishing_handles_missing_optional_keys(tmp_path: Path) -> None:
    from src.publishing import write_citation_cff, write_zenodo_metadata

    bare = {"paper": {"title": "Bare title"}, "authors": [{"name": "Solo"}]}
    cff = tmp_path / "CITATION.cff"
    zen = tmp_path / "zen.json"
    write_citation_cff(bare, cff)
    write_zenodo_metadata(bare, zen)
    parsed = yaml.safe_load(cff.read_text())
    assert parsed["title"] == "Bare title"
    assert "doi" not in parsed
    payload = json.loads(zen.read_text())
    assert "doi" not in payload["metadata"]
