#!/usr/bin/env python3
"""Copy the finished illustration to the competition output directory."""

from __future__ import annotations

import os
from pathlib import Path


OUTPUT_NAME = "entry.png"
DEFAULT_OUTPUT_DIR = Path("/output")
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
PNG_IEND = b"\x00\x00\x00\x00IEND\xaeB`\x82"
MAX_IMAGE_BYTES = 1_048_576


def source_image() -> Path:
    """Return the image committed beside this program."""
    return Path(__file__).resolve().with_name(OUTPUT_NAME)


def output_image() -> Path:
    """Resolve the configured output folder, falling back to /output."""
    configured = os.environ.get("MAKEFUN_OUTPUT_DIR")
    return Path(configured) / OUTPUT_NAME if configured else DEFAULT_OUTPUT_DIR / OUTPUT_NAME


def read_valid_png(path: Path) -> bytes:
    """Read the asset and reject oversized or obviously incomplete PNG files."""
    image = path.read_bytes()
    if len(image) > MAX_IMAGE_BYTES:
        raise ValueError(f"{path.name} exceeds the 1 MiB image limit")
    if not image.startswith(PNG_SIGNATURE):
        raise ValueError(f"{path.name} does not have a PNG signature")
    if not image.endswith(PNG_IEND):
        raise ValueError(f"{path.name} is missing its terminal PNG IEND chunk")
    return image


def main() -> None:
    """Create the output folder and copy the image without altering its bytes."""
    source = source_image()
    image = read_valid_png(source)
    destination = output_image()
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_bytes(image)


if __name__ == "__main__":
    main()
