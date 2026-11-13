#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# dependencies = ["ezdxf>=1.3"]
# ///
"""cua_vao.py FILE [--json] — the one door for every input the skill takes
(references/phieu.md): a brief form (phieu.json, `cad-brief/1`), a DXF of an
existing site or building, or anything else, which is turned away with what
to bring instead. Reading a DXF needs ezdxf (`uv run cua_vao.py FILE`); the
brief form needs only the standard library.

Exit 0 = accepted, 1 = turned away with the list of what to fix,
2 = the file could not be read.
"""
import argparse
import json
import pathlib
import sys

SCHEMA = "cad-brief/1"
TYPES = ("house", "apartment", "hotel", "apartment_building")
LABELS = {  # every field, in words a reader understands
    "type": "loại công trình", "work": "xây mới hay cải tạo", "depth": "độ sâu hồ sơ",
    "place": "nơi xây", "site": "khu đất (các cạnh, hoặc file DXF)", "street_edge": "cạnh giáp đường",
    "street_width_mm": "bề rộng đường", "setbacks": "khoảng lùi", "north": "hướng bắc",
    "limits": "chỉ tiêu quy hoạch", "budget": "tiền", "rules": "luật áp dụng",
    "occupants": "ai ở", "rooms_needed": "các phòng cần có", "floors_wanted": "số tầng mong muốn",
    "existing_dxf": "file DXF căn hộ có sẵn", "keep_untouched": "phần không được đụng",
    "room_types": "số phòng theo loại", "stars": "hạng sao", "services": "các khu dịch vụ",
    "unit_types": "số căn theo loại", "floors": "số tầng nổi", "basements": "số tầng hầm",
    "podium": "khối đế",
}
COMMON = ("type", "work", "depth", "place", "site")
OPTIONAL = ("street_edge", "street_width_mm", "setbacks", "north", "limits", "budget", "rules")
BY_TYPE = {
    "house": ("occupants", "rooms_needed", "floors_wanted"),
    "apartment": ("existing_dxf", "keep_untouched", "rooms_needed"),
    "hotel": ("room_types", "stars", "services"),
    "apartment_building": ("unit_types", "floors", "basements", "podium"),
}
MEASURED = ("site", "street_width_mm", "existing_dxf")  # the real world: never estimated
SEEN_ONLY = {  # files the skill reads to understand, never to measure
    ".pdf": "bản PDF", ".png": "ảnh", ".jpg": "ảnh", ".jpeg": "ảnh", ".tif": "bản quét",
    ".tiff": "bản quét", ".heic": "ảnh", ".webp": "ảnh", ".dwg": "file DWG",
}


def is_int(v):
    return isinstance(v, int) and not isinstance(v, bool)


def pos_int(v):
    return is_int(v) and v > 0


def list_of(v, keys, count_keys=("count",)):
    """A non-empty list of tables, each with all of `keys` and a positive
    number under one of `count_keys`."""
    if not isinstance(v, list) or not v:
        return False
    positive = lambda x: isinstance(x, (int, float)) and not isinstance(x, bool) and x > 0  # noqa: E731
    return all(isinstance(item, dict) and all(k in item for k in keys)
               and any(positive(item.get(k)) for k in count_keys) for item in v)


def text(v):
    return isinstance(v, str) and v.strip() != ""


