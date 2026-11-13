"""A section through the building, built from the number table alone.

The cut runs along grid-square segments; segments parallel to the look
direction are the jogs of a broken cut and draw nothing. Along the cutting
segments, s is the horizontal position on the sheet (left to right as seen
looking the way `look` says) and z the elevation. Rules: references/ve.md,
"Một hình mặt cắt phải có gì". Structure sizes are estimates for drawing.
"""
import math

from bang_so import Floor, resolve
from hinh import Cells, bbox, inside, room_outline
from ky_hieu import Stair, _arrow, cao_do
from lenh import text_width
from mat_bang import box, grow, hang_kich_thuoc, overlaps

DEFAULTS = {"slab": 100, "beam": [200, 300], "parapet": 1000, "footing_depth": 1500,
            "footing_width": 800, "stair_waist": 120, "rail_height": 900}
EARTH_BAND = 400  # mm of cut earth hatched below the ground line
HEADROOM = 2000   # mm clear above any tread


def structure(d, todo):
    out = {}
    for k, v in DEFAULTS.items():
        entry = d.get("structure", {}).get(k)
        if entry is None:
            todo.append(f"mặt cắt: {k} lấy mặc định {v} (ước)")
            out[k] = v
        else:
            out[k] = entry["value"]
    return out


class Cut:
    """Maps plan points on the cut to (s, z) on the sheet."""

    def __init__(self, section, grid):
        self.name = section["name"]
        pts = [resolve(p, grid) for p in section["path"]]
        look = section["look"]
        self.axis = 1 if look in ("+x", "-x") else 0      # plan axis the cut runs along
        self.flip = look in ("+x", "-y")                   # sheet runs against that axis
        self.segments = []                                 # (fixed coordinate, s0, s1)
        for a, b in zip(pts, pts[1:]):
            if a[1 - self.axis] == b[1 - self.axis] and a[self.axis] != b[self.axis]:
                lo, hi = sorted((self.s(a), self.s(b)))
                self.segments.append((a[1 - self.axis], lo, hi))

    def s(self, p):
        v = p[self.axis]
        return -v if self.flip else v

    def at(self, s):
        """The cutting segment covering s, as its fixed plan coordinate, or None."""
        return next((c for c, lo, hi in self.segments if lo <= s <= hi), None)

    def crosses(self, poly):
        """The s range where a plan polygon meets the cut, or None."""
        best = None
        for c, lo, hi in self.segments:
            x0, y0, x1, y1 = bbox(poly)
            fixed_lo, fixed_hi = (x0, x1) if self.axis == 1 else (y0, y1)
            if not fixed_lo < c < fixed_hi:
                continue
            along = [self.s(p) for p in poly]
            a, b = max(min(along), lo), min(max(along), hi)
            if a < b:
                best = (a, b) if best is None else (min(best[0], a), max(best[1], b))
        return best


