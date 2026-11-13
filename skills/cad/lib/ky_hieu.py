"""Plan symbols beyond walls and openings: stairs, voids, railings, shafts,
furniture and fixtures, level marks, the north arrow and the section line.
Each appends CADCraft commands to a `Lenh` and returns the polygons later
text must avoid. Rules: references/ve.md, "Một hình mặt bằng phải có gì".
"""
import math

from hinh import bbox, inside
from lenh import BLOCKS, text_width
from mat_bang import box, grow, overlaps

DIRS = {"+x": (1, 0), "-x": (-1, 0), "+y": (0, 1), "-y": (0, -1)}
FIXTURES = {"BON-CAU", "LAVABO", "CHAU-RUA-BEP", "BAN-BEP", "MAY-GIAT"}  # on A-FLOR; the rest on A-FURN
# footprint of each symbol in assets/blocks/, centred on its origin (width, depth)
SIZES = {"GIUONG-DOI": (1600, 2000), "GIUONG-DON": (1000, 2000), "SOFA-3": (2000, 800),
         "BAN-AN-6": (1700, 1400), "BON-CAU": (400, 650), "LAVABO": (500, 400),
         "CHAU-RUA-BEP": (800, 450), "BAN-BEP": (600, 2000), "MAY-GIAT": (600, 600)}


# ---- stairs ----------------------------------------------------------------

class Stair:
    """A stair in plan. Local frame: x along the first flight from its first
    step (`start`, on the wall side), y across toward the side it turns to.
    `role` is how this floor sees it: "bottom" (it leaves from here), "middle"
    (it arrives here and leaves again), "top" (it only arrives)."""

    def __init__(self, st, types):
        t = types["stairs"][st["type"]]
        self.id = st["id"]
        self.kind = t["kind"]
        self.fw = t["flight_width"]
        self.b = t["tread"]
        self.gap = t.get("gap", 0)
        self.landing = t.get("landing", self.fw)
        self.risers = st.get("risers") or 18
        ex = DIRS[st["dir"]]
        left = (-ex[1], ex[0])
        ey = left if st.get("turn", "left") == "left" else (-left[0], -left[1])
        sx, sy = st["start"]
        self.P = lambda x, y: (sx + ex[0] * x + ey[0] * y, sy + ex[1] * x + ey[1] * y)  # noqa: E731
        self.angle = math.degrees(math.atan2(ex[1], ex[0]))
        if self.kind == "u_turn":
            r1 = (self.risers + 1) // 2
            self.f1, self.f2 = r1 - 1, self.risers - r1 - 1
        else:
            self.f1, self.f2 = self.risers - 1, 0

    @property
    def supported(self):
        return self.kind in ("straight", "u_turn")

    def footprint(self):
        if self.kind == "u_turn":
            run = self.f1 * self.b + self.landing
            return [self.P(0, 0), self.P(run, 0), self.P(run, 2 * self.fw + self.gap), self.P(0, 2 * self.fw + self.gap)]
        return [self.P(0, 0), self.P(self.f1 * self.b, 0), self.P(self.f1 * self.b, self.fw), self.P(0, self.fw)]


