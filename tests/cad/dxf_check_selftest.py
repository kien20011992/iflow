#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# dependencies = ["ezdxf>=1.3"]
# ///
"""Self-test of skills/cad/scripts/dxf_check.py: build one sound drawing and
one copy per planted defect, and require the checker to stay quiet on the
first and to name exactly the planted defect on each of the others.

Run: uv run tests/cad/dxf_check_selftest.py
"""
import pathlib
import sys
import tempfile

import ezdxf

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "skills/cad/scripts"))
sys.dont_write_bytecode = True  # leave no __pycache__ inside the skill
from dxf_check import check  # noqa: E402


def drawing(defect=None):
    """A 4 x 3 m room with walls, an area label, two dimension rows."""
    doc = ezdxf.new("R2000" if defect == "version" else "R2018", units=4, setup=True)
    doc.header["$MEASUREMENT"] = 1
    for layer in ("A-WALL", "A-DIMS", "A-TEXT", "X-AREA"):
        doc.layers.add(layer)
    doc.styles.add("VN", font={"text": "txt.shx", "fontname": "Arial"}.get(defect, "arial.ttf"))
    style = doc.dimstyles.duplicate_entry("EZDXF", "A100")
    style.dxf.dimlfac, style.dxf.dimscale = 1, 100
    msp = doc.modelspace()

    outer = [(-220, -220), (4220, -220), (4220, 3220), (-220, 3220)]
    if defect == "walls":
        outer[2], outer[3] = outer[3], outer[2]  # a bow-tie crosses itself
    if defect == "touch":  # two wall masses meeting at one corner, in one outline
        outer = [(-220, -220), (0, -220), (0, 0), (220, 0), (220, 220), (0, 220), (0, 0), (-220, 0)]
    msp.add_lwpolyline(outer, close=True, dxfattribs={"layer": "A-WALL"})
    msp.add_lwpolyline([(0, 0), (4000, 0), (4000, 3000), (0, 3000)], close=True,
                       dxfattribs={"layer": "X-AREA"})
    label = "PHÒNG NGỦ\n15,00 m²" if defect == "areas" else "PHÒNG NGỦ\n12,00 m²"
    msp.add_mtext(label, dxfattribs={"layer": "A-TEXT", "style": "VN", "char_height": 250,
                                     "insert": (2000, 1500)})
    if defect == "onobjects":
        doc.layers.add("A-FURN")
        msp.add_lwpolyline([(1500, 1200), (2600, 1200), (2600, 2600), (1500, 2600)], close=True,
                           dxfattribs={"layer": "A-FURN"})
    # A light well around the label is a large outline: no clash by itself.
    doc.layers.add("A-FLOR")
    msp.add_lwpolyline([(400, 400), (3600, 400), (3600, 2700), (400, 2700)], close=True,
                       dxfattribs={"layer": "A-FLOR"})
    if defect == "edge":  # a railing line running through the label
        msp.add_line((1000, 1300), (3000, 1300), dxfattribs={"layer": "A-FLOR"})
    if defect == "onlines":  # a section cut drawn through the room name
        doc.layers.add("A-ANNO")
        msp.add_line((2400, -500), (2400, 3500), dxfattribs={"layer": "A-ANNO"})
    if defect == "clash":
        msp.add_mtext("GHI CHÚ", dxfattribs={"layer": "A-TEXT", "style": "VN", "char_height": 250,
                                            "insert": (2100, 1500)})
    if defect in ("leader", "leaderbad"):  # a small room labelled outside, by a leader
        msp.add_lwpolyline([(5000, 3500), (6000, 3500), (6000, 4500), (5000, 4500)], close=True,
                           dxfattribs={"layer": "X-AREA"})
        msp.add_mtext("VS\n" + ("2,00" if defect == "leaderbad" else "1,00") + " m²",
                      dxfattribs={"layer": "A-TEXT", "style": "VN", "char_height": 250,
                                  "insert": (7500, 5000)})
        msp.add_line((5500, 4000), (7400, 4800), dxfattribs={"layer": "A-TEXT"})
    if defect == "layer0":
        msp.add_line((0, 0), (100, 100))

    def dim(a, b, row, text="<>"):
        msp.add_linear_dim(base=(0, row), p1=(a, 0), p2=(b, 0), text=text, dimstyle="A100",
                           dxfattribs={"layer": "A-DIMS"}).render()

    dim(0, 2000, -800)
    dim(2000, 3500 if defect == "chain" else 4000, -800)
    dim(0, 4000, -1600, text="4500" if defect == "dims" else "<>")
    # A second floor beside the first shares the dimension rows; that is no gap.
    msp.add_lwpolyline([(10000, 0), (14000, 0), (14000, 3000), (10000, 3000)], close=True,
                       dxfattribs={"layer": "X-AREA"})
    msp.add_mtext("BẾP\n12,00 m²", dxfattribs={"layer": "A-TEXT", "style": "VN", "char_height": 250,
                                              "insert": (12000, 1500)})
    dim(10000, 12000, -800)
    dim(12000, 14000, -800)
    dim(10000, 14000, -1600)
    return doc


def main():
    failures = []
    with tempfile.TemporaryDirectory() as tmp:
        for defect in (None, "version", "text", "fontname", "walls", "touch", "clash", "onobjects", "edge", "onlines", "areas", "leader", "leaderbad", "layer0", "dims", "chain"):
            path = f"{tmp}/{defect or 'sound'}.dxf"
            drawing(defect).saveas(path)
            results = {r["id"]: r for r in check(path, "X-AREA", "A-WALL", "AC1032")}
            flagged = {k for k, r in results.items() if r["status"] in ("fail", "warn")}
            want = set() if defect in (None, "leader") else {{"chain": "dims", "fontname": "text", "touch": "walls", "edge": "onobjects", "leaderbad": "areas"}.get(defect, defect)}
            ok = flagged == want and (defect != "chain" or results["dims"]["status"] == "warn")
            print(f"{'ok  ' if ok else 'FAIL'} {defect or 'sound':8} flagged: {sorted(flagged) or '-'}")
            if not ok:
                failures.append(defect or "sound")
                for key in sorted(flagged ^ want):
                    print(f"       {key}: {results[key]['details']}")
    print(f"{16 - len(failures)} passed, {len(failures)} failed")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