def mat_cat(L, d, section, origin, floors=None):
    """Draw one section; returns the list of things left for the user and the
    extent (x0, y0, x1, y1) in sheet coordinates. `floors`: {level: Floor},
    built once by the caller (built here when not given)."""
    L.origin = origin
    todo = []
    S = structure(d, todo)
    cut = Cut(section, d["grid"])
    if not cut.segments:
        return [f"mặt cắt {section['name']}: đường cắt không đi theo trục"], None
    levels = d["levels"]
    floors = floors or {lv["name"]: Floor(d, lv["name"]) for lv in levels}
    z_of = {lv["name"]: lv["elevation"] for lv in levels}
    ground = d.get("site", {}).get("ground_elevation", 0)
    slab, (bw, bh) = S["slab"], S["beam"]
    obstacles = []

    # The building's extent along the cut, from the walls the cut crosses.
    spans = [cut.crosses(w.rect()) for f in floors.values() for w in f.walls if w.t > 0]
    spans = [x for x in spans if x]
    if not spans:
        return [f"mặt cắt {section['name']}: đường cắt không qua tường nào"], None
    s_min, s_max = min(a for a, _ in spans), max(b for _, b in spans)
    plates = list(levels)              # every level has a floor plate…
    lowest = levels[0]["name"]         # …the lowest one lies on the ground, without beams
    top = max(z_of[lv["name"]] for lv in levels)

    def rect(s0, z0, s1, z1):
        return [(s0, z0), (s1, z0), (s1, z1), (s0, z1)]

    solids = []  # every cut part drawn: room names keep off them

    def solid(poly, layer="S-CUTS"):
        L.solid(poly, layer)
        solids.append(poly)

    # Holes in each floor plate where the cut meets a void or a stair coming up.
    def holes(name):
        out, glass = [], []
        f = floors[name]
        for v in f.voids:
            r = cut.crosses(v["rect"])
            if r:
                (glass if v["floor"] == "glass" else out).append(r)
        for lower in floors.values():
            for st in lower.stairs:
                if st["up_to"] != name:
                    continue
                stair = Stair(st, d["types"])
                r = cut.crosses(stair.footprint())  # the stair well: flights and landing
                if r and stair.supported:
                    out.append(r)
        return out, glass

    def cut_band(z0, z1, gaps, layer="S-CUTS"):
        """A solid band from s_min to s_max at z0..z1, broken by the gaps."""
        edges = [s_min]
        for a, b in sorted(gaps):
            edges += [max(a, s_min), min(b, s_max)]
        edges.append(s_max)
        for a, b in zip(edges[::2], edges[1::2]):
            if b - a > 1:
                solid(rect(a, z0, b, z1), layer)

    grid_s = sorted(cut.s((v, 0) if cut.axis == 0 else (0, v)) for v in d["grid"]["xy"[cut.axis]].values())
    # Floor plates, beams under the suspended ones, glass floors as two thin lines.
    for lv in plates:
        z = z_of[lv["name"]]
        gaps, glass = holes(lv["name"])
        cut_band(z - slab, z, gaps + glass)
        for a, b in glass:
            L.line((a, z), (b, z), "A-GLAZ")
            L.line((a, z - slab / 3), (b, z - slab / 3), "A-GLAZ")
        if lv["name"] != lowest:
            for g in grid_s:
                if s_min <= g <= s_max and not any(a < g < b for a, b in gaps + glass):
                    half = bw / 2
                    solid(rect(max(g - half, s_min), z - slab - bh, min(g + half, s_max), z - slab), "S-CUTS")
    # Parapet on the roof edges.
    roof = next((lv for lv in levels if lv["kind"] == "roof"), None)
    if roof:
        zr = z_of[roof["name"]]
        for s0 in (s_min, s_max - 200):
            solid(rect(s0, zr, s0 + 200, zr + S["parapet"]), "S-CUTS")

    # Walls the cut crosses, storey by storey, broken by their openings.
    footings = set()
    names = [lv["name"] for lv in levels]
    for k, lv in enumerate(levels):
        if lv["kind"] == "roof":
            continue
        name = lv["name"]
        z0 = z_of[name]
        z_next = z_of[names[k + 1]] if k + 1 < len(names) else z0 + lv["height"]
        z_top = z_next - slab - bh
        f = floors[name]
        for w in f.walls:
            if w.t == 0:
                continue
            r = cut.crosses(w.rect())
            if not r or r[1] - r[0] > w.t + 1:
                continue  # not crossing the cut, or running along it
            c = cut.at((r[0] + r[1]) / 2)
            pieces = [(z0, z_top)]
            for op in f.openings:
                if op.wall is not w:
                    continue
                pos = [op.wall.at(s_, 0)[1 - cut.axis] for s_ in op.span]
                if not (min(pos) < c < max(pos)):
                    continue
                t = d["types"]["openings"][op.label]
                lo = z0 + t.get("sill", 0)
                hi = lo + t.get("height", 2200)
                pieces = [(a, b) for a, b in pieces for a, b in ((a, min(b, lo)), (max(a, hi), b)) if b - a > 1]
                layer = "A-GLAZ" if op.kind == "window" else "A-DOOR"
                mid = (r[0] + r[1]) / 2
                L.line((mid, lo), (mid, hi), layer)
                if op.kind == "window":
                    L.line((r[0], lo), (r[1], lo), layer)
            for a, b in pieces:
                solid(rect(r[0], a, r[1], b), "S-CUTS")
            if name == lowest:
                footings.add((round(r[0]), round(r[1])))

    # Footings under the walls cut on the ground floor, then the ground.
    fd, fw = S["footing_depth"], S["footing_width"]
    z_ground_floor = z_of[lowest]
    for a, b in sorted(footings):
        mid = (a + b) / 2
        foot = min(ground, z_ground_floor) - fd  # under the lowest floor, basement included
        solid(rect(a, foot + 300, b, z_ground_floor - slab))
        solid(rect(mid - fw / 2, foot, mid + fw / 2, foot + 300))
    site = d.get("site", {}).get("outline")
    g0, g1 = (min(cut.s(p) for p in site), max(cut.s(p) for p in site)) if site else (s_min - 2000, s_max + 2000)
    L.line((g0, ground), (s_min, ground), "C-TOPO")
    L.line((s_max, ground), (g1, ground), "C-TOPO")
    necks = sorted(footings)
    xs = [g0] + [v for a, b in necks for v in (a, b)] + [g1]
    for a, b in zip(xs[::2], xs[1::2]):
        if b - a < 50:
            continue
        inside_house = s_min <= a and b <= s_max
        ztop = (z_ground_floor - slab) if inside_house else ground
        L.pline(rect(a, ztop - EARTH_BAND, b, ztop), "C-TOPO")
        L.c("hatch", handles=["{last}"], pattern="ANSI31", scale=L.scale / 4)
    if site:
        todo.append("mặt cắt: mẫu tô đất ANSI31 cần người mở AutoCAD xem lại")

    # Stairs: the flight the cut passes through, cut; the one behind it, seen.
    for name, f in floors.items():
        for st in f.stairs:
            stair = Stair(st, d["types"])
            if not stair.supported or not cut.crosses(stair.footprint()):
                continue
            d_axis = 0 if st["dir"] in ("+x", "-x") else 1
            if d_axis != cut.axis:
                todo.append(f"mặt cắt: thang {st['id']} bị cắt ngang vế, chưa vẽ")
                continue
            z0 = z_of[name]
            h = (z_of[st["up_to"]] - z0) / stair.risers
            ttop = S["stair_waist"]
            span = cut.crosses(stair.footprint())
            c = cut.at((span[0] + span[1]) / 2)  # the segment that passes through this stair
            for flight, (y_lo, y_hi), steps, z_start, forward in _flights(stair, h, z0):
                sl = cut.s(stair.P(0, 0))
                sgn = 1 if cut.s(stair.P(stair.b, 0)) > sl else -1
                across = [stair.P(0, y_lo)[1 - cut.axis], stair.P(0, y_hi)[1 - cut.axis]]
                is_cut = min(across) < c < max(across)
                pts = _profile(cut, stair, steps, z_start, h, forward, flight, sgn)
                if is_cut:
                    waist = _waist(pts, ttop)
                    solid(pts + waist, "S-CUTS")
                    # one handrail line along the cut flight, measured up from the nosings
                    rail = S["rail_height"]
                    L.line((pts[0][0], pts[0][1] + rail), (pts[-1][0], pts[-1][1] + rail), "A-RAIL")
                else:
                    L.pline(pts, "A-ELEV", closed=False)
                    solids.append(pts + [pts[-1], pts[0]])
            run = stair.f1 * stair.b
            if stair.kind == "u_turn":  # the landing plate, one piece
                s1 = cut.s(stair.P(run, 0))
                s2 = cut.s(stair.P(run + stair.landing, 0))
                zl = z0 + (stair.f1 + 1) * h
                solid(rect(min(s1, s2), zl - ttop, max(s1, s2), zl), "S-CUTS")
                run += stair.landing
            clear = _headroom(stair, h, z0, z_of[st["up_to"]], slab, run)
            if clear < HEADROOM:
                todo.append(f"mặt cắt: khoảng đầu thang {st['id']} chỉ {clear:.0f} mm")

    # Level marks right of the building, vertical dimensions left, grid below.
    xm = max(s_max, g1) + L.size("first_dim")
    zs = sorted({ground} | {z_of[lv["name"]] for lv in plates} | ({z_of[roof["name"]] + S["parapet"]} if roof else set()))
    prev, shift = None, 0
    for z in zs:  # marks closer than their own height step aside, alternately
        shift = (L.size("text") * 6 if shift == 0 else 0) if prev is not None and z - prev < L.size("text") * 2.6 else 0
        obstacles += cao_do(L, (xm + shift, z), z)
        prev = z
    xd = min(s_min, g0) - L.size("first_dim")
    obstacles += hang_kich_thuoc(L, "y", zs, xd, s_min, obstacles)
    obstacles += hang_kich_thuoc(L, "y", [zs[0], zs[-1]], xd - L.size("dim_gap"), s_min, obstacles)
    bottom = min(ground, z_ground_floor) - fd  # the footings' underside, below any basement
    zb = bottom - L.size("first_dim")
    inside_grid = [g for g in grid_s if s_min - 1 <= g <= s_max + 1]
    if len(inside_grid) >= 2:
        obstacles += hang_kich_thuoc(L, "x", inside_grid, zb, bottom, obstacles)
        zb -= L.size("dim_gap")
    obstacles += hang_kich_thuoc(L, "x", [s_min, s_max], zb, bottom, obstacles)
    r = L.size("grid_circle") / 2
    zr_ = zb - L.size("dim_gap") - r
    labels = {}
    for n_, v in d["grid"]["xy"[cut.axis]].items():
        labels[cut.s((v, 0) if cut.axis == 0 else (0, v))] = n_
    for g in inside_grid:
        L.line((g, zr_ + r), (g, top + S["parapet"] + 500), "A-GRID")
        L.circle((g, zr_), r, "A-GRID", linetype="Continuous")
        L.mtext((g, zr_), labels[g], L.size("grid_text"), "A-GRID")

    # Every space the cut passes through is named, inside it and clear of what is cut.
    hgt = L.size("text")
    for k, lv in enumerate(levels):
        if lv["kind"] == "roof":
            continue
        f = floors[lv["name"]]
        cells = Cells(f)
        if cells.empty:
            continue
        z0 = z_of[lv["name"]]
        for room in f.rooms:
            info = room_outline(cells, room["at"])
            if info is None:
                continue
            w = text_width(room["name"], hgt)
            spots = []
            for c, lo, hi in cut.segments:
                for k_ in range(int((hi - lo) // hgt) + 1):
                    s_ = lo + k_ * hgt
                    plan = (s_ if not cut.flip else -s_, c) if cut.axis == 0 else (c, s_ if not cut.flip else -s_)
                    if inside(plan, info["outline"]):
                        spots.append(s_)
            if not spots or max(spots) - min(spots) < 1000:
                continue  # the cut only grazes this room
            mid = sum(spots) / len(spots)
            name = room["name"]
            lines_opts = [[name]]
            if ", " in name:
                lines_opts.append([name.split(", ", 1)[0] + ",", name.split(", ", 1)[1]])
            elif " " in name:
                lines_opts.append(name.split(" ", 1))
            placed = False
            for lines in lines_opts:
                w = max(text_width(t, hgt) for t in lines)
                tall = hgt * (1.5 * len(lines) - 0.5)
                for s_ in sorted(spots, key=lambda v: abs(v - mid)):
                    if not (min(spots) <= s_ - w / 2 and s_ + w / 2 <= max(spots)):
                        continue
                    for zc in (z0 + 1500, z0 + 1100, z0 + 1900, z0 + 2400, z0 + 700):
                        b = box(s_, zc, w, tall)
                        if any(overlaps(grow(b, hgt / 4), o) for o in solids + obstacles):
                            continue
                        for i, t in enumerate(lines):
                            L.mtext((s_, zc + tall / 2 - hgt / 2 - i * 1.5 * hgt), t, hgt, "A-TEXT")
                        obstacles.append(b)
                        placed = True
                        break
                    if placed:
                        break
                if placed:
                    break
            if not placed:
                todo.append(f"mặt cắt: tên {room['name']} ({lv['name']}) không có chỗ")

    # A void the cut passes through is named too, at mid height of each storey it opens.
    for lv in levels:
        if lv["kind"] == "roof":
            continue
        for v in floors[lv["name"]].voids:
            span = cut.crosses(v["rect"])
            if not span or v["floor"] != "none":
                continue
            zc = z_of[lv["name"]] + 1500
            b = box((span[0] + span[1]) / 2, zc, text_width("Giếng trời", hgt), hgt)
            if not any(overlaps(grow(b, hgt / 2), o) for o in solids + obstacles):
                L.mtext(((span[0] + span[1]) / 2, zc), "Giếng trời", hgt, "A-TEXT")
                obstacles.append(b)

    # Title and the note on estimated structure.
    tz = zr_ - r - 2 * L.size("title")
    mid = (s_min + s_max) / 2
    L.mtext((mid, tz), f"MẶT CẮT {section['name']} - TL 1:{d['project']['scale']}", L.size("title"), "A-TEXT")
    note = (f"Sàn {slab}, dầm {bw}x{bh}, móng sâu {fd}: ước để vẽ, kỹ sư tính. Cao độ: m.")
    L.mtext((mid, tz - 1.6 * L.size("title")), note, L.size("text"), "A-TEXT")
    return todo, (min(xd, g0) - 3 * L.size("dim_gap"), tz - 3 * L.size("title"),
                  xm + 6 * L.size("text") + 2000, top + S["parapet"] + 1500)


def _flights(stair, h, z0):
    """(index, across range, treads, start elevation, forward) for each flight."""
    if stair.kind == "u_turn":
        y2 = stair.fw + stair.gap
        return [(1, (0, stair.fw), stair.f1, z0, True),
                (2, (y2, y2 + stair.fw), stair.f2, z0 + (stair.f1 + 1) * h, False)]
    return [(1, (0, stair.fw), stair.f1, z0, True)]


def _profile(cut, stair, steps, z_start, h, forward, flight, sgn):
    """Stepped line of one flight, as (s, z) from its foot to its head."""
    b = stair.b
    if forward:
        x0 = 0
        step = b
    else:
        x0 = stair.f1 * b
        step = -b
    s0 = cut.s(stair.P(x0, 0))
    ds = sgn * step
    pts = [(s0, z_start)]
    z = z_start
    s_ = s0
    for k in range(steps + 1):
        z += h
        pts.append((s_, z))
        if k < steps:
            s_ += ds
            pts.append((s_, z))
    return pts


def _waist(pts, t):
    """Underside of a flight: from below its head back to below its foot."""
    (sa, za), (sb, zb) = pts[0], pts[-1]
    slope = math.hypot(sb - sa, zb - za) / (abs(sb - sa) or 1)
    return [(sb, zb - t * slope), (sa, za - t * slope)]


def _headroom(stair, h, z0, z_up, slab, well):
    """Clear height above the treads of the first flight that lie under the
    slab above, i.e. outside the stair well cut in it (`well`: its length
    along the flight from the first step). Infinite when the well covers all."""
    worst = math.inf
    for k in range(stair.f1):
        if (k + 1) * stair.b > well:
            worst = min(worst, (z_up - slab) - (z0 + (k + 1) * h))
    return worst
