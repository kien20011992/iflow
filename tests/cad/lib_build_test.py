#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# dependencies = ["ezdxf>=1.3"]
# ///
"""Build test of the drawing library: draw three sets through CADCraft with
lib/build_mau.py (the townhouse ground floor; the whole townhouse with its
section; the apartment block's basement, ground and typical floors with its
section), then read each file back with the two checkers that are not
CADCraft (scripts/dxf_check.py, scripts/plan_check.py) and with CADCraft's
own audit. No check may fail; warnings are listed.

Exit 77 (skipped) when cadcraft-cli is not installed. Run:
uv run tests/cad/lib_build_test.py
"""
import contextlib
import io
import json
import pathlib
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "skills/cad/lib"))
sys.path.insert(0, str(ROOT / "skills/cad/scripts"))
sys.dont_write_bytecode = True  # leave no __pycache__ inside the skill
import build_mau  # noqa: E402
import dxf_check  # noqa: E402
import plan_check  # noqa: E402
from chay import find_cli  # noqa: E402

SKIP = 77


def audit(cli, dxf):
    """CADCraft's own structure check on the saved file: its error count."""
    r = subprocess.run([cli, "run", str(dxf), "--cmd", "audit {}"], capture_output=True, text=True)
    for line in r.stdout.splitlines():
        if line.startswith("{") and "errors" in line:
            return json.loads(line)["errors"]
    return None


CASES = [  # (name, sample table, drawings kept: None = all)
    ("nhà phố, tầng 1", "pho-da-nang.json", {"plan:L1"}),
    ("nhà phố, ba tầng và mặt cắt", "pho-da-nang.json", None),
    ("chung cư, hầm, tầng 1, tầng điển hình, mặt cắt", "chung-cu-ktdd5.json", None),
]


def main():
    cli = find_cli()
    if cli is None:
        print("skipped: cadcraft-cli không có trên máy")
        return SKIP
    passed = failed = 0
    with tempfile.TemporaryDirectory() as tmp:
        for k, (name, table, keep) in enumerate(CASES):
            d = json.loads((ROOT / "tests/cad/bang-so" / table).read_text(encoding="utf-8"))
            if keep:
                d["drawings"] = [x for x in d["drawings"] if x["id"] in keep]
            params, out = pathlib.Path(tmp) / f"p{k}.json", pathlib.Path(tmp) / f"b{k}.dxf"
            params.write_text(json.dumps(d, ensure_ascii=False), encoding="utf-8")
            log = io.StringIO()
            with contextlib.redirect_stdout(log):
                code = build_mau.main([str(params), str(out)])
            if code != 0 or not out.exists():
                print(log.getvalue())
                print(f"FAIL  {name}: build_mau.py exit {code}")
                failed += 1
                continue
            results = dxf_check.check(str(out), "X-AREA", "A-WALL", "AC1032") + plan_check.check(str(out), d)
            bad = [r for r in results if r["status"] == "fail"]
            for r in bad:
                print(f"FAIL  {name}: {r['title']}: {r['details'][:5]}")
            errors = audit(cli, out)
            if errors:
                print(f"FAIL  {name}: CADCraft audit báo {errors} lỗi")
            ok = not bad and errors == 0
            passed += ok
            failed += not ok
            warned = [r["title"] for r in results if r["status"] == "warn"]
            print(f"{'ok  ' if ok else 'FAIL'} {name}: {len(results) - len(bad)}/{len(results)} phép đạt hoặc cần xem"
                  + (f"; cần xem: {', '.join(warned)}" if warned else ""))
    print(f"{passed} passed, {failed} failed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
