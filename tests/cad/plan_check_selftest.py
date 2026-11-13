#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# dependencies = ["ezdxf>=1.3"]
# ///
"""Self-test of skills/cad/scripts/plan_check.py: a small two-storey house as a
number table, a drawing of it built here with ezdxf (never by the skill's
drawing library), and one copy per planted defect. The sound pair must pass
every check; each defect must make its own check fail (or ask for a look,
for the stacking check), and leave the other checks as they were.

Run: uv run tests/cad/plan_check_selftest.py
"""
import copy
import math
import pathlib
import sys
import tempfile

import ezdxf

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "skills/cad/scripts"))
sys.dont_write_bytecode = True  # leave no __pycache__ inside the skill
import params_check  # noqa: E402
from plan_check import check, flatten, resolve  # noqa: E402

ORIGIN = {"L1": (0, 0), "L2": (20000, 0)}


def P(xn, xo, yn, yo):
    return [[xn, xo], [yn, yo]]


def W(i, t, a, b, align="center"):
    return {"id": i, "type": t, "from": a, "to": b, "align": align}


def shell(extra_walls):
    cols = [{"id": f"c{k}", "type": "C", "at": P(x, ox, y, oy)}
            for k, (x, ox, y, oy) in enumerate([("1", 100, "A", 100), ("3", -100, "A", 100),
                                                ("1", 100, "C", -100), ("3", -100, "C", -100)])]
    return [W("wA", "ext", P("1", 0, "A", 0), P("3", 0, "A", 0), "left"),
            W("wC", "ext", P("1", 0, "C", 0), P("3", 0, "C", 0), "right"),
            W("w1", "ext", P("1", 0, "A", 0), P("1", 0, "C", 0), "right"),
            W("w3", "ext", P("3", 0, "A", 0), P("3", 0, "C", 0), "left"),
            W("wB", "int", P("1", 0, "B", 0), P("3", 0, "B", 0))] + extra_walls, cols


def table():
    w1, c1 = shell([W("w2", "virtual", P("2", 0, "B", 0), P("2", 0, "C", 0))])
    w2, c2 = shell([W("w2", "int", P("2", 0, "B", 0), P("2", 0, "C", 0))])
    wc_place = {"cluster": "wc", "at": P("3", -1700, "C", -2000)}
    return {
        "schema": "cad-params/1",
        "project": {"name": "Nhà thử", "type": "house", "depth": "construction", "scale": 100},
        "site": {"outline": [[-2000, -2000], [8000, -2000], [8000, 10000], [-2000, 10000]]},
        "grid": {"x": {"1": 0, "2": 3000, "3": 6000}, "y": {"A": 0, "B": 4000, "C": 8000}},
        "levels": [{"name": "L1", "elevation": 0, "height": 3000, "kind": "ground"},
                   {"name": "L2", "elevation": 3000, "height": 3000, "kind": "typical"},
                   {"name": "Mai", "elevation": 6000, "height": 0, "kind": "roof"}],
        "types": {
            "walls": {"ext": {"thickness": 200}, "int": {"thickness": 100}, "virtual": {"thickness": 0}},
            "openings": {"P7": {"kind": "door", "width": 700, "height": 2100},
                         "P8": {"kind": "door", "width": 800, "height": 2100},
                         "P9": {"kind": "door", "width": 900, "height": 2100},
                         "V12": {"kind": "window", "width": 1200, "height": 1400, "sill": 900}},
            "stairs": {"T": {"kind": "straight", "flight_width": 900, "tread": 270}},
            "columns": {"C": {"size": [200, 200]}}},
        "clusters": {"wc": {
            "grid": {"x": {"a": 0, "b": 1500}, "y": {"m": 0, "n": 1800}},
            "walls": [W("wy", "int", P("a", 0, "m", 0), P("b", 0, "m", 0)),
                      W("wx", "int", P("a", 0, "m", 0), P("a", 0, "n", 0))],
            "openings": [{"id": "d", "wall": "wy", "type": "P7", "offset": 300,
                          "hinge": "start", "swing": "left"}],
            "rooms": [{"id": "r", "name": "WC", "at": P("a", 750, "m", 900), "use": "wet"}]}},
        "floors": {
            "L1": {"walls": w1, "columns": c1,
                   "openings": [
                       {"id": "vao", "wall": "wA", "type": "P9", "offset": 2500, "hinge": "start", "swing": "left"},
                       {"id": "o2", "wall": "wB", "type": "P8", "offset": 1000, "hinge": "start", "swing": "left"}],
                   "rooms": [
                       {"id": "khach", "name": "Khách", "at": P("1", 1000, "A", 2000), "use": "shared", "need_area": 20},
                       {"id": "bep", "name": "Bếp", "at": P("1", 1500, "B", 2000), "use": "shared"},
                       {"id": "sanh", "name": "Sảnh thang", "at": P("2", 700, "B", 1000), "use": "circulation"}],
                   "stairs": [{"id": "t", "type": "T", "start": P("2", 200, "B", 200), "dir": "+x",
                               "up_to": "L2", "risers": 18}],
                   "placements": [copy.deepcopy(wc_place)]},
            "L2": {"walls": w2, "columns": c2,
                   "openings": [
                       {"id": "v", "wall": "wA", "type": "V12", "offset": 2000},
                       {"id": "o-truoc", "wall": "wB", "type": "P8", "offset": 3800, "hinge": "start", "swing": "right"},
                       {"id": "o-sau", "wall": "w2", "type": "P8", "offset": 1000, "hinge": "start", "swing": "left"}],
                   "rooms": [
                       {"id": "ngu1", "name": "Ngủ trước", "at": P("1", 1000, "A", 2000), "use": "private"},
                       {"id": "ngu2", "name": "Ngủ sau", "at": P("1", 1500, "B", 2000), "use": "private"},
                       {"id": "sanh", "name": "Sảnh", "at": P("2", 700, "B", 1000), "use": "circulation"}],
                   "furniture": [{"id": "giuong", "block": "GIUONG", "at": P("1", 1200, "A", 1400)}],
                   "placements": [copy.deepcopy(wc_place)]}},
        "drawings": [{"id": "plan:L1", "origin": list(ORIGIN["L1"])},
                     {"id": "plan:L2", "origin": list(ORIGIN["L2"])}],
    }


