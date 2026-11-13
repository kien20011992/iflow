#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# dependencies = ["ezdxf>=1.3"]
# ///
"""dxf_check.py FILE [--json] — read a DXF with a reader that is not CADCraft
and report what is wrong with it as a drawing handed to AutoCAD.

Run it with `uv run dxf_check.py FILE`, or with any Python that has ezdxf.
It knows nothing about how the file was built: every expected value comes
from the file itself (a dimension against its own two points, an area label
against the outline it sits in). Exit 0 = no check failed, 1 = at least one
failed, 2 = the file could not be read.
"""
import argparse
import json
import math
import re
import sys

import ezdxf
from ezdxf import bbox
from ezdxf.entities import DimStyleOverride

TOL = 1.0  # mm; one unit of rounding on a drawing in whole millimetres
AREA_TOL = 0.06  # m2; a label rounded to two decimals, plus slack
AREA_RE = re.compile(r"(\d+(?:[.,]\d+)?)\s*m(?:²|2|\^2)")
NUM_RE = re.compile(r"-?\d+(?:[.,]\d+)?")


def polygon_area(pts):
    return abs(sum(a[0] * b[1] - b[0] * a[1] for a, b in zip(pts, pts[1:] + pts[:1]))) / 2


def inside(p, pts):
    x, y, hit = p[0], p[1], False
    for (x1, y1), (x2, y2) in zip(pts, pts[1:] + pts[:1]):
        if (y1 > y) != (y2 > y) and x < (x2 - x1) * (y - y1) / (y2 - y1) + x1:
            hit = not hit
    return hit


def crosses(a, b, c, d):
    def side(p, q, r):
        return (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])
    return side(a, b, c) * side(a, b, d) < 0 and side(c, d, a) * side(c, d, b) < 0


def self_crossing(pts):
    segs = list(zip(pts, pts[1:] + pts[:1]))
    return any(crosses(*segs[i], *segs[j])
               for i in range(len(segs)) for j in range(i + 2, len(segs))
               if not (i == 0 and j == len(segs) - 1))


def self_touching(pts):
    seen = {}
    for i, (x, y) in enumerate(pts):
        key = (round(x, 3), round(y, 3))
        if key in seen and i - seen[key] > 1 and not (seen[key] == 0 and i == len(pts) - 1):
            return True
        seen[key] = i
    return False


SOLID_AREA = 4.0e6  # mm2: closed shapes up to a double bed count as solid


def segments(e):
    """Straight pieces of a line or polyline, arcs replaced by their chord."""
    if e.dxftype() == "LINE":
        return [((e.dxf.start[0], e.dxf.start[1]), (e.dxf.end[0], e.dxf.end[1]))]
    if e.dxftype() == "LWPOLYLINE":
        pts = [(x, y) for x, y, _ in e.get_points("xyb")]
        pairs = list(zip(pts, pts[1:]))
        return pairs + ([(pts[-1], pts[0])] if e.closed and len(pts) > 2 else [])
    return []


def shrink(box, part=0.15):
    """The box minus a margin, so a line that only grazes a text's edge passes."""
    dx, dy = (box[2] - box[0]) * part, (box[3] - box[1]) * part
    return box[0] + dx, box[1] + dy, box[2] - dx, box[3] - dy


def segment_hits_box(a, b, box):
    """Liang-Barsky: does segment a-b pass through the box?"""
    (x0, y0), (x1, y1) = a, b
    dx, dy, t0, t1 = x1 - x0, y1 - y0, 0.0, 1.0
    for p, q in ((-dx, x0 - box[0]), (dx, box[2] - x0), (-dy, y0 - box[1]), (dy, box[3] - y0)):
        if p == 0:
            if q < 0:
                return False
        else:
            t = q / p
            if p < 0:
                t0 = max(t0, t)
            else:
                t1 = min(t1, t)
            if t0 > t1:
                return False
    return True


