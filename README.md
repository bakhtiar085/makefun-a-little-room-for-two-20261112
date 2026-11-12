# A Little Room for Two

An original digital illustration of a sleepy otter sheltering a duckling under
a broad leaf umbrella. The quiet colors, close pose, and small stitched heart
give the pair a gentle story.

## Run

With Python 3.13, run the standard-library-only competition entrypoint:

```sh
python3.13 main.py
```

It writes `entry.png` to `/output` by default. Set `MAKEFUN_OUTPUT_DIR` to use
another directory.

## Development

`artwork.svg` is the editable illustration. To rebuild `entry.png`, install
WeasyPrint, Poppler (`pdftoppm`), and Pillow, then run:

```sh
python3 render_art.py
```

The competition runtime does not use the development renderer or its
dependencies.

## Checks

- Regenerated `entry.png` from `artwork.svg` with the available development
  renderer.
- Ran `main.py` twice with Python 3.13 from a temporary working directory and
  minimal environment; each output matched the committed image byte for byte.
- Confirmed the image is a 1024×1024 RGBA PNG, 78,684 bytes, with a PNG
  signature and terminal IEND chunk (under the 1 MiB limit).
