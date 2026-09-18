"""SVG drawings for Kunwari River voided-slab bridge."""

from __future__ import annotations

from pathlib import Path


def deck_cross_section_svg() -> str:
    """
    Transverse cross-section of RCC voided slab (dimensions from design note p.5).
    Overall width 8.4 m, depth 1.2 m, 4 × Ø0.6 m voids.
    """
    # Scale: 1 m = 80 px; origin top-left with margins
    s = 80
    margin = 60
    W = 8.4 * s
    H = 1.2 * s
    total_w = int(W + 2 * margin)
    total_h = int(H + 2 * margin + 80)

    # Web / void layout: soffit web 5.1 m centred; voids Ø0.6 with 0.6 gaps
    # From left: cantilever 1.65 m each side approx ( (8.4-5.1)/2 = 1.65 )
    # Note shows cantilevers 1.35 taper + edge details; use 8.4 overall.

    voids = []
    # Place 4 voids centred in 5.1 m web band
    web_left = margin + (8.4 - 5.1) / 2 * s
    # void centres: start after edge distance; pattern dia + gap
    # Approximate equal spacing in web: centres at web_left + 0.75 + i*1.2
    for i in range(4):
        cx = web_left + (0.75 + i * 1.2) * s
        cy = margin + 0.6 * s  # mid-depth of 1.2 m slab (void centre)
        voids.append((cx, cy, 0.3 * s))

    void_circles = "\n".join(
        f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" fill="#f7f3ea" stroke="#1f3a5f" stroke-width="2"/>'
        for cx, cy, r in voids
    )

    # Tapered cantilever outline (simplified polygon)
    # Top slab full width; soffit narrower with tapers
    top_y = margin
    bot_y = margin + H
    tip_t = 0.15 * s
    # Outer profile
    poly = (
        f"{margin},{top_y} "
        f"{margin + W},{top_y} "
        f"{margin + W},{top_y + tip_t} "
        f"{margin + W - 1.35 * s},{bot_y} "
        f"{margin + 1.35 * s},{bot_y} "
        f"{margin},{top_y + tip_t}"
    )

    return f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{total_w}" height="{total_h}" viewBox="0 0 {total_w} {total_h}">
  <defs>
    <linearGradient id="deckFill" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#d9e2ec"/>
      <stop offset="100%" stop-color="#bcccdc"/>
    </linearGradient>
  </defs>
  <rect width="100%" height="100%" fill="#f5f7fa"/>
  <text x="{margin}" y="28" font-family="Georgia, serif" font-size="18" fill="#102a43">
    Kunwari River – RCC Voided Slab Cross-Section
  </text>
  <text x="{margin}" y="48" font-family="Georgia, serif" font-size="12" fill="#486581">
    Deck 8.4 m × 1.2 m | 4 Ø 0.6 m voids | Carriageway 7.5 m | MP PWD
  </text>
  <polygon points="{poly}" fill="url(#deckFill)" stroke="#102a43" stroke-width="2.5"/>
  {void_circles}
  <!-- Dimension: overall width -->
  <line x1="{margin}" y1="{bot_y + 28}" x2="{margin + W}" y2="{bot_y + 28}" stroke="#334e68" stroke-width="1.5"/>
  <text x="{margin + W/2}" y="{bot_y + 48}" text-anchor="middle" font-family="Georgia, serif" font-size="13" fill="#334e68">8.40 m</text>
  <!-- Depth -->
  <line x1="{margin + W + 20}" y1="{top_y}" x2="{margin + W + 20}" y2="{bot_y}" stroke="#334e68" stroke-width="1.5"/>
  <text x="{margin + W + 28}" y="{margin + H/2}" font-family="Georgia, serif" font-size="13" fill="#334e68">1.20 m</text>
  <text x="{margin}" y="{total_h - 16}" font-family="Georgia, serif" font-size="11" fill="#829ab1">
    As per DESIGN-MPPWD-JPSG-KUWARI_RIVER-R0-2P · voids 18.52% &lt; 40% (IRC SP 64)
  </text>
</svg>
'''


def longitudinal_elevation_svg() -> str:
    """Simple longitudinal elevation of one 25 m expansion-joint span unit."""
    s = 25  # px per m
    margin = 50
    L = 25.0 * s
    depth = 1.2 * s
    bearing = 0.5 * s
    total_w = int(L + 2 * margin)
    total_h = 220
    deck_y = 80
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{total_w}" height="{total_h}" viewBox="0 0 {total_w} {total_h}">
  <rect width="100%" height="100%" fill="#f5f7fa"/>
  <text x="{margin}" y="28" font-family="Georgia, serif" font-size="18" fill="#102a43">
    Longitudinal Elevation – Span Unit (c/c Exp. Joint = 25 m)
  </text>
  <text x="{margin}" y="48" font-family="Georgia, serif" font-size="12" fill="#486581">
    Effective span c/c bearings = 24.0 m · Simply supported voided slab
  </text>
  <!-- Deck -->
  <rect x="{margin}" y="{deck_y}" width="{L}" height="{depth}" fill="#bcccdc" stroke="#102a43" stroke-width="2"/>
  <!-- Bearings -->
  <rect x="{margin + bearing - 8}" y="{deck_y + depth}" width="16" height="12" fill="#334e68"/>
  <rect x="{margin + L - bearing - 8}" y="{deck_y + depth}" width="16" height="12" fill="#334e68"/>
  <!-- Supports -->
  <rect x="{margin + bearing - 30}" y="{deck_y + depth + 12}" width="60" height="40" fill="#829ab1" stroke="#102a43"/>
  <rect x="{margin + L - bearing - 30}" y="{deck_y + depth + 12}" width="60" height="40" fill="#829ab1" stroke="#102a43"/>
  <!-- Dims -->
  <line x1="{margin}" y1="190" x2="{margin + L}" y2="190" stroke="#334e68"/>
  <text x="{margin + L/2}" y="208" text-anchor="middle" font-family="Georgia, serif" font-size="13" fill="#334e68">25.00 m (c/c expansion joint)</text>
  <line x1="{margin + bearing}" y1="170" x2="{margin + L - bearing}" y2="170" stroke="#d64545" stroke-dasharray="4 3"/>
  <text x="{margin + L/2}" y="165" text-anchor="middle" font-family="Georgia, serif" font-size="12" fill="#d64545">24.00 m (c/c bearings)</text>
</svg>
'''


def write_drawings(out_dir: str | Path) -> list[Path]:
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    files = {
        "deck_cross_section.svg": deck_cross_section_svg(),
        "longitudinal_elevation.svg": longitudinal_elevation_svg(),
    }
    paths = []
    for name, content in files.items():
        p = out / name
        p.write_text(content)
        paths.append(p)
    return paths
