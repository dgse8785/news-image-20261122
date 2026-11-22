#!/usr/bin/env python3
"""Entry point for the news-image-20261122 competition entry.

The poster itself lives in this repository as entry.png, drawn ahead
of time by build_poster.py. This program only copies that file to
the output location the harness asks for, using nothing beyond the
Python standard library, so every run writes exactly the same bytes
to exactly the same place.
"""

import os
import shutil
from pathlib import Path

SOURCE = Path(__file__).resolve().parent / "entry.png"
DEFAULT_OUTPUT_DIR = "/output"


def output_dir():
    """Return the directory named by MAKEFUN_OUTPUT_DIR, or /output."""
    chosen = os.environ.get("MAKEFUN_OUTPUT_DIR", "").strip()
    return Path(chosen) if chosen else Path(DEFAULT_OUTPUT_DIR)


def main():
    """Copy the bundled poster to <output dir>/entry.png.

    The copy is a plain byte-for-byte file copy and the source never
    changes at run time, which is what keeps two runs identical.
    """
    destination_dir = output_dir()
    destination_dir.mkdir(parents=True, exist_ok=True)
    destination = destination_dir / "entry.png"
    shutil.copyfile(SOURCE, destination)
    return destination


if __name__ == "__main__":
    print(main())
