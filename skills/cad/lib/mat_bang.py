"""Drawing functions for one floor plan. Each takes plan coordinates and
appends CADCraft commands to a `Lenh`; the ones that place text return the
box they used so later placements can avoid it. Layers and symbols follow
references/ve.md and the contract in references/bang-so.md.
"""
import math

from hinh import area, bbox, inside
from lenh import BLOCKS, text_width

# ---- small geometry ---------------------------------------------------------


def box(cx, cy, w, h):
    return [(cx - w / 2, cy - h / 2), (cx + w / 2, cy - h / 2), (cx + w / 2, cy + h / 2), (cx - w / 2, cy + h / 2)]


def _cross(a, b, c, d):
    def side(p, q, r):
        return (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])
    return side(a, b, c) * side(a, b, d) < 0 and side(c, d, a) * side(c, d, b) < 0


def overlaps(p, q):
    """Two polygons share some area (touching edges do not count)."""
    a, b = bbox(p), bbox(q)
    if a[2] <= b[0] or b[2] <= a[0] or a[3] <= b[1] or b[3] <= a[1]:
        return False  # boxes apart: the cheap answer, most of the time
    if any(inside(v, q) for v in p) or any(inside(v, p) for v in q):
        return True
    return any(_cross(p[i - 1], p[i], q[k - 1], q[k]) for i in range(len(p)) for k in range(len(q)))


def segment_hits(a, b, poly):
    """A straight segment crosses or enters a polygon."""
    if inside(a, poly) or inside(b, poly):
        return True
    return any(_cross(a, b, poly[k - 1], poly[k]) for k in range(len(poly)))


def grow(poly, by):
    x0, y0, x1, y1 = bbox(poly)
    return [(x0 - by, y0 - by), (x1 + by, y0 - by), (x1 + by, y1 + by), (x0 - by, y1 + by)]


def fits(candidate, room, obstacles):
    return all(inside(v, room) for v in candidate) and not any(overlaps(candidate, o) for o in obstacles)


# ---- walls, columns, openings ---------------------------------------------


def tuong(L, loops):
    """The cut wall mass: each outline of it, closed, on A-WALL (left unfilled)."""
    for loop in loops:
        L.pline(loop, "A-WALL")


def tuong_giai_doan(L, walls):
    """Walls that are not standing once the work is done: to be demolished on
    A-DEMO, to be built later on A-FUTR, both dashed by their layer."""
    for w in walls:
        L.pline(w.rect(), "A-DEMO" if w.phase == "demolish" else "A-FUTR")


def cot(L, columns):
    """Columns, solid filled on A-COLS."""
    for c in columns:
        L.solid(c["rect"], "A-COLS")


def door_block(op):
    """The leaf symbol for this door, or None when assets/blocks/ has no leaf of
    its width (the caller then marks the door for the user)."""
    left_of_leaf = (op.closed_dir[0] * op.open_dir[1] - op.closed_dir[1] * op.open_dir[0]) > 0
    width = int(op.width) if float(op.width).is_integer() else op.width
    name = f"CUA-{width}-{'T' if left_of_leaf else 'P'}"
    return name if (L_BLOCKS / f"{name}.dxf").exists() else None


L_BLOCKS = BLOCKS


def cua(L, op):
    """A door: the leaf block inserted at its hinge, on the face it opens toward.
    T blocks open to the left of their x axis, P blocks to the right; the block
    is turned so its x axis follows the closed leaf."""
    name = door_block(op)
    rot = math.degrees(math.atan2(op.closed_dir[1], op.closed_dir[0]))
    L.insert(name, op.hinge_point, "A-DOOR", rotation=rot, attribs={"ID": op.id})
    x0, y0, x1, y1 = bbox(op.sector())  # the whole quarter square: what a reader sees as the door
    return [[(x0, y0), (x1, y0), (x1, y1), (x0, y1)]]


def cua_so(L, op, layer="A-GLAZ", name="CUA-SO"):
    """A window (or a shutter): a unit symbol scaled to the opening and the wall."""
    w = op.wall
    L.insert(name, op.centre, layer, rotation=w.angle, scale=[op.width, w.t], attribs={"ID": op.id})
    return []


def cua_cuon(L, op):
    return cua_so(L, op, layer="A-DOOR", name="CUA-CUON")


def ve_o_cua(L, op):
    """Draw one opening; returns (obstacles, None) or ([], why it was not drawn)."""
    if op.wall.t == 0:
        return [], f"ô cửa {op.id} nằm trên ranh ảo bề dày 0"
    if op.kind == "door":
        if door_block(op) is None:
            return [], f"cửa {op.id} rộng {op.width}: chưa có block cánh cỡ này"
        return cua(L, op), None
    if op.kind == "window":
        return cua_so(L, op), None
    return cua_cuon(L, op), None


