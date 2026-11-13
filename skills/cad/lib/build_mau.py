#!/usr/bin/env python3
"""build_mau.py PARAMS OUT.dxf [--png] [--plans L1,L2] — the sample build:
draw every floor plan listed in the table's drawings through CADCraft, with
the library's functions. Copy it into the project and change only what the
project needs; keep the order (walls, openings, room names, tags, marks,
dimensions, grid) so later text avoids earlier text.

What the library does not draw yet is marked on the drawing with a cloud and
listed at the end of the run under "Chưa vẽ" — that list goes to the handover.
Exit code: CADCraft's (0 = saved), or 1 when the table fails params_check.py.
"""
import argparse
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent / "scripts"))
sys.dont_write_bytecode = True  # leave no __pycache__ inside the skill

import params_check  # noqa: E402
from bang_so import Floor, resolve  # noqa: E402
from chay import run  # noqa: E402
from hinh import Cells, bbox, room_outline  # noqa: E402
from lenh import Lenh  # noqa: E402
from mat_bang import (box, cot, danh_dau, hang_kich_thuoc, nhan_cua, ranh_dat, ten_phong,  # noqa: E402
                      ten_phong_ngoai, tieu_de, truc, tuong, ve_o_cua)

LEVEL_TITLE = "MẶT BẰNG {name} - TL 1:{scale}"
FACADE_REACH = 500  # mm: a wall whose outer face is this close to the building's edge is on that facade


