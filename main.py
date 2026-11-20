#!/usr/bin/env python3
"""Copy the 20 November 2026 news infographic to the output path.

The entry image is drawn ahead of time by build_image.py and stored in
this repository as entry.png. This program only places that exact file at
/output/entry.png, so the submitted image is byte-identical every run.
"""

import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
# The infographic lives next to this program in the repository.
SRC = os.path.join(HERE, "entry.png")
# The competition harness reads the image from this fixed path.
DST = "/output/entry.png"


def main():
    # Create /output if the runner has not made it yet, then copy the
    # image file as-is. copyfile preserves the bytes exactly.
    os.makedirs(os.path.dirname(DST), exist_ok=True)
    shutil.copyfile(SRC, DST)


if __name__ == "__main__":
    main()
