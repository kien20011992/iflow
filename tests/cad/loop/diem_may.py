#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# dependencies = ["ezdxf>=1.3"]
# ///
"""diem_may.py DXF PARAMS [--build BUILD.PY] [--json] — part A of the common
rubric (tests/cad/loop/thang-chung.md), scored by machine: run the number-table
checker, the DXF checker, the table-against-drawing checker, the law checker
and CADCraft's own audit on one round's files, and turn what they say into
points by the rules written below. It also reports, apart from the score,
what was handed back: clouds the drawing library left on A-REVS for what it
could not draw, and with --build-log the "Chưa vẽ" list of the last build.py
run sorted by kind, each beside the number of things the table asks to draw. With --build, also
report how much of the
project's build.py differs from lib/build_mau.py: the share drawn outside the
drawing library, reported apart and never added to the score.

Part A is raw points over the points of the items that ran (25 when
CADCraft is installed); it is never rescaled. Exit 0 when it could score, 2
when an input file could not be read.
"""
import argparse
import difflib
import json
import os
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
SCRIPTS = ROOT / "skills/cad/scripts"
BUILD_MAU = ROOT / "skills/cad/lib/build_mau.py"
TIMEOUT = 900  # seconds for one checker; a hung tool scores 0, not forever

# id: (title, points). The rules for each live in score_item.
ITEMS = {
    "A1": ("Bảng số qua params_check.py", 4),
    "A2": ("File qua dxf_check.py", 7),
    "A3": ("File khớp bảng số qua plan_check.py", 6),
    "A4": ("Không phép luật nào trượt qua luat_check.py", 4),
    "A5": ("Audit của CADCraft không lỗi", 4),
}


def run_checker(args):
    """{"code": exit code, "data": its --json output or None, "why": text when it did not run}."""
    env = dict(os.environ, PYTHONIOENCODING="utf-8", PYTHONDONTWRITEBYTECODE="1")
    try:
        r = subprocess.run([sys.executable, *map(str, args), "--json"], capture_output=True, text=True,
                           encoding="utf-8", errors="replace", timeout=TIMEOUT, env=env)
    except subprocess.TimeoutExpired:
        return {"code": None, "data": None, "why": f"quá {TIMEOUT} giây"}
    try:
        return {"code": r.returncode, "data": json.loads(r.stdout), "why": None}
    except ValueError:
        return {"code": r.returncode, "data": None, "why": f"mã {r.returncode}"}


def run_audit(dxf):
    """CADCraft audit error count; "none" when CADCraft is not installed;
    None when it ran but gave no count."""
    for d in ("skills/cad/lib", "tests/cad"):
        if str(ROOT / d) not in sys.path:
            sys.path.insert(0, str(ROOT / d))
    sys.dont_write_bytecode = True
    from chay import find_cli  # noqa: E402  (only finds the program; draws nothing)
    from lib_build_test import audit  # noqa: E402  (the one audit parser of the repo)
    cli = find_cli()
    return "none" if cli is None else audit(cli, dxf, TIMEOUT)


def score_item(key, got, table_ok=True):
    """Points (None = not run) and a one-line reason for one item.

    got for A1–A4: what run_checker returned; A5: what run_audit returned.
    A broken number table (table_ok False) leaves A3 and A4 nothing to check:
    they score 0, as thang-chung.md says."""
    full = ITEMS[key][1]
    if key == "A5":
        if got == "none":
            return None, "máy không có CADCraft, chưa chạy"
        if got is None:
            return 0, "CADCraft chạy nhưng không ra số lỗi đọc được (hỏng, treo hay đổi cách in)"
        return (full, "0 lỗi") if got == 0 else (0, f"{got} lỗi")
    if key in ("A3", "A4") and not table_ok:
        return 0, "bảng số hỏng nên không kiểm được"
    data = got["data"]
    if data is None:
        return 0, f"trình kiểm không chạy được ({got['why']})"
    if key == "A1":
        if data["errors"]:
            return 0, f"{len(data['errors'])} lỗi khuôn"
        return full, "không lỗi" + (f", {len(data['warnings'])} cảnh báo" if data["warnings"] else "")
    fails = [r for r in data if r["status"] == "fail"]
    warns = [r for r in data if r["status"] == "warn"]
    if key == "A4":  # a law look usually means a missing input, not a bad drawing
        return (0, f"{len(fails)} phép trượt") if fails else (full, f"không phép nào trượt, {len(warns)} cần xem")
    if fails:
        return 0, f"{len(fails)} phép trượt: " + ", ".join(r["id"] for r in fails)
    if warns:
        return full / 2, f"{len(warns)} phép cần xem: " + ", ".join(r["id"] for r in warns)
    return full, "mọi phép đạt"


