#!/usr/bin/env python3
"""params_check.py FILE [--json] — check a number table (params.json) against
the shared template `cad-params/1`, described in references/bang-so.md.

Standard library only. It checks the table on its own: shape, allowed values,
whole millimetres, every name that points somewhere, each opening inside its
wall, and clusters that never contain themselves. It draws nothing and reads
no DXF: whether the drawing matches the table is another checker's job.

Exit 0 = no error (warnings may remain), 1 = at least one error,
2 = the file could not be read as JSON.
"""
import argparse
import json
import math
import sys

SCHEMA = "cad-params/1"
PROJECT_TYPES = ("house", "apartment", "hotel", "apartment_building")
DEPTHS = ("construction", "scheme")
LEVEL_KINDS = ("basement", "ground", "typical", "roof")
PHASES = ("existing", "demolish", "new", "future")
ALIGNS = ("center", "left", "right")
OPENING_KINDS = ("door", "window", "shutter", "opening")
STAIR_KINDS = ("straight", "u_turn", "l_turn")
ROOM_USES = ("private", "shared", "wet", "service", "circulation", "outdoor")
SHAFT_KINDS = ("lift", "duct", "garbage", "other")
DIRS = ("+x", "-x", "+y", "-y")
ROTATIONS = (0, 90, 180, 270)
MIRRORS = ("none", "x", "y")
SOURCES = ("user", "model", "default")
LOOKS = DIRS
DRAWING_KINDS = ("plan", "section", "elevation", "site")
JAMB = 100  # mm of wall left on each side of an opening
# Keys whose numbers may carry decimals; every other number is whole mm.
DECIMAL_KEYS = {"need_area", "value", "north_deg"}
PLAN_LISTS = ("walls", "columns", "openings", "stairs", "rooms", "shafts",
              "voids", "parking", "furniture", "railings", "placements", "outside")
REQUIRED = ("schema", "project", "grid", "levels", "types", "floors", "drawings")
STRUCTURE_KEYS = ("slab", "beam", "parapet", "footing_depth", "footing_width", "stair_waist",
                  "rail_height")
NEEDS_SITE = ("house", "hotel", "apartment_building")


class Report:
    def __init__(self):
        self.errors, self.warnings = [], []

    def err(self, path, msg):
        self.errors.append({"path": path, "msg": msg})

    def warn(self, path, msg):
        self.warnings.append({"path": path, "msg": msg})


def is_int(v):
    return isinstance(v, int) and not isinstance(v, bool)


def is_num(v):
    return (isinstance(v, (int, float)) and not isinstance(v, bool)
            and math.isfinite(v))


# ---- stage 1: shape and allowed values -------------------------------------

def check_numbers(node, path, rep, key=None):
    """Every number is whole mm unless its key is one of DECIMAL_KEYS."""
    if isinstance(node, dict):
        for k, v in node.items():
            check_numbers(v, f"{path}.{k}" if path else k, rep, k)
    elif isinstance(node, list):
        for i, v in enumerate(node):
            check_numbers(v, f"{path}[{i}]", rep, key)
    elif isinstance(node, float) and key not in DECIMAL_KEYS:
        rep.err(path, f"số {node} không phải milimét nguyên")


def need(obj, key, path, rep, kind=None):
    if not isinstance(obj, dict) or key not in obj:
        rep.err(f"{path}.{key}", "thiếu trường bắt buộc")
        return None
    v = obj[key]
    if kind == "int" and not is_int(v):
        if not isinstance(v, float):  # a decimal is already named by check_numbers
            rep.err(f"{path}.{key}", f"phải là số nguyên, đang là {v!r}")
        return None
    if kind in ("pos", "nonneg"):
        if not is_int(v):
            if not isinstance(v, float):
                rep.err(f"{path}.{key}", f"phải là số nguyên, đang là {v!r}")
            return None
        if v < (1 if kind == "pos" else 0):
            rep.err(f"{path}.{key}", f"phải {'lớn hơn 0' if kind == 'pos' else 'không âm'}, đang là {v}")
            return None
    if kind == "str" and not (isinstance(v, str) and v):
        rep.err(f"{path}.{key}", f"phải là chữ, đang là {v!r}")
        return None
    if kind == "dict" and not isinstance(v, dict):
        rep.err(f"{path}.{key}", "phải là một bảng")
        return None
    if kind == "list" and not isinstance(v, list):
        rep.err(f"{path}.{key}", "phải là một danh sách")
        return None
    return v


