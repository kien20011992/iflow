#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# dependencies = ["ezdxf>=1.3"]
# ///
"""plan_check.py DXF PARAMS [--json] — check a drawing against its number
table, and check that the building it shows can be walked through.

Run it with `uv run plan_check.py FILE.dxf params.json`, or with any Python
that has ezdxf. The table must pass params_check.py first. The drawing is read
by the rules in references/bang-so.md ("Bảng số hiện lên file DXF thế nào");
every expected value is recomputed here from the table, never taken from the
drawing library, so a fault in the library cannot vouch for itself.

Exit 0 = no check failed, 1 = at least one failed (or the table is not valid),
2 = a file could not be read.
"""
import argparse
import json
import math
import pathlib
import sys
from collections import deque

import ezdxf
from ezdxf import bbox

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
sys.dont_write_bytecode = True
from dxf_check import crosses, inside, polygon_area  # noqa: E402
import params_check  # noqa: E402

POS_TOL = 1.0         # mm: an opening sits where the table puts it
NEED_LOW = 0.90       # below 90 % of the brief's area fails
NEED_BAND = 0.10      # more than 10 % off either way is worth a look
GROSS_TOL = 0.03      # rooms + walls must cover the footprint within 3 %
CELL = 50             # mm: raster cell for the footprint sum
TREAD_MIN = 250       # mm, the custom in references/ve.md when no code is known
STEP_MIN, STEP_MAX = 550, 650  # 2 x riser + tread, same source
STACK_TOL = 50        # mm: a column above sits on the one below
SIDE_REACH = 100      # mm past the wall face where a door's two rooms are probed
REGION_MARGIN = 1000  # mm around a plan's walls that still belongs to that plan
STAIR_REACH = 3000    # mm: the upper room a stair lands in lies this close to its foot
DOOR_KINDS = ("door", "shutter", "opening")


# ---- the table, flattened ---------------------------------------------------

def resolve(p, grid):
    return tuple(grid[axis][ref[0]] + sum(ref[1:]) for axis, ref in zip(("x", "y"), p))


def make_transform(at, rotate, mirror):
    ang = math.radians(rotate or 0)
    c, s = round(math.cos(ang)), round(math.sin(ang))

    def f(pt):
        x, y = pt
        if mirror == "x":
            x = -x
        elif mirror == "y":
            y = -y
        return (at[0] + c * x - s * y, at[1] + s * x + c * y)
    return f


def compose(outer, inner):
    return lambda pt: outer(inner(pt))


def flip(side, mirrored):
    if not mirrored or side is None:
        return side
    return {"left": "right", "right": "left"}.get(side, side)


def new_level():
    return {k: [] for k in ("walls", "openings", "rooms", "columns", "stairs",
                            "voids", "shafts", "furniture")}


