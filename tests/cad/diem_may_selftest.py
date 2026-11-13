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


def scored_paths(tmp, name):
    return pathlib.Path(tmp) / f"{name}.dxf", pathlib.Path(tmp) / f"{name}.json"


def report(tmp, name, d, o, extra=None):
    dxf, params = scored_paths(tmp, name)
    build(d, o, str(dxf), extra)
    params.write_text(json.dumps(d, ensure_ascii=False), encoding="utf-8")
    return diem_may.score(dxf, params)


def scored(tmp, name, d, o, extra=None):
    return {k: v["points"] for k, v in report(tmp, name, d, o, extra)["items"].items()}


def layer0(msp):
    msp.add_line((0, 0), (100, 100))


def two_clouds(msp):
    msp.doc.layers.add("A-REVS")
    for x in (0, 3000):
        msp.add_lwpolyline([(x, 0), (x + 500, 0), (x + 500, 500), (x, 500)], close=True,
                           dxfattribs={"layer": "A-REVS"})
    # CADCraft may close a cloud by repeating its first point instead of setting the flag.
    msp.add_lwpolyline([(6000, 0), (6500, 0), (6500, 500), (6000, 0)], dxfattribs={"layer": "A-REVS"})
    msp.add_mtext("chưa vẽ: thang t1", dxfattribs={"layer": "A-REVS", "insert": (0, 600)})


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

        # Clouds left for what the library could not draw are counted, never scored.
        h = report(tmp, "clouds", flat_table(), outlines(), two_clouds)["handed_back"]
        base = diem_may.score(*scored_paths(tmp, "sound"))["handed_back"]
        expect(h["clouds"] == 3 and base["clouds"] == 0 and h["table_items"] == base["table_items"] > 0
               and h["share"] == round(3 / h["table_items"], 3),
               "đếm đám mây bị giao lại, kể cả đám mây khép bằng điểm đầu lặp lại", h)

        d, o, _, _ = small_bedroom(flat_table(), outlines())
        got = scored(tmp, "law", d, o)
        expect(got["A4"] == 0, "phòng ngủ dưới luật mất A4", got)

    # The "Chưa vẽ" list of a build log: only the last run's list counts.
    with tempfile.TemporaryDirectory() as tmp:
        log = pathlib.Path(tmp) / "build.log"
        log.write_text("cadcraft-cli: mã thoát 0\nChưa vẽ:\n  - cũ\ncadcraft-cli: mã thoát 0\nChưa vẽ:\n  - hình site\n"
                       "  - L1: nhãn DS của cv không có chỗ\n  - L1: Lối xe xuống hầm (ram dốc)\n"
                       "  - L2: diện tích Sảnh tính cả 13.52 m² cột hay ô trống đứng giữa phòng\n", encoding="utf-8")
        g = diem_may.handed_back_log(log)
        clean = pathlib.Path(tmp) / "clean.log"  # a clean last run leaves nothing from the run before
        clean.write_text("cadcraft-cli: mã thoát 0\nChưa vẽ:\n  - cũ\ncadcraft-cli: mã thoát 0\n", encoding="utf-8")
        g16 = pathlib.Path(tmp) / "utf16.log"  # Windows PowerShell 5.1 writes UTF-16 with a byte-order mark
        g16.write_text("Chưa vẽ:\n  - hình site\n", encoding="utf-16")
        clean_g, utf16_g = diem_may.handed_back_log(clean), diem_may.handed_back_log(g16)
    expect(clean_g["listed"] == 0 and utf16_g["listed"] == 1, "lần dựng cuối sạch thì danh sách rỗng; đọc được log UTF-16",
           (clean_g, utf16_g))
    expect(g == {"listed": 4, "text_no_spot": 1, "assumed": 0, "area_note": 1, "needs_eye": 0, "undrawn": 2,
                 "drawings": 1}, "đọc danh sách chưa vẽ của lần dựng cuối", g)

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
