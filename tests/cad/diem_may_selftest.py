#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# dependencies = ["ezdxf>=1.3"]
# ///
"""Self-test of tests/cad/loop/diem_may.py, the machine part of the common
rubric. A small flat drawn with ezdxf (the pair luat_check_selftest.py uses)
is scored, then each planted defect must cost exactly its own item: a stray
entity on layer 0 A2, a missing door A3, a bedroom under the law A4. A broken
number table costs A1, and A3 and A4 with it, since nothing can be checked
against it (the rule thang-chung.md states). CADCraft's audit is left out here (A5 is scored as not run),
so the test runs on machines without CADCraft.

Run: uv run tests/cad/diem_may_selftest.py
"""
import json
import pathlib
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tests/cad"))
sys.path.insert(0, str(ROOT / "tests/cad/loop"))
sys.dont_write_bytecode = True
import diem_may  # noqa: E402
from luat_check_selftest import flat_table, small_bedroom  # noqa: E402
from plan_check_selftest import build, outlines  # noqa: E402

diem_may.run_audit = lambda dxf: "none"  # no CADCraft in the self-test


def scored(tmp, name, d, o, extra=None):
    dxf, params = pathlib.Path(tmp) / f"{name}.dxf", pathlib.Path(tmp) / f"{name}.json"
    build(d, o, str(dxf), extra)
    params.write_text(json.dumps(d, ensure_ascii=False), encoding="utf-8")
    return {k: v["points"] for k, v in diem_may.score(dxf, params)["items"].items()}


def layer0(msp):
    msp.add_line((0, 0), (100, 100))


def no_door(msp):
    for e in msp.query("INSERT"):
        if e.has_attrib("ID") and e.get_attrib_text("ID") == "o2":
            msp.delete_entity(e)


def main():
    passed, failed = [], []

    def expect(ok, what, got=None):
        print(f"{'ok  ' if ok else 'FAIL'} {what}" + ("" if ok else f": {got}"))
        (passed if ok else failed).append(what)

    with tempfile.TemporaryDirectory() as tmp:
        sound = scored(tmp, "sound", flat_table(), outlines())
        expect(sound["A1"] == 4 and sound["A3"] == 6 and sound["A4"] == 4 and sound["A2"] > 0
               and sound["A5"] is None, "bản đúng: A1, A3, A4 đủ điểm, A2 có điểm, A5 bỏ qua", sound)

        bad = flat_table()
        bad["schema"] = "cad-params/9"
        got = scored(tmp, "schema", bad, outlines())
        expect(got["A1"] == 0 and got["A2"] == sound["A2"] and got["A3"] == 0 and got["A4"] == 0,
               "bảng số sai khuôn: mất A1, A3, A4 (không kiểm được), giữ A2", got)

        for name, extra, key in (("layer0", layer0, "A2"), ("no_door", no_door, "A3")):
            got = scored(tmp, name, flat_table(), outlines(), extra)
            others = {k: v for k, v in got.items() if k != key}
            expect(got[key] < sound[key] and others == {k: v for k, v in sound.items() if k != key},
                   f"{name}: chỉ mất {key}", got)

        d, o, _, _ = small_bedroom(flat_table(), outlines())
        got = scored(tmp, "law", d, o)
        expect(got["A4"] == 0, "phòng ngủ dưới luật mất A4", got)

    # Part A is never rescaled: an item that did not run lowers the maximum, not the points.
    rep = diem_may.tally({"A1": (4, ""), "A2": (3.5, ""), "A3": (6, ""), "A4": (4, ""), "A5": (None, "")})
    expect(rep["A"] == 17.5 and rep["of"] == 21, "điểm A không quy đổi; mục chưa chạy giảm mẫu số", rep)
    # CADCraft that ran but printed no readable count scores 0, it does not vanish.
    expect(diem_may.score_item("A5", None)[0] == 0 and diem_may.score_item("A5", "none")[0] is None
           and diem_may.score_item("A5", 0)[0] == 4, "audit không ra số thì 0 điểm, máy không có CADCraft thì chưa chạy")
    # An unreadable input is an error (exit 2), not a low score.
    with tempfile.TemporaryDirectory() as tmp:
        p = pathlib.Path(tmp) / "bad.json"
        p.write_text("{", encoding="utf-8")
        code = diem_may.main([str(p), str(p)])
    expect(code == 2, "file đầu vào hỏng thì thoát mã 2", code)

    # Lines outside the drawing library: a copy with two lines changed and one added.
    base = diem_may.BUILD_MAU.read_text(encoding="utf-8").splitlines()
    mine = base[:10] + ["x = 1", "y = 2", "z = 3"] + base[12:]
    with tempfile.TemporaryDirectory() as tmp:
        p = pathlib.Path(tmp) / "build.py"
        p.write_text("\n".join(mine) + "\n", encoding="utf-8")
        o = diem_may.outside_library(p)
    expect(o["changed_or_added"] == 3 and o["lines"] == len(mine) and o["library_lines_dropped"] == 2,
           "đếm đúng dòng vẽ ngoài thư viện và dòng thư viện bị bỏ", o)

    print(f"{len(passed)} passed, {len(failed)} failed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
