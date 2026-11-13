#!/usr/bin/env python3
"""Self-test of the drawing library (skills/cad/lib/) without CADCraft: draw
the ground floor of tests/cad/bang-so/pho-da-nang.json into a command list,
then compare it with numbers worked out by hand from the brief.

Standard library only. Run: python3 tests/cad/lib_selftest.py
"""
import json
import math
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "skills/cad/lib"))
sys.dont_write_bytecode = True  # leave no __pycache__ inside the skill
import bang_so  # noqa: E402
import hinh  # noqa: E402
from build_mau import ve_tang  # noqa: E402
from lenh import Lenh, text_width  # noqa: E402

TABLE = ROOT / "tests/cad/bang-so/pho-da-nang.json"

# By hand from the brief: inner wall faces 200 / 4800 across, partitions 100
# centred, the WC 1500 x 2000 in the corner at axis 2 / E.
ROOMS = {"Cửa hàng": 4.6 * 3.75,
         "Thang, lối đi": 4.6 * 3.9 + 2.7 * 0.05,
         "Bếp, ăn": 4.6 * 4.65 + 2.7 * 0.05 + 3.0 * 2.1,
         "WC": 1.5 * 2.0}
OPENINGS = 4.0 * 0.2 + 0.9 * 0.2 + 0.8 * 0.1 + 0.7 * 0.1  # cut out of the wall mass
INSERTS = {"o1": (2500, 100),     # shutter: centre of the opening on the wall's centre line
           "o2": (1000, 4050),    # doors: the hinge, on the face the leaf opens to
           "o3": (300, 14800),
           "o4": (4650, 12800)}


def commands(cmds):
    for c in cmds:
        cid, _, body = c.partition(" ")
        yield cid, json.loads(body)


def box(cx, cy, w, h):
    return (cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2)


def hit(a, b):
    return a[0] < b[2] and b[0] < a[2] and a[1] < b[3] and b[1] < a[3]