def thang(L, st, role):
    """Draw one stair for this floor's role; returns its footprint as obstacle."""
    s = st
    b, fw, f1 = s.b, s.fw, s.f1
    P = s.P
    cut = max(2, round(f1 / 3)) * b - b / 2 if role in ("bottom", "middle") else None
    num_h = L.size("text") * 0.72  # 1.8 mm on paper
    lab_h = L.size("text")

    def tread_line(x, y0, y1, layer):
        L.line(P(x, y0), P(x, y1), layer)

    # first flight
    for k in range(f1 + 1):
        x = k * b
        if cut is not None and x > cut:
            if role == "bottom":
                tread_line(x, 0, fw, "A-OVHD")
        else:
            tread_line(x, 0, fw, "A-STRS")
    end1 = f1 * b
    for y in (0, fw):  # the two sides of the first flight
        if cut is None:
            L.line(P(0, y), P(end1, y), "A-STRS")
        else:
            L.line(P(0, y), P(cut, y), "A-STRS")
            if role == "bottom":
                L.line(P(cut, y), P(end1, y), "A-OVHD")
    if cut is not None:  # the break line across the first flight
        L.line(P(cut - b / 2, -b / 4), P(cut + b / 2, fw + b / 4), "A-STRS")
    # Every tread is numbered when the number fits its tread, else only the
    # first and last of each flight.
    every = num_h <= b * 0.8
    shown = lambda k, last: every or k in (1, last)  # noqa: E731
    for k in range(1, f1 + 1):
        if shown(k, f1) and (cut is None or (k - 0.5) * b < cut or role == "bottom"):
            L.mtext(P((k - 0.5) * b, fw * 0.2), str(k), num_h, "A-STRS")

    if s.kind == "u_turn":
        y2 = fw + s.gap
        start2 = end1 - s.f2 * b
        seen_below = role in ("middle", "top")
        layer2 = "A-STRS" if seen_below else "A-OVHD"
        # landing: one plate, no line across it
        L.pline([P(end1, 0), P(end1 + s.landing, 0), P(end1 + s.landing, y2 + fw), P(end1, y2 + fw)],
                layer2)
        for k in range(s.f2 + 1):
            tread_line(start2 + k * b, y2, y2 + fw, layer2)
        L.line(P(start2, y2), P(end1, y2), layer2)
        L.line(P(start2, y2 + fw), P(end1, y2 + fw), layer2)
        for k in range(1, s.f2 + 1):
            if shown(k, s.f2):
                L.mtext(P(end1 - (k - 0.5) * b, y2 + fw * 0.8), str(f1 + k), num_h, layer2)
        if role in ("middle", "top"):
            _arrow(L, P(start2 + b / 2, y2 + fw / 2), P(end1 - b / 2, y2 + fw / 2), "A-STRS")
            L.mtext(P(start2 + b / 2 + text_width("XUỐNG", lab_h) / 2, y2 + fw * 0.25),
                    "XUỐNG", lab_h, "A-STRS", rotation=s.angle)
    if role in ("bottom", "middle"):
        tip = (cut - b) if cut else end1 - b / 2
        _arrow(L, P(b / 2, fw / 2), P(tip, fw / 2), "A-STRS")
        L.mtext(P(b / 2 + text_width("LÊN", lab_h) / 2, fw * 0.8), "LÊN", lab_h, "A-STRS", rotation=s.angle)
    elif s.kind == "straight":  # a straight stair seen from its top
        _arrow(L, P(end1 - b / 2, fw / 2), P(b / 2, fw / 2), "A-STRS")
        L.mtext(P(end1 - b / 2 - text_width("XUỐNG", lab_h) / 2, fw * 0.8), "XUỐNG", lab_h, "A-STRS",
                rotation=s.angle)
    return [s.footprint()]


def _arrow(L, a, b, layer):
    L.line(a, b, layer)
    d = (b[0] - a[0], b[1] - a[1])
    n = math.hypot(*d) or 1
    u = (d[0] / n, d[1] / n)
    v = (-u[1], u[0])
    s = L.size("text") * 0.6
    L.solid([b, (b[0] - u[0] * 2 * s + v[0] * s * 0.6, b[1] - u[1] * 2 * s + v[1] * s * 0.6),
             (b[0] - u[0] * 2 * s - v[0] * s * 0.6, b[1] - u[1] * 2 * s - v[1] * s * 0.6)], layer)


# ---- openings in floors, railings, shafts ---------------------------------

def gieng_troi(L, void):
    """A void: its edge and a cross on A-FLOR when the floor is open. A glass
    floor is walked on: its edge on A-GLAZ, and the room's text may cross it."""
    r = void["rect"]
    if void["floor"] == "none":
        L.pline(r, "A-FLOR")
        L.line(r[0], r[2], "A-FLOR")
        L.line(r[1], r[3], "A-FLOR")
        return [r]
    L.pline(r, "A-GLAZ")
    return []


def lan_can(L, railing):
    L.pline(railing["points"], "A-RAIL", closed=False)
    pts = railing["points"]
    return [grow([a, b], L.size("text") / 10) for a, b in zip(pts, pts[1:])]


def hop_ky_thuat(L, shaft):
    r = shaft["rect"]
    L.pline(r, "A-FLOR")
    L.line(r[0], r[2], "A-FLOR")
    if shaft.get("kind") == "lift":
        L.line(r[1], r[3], "A-FLOR")
    return [r]


