# Kunwari River Submersible Bridge — Design Package

Digitised bridge design prepared from MP PWD design note
**DESIGN-MPPWD-JPSG-KUWARI_RIVER-R0-2P** (Rev. 09-01-2024):

> Construction of Submersible Bridge across Kunwari River on Sujangharhi Road, Dist. Morena — RCC voided slab (span c/c expansion joint = 25 m).

## Design snapshot

| Item | Value |
|------|-------|
| Structural system | Simply supported RCC voided slab |
| Span c/c bearings / exp. joint | 24.0 m / 25.0 m |
| Deck size | 8.4 m wide × 1.2 m thick |
| Carriageway | 7.5 m (2 lanes) |
| Voids | 4 × Ø 0.6 m (18.52% < 40% → IRC SP 64 normal calc.) |
| Materials | Deck/pier M35, abutment M30, Fe 500 |
| Live load | IRC Class A & 70R wheeled |
| Bearings | 3 × 450×350×52 mm elastomeric pads / support |
| Substructure | Abutments A1/A2 (piles) + Pier P1 (well Ø7.5 / 4.7 m) |

## Package layout

```
bridgedesign/
  data/          # Geometry, materials, forces, reinforcement
  calc/          # Void, flexure, cantilever, bearing, temperature, well checks
  staad/         # STAAD.Pro input reconstructed from the design note
  drawings/      # SVG cross-section & elevation generators
  reports/       # Design summary generator
  tests/         # Verification tests against design-note values
docs/source/     # Source design-note PDF
```

## Quick start

```bash
# From repository root
python3 -m bridgedesign.cli check      # Run key verifications
python3 -m bridgedesign.cli report     # Write summary, JSON, SVG drawings
python3 -m bridgedesign.cli json --pretty

# Tests
python3 -m pytest bridgedesign/tests -q
```

## Outputs

After `report`:

- `bridgedesign/reports/DESIGN_SUMMARY.md` — consolidated design summary
- `bridgedesign/data/design_data.json` — machine-readable parameters
- `bridgedesign/drawings/out/*.svg` — deck section & longitudinal elevation
- `bridgedesign/staad/*.std` — analysis / load-test models

## Codes referenced

IRC:6-2017 · IRC:112-2011 · IRC:78 · IRC SP 64:2016 · MoRTH

## Disclaimer

This repository encodes the **approved design-note values and checks** for review,
detailing, and reproducibility. Final IFC / construction drawings shall follow
client-approved GA drawings; re-run STAAD.Pro on the provided decks before relying
on analysis numbers for construction.
