"""Run one CADCraft session: open the template, play the command list, save
DXF 2018, and optionally plot PNG views. Standard library only."""
import json
import pathlib
import shutil
import subprocess

TEMPLATE = pathlib.Path(__file__).resolve().parents[1] / "assets" / "mau.dxf"


def find_cli():
    for name in ("cadcraft-cli", "cadcraft.cli"):
        path = shutil.which(name)
        if path:
            return path
    return None


CHUNK = 500_000  # bytes of --cmd text per process, well under the kernel's argument limit


def chunks(cmds, limit=CHUNK):
    """Split the command list into runs of at most `limit` bytes. A command that
    refers to the object made just before it ("{last}") stays in the same run,
    because the placeholder only works inside one run."""
    out, cur, size = [], [], 0
    for c in cmds:
        if cur and size + len(c) > limit and "{last}" not in c:
            out.append(cur)
            cur, size = [], 0
        cur.append(c)
        size += len(c)
    out.append(cur)
    return out


def run(cmds, out_dxf, pngs=(), template=TEMPLATE, cli=None):
    """pngs: [(path, [[x0, y0], [x1, y1]], landscape)] windows in model space.
    A long list runs as several CADCraft processes, each reopening the file the
    one before saved. Returns (exit code, stdout, stderr); the DXF exists only
    when the code is 0."""
    cli = cli or find_cli()
    if cli is None:
        raise FileNotFoundError("không thấy cadcraft-cli trên máy")
    out_dxf = pathlib.Path(out_dxf)
    part = out_dxf.with_name(out_dxf.stem + ".part.dxf")
    save = lambda p: "saveas " + json.dumps({"path": str(p), "version": 2018, "binary": False})  # noqa: E731
    groups = chunks(cmds)
    logs = []
    for k, group in enumerate(groups):
        last = k == len(groups) - 1
        args = [cli, "run", "--metric"]
        args += ["--cmd", f"new {json.dumps({'template': str(template)})}"] if k == 0 else [str(part)]
        for c in group:
            args += ["--cmd", c]
        args += ["--cmd", save(out_dxf if last else part)]
        if last:
            for path, window, landscape in pngs:
                args += ["--cmd", "plot " + json.dumps({
                    "path": str(path), "device": "CADCraft PNG", "fit": True, "plotArea": "window",
                    "window": window, "lineweights": True, "landscape": landscape})]
        r = subprocess.run(args, capture_output=True, text=True)
        logs.append(r)
        if r.returncode != 0:
            break
    if part.exists():
        part.unlink()
    return r.returncode, "".join(x.stdout for x in logs), "".join(x.stderr for x in logs)