def main():
    d = bang_so.load(TABLE)
    fails, passed = [], []

    def expect(ok, what):
        print(f"{'ok  ' if ok else 'FAIL'} {what}")
        (passed if ok else fails).append(what)

    floor = bang_so.Floor(d, "L1")
    cells = hinh.Cells(floor)
    got = {}
    for r in floor.rooms:
        info = hinh.room_outline(cells, r["at"])
        got[r["name"]] = info["area"] if info else None
    for name, want in ROOMS.items():
        expect(got.get(name) is not None and abs(got[name] - want) < 1e-6,
               f"diện tích {name}: {got.get(name)} m², tính tay {want:.3f}")
    walls = sum(hinh.area(q) for q in cells.loops(cells.wall_cells())) / 1e6
    total = sum(v for v in got.values() if v) + walls + OPENINGS
    expect(abs(total - 5.0 * 15.0) < 1e-6, f"phòng + tường + ô cửa = {total:.3f} m², phủ bì 75")

    L = Lenh(d["project"]["scale"])
    todo, _ = ve_tang(L, d, "L1", (0, 0))
    cmds = list(commands(L.cmds))

    ins = {c["attribs"]["ID"]: tuple(c["at"]) for cid, c in cmds if cid == "insert" and "attribs" in c}
    for oid, want in INSERTS.items():
        expect(oid in ins and math.dist(ins[oid], want) < 1e-6, f"điểm chèn {oid}: {ins.get(oid)}, tính tay {want}")

    # Text: room names, areas and tags never overlap each other or a door's sweep.
    texts = [(c["text"], box(*c["at"], text_width(c["text"], c["height"]), c["height"]))
             for cid, c in cmds if cid == "mtext" and c.get("rotation", 0) == 0]
    rings = [box(*c["center"], 2 * c["radius"], 2 * c["radius"]) for cid, c in cmds
             if cid == "circle" and c["radius"] < 500]
    # the letters of a tag or a grid name sit inside their ring: the ring stands for both
    def in_ring(b):
        cx, cy = (b[0] + b[2]) / 2, (b[1] + b[3]) / 2
        return any(r[0] < cx < r[2] and r[1] < cy < r[3] for r in rings)
    named = [(t, b) for t, b in texts if not in_ring(b)] + [("vòng", r) for r in rings]
    boxes = [b for _, b in named]
    clash = [f"{named[i][0]!r}/{named[j][0]!r}" for i in range(len(named)) for j in range(i + 1, len(named))
             if hit(named[i][1], named[j][1])]
    expect(not clash, f"chữ và nhãn không đè nhau ({len(boxes)} khung) {clash or ''}")
    sweeps = []
    for op in floor.openings:
        if op.kind == "door":
            xs, ys = zip(*op.sector())
            sweeps.append((op.id, (min(xs), min(ys), max(xs), max(ys)), op))
    inside_sweep = []
    for b in boxes:
        for oid, s, op in sweeps:
            centre = ((b[0] + b[2]) / 2, (b[1] + b[3]) / 2)
            if hinh.inside(centre, op.sector()):
                inside_sweep.append(oid)
    expect(not inside_sweep, f"không chữ nào nằm trong tầm quét cánh cửa {inside_sweep or ''}")

    # Each dimension row closes: its pieces add up to the overall row on that side.
    rows = {}
    for cid, c in cmds:
        if cid != "dimlinear":
            continue
        k = 0 if c["rotation"] == 0 else 1
        rows.setdefault((k, round(c["at"][1 - k])), []).append(abs(c["p2"][k] - c["p1"][k]))
    sides = {}
    for (k, pos), parts in rows.items():
        sides.setdefault((k, pos < 0), []).append(sum(parts))
    for (k, low), sums in sorted(sides.items()):
        expect(len(set(round(s) for s in sums)) == 1,
               f"các hàng kích thước {'ngang' if k == 0 else 'đứng'} phía {'dưới/trái' if low else 'trên/phải'} "
               f"cộng ra cùng một số: {sorted(set(round(s) for s in sums))}")
    expect(any("thang" in t for t in todo), "thang chưa vẽ được báo trong danh sách chưa vẽ")

    # Edges the review found: an empty level, a door with no leaf block, a shaft
    # inside a room, a long command list split between runs.
    todo, ext = ve_tang(Lenh(100), d, "Mai", (0, 0))
    expect(ext is None and any("không có tường" in t for t in todo), "tầng trống: báo, không dừng cả lần chạy")
    d2 = json.loads(json.dumps(d))
    d2["types"]["openings"]["P1"]["width"] = 750
    todo, _ = ve_tang(Lenh(100), d2, "L1", (0, 0))
    expect(any("750" in t for t in todo), "cửa không có block cánh cỡ 750: đánh dấu, ghi vào chưa vẽ")
    d3 = json.loads(json.dumps(d))
    d3["floors"]["L1"]["shafts"] = [{"id": "kt", "kind": "duct", "from": [["1", 200], ["A", 200]],
                                     "to": [["1", 800], ["A", 800]]}]
    f3 = bang_so.Floor(d3, "L1")
    shop = hinh.room_outline(hinh.Cells(f3), f3.rooms[0]["at"])
    expect(abs(shop["area"] - (ROOMS["Cửa hàng"] - 0.36)) < 1e-6,
           f"hộp kỹ thuật 0,6 × 0,6 ở góc không tính vào phòng: {shop['area']:.3f} m²")
    from chay import chunks
    parts = chunks(["a" * 10, "b" * 10, 'hatch {"handles":["{last}"]}', "c" * 10], limit=15)
    expect(all(not p[0].startswith("hatch") for p in parts) and sum(map(len, parts)) == 4,
           f"lệnh dùng {{last}} không bị tách khỏi lệnh trước nó: {[len(p) for p in parts]}")

    print(f"{len(passed)} passed, {len(fails)} failed")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
