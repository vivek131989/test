"""Elastomeric bearing design checks (IRC:83 Part II style), per design note."""

from __future__ import annotations

from dataclasses import dataclass

from bridgedesign.data.parameters import ElastomericBearing


@dataclass
class BearingCheck:
    name: str
    value: float
    limit: float
    unit: str
    ok: bool
    clause: str


def shape_factor(b: ElastomericBearing | None = None) -> float:
    b = b or ElastomericBearing()
    a_eff = b.length_a_mm - 2 * b.side_cover_c_mm
    b_eff = b.width_b_mm - 2 * b.side_cover_c_mm
    return 0.5 * (a_eff * b_eff) / ((a_eff + b_eff) * b.ti_mm)


def check_bearing(b: ElastomericBearing | None = None) -> list[BearingCheck]:
    """
    Design-note Vmax/Vmin are support-group totals for 3 bearings.
    Strain / stress checks use the per-bearing share (matches σmax ≈ 4.6 N/mm² in note).
    """
    b = b or ElastomericBearing()
    s = shape_factor(b)
    n = max(b.n_per_support, 1)
    # Documented compressive strain 2.44 uses full Vmax with Ar·S; keep that formulation
    fzd_n = b.vmax_kn * 1e3
    eps_c = 1.5 * fzd_n / (b.g_n_mm2 * b.ar_mm2 * s)

    # Shear displacement from horizontal load + imposed movement
    vx_from_h = (b.hmax_long_kn * 1e3 * b.te_mm) / (b.ae_mm2 * b.g_n_mm2)
    vx_d = vx_from_h + b.el_long_mm
    eps_q = vx_d / b.te_mm

    # Rotation strain (documented ≈ 0.05)
    a_eff = b.length_a_mm - 2 * b.side_cover_c_mm
    b_eff = b.width_b_mm - 2 * b.side_cover_c_mm
    sum_ti3 = b.n_elastomer_layers * b.ti_mm**3
    eps_a = (b.design_rotation * (a_eff**2 + b_eff**2) * b.ti_mm) / (2 * sum_ti3)

    etd = eps_c + eps_q + eps_a
    # σmax / σmin on a single pad (support total ÷ n bearings)
    sigma_max = (b.vmax_kn * 1e3 / n) / b.ar_mm2
    sigma_min = (b.vmin_kn * 1e3 / n) / b.ar_mm2

    checks = [
        BearingCheck("Shape factor S", round(s, 2), 0.0, "-", True, "Cl. 5.2.3.2"),
        BearingCheck("Compressive strain εc,d", round(eps_c, 2), 7.0, "-", eps_c < 7.0, "Cl. 5.2.3.2"),
        BearingCheck("Shear strain εq,d", round(eps_q, 2), 1.0, "-", eps_q < 1.0, "Cl. 5.2.3.5"),
        BearingCheck("Rotation strain εα,d", round(eps_a, 2), 7.0, "-", eps_a < 7.0, "Cl. 5.2.3.4"),
        BearingCheck("Total design strain εtd", round(etd, 2), 7.0, "-", etd <= 7.0, "Cl. 5.2.3"),
        BearingCheck("σmax (per pad)", round(sigma_max, 2), 10.0, "N/mm²", sigma_max < 10.0, "Cl. 5.2.3.6"),
        BearingCheck("σmin (per pad)", round(sigma_min, 2), 1.0, "N/mm²", sigma_min > 1.0, "Cl. 5.2.3.6"),
    ]
    return checks


def bearing_size_label(b: ElastomericBearing | None = None) -> str:
    b = b or ElastomericBearing()
    return (
        f"{b.length_a_mm:.0f} × {b.width_b_mm:.0f} × {b.total_height_t_mm:.0f} mm "
        f"({b.n_elastomer_layers}×{b.ti_mm:.0f} elastomer + {b.n_steel_laminates}×{b.ts_mm:.0f} steel)"
    )