SHAPES = {  # field: (test, what it should look like)
    "type": (lambda v: v in TYPES, "một trong " + ", ".join(TYPES)),
    "work": (lambda v: v in ("new", "renovation"), "new hoặc renovation"),
    "depth": (lambda v: v in ("construction", "scheme"), "construction hoặc scheme"),
    "place": (lambda v: isinstance(v, dict) and text(v.get("province")), '{"province": …, "ward": …, "street": …}'),
    "site": (lambda v: isinstance(v, dict) and (
        (isinstance(v.get("edges_mm"), list) and len(v["edges_mm"]) >= 3 and all(map(pos_int, v["edges_mm"])))
        or text(v.get("from_dxf"))), '{"edges_mm": [ít nhất ba cạnh, milimét]} hoặc {"from_dxf": "<file>"}'),
    "street_edge": (lambda v: is_int(v) and v >= 0, "số của một cạnh"),
    "street_width_mm": (pos_int, "milimét dương"),
    "setbacks": (lambda v: isinstance(v, list) and all(
        isinstance(s, dict) and is_int(s.get("edge")) and is_int(s.get("mm")) and s["mm"] >= 0 for s in v),
        '[{"edge": số cạnh, "mm": khoảng lùi}]'),
    "north": (lambda v: text(v) or (isinstance(v, (int, float)) and not isinstance(v, bool)), "hướng hoặc góc độ"),
    "limits": (lambda v: isinstance(v, dict) and all(isinstance(x, (int, float)) and not isinstance(x, bool)
                                                     for x in v.values()), "bảng số"),
    "budget": (lambda v: isinstance(v, dict) and pos_int(v.get("amount_vnd")), '{"amount_vnd": số tiền}'),
    "rules": (lambda v: isinstance(v, list) and all(map(text, v)), "danh sách văn bản"),
    "occupants": (lambda v: list_of(v, ("who",)), '[{"who": …, "count": …}]'),
    "rooms_needed": (lambda v: list_of(v, ("room",)), '[{"room": …, "count": …}]'),
    "floors_wanted": (pos_int, "số tầng"),
    "existing_dxf": (text, "đường dẫn file DXF"),
    "keep_untouched": (lambda v: isinstance(v, list) and all(map(text, v)), "danh sách chữ"),
    "room_types": (lambda v: list_of(v, ("type",)), '[{"type": …, "count": …}]'),
    "stars": (lambda v: is_int(v) and 1 <= v <= 5, "số từ 1 tới 5"),
    "services": (lambda v: isinstance(v, list) and all(map(text, v)), "danh sách chữ"),
    "unit_types": (lambda v: list_of(v, ("type",), ("count", "share_pct")), '[{"type": …, "count" hoặc "share_pct": …}]'),
    "floors": (pos_int, "số tầng"),
    "basements": (lambda v: is_int(v) and v >= 0, "số tầng hầm, 0 khi không có"),
    "podium": (text, 'chữ mô tả, hoặc "none"'),
}


def check_brief(d):
    """Problems with a brief: (field, message) pairs; empty means accepted."""
    out = []
    if not isinstance(d, dict) or d.get("schema") != SCHEMA:
        return [("schema", f"phiếu phải ghi \"schema\": \"{SCHEMA}\"")]
    kind = d.get("type", {}).get("value") if isinstance(d.get("type"), dict) else None
    kind = kind if isinstance(kind, str) else None  # a wrong shape is reported below, not used as a key
    required = list(COMMON) + list(BY_TYPE.get(kind, ()))
    if kind == "apartment":
        required.remove("site")  # a flat is drawn from its existing plan, not from a plot
    known = set(COMMON) | set(OPTIONAL) | {f for fs in BY_TYPE.values() for f in fs} | {"schema", "note"}
    for key in d:
        if key not in known:
            out.append((key, f"ô \"{key}\" không thuộc phiếu {SCHEMA}"))
    for key in required:
        cell = d.get(key)
        if cell is None:
            out.append((key, f"thiếu ô {LABELS[key]}"))
        elif isinstance(cell, dict) and cell.get("pending"):
            what = "người dùng đo hoặc đưa giấy tờ" if key in MEASURED else "hỏi người dùng hoặc tra"
            out.append((key, f"ô {LABELS[key]} còn trống: {what}"))
    for key, cell in d.items():
        if key in ("schema", "note") or key not in LABELS:
            continue
        if not isinstance(cell, dict):
            out.append((key, f"ô {LABELS[key]} phải viết {{\"value\": …, \"by\": …}}"))
            continue
        if cell.get("pending"):
            continue
        if "value" not in cell:
            out.append((key, f"ô {LABELS[key]}: thiếu value"))
            continue
        if cell.get("by", "user") not in ("user", "model"):
            out.append((key, f"ô {LABELS[key]}: by phải là user hoặc model"))
        if key in MEASURED and "by" not in cell:
            out.append((key, f"ô {LABELS[key]} là số đo thế giới thật: ghi rõ \"by\": \"user\" và nguồn"))
        if key in MEASURED and cell.get("by") == "model":
            out.append((key, f"ô {LABELS[key]} là số đo thế giới thật, AI không được ước: "
                             "người dùng đo, đưa giấy tờ, hoặc đưa file DXF"))
        test, shape = SHAPES[key]
        if not test(cell["value"]):
            out.append((key, f"ô {LABELS[key]} phải là {shape}"))
    # A street edge or a setback must name an edge the plot has.
    site = d.get("site", {}).get("value") if isinstance(d.get("site"), dict) else None
    edges = len(site["edges_mm"]) if isinstance(site, dict) and isinstance(site.get("edges_mm"), list) else None
    if edges and edges >= 3:  # a plot of fewer edges is already reported above
        refs = []
        se = d.get("street_edge", {})
        if isinstance(se, dict) and is_int(se.get("value")):
            refs.append(("street_edge", se["value"]))
        sb = d.get("setbacks", {})
        if isinstance(sb, dict) and isinstance(sb.get("value"), list):
            refs += [("setbacks", s.get("edge")) for s in sb["value"] if isinstance(s, dict) and is_int(s.get("edge"))]
        for key, e in refs:
            if not 0 <= e < edges:
                out.append((key, f"ô {LABELS[key]} nói cạnh {e}, mà khu đất chỉ có cạnh 0 tới {edges - 1}"))
    return out


