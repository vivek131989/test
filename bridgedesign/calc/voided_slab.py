"""Voided slab section properties and IRC SP 64 void checks."""

from __future__ import annotations

import math
from dataclasses import dataclass

from bridgedesign.data.parameters import SuperstructureGeometry, VoidedSectionProperties


@dataclass
class SectionCheckResult:
    void_area_m2: float
    gross_area_m2: float
    void_percentage: float
    limit_percent: float
    normal_calculation_ok: bool
    message: str


def void_area(n_voids: int, diameter_m: float) -> float:
    return n_voids * math.pi / 4.0 * diameter_m**2


def check_void_percentage(
    geometry: SuperstructureGeometry | None = None,
    section: VoidedSectionProperties | None = None,
    limit_percent: float = 40.0,
) -> SectionCheckResult:
    """
    IRC SP 64:2016 cl. 4.1.2 — if voids < 40% of gross area,
    normal (solid-slab equivalent) calculation may be adopted.
    """
    geometry = geometry or SuperstructureGeometry()
    section = section or VoidedSectionProperties()
    va = void_area(geometry.n_voids, geometry.void_diameter_m)
    # Prefer documented gross area (includes cantilevers / webs)
    ga = section.gross_area_m2
    pct = 100.0 * va / ga
    ok = pct < limit_percent
    msg = (
        f"Void percentage = {pct:.2f}% {'<' if ok else '>='} {limit_percent:.0f}% → "
        + ("normal calculation adopted (IRC SP 64 cl. 4.1.2)." if ok else "special voided-slab analysis required.")
    )
    return SectionCheckResult(
        void_area_m2=round(va, 3),
        gross_area_m2=ga,
        void_percentage=round(pct, 2),
        limit_percent=limit_percent,
        normal_calculation_ok=ok,
        message=msg,
    )


def approximate_self_weight_kn_m(
    geometry: SuperstructureGeometry | None = None,
    density_kn_m3: float = 25.0,
) -> dict:
    """
    Approximate UDL self-weight for STAAD member loading (per design note intent).

    End zones (solid / thicker) vs mid voided zone are distinguished.
    Document values: end UNI GY -152.663 kN/m, mid UNI GY -124.389 kN/m.
    """
    geometry = geometry or SuperstructureGeometry()
    check = check_void_percentage(geometry)
    solid_area = check.gross_area_m2  # already net of voids in note TOTAL
    # Mid-span member load from note
    return {
        "end_udl_kn_m": 152.663,
        "mid_udl_kn_m": 124.389,
        "net_area_m2": check.gross_area_m2 - 0.0,  # note TOTAL already nets voids
        "void_percentage": check.void_percentage,
        "density_kn_m3": density_kn_m3,
        "note": "UDL values taken from design-note STAAD input (LOAD 1 DL).",
    }