def one_of(obj, key, allowed, path, rep, required=True, default=None):
    if not isinstance(obj, dict) or key not in obj:
        if required:
            rep.err(f"{path}.{key}", "thiếu trường bắt buộc")
        return default
    v = obj[key]
    if isinstance(v, bool) or v not in allowed:
        rep.err(f"{path}.{key}", f"giá trị {v!r} không thuộc {', '.join(map(str, allowed))}")
        return None
    return v


def tables(obj, key, path, rep):
    """The items of an optional list of tables, as (index, item); a wrong
    type becomes an error line instead of a crash."""
    items = obj.get(key, []) if isinstance(obj, dict) else []
    where = f"{path}.{key}" if path else key
    if not isinstance(items, list):
        rep.err(where, "phải là một danh sách")
        return []
    out = []
    for i, o in enumerate(items):
        if isinstance(o, dict):
            out.append((i, o))
        else:
            rep.err(f"{where}[{i}]", "phải là một bảng")
    return out


def check_point_shape(p, path, rep):
    ok = (isinstance(p, list) and len(p) == 2 and all(
        isinstance(a, list) and len(a) >= 1 and isinstance(a[0], str)
        and all(is_num(o) for o in a[1:]) for a in p))
    if not ok:
        rep.err(path, "điểm phải viết [[trục x, lệch…], [trục y, lệch…]]")
    return ok


def check_provenance(obj, path, rep):
    if isinstance(obj, dict):
        if "by" in obj and obj["by"] not in SOURCES:
            rep.err(f"{path}.by", f"giá trị {obj['by']!r} không thuộc {', '.join(SOURCES)}")
        if "pending" in obj and not isinstance(obj["pending"], bool):
            rep.err(f"{path}.pending", "phải là true hoặc false")


