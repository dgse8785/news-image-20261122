#!/usr/bin/env python3
"""Deliver the finished poster for the 22 November 2026 edition.

The artwork already sits beside this file under the name entry.png.
Running this module moves a faithful copy of those bytes into the
folder the competition runner designates, falling back to /output
when no alternative folder has been supplied through the
environment.  Only the standard library takes part, and the source
bytes never change at run time, so repeated runs stay identical.
The copy is a plain read-then-write of the byte payload, nothing
is decoded, redrawn, or re-encoded along the way.
"""

import os
from pathlib import Path

POSTER_NAME = "entry.png"
ENV_KEY = "MAKEFUN_OUTPUT_DIR"
FALLBACK_FOLDER = Path("/output")


def chosen_folder():
    """Pick the output folder, honouring the environment override."""
    raw_value = os.getenv(ENV_KEY)
    if raw_value and raw_value.strip():
        return Path(raw_value.strip())
    return FALLBACK_FOLDER


def publish_poster():
    """Write the bundled poster bytes into the chosen folder."""
    bundle_path = Path(__file__).resolve().parent / POSTER_NAME
    payload = bundle_path.read_bytes()
    folder = chosen_folder()
    folder.mkdir(parents=True, exist_ok=True)
    target_path = folder / POSTER_NAME
    target_path.write_bytes(payload)
    return target_path


if __name__ == "__main__":
    print("Delivered:", publish_poster())