def R(x0, y0, x1, y1):
    return [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]


HALL_WITH_WC = [(3000, 4050), (5800, 4050), (5800, 5950), (4250, 5950), (4250, 7800), (3000, 7800)]


def outlines():
    """Room outlines by wall faces, per level, as the drawing library would trace them."""
    return {
        "L1": {"khach": R(200, 200, 5800, 3950), "bep": R(200, 4050, 3000, 7800),
               "sanh": HALL_WITH_WC, "wc": R(4350, 6050, 5800, 7800)},
        "L2": {"ngu1": R(200, 200, 5800, 3950), "ngu2": R(200, 4050, 2950, 7800),
               "sanh": [(3050, 4050)] + HALL_WITH_WC[1:5] + [(3050, 7800)],
               "wc": R(4350, 6050, 5800, 7800)},
    }


def door_block(doc, width, hinge, swing, window):
    name = f"{'WIN' if window else 'DOOR'}_{width}_{hinge}_{swing}"
    if name in doc.blocks:
        return name
    blk = doc.blocks.new(name)
    h = width / 2
    blk.add_line((-h, 0), (h, 0))
    if not window:
        cx = -h if hinge == "start" else h
        closed = 0 if hinge == "start" else 180
        opened = 90 if swing == "left" else 270
        a0, a1 = sorted((closed, opened))
        if (hinge, swing) == ("start", "right"):
            a0, a1 = 270, 360
        blk.add_arc((cx, 0), width, a0, a1)
    blk.add_attdef("ID", (0, 0), dxfattribs={"height": 100})
    return name


def build(d, outl, path, extra=None):
    """Draw the table by the contract in references/bang-so.md."""
    doc = ezdxf.new("R2018", units=4)
    for layer in ("X-AREA", "A-DOOR", "A-GLAZ", "A-COLS", "A-FURN"):
        doc.layers.add(layer)
    bed = doc.blocks.new("GIUONG")
    bed.add_lwpolyline(R(-800, -1000, 800, 1000), close=True)
    msp = doc.modelspace()
    flat = flatten(d)
    src = {}
    for n in ("L1", "L2"):
        ox, oy = ORIGIN[n]
        for poly in outl[n].values():
            msp.add_lwpolyline([(x + ox, y + oy) for x, y in poly], close=True,
                               dxfattribs={"layer": "X-AREA"})
        for c in flat[n]["columns"]:
            x, y = c["at"]
            msp.add_lwpolyline(R(x - 100 + ox, y - 100 + oy, x + 100 + ox, y + 100 + oy),
                               close=True, dxfattribs={"layer": "A-COLS"})
        # door hinge and swing from the table (cluster doors are not mirrored here)
        for block in [d["floors"][n]] + [d["clusters"]["wc"]]:
            for o in block.get("openings", []):
                src.setdefault((n, o["id"]), o)
        for o in flat[n]["openings"]:
            raw = src.get((n, o["id"].split("/")[-1]), {})
            window = o["kind"] == "window"
            name = door_block(doc, o["width"], raw.get("hinge", "start"), raw.get("swing", "left"), window)
            ang = math.degrees(math.atan2(o["u"][1], o["u"][0]))
            x, y = o["centre"]
            ins = msp.add_blockref(name, (x + ox, y + oy), dxfattribs={
                "layer": "A-GLAZ" if window else "A-DOOR", "rotation": ang})
            ins.add_attrib("ID", o["id"], (x + ox, y + oy))
        for f in d["floors"][n].get("furniture", []):
            x, y = resolve(f["at"], d["grid"])
            msp.add_blockref(f["block"], (x + ox, y + oy), dxfattribs={"layer": "A-FURN"})
    if extra:
        extra(msp)
    doc.saveas(path)


