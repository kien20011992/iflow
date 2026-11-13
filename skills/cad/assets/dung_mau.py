#!/usr/bin/env python3
"""dung_mau.py [CADCRAFT] — rebuild the skill's template drawing and symbol
blocks through CADCraft, next to this script:

  mau.dxf           layers, linetypes, the text style: what every drawing
                    starts from (an office replaces it with its own template)
  blocks/*.dxf      one symbol per file; an architect can edit them in AutoCAD

Standard library only; needs cadcraft-cli (or the path given). Block frames:
x runs along the wall from its `from` end to its `to` end, y to its left.

  CUA-<w>-T  door leaf of width w hinged at the origin, closed along +x,
             opening to +y (arc 0..90 degrees)
  CUA-<w>-P  the same leaf opening to -y (arc 270..360 degrees)
  CUA-SO     window, a unit square centred on the origin: insert it scaled
             to [width, wall thickness]
  CUA-CUON   rolling shutter, unit square like CUA-SO

Every opening block carries a hidden attribute ID (references/bang-so.md).
"""
import json
import pathlib
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
DOOR_WIDTHS = (600, 700, 800, 900, 1000, 1200)
FONT = "arial.ttf"
STYLE = "VN"

# name, colour, linetype, lineweight (mm) — the default set in references/ve.md
LAYERS = [
    ("A-GRID", "Red", "CENTER", 0.18), ("A-WALL", "White", "Continuous", 0.5),
    ("A-COLS", "White", "Continuous", 0.5), ("A-DOOR", "Green", "Continuous", 0.25),
    ("A-GLAZ", "Cyan", "Continuous", 0.25), ("A-STRS", "Yellow", "Continuous", 0.25),
    ("A-FLOR", "Blue", "Continuous", 0.18), ("A-OVHD", "Magenta", "HIDDEN", 0.18),
    ("A-FURN", "Blue", "Continuous", 0.13), ("A-PATT", "Magenta", "Continuous", 0.13),
    ("A-DIMS", "Red", "Continuous", 0.18), ("A-TEXT", "White", "Continuous", 0.18),
    ("A-FUTR", "Magenta", "HIDDEN", 0.18), ("A-RAIL", "Yellow", "Continuous", 0.25),
    ("S-CUTS", "White", "Continuous", 0.5), ("A-ELEV", "Blue", "Continuous", 0.18),
    ("C-TOPO", "Green", "Continuous", 0.35), ("A-ANNO", "White", "Continuous", 0.18),
    ("C-PROP", "Green", "PHANTOM", 0.25), ("X-AREA", "Yellow", "Continuous", None),
    ("A-REVS", "Magenta", "Continuous", 0.25), ("A-DEMO", "Yellow", "HIDDEN", 0.25),
]


def cmd(cid, **kw):
    return ["--cmd", f"{cid} {json.dumps(kw, ensure_ascii=False)}"]


def run(cli, args):
    r = subprocess.run([cli, "run", "--metric", *args], capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit(f"cadcraft-cli thất bại ({r.returncode}): {r.stderr.strip()[-800:]}")


def save(path):
    return cmd("saveas", path=str(path), version=2018, binary=False)


def units():
    return cmd("units", lunits=2, luprec=0, insunits=4)


def main(argv):
    cli = argv[1] if len(argv) > 1 else "cadcraft-cli"
    blocks = HERE / "blocks"
    blocks.mkdir(exist_ok=True)

    args = units() + cmd("linetype", load="*")
    for name, colour, lt, lw in LAYERS:
        kw = dict(name=name, color=colour, linetype=lt)
        if lw:
            kw["lineweight"] = lw
        args += cmd("layer.new", **kw)
    args += cmd("layer.set", name="X-AREA", plot=False)
    args += cmd("style", name=STYLE, font=FONT, current=True)
    args += cmd("layer.current", name="A-TEXT") + save(HERE / "mau.dxf")
    run(cli, args)

    def symbol(name, body):
        id_tag = cmd("attdef", tag="ID", at=[0, 0], height=0.1 if name in ("CUA-SO", "CUA-CUON") else 100,
                     invisible=True)
        run(cli, units() + body + id_tag + save(blocks / f"{name}.dxf"))

    for w in DOOR_WIDTHS:
        symbol(f"CUA-{w}-T", cmd("line", points=[[0, 0], [0, w]])
               + cmd("arc", center=[0, 0], radius=w, start=0, end=90))
        symbol(f"CUA-{w}-P", cmd("line", points=[[0, 0], [0, -w]])
               + cmd("arc", center=[0, 0], radius=w, start=270, end=360))
    # Window: jambs and a double glazing line across the wall.
    symbol("CUA-SO", cmd("line", points=[[-0.5, -0.5], [-0.5, 0.5]])
           + cmd("line", points=[[0.5, -0.5], [0.5, 0.5]])
           + cmd("line", points=[[-0.5, -0.08], [0.5, -0.08]])
           + cmd("line", points=[[-0.5, 0.08], [0.5, 0.08]]))
    # Rolling shutter: jambs and two thin lines in the middle of the wall.
    symbol("CUA-CUON", cmd("line", points=[[-0.5, -0.5], [-0.5, 0.5]])
           + cmd("line", points=[[0.5, -0.5], [0.5, 0.5]])
           + cmd("line", points=[[-0.5, -0.1], [0.5, -0.1]])
           + cmd("line", points=[[-0.5, 0.1], [0.5, 0.1]]))
    # Furniture and fixtures, centred on the origin; the side against the wall is +y.
    def rect(w, h, cx=0, cy=0):
        return cmd("pline", vertices=[[cx - w / 2, cy - h / 2], [cx + w / 2, cy - h / 2],
                                      [cx + w / 2, cy + h / 2], [cx - w / 2, cy + h / 2]], closed=True)

    def plain(name, body):
        run(cli, units() + body + save(blocks / f"{name}.dxf"))

    plain("GIUONG-DOI", rect(1600, 2000) + rect(650, 350, -375, 750) + rect(650, 350, 375, 750)
          + cmd("line", points=[[-800, 450], [800, 450]]))
    plain("GIUONG-DON", rect(1000, 2000) + rect(650, 350, 0, 750) + cmd("line", points=[[-500, 450], [500, 450]]))
    plain("SOFA-3", rect(2000, 800) + cmd("line", points=[[-1000, 200], [1000, 200]])
          + cmd("line", points=[[-800, -400], [-800, 200]]) + cmd("line", points=[[800, -400], [800, 200]]))
    plain("BAN-AN-6", rect(900, 1400) + rect(400, 400, -650, -450) + rect(400, 400, -650, 0)
          + rect(400, 400, -650, 450) + rect(400, 400, 650, -450) + rect(400, 400, 650, 0)
          + rect(400, 400, 650, 450))
    plain("BON-CAU", rect(400, 200, 0, 225) + cmd("circle", center=[0, -75], radius=180))
    plain("LAVABO", rect(500, 400) + cmd("circle", center=[0, -20], radius=140))
    plain("CHAU-RUA-BEP", rect(800, 450) + rect(340, 330, -190, -20) + rect(340, 330, 190, -20))
    plain("BAN-BEP", rect(600, 2000))
    plain("MAY-GIAT", rect(600, 600) + cmd("circle", center=[0, 0], radius=230))
    for bak in list(HERE.glob("*.bak")) + list(blocks.glob("*.bak")):
        bak.unlink()  # CADCraft keeps the previous file as .bak when it overwrites
    print(f"mau.dxf và {len(list(blocks.glob('*.dxf')))} block ở {HERE}")


if __name__ == "__main__":
    main(sys.argv)
