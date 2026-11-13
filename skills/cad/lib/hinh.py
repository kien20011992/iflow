"""Plan geometry from square walls: the solid wall mass as closed outlines,
and each room's outline traced from its point, by a cell model whose cell
edges are every wall face, opening jamb and column face (no rounding).

A cell is wall, column, opening (separates rooms, not drawn as wall), a void
with no floor, or free. Walls of thickness 0 block the passage between two
free cells without being cells. Walls that are not square to the axes are
left out; the caller marks them for the user.
"""
from collections import deque

FREE, WALL, COL, OPEN, VOID, SHAFT = 0, 1, 2, 3, 4, 5


def area(poly):
    return abs(sum(poly[i - 1][0] * poly[i][1] - poly[i][0] * poly[i - 1][1]
                   for i in range(len(poly)))) / 2


def inside(p, poly):
    x, y = p
    hit = False
    for (ax, ay), (bx, by) in zip(poly, poly[1:] + poly[:1]):
        if (ay > y) != (by > y) and x < ax + (y - ay) * (bx - ax) / (by - ay):
            hit = not hit
    return hit


def bbox(poly):
    xs, ys = [p[0] for p in poly], [p[1] for p in poly]
    return min(xs), min(ys), max(xs), max(ys)


class Cells:
    def __init__(self, floor, margin=1000):
        walls = [w for w in floor.walls if w.square]
        solid = [w for w in walls if w.t > 0]
        self.thin = [w for w in walls if w.t == 0]
        self.skipped = [w for w in floor.walls if not w.square]
        cuts = [o.wall.rect(*o.span) for o in floor.openings if o.wall in solid]
        boxes = [bbox(w.rect()) for w in solid] + [bbox(c["rect"]) for c in floor.columns] + \
                [bbox(r) for r in cuts] + [bbox(v["rect"]) for v in floor.voids] + \
                [bbox(s["rect"]) for s in floor.shafts]
        self.empty = not boxes and not self.thin
        if self.empty:  # a level with nothing on it: no cells, no rooms
            self.xs, self.ys, self.kind, self.blocked = [0, 1], [0, 1], [[FREE]], set()
            return
        xs = {b[0] for b in boxes} | {b[2] for b in boxes}
        ys = {b[1] for b in boxes} | {b[3] for b in boxes}
        for w in self.thin:
            xs |= {w.a[0], w.b[0]}
            ys |= {w.a[1], w.b[1]}
        x0, y0, x1, y1 = min(xs) - margin, min(ys) - margin, max(xs) + margin, max(ys) + margin
        self.xs = sorted(xs | {x0, x1})
        self.ys = sorted(ys | {y0, y1})
        nx, ny = len(self.xs) - 1, len(self.ys) - 1
        self.kind = [[FREE] * nx for _ in range(ny)]
        layers = ([(bbox(v["rect"]), VOID) for v in floor.voids if v["floor"] == "none"]
                  + [(bbox(s["rect"]), SHAFT) for s in floor.shafts]
                  + [(bbox(w.rect()), WALL) for w in solid]
                  + [(bbox(c["rect"]), COL) for c in floor.columns]
                  + [(bbox(r), OPEN) for r in cuts])
        for j in range(ny):
            cy = (self.ys[j] + self.ys[j + 1]) / 2
            for i in range(nx):
                cx = (self.xs[i] + self.xs[i + 1]) / 2
                for (bx0, by0, bx1, by1), k in layers:  # later layers win
                    if bx0 < cx < bx1 and by0 < cy < by1:
                        self.kind[j][i] = k
        self.blocked = set()
        for w in self.thin:
            if abs(w.u[1]) < 1e-9:  # runs along x at y = w.a[1]
                yv, a, b = w.a[1], *sorted((w.a[0], w.b[0]))
                j = self.ys.index(yv)
                for i in range(nx):
                    if a <= self.xs[i] and self.xs[i + 1] <= b:
                        self.blocked.add(((i, j - 1), (i, j)))
            else:
                xv, a, b = w.a[0], *sorted((w.a[1], w.b[1]))
                i = self.xs.index(xv)
                for j in range(ny):
                    if a <= self.ys[j] and self.ys[j + 1] <= b:
                        self.blocked.add(((i - 1, j), (i, j)))

    def cell_of(self, p):
        """The cell holding p; a point on a cell edge belongs to the cell above or right."""
        for i in range(len(self.xs) - 1):
            if self.xs[i] <= p[0] < self.xs[i + 1]:
                break
        else:
            return None
        for j in range(len(self.ys) - 1):
            if self.ys[j] <= p[1] < self.ys[j + 1]:
                return i, j
        return None

    def room_cells(self, p):
        start = self.cell_of(p)
        if start is None or self.kind[start[1]][start[0]] != FREE:
            return set()
        seen, queue = {start}, deque([start])
        nx, ny = len(self.xs) - 1, len(self.ys) - 1
        while queue:
            i, j = queue.popleft()
            for a, b in ((i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)):
                if not (0 <= a < nx and 0 <= b < ny) or (a, b) in seen:
                    continue
                if self.kind[b][a] != FREE:
                    continue
                edge = tuple(sorted(((i, j), (a, b))))
                if edge in self.blocked:
                    continue
                if a in (0, nx - 1) or b in (0, ny - 1):
                    return set()  # leaks out of the building: no closed room here
                seen.add((a, b))
                queue.append((a, b))
        return seen

    def wall_cells(self):
        return {(i, j) for j, row in enumerate(self.kind) for i, k in enumerate(row) if k in (WALL, COL)}

    def loops(self, cells):
        """Outlines of a set of cells, counter-clockwise around the cells,
        corners only; a set touching itself at a corner gives two loops."""
        edges = {}
        for i, j in cells:
            x0, x1, y0, y1 = self.xs[i], self.xs[i + 1], self.ys[j], self.ys[j + 1]
            for nb, a, b in (((i, j - 1), (x0, y0), (x1, y0)), ((i + 1, j), (x1, y0), (x1, y1)),
                             ((i, j + 1), (x1, y1), (x0, y1)), ((i - 1, j), (x0, y1), (x0, y0))):
                if nb not in cells:
                    edges.setdefault(a, []).append(b)
        loops = []
        while edges:
            start = next(iter(edges))
            loop, prev, cur = [start], None, start
            while True:
                outs = edges[cur]
                if len(outs) == 1:
                    nxt = outs.pop()
                else:  # a corner shared by two cells: turn left, keeping each piece apart
                    nxt = max(outs, key=lambda q: turn(prev, cur, q))
                    outs.remove(nxt)
                if not outs:
                    del edges[cur]
                prev, cur = cur, nxt
                if cur == start:
                    break
                loop.append(cur)
            loops.append(simplify(loop))
        return loops


