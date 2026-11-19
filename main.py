#!/usr/bin/env python3
"""Entry program for make.fun competition news-image-20261119.

Copies the pre-rendered front-page image (entry.png, in this same
directory, drawn by draw_image.py) to the output location as
entry.png.

Standard library only: no third-party imports, no network access,
no randomness. Running it twice produces byte-identical output,
because it is a plain file copy.

Output directory: the MAKEFUN_OUTPUT_DIR environment variable when
it is set, otherwise /output.
"""

import os
import shutil
import sys
from pathlib import Path

SOURCE_NAME = "entry.png"
OUTPUT_NAME = "entry.png"
DEFAULT_OUTPUT_DIR = "/output"


def main():
    here = Path(__file__).resolve().parent
    source = here / SOURCE_NAME
    if not source.is_file():
        print(f"error: {source} not found", file=sys.stderr)
        return 1

    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or DEFAULT_OUTPUT_DIR
    destination = Path(output_dir) / OUTPUT_NAME
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, destination)

    size = destination.stat().st_size
    print(f"copied {source} -> {destination} ({size} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
