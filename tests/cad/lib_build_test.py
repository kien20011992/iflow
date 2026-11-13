#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# dependencies = ["ezdxf>=1.3"]
# ///
"""Build test of the drawing library: draw the ground floor of
tests/cad/bang-so/pho-da-nang.json through CADCraft with lib/build_mau.py,
then read the file back with the two checkers that are not CADCraft
(scripts/dxf_check.py and scripts/plan_check.py). No check may fail.

Exit 77 (skipped) when cadcraft-cli is not installed. Run:
uv run tests/cad/lib_build_test.py
"""
import contextlib
import io
import json
import pathlib
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


def main():
    if find_cli() is None:
        print("skipped: cadcraft-cli không có trên máy")
        return SKIP
    d = json.loads((ROOT / "tests/cad/bang-so/pho-da-nang.json").read_text(encoding="utf-8"))
    d["drawings"] = [x for x in d["drawings"] if x["id"] == "plan:L1"]
    with tempfile.TemporaryDirectory() as tmp:
        params, out = pathlib.Path(tmp) / "params.json", pathlib.Path(tmp) / "pho.dxf"
        params.write_text(json.dumps(d, ensure_ascii=False), encoding="utf-8")
        log = io.StringIO()
        with contextlib.redirect_stdout(log):
            code = build_mau.main([str(params), str(out)])
        if code != 0 or not out.exists():
            print(log.getvalue())
            print(f"FAIL  build_mau.py exit {code}")
            print("0 passed, 1 failed")
            return 1
        failed = []
        results = dxf_check.check(str(out), "X-AREA", "A-WALL", "AC1032") + plan_check.check(str(out), d)
        for r in results:
            if r["status"] == "fail":
                failed.append(r)
                print(f"FAIL  {r['title']}: {r['details']}")
        warned = [r["title"] for r in results if r["status"] == "warn"]
        print(f"{len(results) - len(failed)} passed, {len(failed)} failed"
              + (f" ({len(warned)} cần xem: {', '.join(warned)})" if warned else ""))
        return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
