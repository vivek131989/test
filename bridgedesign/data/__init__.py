"""JSON-serialisable design data snapshot matching the design note."""

from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path

from bridgedesign.data.parameters import default_design


def export_design_json(path: str | Path | None = None) -> dict:
    design = default_design()
    data = {
        "project": asdict(design.project),
        "geometry": asdict(design.geometry),
        "materials": asdict(design.materials),
        "levels": asdict(design.levels),
        "loading": asdict(design.loading),
        "section": asdict(design.section),
        "reinforcement": asdict(design.reinforcement),
        "forces": asdict(design.forces),
        "bearing": asdict(design.bearing),
        "well": asdict(design.well),
        "stopper": asdict(design.stopper),
        "components": design.components(),
    }
    if path is not None:
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(data, indent=2))
    return data