def add_block(out, block, grid, tf, mirrored, prefix, d, level_name, next_level):
    """Copy one floor or cluster into `out`, in building coordinates."""
    types = d["types"]
    pt = lambda p: tf(resolve(p, grid))  # noqa: E731
    walls = {}
    for w in block.get("walls", []):
        t = types["walls"][w["type"]]["thickness"]
        rec = {"id": prefix + w["id"], "a": pt(w["from"]), "b": pt(w["to"]), "t": t,
               "align": flip(w.get("align", "center"), mirrored)}
        walls[w["id"]] = rec
        # a wall to be demolished, or built later, does not stand in the finished plan
        if w.get("phase", "new") in ("new", "existing"):
            out["walls"].append(rec)
    standing = {id(r) for r in out["walls"]}
    built = lambda o: o.get("phase", "new") in ("new", "existing")  # noqa: E731
    for o in block.get("openings", []):
        w = walls[o["wall"]]
        if id(w) not in standing or not built(o):
            continue
        t = types["openings"][o["type"]]
        a, b = w["a"], w["b"]
        length = math.hypot(b[0] - a[0], b[1] - a[1])
        ux, uy = (b[0] - a[0]) / length, (b[1] - a[1]) / length
        lo, hi = {"center": (-w["t"] / 2, w["t"] / 2), "left": (0, w["t"]),
                  "right": (-w["t"], 0)}[w["align"]]

        def at(along, across):
            return (a[0] + ux * along - uy * across, a[1] + uy * along + ux * across)
        centre = at(o["offset"] + t["width"] / 2, (lo + hi) / 2)
        if t["kind"] == "door":
            # A door leaf is drawn from its hinge, on the wall face it opens toward.
            hinge = o.get("hinge", "start")
            swing = flip(o.get("swing", "left"), mirrored)
            insert = at(o["offset"] + (0 if hinge == "start" else t["width"]),
                        hi if swing == "left" else lo)
        else:
            insert = centre
        out["openings"].append({"id": prefix + o["id"], "centre": centre, "insert": insert,
                                "u": (ux, uy), "kind": t["kind"], "wall_t": w["t"],
                                "width": t["width"]})
    for r in block.get("rooms", []):
        out["rooms"].append({"id": prefix + r["id"], "name": r["name"], "at": pt(r["at"]),
                             "use": r["use"], "need_area": r.get("need_area")})
    for c in filter(built, block.get("columns", [])):
        out["columns"].append({"id": prefix + c["id"], "at": pt(c["at"])})
    for s in filter(built, block.get("stairs", [])):
        up = next_level if s["up_to"] == "next" else s["up_to"]
        out["stairs"].append({"id": prefix + s["id"], "at": pt(s["start"]), "type": s["type"],
                              "up_to": up, "risers": s.get("risers"), "level": level_name})
    for key in ("voids", "shafts"):
        for v in block.get(key, []):
            if key == "voids" and v.get("floor", "none") != "none":
                continue  # a glass floor is walked on: part of the room below it
            a, b = pt(v["from"]), pt(v["to"])
            out[key].append({"id": prefix + v["id"], "poly": rect(a, b)})
    for i, pl in enumerate(block.get("placements", [])):
        place(out, pl, i, grid, tf, mirrored, prefix, d, level_name, next_level)


def place(out, pl, index, grid, tf, mirrored, prefix, d, level_name, next_level):
    cl = d["clusters"][pl["cluster"]]
    local = make_transform(resolve(pl["at"], grid), pl.get("rotate", 0), pl.get("mirror", "none"))
    m = mirrored != (pl.get("mirror", "none") != "none")
    add_block(out, cl, cl["grid"], compose(tf, local), m,
              f"{prefix}{pl['cluster']}#{index}/", d, level_name, next_level)


def flatten(d):
    """Every level's objects with placements unrolled, keyed by level name."""
    names = [lv["name"] for lv in d["levels"]]
    out = {n: new_level() for n in names}
    ident = lambda p: p  # noqa: E731
    for i, n in enumerate(names):
        nxt = names[i + 1] if i + 1 < len(names) else None
        if n in d["floors"]:
            add_block(out[n], d["floors"][n], d["grid"], ident, False, "", d, n, nxt)
    for i, pl in enumerate(d.get("placements", [])):
        for n in pl["levels"]:
            k = names.index(n)
            nxt = names[k + 1] if k + 1 < len(names) else None
            place(out[n], pl, f"g{i}", d["grid"], ident, False, "", d, n, nxt)
    return out


def rect(a, b):
    x0, x1 = sorted((a[0], b[0]))
    y0, y1 = sorted((a[1], b[1]))
    return [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]


def wall_poly(w):
    a, b, t = w["a"], w["b"], w["t"]
    length = math.hypot(b[0] - a[0], b[1] - a[1])
    nx, ny = -(b[1] - a[1]) / length, (b[0] - a[0]) / length  # left normal
    lo, hi = {"center": (-t / 2, t / 2), "left": (0, t), "right": (-t, 0)}[w["align"]]
    return [(a[0] + nx * lo, a[1] + ny * lo), (b[0] + nx * lo, b[1] + ny * lo),
            (b[0] + nx * hi, b[1] + ny * hi), (a[0] + nx * hi, a[1] + ny * hi)]


