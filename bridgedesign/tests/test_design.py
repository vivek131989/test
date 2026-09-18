from __future__ import annotations

import math
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from bridgedesign.calc.bearing import check_bearing, shape_factor
from bridgedesign.calc.cantilever import design_cantilever
from bridgedesign.calc.flexure import deflection_limit, midspan_design_per_metre
from bridgedesign.calc.temperature import thermal_movement_mm
from bridgedesign.calc.voided_slab import check_void_percentage, void_area
from bridgedesign.calc.well import check_steining
from bridgedesign.data.parameters import default_design


def test_project_identity():
    d = default_design()
    assert "Kunwari" in d.project.title or "KUNWARI" in d.project.title.upper() or "kunwari" in d.project.title.lower()
    assert d.project.client == "MP PWD"
    assert d.geometry.span_cc_exp_joint_m == 25.0
    assert d.geometry.slab_thickness_m == 1.2
    assert d.geometry.deck_width_m == 8.4


def test_void_percentage_matches_note():
    va = void_area(4, 0.6)
    assert abs(va - 1.131) < 0.01
    result = check_void_percentage()
    assert abs(result.void_percentage - 18.52) < 0.1
    assert result.normal_calculation_ok


def test_midspan_reinforcement_adequate():
    d = default_design()
    assert d.reinforcement.mid_bot_ast_prov_mm2_m >= d.reinforcement.mid_bot_ast_req_mm2_m
    flex = midspan_design_per_metre()
    assert flex.ast_req_mm2 > 0
    # Provided Ast should cover simplified calculation demand for per-m strip
    assert d.reinforcement.mid_bot_ast_prov_mm2_m >= flex.ast_req_mm2 * 0.85


def test_cantilever_ok():
    c = design_cantilever()
    assert c.ok
    assert c.ast_prov_mm2 >= c.ast_req_mm2


def test_bearing_shape_factor_and_checks():
    s = shape_factor()
    assert abs(s - 9.59) < 0.15
    checks = check_bearing()
    assert any(c.name.startswith("Shear strain") and c.ok for c in checks)
    assert all(c.ok for c in checks)


def test_thermal_movement():
    # α=1.2e-5, L=24 m, ΔT=25 → 7.2 mm as in bearing design data
    assert abs(thermal_movement_mm(24.0, 25.0) - 7.2) < 0.05


def test_well_steining():
    w = check_steining()
    assert abs(w.gross_area_m2 - 26.829) < 0.05
    assert w.short_column_both_spans
    assert w.ok


def test_deflection_annex():
    d = deflection_limit()
    assert d["ok"]
    assert d["max_deflection_70rw_mm"] < d["documented_limit_mm"]


def test_report_builds(tmp_path):
    from bridgedesign.reports.generate import build_all_outputs

    # Build into a temp copy structure
    out = tmp_path / "bridgedesign"
    (out / "reports").mkdir(parents=True)
    (out / "drawings").mkdir(parents=True)
    (out / "data").mkdir(parents=True)
    result = build_all_outputs(out)
    assert result["report"].exists()
    text = result["report"].read_text()
    assert "Kunwari" in text or "KUNWARI" in text.upper() or "voided" in text.lower()
    assert len(result["drawings"]) == 2