def text_box(e):
    """Axis-aligned box (x0, y0, x1, y1) a TEXT or MTEXT covers, estimated."""
    lines = text_of(e).splitlines() or [""]
    if e.dxftype() == "MTEXT":
        h = e.dxf.get("char_height", 1.0)
        col, row = (e.dxf.get("attachment_point", 1) - 1) % 3, (e.dxf.get("attachment_point", 1) - 1) // 3
        rot = e.get_rotation()
        anchor = e.dxf.insert
        height = h * (1 + 1.4 * (len(lines) - 1))
        top = {0: 0, 1: height / 2, 2: height}[row]
    else:
        h = e.dxf.get("height", 1.0)
        halign, valign = e.dxf.get("halign", 0), e.dxf.get("valign", 0)
        col = {0: 0, 1: 1, 2: 2, 4: 1}.get(halign, 0)
        rot = e.dxf.get("rotation", 0.0)
        anchor = e.dxf.align_point if (halign or valign) and e.dxf.hasattr("align_point") else e.dxf.insert
        height = h
        top = {0: h, 1: h, 2: h / 2, 3: 0}.get(valign, h)
    width = max(len(line) for line in lines) * 0.7 * h
    left = {0: 0, 1: -width / 2, 2: -width}[col]
    corners = [(left, top), (left + width, top), (left, top - height), (left + width, top - height)]
    c, s_ = math.cos(math.radians(rot)), math.sin(math.radians(rot))
    pts = [(anchor[0] + x * c - y * s_, anchor[1] + x * s_ + y * c) for x, y in corners]
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    return min(xs), min(ys), max(xs), max(ys)


def overlap(a, b, gap=None):
    """True when two boxes overlap, or sit closer than a tenth of the smaller
    one's short side: two numbers that touch read as one."""
    if gap is None:
        gap = 0.1 * min(a[2] - a[0], a[3] - a[1], b[2] - b[0], b[3] - b[1])
    w = min(a[2], b[2]) - max(a[0], b[0]) + gap
    h = min(a[3], b[3]) - max(a[1], b[1]) + gap
    return w > 0 and h > 0


UNICODE_ESCAPE = re.compile(r"\\U\+([0-9A-Fa-f]{4})")


def text_of(e):
    """The readable text; a pre-2007 file keeps non-Latin letters as \\U+XXXX."""
    raw = e.plain_text() if e.dxftype() == "MTEXT" else e.dxf.get("text", "")
    return UNICODE_ESCAPE.sub(lambda m: chr(int(m.group(1), 16)), raw)


def at(e):
    p = e.dxf.insert
    return f"({p[0]:.0f}, {p[1]:.0f})"