# ---- the drawing -----------------------------------------------------------

def closed_outlines(msp, layer):
    out = []
    for e in msp.query(f'LWPOLYLINE[layer=="{layer}"]'):
        pts = [tuple(p[:2]) for p in e.get_points("xy")]
        if len(pts) >= 3 and (e.closed or pts[0] == pts[-1]):
            if pts[0] == pts[-1]:
                pts = pts[:-1]
            out.append(pts)
    return out


def centroid(pts):
    return (sum(p[0] for p in pts) / len(pts), sum(p[1] for p in pts) / len(pts))


def polys_touch(a, b):
    if any(inside(p, b) for p in a) or any(inside(p, a) for p in b):
        return True
    return any(crosses(a[i - 1], a[i], b[j - 1], b[j])
               for i in range(len(a)) for j in range(len(b)))


def sector(arc, steps=12):
    """The swept area of a door leaf, in world coordinates: a mirrored block
    yields arcs in a flipped coordinate system, so convert through the OCS."""
    c = arc.ocs().to_wcs(arc.dxf.center)
    a0, a1 = arc.dxf.start_angle, arc.dxf.end_angle
    if a1 < a0:
        a1 += 360
    angles = [a0 + (a1 - a0) * k / steps for k in range(steps + 1)]
    return [(c.x, c.y)] + [(v.x, v.y) for v in arc.vertices(angles)]


# ---- raster sum: rooms + walls against the footprint ---------------------

def raster(polys_by_bit, box):
    x0, y0, x1, y1 = box
    nx, ny = int(math.ceil((x1 - x0) / CELL)) + 2, int(math.ceil((y1 - y0) / CELL)) + 2
    ox, oy = x0 - CELL, y0 - CELL
    grid = [bytearray(nx) for _ in range(ny)]
    for bit, polys in polys_by_bit.items():
        for poly in polys:
            ys = [p[1] for p in poly]
            j0 = max(0, int((min(ys) - oy) / CELL) - 1)
            j1 = min(ny - 1, int((max(ys) - oy) / CELL) + 1)
            for j in range(j0, j1 + 1):
                yc = oy + (j + 0.5) * CELL
                xs = []
                for k in range(len(poly)):
                    (ax, ay), (bx, by) = poly[k - 1], poly[k]
                    if (ay <= yc) != (by <= yc):
                        xs.append(ax + (yc - ay) * (bx - ax) / (by - ay))
                xs.sort()
                row = grid[j]
                for xa, xb in zip(xs[::2], xs[1::2]):
                    # cells whose centre lies in [xa, xb): half-open like the rows
                    i0 = max(0, int(math.ceil((xa - ox) / CELL - 0.5)))
                    i1 = min(nx - 1, int(math.ceil((xb - ox) / CELL - 0.5)) - 1)
                    for i in range(i0, i1 + 1):
                        row[i] |= bit
    return grid, nx, ny


def footprint_sum(rooms, walls, extras):
    pts = [p for poly in rooms + walls + extras for p in poly]
    box = (min(p[0] for p in pts), min(p[1] for p in pts),
           max(p[0] for p in pts), max(p[1] for p in pts))
    grid, nx, ny = raster({1: walls + extras, 2: rooms}, box)
    outside = [bytearray(nx) for _ in range(ny)]
    queue = deque([(0, 0)])
    outside[0][0] = 1
    while queue:
        i, j = queue.popleft()
        for a, b in ((i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)):
            if 0 <= a < nx and 0 <= b < ny and not outside[b][a] and not grid[b][a]:
                outside[b][a] = 1
                queue.append((a, b))
    foot = gap = both = 0
    for j in range(ny):
        for i in range(nx):
            if outside[j][i]:
                continue
            foot += 1
            v = grid[j][i]
            if v == 0:
                gap += 1
            elif v == 3:
                both += 1
    cell_m2 = CELL * CELL / 1e6
    return foot * cell_m2, gap * cell_m2, both * cell_m2


