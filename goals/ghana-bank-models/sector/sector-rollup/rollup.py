#!/usr/bin/env python3
"""Compatibility entry point for accepted-only rollup.mjs."""
import subprocess
import sys
from pathlib import Path
raise SystemExit(subprocess.call(["node", str(Path(__file__).with_name("rollup.mjs")), *sys.argv[1:]]))
