#!/usr/bin/env python3
"""Tray launcher stub — Paul Pearl/Upstream Drive (pythonw / future Inc or PM wire)."""

from __future__ import annotations

import os
import runpy
import sys

_INC_ROOT = os.path.dirname(os.path.abspath(__file__))
_PKG_DIR = os.path.join(_INC_ROOT, "paul_pearl_engagement")

for _path in (_INC_ROOT, _PKG_DIR):
    if _path not in sys.path:
        sys.path.insert(0, _path)

# Preserve --tray-restart for single-instance handoff inside tray_host.
runpy.run_path(
    os.path.join(_PKG_DIR, "tray_host.py"),
    run_name="__main__",
)