def check_plan_shape(block, path, rep, is_cluster=False):
    """A floor or a cluster: lists of objects, each with an id and a phase."""
    if not isinstance(block, dict):
        rep.err(path, "phải là một bảng")
        return
    allowed = set(PLAN_LISTS) | ({"grid"} if is_cluster else set()) | {"note"}
    for k in block:
        if k not in allowed:
            rep.err(f"{path}.{k}", "phần không có trong khuôn")
    for name in PLAN_LISTS:
        items = block.get(name, [])
        if not isinstance(items, list):
            rep.err(f"{path}.{name}", "phải là một danh sách")
            continue
        for i, o in enumerate(items):
            p = f"{path}.{name}[{i}]"
            if not isinstance(o, dict):
                rep.err(p, "phải là một bảng")
                continue
            check_provenance(o, p, rep)
            if name == "placements":
                if "id" in o:
                    need(o, "id", p, rep, "str")
                need(o, "cluster", p, rep, "str")
                if "at" in o:
                    check_point_shape(o["at"], f"{p}.at", rep)
                else:
                    rep.err(f"{p}.at", "thiếu trường bắt buộc")
                one_of(o, "rotate", ROTATIONS, p, rep, required=False)
                one_of(o, "mirror", MIRRORS, p, rep, required=False)
                continue
            need(o, "id", p, rep, "str")
            one_of(o, "phase", PHASES, p, rep, required=False)
            for key in ("from", "to", "at", "start", "near"):
                if key in o:
                    check_point_shape(o[key], f"{p}.{key}", rep)
            if name == "walls":
                for key in ("from", "to"):
                    if key not in o:
                        rep.err(f"{p}.{key}", "thiếu trường bắt buộc")
                need(o, "type", p, rep, "str")
                one_of(o, "align", ALIGNS, p, rep, required=False)
            elif name == "columns":
                need(o, "type", p, rep, "str")
                if "at" not in o:
                    rep.err(f"{p}.at", "thiếu trường bắt buộc")
            elif name == "openings":
                need(o, "wall", p, rep, "str")
                need(o, "type", p, rep, "str")
                need(o, "offset", p, rep, "int")
                one_of(o, "hinge", ("start", "end"), p, rep, required=False)
                one_of(o, "swing", ("left", "right"), p, rep, required=False)
            elif name == "stairs":
                need(o, "type", p, rep, "str")
                if "start" not in o:
                    rep.err(f"{p}.start", "thiếu trường bắt buộc")
                one_of(o, "dir", DIRS, p, rep)
                one_of(o, "turn", ("left", "right"), p, rep, required=False)
                need(o, "up_to", p, rep, "str")
            elif name == "rooms":
                need(o, "name", p, rep, "str")
                if "at" not in o:
                    rep.err(f"{p}.at", "thiếu trường bắt buộc")
                one_of(o, "use", ROOM_USES, p, rep)
                if "need_area" in o and not (is_num(o["need_area"]) and o["need_area"] > 0):
                    rep.err(f"{p}.need_area", "phải là số m² dương")
            elif name in ("shafts", "voids", "parking"):
                for key in ("from", "to"):
                    if key not in o:
                        rep.err(f"{p}.{key}", "thiếu trường bắt buộc")
                if name == "shafts":
                    one_of(o, "kind", SHAFT_KINDS, p, rep)
                if name == "voids":
                    one_of(o, "floor", ("none", "glass"), p, rep, required=False)
                if name == "parking":
                    one_of(o, "vehicle", ("car", "motorbike"), p, rep)
                    need(o, "count", p, rep, "int")
            elif name == "furniture":
                need(o, "block", p, rep, "str")
                if "at" not in o:
                    rep.err(f"{p}.at", "thiếu trường bắt buộc")
                one_of(o, "rotate", ROTATIONS, p, rep, required=False)
            elif name == "railings":
                pts = need(o, "points", p, rep, "list")
                if pts is not None:
                    if len(pts) < 2:
                        rep.err(f"{p}.points", "cần ít nhất hai điểm")
                    for j, q in enumerate(pts):
                        check_point_shape(q, f"{p}.points[{j}]", rep)
            elif name == "outside":
                need(o, "what", p, rep, "str")
                if "near" not in o:
                    rep.err(f"{p}.near", "thiếu trường bắt buộc")


def check_grid_shape(grid, path, rep):
    if not isinstance(grid, dict):
        rep.err(path, "phải là một bảng")
        return
    for axis in ("x", "y"):
        g = grid.get(axis)
        if not isinstance(g, dict) or not g:
            rep.err(f"{path}.{axis}", "cần ít nhất một trục")
            continue
        for name, v in g.items():
            if not is_num(v):
                rep.err(f"{path}.{axis}.{name}", "tọa độ trục phải là số")