def turn(prev, cur, nxt):
    """Larger for a sharper left turn."""
    if prev is None:
        return 0
    ax, ay = cur[0] - prev[0], cur[1] - prev[1]
    bx, by = nxt[0] - cur[0], nxt[1] - cur[1]
    return ax * by - ay * bx


def simplify(loop):
    out = []
    n = len(loop)
    for k in range(n):
        a, b, c = loop[k - 1], loop[k], loop[(k + 1) % n]
        if (b[0] - a[0]) * (c[1] - b[1]) - (b[1] - a[1]) * (c[0] - b[0]) != 0:
            out.append(b)
    return out


def room_outline(cells_model, p):
    """The outline of the room holding point p, its area in m², and its
    cell centres (candidate label points); None when p is not in a closed room."""
    cells = cells_model.room_cells(p)
    if not cells:
        return None
    loops = cells_model.loops(cells)
    outer = max(loops, key=area)
    holes = sum(area(q) for q in loops if q is not outer)
    # The outline drawn on X-AREA is the outer loop only, so the printed area is
    # the outer loop's too (the checkers measure that outline); `hole_area` is
    # what it includes — a column or void standing free in the room — for the
    # handover list.
    centres = [((cells_model.xs[i] + cells_model.xs[i + 1]) / 2, (cells_model.ys[j] + cells_model.ys[j + 1]) / 2)
               for i, j in cells]
    return {"outline": outer, "area": area(outer) / 1e6, "holes": len(loops) - 1,
            "hole_area": holes / 1e6, "centres": centres}
