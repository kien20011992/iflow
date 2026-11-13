"""Read a number table (`cad-params/1`, references/bang-so.md) into plan
coordinates for the drawing functions. The table must already pass
scripts/params_check.py; nothing here re-validates it.
"""
import json
import math


def load(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def resolve(p, grid):
    """[[xname, offs…], [yname, offs…]] -> (x, y) in mm."""
    return tuple(grid[axis][ref[0]] + sum(ref[1:]) for axis, ref in zip(("x", "y"), p))


def wall_side(align, t):
    """(lo, hi): where the wall body lies across its line, to the left = +."""
    return {"center": (-t / 2, t / 2), "left": (0.0, float(t)), "right": (-float(t), 0.0)}[align]


class Wall:
    def __init__(self, raw, grid, types):
        self.id = raw["id"]
        self.type = raw["type"]
        self.a = resolve(raw["from"], grid)
        self.b = resolve(raw["to"], grid)
        self.t = types["walls"][raw["type"]]["thickness"]
        self.align = raw.get("align", "center")
        self.phase = raw.get("phase", "new")
        dx, dy = self.b[0] - self.a[0], self.b[1] - self.a[1]
        self.length = math.hypot(dx, dy)
        self.u = (dx / self.length, dy / self.length)
        self.n = (-self.u[1], self.u[0])  # left normal
        self.lo, self.hi = wall_side(self.align, self.t)

    @property
    def square(self):
        return abs(self.u[0]) < 1e-9 or abs(self.u[1]) < 1e-9

    def at(self, along, across):
        return (self.a[0] + self.u[0] * along + self.n[0] * across,
                self.a[1] + self.u[1] * along + self.n[1] * across)

    def rect(self, s0=0.0, s1=None):
        """The wall body between two distances along it, as a polygon."""
        s1 = self.length if s1 is None else s1
        return [self.at(s0, self.lo), self.at(s1, self.lo), self.at(s1, self.hi), self.at(s0, self.hi)]

    @property
    def angle(self):
        return math.degrees(math.atan2(self.u[1], self.u[0]))


class Opening:
    def __init__(self, raw, wall, types):
        t = types["openings"][raw["type"]]
        self.id = raw["id"]
        self.label = raw["type"]
        self.kind = t["kind"]
        self.width = t["width"]
        self.wall = wall
        self.offset = raw["offset"]
        self.hinge = raw.get("hinge", "start")
        self.swing = raw.get("swing", "left")
        self.centre = wall.at(self.offset + self.width / 2, (wall.lo + wall.hi) / 2)

    @property
    def span(self):
        return self.offset, self.offset + self.width

    @property
    def side(self):
        """+1 when the leaf opens to the wall's left, -1 to its right."""
        return 1 if self.swing == "left" else -1

    @property
    def hinge_point(self):
        s = self.offset if self.hinge == "start" else self.offset + self.width
        return self.wall.at(s, self.wall.hi if self.side > 0 else self.wall.lo)

    @property
    def closed_dir(self):
        """Direction from the hinge along the closed leaf."""
        k = 1 if self.hinge == "start" else -1
        return (self.wall.u[0] * k, self.wall.u[1] * k)

    @property
    def open_dir(self):
        return (self.wall.n[0] * self.side, self.wall.n[1] * self.side)

    def sector(self, steps=12):
        """The area the leaf sweeps, as a polygon."""
        h, c, o = self.hinge_point, self.closed_dir, self.open_dir
        pts = [h]
        for k in range(steps + 1):
            t = math.pi / 2 * k / steps
            pts.append((h[0] + self.width * (c[0] * math.cos(t) + o[0] * math.sin(t)),
                        h[1] + self.width * (c[1] * math.cos(t) + o[1] * math.sin(t))))
        return pts


class Floor:
    """One floor's objects, without clusters (those are marked, not drawn yet)."""

    def __init__(self, d, level):
        grid, types = d["grid"], d["types"]
        raw = d["floors"].get(level, {})
        self.level = level
        self.grid = grid
        self.walls = [Wall(w, grid, types) for w in raw.get("walls", [])]
        by_id = {w.id: w for w in self.walls}
        self.openings = [Opening(o, by_id[o["wall"]], types) for o in raw.get("openings", [])]
        self.rooms = [dict(r, at=resolve(r["at"], grid)) for r in raw.get("rooms", [])]
        self.columns = []
        for c in raw.get("columns", []):
            w, h = types["columns"][c["type"]]["size"]
            x, y = resolve(c["at"], grid)
            self.columns.append({"id": c["id"], "rect": rect((x - w / 2, y - h / 2), (x + w / 2, y + h / 2))})
        self.voids = [{"id": v["id"], "floor": v.get("floor", "none"),
                       "rect": rect(resolve(v["from"], grid), resolve(v["to"], grid))}
                      for v in raw.get("voids", [])]
        self.stairs = [dict(s, start=resolve(s["start"], grid)) for s in raw.get("stairs", [])]
        self.furniture = [dict(f, at=resolve(f["at"], grid)) for f in raw.get("furniture", [])]
        self.railings = raw.get("railings", [])
        self.placements = raw.get("placements", [])
        self.outside = [dict(o, near=resolve(o["near"], grid)) for o in raw.get("outside", [])]
        self.shafts = [{"id": s["id"], "rect": rect(resolve(s["from"], grid), resolve(s["to"], grid))}
                       for s in raw.get("shafts", [])]


def rect(a, b):
    x0, x1 = sorted((a[0], b[0]))
    y0, y1 = sorted((a[1], b[1]))
    return [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]