def stage_shape(d, rep):
    if not isinstance(d, dict):
        rep.err("", "bảng số phải là một bảng JSON")
        return
    if d.get("schema") != SCHEMA:
        rep.err("schema", f"khuôn {d.get('schema')!r} không phải {SCHEMA!r}")
        return
    missing = [k for k in REQUIRED if k not in d]
    for k in missing:
        rep.err(k, "thiếu phần bắt buộc")
    if missing:
        return
    check_numbers(d, "", rep)

    proj = need(d, "project", "", rep, "dict") or {}
    one_of(proj, "type", PROJECT_TYPES, "project", rep)
    one_of(proj, "depth", DEPTHS, "project", rep)
    need(proj, "scale", "project", rep, "pos")
    if proj.get("type") in NEEDS_SITE and "site" not in d:
        rep.err("site", f"loại công trình {proj['type']} cần phần khu đất")

    site = d.get("site")
    if site is not None:
        if not isinstance(site, dict):
            rep.err("site", "phải là một bảng")
        else:
            if "outline" in site:
                ol = site["outline"]
                if not (isinstance(ol, list) and len(ol) >= 3 and all(
                        isinstance(q, list) and len(q) == 2 and all(is_num(c) for c in q)
                        for q in ol)):
                    rep.err("site.outline", "ranh đất là danh sách ít nhất ba điểm [x, y]")
            elif "from_dxf" not in site:
                rep.err("site", "cần outline hoặc from_dxf")
            ol = site.get("outline")
            n_edges = len(ol) if isinstance(ol, list) else None
            setbacks = tables(site, "setbacks", "site", rep)
            edge_refs = [(f"site.setbacks[{i}]", s, "edge") for i, s in setbacks]
            if "front_edge" in site:
                edge_refs.append(("site", site, "front_edge"))
            for p, obj, key in edge_refs:
                e = need(obj, key, p, rep, "nonneg")
                if e is not None and n_edges is not None and e >= n_edges:
                    rep.err(f"{p}.{key}", f"ranh đất chỉ có cạnh 0 tới {n_edges - 1}")
            for i, s in setbacks:
                need(s, "mm", f"site.setbacks[{i}]", rep, "nonneg")
                check_provenance(s, f"site.setbacks[{i}]", rep)
            if "north_deg" in site and not is_num(site["north_deg"]):
                rep.err("site.north_deg", "phải là số độ")
            for i, lim in tables(site, "limits", "site", rep):
                need(lim, "name", f"site.limits[{i}]", rep, "str")
                if not is_num(lim.get("value")):
                    rep.err(f"site.limits[{i}].value", "phải là số")
                check_provenance(lim, f"site.limits[{i}]", rep)

    check_grid_shape(d["grid"], "grid", rep)

    levels = need(d, "levels", "", rep, "list") or []
    if not levels:
        rep.err("levels", "cần ít nhất một tầng")
    for i, lv in (tables(d, "levels", "", rep) if isinstance(d["levels"], list) else []):
        p = f"levels[{i}]"
        need(lv, "name", p, rep, "str")
        need(lv, "elevation", p, rep, "int")
        need(lv, "height", p, rep, "nonneg")
        one_of(lv, "kind", LEVEL_KINDS, p, rep)

    types = need(d, "types", "", rep, "dict") or {}
    for group in ("walls", "openings", "stairs", "columns"):
        table = types.get(group, {})
        if not isinstance(table, dict):
            rep.err(f"types.{group}", "phải là một bảng")
            continue
        for name, t in table.items():
            p = f"types.{group}.{name}"
            if not isinstance(t, dict):
                rep.err(p, "phải là một bảng")
                continue
            check_provenance(t, p, rep)
            if group == "walls":
                th = need(t, "thickness", p, rep, "int")
                if th is not None and th < 0:
                    rep.err(f"{p}.thickness", "bề dày không âm")
            elif group == "openings":
                kind = one_of(t, "kind", OPENING_KINDS, p, rep)
                need(t, "width", p, rep, "pos")
                if proj.get("depth") == "construction":
                    need(t, "height", p, rep, "pos")
                    if kind == "window":
                        need(t, "sill", p, rep, "nonneg")
            elif group == "stairs":
                one_of(t, "kind", STAIR_KINDS, p, rep)
                need(t, "flight_width", p, rep, "pos")
                need(t, "tread", p, rep, "pos")
            elif group == "columns":
                size = need(t, "size", p, rep, "list")
                if size is not None and not (len(size) == 2 and all(is_int(s) and s > 0 for s in size)):
                    rep.err(f"{p}.size", "cỡ cột là [rộng, sâu]")

    floors = need(d, "floors", "", rep, "dict") or {}
    for name, block in floors.items():
        check_plan_shape(block, f"floors.{name}", rep)
    clusters = d.get("clusters", {})
    if not isinstance(clusters, dict):
        rep.err("clusters", "phải là một bảng")
        clusters = {}
    for name, block in clusters.items():
        if not isinstance(block, dict) or "grid" not in block:
            rep.err(f"clusters.{name}.grid", "cụm cần lưới riêng")
            continue
        check_grid_shape(block["grid"], f"clusters.{name}.grid", rep)
        check_plan_shape(block, f"clusters.{name}", rep, is_cluster=True)
    for i, pl in tables(d, "placements", "", rep):
        p = f"placements[{i}]"
        need(pl, "cluster", p, rep, "str")
        if "at" in pl:
            check_point_shape(pl["at"], f"{p}.at", rep)
        else:
            rep.err(f"{p}.at", "thiếu trường bắt buộc")
        need(pl, "levels", p, rep, "list")
        one_of(pl, "rotate", ROTATIONS, p, rep, required=False)
        one_of(pl, "mirror", MIRRORS, p, rep, required=False)

    for i, sec in tables(d, "sections", "", rep):
        p = f"sections[{i}]"
        need(sec, "name", p, rep, "str")
        one_of(sec, "look", LOOKS, p, rep)
        path_pts = need(sec, "path", p, rep, "list") or []
        if len(path_pts) < 2:
            rep.err(f"{p}.path", "đường cắt cần ít nhất hai điểm")
        for j, q in enumerate(path_pts):
            check_point_shape(q, f"{p}.path[{j}]", rep)

    seen_ids = set()
    for i, dr in tables(d, "drawings", "", rep):
        p = f"drawings[{i}]"
        did = need(dr, "id", p, rep, "str")
        if did in seen_ids:
            rep.err(f"{p}.id", f"hình {did!r} trùng")
        seen_ids.add(did)
        kind = did.partition(":")[0] if did else None
        if did and kind not in DRAWING_KINDS:
            rep.err(f"{p}.id", f"loại hình {kind!r} không thuộc {', '.join(DRAWING_KINDS)}")
        elif kind == "site" and "site" not in d:
            rep.err(f"{p}.id", "hình khu đất cần phần site")
        elif kind == "elevation" and did.partition(":")[2] not in DIRS:
            rep.err(f"{p}.id", f"mặt đứng ghi theo hướng nhìn: elevation:{'|'.join(DIRS)}")
        org = need(dr, "origin", p, rep, "list")
        if org is not None and not (len(org) == 2 and all(is_num(c) for c in org)):
            rep.err(f"{p}.origin", "gốc hình là [x, y]")

    structure = d.get("structure", {})
    if not isinstance(structure, dict):
        rep.err("structure", "phải là một bảng")
        structure = {}
    for key, entry in structure.items():
        p = f"structure.{key}"
        if key not in STRUCTURE_KEYS:
            rep.err(p, f"không thuộc {', '.join(STRUCTURE_KEYS)}")
            continue
        if not isinstance(entry, dict) or "value" not in entry:
            rep.err(p, "viết {\"value\": số, \"by\": …}")
            continue
        check_provenance(entry, p, rep)
        v = entry["value"]
        pair = key == "beam"
        ok = (isinstance(v, list) and len(v) == 2 and all(is_int(x) and x > 0 for x in v)) if pair \
            else (is_int(v) and v > 0)
        if not ok:
            rep.err(f"{p}.value", "[rộng, cao] milimét dương" if pair else "milimét dương")

    rules = d.get("rules", [])
    if not (isinstance(rules, list) and all(isinstance(r, str) for r in rules)):
        rep.err("rules", "là danh sách mã dòng luật")


