#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# dependencies = ["ezdxf>=1.3"]
# ///
"""luat_check.py DXF PARAMS [--rules FILE] [--json] — check a drawing and its
number table against the law, reading every threshold from a rules table
(assets/luat/vn.json by default): when the law changes, the table changes,
not this code. Every result names the rule rows it used.

A check fails only when its rule row was read in the original text
(certainty "goc"), is in force on the table's submission date, and every
input it needs (fire-resistance grade, fire-safety height, people per floor…,
from `law_inputs`) is given. Otherwise it asks for a look: missing inputs,
weaker certainty, texts that disagree, a result just under a limit, or a
limit each city sets for itself.

It reads the file and the table the way plan_check.py does (same unrolling,
same room outlines), never through the drawing library.
Exit 0 = nothing failed, 1 = something failed or the table is not valid,
2 = a file could not be read.
"""
import argparse
import datetime
import heapq
import json
import math
import pathlib
import sys

import ezdxf

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.dont_write_bytecode = True
import params_check  # noqa: E402
from dxf_check import inside, polygon_area  # noqa: E402
from plan_check import closed_outlines, flatten, footprint_sum, wall_poly  # noqa: E402

RULES = HERE.parent / "assets" / "luat" / "vn.json"
ROW_KEYS = ("id", "what", "check", "value", "unit", "applies", "doc", "clause", "effective_from", "read_on",
            "certainty", "source")
CERTAINTY = ("goc", "thuat_lai", "cach_hieu", "dia_phuong")
NEAR = 0.10  # a travel distance within 10 % under its limit asks for a look


def interp(points, x):
    """Linear interpolation over [[x, y], …] sorted by x, clamped at both ends."""
    if x <= points[0][0]:
        return points[0][1]
    for (x0, y0), (x1, y1) in zip(points, points[1:]):
        if x <= x1:
            return y0 + (y1 - y0) * (x - x0) / (x1 - x0)
    return points[-1][1]


def table2(rule, height, plot):
    v = rule["value"]
    rows = [interp(list(zip(v["plots_m2"], row)), plot) for row in v["table"]]
    hs = v["heights_mm"]
    return interp(list(zip(hs, rows)), height)


def rules_errors(rules):
    """What makes a rules table unusable, as lines; empty when it is sound."""
    if not isinstance(rules, dict) or not isinstance(rules.get("rules"), list):
        return ["không có danh sách \"rules\""]
    errs = []
    for i, r in enumerate(rules["rules"]):
        if not isinstance(r, dict):
            errs.append(f"dòng {i}: không phải một object")
            continue
        rid = r.get("id", f"dòng {i}")
        errs += [f"{rid}: thiếu {k}" for k in ROW_KEYS if k not in r]
        if "certainty" in r and r["certainty"] not in CERTAINTY:
            errs.append(f"{rid}: mức chắc {r['certainty']!r} không thuộc {', '.join(CERTAINTY)}")
        if not isinstance(r.get("applies"), dict) or not isinstance(r["applies"].get("types"), list):
            errs.append(f"{rid}: applies.types phải là một danh sách")
        if r.get("condition") is not None and not isinstance(r["condition"], dict):
            errs.append(f"{rid}: condition phải là object hay null")
    return errs