def outside_library(build):
    """How much of the project's build.py departs from lib/build_mau.py: lines
    added or changed, and library lines dropped."""
    mine = pathlib.Path(build).read_text(encoding="utf-8").splitlines()
    base = BUILD_MAU.read_text(encoding="utf-8").splitlines()
    sm = difflib.SequenceMatcher(None, base, mine, autojunk=False)
    same = sum(b.size for b in sm.get_matching_blocks())
    return {"lines": len(mine), "changed_or_added": len(mine) - same, "library_lines_dropped": len(base) - same,
            "share": round((len(mine) - same) / len(mine), 3) if mine else 0.0}


KINDS = (  # how a line of the "Chưa vẽ" list reads, first match wins
    ("text_no_spot", lambda t: "không có chỗ" in t),         # a label or room name found no free spot
    ("assumed", lambda t: "lấy mặc định" in t or "(ước)" in t),  # drawn, from a default the user must confirm
    ("area_note", lambda t: "diện tích" in t and "tính cả" in t),  # a note on a number
    ("needs_eye", lambda t: "cần người" in t),               # drawn, a person must look at it in AutoCAD
)


def read_log(log):
    """A build log as text: UTF-8, or UTF-16 when it starts with a byte-order
    mark (Windows PowerShell 5.1 redirection). Raises when it is neither."""
    raw = pathlib.Path(log).read_bytes()
    if raw[:2] in (b"\xff\xfe", b"\xfe\xff"):
        return raw.decode("utf-16")
    return raw.decode("utf-8-sig")


def handed_back_log(log):
    """The "Chưa vẽ" list build.py prints at the end of a run, sorted by kind.
    What fits no kind above is a part of the drawing not drawn ("undrawn");
    "drawings" counts the whole drawings among them ("hình site")."""
    lines, on = [], False
    for line in read_log(log).splitlines():
        if line.startswith("cadcraft-cli:"):  # every build.py run prints this first: a new run starts
            on, lines = False, []
            continue
        if line.strip().startswith("Chưa vẽ"):
            on, lines = True, []  # the last run's list counts
            continue
        if on:
            if line.startswith("  - "):
                lines.append(line[4:])
            elif line.strip():
                on = False
    out = {k: 0 for k, _ in KINDS}
    out.update(undrawn=0, drawings=0, listed=len(lines))
    for t in lines:
        kind = next((k for k, test in KINDS if test(t)), "undrawn")
        out[kind] += 1
        if kind == "undrawn" and t.startswith("hình "):
            out["drawings"] += 1
    return out


def handed_back(dxf, params):
    """Clouds the drawing library left on A-REVS for what it could not draw,
    and how many things the table asks to draw (rooms, openings, stairs and
    furniture on every level that has a plan). The two are compared, not
    divided as parts of one whole: a cloud can also mark a skewed wall or a
    whole drawing, so the ratio may pass 100 %."""
    import ezdxf  # noqa: E402
    if str(SCRIPTS) not in sys.path:
        sys.path.insert(0, str(SCRIPTS))
    sys.dont_write_bytecode = True
    from plan_check import flatten  # noqa: E402  (a checker, not the drawing library)
    d = json.loads(pathlib.Path(params).read_text(encoding="utf-8"))
    msp = ezdxf.readfile(str(dxf)).modelspace()

    def closed(e):
        pts = [tuple(p[:2]) for p in (e.get_points("xy") if e.dxftype() == "LWPOLYLINE" else e.points())]
        return e.is_closed if e.dxftype() == "POLYLINE" else (e.closed or (len(pts) > 2 and pts[0] == pts[-1]))

    clouds = sum(1 for e in msp.query("LWPOLYLINE POLYLINE[layer=='A-REVS']") if closed(e))
    flat = flatten(d)
    plans = {dr["id"][5:] for dr in d.get("drawings", []) if dr["id"].startswith("plan:")}
    items = sum(len(flat[n][k]) for n in plans if n in flat for k in ("rooms", "openings", "stairs", "furniture"))
    return {"clouds": clouds, "table_items": items, "share": round(clouds / items, 3) if items else None}


