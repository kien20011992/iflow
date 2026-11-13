#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# dependencies = ["ezdxf>=1.3"]
# ///
"""Self-test of skills/cad/scripts/luat_check.py: the small two-storey house of
plan_check_selftest.py, its upper floor turned into one flat (a cluster of
kind "unit"), drawn here with ezdxf. The sound pair passes every law check;
each planted defect makes its own check fail, or ask for a look when the rule
or the inputs are not firm enough to fail.

Run: uv run tests/cad/luat_check_selftest.py
"""
import copy
import json
import pathlib
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tests/cad"))
sys.path.insert(0, str(ROOT / "skills/cad/scripts"))
sys.dont_write_bytecode = True  # leave no __pycache__ inside the skill
import params_check  # noqa: E402
from luat_check import Law, check  # noqa: E402
from plan_check_selftest import P, R, build, outlines, table  # noqa: E402

RULES = json.loads((ROOT / "skills/cad/assets/luat/vn.json").read_text(encoding="utf-8"))
INPUTS = {"fire_resistance": "II", "s_class": "S0", "fire_height_mm": 7000, "people_per_floor": 20,
          "area_kind": "new", "road_district_or_above": False, "submit_date": "2026-11-13"}


def flat_table():
    """The upper floor's two bedrooms become one flat placed on L2."""
    d = table()
    d["project"]["type"] = "apartment_building"
    d["site"]["outline"] = [[-2000, -2000], [8000, -2000], [8000, 10000], [-2000, 10000]]
    rooms = [r for r in d["floors"]["L2"]["rooms"] if r["id"] in ("ngu1", "ngu2")]
    d["floors"]["L2"]["rooms"] = [r for r in d["floors"]["L2"]["rooms"] if r["id"] not in ("ngu1", "ngu2")]
    d["clusters"]["can"] = {"kind": "unit", "unit_type": "2N", "grid": copy.deepcopy(d["grid"]), "rooms": rooms}
    d["floors"]["L2"]["placements"].append({"cluster": "can", "at": P("1", 0, "A", 0)})
    d["floors"]["L1"]["parking"] = [
        {"id": "oto", "vehicle": "car", "count": 1, "from": P("1", -2000, "A", -3000), "to": P("1", 1000, "A", -200)},
        {"id": "xm", "vehicle": "motorbike", "count": 4, "from": P("2", 0, "A", -3000), "to": P("3", 0, "A", -200)}]
    d["law_inputs"] = {k: {"value": v, "by": "model"} for k, v in INPUTS.items()}
    return d


def run(d, o, tmp, name, rules=RULES):
    rep = params_check.check(d)
    assert not rep.errors, f"{name}: the test table is not valid: {rep.errors}"
    path = str(pathlib.Path(tmp) / f"{name}.dxf")
    build(d, o, path)
    return {r["id"]: r for r in check(path, d, rules)}


def small_bedroom(d, o):
    o["L2"]["ngu2"] = R(200, 4050, 2330, 7800)  # 7.99 m²
    return d, o, "bedroom_area_min", "fail"


def small_flat(d, o):
    o["L2"]["ngu1"] = R(200, 200, 3000, 3950)  # the flat drops to about 20.8 m²
    return d, o, "unit_area_min", "fail"


def narrow_stair(d, o):
    d["types"]["stairs"]["T"]["flight_width"] = 800  # 20 people a floor: 900 applies
    return d, o, "stairs_law", "fail"


def short_tread(d, o):
    d["types"]["stairs"]["T"]["tread"] = 220
    return d, o, "stairs_law", "fail"


def narrow_stair_no_inputs(d, o):
    d["types"]["stairs"]["T"]["flight_width"] = 800  # 700 might apply: unknown without the inputs
    for k in ("fire_height_mm", "people_per_floor"):
        d["law_inputs"].pop(k)
    return d, o, "stairs_law", "warn"


def hotel_one_stair(d, o):
    d["project"]["type"] = "hotel"
    d["clusters"]["can"]["kind"] = "room"
    return d, o, "exits_count", "fail"


def too_dense(d, o):
    d["site"]["outline"] = [[0, 0], [6000, 0], [6000, 9000], [0, 9000]]  # 54 m² plot, 48 m² built: 89 % > 75 %
    return d, o, "plot", "fail"


def too_dense_hotel(d, o):
    too_dense(d, o)
    d["project"]["type"] = "hotel"  # the hotel table is a reading, not the text: a look, not a failure
    d["clusters"]["can"]["kind"] = "room"
    d["floors"]["L1"]["stairs"].append({"id": "t2", "type": "T", "start": P("1", 400, "B", 400), "dir": "+x",
                                        "up_to": "L2", "risers": 18})
    return d, o, "plot", "warn"


def no_parking(d, o):
    d["floors"]["L1"]["parking"] = []
    return d, o, "services", "fail"


DEFECTS = [small_bedroom, small_flat, narrow_stair, short_tread, narrow_stair_no_inputs, hotel_one_stair,
           too_dense, too_dense_hotel, no_parking]


def main():
    passed, failed = [], []

    def expect(ok, what, got=None):
        print(f"{'ok  ' if ok else 'FAIL'} {what}" + ("" if ok else f": {got}"))
        (passed if ok else failed).append(what)

    with tempfile.TemporaryDirectory() as tmp:
        sound = run(flat_table(), outlines(), tmp, "sound")
        off = {k: r["details"] for k, r in sound.items() if r["status"] not in ("pass", "skip") and k != "local"}
        expect(not off and sound["local"]["status"] == "warn",
               "bản đúng đạt mọi phép, chỉ còn luật địa phương cần xem", off)
        for plant in DEFECTS:
            d, o, key, want = plant(flat_table(), outlines())
            got = run(d, o, tmp, plant.__name__)
            status = got.get(key, {}).get("status")
            expect(status == want, f"{plant.__name__}: {key} = {want}", (status, got.get(key, {}).get("details")))
    # A rule row applies only from its date: the electric-vehicle amendment starts on 2026-12-15.
    d = flat_table()
    before = {r["id"] for r in Law(RULES, d).rows}
    d["law_inputs"]["submit_date"]["value"] = "2027-01-04"
    after = {r["id"] for r in Law(RULES, d).rows}
    expect("q04-cho-xe-dien" not in before and "q04-cho-xe-dien" in after,
           "dòng luật chỉ áp từ ngày hiệu lực của nó")
    print(f"{len(passed)} passed, {len(failed)} failed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
