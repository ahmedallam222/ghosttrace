"""Handles writing .ghost.json files."""

import json
from pathlib import Path


def save_trace(trace: dict, output_path: str | None = None) -> Path:
    """Save a ghost trace dict to a .ghost.json file."""
    if output_path is None:
        session_id = trace["session"]["id"]
        output_path = f"{session_id}.ghost.json"

    path = Path(output_path)
    path.write_text(json.dumps(trace, indent=2), encoding="utf-8")
    return path
