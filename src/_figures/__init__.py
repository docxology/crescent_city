"""Internal implementation modules for ``src.figures``.

Each submodule defines one or more pure plotting functions of signature::

    def plot_<name>(... , output_dir: Path) -> Path

returning the path of the saved PNG. Submodules avoid cross-importing each
other so a single figure can be regenerated without loading the others.

Public consumers should import from :mod:`src.figures` rather than from this
package — the public module wires every plotter into the
:data:`src.figures.FIGURE_REGISTRY` and applies the project's shared
matplotlib style.
"""

from __future__ import annotations
