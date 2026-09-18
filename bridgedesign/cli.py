"""CLI entry points for the Kunwari River bridge design package."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

# Allow running as `python -m bridgedesign.cli` from repo root
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT.parent) not in sys.path:
    sys.path.insert(0, str(ROOT.parent))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Kunwari River submersible bridge design toolkit (MP PWD design note)"
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_report = sub.add_parser("report", help="Generate design summary markdown + drawings + JSON")
    p_report.add_argument(
        "--out-root",
        type=Path,
        default=Path(__file__).resolve().parent,
        help="bridgedesign package root (default: this package)",
    )

    sub.add_parser("check", help="Run key verification checks and print status")

    p_json = sub.add_parser("json", help="Print design data JSON to stdout")
    p_json.add_argument("--pretty", action="store_true")

    args = parser.parse_args(argv)

    if args.cmd == "report":
        from bridgedesign.reports.generate import build_all_outputs

        result = build_all_outputs(args.out_root)
        print(f"Report: {result['report']}")
        for d in result["drawings"]:
            print(f"Drawing: {d}")
        print(f"JSON keys: {', '.join(result['data_keys'])}")
        return 0

    if args.cmd == "check":
        from bridgedesign.calc import (
            check_bearing,
            check_steining,
            check_void_percentage,
            deflection_limit,
            design_cantilever,
            midspan_design_per_metre,
        )

        void = check_void_percentage()
        flex = midspan_design_per_metre()
        cant = design_cantilever()
        bearing_ok = all(c.ok for c in check_bearing())
        well = check_steining()
        deflect = deflection_limit()

        rows = [
            ("Void percentage (IRC SP 64)", void.normal_calculation_ok, void.message),
            ("Deck mid-span flexure Ast", flex.capacity_ok, flex.message),
            ("Cantilever reinforcement", cant.ok, cant.bars),
            ("Elastomeric bearing", bearing_ok, "See bearing checks"),
            ("Well steining", well.ok, well.messages[-1] if well.messages else ""),
            ("Service deflection", deflect["ok"], f"δ={deflect['max_deflection_70rw_mm']} mm"),
        ]
        all_ok = True
        for name, ok, detail in rows:
            status = "PASS" if ok else "FAIL"
            all_ok = all_ok and ok
            print(f"[{status}] {name}: {detail}")
        return 0 if all_ok else 1

    if args.cmd == "json":
        from bridgedesign.data import export_design_json

        data = export_design_json()
        print(json.dumps(data, indent=2 if args.pretty else None))
        return 0

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