class Law:
    def __init__(self, rules, d):
        self.d = d
        self.kind = d["project"]["type"]
        self.inputs = {k: e["value"] for k, e in d.get("law_inputs", {}).items()}
        self.date = self.inputs.get("submit_date", datetime.date.today().isoformat())
        self.soft = {}  # row id -> why a breach of that row is only a look
        lv = d["levels"]
        storeys = len([x for x in lv if x["kind"] not in ("roof", "basement")])
        basements = len([x for x in lv if x["kind"] == "basement"])
        ppl = self.inputs.get("people_per_floor")
        self.rows = []
        for r in rules["rules"]:
            a = r["applies"]
            if self.kind not in a.get("types", []) or r["effective_from"] > self.date \
                    or (r.get("effective_to") and self.date > r["effective_to"]):
                continue
            if "people_per_floor_over" in a and not (ppl is not None and ppl > a["people_per_floor_over"]):
                continue
            scope = a.get("house_in_scope_if_any")
            if self.kind == "house" and scope:
                fh, vol = self.inputs.get("fire_height_mm"), self.inputs.get("volume_m3")
                if not (storeys >= scope["storeys_min"] or basements >= scope["basements_min"]
                        or (fh is not None and fh >= scope["fire_height_min_mm"])
                        or (vol is not None and vol >= scope["volume_min_m3"])):
                    self.soft[r["id"]] = (
                        "nhà riêng lẻ nhỏ theo TCVN 13967:2024 (chưa đọc), số của QCVN 06 chỉ để tham khảo"
                        if fh is not None and vol is not None else
                        "nhà riêng lẻ chỉ theo QCVN 06 khi ≥ 7 tầng, cao PCCC ≥ 25 m, ≥ 5.000 m³ hay > 1 hầm: "
                        "thiếu chiều cao PCCC hay khối tích (volume_m3)")
            self.rows.append(r)

    def rows_for(self, check):
        return [r for r in self.rows if r.get("check") == check]

    def firm(self, rule, needs=()):
        """Whether a breach of this rule may be reported as a failure."""
        return (rule["certainty"] == "goc" and rule["id"] not in self.soft
                and all(k in self.inputs for k in needs))

    def put(self, rule, bad, warn, msg, needs=()):
        """File a breach as a failure when the rule is firm, else as a look, saying why."""
        if self.firm(rule, needs):
            bad.append(msg)
        else:
            why = self.soft.get(rule["id"])
            warn.append(msg + (f"; {why}" if why else ""))


def travel_limits(law):
    """The travel limits [between two stairs, dead end] a plan is held to, and
    whether a breach may fail. None when no travel rule applies."""
    rows = law.rows_for("travel_max")
    if not rows:
        return None
    rule = rows[0]
    fh = law.inputs.get("fire_height_mm")
    tall = law.rows_for("travel_max_tall")
    if tall and fh is not None and fh > tall[0]["applies"]["fire_height_min_mm"].get(law.kind, math.inf):
        # A very tall building has its own limits; the hotel table no longer applies.
        return {"limits": tall[0]["value"], "rule": tall[0], "needs": ("fire_height_mm",),
                "alt": None, "alt_dead_end": None, "note": None}
    grade, sclass = law.inputs.get("fire_resistance"), law.inputs.get("s_class")
    key = "V" if grade == "V" else f"{grade}-{sclass}"
    limits, note = rule["value"].get(key), None
    if limits is None:
        limits = [min(v[i] for v in rule["value"].values()) for i in (0, 1)]
        note = ("thiếu bậc chịu lửa hay cấp S trong law_inputs" if grade is None or sclass is None and grade != "V"
                else f"cặp {key} không có trong bảng") + \
            f": tạm so với mức chặt nhất {limits[0] / 1000:.0f} và {limits[1] / 1000:.0f} m"
    alt = law.rows_for("travel_max_alt")
    alt = alt[0] if alt and key in alt[0]["value"] else None
    return {"limits": limits, "rule": rule, "needs": ("fire_resistance", "s_class"), "alt": alt,
            "alt_dead_end": alt["value"][key][1] if alt else None, "note": note}


def lifts_needed(v, storeys, units, people):
    """Lifts a block needs by flats, and by people when the count is known (else None)."""
    base = max([c for s_, c in v["from_storeys"] if storeys >= s_] or [0])
    if not base:
        return 0, 0
    by_units = max(base, math.ceil(units / v["per_units"]))
    by_people = max(base, math.ceil(people / v["per_people"])) if people is not None and v.get("per_people") else None
    return by_units, by_people