# ---- stage 2: names that point somewhere, fit, clusters --------------------

def resolve(p, grid):
    """A point [[xname, offs…], [yname, offs…]] -> (x, y), or None."""
    out = []
    for axis, ref in zip(("x", "y"), p):
        base = grid[axis].get(ref[0])
        if base is None:
            return None
        out.append(base + sum(ref[1:]))
    return tuple(out)


def check_point_names(p, grid, path, rep):
    ok = True
    for axis, ref in zip(("x", "y"), p):
        if ref[0] not in grid[axis]:
            rep.err(path, f"không có trục {ref[0]!r} theo phương {axis}")
            ok = False
    return ok


def check_plan_refs(block, grid, path, d, rep, level_names):
    types = d["types"]
    clusters = d.get("clusters", {})
    seen = {}
    for name in PLAN_LISTS:
        for i, o in enumerate(block.get(name, [])):
            p = f"{path}.{name}[{i}]"
            oid = o.get("id")
            if oid is not None:
                if oid in seen:
                    rep.err(f"{p}.id", f"id {oid!r} trùng với {seen[oid]}")
                else:
                    seen[oid] = p
            for key in ("from", "to", "at", "start", "near"):
                if key in o:
                    check_point_names(o[key], grid, f"{p}.{key}", rep)
            for j, q in enumerate(o.get("points", []) if name == "railings" else []):
                check_point_names(q, grid, f"{p}.points[{j}]", rep)
            group = {"walls": "walls", "openings": "openings", "stairs": "stairs",
                     "columns": "columns"}.get(name)
            if group and o.get("type") not in types.get(group, {}):
                rep.err(f"{p}.type", f"không có loại {o.get('type')!r} trong types.{group}")
            if name == "stairs" and o.get("up_to") not in level_names + ["next"]:
                rep.err(f"{p}.up_to", f"không có tầng {o.get('up_to')!r}")
            if name == "placements" and o.get("cluster") not in clusters:
                rep.err(f"{p}.cluster", f"không có cụm {o.get('cluster')!r}")

    for i, w in enumerate(block.get("walls", [])):
        a, b = resolve(w["from"], grid), resolve(w["to"], grid)
        if a is not None and a == b:
            rep.err(f"{path}.walls[{i}]", "tường dài 0: from trùng to")
    walls = {w["id"]: w for w in block.get("walls", [])}
    for i, o in enumerate(block.get("openings", [])):
        p = f"{path}.openings[{i}]"
        w = walls.get(o.get("wall"))
        if w is None:
            rep.err(f"{p}.wall", f"không có tường {o.get('wall')!r} ở {path}")
            continue
        t = types.get("openings", {}).get(o.get("type"))
        a, b = resolve(w["from"], grid), resolve(w["to"], grid)
        if t is None or a is None or b is None:
            continue  # already reported above
        length = math.hypot(b[0] - a[0], b[1] - a[1])
        lo, hi = o["offset"], o["offset"] + t["width"]
        if lo < JAMB or hi > length - JAMB:
            rep.err(f"{p}.offset", f"ô cửa từ {lo} tới {hi} không lọt tường dài "
                    f"{length:.0f} với má {JAMB} mỗi bên")


