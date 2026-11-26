# Build the Crescent City manuscript

Prepare a clean checkout of this repository and install uv, Pandoc 3.14,
pandoc-crossref built for that Pandoc version, and XeLaTeX with Template's
LaTeX packages. The project and Template use independent locked environments.

```sh
crescent_source="$(pwd -P)"
git clone https://github.com/docxology/template.git ../crescent-template
git -C ../crescent-template checkout --detach 87704feae0a4490ef7dad9c931d268e8c30273c2
cd ../crescent-template
crescent_template="$(pwd -P)"
uv sync --locked --no-dev
mkdir -p projects/working
git -C "$crescent_source" worktree add --detach "$PWD/projects/working/crescent_city" HEAD

(
  cd projects/working/crescent_city
  uv sync --locked --extra dev --python 3.14
  mkdir -p .venv/share/nltk_data/corpora
  curl -fsSLo .venv/share/nltk_data/corpora/cmudict.zip \
    https://raw.githubusercontent.com/nltk/nltk_data/550b6625bcef1f2abff2ff770a5a0d272c9c6b2a/packages/corpora/cmudict.zip
  .venv/bin/python -m zipfile -e .venv/share/nltk_data/corpora/cmudict.zip \
    .venv/share/nltk_data/corpora
  export TEMPLATE_REPO_ROOT="$crescent_template" MPLBACKEND=Agg
  .venv/bin/python -m pytest tests/ -q
  .venv/bin/python scripts/run_history_pipeline.py --strict
  .venv/bin/python scripts/z_generate_manuscript_variables.py
)
uv run --no-sync python scripts/pipeline/stage_03_render.py \
  --project working/crescent_city --skip-manuscript-hydration
uv run --no-sync python scripts/pipeline/stage_04_validate.py \
  --project working/crescent_city
```

The pronunciation dictionary supports the prose metrics. Its pinned archive
has SHA-256 `d07cca47fd72ad32ea9d8ad1219f85301eeaf4568f8b6b73747506a71fb5afd6`.
Source tests, analysis, figure generation and manuscript rendering can run
offline after the environments and dictionary are present.

Find the manuscript and HTML in the render worktree's
`output/pdf/crescent_city_combined.pdf` and `output/web/index.html`.
The build writes the figure provenance manifest and accessibility registry
under `output/figures/`, and the validation and provenance receipts under
`output/reports/`.

Inside the render worktree, use
`.venv/bin/python scripts/run_history_pipeline.py --list` to inspect project
steps and `.venv/bin/python scripts/run_history_pipeline.py --figures-only`
to regenerate the figure set. For alternate source inputs use the runner's
`--project-root` and `--config` options.

[Documentation index](README.md) · [Manuscript](manuscript/README.md) · [Artifact guide](rendering_and_outputs.md)
