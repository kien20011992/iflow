#!/usr/bin/env python3
"""Self-test of skills/cad/scripts/params_check.py: the three sample number
tables in tests/cad/bang-so/ must come out with no error, and each copy with
one planted defect must come out with exactly one error, at the planted spot.

Standard library only. Run: python3 tests/cad/params_check_selftest.py
"""
import copy
import json
import pathlib
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "skills/cad/scripts"))
sys.dont_write_bytecode = True  # leave no __pycache__ inside the skill
from params_check import check, load as load_file  # noqa: E402

SAMPLES = ROOT / "tests/cad/bang-so"


def load(name):
    return json.loads((SAMPLES / name).read_text(encoding="utf-8"))


def opening(d, level, oid):
    return next(o for o in d["floors"][level]["openings"] if o["id"] == oid)


def wrong_version(d):
    d["schema"] = "cad-params/0"
    return "schema"


def missing_levels(d):
    del d["levels"]
    return "levels"


def odd_phase(d):
    d["floors"]["L1"]["walls"][0]["phase"] = "half-built"
    return "floors.L1.walls[0].phase"


def decimal_mm(d):
    opening(d, "L1", "o2")["offset"] = 1000.5
    return "floors.L1.openings[1].offset"


def unknown_grid(d):
    d["floors"]["L2"]["rooms"][0]["at"][0][0] = "7"
    return "floors.L2.rooms[0].at"


def unknown_type(d):
    d["floors"]["L3"]["walls"][4]["type"] = "brick300"
    return "floors.L3.walls[4].type"


def opening_on_missing_wall(d):
    opening(d, "L2", "o3")["wall"] = "wZ"
    return "floors.L2.openings[2].wall"


def opening_overflows_wall(d):
    opening(d, "L1", "o1")["offset"] = 1000  # 1000 + 4000 > 5000 - 100
    return "floors.L1.openings[0].offset"


def duplicate_id(d):
    d["floors"]["L2"]["rooms"][1]["id"] = "r1"
    return "floors.L2.rooms[1].id"


def cluster_contains_itself(d):
    d["clusters"]["can-2N"]["placements"] = [
        {"cluster": "tang-dien-hinh", "at": [["a", 0], ["m", 0]]}]
    # The loop is reported from whichever cluster the search starts at.
    return ("clusters.can-2N.placements", "clusters.tang-dien-hinh.placements"), "tự chứa"


def setback_on_missing_edge(d):
    d["site"]["setbacks"].append({"edge": 9, "mm": 100})
    return "site.setbacks[4].edge"


def negative_width(d):
    d["types"]["openings"]["P1"]["width"] = -800
    return "types.openings.P1.width"


def bool_rotation(d):
    d["floors"]["L1"]["furniture"][0]["rotate"] = False
    return "floors.L1.furniture[0].rotate"


def placements_not_a_list(d):
    d["placements"] = 5
    return "placements"


def placement_id_not_text(d):
    d["clusters"]["tang-dien-hinh"]["placements"][0]["id"] = [1]
    return "clusters.tang-dien-hinh.placements[0].id"


def beam_not_a_pair(d):
    d["structure"]["beam"]["value"] = 300
    return "structure.beam.value"


def odd_law_input(d):
    d["law_inputs"] = {"fire_resistance": {"value": "VI", "by": "model"}}
    return "law_inputs.fire_resistance.value"


def odd_cluster_kind(d):
    d["clusters"]["can-2N"]["kind"] = "flat"
    return "clusters.can-2N.kind"


def drawing_twice(d):
    d["drawings"].append({"id": "plan:L1", "origin": [0, 90000]})
    return "drawings[4].id"


DEFECTS = [
    ("pho-da-nang.json", wrong_version),
    ("pho-da-nang.json", missing_levels),
    ("pho-da-nang.json", odd_phase),
    ("pho-da-nang.json", decimal_mm),
    ("pho-da-nang.json", unknown_grid),
    ("pho-da-nang.json", unknown_type),
    ("pho-da-nang.json", opening_on_missing_wall),
    ("pho-da-nang.json", opening_overflows_wall),
    ("pho-da-nang.json", duplicate_id),
    ("chung-cu-ktdd5.json", cluster_contains_itself),
    ("pho-da-nang.json", setback_on_missing_edge),
    ("pho-da-nang.json", negative_width),
    ("pho-da-nang.json", bool_rotation),
    ("pho-da-nang.json", placements_not_a_list),
    ("chung-cu-ktdd5.json", placement_id_not_text),
    ("pho-da-nang.json", drawing_twice),
    ("pho-da-nang.json", beam_not_a_pair),
    ("pho-da-nang.json", odd_law_input),
    ("chung-cu-ktdd5.json", odd_cluster_kind),
]


def matches(err, where):
    paths, words = (where if isinstance(where, tuple) else ((where,), None))
    if isinstance(paths, str):
        paths = (paths,)
    return err["path"] in paths and (words is None or words in err["msg"])


def duplicate_key(tmp):
    """A key written twice is lost by plain json.load; the loader names it."""
    text = (SAMPLES / "pho-da-nang.json").read_text(encoding="utf-8")
    text = text.replace('"2": 5000', '"2": 5000, "2": 5200', 1)
    path = pathlib.Path(tmp) / "dup.json"
    path.write_text(text, encoding="utf-8")
    d, dups = load_file(path)
    return check(d, dups).errors


def main():
    passed = failed = 0
    samples = sorted(p.name for p in SAMPLES.glob("*.json"))
    if len(samples) != 3:
        print(f"FAIL  expected the three sample tables in {SAMPLES}, found {samples}")
        return 1
    for sample in samples:
        rep = check(*load_file(SAMPLES / sample))
        if rep.errors:
            print(f"FAIL  {sample} should be clean: {rep.errors}")
            failed += 1
        else:
            passed += 1
    for sample, plant in DEFECTS:
        d = copy.deepcopy(load(sample))
        where = plant(d)
        errs = check(d).errors
        if len(errs) == 1 and matches(errs[0], where):
            passed += 1
        else:
            print(f"FAIL  {plant.__name__}: expected one error at {where}, got {errs}")
            failed += 1
    with tempfile.TemporaryDirectory() as tmp:
        errs = duplicate_key(tmp)
    if len(errs) == 1 and errs[0]["path"] == "2" and "hai lần" in errs[0]["msg"]:
        passed += 1
    else:
        print(f"FAIL  duplicate_key: expected one error for key '2', got {errs}")
        failed += 1
    print(f"{passed} passed, {failed} failed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