def stage_refs(d, rep):
    grid = d["grid"]
    level_names = [lv["name"] for lv in d["levels"]]
    seen = set()
    for i, n in enumerate(level_names):
        if n in seen:
            rep.err(f"levels[{i}].name", f"tầng {n!r} trùng tên")
        seen.add(n)
    for i in range(1, len(d["levels"])):
        lo, hi = d["levels"][i - 1], d["levels"][i]
        if lo["elevation"] + lo["height"] != hi["elevation"]:
            rep.err(f"levels[{i}].elevation",
                    f"tầng {hi['name']} ở {hi['elevation']}, mà tầng dưới tới "
                    f"{lo['elevation'] + lo['height']}")
    for name, block in d["floors"].items():
        if name not in level_names:
            rep.err(f"floors.{name}", f"không có tầng {name!r} trong levels")
            continue
        check_plan_refs(block, grid, f"floors.{name}", d, rep, level_names)
    clusters = d.get("clusters", {})
    for name, block in clusters.items():
        check_plan_refs(block, block["grid"], f"clusters.{name}", d, rep, level_names)
    for i, pl in enumerate(d.get("placements", [])):
        p = f"placements[{i}]"
        if pl.get("cluster") not in clusters:
            rep.err(f"{p}.cluster", f"không có cụm {pl.get('cluster')!r}")
        check_point_names(pl["at"], grid, f"{p}.at", rep)
        for j, lv in enumerate(pl.get("levels", [])):
            if lv not in level_names:
                rep.err(f"{p}.levels[{j}]", f"không có tầng {lv!r}")

    # A cluster never contains itself, directly or through another cluster.
    edges = {n: {pl.get("cluster") for pl in b.get("placements", [])}
             for n, b in clusters.items()}
    reported = set()
    for start in clusters:
        stack, trail = [(start, [start])], set()
        while stack:
            node, chain = stack.pop()
            for nxt in edges.get(node, ()):
                if nxt == start:
                    loop = frozenset(chain)
                    if loop not in reported:
                        reported.add(loop)
                        rep.err(f"clusters.{start}.placements",
                                "cụm tự chứa chính nó: " + " → ".join(chain + [start]))
                elif nxt in edges and nxt not in trail:
                    trail.add(nxt)
                    stack.append((nxt, chain + [nxt]))

    section_names = set()
    for i, sec in enumerate(d.get("sections", [])):
        if sec["name"] in section_names:
            rep.err(f"sections[{i}].name", f"mặt cắt {sec['name']!r} trùng tên")
        section_names.add(sec["name"])
    for i, dr in enumerate(d["drawings"]):
        kind, _, ref = dr["id"].partition(":")
        if kind == "plan" and ref not in level_names:
            rep.err(f"drawings[{i}].id", f"không có tầng {ref!r}")
        if kind == "section" and ref not in section_names:
            rep.err(f"drawings[{i}].id", f"không có mặt cắt {ref!r} trong sections")
    for i, sec in enumerate(d.get("sections", [])):
        for j, q in enumerate(sec.get("path", [])):
            check_point_names(q, grid, f"sections[{i}].path[{j}]", rep)

    # Warning: what the drawing will hand back to the user.
    for where, block in list(d["floors"].items()) + [(f"clusters.{n}", b) for n, b in clusters.items()]:
        prefix = where if where.startswith("clusters.") else f"floors.{where}"
        for i, o in enumerate(block.get("outside", [])):
            rep.warn(f"{prefix}.outside[{i}]", f"ngoài khuôn, sẽ giao lại: {o.get('what')}")