def stair_box(s, types):
    t = types["stairs"][s["type"]]
    risers = s.get("risers") or 18
    run_len = (risers // 2 - 1) * t["tread"] + t.get("landing", t["flight_width"]) \
        if t["kind"] == "u_turn" else (risers - 1) * t["tread"]
    across = 2 * t["flight_width"] + t.get("gap", 0) if t["kind"] == "u_turn" else t["flight_width"]
    d = {"+x": (1, 0), "-x": (-1, 0), "+y": (0, 1), "-y": (0, -1)}[s["dir"]]
    side = 1 if s.get("turn", "left") == "left" else -1
    n = (-d[1] * side, d[0] * side)
    x, y = s["start"]
    pts = [(x, y), (x + d[0] * run_len, y + d[1] * run_len),
           (x + d[0] * run_len + n[0] * across, y + d[1] * run_len + n[1] * across),
           (x + n[0] * across, y + n[1] * across)]
    return pts


def ve_tang(L, d, level, origin):
    """Draw one floor plan; return the list of things left undrawn."""
    L.origin = origin
    f = Floor(d, level)
    m = Cells(f)
    todo = [f"{level}: tường xiên {w.id}" for w in m.skipped]
    marks_extra = [(w.rect(), f"tường xiên {w.id}") for w in m.skipped]
    if m.empty:
        return todo + [f"{level}: tầng không có tường, cột hay ô trống nào"], None
    if "site" in d and "outline" in d["site"]:
        ranh_dat(L, d["site"]["outline"])
    loops = m.loops(m.wall_cells())
    tuong(L, loops)
    cot(L, f.columns)
    obstacles = []
    for op in f.openings:
        got, why = ve_o_cua(L, op)
        obstacles += got
        if why:
            todo.append(f"{level}: {why}")
            marks_extra.append((op.wall.rect(*op.span), why))

    rooms, small = {}, []
    for r in f.rooms:
        info = room_outline(m, r["at"])
        if info is None:
            todo.append(f"{level}: phòng {r['name']} không khép kín, chưa vẽ đường bao")
            continue
        rooms[r["id"]] = info
        if info["holes"]:
            todo.append(f"{level}: diện tích {r['name']} tính cả {info['hole_area']:.2f} m² cột hay ô trống "
                        f"đứng giữa phòng")
    for r in f.rooms:
        if r["id"] in rooms:
            got = ten_phong(L, r, rooms[r["id"]], obstacles)
            if got:
                obstacles += got
            else:
                small.append(r)
    outlines = [i["outline"] for i in rooms.values()]
    for op in f.openings:
        ring = nhan_cua(L, op, outlines, obstacles)
        if ring:
            obstacles.append(ring)
        else:
            todo.append(f"{level}: nhãn {op.label} của {op.id} không có chỗ")

    # Dimensions outside the walls, then the grid rings beyond them.
    X0, Y0, X1, Y1 = bbox([p for q in loops for p in q])
    first, gap = L.size("first_dim"), L.size("dim_gap")
    grid = d["grid"]
    rows = {"bottom": Y0 - first, "top": Y1 + first, "left": X0 - first, "right": X1 + first}
    step = {"bottom": -gap, "top": gap, "left": -gap, "right": gap}
    for side, face in (("bottom", Y0), ("top", Y1), ("left", X0), ("right", X1)):
        axis = "x" if side in ("bottom", "top") else "y"
        jambs = []
        for op in f.openings:
            b = bbox(op.wall.rect())
            along_x = abs(op.wall.u[1]) < 1e-9  # the wall runs along x
            # on this facade: parallel to it, its outer face within a column's depth of the edge
            near = FACADE_REACH
            on = {"bottom": along_x and b[1] - Y0 <= near, "top": along_x and Y1 - b[3] <= near,
                  "left": not along_x and b[0] - X0 <= near, "right": not along_x and X1 - b[2] <= near}[side]
            if on and op.wall.square:
                for s in op.span:
                    p = op.wall.at(s, 0)
                    jambs.append(p[0] if axis == "x" else p[1])
        ends = [X0, X1] if axis == "x" else [Y0, Y1]
        lines = sorted(grid[axis].values())
        at = rows[side]
        if jambs:
            obstacles += hang_kich_thuoc(L, axis, ends + jambs, at, face, obstacles)
            at += step[side]
        if side in ("bottom", "left"):
            if len(lines) > 2 or sorted(lines) != ends:
                obstacles += hang_kich_thuoc(L, axis, lines, at, face, obstacles)
                at += step[side]
            obstacles += hang_kich_thuoc(L, axis, ends, at, face, obstacles)
            at += step[side]
        rows[side] = at
    for r in small:  # labels too large for their room, outside with a leader
        got = ten_phong_ngoai(L, r, rooms[r["id"]], obstacles, (X0, Y0, X1, Y1))
        if got:
            obstacles += got
        else:
            todo.append(f"{level}: tên phòng {r['name']} không có chỗ, kể cả ngoài nhà")
    # What the library does not draw yet: clouds, after the dimensions so notes avoid them.
    marks = [(stair_box(s, d["types"]), f"thang {s['id']}") for s in f.stairs]
    marks += [(box(*x["at"], 600, 600), f"đồ {x['block']}") for x in f.furniture]
    marks += [(v["rect"], "giếng trời, ô thông tầng") for v in f.voids]
    marks += [(v["rect"], f"hộp kỹ thuật {v['id']}") for v in f.shafts]
    marks += marks_extra
    for rl in f.railings:
        pts = [resolve(p, f.grid) for p in rl["points"]]
        x0, y0, x1, y1 = bbox(pts)
        marks.append(([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], "lan can"))
    for pl in f.placements:
        marks.append((box(*resolve(pl["at"], f.grid), 1000, 1000), f"cụm {pl['cluster']}"))
    for o in f.outside:
        marks.append((box(*o["near"], 1000, 1000), o["what"]))
    for poly, what in marks:
        note = danh_dau(L, poly, what, obstacles, within=[(X0, Y0), (X1, Y0), (X1, Y1), (X0, Y1)])
        if note:
            obstacles.append(note)
        todo.append(f"{level}: {what}")

    r = L.size("grid_circle") / 2
    sx0, sy0, sx1, sy1 = bbox(d["site"]["outline"]) if "site" in d and "outline" in d["site"] \
        else (X0, Y0, X1, Y1)
    y_ring = (min(rows["bottom"], sy0 - gap) - r, max(rows["top"], sy1 + gap) + r)
    x_ring = (min(rows["left"], sx0 - gap) - r, max(rows["right"], sx1 + gap) + r)
    truc(L, grid, x_ring, y_ring)
    name = {"ground": "TẦNG 1"}.get(next(lv["kind"] for lv in d["levels"] if lv["name"] == level), level)
    tieu_de(L, ((X0 + X1) / 2, y_ring[0] - r - 2 * L.size("title")),
            LEVEL_TITLE.format(name=name if name != level else f"TẦNG {level}", scale=d["project"]["scale"]))
    return todo, (x_ring[0] - 2 * r, y_ring[0] - 4 * L.size("title"), x_ring[1] + 2 * r, y_ring[1] + 2 * r)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("params")
    ap.add_argument("out")
    ap.add_argument("--png", action="store_true", help="also plot one PNG per plan next to OUT")
    ap.add_argument("--plans", help="only these levels, comma-separated")
    args = ap.parse_args(argv)

    d, dups = params_check.load(args.params)
    rep = params_check.check(d, dups)
    if rep.errors:
        for e in rep.errors:
            print(f"LỖI   {e['path']}: {e['msg']}")
        return 1
    L = Lenh(d["project"]["scale"])
    L.setup()
    todo, pngs = [], []
    want = set(args.plans.split(",")) if args.plans else None
    out = pathlib.Path(args.out)
    for dr in d["drawings"]:
        kind, _, ref = dr["id"].partition(":")
        if kind != "plan" or (want and ref not in want):
            if kind != "plan":
                todo.append(f"hình {dr['id']}")
            continue
        got, ext = ve_tang(L, d, ref, tuple(dr["origin"]))
        todo += got
        if args.png and ext:
            ox, oy = dr["origin"]
            x0, y0, x1, y1 = ext
            win = [[x0 + ox, y0 + oy], [x1 + ox, y1 + oy]]
            pngs.append((out.with_name(f"{out.stem}-{ref}.png"), win, (x1 - x0) > (y1 - y0)))
    code, stdout, stderr = run(L.cmds, out, pngs)
    print(f"cadcraft-cli: mã thoát {code}, {len(L.cmds)} lệnh -> {out}")
    if code != 0:
        print(stderr.strip()[-1500:])
    if todo:
        print("Chưa vẽ:")
        for t in todo:
            print(f"  - {t}")
    return code


if __name__ == "__main__":
    sys.exit(main())