# ---- labels -----------------------------------------------------------------


def _tag_spots(op, r, gap):
    """Where a door tag may go, in the order references/ve.md tries them: beside
    the hinge jamb, beside the far jamb, in front of the door — all on the side
    the leaf opens to, outside its sweep — then outside the door by the hinge."""
    h, c, o = op.hinge_point, op.closed_dir, op.open_dir
    d = r + gap
    w = op.width
    inner = [(h[0] - c[0] * d + o[0] * d, h[1] - c[1] * d + o[1] * d),
             (h[0] + c[0] * (w + d) + o[0] * d, h[1] + c[1] * (w + d) + o[1] * d),
             (h[0] + c[0] * w / 2 + o[0] * (w + d), h[1] + c[1] * w / 2 + o[1] * (w + d))]
    t = op.wall.t
    outer = [(h[0] - c[0] * d - o[0] * (t + d), h[1] - c[1] * d - o[1] * (t + d)),
             (h[0] + c[0] * (w + d) - o[0] * (t + d), h[1] + c[1] * (w + d) - o[1] * (t + d)),
             (h[0] + c[0] * w / 2 - o[0] * (t + d), h[1] + c[1] * w / 2 - o[1] * (t + d))]
    outer += [(h[0] + c[0] * (w + d + k * d) - o[0] * (t + d * (1 + j)),
               h[1] + c[1] * (w + d + k * d) - o[1] * (t + d * (1 + j))) for k in range(4) for j in range(3)]
    return inner, outer


def nhan_cua(L, op, rooms, obstacles, emit=True):
    """The tag of an opening (P1, V1…): a ring with its type name. Returns the
    ring's box, or None when no free spot was found. With emit=False nothing
    is drawn; draw the returned ring later with ve_nhan_cua."""
    r = L.size("tag") / 2
    gap = L.size("text")
    if op.kind == "door":
        inner, outer = _tag_spots(op, r, gap)
        spots = [(p, True) for p in inner] + [(p, False) for p in outer]
    else:  # windows and shutters: inside the house, along the wall
        w = op.wall
        mid = op.offset + op.width / 2
        spots = []
        for side in (1, -1):
            across = (w.hi if side > 0 else w.lo) + side * (r + gap)
            for along in (mid, op.offset - r - gap, op.offset + op.width + r + gap):
                spots.append((w.at(along, across), True))
    # the side the leaf does not open to: a room, or outside the house
    h, o = op.hinge_point, op.open_dir
    probe = (h[0] - o[0] * (op.wall.t + gap), h[1] - o[1] * (op.wall.t + gap))
    exterior = not any(inside(probe, q) for q in rooms)
    for p, in_room in spots:
        ring = box(p[0], p[1], 2 * r, 2 * r)
        room = next((q for q in rooms if inside(p, q)), None)
        if room is not None and not all(inside(v, room) for v in ring):
            continue  # a tag never straddles a room's edge
        if room is None and (in_room or not exterior):
            continue  # only an outside door may carry its tag outside the house
        if any(overlaps(grow(ring, gap / 2), o) for o in obstacles):
            continue
        if emit:
            ve_nhan_cua(L, op, ring)
        return ring
    return None


def ve_nhan_cua(L, op, ring):
    x0, y0, x1, y1 = bbox(ring)
    p = ((x0 + x1) / 2, (y0 + y1) / 2)
    L.circle(p, (x1 - x0) / 2, "A-ANNO")
    L.mtext(p, op.label, L.size("text"), "A-ANNO")


def ten_phong(L, room, info, obstacles):
    """Room name and area as centred MTEXTs inside the room, away from door
    sweeps, tags and other text, and the room outline on X-AREA. Returns the
    boxes used, or None when the text does not fit anywhere in the room: then
    call ten_phong_ngoai once the dimensions are drawn."""
    L.pline(info["outline"], "X-AREA")
    plan = cho_ten_phong(L, room, info, obstacles)
    if plan is None:
        return None
    ve_ten_phong(L, plan)
    return [b for *_, b in plan]


def ve_ten_phong(L, plan):
    for text, size, rot, at, _ in plan:
        L.mtext(at, text, size, "A-TEXT", rotation=rot)


