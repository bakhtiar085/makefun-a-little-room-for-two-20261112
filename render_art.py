#!/usr/bin/env python3
"""Render the editable SVG as the committed 1024px PNG.

Development requirements: WeasyPrint, Poppler's ``pdftoppm`` executable,
and Pillow. The competition entrypoint uses only Python's standard library
and copies the already-rendered image.
"""

from __future__ import annotations

import subprocess
import tempfile
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parent
SVG_PATH = ROOT / "artwork.svg"
PNG_PATH = ROOT / "entry.png"
IMAGE_SIZE = 1024
RENDER_DPI = 96


def render_pdf(pdf_path: Path) -> None:
    """Lay out the SVG at its native square size and write a temporary PDF."""
    from weasyprint import HTML

    page_css = (
        f"@page{{size:{IMAGE_SIZE}px {IMAGE_SIZE}px;margin:0}}"
        f"html,body{{margin:0;width:{IMAGE_SIZE}px;height:{IMAGE_SIZE}px}}"
        f"img{{display:block;width:{IMAGE_SIZE}px;height:{IMAGE_SIZE}px}}"
    )
    markup = (
        f"<html><head><style>{page_css}</style></head>"
        f'<body><img src="{SVG_PATH.as_uri()}"></body></html>'
    )
    HTML(string=markup, base_url=str(ROOT)).write_pdf(pdf_path)


def rasterize_pdf(pdf_path: Path, output_stem: Path) -> Path:
    """Use Poppler to create a lossless PNG from the one-page PDF."""
    subprocess.run(
        [
            "pdftoppm",
            "-png",
            "-singlefile",
            "-r",
            str(RENDER_DPI),
            str(pdf_path),
            str(output_stem),
        ],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    return output_stem.with_suffix(".png")


def save_optimized_png(source_png: Path) -> None:
    """Normalize the raster to RGBA and save a compact PNG beside this script."""
    with Image.open(source_png) as image:
        if image.size != (IMAGE_SIZE, IMAGE_SIZE):
            raise ValueError(f"Expected a {IMAGE_SIZE}x{IMAGE_SIZE} render, got {image.size}")
        image.convert("RGBA").save(PNG_PATH, format="PNG", optimize=True)


def main() -> None:
    """Render the editable illustration through the development toolchain."""
    if not SVG_PATH.is_file():
        raise FileNotFoundError(f"Editable artwork is missing: {SVG_PATH.name}")

    with tempfile.TemporaryDirectory(prefix="cutest-picture-render-") as temp_name:
        temporary_dir = Path(temp_name)
        pdf_path = temporary_dir / "artwork.pdf"
        png_stem = temporary_dir / "rendered"
        render_pdf(pdf_path)
        rendered_png = rasterize_pdf(pdf_path, png_stem)
        save_optimized_png(rendered_png)


if __name__ == "__main__":
    main()
