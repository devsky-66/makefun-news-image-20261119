#!/usr/bin/env python3
"""Copy the bundled infographic to the make.fun output directory.

Standard library only, no network. The image is drawn at build time by
draw_infographic.py and shipped in this repository as entry.png; this
program reproduces it byte for byte on every run.
"""
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output/entry.png")
    # MAKEFUN_OUTPUT_DIR may be a directory or a full file path.
    if out_dir.endswith(".png"):
        dest = out_dir
    else:
        dest = os.path.join(out_dir, "entry.png")
    os.makedirs(os.path.dirname(dest) or ".", exist_ok=True)
    shutil.copyfile(os.path.join(HERE, "entry.png"), dest)
    print("wrote", dest)
    return 0


if __name__ == "__main__":
    sys.exit(main())