# ---- planted defects: each returns (table, outlines, extra, check id, status)

def missing_door(d, o):
    def drop(msp):
        for e in msp.query("INSERT"):
            if e.has_attrib("ID") and e.get_attrib_text("ID") == "o2":
                msp.delete_entity(e)
    return d, o, drop, "openings", "fail"


def extra_door(d, o):
    def add(msp):
        msp.add_blockref("DOOR_800_start_left", (1000, 1000), dxfattribs={"layer": "A-DOOR"}).add_attrib("ID", "zz")
    return d, o, add, "openings", "fail"


def moved_door(d, o):
    def move(msp):
        for e in msp.query("INSERT"):
            if e.has_attrib("ID") and e.get_attrib_text("ID") == "o2":
                e.dxf.insert = (e.dxf.insert.x + 500, e.dxf.insert.y)
    return d, o, move, "openings", "fail"


def room_below_need(d, o):
    d["floors"]["L1"]["rooms"][0]["need_area"] = 30
    return d, o, None, "need_area", "fail"


def rooms_share_outline(d, o):
    del o["L1"]["bep"]
    o["L1"]["sanh"] = [(200, 4050)] + HALL_WITH_WC[1:5] + [(200, 7800)]
    return d, o, None, "rooms", "fail"


def stair_too_steep(d, o):
    d["types"]["stairs"]["T"]["tread"] = 200
    return d, o, None, "stairs", "fail"


def bed_in_door_swing(d, o):
    d["floors"]["L2"]["furniture"][0]["at"] = P("1", 4200, "A", 2800)
    return d, o, None, "swing", "fail"


def bed_in_mirrored_door_swing(d, o):
    """The same door drawn with a mirrored block: its swing must still be found."""
    d["floors"]["L2"]["furniture"][0]["at"] = P("1", 4200, "A", 2800)

    def mirror(msp):
        doc = msp.doc
        for e in msp.query("INSERT"):
            if e.has_attrib("ID") and e.get_attrib_text("ID") == "o-truoc":
                pos = e.dxf.insert
                msp.delete_entity(e)
                name = door_block(doc, 800, "end", "right", False)
                ins = msp.add_blockref(name, pos, dxfattribs={"layer": "A-DOOR", "xscale": -1})
                ins.add_attrib("ID", "o-truoc", pos)
    return d, o, mirror, "swing", "fail"


def gap_between_room_and_wall(d, o):
    o["L1"]["khach"] = R(200, 200, 5000, 3950)
    return d, o, None, "gross", "fail"


def room_unreachable(d, o):
    d["floors"]["L2"]["openings"] = [x for x in d["floors"]["L2"]["openings"] if x["id"] != "o-sau"]
    return d, o, None, "reach", "fail"


def through_private(d, o):
    ops = [x for x in d["floors"]["L2"]["openings"] if x["id"] != "o-sau"]
    ops.append({"id": "o-qua", "wall": "wB", "type": "P8", "offset": 1000, "hinge": "start", "swing": "left"})
    d["floors"]["L2"]["openings"] = ops
    return d, o, None, "private", "fail"


def wet_not_stacked(d, o):
    d["floors"]["L1"]["placements"] = []
    o["L1"]["sanh"] = R(3000, 4050, 5800, 7800)
    del o["L1"]["wc"]
    return d, o, None, "stack", "warn"


def column_not_stacked(d, o):
    d["floors"]["L2"]["columns"].append({"id": "c-giua", "type": "C", "at": P("2", 0, "A", 1500)})
    return d, o, None, "stack", "warn"


DEFECTS = [missing_door, extra_door, moved_door, room_below_need, rooms_share_outline,
           stair_too_steep, bed_in_door_swing, bed_in_mirrored_door_swing,
           gap_between_room_and_wall, room_unreachable, through_private,
           wet_not_stacked, column_not_stacked]


def run(d, o, extra, tmp, name):
    rep = params_check.check(d)
    assert not rep.errors, f"{name}: the test table itself is not valid: {rep.errors}"
    path = str(pathlib.Path(tmp) / f"{name}.dxf")
    build(d, o, path, extra)
    return {r["id"]: r for r in check(path, d)}


def main():
    passed = failed = 0
    with tempfile.TemporaryDirectory() as tmp:
        sound = run(table(), outlines(), None, tmp, "sound")
        off = {k: r for k, r in sound.items() if r["status"] != "pass"}
        if off:
            print(f"FAIL  the sound drawing should pass every check: {off}")
            failed += 1
        else:
            passed += 1
        for plant in DEFECTS:
            d, o, extra, key, want = plant(table(), outlines())
            got = run(d, o, extra, tmp, plant.__name__)
            others = {k: r["status"] for k, r in got.items()
                      if k != key and r["status"] != sound[k]["status"]}
            if got[key]["status"] == want and not others:
                passed += 1
            else:
                print(f"FAIL  {plant.__name__}: expected {key}={want}, got "
                      f"{got[key]['status']} {got[key]['details']}; others changed: {others}")
                failed += 1
    print(f"{passed} passed, {failed} failed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
