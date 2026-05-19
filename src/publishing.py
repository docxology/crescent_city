"""Publishing artifact generation for crescent_city.

Wires :mod:`infrastructure.publishing` into the project pipeline. Emits

* ``output/CITATION.cff`` — Citation File Format 1.2.0 (zenodo-friendly).
* ``output/zenodo_metadata.json`` — payload usable with the Zenodo API or
  the manual deposit form.

Both files are derived from ``manuscript/config.yaml`` so there is no
hand-edited source-of-truth drift between the manuscript header and the
publication artifacts.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any, Mapping

from infrastructure.publishing.citations import generate_citation_bibtex
from infrastructure.publishing.models import PublicationMetadata

# ``yaml.safe_load`` returns ``Any``; we accept the same here. Down in the
# helpers we narrow to ``dict[str, Any]`` for the per-section payloads.
Config = Mapping[str, Any]
DEFAULT_REPOSITORY_URL = "https://github.com/docxology/crescent_city"


def _publication_license(config: Config) -> str:
    """Return the license for the published scholarly artifact.

    ``metadata.license`` is intentionally interpreted as the manuscript /
    publication license. Optional ``code_license`` and ``data_license`` values
    document the repository's mixed-license reality in project prose, but CFF
    and Zenodo each accept a single license for the deposited object.
    """
    metadata_blk = config.get("metadata", {}) or {}
    return str(metadata_blk.get("license") or "CC-BY-4.0")


def _repository_url(config: Config, explicit: str | None = None) -> str:
    """Return the configured public repository URL for release metadata."""
    if explicit:
        return explicit
    publication = config.get("publication", {}) or {}
    metadata_blk = config.get("metadata", {}) or {}
    return str(publication.get("repository_url") or metadata_blk.get("repository_url") or DEFAULT_REPOSITORY_URL)


@dataclass
class PublishingArtifacts:
    """Filesystem paths of every artifact written by :func:`write_publishing_artifacts`."""

    citation_cff: Path
    zenodo_metadata: Path
    bibtex: Path


def _authors_from_config(authors_block: list[Mapping[str, Any]]) -> list[dict[str, str]]:
    """Normalize ``config.yaml::authors`` into CFF-shaped records."""
    cff_authors: list[dict[str, str]] = []
    for a in authors_block:
        name = str(a.get("name") or "").strip()
        if not name:
            continue
        # Split "First Middle Last" on the last space — robust enough for
        # ASCII Latin names. Multi-word given names are handled by joining
        # everything before the final token.
        parts = name.rsplit(" ", 1)
        if len(parts) == 2:
            given, family = parts
        else:
            given, family = "", name
        rec: dict[str, str] = {
            "family-names": family,
            "given-names": given,
        }
        if a.get("orcid"):
            rec["orcid"] = f"https://orcid.org/{a['orcid']}"
        if a.get("affiliation"):
            rec["affiliation"] = str(a["affiliation"])
        if a.get("email"):
            rec["email"] = str(a["email"])
        cff_authors.append(rec)
    return cff_authors


def write_citation_cff(
    config: Config,
    output_path: Path,
    repository_url: str | None = None,
) -> Path:
    """Write a CFF 1.2.0 file at *output_path* derived from *config*.

    *config* is the dict returned by ``yaml.safe_load`` of
    ``manuscript/config.yaml``. The function tolerates missing keys with
    sensible defaults so a freshly-scaffolded project still emits a
    valid file.
    """
    paper = config.get("paper", {}) or {}
    publication = config.get("publication", {}) or {}
    repo_url = _repository_url(config, repository_url)
    cff = {
        "cff-version": "1.2.0",
        "message": "If you use this manuscript or its build pipeline, please cite as below.",
        "title": str(paper.get("title") or "Untitled"),
        "version": str(paper.get("version") or "0.0.0"),
        "date-released": str(publication.get("year") or date.today().year) + "-01-01",
        "authors": _authors_from_config(list(config.get("authors") or [])),
        "keywords": list(config.get("keywords") or []),
        "license": _publication_license(config),
        "repository-code": repo_url,
        "type": "dataset",  # manuscript + reproducible figure pipeline
    }
    doi = publication.get("doi")
    if doi:
        cff["doi"] = str(doi)

    if paper.get("subtitle"):
        cff["abstract"] = str(paper["subtitle"])

    output_path.parent.mkdir(parents=True, exist_ok=True)
    # Hand-rolled YAML emission so the file is stable for git diffs
    # (avoids PyYAML's default key reordering and inconsistent quoting).
    lines: list[str] = []
    for key in (
        "cff-version",
        "message",
        "title",
        "version",
        "date-released",
        "license",
        "repository-code",
        "type",
    ):
        if cff.get(key):
            lines.append(f"{key}: {json.dumps(cff[key])}")
    if cff.get("doi"):
        lines.append(f"doi: {json.dumps(cff['doi'])}")
    if cff.get("abstract"):
        lines.append(f"abstract: {json.dumps(cff['abstract'])}")
    if cff.get("keywords"):
        lines.append("keywords:")
        for kw in cff["keywords"]:
            lines.append(f"  - {json.dumps(kw)}")
    if cff.get("authors"):
        lines.append("authors:")
        for a in cff["authors"]:
            lines.append(f"  - family-names: {json.dumps(a['family-names'])}")
            if a.get("given-names"):
                lines.append(f"    given-names: {json.dumps(a['given-names'])}")
            if a.get("orcid"):
                lines.append(f"    orcid: {json.dumps(a['orcid'])}")
            if a.get("affiliation"):
                lines.append(f"    affiliation: {json.dumps(a['affiliation'])}")
            if a.get("email"):
                lines.append(f"    email: {json.dumps(a['email'])}")

    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return output_path


def write_zenodo_metadata(
    config: Config,
    output_path: Path,
) -> Path:
    """Emit a Zenodo-API-shaped metadata payload at *output_path*."""
    paper = config.get("paper", {}) or {}
    publication = config.get("publication", {}) or {}
    metadata_blk = config.get("metadata", {}) or {}
    repo_url = _repository_url(config)
    base_description = str(paper.get("subtitle") or paper.get("title") or "")
    if base_description and not base_description.endswith((".", "!", "?")):
        base_description += "."
    description = f"{base_description} Source repository: {repo_url}.".strip()

    creators: list[dict[str, str]] = []
    for a in list(config.get("authors") or []):
        rec = {"name": str(a.get("name") or "").strip()}
        if a.get("orcid"):
            rec["orcid"] = str(a["orcid"])
        if a.get("affiliation"):
            rec["affiliation"] = str(a["affiliation"])
        if rec["name"]:
            creators.append(rec)

    payload = {
        "metadata": {
            "title": str(paper.get("title") or "Untitled"),
            "description": description,
            "upload_type": "publication",
            "publication_type": "report",
            "publication_date": str(publication.get("year") or date.today().year) + "-01-01",
            "creators": creators,
            "keywords": list(config.get("keywords") or []),
            "license": _publication_license(config).lower().replace(" ", "-"),
            "version": str(paper.get("version") or "0.0.0"),
            "language": str(metadata_blk.get("language") or "en"),
        }
    }
    doi = publication.get("doi")
    if doi:
        payload["metadata"]["doi"] = str(doi)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return output_path


def write_bibtex_self_citation(
    config: Config,
    output_path: Path,
) -> Path:
    """Generate a BibTeX self-citation for the manuscript."""
    paper = config.get("paper", {}) or {}
    publication = config.get("publication", {}) or {}
    repo_url = _repository_url(config)
    authors = [str(a.get("name") or "").strip() for a in list(config.get("authors") or []) if a.get("name")]
    md = PublicationMetadata(
        title=str(paper.get("title") or "Untitled"),
        authors=authors,
        abstract=str(paper.get("subtitle") or ""),
        keywords=list(config.get("keywords") or []),
        doi=str(publication["doi"]) if publication.get("doi") else None,
        publication_date=str(publication.get("year") or date.today().year),
        license=_publication_license(config),
        repository_url=repo_url,
    )
    bib = generate_citation_bibtex(md)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(bib + "\n", encoding="utf-8")
    return output_path


def write_publishing_artifacts(
    config: Config,
    output_dir: Path,
    repository_url: str | None = None,
) -> PublishingArtifacts:
    """Write the three publishing artifacts under *output_dir* and return their paths."""
    cff = write_citation_cff(config, output_dir / "CITATION.cff", repository_url=repository_url)
    zenodo = write_zenodo_metadata(config, output_dir / "zenodo_metadata.json")
    bib = write_bibtex_self_citation(config, output_dir / "self_citation.bib")
    return PublishingArtifacts(citation_cff=cff, zenodo_metadata=zenodo, bibtex=bib)
