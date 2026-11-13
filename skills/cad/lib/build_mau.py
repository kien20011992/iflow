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
import math
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
from ky_hieu import (Stair, cao_do, cao_do_size, do_dac, duong_cat, free_spot, gieng_troi,  # noqa: E402
                     hop_ky_thuat, huong_bac, lan_can, thang)
from lenh import Lenh  # noqa: E402
from mat_cat import mat_cat  # noqa: E402
from hinh import inside  # noqa: E402
from mat_bang import (box, cho_ten_phong, cot, danh_dau, hang_kich_thuoc, nhan_cua, ranh_dat,  # noqa: E402
                      ten_phong_ngoai, tieu_de, truc, tuong, tuong_giai_doan, ve_nhan_cua, ve_o_cua,
                      ve_ten_phong)

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


def ve_tang(L, d, level, origin, arrivals=(), floor=None):
    """Draw one floor plan; return the list of things left undrawn and the
    plan's extent. `arrivals`: stairs of other floors that come up to this one;
    `floor`: this level's Floor when the caller already built it."""
    L.origin = origin
    f = floor or Floor(d, level)
    m = Cells(f)
    todo = [f"{level}: tường xiên {w.id}" for w in m.skipped]
    marks_extra = [(w.rect(), f"tường xiên {w.id}") for w in m.skipped]
    if m.empty:
        return todo + [f"{level}: tầng không có tường, cột hay ô trống nào"], None
    if "site" in d and "outline" in d["site"]:
        ranh_dat(L, d["site"]["outline"])
    loops = m.loops(m.wall_cells())
    tuong(L, loops)
    tuong_giai_doan(L, f.other_walls)
    todo += [f"{level}: ô cửa {op.id} chưa đứng khi xong việc (phá hay xây sau), chưa vẽ"
             for op in f.skipped_openings]
    todo += [f"{level}: {kind} {oid} ({phase}) chưa vẽ" for kind, oid, phase in f.unbuilt]
    cot(L, f.columns)
    obstacles = []
    for op in f.openings:
        got, why = ve_o_cua(L, op)
        obstacles += got
        if why:
            todo.append(f"{level}: {why}")
            marks_extra.append((op.wall.rect(*op.span), why))

    # The section line first: room names move off it, never the line (ve.md).
    for sec in d.get("sections", []):
        path = [resolve(p, d["grid"]) for p in sec["path"]]
        if all(a[0] == b[0] or a[1] == b[1] for a, b in zip(path, path[1:])):
            obstacles += duong_cat(L, sec, path)
        else:
            todo.append(f"{level}: đường cắt {sec['name']} xiên, chưa vẽ")
    # Stairs as this floor sees them: leaving from here, arriving too, or arriving only.
    for st, role in stair_roles(f.stairs, arrivals):
        stair = Stair(st, d["types"])
        if stair.supported:
            obstacles += thang(L, stair, role)
        else:
            marks_extra.append((stair_box(st, d["types"]), f"thang {st['id']} ({stair.kind})"))
    for v in f.voids:
        obstacles += gieng_troi(L, v)
    for rl in f.railings:
        obstacles += lan_can(L, rl)
    for sh in f.shafts:
        obstacles += hop_ky_thuat(L, sh)
    for item in f.furniture:
        got, why = do_dac(L, item)
        obstacles += got
        if why:
            marks_extra.append((box(*item["at"], 600, 600), why))

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
    # Room labels are chosen first and drawn after the tags: when a door tag
    # finds no spot, the label of the room it opens into steps aside (ve.md).
    labels = {}
    for r in f.rooms:
        if r["id"] in rooms:
            L.pline(rooms[r["id"]]["outline"], "X-AREA")
            plan = cho_ten_phong(L, r, rooms[r["id"]], obstacles)
            if plan:
                labels[r["id"]] = plan
                obstacles += [b for *_, b in plan]
            else:
                small.append(r)
    outlines = [i["outline"] for i in rooms.values()]
    for op in f.openings:
        ring = nhan_cua(L, op, outlines, obstacles)
        if ring is not None:
            obstacles.append(ring)
        else:
            if op.kind == "door":  # the room the leaf opens into
                h, o = op.hinge_point, op.open_dir
                probes = [(h[0] + o[0] * op.width / 2, h[1] + o[1] * op.width / 2)]
            else:  # a window: the room on either side of it
                c, n, reach = op.centre, op.wall.n, op.wall.t / 2 + op.width / 2
                probes = [(c[0] + n[0] * reach, c[1] + n[1] * reach), (c[0] - n[0] * reach, c[1] - n[1] * reach)]
            rid = next((k for p in probes for k, i in rooms.items() if k in labels and inside(p, i["outline"])), None)
            if rid:
                # try the tag with that room's label lifted; keep the swap only
                # when the label then finds another place in its room
                moved = labels.pop(rid)
                for *_, b in moved:
                    obstacles.remove(b)
                ring = nhan_cua(L, op, outlines, obstacles, emit=False)
                room = next(r for r in f.rooms if r["id"] == rid)
                plan = cho_ten_phong(L, room, rooms[rid], obstacles + ([ring] if ring else []))
                if ring and plan:
                    ve_nhan_cua(L, op, ring)
                    obstacles.append(ring)
                    labels[rid] = plan
                    obstacles += [b for *_, b in plan]
                else:
                    ring = None
                    labels[rid] = moved
                    obstacles += [b for *_, b in moved]
        if ring is None:
            todo.append(f"{level}: nhãn {op.label} của {op.id} không có chỗ")
    for plan in labels.values():
        ve_ten_phong(L, plan)
    # The floor level, in a hall if there is one.
    z = next(lv["elevation"] for lv in d["levels"] if lv["name"] == level)
    w, h = cao_do_size(L, z)
    halls = [r for r in f.rooms if r["id"] in rooms and r["use"] == "circulation"] + \
            [r for r in f.rooms if r["id"] in rooms and r["use"] != "circulation"]
    spot = next((p for p in (free_spot(rooms[r["id"]], w, h, obstacles, r["at"]) for r in halls) if p), None)
    if spot:  # place the mark so the box cao_do returns is centred on the spot checked
        s_ = L.size("text")
        obstacles += cao_do(L, (spot[0] - (w - s_) / 2 + 0.6 * s_, spot[1] - 1.1 * s_), z)
    else:
        todo.append(f"{level}: ký hiệu cao độ sàn không có chỗ")

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
    marks = list(marks_extra)
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
    north = d.get("site", {}).get("north_deg")
    if north is not None:
        huong_bac(L, (x_ring[1] + 3 * r, y_ring[0]), north)
    tieu_de(L, ((X0 + X1) / 2, y_ring[0] - r - 2 * L.size("title")),
            LEVEL_TITLE.format(name=level_title(d, level), scale=d["project"]["scale"]))
    return todo, (x_ring[0] - 2 * r, y_ring[0] - 4 * L.size("title"), x_ring[1] + 6 * r, y_ring[1] + 2 * r)