# ---- the checks -------------------------------------------------------------

def check(dxf_path, d):
    doc = ezdxf.readfile(dxf_path)
    msp = doc.modelspace()
    out = []

    def add(key, title, bad, warn=(), skip=None):
        status = "skip" if skip else "fail" if bad else "warn" if warn else "pass"
        out.append({"id": key, "title": title, "status": status,
                    "details": [skip] if skip else list(bad) + list(warn)})

    flat = flatten(d)
    names = [lv["name"] for lv in d["levels"]]
    elev = {lv["name"]: lv["elevation"] for lv in d["levels"]}
    kinds = {lv["name"]: lv["kind"] for lv in d["levels"]}
    origins = {dr["id"][5:]: tuple(dr["origin"]) for dr in d["drawings"]
               if dr["id"].startswith("plan:")}
    plans = [n for n in names if n in origins]
    if not plans:
        add("plans", "Có mặt bằng để kiểm", [], skip="danh mục hình không có mặt bằng nào")
        return out
    shift = lambda p, n: (p[0] + origins[n][0], p[1] + origins[n][1])  # noqa: E731
    unshift = lambda p, n: (p[0] - origins[n][0], p[1] - origins[n][1])  # noqa: E731

    # Each plan's area in the file: the table's walls and rooms, plus a margin.
    # Sections, elevations and the site plan sit elsewhere and are not read.
    region = {}
    for n in plans:
        pts = [shift(q, n) for w in flat[n]["walls"] for q in (w["a"], w["b"])]
        pts += [shift(r["at"], n) for r in flat[n]["rooms"]]
        region[n] = ((min(p[0] for p in pts) - REGION_MARGIN, min(p[1] for p in pts) - REGION_MARGIN,
                      max(p[0] for p in pts) + REGION_MARGIN, max(p[1] for p in pts) + REGION_MARGIN)
                     if pts else None)

    def plan_of(p):
        return next((n for n in plans if region[n] and region[n][0] <= p[0] <= region[n][2]
                     and region[n][1] <= p[1] <= region[n][3]), None)

    # Openings: one block per id, where the table puts it, no extras.
    inserts = []
    for e in msp.query('INSERT[layer=="A-DOOR" | layer=="A-GLAZ"]'):
        pos = (e.dxf.insert.x, e.dxf.insert.y)
        n = plan_of(pos)
        if n is None:
            continue
        oid = e.get_attrib_text("ID") if e.has_attrib("ID") else None
        inserts.append({"id": oid, "pos": pos, "plan": n, "layer": e.dxf.layer, "used": False})
    bad, by_id = [], {}
    for ins in inserts:
        by_id.setdefault((ins["plan"], ins["id"]), []).append(ins)
    for n in plans:
        for o in flat[n]["openings"]:
            want = shift(o["insert"], n)
            layer = "A-GLAZ" if o["kind"] == "window" else "A-DOOR"
            cands = [i for i in by_id.get((n, o["id"]), []) if not i["used"]]
            hit = next((i for i in cands if math.dist(i["pos"], want) <= POS_TOL), None)
            if hit:
                hit["used"] = True
                if hit["layer"] != layer:
                    bad.append(f"{n} {o['id']}: nằm trên {hit['layer']}, phải là {layer}")
            elif cands:
                near = min(cands, key=lambda i: math.dist(i["pos"], want))
                bad.append(f"{n} {o['id']}: lệch {math.dist(near['pos'], want):.0f} mm so với bảng số")
                near["used"] = True
            else:
                bad.append(f"{n} {o['id']}: không có block ô cửa mang ID này")
    for ins in inserts:
        if not ins["used"]:
            bad.append(f"{ins['plan']}: block ô cửa thừa ở ({ins['pos'][0]:.0f}, {ins['pos'][1]:.0f}), "
                       f"ID {ins['id']!r}")
    add("openings", "Ô cửa khớp bảng số: đủ, đúng chỗ, không thừa", bad)

    # Rooms: each has exactly one outline, and no outline holds two rooms.
    outlines = closed_outlines(msp, "X-AREA")
    room_poly = {}
    bad = []
    for n in plans:
        holders = {}
        for r in flat[n]["rooms"]:
            p = shift(r["at"], n)
            hits = [k for k, poly in enumerate(outlines) if inside(p, poly)]
            if not hits:
                bad.append(f"{n} {r['name']} ({r['id']}): không có đường bao X-AREA chứa nó")
                continue
            k = min(hits, key=lambda k: polygon_area(outlines[k]))
            room_poly[(n, r["id"])] = [unshift(q, n) for q in outlines[k]]
            holders.setdefault(k, []).append(r)
        for k, rs in holders.items():
            if len(rs) > 1:
                bad.append(f"{n}: một đường bao chứa {len(rs)} phòng: "
                           + ", ".join(r["name"] for r in rs) + " (thiếu tường hay ranh ảo)")
    add("rooms", "Mỗi phòng một đường bao riêng", bad)

    # Area against the brief's need.
    bad, warn = [], []
    for n in plans:
        for r in flat[n]["rooms"]:
            poly = room_poly.get((n, r["id"]))
            if not r["need_area"] or poly is None:
                continue
            got, need = polygon_area(poly) / 1e6, r["need_area"]
            line = f"{n} {r['name']}: {got:.2f} m² so với nhu cầu {need} m²"
            if got < need * NEED_LOW:
                bad.append(line)
            elif abs(got - need) > need * NEED_BAND:
                warn.append(line)
    add("need_area", "Diện tích phòng so với nhu cầu của đề", bad, warn)

    # Rooms + walls = footprint.
    bad = []
    for n in plans:
        rooms = [room_poly[(n, r["id"])] for r in flat[n]["rooms"] if (n, r["id"]) in room_poly]
        walls = [wall_poly(w) for w in flat[n]["walls"] if w["t"] > 0]
        extras = [v["poly"] for v in flat[n]["voids"] + flat[n]["shafts"]]
        if not rooms or not walls:
            continue
        foot, gap, both = footprint_sum(rooms, walls, extras)
        if gap > foot * GROSS_TOL:
            bad.append(f"{n}: {gap:.2f} m² trong phủ bì {foot:.2f} m² không thuộc phòng, tường hay ô trống nào")
        if both > foot * GROSS_TOL:
            bad.append(f"{n}: {both:.2f} m² đường bao phòng đè lên tường")
    add("gross", "Phòng cộng tường bằng phủ bì", bad)

    # Columns and wet rooms stack.
    warn = []
    cols = {n: [] for n in plans}
    for q in (centroid(p) for p in closed_outlines(msp, "A-COLS")):
        n = plan_of(q)
        if n:
            cols[n].append(unshift(q, n))
    for lo, hi in zip(plans, plans[1:]):
        if names.index(hi) != names.index(lo) + 1:
            continue
        for c in cols[hi]:
            if not any(math.dist(c, b) <= STACK_TOL for b in cols[lo]):
                warn.append(f"{hi}: cột ở ({c[0]:.0f}, {c[1]:.0f}) không có cột {lo} bên dưới")
        wet_lo = [room_poly[(lo, r["id"])] for r in flat[lo]["rooms"]
                  if r["use"] == "wet" and (lo, r["id"]) in room_poly]
        for r in flat[hi]["rooms"]:
            poly = room_poly.get((hi, r["id"]))
            if r["use"] == "wet" and poly and not any(inside(centroid(poly), q) for q in wet_lo):
                warn.append(f"{hi} {r['name']}: không có khu ướt {lo} bên dưới")
    add("stack", "Cột và khu ướt chồng thẳng", [], warn)

    # Stairs can be walked.
    bad, missing, count = [], [], 0
    for n in names:
        for s in flat[n]["stairs"]:
            count += 1
            t = d["types"]["stairs"][s["type"]]
            if not s["risers"]:
                missing.append(f"{n} {s['id']}: bảng số thiếu risers, chưa tính được cao bậc")
                continue
            if s["up_to"] is None:
                bad.append(f"{n} {s['id']}: up_to là next nhưng không có tầng trên")
                continue
            h = (elev[s["up_to"]] - elev[n]) / s["risers"]
            b = t["tread"]
            if b < TREAD_MIN:
                bad.append(f"{n} {s['id']}: mặt bậc {b} dưới {TREAD_MIN}")
            if not STEP_MIN <= 2 * h + b <= STEP_MAX:
                bad.append(f"{n} {s['id']}: 2×{h:.0f} + {b} = {2 * h + b:.0f}, "
                           f"ngoài {STEP_MIN}–{STEP_MAX}")
    add("stairs", "Thang đi được", bad, missing,
        skip=None if count else "bảng số không có thang")

    # Door leaves clear furniture.
    furn = []
    for e in msp.query('INSERT[layer=="A-FURN" | layer=="A-FLOR"]'):
        ext = bbox.extents([e])
        if ext.has_data:
            (x0, y0, _), (x1, y1, _) = ext.extmin, ext.extmax
            furn.append((e.dxf.name, [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]))
    bad = []
    for e in msp.query('INSERT[layer=="A-DOOR"]'):
        oid = e.get_attrib_text("ID") if e.has_attrib("ID") else "?"
        for arc in (v for v in e.virtual_entities() if v.dxftype() == "ARC"):
            sec = sector(arc)
            for name, box in furn:
                if polys_touch(sec, shrink_box(box)):
                    bad.append(f"cánh cửa {oid} quét vào {name}")
    add("swing", "Cánh cửa không vướng đồ đạc, thiết bị", bad)

    # Reachability and private rooms.
    graph, entries = build_graph(flat, plans, room_poly, kinds)
    use = {(n, r["id"]): r for n in plans for r in flat[n]["rooms"]}
    reach = bfs(graph, entries, set())
    bad = [f"{k[0]} {use[k]['name']}: không tới được từ cửa ra ngoài nào"
           for k in use if k not in reach]
    if not entries:
        bad.insert(0, "không có cửa ra ngoài nào")
    add("reach", "Tới được mọi phòng từ cửa ra ngoài", bad)
    bad = []
    private = {k for k, r in use.items() if r["use"] == "private"}
    for k, r in use.items():
        if k not in reach or r["use"] == "wet":
            continue  # a bathroom off one bedroom is an en-suite, not a passage
        if k not in bfs(graph, entries, private - {k}):
            bad.append(f"{k[0]} {r['name']}: chỉ tới được khi đi xuyên một phòng riêng")
    add("private", "Không phải đi xuyên phòng riêng", bad)
    return out


