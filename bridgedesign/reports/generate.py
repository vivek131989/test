"""Generate a design summary report from the encoded design note."""

from __future__ import annotations

from pathlib import Path

from bridgedesign.calc import (
    bearing_size_label,
    check_bearing,
    check_steining,
    check_void_percentage,
    deflection_limit,
    design_cantilever,
    effective_bridge_temperature,
    midspan_design_per_metre,
    thermal_movement_mm,
)
from bridgedesign.data.parameters import default_design
from bridgedesign.drawings.svg import write_drawings


def generate_markdown_report(out_path: str | Path) -> Path:
    d = default_design()
    void = check_void_percentage()
    flex = midspan_design_per_metre()
    cant = design_cantilever()
    bearings = check_bearing()
    temp = effective_bridge_temperature()
    well = check_steining()
    deflect = deflection_limit()
    movement = thermal_movement_mm()

    lines = [
        f"# Design Summary — {d.project.title}",
        "",
        f"**Client:** {d.project.client}  ",
        f"**Job:** {d.project.job_name}  ",
        f"**Document:** {d.project.document_ref}  ",
        f"**Revision date:** {d.project.revision_date}  ",
        "",
        "## 1. Scope",
        "",
        "This package digitises the MP PWD design note for the Kunwari River "
        "submersible bridge (RCC voided slab, 25 m c/c expansion joint). "
        "Key geometry, loads, STAAD inputs, and verification checks are "
        "reproduced for design review and downstream detailing.",
        "",
        "### Components",
        "",
    ]
    for c in d.components():
        lines.append(f"- {c}")

    lines += [
        "",
        "## 2. Geometry & materials",
        "",
        "| Item | Value |",
        "|------|-------|",
        f"| Span c/c bearings | {d.geometry.span_cc_bearing_m:.2f} m |",
        f"| Span c/c expansion joint | {d.geometry.span_cc_exp_joint_m:.2f} m |",
        f"| Slab thickness | {d.geometry.slab_thickness_m:.3f} m |",
        f"| Deck / carriageway width | {d.geometry.deck_width_m:.2f} / {d.geometry.carriageway_width_m:.2f} m |",
        f"| Voids | {d.geometry.n_voids} × Ø {d.geometry.void_diameter_m:.2f} m |",
        f"| Deck concrete / steel | {d.materials.deck_concrete_grade} / {d.materials.steel_grade} |",
        f"| Abutment concrete | {d.materials.abutment_concrete_grade} |",
        f"| Pier / well concrete | {d.materials.pier_concrete_grade} |",
        "",
        f"**Void check:** {void.message}",
        "",
        "## 3. Loads (IRC:6)",
        "",
        f"- Live load: {', '.join(d.loading.live_loads)}",
        f"- Impact factor (slab): {d.loading.impact_factor_slab}",
        f"- Temperature rise/fall: ±{d.loading.temp_rise_fall_c} °C "
        f"(max shade {temp.max_air_shade_c} °C, min {temp.min_air_shade_c} °C)",
        f"- Free thermal movement (±25 °C on 24 m): {movement:.1f} mm",
        f"- Seismic Zone {d.loading.seismic_zone} (Z={d.loading.zone_factor_z})",
        "",
        "## 4. Factored deck forces (STAAD / design note §3.4)",
        "",
        "| Location | Value |",
        "|----------|-------|",
        f"| Mid-span moment | {d.forces.midspan_moment_knm:.0f} kN·m |",
        f"| 0.3L moment | {d.forces.span_0_3l_moment_knm:.0f} kN·m |",
        f"| Shear at d_eff | {d.forces.shear_at_deff_kn:.0f} kN |",
        "",
        f"**Flexure (per metre strip):** {flex.message}  ",
        f"Provided Ast (bottom mid-span) = {d.reinforcement.mid_bot_ast_prov_mm2_m:.0f} mm²/m "
        f"({d.reinforcement.mid_bot_bars}) — "
        f"{'OK' if d.reinforcement.mid_bot_ast_prov_mm2_m >= d.reinforcement.mid_bot_ast_req_mm2_m else 'CHECK'}",
        "",
        "## 5. Reinforcement summary (deck)",
        "",
        "| Location | Required | Provided | Detail |",
        "|----------|----------|----------|--------|",
        f"| Top mid-span | {d.reinforcement.mid_top_ast_req_mm2_m:.0f} mm²/m | "
        f"{d.reinforcement.mid_top_ast_prov_mm2_m:.0f} mm²/m | {d.reinforcement.mid_top_bars} |",
        f"| Bottom mid-span | {d.reinforcement.mid_bot_ast_req_mm2_m:.0f} mm²/m | "
        f"{d.reinforcement.mid_bot_ast_prov_mm2_m:.0f} mm²/m | {d.reinforcement.mid_bot_bars} |",
        f"| Distribution | {d.reinforcement.dist_ast_req_mm2_m:.0f} mm²/m | "
        f"{d.reinforcement.dist_ast_prov_mm2_m:.0f} mm²/m | {d.reinforcement.dist_bars} |",
        f"| Shear links | — | — | {d.reinforcement.shear_links} |",
        f"| Cantilever top | {cant.ast_req_mm2:.0f} mm² | {cant.ast_prov_mm2:.0f} mm² | {cant.bars} |",
        "",
        "## 6. Elastomeric bearings",
        "",
        f"- Arrangement: **{d.bearing.n_per_support} bearings / support**",
        f"- Size: **{bearing_size_label()}**",
        f"- Vmax / Vmin: {d.bearing.vmax_kn:.1f} / {d.bearing.vmin_kn:.1f} kN",
        "",
        "| Check | Value | Limit | Status | Clause |",
        "|-------|-------|-------|--------|--------|",
    ]
    for ch in bearings:
        if ch.limit == 0.0 and ch.unit == "-":
            continue
        lines.append(
            f"| {ch.name} | {ch.value} {ch.unit} | {ch.limit} {ch.unit} | "
            f"{'OK' if ch.ok else 'FAIL'} | {ch.clause} |"
        )

    lines += [
        "",
        "## 7. Substructure snapshot",
        "",
        "### Abutments A1 & A2",
        f"- Cap top / bottom RL: {d.levels.abutment_cap_top} / {d.levels.abutment_cap_bottom} m",
        f"- Pile cap bottom RL: {d.levels.pile_cap_bottom} m | Scour RL: {d.levels.scour_level} m",
        f"- Concrete grade: {d.materials.abutment_concrete_grade}",
        "",
        "### Pier P1 – well foundation",
        f"- Well OD / ID: {d.well.outer_dia_m} / {d.well.inner_dia_m} m "
        f"(Ag = {well.gross_area_m2} m²)",
        f"- Steining long. steel: {d.well.steining_outer_bars} outer + "
        f"{d.well.steining_inner_bars} inner (total {well.ast_total_prov_mm2:.0f} mm²)",
        f"- Hoops: {d.well.hoop_bars}",
    ]
    for m in well.messages:
        lines.append(f"- {m}")

    lines += [
        "",
        "### Stoppers",
        f"- Design shear Vu = {d.stopper.vu_kn} kN | {d.stopper.main_bars} main / {d.stopper.stirrups} stirrups",
        "",
        "## 8. Service deflection (load-test annex)",
        "",
        f"- Permissible (span/800, as tabulated): {deflect['documented_limit_mm']} mm",
        f"- Max deflection 70R wheeled: {deflect['max_deflection_70rw_mm']} mm",
        f"- Max deflection 2×Class A: {deflect['max_deflection_2a_mm']} mm",
        f"- Status: **{'OK' if deflect['ok'] else 'CHECK'}**",
        "",
        "## 9. Reference codes",
        "",
    ]
    for code in d.project.codes:
        lines.append(f"- {code}")

    lines += [
        "",
        "## 10. Artefacts in this repository",
        "",
        "- `bridgedesign/data/` — design parameters",
        "- `bridgedesign/calc/` — verification calculators",
        "- `bridgedesign/staad/` — STAAD.Pro input files",
        "- `bridgedesign/drawings/` — SVG section / elevation",
        "- `docs/source/` — source design-note PDF",
        "",
        "---",
        "*Generated by the `bridgedesign` package. Construction drawings and bar-bending "
        "schedules shall follow approved GA drawings; re-run STAAD before IFC.*",
        "",
    ]

    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(lines))
    return out_path


def build_all_outputs(root: str | Path | None = None) -> dict:
    root = Path(root) if root else Path(__file__).resolve().parents[1]
    report = generate_markdown_report(root / "reports" / "DESIGN_SUMMARY.md")
    drawings = write_drawings(root / "drawings" / "out")
    from bridgedesign.data import export_design_json

    data = export_design_json(root / "data" / "design_data.json")
    return {"report": report, "drawings": drawings, "data_keys": list(data.keys())}