def level_title(d, level):
    """"TẦNG 2" for a level named L2, "TẦNG 1" for the ground level, "TẦNG HẦM B1"…"""
    kind = next(lv["kind"] for lv in d["levels"] if lv["name"] == level)
    if kind == "ground":
        return "TẦNG 1"
    if kind == "basement":
        return f"TẦNG HẦM {level}"
    digits = "".join(ch for ch in level if ch.isdigit())
    return f"TẦNG {digits}" if level.upper().startswith("L") and digits else f"TẦNG {level}"


def stair_roles(leaving, arrivals):
    """(stair, role) pairs: a stair leaving from here is "middle" when one from
    below arrives at the same foot, else "bottom"; an arrival with no stair
    leaving from its foot is drawn whole, "top"."""
    out = []
    for st in leaving:
        same = any(math.dist(a["start"], st["start"]) < 1 for a in arrivals)
        out.append((st, "middle" if same else "bottom"))
    for a in arrivals:
        if not any(math.dist(a["start"], st["start"]) < 1 for st in leaving):
            out.append((a, "top"))
    return out


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
    floors = {lv["name"]: Floor(d, lv["name"]) for lv in d["levels"]}  # unrolled once
    for dr in d["drawings"]:
        kind, _, ref = dr["id"].partition(":")
        if want and kind == "section":
            continue  # --plans asked for plans only: left out on purpose, not missing
        if kind == "section":
            sec = next(s for s in d.get("sections", []) if s["name"] == ref)
            got, ext = mat_cat(L, d, sec, tuple(dr["origin"]), floors)
            todo += got
            if args.png and ext:
                ox, oy = dr["origin"]
                x0, y0, x1, y1 = ext
                pngs.append((out.with_name(f"{out.stem}-{ref}.png"),
                             [[x0 + ox, y0 + oy], [x1 + ox, y1 + oy]], (x1 - x0) > (y1 - y0)))
            continue
        if kind != "plan" or (want and ref not in want):
            if kind != "plan":
                todo.append(f"hình {dr['id']}")
            continue
        arrivals = [st for name, fl in floors.items() if name != ref for st in fl.stairs if st["up_to"] == ref]
        got, ext = ve_tang(L, d, ref, tuple(dr["origin"]), arrivals, floors[ref])
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
