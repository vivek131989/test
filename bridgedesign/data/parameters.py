"""
Project and geometry parameters extracted from the design note
(DESIGN-MPPWD-JPSG-KUWARI_RIVER-R0-2P, Rev. 09-01-2024).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List


@dataclass(frozen=True)
class ProjectInfo:
    title: str = (
        "Construction of Submersible Bridge across Kunwari River "
        "on Sujangharhi Road, Dist. Morena"
    )
    client: str = "MP PWD"
    job_name: str = "RCC VOIDED SLAB (SPAN C/C EXP. JOINT = 25m)"
    revision_date: str = "09-01-2024"
    document_ref: str = "DESIGN-MPPWD-JPSG-KUWARI_RIVER-R0-2P"
    codes: tuple = (
        "IRC:6-2017",
        "IRC:112-2011",
        "IRC:78-2014",
        "IRC SP 64:2016",
        "MoRTH Specifications",
    )


@dataclass(frozen=True)
class SuperstructureGeometry:
    """Voided slab deck – single span unit between expansion joints."""

    n_spans_unit: int = 1
    span_cc_bearing_m: float = 24.00
    span_cc_exp_joint_m: float = 25.00
    slab_thickness_m: float = 1.200
    deck_width_m: float = 8.40
    carriageway_width_m: float = 7.50
    footpath_width_m: float = 0.00
    wearing_coat_m: float = 0.075
    wearing_coat_dispersion_m: float = 0.065
    crash_barrier_width_m: float = 0.45
    crash_barrier_plan_m: tuple = (0.50, 0.50)
    height_of_fill_m: float = 0.00
    void_diameter_m: float = 0.60
    n_voids: int = 4
    void_gap_m: float = 0.60
    top_slab_thickness_m: float = 0.200
    soffit_web_width_m: float = 5.10
    cantilever_beyond_web_m: float = 1.35
    cantilever_tip_thickness_m: float = 0.150
    cantilever_root_extra_m: float = 0.850
    camber_percent: float = 2.5
    expansion_joint_type: str = "Strip seal"
    expansion_gap_m: float = 0.040


@dataclass(frozen=True)
class Materials:
    # Deck / voided slab
    deck_concrete_grade: str = "M35"
    deck_fck_mpa: float = 35.0
    # Abutment substructure / foundation
    abutment_concrete_grade: str = "M30"
    abutment_fck_mpa: float = 30.0
    # Pier / well
    pier_concrete_grade: str = "M35"
    pier_fck_mpa: float = 35.0
    steel_grade: str = "Fe500"
    fyk_mpa: float = 500.0
    es_mpa: float = 2.0e5
    concrete_density_kn_m3: float = 25.0
    wet_density_t_m3: float = 2.00
    dry_density_t_m3: float = 2.50
    soil_density_t_m3: float = 2.00
    steel_density_t_m3: float = 7.85
    alpha_thermal: float = 1.20e-5
    gamma_m_concrete_basic: float = 1.50
    gamma_m_steel_basic: float = 1.15
    alpha_cc: float = 0.67


@dataclass(frozen=True)
class Levels:
    """Salient reduced levels (m). Indicative as noted in design note."""

    deck_level: float = 92.575
    soffit_level: float = 90.800
    fsl_assumed: float = 89.800
    hfl: float = 90.000
    # Abutment
    abutment_cap_top: float = 90.300
    abutment_cap_bottom: float = 89.800
    abutment_ground_lbl: float = 88.910
    pile_cap_bottom: float = 86.810
    scour_level: float = 74.800
    # Pier P1
    pier_cap_top: float = 90.300
    pier_cap_bottom: float = 89.300
    pier_ground_lbl: float = 86.500
    well_cap_bottom: float = 84.500


@dataclass(frozen=True)
class LoadingParams:
    live_loads: tuple = ("IRC Class A", "IRC 70R Wheeled")
    impact_factor_slab: float = 1.25
    impact_factor_substructure: float = 1.15
    n_lanes: int = 2
    seismic_zone: str = "II"
    zone_factor_z: float = 0.10
    importance_factor: float = 1.2
    sa_g: float = 2.5
    seismic_coefficient: float = 0.15
    max_air_shade_temp_c: float = 47.5
    min_air_shade_temp_c: float = 0.0
    temp_rise_fall_c: float = 33.75
    temp_rise_fall_bearing_c: float = 25.0


@dataclass(frozen=True)
class VoidedSectionProperties:
    """Section properties from design note page 5 (gross voided slab)."""

    gross_area_m2: float = 6.1065
    void_area_m2: float = 1.131  # 4 × π/4 × 0.6²
    void_percentage: float = 18.52  # < 40% → IRC SP 64 cl. 4.1.2 normal calc
    sum_ay: float = 4.73
    sum_ay2: float = 3.57
    sum_i0: float = 0.49


@dataclass(frozen=True)
class ReinforcementSummary:
    """Deck reinforcement summary (design note §6.0)."""

    # Mid-span top (compression / hogging if continuous; here top face)
    mid_top_deff_mm: float = 1136.0
    mid_top_ast_req_mm2_m: float = 1916.0
    mid_top_ast_prov_mm2_m: float = 1933.0
    mid_top_bars: str = "16 mm dia @ 104 mm c/c"
    # Mid-span bottom (main tension)
    mid_bot_deff_mm: float = 1128.0
    mid_bot_ast_req_mm2_m: float = 11532.0
    mid_bot_ast_prov_mm2_m: float = 15466.0
    mid_bot_bars: str = "32 mm dia @ 104 mm c/c (main + extra)"
    # Distribution
    dist_ast_req_mm2_m: float = 2306.0
    dist_ast_prov_mm2_m: float = 3217.0
    dist_bars: str = "16 mm dia @ 125 mm c/c"
    # Shear links at support
    shear_links: str = "12 mm dia @ 100 mm c/c long. / 500 mm c/c trans."
    # Cantilever
    cantilever_bars: str = "12 mm dia @ 150 mm + 16 mm dia @ 150 mm (top)"
    cantilever_ast_prov_mm2: float = 2094.0


@dataclass(frozen=True)
class FactoredMoments:
    """Factored forces for solid/voided slab (design note §3.4), full deck width."""

    midspan_moment_knm: float = 22890.0
    span_0_3l_moment_knm: float = 19490.0
    shear_at_deff_kn: float = 3159.0
    # SLS rare (illustrative companion values from note)
    sls_midspan_moment_knm: float = 16304.0
    sls_0_3l_moment_knm: float = 13891.0


@dataclass(frozen=True)
class ElastomericBearing:
    n_per_support: int = 3
    length_a_mm: float = 450.0
    width_b_mm: float = 350.0
    total_height_t_mm: float = 52.0
    n_elastomer_layers: int = 3
    n_steel_laminates: int = 4
    ti_mm: float = 10.0
    ts_mm: float = 3.0
    side_cover_c_mm: float = 5.0
    te_mm: float = 40.0
    ae_mm2: float = 149600.0
    ar_mm2: float = 143864.0
    g_n_mm2: float = 0.9
    eb_n_mm2: float = 2000.0
    fy_steel_n_mm2: float = 250.0
    vmax_kn: float = 2019.11
    vmin_kn: float = 719.229
    hmax_long_kn: float = 32.5532
    hmax_lat_kn: float = 20.3349
    el_long_mm: float = 7.0
    design_rotation: float = 0.0001


@dataclass(frozen=True)
class WellFoundation:
    """Pier P1 well / shaft geometry (design note)."""

    outer_dia_m: float = 7.50
    inner_dia_m: float = 4.70
    gross_area_m2: float = 26.829
    gross_mi_m4: float = 131.362
    radius_of_gyration_m: float = 2.213
    steining_outer_bars: str = "136–16 mm dia"
    steining_inner_bars: str = "136–16 mm dia"
    steining_ast_total_mm2: float = 54689.0
    hoop_bars: str = "10 mm dia @ 200 mm c/c both faces"
    pier_cap_length_m: float = 7.10


@dataclass(frozen=True)
class StopperDesign:
    grade_concrete: str = "M35"
    grade_steel: str = "Fe500"
    n_stoppers: int = 1
    vu_kn: float = 339.2
    height_mm: float = 500.0
    plan_a_mm: float = 2500.0
    plan_b_mm: float = 1300.0
    force_application_a_mm: float = 750.0
    main_bars: str = "25 mm dia"
    stirrups: str = "12 mm dia"
    effective_depth_mm: float = 425.5


@dataclass
class BridgeDesign:
    """Aggregate design model for the Kunwari River bridge."""

    project: ProjectInfo = field(default_factory=ProjectInfo)
    geometry: SuperstructureGeometry = field(default_factory=SuperstructureGeometry)
    materials: Materials = field(default_factory=Materials)
    levels: Levels = field(default_factory=Levels)
    loading: LoadingParams = field(default_factory=LoadingParams)
    section: VoidedSectionProperties = field(default_factory=VoidedSectionProperties)
    reinforcement: ReinforcementSummary = field(default_factory=ReinforcementSummary)
    forces: FactoredMoments = field(default_factory=FactoredMoments)
    bearing: ElastomericBearing = field(default_factory=ElastomericBearing)
    well: WellFoundation = field(default_factory=WellFoundation)
    stopper: StopperDesign = field(default_factory=StopperDesign)

    def components(self) -> List[str]:
        return [
            "RCC voided slab superstructure (25 m c/c expansion joint)",
            "Elastomeric bearings (3 per support)",
            "Abutments A1 & A2 with pile foundation",
            "Pier P1 with well foundation",
            "Transverse stoppers",
            "Approach slab",
        ]


def default_design() -> BridgeDesign:
    return BridgeDesign()