def hotel_one_exit(ex, inputs, floor_m2):
    """Whether 3.2.6.2 a lets a hotel floor have one exit: "ok", a line saying
    what still has to be true, or None when it does not."""
    grade, fh, ppl = inputs.get("fire_resistance"), inputs.get("fire_height_mm"), inputs.get("people_per_floor")
    if grade in ex["not_for_fire_resistance"]:
        return None
    if grade is None or fh is None or ppl is None:
        return (f"khách sạn có thể được một lối theo {ex['clause']}: thiếu bậc chịu lửa, chiều cao PCCC "
                f"hay số người mỗi tầng")
    for hmax, amax, pmax, also in ex["rows"]:
        if fh <= hmax:
            if floor_m2 <= amax and ppl <= pmax:
                return "ok" if not also else f"được một lối theo {ex['clause']} nếu có {also}"
            return None
    return None


def tag(rule):
    return f"[{rule['id']}: {rule['doc'].split(';')[0]}, {rule['clause']}]"


def check(dxf_path, d, rules):
    law = Law(rules, d)
    doc = ezdxf.readfile(dxf_path)
    msp = doc.modelspace()
    flat = flatten(d)
    levels = d["levels"]
    names = [lv["name"] for lv in levels]
    elev = {lv["name"]: lv["elevation"] for lv in levels}
    kinds = {lv["name"]: lv["kind"] for lv in levels}
    origins = {dr["id"][5:]: tuple(dr["origin"]) for dr in d["drawings"] if dr["id"].startswith("plan:")}
    plans = [n for n in names if n in origins]
    clusters = d.get("clusters", {})
    out = []

    def add(key, title, bad, warn=(), skip=None):
        status = "skip" if skip else "fail" if bad else "warn" if warn else "pass"
        out.append({"id": key, "title": title, "status": status,
                    "details": [skip] if skip else list(bad) + list(warn)})

    # Room outlines, as plan_check reads them: the smallest X-AREA outline holding the room point.
    outlines = closed_outlines(msp, "X-AREA")
    room_poly = {}
    for n in plans:
        ox, oy = origins[n]
        for r in flat[n]["rooms"]:
            p = (r["at"][0] + ox, r["at"][1] + oy)
            hits = [o for o in outlines if inside(p, o)]
            if hits:
                room_poly[(n, r["id"])] = [(x - ox, y - oy) for x, y in min(hits, key=polygon_area)]

    def area(n, r):
        poly = room_poly.get((n, r["id"]))
        return polygon_area(poly) / 1e6 if poly else None

    def unit_of(rid):
        """The id prefix of the flat (or hotel room) a room belongs to, or None."""
        parts = rid.split("/")[:-1]
        for k in range(len(parts), 0, -1):
            name = parts[k - 1].split("#")[0]
            if clusters.get(name, {}).get("kind") in ("unit", "room"):
                return "/".join(parts[:k])
        return None

    # 1. Flat and bedroom areas.
    for check_key, title in (("unit_area_min", "Diện tích căn hộ tối thiểu"),
                             ("bedroom_area_min", "Diện tích phòng ngủ tối thiểu")):
        rows = law.rows_for(check_key)
        if not rows:
            continue
        rule = rows[0]
        bad, warn = [], []
        for n in plans:
            if check_key == "unit_area_min":
                units = {}
                for r in flat[n]["rooms"]:
                    u = unit_of(r["id"])
                    if u and clusters[u.split("/")[-1].split("#")[0]].get("kind") == "unit":
                        units.setdefault(u, []).append(r)
                items = []
                for u, rs in units.items():
                    areas = [area(n, r) for r in rs]
                    if None in areas:
                        warn.append(f"{n} {u}: {areas.count(None)} phòng không có đường bao trên X-AREA, "
                                    f"chưa cộng được diện tích căn {tag(rule)}")
                    else:
                        items.append((u, sum(areas)))
            else:
                items = [(r["id"], area(n, r)) for r in flat[n]["rooms"]
                         if r["use"] == "private" and (unit_of(r["id"]) or law.kind == "apartment")]
            for name, a in items:
                if a is None:
                    continue
                if a < rule["value"]:
                    law.put(rule, bad, warn, f"{n} {name}: {a:.2f} m² dưới {rule['value']} m² {tag(rule)}")
        if not bad and not warn and not any(True for n in plans for _ in flat[n]["rooms"]):
            add(check_key, title, [], skip="không có phòng")
        else:
            add(check_key, title, bad, warn)

    # 2. Stairs: flight width, tread, riser.
    stairs = [(n, s) for n in names for s in flat[n]["stairs"]]
    ppl = law.inputs.get("people_per_floor")
    fh = law.inputs.get("fire_height_mm")
    bad, warn = [], []
    missing_risers = {}
    width_rows = law.rows_for("stair_width_min")
    small = [r for r in width_rows if "fire_height_max_mm" in r["applies"]]
    crowd = [r for r in width_rows if "people_per_floor_over" in r["applies"]]
    normal = [r for r in width_rows if r not in small and r not in crowd]
    for n, s in stairs:
        t = d["types"]["stairs"][s["type"]]
        rule = None
        if crowd:
            rule = crowd[0]
        elif small and fh is not None and ppl is not None and fh <= small[0]["applies"]["fire_height_max_mm"] \
                and ppl <= small[0]["applies"]["people_per_floor_max"]:
            rule = small[0]
        elif normal:
            rule = normal[0]
        if rule and t["flight_width"] < rule["value"]:
            msg = f"{n} {s['id']}: bản thang {t['flight_width']} mm dưới {rule['value']} mm {tag(rule)}"
            low_ok = small and small[0]["value"] <= t["flight_width"]
            if low_ok and (fh is None or ppl is None):
                warn.append(msg + "; được 700 mm nếu nhà ≤ 15 m và ≤ 15 người/tầng: cần chiều cao PCCC và số người")
            else:
                law.put(rule, bad, warn, msg, ("fire_height_mm", "people_per_floor"))
        for r in law.rows_for("tread_min"):
            if t["tread"] < r["value"]:
                law.put(r, bad, warn, f"{n} {s['id']}: mặt bậc {t['tread']} mm dưới {r['value']} mm {tag(r)}")
        for r in law.rows_for("riser_range"):
            if not s.get("risers") or s["up_to"] not in elev:
                missing_risers.setdefault(s["id"].split("/")[-1], []).append(n)
                continue
            h = (elev[s["up_to"]] - elev[n]) / s["risers"]
            lo, hi = r["value"]
            if not lo <= h <= hi:
                law.put(r, bad, warn, f"{n} {s['id']}: cổ bậc {h:.0f} mm ngoài {lo}–{hi} mm {tag(r)}")
    for sid, lvls in missing_risers.items():  # one line per stair, not per floor
        warn.append(f"thang {sid} ({', '.join(lvls)}): bảng số thiếu số bậc, chưa tính được cổ bậc "
                    f"{tag(law.rows_for('riser_range')[0])}")
    if stairs:
        add("stairs_law", "Thang đúng luật: bản thang, mặt bậc, cổ bậc", bad, warn)
    else:
        add("stairs_law", "Thang đúng luật: bản thang, mặt bậc, cổ bậc", [], skip="bảng số không có thang")

    # Stair rooms and exit doors on each plan.
    def room_at(n, p):
        hits = [r["id"] for r in flat[n]["rooms"] if (n, r["id"]) in room_poly and inside(p, room_poly[(n, r["id"])])]
        return min(hits, key=lambda i: polygon_area(room_poly[(n, i)])) if hits else None

    def nearest_room(n, p):
        best = None
        for r in flat[n]["rooms"]:
            poly = room_poly.get((n, r["id"]))
            if poly:
                dd = 0 if inside(p, poly) else min(math.dist(p, q) for q in poly)
                if best is None or dd < best[0]:
                    best = (dd, r["id"])
        return best[1] if best and best[0] <= 3000 else None

    stair_rooms = {}
    for n in plans:
        feet = [s["at"] for s in flat[n]["stairs"]]
        feet += [s["at"] for m in names for s in flat[m]["stairs"] if s["up_to"] == n]
        stair_rooms[n] = {nearest_room(n, p) for p in feet} - {None}

    def door_sides(n, o):
        (cx, cy), (ux, uy) = o["centre"], o["u"]
        reach = o["wall_t"] / 2 + 100
        return [room_at(n, (cx - uy * reach, cy + ux * reach)), room_at(n, (cx + uy * reach, cy - ux * reach))]

    doors = {n: [(o, door_sides(n, o)) for o in flat[n]["openings"] if o["kind"] in ("door", "shutter", "opening")]
             for n in plans}

    # 3. Exit doors and corridors.
    bad, warn = [], []
    use = {(n, r["id"]): r["use"] for n in plans for r in flat[n]["rooms"]}

    def on_escape_route(n, o, sides):
        """A door people leave by: out of the house on the ground floor, into a
        stair room from a hall, or the entrance of a flat or hotel room."""
        if kinds[n] == "ground" and None in sides:
            return True
        a, b = sides
        if None in sides:
            return False
        if any(sd in stair_rooms[n] for sd in sides):
            other = b if a in stair_rooms[n] else a
            return use.get((n, other)) == "circulation" or bool(unit_of(other)) != bool(unit_of(a if other == b else b))
        return bool(unit_of(a)) != bool(unit_of(b))

    door_rows = law.rows_for("exit_door_width_min")
    door_rows = [r for r in door_rows if "people_per_floor_over" in r["applies"]][:1] or door_rows
    for r in door_rows:
        for n in plans:
            for o, sides in doors[n]:
                exit_door = on_escape_route(n, o, sides)
                if exit_door and o["kind"] == "door" and o["width"] < r["value"]:
                    law.put(r, bad, warn, f"{n} {o['id']}: cửa thoát nạn {o['width']} mm dưới {r['value']} mm {tag(r)}")
    for r in law.rows_for("corridor_width_min"):
        for n in plans:
            for room in flat[n]["rooms"]:
                poly = room_poly.get((n, room["id"]))
                if room["use"] != "circulation" or not poly or room["id"] in stair_rooms[n]:
                    continue
                xs, ys = [p[0] for p in poly], [p[1] for p in poly]
                w = min(max(xs) - min(xs), max(ys) - min(ys))
                rect_like = polygon_area(poly) >= 0.9 * (max(xs) - min(xs)) * (max(ys) - min(ys))
                if w < r["value"]:
                    msg = f"{n} {room['name']}: hành lang rộng {w:.0f} mm dưới {r['value']} mm {tag(r)}"
                    if rect_like:
                        law.put(r, bad, warn, msg)
                    else:
                        warn.append(msg + " (đo gần đúng)")
    add("exits_width", "Cửa thoát nạn và hành lang đủ rộng", bad, warn)

    # 4. Number of exits per storey and their spacing.
    def floor_m2(n):
        walls = [wall_poly(w) for w in flat[n]["walls"] if w["t"] > 0]
        return footprint_sum([], walls, [])[0] if walls else 0

    bad, warn = [], []
    for r in law.rows_for("exits_min"):
        for n in plans:
            if kinds[n] in ("roof", "basement"):
                continue
            unit_area = sum(a for a in (area(n, rr) for rr in flat[n]["rooms"] if unit_of(rr["id"])) if a)
            cond = r.get("condition") or {}
            need = law.kind == "hotel" or unit_area > cond.get("apartment_units_area_m2_over", 0) \
                or (ppl or 0) >= 50
            if need and len(stair_rooms[n]) < r["value"]:
                msg = (f"{n}: {len(stair_rooms[n])} lối thoát (thang), cần {r['value']}; "
                       f"diện tích căn hộ trên tầng {unit_area:.0f} m² {tag(r)}")
                if law.kind == "hotel" and len(stair_rooms[n]) == 1 and r.get("one_exit_hotel"):
                    verdict = hotel_one_exit(r["one_exit_hotel"], law.inputs, floor_m2(n))
                    if verdict == "ok":
                        continue
                    if verdict:
                        warn.append(f"{msg}; {verdict}")
                        continue
                    law.put(r, bad, warn, msg)
                else:
                    law.put(r, bad, warn, msg + "; ngoại lệ một lối ở 3.2.6.2 cần xét tay")
    for r in law.rows_for("exits_spacing_min"):
        for n in plans:
            sr = sorted(stair_rooms[n])
            if len(sr) < 2:
                continue
            pts = [q for w in flat[n]["walls"] for q in (w["a"], w["b"])]
            diag = math.dist((min(p[0] for p in pts), min(p[1] for p in pts)),
                             (max(p[0] for p in pts), max(p[1] for p in pts)))
            share = r["value"]["with_sprinkler"] if law.inputs.get("sprinkler") else r["value"]["of_diagonal"]
            need = max(diag * share, r["value"]["min_mm"])
            cent = {k: [o["centre"] for o, sides in doors[n] if k in sides] for k in sr}
            far = max((math.dist(a, b) for i, k in enumerate(sr) for k2 in sr[i + 1:]
                       for a in cent[k] for b in cent[k2]), default=0)
            if far and far < need:
                msg = f"{n}: hai lối thoát cách {far:.0f} mm, cần ≥ {need:.0f} mm {tag(r)}"
                law.put(r, bad, warn, msg, () if "sprinkler" in law.inputs else ("sprinkler",))
    add("exits_count", "Số lối thoát mỗi tầng và khoảng cách giữa chúng", bad, warn,
        skip=None if law.rows_for("exits_min") else "luật không bắt số lối thoát cho loại công trình này")

    # 5. Travel distance from each flat or room door to the nearest stair door.
    t = travel_limits(law)
    if t:
        rule, limits = t["rule"], t["limits"]
        bad, warn = [], []
        if t["note"]:
            warn.append(f"{t['note']} {tag(rule)}")
        for n in plans:
            graph = {}
            for o, sides in doors[n]:
                for sd in sides:
                    if sd:
                        graph.setdefault(sd, []).append(o)
            targets = {o["id"] for o, sides in doors[n] if any(sd in stair_rooms[n] for sd in sides)}
            for o, sides in doors[n]:
                inner = [sd for sd in sides if sd and unit_of(sd)]
                outer = [sd for sd in sides if sd and not unit_of(sd)]
                if not inner or not outer or o["id"] in targets:
                    continue
                dist, reached = _dijkstra(o, graph, outer, targets, stair_rooms[n], doors[n])
                if dist is None:
                    continue
                between = reached >= 2
                limit = limits[0] if between else limits[1]
                lo = hi = limit
                if t["alt"] and not between:  # two texts give two dead-end limits: between them asks for a look
                    lo, hi = min(limit, t["alt_dead_end"]), max(limit, t["alt_dead_end"])
                msg = f"{n} cửa {o['id']}: đi {dist / 1000:.1f} m tới thang"
                if dist > hi:
                    line = f"{msg}, quá {hi / 1000:.0f} m {tag(rule)}"
                    if t["note"]:
                        warn.append(line)
                    else:
                        law.put(rule, bad, warn, line, t["needs"])
                elif dist > lo:
                    warn.append(f"{msg}: giữa hai ngưỡng hành lang cụt {lo / 1000:.0f} và {hi / 1000:.0f} m "
                                f"của hai bảng {tag(rule)} {tag(t['alt'])}")
                elif dist > lo * (1 - NEAR):
                    warn.append(f"{msg}, sát ngưỡng {lo / 1000:.0f} m {tag(rule)}")
        add("travel", "Quãng đi tới lối thoát", bad, warn)

    # 6. Plot: density, total floor area, setback.
    site = d.get("site", {}).get("outline")
    if site:
        plot = polygon_area([tuple(p) for p in site]) / 1e6
        foot = {}
        for n in names:
            walls = [wall_poly(w) for w in flat[n]["walls"] if w["t"] > 0]
            if walls and kinds[n] not in ("roof",):
                foot[n] = footprint_sum([], walls, [])[0]
        above = [n for n in names if kinds[n] not in ("roof", "basement") and n in foot]
        ground = next((n for n in above if kinds[n] == "ground"), above[0] if above else None)
        height = max(elev.values()) - (elev[ground] if ground else 0)
        bad, warn = [], []
        dens = foot.get(ground, 0) / plot * 100 if ground else 0
        for r in law.rows_for("density_max"):
            if "by_plot_m2" in r["value"]:
                limit = interp(r["value"]["by_plot_m2"], plot)
                ex = law.rows_for("density_max_existing")
                if ex and law.inputs.get("area_kind") == "existing" and plot <= ex[0]["value"]["plot_max_m2"] \
                        and height <= ex[0]["value"]["height_max_mm"]:
                    limit = ex[0]["value"]["density"]
            else:
                limit = table2(r, height, plot)
            line = f"mật độ {dens:.1f} % trên lô {plot:.0f} m², tối đa {limit:.1f} % {tag(r)}"
            if dens > limit + 0.05:
                law.put(r, bad, warn, line, ("area_kind",) if "by_plot_m2" in r["value"] else ())
        lim = d.get("site", {}).get("limits", [])
        for item in lim:
            if item["name"] == "density_min_pct" and dens < item["value"]:
                warn.append(f"mật độ {dens:.1f} % dưới mức tối thiểu {item['value']} % của đề")
            if item["name"] == "density_max_pct" and dens > item["value"]:
                bad.append(f"mật độ {dens:.1f} % vượt mức tối đa {item['value']} % của đề")
        for r in law.rows_for("floor_area_ratio_max"):
            total = sum(foot[n] for n in above)
            if total > r["value"] * plot:
                law.put(r, bad, warn, f"tổng sàn {total:.0f} m² quá {r['value']} lần lô {tag(r)}")
        for r in law.rows_for("setback_min"):
            road = law.inputs.get("road_area_level_or_above")
            if road is None:
                warn.append(f"chưa biết đường giáp lô có từ cấp khu vực trở lên không {tag(r)}")
                continue
            if not road:
                continue
            width = law.inputs.get("road_width_m")
            if width is None:
                warn.append(f"thiếu bề rộng đường để tra khoảng lùi {tag(r)}")
                continue
            v = r["value"]
            row = sum(1 for w in v["road_widths_m"] if width >= w)
            col = sum(1 for h in v["heights_mm"] if height >= h)
            need = v["table"][row][col] * 1000
            fe = d["site"].get("front_edge", 0)
            a, b = site[fe], site[(fe + 1) % len(site)]
            pts = [q for w in flat[ground]["walls"] if w["t"] > 0 for q in wall_poly(w)] if ground else []
            gap = min((_seg_dist(q, a, b) for q in pts), default=math.inf)
            if gap + 1 < need:
                law.put(r, bad, warn, f"lùi {gap:.0f} mm so với cạnh giáp đường, cần ≥ {need:.0f} mm {tag(r)}")
        add("plot", "Mật độ, tổng sàn, khoảng lùi", bad, warn)

    # 7. Lifts and parking for flats.
    unit_keys = {(n, unit_of(r["id"])) for n in names for r in flat[n]["rooms"]
                 if unit_of(r["id"]) and clusters[unit_of(r["id"]).split("/")[-1].split("#")[0]].get("kind") == "unit"}
    units = len(unit_keys)
    storeys = len([n for n in names if kinds[n] not in ("roof", "basement")])
    bad, warn = [], []
    for r in law.rows_for("lifts_min"):
        lifts = max((len([s for s in flat[n]["shafts"] if s.get("kind") == "lift"]) for n in names), default=0)
        people = ppl * (storeys - 1) if ppl is not None else None  # the ground floor does not count
        need, by_people = lifts_needed(r["value"], storeys, units, people)
        if lifts < need:
            law.put(r, bad, warn, f"{lifts} thang máy cho {storeys} tầng, {units} căn; cần ≥ {need} {tag(r)}")
        elif by_people and lifts < by_people:
            warn.append(f"{lifts} thang máy; tính theo {people} người thì cần ≥ {by_people}, văn bản cho "
                        f"{r['value']['per_people']} người hoặc {r['value']['per_units']} căn một thang {tag(r)}")
        elif need and by_people is None:
            warn.append(f"chưa biết số người mỗi tầng, chưa tính thang máy theo người {tag(r)}")
    for r in law.rows_for("parking_area_min"):
        car = sum(polygon_area(p["poly"]) / 1e6 for n in names for p in flat[n]["parking"] if p["vehicle"] == "car")
        bike = sum(polygon_area(p["poly"]) / 1e6 for n in names for p in flat[n]["parking"]
                   if p["vehicle"] == "motorbike")
        measured = [area(n, rr) for (n, u) in unit_keys for rr in flat[n]["rooms"] if unit_of(rr["id"]) == u]
        complete = bool(measured) and None not in measured  # every flat drawn and outlined
        v = r["value"]
        need_car = max(v["per_4_units_m2"] * units / 4,
                       v["per_100m2_units"] * sum(measured) / 100 if complete else 0)
        if units and car < need_car:
            law.put(r, bad, warn, f"chỗ ô tô {car:.0f} m², cần ≥ {need_car:.0f} m² {tag(r)}")
        if units and not complete:
            warn.append(f"chưa đo được diện tích mọi căn (tầng không vẽ hay phòng thiếu đường bao): mức "
                        f"{v['per_100m2_units']} m² cho 100 m² căn chưa tính {tag(r)}")
        if units and bike < v["motorbike_per_unit_m2"] * units:
            law.put(r, bad, warn, f"chỗ xe máy {bike:.0f} m², cần ≥ {v['motorbike_per_unit_m2'] * units} m² {tag(r)}")
    if law.rows_for("lifts_min") or law.rows_for("parking_area_min"):
        add("services", "Thang máy và chỗ để xe", bad, warn)

    # 8. What each city decides.
    local = law.rows_for("local_only")
    if local:
        add("local", "Luật địa phương", [], [f"{r['what']}: xem quy chế kiến trúc nơi xây {tag(r)}" for r in local])
    return out


