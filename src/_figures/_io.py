"""I/O helpers for figure persistence.

Every figure in the suite saves to both PNG (raster, embedded in the PDF)
and SVG (vector, for slides and web). Centralizing the save logic here
keeps individual plotting functions focused on the plot itself.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt


def save_figure(fig: plt.Figure, name: str, output_dir: Path) -> Path:
    """Persist *fig* as ``{name}.png`` and ``{name}.svg`` under ``output_dir``.

    Creates ``output_dir`` if it does not exist. Closes ``fig`` after saving
    so that long-running figure-generation passes (e.g. the full 24-figure
    suite) do not accumulate matplotlib state and exhaust process memory.

    Args:
        fig: A finalized :class:`matplotlib.figure.Figure`.
        name: Base filename, without extension. ``analysis`` saves as
            ``analysis.png`` and ``analysis.svg``.
        output_dir: Directory in which to write both files.

    Returns:
        Path of the PNG file — the project's manifest-collection
        convention. Scripts print this path to stdout so the rendering
        pipeline can locate generated figures without scanning.
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    png = output_dir / f"{name}.png"
    svg = output_dir / f"{name}.svg"
    # Pin PNG metadata to empty dict so matplotlib doesn't embed a creation
    # timestamp; pin SVG metadata to None so element-IDs come from the
    # hashsalt configured in _style. Together these guarantee that
    # consecutive runs of the same plotter produce byte-identical output.
    fig.savefig(png, format="png", metadata={"Software": "matplotlib"})
    fig.savefig(svg, format="svg", metadata={"Date": None})
    plt.close(fig)
    return png
