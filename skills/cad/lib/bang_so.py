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


def flip(side, mirrored):
    return {"left": "right", "right": "left"}.get(side, side) if mirrored else side


class Wall:
    def __init__(self, raw, pt, types, mirrored=False, prefix=""):
        self.id = prefix + raw["id"]
        self.type = raw["type"]
        self.a = pt(raw["from"])
        self.b = pt(raw["to"])
        self.t = types["walls"][raw["type"]]["thickness"]
        self.align = flip(raw.get("align", "center"), mirrored)
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
    def __init__(self, raw, wall, types, mirrored=False, prefix=""):
        t = types["openings"][raw["type"]]
        self.id = prefix + raw["id"]
        self.label = raw["type"]
        self.kind = t["kind"]
        self.width = t["width"]
        self.wall = wall
        self.offset = raw["offset"]
        self.hinge = raw.get("hinge", "start")
        self.swing = flip(raw.get("swing", "left"), mirrored)
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


DIRS = {"+x": (1, 0), "-x": (-1, 0), "+y": (0, 1), "-y": (0, -1)}
DRAWN = ("new", "existing")  # phases standing once the work is done


def transform(at, rotate, mirror):
    """Point and direction maps for one placement: mirror, then rotate, then move."""
    c, s_ = round(math.cos(math.radians(rotate))), round(math.sin(math.radians(rotate)))

    def vec(v):
        x, y = v
        if mirror == "x":
            x = -x
        elif mirror == "y":
            y = -y
        return (c * x - s_ * y, s_ * x + c * y)

    def point(p):
        x, y = vec(p)
        return (at[0] + x, at[1] + y)
    return point, vec


class Floor:
    """One floor's objects in building coordinates, every placement of a cluster
    unrolled — inside the floor, and from the table's root for this level — with
    ids extended as references/bang-so.md says (`cụm#n/…`, `cụm#g<n>/…`).
    Walls that are demolished or built later are kept apart in `other_walls`."""

    def __init__(self, d, level):
        self.level = level
        self.grid = d["grid"]
        self.types = d["types"]
        self.d = d
        for key in ("walls", "other_walls", "openings", "rooms", "columns", "voids", "stairs",
                    "furniture", "railings", "outside", "shafts", "skipped_openings", "unbuilt"):
            setattr(self, key, [])
        names = [lv["name"] for lv in d["levels"]]
        k = names.index(level) if level in names else -1
        self.next_level = names[k + 1] if 0 <= k < len(names) - 1 else None
        ident = (lambda p: p, lambda v: v)
        if level in d["floors"]:
            self._add(d["floors"][level], self.grid, ident, False, "")
        for i, pl in enumerate(d.get("placements", [])):
            if level in pl["levels"]:
                self._place(pl, f"g{i}", self.grid, ident, False, "")

    def _place(self, pl, index, grid, outer, mirrored, prefix):
        cl = self.d["clusters"][pl["cluster"]]
        p_in, v_in = transform(resolve(pl["at"], grid), pl.get("rotate", 0), pl.get("mirror", "none"))
        p_out, v_out = outer
        tf = (lambda p: p_out(p_in(p)), lambda v: v_out(v_in(v)))
        m = mirrored != (pl.get("mirror", "none") != "none")
        self._add(cl, cl["grid"], tf, m, f"{prefix}{pl['cluster']}#{index}/")

    def _add(self, raw, grid, tf, mirrored, prefix):
        point, vec = tf
        pt = lambda p: point(resolve(p, grid))  # noqa: E731
        types = self.types

        def standing(key):
            """The objects of one list that stand once the work is done; the
            others (to be demolished, built later) are kept for the handover."""
            out = []
            for o in raw.get(key, []):
                if o.get("phase", "new") in DRAWN:
                    out.append(o)
                else:
                    self.unbuilt.append((key, prefix + o["id"], o["phase"]))
            return out
        walls = {}
        for w in raw.get("walls", []):
            wall = Wall(w, pt, types, mirrored, prefix)
            walls[w["id"]] = wall
            (self.walls if wall.phase in DRAWN else self.other_walls).append(wall)
        for o in raw.get("openings", []):
            op = Opening(o, walls[o["wall"]], types, mirrored, prefix)
            standing_op = op.wall.phase in DRAWN and o.get("phase", "new") in DRAWN
            (self.openings if standing_op else self.skipped_openings).append(op)
        for r in raw.get("rooms", []):
            self.rooms.append(dict(r, id=prefix + r["id"], at=pt(r["at"])))
        for c in standing("columns"):
            w, h = types["columns"][c["type"]]["size"]
            x, y = pt(c["at"])
            ex, ey = vec((w / 2, h / 2))
            self.columns.append({"id": prefix + c["id"],
                                 "rect": rect((x - abs(ex), y - abs(ey)), (x + abs(ex), y + abs(ey)))})
        for v in raw.get("voids", []):
            self.voids.append({"id": prefix + v["id"], "floor": v.get("floor", "none"),
                               "rect": rect(pt(v["from"]), pt(v["to"]))})
        for sh in standing("shafts"):
            self.shafts.append({"id": prefix + sh["id"], "kind": sh.get("kind"),
                                "rect": rect(pt(sh["from"]), pt(sh["to"]))})
        for st in standing("stairs"):
            dx, dy = vec(DIRS[st["dir"]])
            direction = next(k for k, v in DIRS.items() if v == (round(dx), round(dy)))
            up = self.next_level if st["up_to"] == "next" else st["up_to"]
            self.stairs.append(dict(st, id=prefix + st["id"], start=pt(st["start"]), dir=direction,
                                    turn=flip(st.get("turn", "left"), mirrored), up_to=up))
        for f in standing("furniture"):
            # the placement turns the piece too: follow its axis through the placement
            a = math.radians(f.get("rotate", 0))
            ux, uy = vec((math.cos(a), math.sin(a)))
            rot = round(math.degrees(math.atan2(uy, ux))) % 360
            self.furniture.append(dict(f, id=prefix + f["id"], at=pt(f["at"]), rotate=rot))
        for rl in standing("railings"):
            self.railings.append({"id": prefix + rl["id"], "points": [pt(p) for p in rl["points"]]})
        for o in raw.get("outside", []):
            self.outside.append(dict(o, id=prefix + o["id"], near=pt(o["near"])))
        for i, pl in enumerate(raw.get("placements", [])):
            self._place(pl, i, grid, tf, mirrored, prefix)


def rect(a, b):
    x0, x1 = sorted((a[0], b[0]))
    y0, y1 = sorted((a[1], b[1]))
    return [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]
