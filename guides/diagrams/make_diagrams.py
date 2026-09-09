#!/usr/bin/env python3
"""Regenerate every SVG in this folder from the dimensions in diag_*.py.

    python3 guides/diagrams/make_diagrams.py

Stdlib only. Each diag_NN module exposes build(outdir) -> [(filename, caption)].
When a CUTLIST number changes, edit the constants at the top of the matching
diag_NN.py and rerun; the guides embed the SVGs by filename so nothing else moves.
"""
import importlib
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

MODULES = ["diag_02", "diag_03", "diag_04", "diag_06"]


def main():
    made = []
    for name in MODULES:
        mod = importlib.import_module(name)
        made += mod.build(HERE)
    for fn, cap in made:
        print(f"{fn:36s} {cap}")
    print(f"{len(made)} diagrams written to {HERE}")


if __name__ == "__main__":
    main()
