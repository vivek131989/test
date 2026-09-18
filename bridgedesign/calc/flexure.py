"""IRC:112 flexure / shear helpers for deck verification (per metre width)."""

from __future__ import annotations

import math
from dataclasses import dataclass


@dataclass
class FlexureResult:
    mu_knm: float
    b_mm: float
    d_mm: float
    fck: float
    fy: float
    xu_mm: float
    xu_lim_mm: float
    lever_arm_mm: float
    ast_req_mm2: float
    under_reinforced: bool
    capacity_ok: bool
    message: str


def fcd(fck: float, alpha: float = 0.67, gamma_m: float = 1.5) -> float:
    return alpha * fck / gamma_m


def fyd(fy: float, gamma_m: float = 1.15) -> float:
    return fy / gamma_m


def design_flexure_singly_reinforced(
    mu_knm: float,
    b_mm: float,
    d_mm: float,
    fck: float = 35.0,
    fy: float = 500.0,
    ast_provided_mm2: float | None = None,
) -> FlexureResult:
    """
    Simplified rectangular stress-block flexure design (IRC:112 / IS 456 style).
    Mu in kN·m for width b.
    """
    mu_nmm = mu_knm * 1e6
    # xu from equilibrium of Mu = 0.36 fck b xu (d - 0.42 xu)
    # Solve quadratic: 0.36 fck b * 0.42 xu^2 - 0.36 fck b d xu + Mu = 0
    a = 0.36 * fck * b_mm * 0.42
    bcoef = -0.36 * fck * b_mm * d_mm
    c = mu_nmm
    disc = bcoef**2 - 4 * a * c
    if disc < 0:
        # Section inadequate even as balanced – report limiting
        xu = 0.48 * d_mm if fy >= 500 else 0.53 * d_mm
        under = False
        z = d_mm - 0.42 * xu
        ast = mu_nmm / (0.87 * fy * z) if z > 0 else float("inf")
        return FlexureResult(
            mu_knm=mu_knm,
            b_mm=b_mm,
            d_mm=d_mm,
            fck=fck,
            fy=fy,
            xu_mm=xu,
            xu_lim_mm=xu,
            lever_arm_mm=z,
            ast_req_mm2=ast,
            under_reinforced=False,
            capacity_ok=False,
            message="Required Mu exceeds balanced-section capacity (double reinforcement needed).",
        )

    xu = (-bcoef - math.sqrt(disc)) / (2 * a)
    # xu,max for Fe500 ≈ 0.46 d (IRC:112 parabolic/bilinear); use 0.48d conservative IS-style
    xu_lim = 0.46 * d_mm
    under = xu <= xu_lim
    z = d_mm - 0.42 * xu
    ast = mu_nmm / (0.87 * fy * z)
    capacity_ok = True
    if ast_provided_mm2 is not None:
        capacity_ok = ast_provided_mm2 >= ast and under
    msg = (
        f"Ast req = {ast:.0f} mm²; xu/d = {xu/d_mm:.3f} "
        f"({'under' if under else 'over'}-reinforced)."
    )
    return FlexureResult(
        mu_knm=mu_knm,
        b_mm=b_mm,
        d_mm=d_mm,
        fck=fck,
        fy=fy,
        xu_mm=xu,
        xu_lim_mm=xu_lim,
        lever_arm_mm=z,
        ast_req_mm2=ast,
        under_reinforced=under,
        capacity_ok=capacity_ok,
        message=msg,
    )


def midspan_design_per_metre(
    total_mu_knm: float = 22890.0,
    deck_width_m: float = 8.40,
    d_mm: float = 1128.0,
    fck: float = 35.0,
    fy: float = 500.0,
    ast_provided_mm2_m: float = 15466.0,
) -> FlexureResult:
    """Distribute full-deck factored mid-span moment to per-metre strip."""
    mu_per_m = total_mu_knm / deck_width_m
    return design_flexure_singly_reinforced(
        mu_knm=mu_per_m,
        b_mm=1000.0,
        d_mm=d_mm,
        fck=fck,
        fy=fy,
        ast_provided_mm2=ast_provided_mm2_m,
    )


def deflection_limit(span_m: float = 14.0) -> dict:
    """
    Service deflection check span/800 (design note load-test annex).
    Effective span for simply supported slab ≈ 24 m between bearings;
    permissible midspan deflection = 24000/800 = 30 mm for full span,
    note tabulates 17.5 mm for the test arrangement (L≈14 m).
    """
    return {
        "span_mm": span_m * 1000.0,
        "limit_span_over_800_mm": span_m * 1000.0 / 800.0,
        "documented_limit_mm": 17.5,
        "max_deflection_70rw_mm": 7.61,
        "max_deflection_2a_mm": 7.33,
        "ok": 7.61 < 17.5,
    }