def shrink_box(box, by=20):
    (x0, y0), _, (x1, y1), _ = box
    return [(x0 + by, y0 + by), (x1 - by, y0 + by), (x1 - by, y1 - by), (x0 + by, y1 - by)]


def dist_to_poly(p, poly):
    if inside(p, poly):
        return 0.0
    best = math.inf
    for (ax, ay), (bx, by) in zip(poly, poly[1:] + poly[:1]):
        dx, dy = bx - ax, by - ay
        t = max(0.0, min(1.0, ((p[0] - ax) * dx + (p[1] - ay) * dy) / (dx * dx + dy * dy or 1)))
        best = min(best, math.dist(p, (ax + t * dx, ay + t * dy)))
    return best


def build_graph(flat, plans, room_poly, kinds):
    """Rooms linked by doors, open boundaries and stairs. A door with a room on
    one side only is a way in from outside on a ground level; on an upper
    level it is a balcony or a terrace and starts nothing."""
    graph, entries = {}, set()

    def room_at(n, p):
        hits = [r["id"] for r in flat[n]["rooms"]
                if (n, r["id"]) in room_poly and inside(p, room_poly[(n, r["id"])])]
        return (n, min(hits, key=lambda i: polygon_area(room_poly[(n, i)]))) if hits else None

    def in_void(n, p):
        return any(inside(p, v["poly"]) for v in flat[n]["voids"] + flat[n]["shafts"])

    def link(a, b):
        graph.setdefault(a, set()).add(b)
        graph.setdefault(b, set()).add(a)

    for n in plans:
        # Rooms drawn inside one outline are one space; the rooms check reports it.
        keys = [(n, r["id"]) for r in flat[n]["rooms"] if (n, r["id"]) in room_poly]
        for i, a in enumerate(keys):
            for b in keys[i + 1:]:
                if room_poly[a] == room_poly[b]:
                    link(a, b)
        for o in flat[n]["openings"]:
            if o["kind"] not in DOOR_KINDS:
                continue
            (cx, cy), (ux, uy) = o["centre"], o["u"]
            reach = o["wall_t"] / 2 + SIDE_REACH
            sides = [(cx - uy * reach, cy + ux * reach), (cx + uy * reach, cy - ux * reach)]
            rooms = [room_at(n, p) for p in sides]
            if all(rooms):
                link(*rooms)
            elif (any(rooms) and kinds[n] == "ground"
                  and not any(in_void(n, p) for p, r in zip(sides, rooms) if not r)):
                entries.add(next(r for r in rooms if r))
        for w in flat[n]["walls"]:
            if w["t"] != 0:
                continue
            a, b = w["a"], w["b"]
            m = ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)
            length = math.hypot(b[0] - a[0], b[1] - a[1])
            nx, ny = -(b[1] - a[1]) / length * SIDE_REACH, (b[0] - a[0]) / length * SIDE_REACH
            ra, rb = room_at(n, (m[0] + nx, m[1] + ny)), room_at(n, (m[0] - nx, m[1] - ny))
            if ra and rb and ra != rb:
                link(ra, rb)
        for s in flat[n]["stairs"]:
            up = s["up_to"]
            if up not in plans:
                continue
            # The foot of a stair may sit on a wall face, and upstairs it is often
            # over the stair well: on both floors take the nearest room within reach.
            ends = []
            for lv in (n, up):
                near = [(dist_to_poly(s["at"], room_poly[(lv, r["id"])]), r["id"])
                        for r in flat[lv]["rooms"] if (lv, r["id"]) in room_poly]
                near = [x for x in near if x[0] <= STAIR_REACH]
                ends.append((lv, min(near)[1]) if near else None)
            if all(ends):
                link(*ends)
    return graph, entries