def check(path, area_layer, wall_layer, want_version, object_layers=("A-FURN", "A-FLOR", "A-DOOR"),
          anno_layer="A-ANNO"):
    doc = ezdxf.readfile(path)
    msp = list(doc.modelspace())
    out = []

    def add(key, title, bad, warn=(), skip=None):
        status = "skip" if skip else "fail" if bad else "warn" if warn else "pass"
        out.append({"id": key, "title": title, "status": status,
                    "details": [skip] if skip else list(bad) + list(warn)})

    auditor = doc.audit()
    add("audit", "File đọc được, không lỗi cấu trúc",
        [f"{e.code}: {e.message}" for e in auditor.errors])

    add("version", f"Định dạng {want_version}, chữ lưu UTF-8",
        [] if doc.dxfversion == want_version else [f"file là {doc.dxfversion}"])

    units, metric = doc.header.get("$INSUNITS"), doc.header.get("$MEASUREMENT")
    add("units", "Đơn vị milimét, hệ mét",
        [m for m in (f"$INSUNITS = {units}, cần 4" if units != 4 else "",
                     f"$MEASUREMENT = {metric}, cần 1" if metric != 1 else "") if m])

    on0 = [e.dxftype() for e in msp if e.dxf.layer == "0"]
    add("layer0", "Không có đối tượng ở layer 0",
        [f"{len(on0)} đối tượng: {', '.join(sorted(set(on0)))}"] if on0 else [])

    names = {b.name for b in doc.blocks}
    add("blocks", "Mọi block được chèn đều có định nghĩa",
        [f"thiếu block {e.dxf.name}" for e in msp
         if e.dxftype() == "INSERT" and e.dxf.name not in names])

    texts = [e for e in msp if e.dxftype() in ("TEXT", "MTEXT")]
    bad = [f"chữ rỗng tại {at(e)}" for e in texts if not text_of(e).strip()]
    bad += [f"chữ vỡ dấu tại {at(e)}: {text_of(e)!r}" for e in texts
            if "�" in text_of(e) or "??" in text_of(e)]
    used = {e.dxf.get("style", "Standard") for e in texts}
    # AutoCAD reads a font name with no extension as an SHX file.
    shx = [f"kiểu chữ {s.dxf.name} dùng font {s.dxf.font!r}, cần tên file .ttf" for s in doc.styles
           if s.dxf.name in used and not s.dxf.get("font", "").lower().endswith((".ttf", ".otf"))]
    add("text", "Chữ không rỗng, không vỡ dấu, dùng font TrueType", bad + shx,
        skip=None if texts else "bản vẽ không có chữ")

    dims = [e for e in msp if e.dxftype() == "DIMENSION" and e.dimtype in (0, 1)]
    bad, chains = [], {}
    for e in dims:
        real = e.get_measurement()
        where = f"kích thước tại ({e.dxf.defpoint[0]:.0f}, {e.dxf.defpoint[1]:.0f})"
        override = e.dxf.get("text", "")
        if override not in ("", "<>"):
            bad.append(f"{where}: chữ số bị gõ đè {override!r}, hình đo {real:.0f}")
        if e.dxf.hasattr("actual_measurement") and abs(e.dxf.actual_measurement - real) > TOL:
            bad.append(f"{where}: file ghi {e.dxf.actual_measurement:.0f}, hình đo {real:.0f}")
        block = e.get_geometry_block()
        shown = next((NUM_RE.search(text_of(t)) for t in block or []
                      if t.dxftype() in ("TEXT", "MTEXT")), None)
        factor = DimStyleOverride(e).get("dimlfac", 1.0) or 1.0
        if shown and override in ("", "<>"):
            value = float(shown.group().replace(",", "."))
            if abs(value - real * factor) > TOL:
                bad.append(f"{where}: hiện {value:g}, hình đo {real * factor:.0f}")
        angle = round(e.dxf.get("angle", 0.0)) % 180
        if e.dimtype == 0 and angle in (0, 90):
            axis = 0 if angle == 0 else 1
            a, b = sorted((e.dxf.defpoint2[axis], e.dxf.defpoint3[axis]))
            chains.setdefault((angle, round(e.dxf.defpoint[1 - axis])), []).append((a, b))
    # A row holds one chain per drawing: floors placed side by side share rows,
    # so a gap longer than the row's longest span starts a new chain.
    runs = []
    for (angle, line), spans in sorted(chains.items()):
        spans.sort()
        longest = max(b - a for a, b in spans)
        run = [spans[0]]
        for span in spans[1:]:
            if span[0] - run[-1][1] > longest:
                runs.append((angle, line, run))
                run = []
            run.append(span)
        runs.append((angle, line, run))
    warn = []
    for angle, line, spans in runs:
        name = f"hàng kích thước {'ngang' if angle == 0 else 'đứng'} tại {line}"
        for (_, end), (start, _) in zip(spans, spans[1:]):
            if abs(start - end) > TOL:
                warn.append(f"{name}: hở hoặc chồng {abs(start - end):.0f} tại {end:.0f}")
        lo, hi = spans[0][0], spans[-1][1]
        # Compare a row only with the next parallel row of the same drawing:
        # the nearest one beyond it that covers most of it, within its own length.
        later = [(line2, other) for angle2, line2, other in runs
                 if angle2 == angle and 0 < line2 - line <= hi - lo
                 and min(hi, other[-1][1]) - max(lo, other[0][0]) > 0.8 * max(hi - lo, other[-1][1] - other[0][0])]
        if later:
            line2, other = min(later, key=lambda item: item[0])
            lo2, hi2 = other[0][0], other[-1][1]
            if abs(lo - lo2) > TOL or abs(hi - hi2) > TOL:
                warn.append(f"{name} dài {hi - lo:.0f}, hàng tại {line2} dài {hi2 - lo2:.0f}: không khép")
    add("dims", "Kích thước khớp với hình, các hàng khép nhau", bad, warn,
        skip=None if dims else "bản vẽ không có kích thước thẳng")

    # Text boxes are estimated from the text itself (0.7 x height per character,
    # an Arial-like width), never from a rendered image, so the check does not
    # depend on which fonts this machine has.
    boxes = []
    for e in texts:
        boxes.append((text_box(e), f"{text_of(e).splitlines()[0][:20]!r} tại {at(e)}"))
    for e in msp:  # labels drawn inside blocks, such as door and window tags
        if e.dxftype() != "INSERT":
            continue
        for t in list(e.attribs) + [v for v in e.virtual_entities() if v.dxftype() in ("TEXT", "MTEXT")]:
            if t.dxftype() == "ATTRIB" and t.is_invisible:
                continue  # a hidden tag, such as the opening ID the checkers read, is never printed
            if text_of(t).strip():
                boxes.append((text_box(t), f"nhãn {text_of(t)!r} của block {e.dxf.name} tại {at(e)}"))
    for e in dims:
        for t in e.get_geometry_block() or []:
            if t.dxftype() in ("TEXT", "MTEXT") and text_of(t).strip():
                boxes.append((text_box(t), f"số kích thước {text_of(t)!r} tại {at(t)}"))
    # A short label inside a circle (a door tag) takes the circle's box.
    for c in (e for e in msp if e.dxftype() == "CIRCLE"):
        cx, cy, r = c.dxf.center[0], c.dxf.center[1], c.dxf.radius
        for k, (b, name) in enumerate(boxes):
            mx, my = (b[0] + b[2]) / 2, (b[1] + b[3]) / 2
            if (mx - cx) ** 2 + (my - cy) ** 2 < r * r and b[2] - b[0] < 2 * r:
                boxes[k] = ((cx - r, cy - r, cx + r, cy + r), name)
    clash = []
    for i in range(len(boxes)):
        for j in range(i + 1, len(boxes)):
            if overlap(boxes[i][0], boxes[j][0]):
                clash.append(f"{boxes[i][1]} đè {boxes[j][1]}")
    add("clash", "Chữ không đè lên chữ (ước bề rộng theo font kiểu Arial)", [],
        clash[:15] + ([f"… và {len(clash) - 15} chỗ nữa"] if len(clash) > 15 else []),
        skip=None if boxes else "bản vẽ không có chữ")

    # Labels must also stay off furniture, fixtures and door swings: the
    # extents of each object on those layers (a door block's extents hold its swing).
    # A label must not cross an object's outline. Small closed shapes
    # (furniture, fixtures) and door blocks, whose extents hold the swing, also
    # count as solid; a large outline such as a light well or a glass floor
    # counts only by its edges, so a label may sit inside it.
    solid, edges = [], []
    for e in msp:
        if e.dxf.layer not in object_layers:
            continue
        box = bbox.extents([e])
        if not box.has_data:
            continue
        name = f"{e.dxftype()} trên {e.dxf.layer} tại ({box.center.x:.0f}, {box.center.y:.0f})"
        if e.dxftype() == "INSERT" or (e.dxftype() == "LWPOLYLINE" and e.closed
                                       and polygon_area([(x, y) for x, y, _ in e.get_points("xyb")]) <= SOLID_AREA):
            solid.append(((box.extmin.x, box.extmin.y, box.extmax.x, box.extmax.y), name))
        for a, b in segments(e):
            edges.append((a, b, name))
    labels = [(b, name) for b, name in boxes if not name.startswith("số kích thước")]
    hits = [f"{name} đè {thing}" for b, name in labels for tb, thing in solid if overlap(b, tb, gap=0)]
    hits += [f"{name} cắt cạnh của {thing}" for b, name in labels for a, c, thing in edges
             if segment_hits_box(a, c, b) and not any(thing == t for _, t in solid)]
    hits = list(dict.fromkeys(hits))
    things = solid + edges
    add("onobjects", "Chữ không đè đồ đạc, thiết bị và tầm quét cửa", [],
        hits[:15] + ([f"… và {len(hits) - 15} chỗ nữa"] if len(hits) > 15 else []),
        skip=None if things and boxes else "không có đồ đạc, thiết bị hay cửa trên các layer đã nêu")

    # Text must not sit on another dimension's lines or on an annotation line
    # such as a section cut: a number pushed out of a narrow gap often lands on
    # the next row.
    lines = []
    for k, e in enumerate(dims):
        for g in e.get_geometry_block() or []:
            if g.dxftype() == "LINE":
                lines.append(((g.dxf.start[0], g.dxf.start[1]), (g.dxf.end[0], g.dxf.end[1]), k))
    for e in msp:
        if e.dxf.layer == anno_layer and e.dxftype() in ("LINE", "LWPOLYLINE"):
            lines += [(a, b, None) for a, b in segments(e)]
    owner = {}
    for k, e in enumerate(dims):
        for t in e.get_geometry_block() or []:
            if t.dxftype() in ("TEXT", "MTEXT"):
                owner[f"số kích thước {text_of(t)!r} tại {at(t)}"] = k
    crossed = []
    for b, name in boxes:
        for a, c, k in lines:
            if k is not None and owner.get(name) == k:
                continue
            if segment_hits_box(a, c, shrink(b)):
                what = "đường cắt hoặc nét chú thích" if k is None else "nét của kích thước khác"
                crossed.append(f"{name} nằm trên {what}")
                break
    add("onlines", "Chữ không nằm trên nét kích thước khác hay đường cắt", [],
        crossed[:15] + ([f"… và {len(crossed) - 15} chỗ nữa"] if len(crossed) > 15 else []),
        skip=None if boxes and lines else "không có kích thước hay đường cắt")

    def outlines(layer):
        return [(e, [(x, y) for x, y, _ in e.get_points("xyb")]) for e in msp
                if e.dxftype() == "LWPOLYLINE" and e.dxf.layer == layer]

    walls = outlines(wall_layer)
    bad = [f"đường tại ({p[0][0]:.0f}, {p[0][1]:.0f}) không khép kín" for e, p in walls if not e.closed]
    bad += [f"đường tại ({p[0][0]:.0f}, {p[0][1]:.0f}) tự cắt" for e, p in walls
            if e.closed and self_crossing(p)]
    # A wall that meets itself at one corner (two masses touching at a column)
    # is read as self-intersecting by CADCraft and AutoCAD alike.
    bad += [f"đường tại ({p[0][0]:.0f}, {p[0][1]:.0f}) chạm chính nó tại một đỉnh" for e, p in walls
            if e.closed and self_touching(p)]
    add("walls", f"Tường trên {wall_layer} là hình khép kín, không tự cắt", bad,
        skip=None if walls else f"không có đường nào trên {wall_layer}")

    rooms = [(e, p) for e, p in outlines(area_layer) if e.closed]
    # A small room may carry its label outside, joined to it by a leader: a
    # straight line with one end inside the room and the other at the label.
    leaders = [(e.dxf.start, e.dxf.end) for e in msp if e.dxftype() == "LINE"
               and e.dxf.layer not in (wall_layer, area_layer)]
    area_texts = [(t, text_box(t)) for t in texts if AREA_RE.search(text_of(t))]

    def near(pt, box, reach):
        x0, y0, x1, y1 = box
        return x0 - reach <= pt[0] <= x1 + reach and y0 - reach <= pt[1] <= y1 + reach

    def led_to(pts):
        found = []
        for a, b in leaders:
            for inner, outer in ((a, b), (b, a)):
                if inside(inner, pts) and not inside(outer, pts):
                    found += [t for t, box in area_texts
                              if near(outer, box, (box[3] - box[1]) / 2)]
        return found

    bad, labelled = [], 0
    for _, pts in rooms:
        real = polygon_area(pts) / 1e6
        owned = [t for t in texts if inside(t.dxf.insert, pts)]
        if not any(AREA_RE.search(text_of(t)) for t in owned):
            owned = led_to(pts)
        labels = [AREA_RE.search(text_of(t)) for t in owned]
        labels = [float(m.group(1).replace(",", ".")) for m in labels if m]
        labelled += bool(labels)
        bad += [f"phòng tại ({pts[0][0]:.0f}, {pts[0][1]:.0f}): ghi {v:g} m², đo được {real:.2f} m²"
                for v in labels if abs(v - real) > AREA_TOL]
    warn = [f"{len(rooms) - labelled} phòng không có số diện tích nằm bên trong"] \
        if rooms and labelled < len(rooms) else []
    add("areas", f"Diện tích ghi trên hình khớp đường bao trên {area_layer}", bad, warn,
        skip=None if rooms else f"không có đường khép kín nào trên {area_layer}")

    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("file")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--area-layer", default="X-AREA")
    ap.add_argument("--wall-layer", default="A-WALL")
    ap.add_argument("--version", default="AC1032", help="AC1032 is DXF 2018")
    ap.add_argument("--object-layers", default="A-FURN,A-FLOR,A-DOOR",
                    help="layers whose objects labels must not cover, comma-separated")
    args = ap.parse_args()
    try:
        results = check(args.file, args.area_layer, args.wall_layer, args.version,
                        tuple(args.object_layers.split(",")))
    except (OSError, ezdxf.DXFError) as err:
        print(f"không đọc được {args.file}: {err}", file=sys.stderr)
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