def _seg_dist(p, a, b):
    ax, ay = a
    bx, by = b
    dx, dy = bx - ax, by - ay
    t = max(0.0, min(1.0, ((p[0] - ax) * dx + (p[1] - ay) * dy) / (dx * dx + dy * dy or 1)))
    return math.dist(p, (ax + t * dx, ay + t * dy))


def _dijkstra(start, graph, rooms, targets, stair_rooms, doors):
    """Shortest walk from a door, through the given rooms and the doors between
    them, to a stair door. Returns (mm, how many stair rooms are reachable)."""
    best, seen = None, set()
    reachable = set()
    heap = [(0.0, id(start), start, tuple(rooms))]
    by_id = {o["id"]: (o, sides) for o, sides in doors}
    while heap:
        dist, _, door, via = heapq.heappop(heap)
        if door["id"] in seen:
            continue
        seen.add(door["id"])
        if door["id"] in targets and door is not start:
            if best is None:
                best = dist
            reachable |= {sd for sd in by_id[door["id"]][1] if sd in stair_rooms}
            continue
        for room in via:
            for nxt in graph.get(room, []):
                if nxt["id"] not in seen:
                    sides = by_id[nxt["id"]][1]
                    heapq.heappush(heap, (dist + math.dist(door["centre"], nxt["centre"]), id(nxt), nxt,
                                          tuple(sd for sd in sides if sd and sd != room)))
    return best, len(reachable)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("dxf")
    ap.add_argument("params")
    ap.add_argument("--rules", default=str(RULES))
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)
    try:
        d, dups = params_check.load(args.params)
        rules = json.loads(pathlib.Path(args.rules).read_text(encoding="utf-8"))
    except (OSError, ValueError) as err:
        print(f"không đọc được: {err}", file=sys.stderr)
        return 2
    errs = rules_errors(rules)
    if errs:
        print(f"Bảng luật {args.rules} không hợp lệ, dừng:")
        for e in errs:
            print(f"LỖI   {e}")
        return 1
    rep = params_check.check(d, dups)
    if rep.errors:
        print("Bảng số chưa qua params_check.py, dừng:")
        for e in rep.errors:
            print(f"LỖI   {e['path']}: {e['msg']}")
        return 1
    try:
        results = check(args.dxf, d, rules)
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