# ---- furniture and fixtures -------------------------------------------------

def do_dac(L, item):
    """A furniture or fixture symbol from assets/blocks/, centred on `at`.
    Returns (obstacles, None), or ([], why) when the symbol does not exist."""
    name = item["block"]
    if not (BLOCKS / f"{name}.dxf").exists() or name not in SIZES:
        return [], f"đồ {name}: chưa có block"
    rot = item.get("rotate", 0)
    L.insert(name, item["at"], "A-FLOR" if name in FIXTURES else "A-FURN", rotation=rot)
    w, h = SIZES[name]
    if rot in (90, 270):
        w, h = h, w
    return [box(*item["at"], w, h)], None


# ---- marks -------------------------------------------------------------------

def free_spot(room, w, h, obstacles, start=None):
    """The first point in a room (by its cell centres, nearest `start` first)
    where a w x h box sits wholly inside and clear of the obstacles."""
    x0, y0, x1, y1 = bbox(room["outline"])
    step = max(h, 100)
    lattice = [(x0 + w / 2 + i * step, y0 + h / 2 + j * step)
               for i in range(int((x1 - x0 - w) // step) + 1) for j in range(int((y1 - y0 - h) // step) + 1)]
    cands = list(room["centres"]) + lattice
    if start is not None:
        cands = sorted(cands, key=lambda p: math.dist(p, start))
    for p in cands:
        b = box(p[0], p[1], w, h)
        if all(inside(v, room["outline"]) for v in b) and not any(overlaps(grow(b, h / 4), o) for o in obstacles):
            return p
    return None


def cao_do(L, at, z):
    """Level mark: a small triangle on the point and the level in metres."""
    s = L.size("text")
    label = "±0.000" if z == 0 else f"{z / 1000:+.3f}"
    x, y = at
    L.pline([(x, y), (x - s * 0.6, y + s), (x + s * 0.6, y + s)], "A-ANNO")
    L.line((x - s * 0.6, y + s), (x + s * 0.8 + text_width(label, s), y + s), "A-ANNO")
    L.mtext((x + s * 0.8 + text_width(label, s) / 2, y + s * 1.7), label, s, "A-ANNO")
    w = s * 1.4 + text_width(label, s)
    return [box(x + w / 2 - s * 0.6, y + s * 1.1, w + s, s * 2.4)]


def cao_do_size(L, z):
    s = L.size("text")
    label = "±0.000" if z == 0 else f"{z / 1000:+.3f}"
    return s * 1.4 + text_width(label, s) + s, s * 2.4


def huong_bac(L, at, north_deg):
    """North arrow: a ring, an arrow through it toward north, and the letter B."""
    r = L.size("grid_circle")
    a = math.radians(north_deg)
    u = (math.cos(a), math.sin(a))
    L.circle(at, r, "A-ANNO")
    _arrow(L, (at[0] - u[0] * r, at[1] - u[1] * r), (at[0] + u[0] * r, at[1] + u[1] * r), "A-ANNO")
    p = (at[0] + u[0] * (r + L.size("text") * 1.2), at[1] + u[1] * (r + L.size("text") * 1.2))
    L.mtext(p, "B", L.size("text"), "A-ANNO")
    return [box(at[0], at[1], 2 * r + 3 * L.size("text"), 2 * r + 3 * L.size("text"))]


def duong_cat(L, section, path):
    """The section line on a plan: a phantom line along the path, an arrow at
    each end toward the side looked at, and the section's name by each arrow."""
    L.pline(path, "A-ANNO", closed=False)
    L.c("properties.set", handles=["{last}"], linetype="PHANTOM")
    look = DIRS[section["look"]]
    h = L.size("room")
    obstacles = [grow([a, b], h / 10) for a, b in zip(path, path[1:])]
    for end in (path[0], path[-1]):
        tip = (end[0] + look[0] * 3 * h, end[1] + look[1] * 3 * h)
        _arrow(L, end, tip, "A-ANNO")
        at = (tip[0] + look[0] * h, tip[1] + look[1] * h)
        L.mtext(at, section["name"], h, "A-ANNO")
        obstacles.append(box(at[0], at[1], text_width(section["name"], h), h))
    return obstacles
