"""Abutment design data snapshot (A1 & A2) from design note."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class AbutmentDesign:
    name: str = "A1 & A2"
    structural_system: str = "simply supported"
    effective_span_m: float = 24.0
    expansion_gap_mm: float = 40.0
    n_lanes: int = 2
    skew_deg: float = 0.0
    concrete_grade: str = "M30"
    fck_mpa: float = 30.0
    fcd_basic_mpa: float = 13.40
    steel_grade: str = "Fe500"
    impact_factor: float = 1.15
    deck_level: float = 92.575
    soffit_level: float = 90.800
    cap_top: float = 90.300
    cap_bottom: float = 89.800
    hfl: float = 90.000
    ground_lbl: float = 88.910
    pile_cap_bottom: float = 86.810
    scour_level: float = 74.800
    foundation_type: str = "pile foundation with pile cap"
    approach_slab: str = "two-way slab, IS 456; LL 20 t bogie"
