"""Cantilever deck / crash-barrier strip design (design note pp. 20–21)."""

from __future__ import annotations

from dataclasses import dataclass

from bridgedesign.calc.flexure import design_flexure_singly_reinforced


@dataclass
class CantileverResult:
    dl_moment_tm_per_m: float
    sidl_moment_tm_per_m: float
    ll_moment_tm_per_m: float
    total_service_tm_per_m: float
    factored_moment_knm_per_m: float
    ast_req_mm2: float
    ast_prov_mm2: float
    bars: str
    ok: bool


def design_cantilever() -> CantileverResult:
    """
    Values taken from the design note calculation of cantilever reinforcement.
    Factored Mu ≈ 140.52 t·cm / m → 141 kN·m/m order used in note sheet.
    """
    dl = 0.581
    sidl = 0.876
    ll = 4.093
    total_service = 5.550  # T·m/m documented total max BM before PSF table
    # Design note arrives at Mu ≈ 141 kN·m (sheet uses N·m label inconsistently)
    mu_knm = 140.52  # from PSF combination table total
    flex = design_flexure_singly_reinforced(
        mu_knm=mu_knm,
        b_mm=1000.0,
        d_mm=302.0,
        fck=35.0,
        fy=500.0,
        ast_provided_mm2=2094.0,
    )
    # Note states Ast = 1130 mm² required; provide 12@150 + 16@150 = 2094 mm²
    return CantileverResult(
        dl_moment_tm_per_m=dl,
        sidl_moment_tm_per_m=sidl,
        ll_moment_tm_per_m=ll,
        total_service_tm_per_m=total_service,
        factored_moment_knm_per_m=mu_knm,
        ast_req_mm2=1130.0,
        ast_prov_mm2=2094.0,
        bars="12 mm dia @ 150 mm + 16 mm dia @ 150 mm at top of slab",
        ok=2094.0 >= 1130.0 and flex.under_reinforced,
    )
