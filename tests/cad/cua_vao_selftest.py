#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# dependencies = ["ezdxf>=1.3"]
# ///
"""Self-test of skills/cad/scripts/cua_vao.py, the skill's one door for input:
the townhouse brief is accepted; the two studio briefs are turned away at the
plot (it exists only on the brief's map); each planted defect is turned away
for its own reason; DXF files built here with ezdxf are judged by units,
layer and closure; a PDF and a photo are turned away with what to bring.

Run: uv run tests/cad/cua_vao_selftest.py
"""
import copy
import json
import pathlib
import sys
import tempfile

import ezdxf

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "skills/cad/scripts"))
sys.dont_write_bytecode = True  # leave no __pycache__ inside the skill
from cua_vao import check_brief, check_dxf, main  # noqa: E402

BRIEFS = ROOT / "tests/cad/phieu"


def brief(name):
    return json.loads((BRIEFS / f"{name}.json").read_text(encoding="utf-8"))


def site_dxf(path, units=4, layer="C-PROP", closed=True, walls=False, extra=None):
    doc = ezdxf.new("R2018", units=units)
    for name in (layer, "A-WALL"):
        if name not in doc.layers:
            doc.layers.add(name)
    msp = doc.modelspace()
    msp.add_lwpolyline([(0, 0), (5000, 0), (5000, 20000), (0, 20000)], close=closed, dxfattribs={"layer": layer})
    if walls:
        msp.add_lwpolyline([(0, 0), (5000, 0), (5000, 200), (0, 200)], close=True, dxfattribs={"layer": "A-WALL"})
    if extra:
        extra(msp)
    doc.saveas(path)


def main_test():
    passed, failed = [], []

    def expect(ok, what, got=None):
        print(f"{'ok  ' if ok else 'FAIL'} {what}" + ("" if ok else f": {got}"))
        (passed if ok else failed).append(what)

    expect(check_brief(brief("pho-da-nang")) == [], "phiếu nhà phố được nhận", check_brief(brief("pho-da-nang")))
    for name in ("chung-cu-ktdd5", "bnb-ktdd5"):
        got = check_brief(brief(name))
        expect([f for f, _ in got] == ["site"], f"phiếu {name} bị chặn đúng ở khu đất, và chỉ ở đó", got)

    def planted(name, change, field):
        d = copy.deepcopy(brief(name))
        change(d)
        got = check_brief(d)
        expect([f for f, _ in got] == [field], f"bản hỏng: {field} ({name})", got)

    planted("pho-da-nang", lambda d: d.pop("rooms_needed"), "rooms_needed")
    planted("pho-da-nang", lambda d: d["site"].update(by="model"), "site")
    planted("pho-da-nang", lambda d: d["site"].update(value={"edges_mm": [5000, 20000]}), "site")
    planted("pho-da-nang", lambda d: d.update(floors_wanted={"value": "ba", "by": "user"}), "floors_wanted")
    planted("pho-da-nang", lambda d: d.update(stret_width_mm={"value": 7000, "by": "user"}), "stret_width_mm")
    planted("pho-da-nang", lambda d: d.update(street_width_mm={"value": 7000, "by": "model"}), "street_width_mm")
    planted("pho-da-nang", lambda d: d["site"].pop("by"), "site")
    planted("pho-da-nang", lambda d: d["type"].update(value=["house"]), "type")
    planted("pho-da-nang", lambda d: d["setbacks"]["value"].append({"edge": 9, "mm": 100}), "setbacks")

    def flat(d):  # a flat to renovate: no plot, but its existing plan is required
        d["type"]["value"] = "apartment"
        d["work"]["value"] = "renovation"
        d.pop("site")
        d.pop("occupants")
        d.pop("floors_wanted")
        d["keep_untouched"] = {"value": ["cột", "hộp kỹ thuật"], "by": "user"}
    planted("pho-da-nang", flat, "existing_dxf")
    planted("chung-cu-ktdd5", lambda d: (d["site"].update(value={"edges_mm": [66200, 29400, 66200, 29400]},
                                                          by="user", pending=False), d.pop("floors")), "floors")
    planted("bnb-ktdd5", lambda d: (d["site"].update(value={"from_dxf": "khu-dat-2.dxf"}, by="user",
                                                     pending=False), d["stars"].update(value=7)), "stars")

    with tempfile.TemporaryDirectory() as tmp:
        t = pathlib.Path(tmp)
        def old_style(msp):  # a closed 2D POLYLINE is a valid boundary
            for e in list(msp.query('LWPOLYLINE[layer=="C-PROP"]')):
                msp.delete_entity(e)
            msp.add_polyline2d([(0, 0), (5000, 0), (5000, 20000), (0, 20000)], close=True,
                               dxfattribs={"layer": "C-PROP"})

        def repeated_first(msp):  # closed by repeating the first point, flag not set
            for e in list(msp.query('LWPOLYLINE[layer=="C-PROP"]')):
                msp.delete_entity(e)
            msp.add_lwpolyline([(0, 0), (5000, 0), (5000, 20000), (0, 20000), (0, 0)], dxfattribs={"layer": "C-PROP"})

        cases = [("đúng", dict(), []), ("sai đơn vị", dict(units=6), ["units"]),
                 ("ranh hở", dict(closed=False), ["C-PROP"]), ("sai layer", dict(layer="0"), ["layers"]),
                 ("có cả ranh và tường", dict(walls=True), []),
                 ("ranh kiểu POLYLINE cũ", dict(extra=old_style), []),
                 ("ranh khép bằng điểm lặp", dict(extra=repeated_first), []),
                 ("ranh tự cắt", dict(extra=lambda m: (
                     [m.delete_entity(e) for e in list(m.query('LWPOLYLINE[layer=="C-PROP"]'))],
                     m.add_lwpolyline([(0, 0), (5000, 20000), (5000, 0), (0, 20000)], close=True,
                                      dxfattribs={"layer": "C-PROP"}))), ["C-PROP"]),
                 ("hai đường ranh", dict(extra=lambda m: m.add_lwpolyline(
                     [(0, 0), (100, 0), (100, 100)], close=True, dxfattribs={"layer": "C-PROP"})), ["C-PROP"]),
                 ("ranh có nét rời", dict(extra=lambda m: m.add_line((0, 0), (10, 10),
                                                                     dxfattribs={"layer": "C-PROP"})), ["C-PROP"]),
                 ("tường hở", dict(extra=lambda m: m.add_lwpolyline([(0, 0), (100, 0), (100, 100)],
                                                                    dxfattribs={"layer": "A-WALL"})), ["A-WALL"])]
        for name, kw, want in cases:
            path = t / f"{name}.dxf"
            site_dxf(path, **kw)
            got = check_dxf(str(path))
            expect([f for f, _ in got] == want, f"DXF {name}", got)
        for name in ("ban-ve.pdf", "anh-khu-dat.jpg"):
            path = t / name
            path.write_bytes(b"x")
            code = main([str(path)])
            expect(code == 1, f"{name} bị chặn kèm lời dặn", code)
        expect(main([str(t / "khong-co.png")]) == 2, "đường dẫn sai: không đọc được, không phải bị chặn")
    print(f"{len(passed)} passed, {len(failed)} failed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main_test())
