"""Persist router results to local files."""

from __future__ import annotations

import json
import os
import uuid
from datetime import datetime
from typing import Any, Dict


def save_result(result: Dict[str, Any], output_dir: str = "results") -> str:
    """Save one result record as JSON under output_dir. Returns the file path."""
    os.makedirs(output_dir, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S-%f")
    filename = f"{stamp}-{uuid.uuid4().hex[:8]}.json"
    path = os.path.join(output_dir, filename)
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(result, handle, indent=2, ensure_ascii=False)
        handle.write("\n")
    return path


def save_results(results, output_dir: str = "results") -> List[str]:
    """Save many result records. Returns the list of file paths."""
    from typing import List  # local import to keep module import order simple

    paths: List[str] = []
    for result in results:
        paths.append(save_result(result, output_dir))
    return paths