def score(dxf, params, build=None, log=None):
    got = {"A1": run_checker([SCRIPTS / "params_check.py", params]),
           "A2": run_checker([SCRIPTS / "dxf_check.py", dxf]),
           "A3": run_checker([SCRIPTS / "plan_check.py", dxf, params]),
           "A4": run_checker([SCRIPTS / "luat_check.py", dxf, params]),
           "A5": run_audit(dxf)}
    table_ok = got["A1"]["data"] is not None and not got["A1"]["data"]["errors"]
    rep = tally({k: score_item(k, v, table_ok) for k, v in got.items()}, build)
    # A report beside the score: it may fail, the score stays.
    h = {}
    if table_ok:
        try:
            h = handed_back(dxf, params)
        except Exception as err:  # noqa: BLE001
            h = {"error": f"không đếm được đám mây: {err}"}
    if log:
        h["log"] = handed_back_log(log)
        n = h.get("table_items")
        h["log_share"] = round(h["log"]["undrawn"] / n, 3) if n else None
        h["text_share"] = round(h["log"]["text_no_spot"] / n, 3) if n else None
    if h:
        rep["handed_back"] = h
    return rep


def tally(items, build=None):
    """Part A as raw points over the points of the items that ran. Never
    rescaled: two scores compare only when their maxima match."""
    ran = {k: v for k, v in items.items() if v[0] is not None}
    rep = {"items": {k: {"title": ITEMS[k][0], "points": v[0], "of": ITEMS[k][1], "why": v[1]}
                     for k, v in items.items()},
           "A": sum(v[0] for v in ran.values()), "of": sum(ITEMS[k][1] for k in ran)}
    if build:
        rep["outside_library"] = outside_library(build)
    return rep


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("dxf")
    ap.add_argument("params")
    ap.add_argument("--build")
    ap.add_argument("--build-log", help='output of the last build.py run, with its "Chưa vẽ" list')
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    try:
        if a.build:
            pathlib.Path(a.build).read_text(encoding="utf-8")
        if a.build_log:
            read_log(a.build_log)
        json.loads(pathlib.Path(a.params).read_text(encoding="utf-8"))
        import ezdxf  # noqa: E402
        ezdxf.readfile(a.dxf)
    except Exception as err:  # noqa: BLE001  an unreadable input is the caller's error, not a score
        print(f"không đọc được: {err}", file=sys.stderr)
        return 2
    rep = score(a.dxf, a.params, a.build, a.build_log)
    if a.json:
        json.dump(rep, sys.stdout, ensure_ascii=False, indent=1)
        print()
        return 0
    for k, it in rep["items"].items():
        pts = "bỏ qua" if it["points"] is None else f"{it['points']:g}/{it['of']}"
        print(f"{k}  {pts:>7}  {it['title']}: {it['why']}")
    print(f"A = {rep['A']:g}/{rep['of']}" + ("" if rep["of"] == 25 else " (có mục chưa chạy: chỉ so với lần chấm cùng mẫu số)"))
    if "handed_back" in rep:
        h = rep["handed_back"]
        pct = lambda v: "—" if v is None else f"{v:.0%}"  # noqa: E731
        if "error" in h:
            print(f"Bị giao lại: {h['error']}")
        elif "clouds" in h:
            print(f"Bị giao lại (không tính điểm): {h['clouds']} đám mây \"chưa vẽ\"; bảng số đòi vẽ "
                  f"{h['table_items']} thứ (so: {pct(h['share'])}; đám mây có thể đánh dấu cả thứ ngoài bảng)")
        else:
            print("Bị giao lại: bảng số hỏng nên không đếm được thứ bảng số đòi vẽ; chỉ đọc danh sách của build.py")
        if "log" in h:
            g = h["log"]
            print(f"Danh sách \"Chưa vẽ\" của build.py: {g['listed']} dòng. Phần chưa vẽ: {g['undrawn']} "
                  f"({g['drawings']} là cả một hình), {pct(h['log_share'])} số thứ bảng số đòi vẽ. Chữ không có "
                  f"chỗ: {g['text_no_spot']} ({pct(h['text_share'])}). Số lấy mặc định: {g['assumed']}. "
                  f"Ghi chú diện tích: {g['area_note']}. Cần người xem trong AutoCAD: {g['needs_eye']}.")
    if "outside_library" in rep:
        o = rep["outside_library"]
        print(f"Ngoài thư viện (không tính điểm): {o['changed_or_added']}/{o['lines']} dòng build.py "
              f"khác lib/build_mau.py ({o['share']:.0%}); {o['library_lines_dropped']} dòng của thư viện bị bỏ")
    return 0


if __name__ == "__main__":
    sys.exit(main())