def cho_ten_phong(L, room, info, obstacles):
    """Where the room's label goes, without drawing it: a list of
    (text, size, rotation, point, box), or None when nothing fits."""
    outline = info["outline"]
    m = L.size("margin")
    area_txt = f"{info['area']:.2f} m²".replace(".", ",")
    x0, y0, x1, y1 = bbox(outline)
    step = L.size("room")
    lattice = [(x0 + i * step, y0 + j * step) for i in range(1, int((x1 - x0) // step))
               for j in range(1, int((y1 - y0) // step))]
    tries = [room["at"]] + sorted(info["centres"] + lattice, key=lambda p: math.dist(p, room["at"]))
    h2 = L.size("text")
    # In the order references/ve.md gives: two lines, smaller, one line, then
    # turned along the room's long side, reading from below.
    layouts = []
    for size in (L.size("room"), h2):
        layouts.append([(room["name"], size, 0, h2 * 0.7), (area_txt, h2, 0, -size * 0.7)])
    # a long name broken over two lines, at the comma or the middle space
    words = room["name"].replace(", ", ",\0").split("\0") if ", " in room["name"] else room["name"].split(" ")
    if len(words) > 1:
        cut = min(range(1, len(words)), key=lambda k: abs(len(" ".join(words[:k])) - len(" ".join(words[k:]))))
        top, bottom = " ".join(words[:cut]), " ".join(words[cut:])
        for size in (L.size("room"), h2):
            layouts.append([(top, size, 0, h2 * 0.7 + size * 1.2), (bottom, size, 0, h2 * 0.7),
                            (area_txt, h2, 0, -size * 0.7)])
    tight = area_txt.replace(" m²", "m²")
    layouts.append([(room["name"], h2, 0, h2 * 0.7), (tight, h2, 0, -h2 * 0.7)])
    layouts.append([(f"{room['name']} {area_txt}", h2, 0, 0)])
    for size in (L.size("room"), h2):
        layouts.append([(room["name"], size, 90, -h2 * 0.7), (area_txt, h2, 90, size * 0.7)])
    for lines in layouts:
        for p in tries:
            placed = []
            for text, size, rot, shift in lines:
                w, h = text_width(text, size) + 2 * m, size + m
                if rot:
                    placed.append((text, size, rot, (p[0] + shift, p[1]), box(p[0] + shift, p[1], h, w)))
                else:
                    placed.append((text, size, rot, (p[0], p[1] + shift), box(p[0], p[1] + shift, w, h)))
            if all(fits(b, outline, obstacles) for *_, b in placed):
                return placed
    return None


def ten_phong_ngoai(L, room, info, obstacles, building):
    """The last resort of references/ve.md for a room too small for its label:
    the label outside the house, clear of dimension lines, joined to the room by
    a straight leader with one end inside the room. `building` is the outer
    box (x0, y0, x1, y1) of the walls. Returns the boxes used, or None."""
    h = L.size("text")
    m = L.size("margin")
    area_txt = f"{info['area']:.2f} m²".replace(".", ",")
    w = max(text_width(room["name"], h), text_width(area_txt, h)) + 2 * m
    tall = 2 * (h + m)
    X0, Y0, X1, Y1 = building
    start = room["at"]
    step = h
    spots = []
    reach = h * 1.5 + tall / 2  # off the face, before the extension lines start
    for k in range(-40, 41):
        spots += [(start[0] + k * step, Y1 + reach), (start[0] + k * step, Y0 - reach),
                  (X1 + reach + w / 2, start[1] + k * step), (X0 - reach - w / 2, start[1] + k * step)]
    longest = 40 * L.scale  # a leader longer than 40 mm on paper no longer reads as one
    for p in sorted(spots, key=lambda q: math.dist(q, start)):
        if math.dist(p, start) > longest:
            break
        nb = box(p[0], p[1] + (h + m) / 2, w, h + m)
        ab = box(p[0], p[1] - (h + m) / 2, w, h + m)
        if any(X0 < v[0] < X1 and Y0 < v[1] < Y1 for b in (nb, ab) for v in b):
            continue
        if any(overlaps(grow(b, m), o) for b in (nb, ab) for o in obstacles):
            continue
        # the leader ends on the area text itself (not its margin): that is what a reader follows
        x0, y0, x1, y1 = bbox(box(p[0], p[1] - (h + m) / 2, text_width(area_txt, h), h))
        # the leader may start anywhere inside the room: take the shortest one
        # that runs over no number, tag or dimension line
        for a in sorted([start] + info["centres"], key=lambda q: math.dist(q, p)):
            end = (min(max(a[0], x0), x1), min(max(a[1], y0), y1))
            if not any(segment_hits(a, end, o) for o in obstacles):
                break
        else:
            continue
        L.mtext((p[0], p[1] + (h + m) / 2), room["name"], h, "A-TEXT")
        L.mtext((p[0], p[1] - (h + m) / 2), area_txt, h, "A-TEXT")
        L.line(a, end, "A-TEXT")
        return [nb, ab, grow([a, end], h / 10)]
    return None


# ---- grid, dimensions, site ----------------------------------------------


def hang_kich_thuoc(L, axis, values, at, face, obstacles):
    """One closed row of dimensions between consecutive values along `axis`
    ("x": a horizontal row at y = at, measured on the face line y = face).
    A number too wide for its gap is moved past the gap's end."""
    vals = sorted(set(round(v, 3) for v in values))
    h = L.size("text")
    thin = h / 10
    # extension lines (face to row) and the dimension line: thin boxes later text avoids
    boxes = [box(v, (face + at) / 2, thin, abs(at - face)) if axis == "x"
             else box((face + at) / 2, v, abs(at - face), thin) for v in vals]
    span = vals[-1] - vals[0]
    boxes.append(box((vals[0] + vals[-1]) / 2, at, span, thin) if axis == "x"
                 else box(at, (vals[0] + vals[-1]) / 2, thin, span))
    gaps = list(zip(vals, vals[1:]))
    fit = [text_width(str(round(b - a)), h) + 2 * L.size("margin") <= b - a for a, b in gaps]
    # where the numbers that fit their gap will stand: moved numbers must avoid them
    staying = [box((a + b) / 2, at + h, text_width(str(round(b - a)), h), h) if axis == "x"
               else box(at - h, (a + b) / 2, h, text_width(str(round(b - a)), h))
               for (a, b), ok in zip(gaps, fit) if ok]
    for k, (a, b) in enumerate(gaps):
        txt = str(round(b - a))
        tw = text_width(txt, h)
        move = None
        if not fit[k]:
            # out past the nearer end of the row first, then the other side, then further out
            order = (a - tw / 2 - h, b + tw / 2 + h) if k == 0 else (b + tw / 2 + h, a - tw / 2 - h)
            for past in order + (b + 1.5 * tw + 2 * h, a - 1.5 * tw - 2 * h):
                cand = (past, at + h) if axis == "x" else (at - h, past)
                cb = box(*cand, tw, h) if axis == "x" else box(*cand, h, tw)
                if not any(overlaps(cb, o) for o in staying + boxes[len(vals) + 1:] + list(obstacles)):
                    move = cand
                    break
            else:
                move = cand
        if axis == "x":
            L.dim((a, face), (b, face), (a, at), 0, move)
            cx, cy = (move or ((a + b) / 2, at + h))
            boxes.append(box(cx, cy, tw, h))
        else:
            L.dim((face, a), (face, b), (at, a), 90, move)
            cx, cy = (move or (at - h, (a + b) / 2))
            boxes.append(box(cx, cy, h, tw))
    return boxes


def truc(L, grid, x_span, y_span):
    """Grid lines across the plan and a ring with the grid name at both ends,
    beyond everything else (x_span, y_span: where the rings sit)."""
    r = L.size("grid_circle") / 2
    th = L.size("grid_text")
    for name, x in grid["x"].items():
        L.line((x, y_span[0] + r), (x, y_span[1] - r), "A-GRID")
        for y in y_span:
            L.circle((x, y), r, "A-GRID", linetype="Continuous")
            L.mtext((x, y), name, th, "A-GRID")
    for name, y in grid["y"].items():
        L.line((x_span[0] + r, y), (x_span[1] - r, y), "A-GRID")
        for x in x_span:
            L.circle((x, y), r, "A-GRID", linetype="Continuous")
            L.mtext((x, y), name, th, "A-GRID")


def ranh_dat(L, outline):
    L.pline([tuple(p) for p in outline], "C-PROP")


def danh_dau(L, poly, what, obstacles, within=None):
    """Mark something the library does not draw yet: a revision cloud around it
    and a short note, both on A-REVS, the note inside `within` when given.
    Returns the note's box (or None when the note found no free spot)."""
    x0, y0, x1, y1 = bbox(poly)
    pad = L.size("text")
    L.revcloud((x0 - pad, y0 - pad), (x1 + pad, y1 + pad))
    h = L.size("text")
    txt = f"chưa vẽ: {what}"
    w = text_width(txt, h)
    for p in (((x0 + x1) / 2, (y0 + y1) / 2), ((x0 + x1) / 2, y1 + pad + h),
              ((x0 + x1) / 2, y0 - pad - h)):
        b = box(p[0], p[1], w, h)
        if within and not all(inside(v, within) for v in b):
            continue
        if not any(overlaps(grow(b, h / 2), o) for o in obstacles):
            L.mtext(p, txt, h, "A-REVS")
            return b
    return None


def tieu_de(L, at, text):
    L.mtext(at, text, L.size("title"), "A-TEXT")
    return box(at[0], at[1], text_width(text, L.size("title")), L.size("title"))


__all__ = ["tuong", "cot", "cua", "cua_so", "cua_cuon", "ve_o_cua", "nhan_cua", "ten_phong",
           "ten_phong_ngoai", "hang_kich_thuoc", "truc", "ranh_dat", "danh_dau", "tieu_de", "area"]