# ---- DXF of an existing site or building ------------------------------------

def check_dxf(path):
    import ezdxf  # only DXF input needs it
    sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
    sys.dont_write_bytecode = True
    from dxf_check import self_crossing

    doc = ezdxf.readfile(path)
    msp = doc.modelspace()
    out = []
    if doc.header.get("$INSUNITS") != 4:
        out.append(("units", "đặt đơn vị bản vẽ là milimét ($INSUNITS = 4) rồi lưu lại"))

    def polylines(layer):
        """(points, closed) of every polyline on a layer, old-style 2D ones too;
        a last point repeating the first closes the shape as the flag does."""
        out_ = []
        for e in msp:
            if e.dxf.layer != layer:
                continue
            if e.dxftype() == "LWPOLYLINE":
                pts = [tuple(p[:2]) for p in e.get_points("xy")]
            elif e.dxftype() == "POLYLINE" and not e.is_3d_polyline and not e.is_poly_face_mesh:
                pts = [tuple(v.dxf.location)[:2] for v in e.vertices]
            else:
                continue
            flag = e.closed if e.dxftype() == "LWPOLYLINE" else e.is_closed
            closed = flag or (len(pts) > 2 and pts[0] == pts[-1])
            if pts and pts[0] == pts[-1]:
                pts = pts[:-1]
            out_.append((pts, closed))
        return out_

    site, walls = polylines("C-PROP"), polylines("A-WALL")
    loose = [e for e in msp if e.dxf.layer == "C-PROP" and e.dxftype() in ("LINE", "ARC")]
    if not site and not walls:
        out.append(("layers", "không thấy ranh đất trên layer C-PROP hay tường trên layer A-WALL: "
                              "vẽ ranh đất thành một đường khép kín trên C-PROP, tường có sẵn trên A-WALL"))
    if loose:
        out.append(("C-PROP", "ranh đất đang là các nét rời: nối lại thành một đường nhiều đoạn khép kín"))
    if len(site) > 1:
        out.append(("C-PROP", f"có {len(site)} đường trên C-PROP: giữ đúng một đường cho ranh đất"))
    for pts, closed in site:
        if not closed:
            out.append(("C-PROP", "ranh đất chưa khép kín: đóng đường nhiều đoạn lại"))
        elif self_crossing(pts):
            out.append(("C-PROP", "ranh đất tự cắt: vẽ lại theo đúng thứ tự các góc"))
    open_walls = [pts for pts, closed in walls if not closed]
    if open_walls:
        out.append(("A-WALL", f"{len(open_walls)} khối tường chưa khép kín trên A-WALL"))
    return out


def turned_away(path):
    kind = SEEN_ONLY.get(path.suffix.lower(), "file này")
    return [("input", f"{kind} chỉ được đọc để hiểu bối cảnh, không lấy số đo từ đó. Đưa thay vào: "
                      "ranh đất hay mặt bằng có sẵn vẽ thành DXF (ranh đất là một đường khép kín trên "
                      "layer C-PROP, tường trên A-WALL, đơn vị milimét), hoặc điền kích thước từng cạnh "
                      "vào phiếu đề bài (references/phieu.md).")]


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("file")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)
    path = pathlib.Path(args.file)
    if not path.is_file():
        print(f"không đọc được {path}: không có file này", file=sys.stderr)
        return 2
    try:
        if path.suffix.lower() == ".json":
            problems = check_brief(json.loads(path.read_text(encoding="utf-8")))
        elif path.suffix.lower() == ".dxf":
            problems = check_dxf(str(path))
        else:
            problems = turned_away(path)
    except ImportError:
        print("đọc DXF cần ezdxf: chạy bằng `uv run cua_vao.py <file>`", file=sys.stderr)
        return 2
    except (OSError, ValueError) as err:
        print(f"không đọc được {path}: {err}", file=sys.stderr)
        return 2
    except Exception as err:  # ezdxf's own read errors
        if type(err).__name__.startswith("DXF"):
            print(f"không đọc được {path}: {err}", file=sys.stderr)
            return 2
        raise
    if args.json:
        print(json.dumps([{"field": f, "msg": m} for f, m in problems], ensure_ascii=False, indent=1))
    else:
        for f, m in problems:
            print(f"CHẶN  {m}")
        print("nhận" if not problems else f"chặn: {len(problems)} điều cần sửa")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
