"""Allow running the package as ``python -m ollama_router``."""

from __future__ import annotations

import sys

from .cli import main

if __name__ == "__main__":
    raise SystemExit(main())
