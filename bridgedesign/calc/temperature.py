"""Temperature load effects on deck (IRC:6), as in design note §3.2."""

from __future__ import annotations

from dataclasses import dataclass

from bridgedesign.data.parameters import LoadingParams, Materials


@dataclass
class TemperatureResult:
    max_air_shade_c: float
    min_air_shade_c: float
    mean_c: float
    bridge_temp_assumed_c: float
    temp_rise_c: float
    temp_fall_c: float
    axial_force_kn: float
    moment_knm: float
    note: str


def effective_bridge_temperature(loading: LoadingParams | None = None) -> TemperatureResult:
    loading = loading or LoadingParams()
    mean = 0.5 * (loading.max_air_shade_temp_c + loading.min_air_shade_temp_c)
    # Design note: bridge temperature assumed = 33.75°C (mean + 10°C allowance)
    bridge = loading.temp_rise_fall_c
    return TemperatureResult(
        max_air_shade_c=loading.max_air_shade_temp_c,
        min_air_shade_c=loading.min_air_shade_temp_c,
        mean_c=mean,
        bridge_temp_assumed_c=bridge,
        temp_rise_c=bridge,
        temp_fall_c=-bridge,
        # Documented gradient effects SF=88.39 t? / M=37.822 — stored as note values in kN/kNm
        axial_force_kn=88.39 * 9.80665,  # if in tonne; design STAAD uses FX ±867.1 kN
        moment_knm=37.822 * 9.80665,
        note=(
            "Uniform ±33.75°C and temperature gradient considered; "
            "STAAD joint loads FX=±867.1 kN, MZ=±371.03 kNm (rise)."
        ),
    )


def thermal_movement_mm(
    length_m: float = 24.0,
    delta_t_c: float = 25.0,
    alpha: float | None = None,
) -> float:
    """Free thermal movement δ = α L ΔT (bearing design uses ±25°C)."""
    alpha = alpha if alpha is not None else Materials().alpha_thermal
    return alpha * length_m * 1000.0 * delta_t_c