def load(path):
    """Read JSON, keeping a list of keys written twice in one table: plain
    json.load would silently keep only the last one."""
    dups = []

    def pairs(items):
        out = {}
        for k, v in items:
            if k in out:
                dups.append(k)
            out[k] = v
        return out

    with open(path, encoding="utf-8") as f:
        return json.load(f, object_pairs_hook=pairs), dups


def check(d, dup_keys=()):
    rep = Report()
    for k in dup_keys:
        rep.err(k, "khoá viết hai lần trong một bảng; JSON chỉ giữ lần sau")
    stage_shape(d, rep)
    if not rep.errors:
        stage_refs(d, rep)
    return rep


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("file")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)
    try:
        d, dups = load(args.file)
    except (OSError, ValueError) as e:
        print(f"không đọc được {args.file}: {e}", file=sys.stderr)
        return 2
    rep = check(d, dups)
    if args.json:
        print(json.dumps({"errors": rep.errors, "warnings": rep.warnings},
                         ensure_ascii=False, indent=1))
    else:
        for e in rep.errors:
            print(f"LỖI   {e['path']}: {e['msg']}")
        for w in rep.warnings:
            print(f"XEM   {w['path']}: {w['msg']}")
        print(f"{len(rep.errors)} lỗi, {len(rep.warnings)} cần xem")
    return 1 if rep.errors else 0


if __name__ == "__main__":
    sys.exit(main())
