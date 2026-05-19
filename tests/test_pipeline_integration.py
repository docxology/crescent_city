"""End-to-end pipeline integration tests.

All tests here depend on the ``pipeline_artifacts`` session fixture,
which runs the pipeline once and shares the artifacts across the
integration suite.
"""

from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

_PROJECT_DIR = Path(__file__).resolve().parent.parent
_REPO_ROOT = _PROJECT_DIR.parent.parent


def _python_for_project_scripts() -> Path:
    venv_py = _PROJECT_DIR / ".venv" / "bin" / "python"
    return venv_py if venv_py.exists() else Path(sys.executable)


class TestPipeline:
    """Top-level pipeline integration tests."""

    def test_pipeline_runs_cleanly(self) -> None:
        result = subprocess.run(
            [
                str(_python_for_project_scripts()),
                str(_PROJECT_DIR / "scripts" / "run_history_pipeline.py"),
            ],
            capture_output=True,
            text=True,
            cwd=str(_REPO_ROOT),
            timeout=180,
        )
        assert result.returncode == 0, f"Pipeline failed (rc={result.returncode}):\n{result.stdout[-500:]}"

    def test_pipeline_report_json(self, pipeline_artifacts, output_dir: Path) -> None:
        p = output_dir / "pipeline_report.json"
        assert p.exists()
        data = json.loads(p.read_text())
        assert data["checks_passed"] >= 5
        assert data["figures_generated"] >= 24

    def test_manuscript_report_json_snapshot(self, pipeline_artifacts, output_dir: Path) -> None:
        p = output_dir / "manuscript_report.json"
        assert p.exists()
        data = json.loads(p.read_text())
        assert data["total_words"] > 5000
        assert "files" in data and len(data["files"]) >= 30

    def test_review_report_md(self, pipeline_artifacts, output_dir: Path) -> None:
        p = output_dir / "review_report.md"
        assert p.exists()
        text = p.read_text()
        assert len(text) > 200
        assert "Checks" in text


class TestPublishingArtifacts:
    """Publishing artifacts emitted by the pipeline."""

    def test_citation_cff_present(self, pipeline_artifacts, output_dir: Path) -> None:
        p = output_dir / "CITATION.cff"
        assert p.exists()
        body = p.read_text()
        assert "cff-version: " in body
        assert "title: " in body

    def test_zenodo_metadata_present(self, pipeline_artifacts, output_dir: Path) -> None:
        p = output_dir / "zenodo_metadata.json"
        assert p.exists()
        payload = json.loads(p.read_text())
        assert payload["metadata"]["title"]
        assert payload["metadata"]["upload_type"] == "publication"

    def test_self_citation_bibtex_present(self, pipeline_artifacts, output_dir: Path) -> None:
        p = output_dir / "self_citation.bib"
        assert p.exists()
        bib = p.read_text()
        assert bib.startswith("@")

    def test_publishing_artifacts_use_config_metadata(
        self, pipeline_artifacts, output_dir: Path, manuscript_dir: Path
    ) -> None:
        """CITATION.cff must reflect ``manuscript/config.yaml`` (no drift)."""
        import yaml

        cfg = yaml.safe_load((manuscript_dir / "config.yaml").read_text())
        cff_body = (output_dir / "CITATION.cff").read_text()
        zenodo = json.loads((output_dir / "zenodo_metadata.json").read_text())
        self_citation = (output_dir / "self_citation.bib").read_text()
        assert cfg["paper"]["title"] in cff_body
        assert cfg["paper"]["version"] in cff_body
        assert cfg["publication"]["doi"] in cff_body
        assert cfg["publication"]["repository_url"] in cff_body
        assert cfg["publication"]["doi"] == zenodo["metadata"]["doi"]
        assert cfg["publication"]["repository_url"] in zenodo["metadata"]["description"]
        assert cfg["publication"]["repository_url"] in self_citation


class TestPDFProvenance:
    """If the combined PDF was rendered upstream, validate it matches the manuscript shape."""

    def test_pdf_has_reasonable_page_count(self) -> None:
        pdf = _PROJECT_DIR / "output" / "pdf" / "crescent_city_combined.pdf"
        if not pdf.exists():
            return  # rendering stage not run in this context
        # Lightweight check: PDF version + non-trivial size + at least one
        # /Page object. We avoid pulling pypdf at test time to keep the
        # suite offline-self-contained.
        head = pdf.read_bytes()[:8]
        assert head.startswith(b"%PDF-"), "Not a PDF"
        size = pdf.stat().st_size
        assert size > 1_000_000, f"PDF unexpectedly small: {size} bytes"
        # Approximate page count from /Count attribute in catalog. We
        # accept anything in [60, 250] — the manuscript is ~115–140 pages
        # depending on figure / table layout.
        page_count_match = re.search(rb"/Count\s+(\d{2,4})", pdf.read_bytes()[:200_000])
        if page_count_match:
            n = int(page_count_match.group(1))
            assert 60 <= n <= 250, f"PDF page count {n} outside band [60, 250]"

    def test_rendered_pdf_sample_pages_are_nonblank(self, tmp_path: Path) -> None:
        """Rasterize sampled rendered-PDF pages when Poppler is available."""
        pdf = _PROJECT_DIR / "output" / "pdf" / "crescent_city_combined.pdf"
        pdftoppm = shutil.which("pdftoppm")
        pdfinfo = shutil.which("pdfinfo")
        if not pdf.exists() or not pdftoppm or not pdfinfo:
            return

        info = subprocess.run([pdfinfo, str(pdf)], capture_output=True, text=True, timeout=30)
        assert info.returncode == 0, info.stderr[-300:]
        page_match = re.search(r"^Pages:\s+(\d+)", info.stdout, re.M)
        assert page_match, info.stdout
        page_count = int(page_match.group(1))
        assert 60 <= page_count <= 250

        from PIL import Image

        for page in (1, min(8, page_count), min(24, page_count)):
            prefix = tmp_path / f"page_{page}"
            result = subprocess.run(
                [
                    pdftoppm,
                    "-f",
                    str(page),
                    "-l",
                    str(page),
                    "-png",
                    "-singlefile",
                    str(pdf),
                    str(prefix),
                ],
                capture_output=True,
                text=True,
                timeout=60,
            )
            assert result.returncode == 0, result.stderr[-300:]
            image_path = prefix.with_suffix(".png")
            assert image_path.exists(), f"pdftoppm did not write {image_path}"
            image = Image.open(image_path).convert("L")
            histogram = image.histogram()
            nonwhite = sum(count for value, count in enumerate(histogram) if value < 250)
            total = image.width * image.height
            assert nonwhite / total > 0.005, f"PDF page {page} rasterized nearly blank"
