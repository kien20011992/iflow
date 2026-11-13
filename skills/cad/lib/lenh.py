"""Command list for one `cadcraft-cli run`: every drawing function appends
CADCraft commands here instead of drawing, so the functions can be tested
without CADCraft. Coordinates are plan coordinates in mm; `origin` shifts a
whole plan to its place in model space (references/bang-so.md).
"""
import json
import pathlib

BLOCKS = pathlib.Path(__file__).resolve().parents[1] / "assets" / "blocks"
STYLE = "VN"
TEXT_FACTOR = 0.7  # estimated width of one character, in text heights (as dxf_check.py)

# Paper sizes in mm; multiply by the scale for model units (references/ve.md).
PAPER = {"text": 2.5, "room": 3.5, "title": 5.0, "grid_text": 3.5, "grid_circle": 8.0,
         "tag": 6.0, "first_dim": 15.0, "dim_gap": 8.0, "margin": 2.0}


def text_width(s, h):
    return len(s) * TEXT_FACTOR * h


class Lenh:
    def __init__(self, scale, blocks=BLOCKS):
        self.scale = scale
        self.cmds = []
        self.origin = (0.0, 0.0)
        self._layer = None
        self._blocks = pathlib.Path(blocks)
        self._loaded = set()

    def size(self, key):
        return PAPER[key] * self.scale

    def p(self, pt):
        return [round(pt[0] + self.origin[0], 3), round(pt[1] + self.origin[1], 3)]

    def c(self, cid, **kw):
        self.cmds.append(f"{cid} {json.dumps(kw, ensure_ascii=False)}")

    def layer(self, name):
        if name != self._layer:
            self.c("layer.current", name=name)
            self._layer = name

    def pline(self, pts, layer, closed=True):
        self.layer(layer)
        self.c("pline", vertices=[self.p(q) for q in pts], closed=closed)

    def line(self, a, b, layer):
        self.layer(layer)
        self.c("line", points=[self.p(a), self.p(b)])

    def solid(self, pts, layer):
        self.pline(pts, layer)
        self.c("hatch", handles=["{last}"], pattern="SOLID")

    def circle(self, centre, radius, layer, linetype=None):
        self.layer(layer)
        self.c("circle", center=self.p(centre), radius=radius)
        if linetype:
            self.c("properties.set", handles=["{last}"], linetype=linetype)

    def mtext(self, at, text, height, layer, attach=5, rotation=0):
        self.layer(layer)
        kw = dict(at=self.p(at), text=text, height=round(height, 3), attach=attach, style=STYLE)
        if rotation:
            kw["rotation"] = rotation
        self.c("mtext", **kw)

    def insert(self, name, at, layer, rotation=0, scale=None, attribs=None):
        """Insert a symbol of assets/blocks/, loading its file the first time."""
        self.layer(layer)
        kw = dict(name=name, at=self.p(at), rotation=round(rotation % 360, 6))
        if name not in self._loaded:
            kw["file"] = str(self._blocks / f"{name}.dxf")
            self._loaded.add(name)
        if scale is not None:
            kw["scale"] = scale
        if attribs:
            kw["attribs"] = attribs
        self.c("insert", **kw)

    def dim(self, p1, p2, at, rotation, move=None):
        self.layer("A-DIMS")
        self.c("dimlinear", p1=self.p(p1), p2=self.p(p2), at=self.p(at), rotation=rotation)
        if move is not None:
            self.c("dimtedit", handles=["{last}"], at=self.p(move))

    def revcloud(self, p1, p2):
        self.layer("A-REVS")
        self.c("revcloud", p1=self.p(p1), p2=self.p(p2), arcLength=round(3 * self.scale))

    def setup(self):
        """Per-drawing settings that depend on the scale."""
        s = self.scale
        self.c("ltscale", scale=s / 5)
        self.c("dimstyle", name="KT", current=True, DIMSCALE=s, DIMTXT=PAPER["text"], DIMTSZ=1.0,
               DIMEXO=1.5, DIMEXE=1.5, DIMTAD=1, DIMGAP=0.8, DIMTMOVE=2, DIMTXSTY=STYLE,
               DIMDEC=0, DIMTIH=0, DIMTOH=0)