def bfs(graph, starts, blocked):
    seen = {s for s in starts if s not in blocked}
    queue = deque(seen)
    while queue:
        a = queue.popleft()
        for b in graph.get(a, ()):
            if b not in seen:
                seen.add(b)
                if b not in blocked:
                    queue.append(b)
    return seen


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("dxf")
    ap.add_argument("params")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)
    try:
        d, dups = params_check.load(args.params)
    except (OSError, ValueError) as err:
        print(f"không đọc được {args.params}: {err}", file=sys.stderr)
        return 2
    rep = params_check.check(d, dups)
    if rep.errors:
        print("Bảng số chưa qua params_check.py, dừng:")
        for e in rep.errors:
            print(f"LỖI   {e['path']}: {e['msg']}")
        return 1
    try:
        results = check(args.dxf, d)
    except (OSError, ezdxf.DXFError) as err:
        print(f"không đọc được {args.dxf}: {err}", file=sys.stderr)
        return 2
    if args.json:
        json.dump(results, sys.stdout, ensure_ascii=False, indent=1)
        print()
    else:
        mark = {"pass": "đạt      ", "fail": "KHÔNG ĐẠT", "warn": "cần xem  ", "skip": "bỏ qua   "}
        for r in results:
            print(f"{mark[r['status']]}  {r['title']}")
            for line in r["details"]:
                print(f"           - {line}")
    return 1 if any(r["status"] == "fail" for r in results) else 0


if __name__ == "__main__":
    sys.exit(main())
