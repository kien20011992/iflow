#!/usr/bin/env python3
"""review.py RESULT.json [-o review.html] — one page a person can review after

    claude plugin eval . --case 'cad-*' --keep-temp --json RESULT.json ...

The built-in report shows the graders' verdicts. This page adds what each run
produced — the whole reply, every file written, every edit made — read from
the run's trace, so run it before the kept sandbox directories are deleted.
It also runs tests/cad.sh and shows its output. Standard library only; the
page follows the Artifact page contract, so it can be published as it is.
"""
import argparse
import base64
import html
import json
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
KIND = {"llm": "Claude chấm theo tiêu chí", "regex": "khớp mẫu chữ",
        "tool_used": "đếm lần gọi công cụ", "tool_order": "thứ tự gọi công cụ",
        "file_exists": "file có hay không", "baseline": "so với bản mẫu"}
esc = html.escape


def frontmatter(path):
    """The single-line keys of a case's prompt.md; enough for its two notes."""
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return {}
    if not text.startswith("---"):
        return {}
    pairs = (line.partition(":") for line in text.split("---", 2)[1].splitlines())
    return {k.strip(): v.strip().strip('"') for k, sep, v in pairs if sep and k[:1].strip()}


def read_trace(path):
    """(final reply, [Write/Edit tool_use blocks], {tool_use_id: refused?}) or None."""
    reply, calls, refused = "", [], {}
    try:
        lines = pathlib.Path(path).read_text(encoding="utf-8").splitlines()
    except (OSError, TypeError):
        return None
    for line in lines:
        try:
            row = json.loads(line)
        except ValueError:
            continue
        if row.get("type") == "result":
            reply = row.get("result") or reply
        message = row.get("message")
        content = message.get("content") if isinstance(message, dict) else None
        for block in content if isinstance(content, list) else []:
            if not isinstance(block, dict):
                continue
            if block.get("type") == "tool_use" and block.get("name") in ("Write", "Edit"):
                calls.append(block)
            elif block.get("type") == "tool_result":
                refused[block.get("tool_use_id")] = bool(block.get("is_error"))
    return reply, calls, refused


def short(path):
    for mark in ("/home/cwd/", "/cwd/"):
        if mark in path:
            return path.split(mark, 1)[1]
    return path


def pill(ok, yes="đạt", no="không đạt"):
    return f'<span class="pill {"good" if ok else "bad"}">{yes if ok else no}</span>'


def file_block(call, refused):
    data = call.get("input", {})
    path, name = short(data.get("file_path", "?")), call.get("name")
    note = ' <span class="pill bad">bị từ chối, không ghi được</span>' if refused.get(call.get("id")) else ""
    head = f'<figcaption><code>{esc(path)}</code> · {"ghi mới" if name == "Write" else "sửa"}{note}</figcaption>'
    if name == "Edit":
        body = (f'<div class="pair"><div><p class="label">Trước</p><pre>{esc(data.get("old_string", ""))}</pre></div>'
                f'<div><p class="label">Sau</p><pre>{esc(data.get("new_string", ""))}</pre></div></div>')
    elif path.endswith(".svg") and "<svg" in data.get("content", ""):
        uri = base64.b64encode(data["content"].encode()).decode()
        body = f'<div class="scroll"><img alt="Sơ đồ {esc(path)}" src="data:image/svg+xml;base64,{uri}"></div>'
    else:
        body = f'<pre>{esc(data.get("content", ""))}</pre>'
    return f'<figure class="file">{head}{body}</figure>'


def grader_item(result, config):
    kind = KIND.get(config.get("type"), config.get("type", ""))
    votes = result.get("judgeVotes")
    why = f"{sum(votes)}/{len(votes)} phiếu đạt" if votes else result.get("explanation", "")
    rubric = config.get("graderMarkdown") or json.dumps(config.get("config", {}), ensure_ascii=False)
    return (f'<li>{pill(result.get("passed"))} <strong>{esc(result.get("name", ""))}</strong>'
            f' <span class="muted">{esc(kind)} · {esc(why)}</span>'
            f'<details class="rubric"><summary>Tiêu chí</summary><p>{esc(rubric)}</p></details></li>')


def run_block(run, number, total, configs):
    parts = []
    if total > 1:
        parts.append(f'<h4>Lần chạy {number} {pill(run.get("passed"))}</h4>')
    if run.get("error"):
        parts.append(f'<p class="note bad">Lần chạy lỗi: {esc(str(run["error"]))}</p>')
    items = "".join(grader_item(g, configs.get(g.get("name"), {})) for g in run.get("graders", []))
    parts.append(f'<h4>Từng phép chấm</h4><ul class="graders">{items}</ul>')
    trace = read_trace(run.get("tracePath"))
    if trace is None:
        parts.append('<p class="note">Không còn file ghi lại lần chạy. Chạy lại với <code>--keep-temp</code> '
                     'rồi dựng trang này ngay sau đó.</p>')
    else:
        reply, calls, refused = trace
        parts.append(f'<h4>Claude trả lời</h4><div class="reply">{esc(reply) or "(không có lời đáp)"}</div>')
        files = "".join(file_block(c, refused) for c in calls) or '<p class="muted">Không ghi và không sửa file nào.</p>'
        parts.append(f'<h4>File đã ghi và đã sửa</h4>{files}')
    return "".join(parts)


def case_block(case, root):
    notes = frontmatter(root / case.get("dir", "") / "prompt.md")
    runs = case.get("arms", {}).get("with", [])
    configs = {g.get("name"): g for g in case.get("graders", [])}
    passed = bool(runs) and all(r.get("passed") for r in runs)
    score = case.get("aggregates", {}).get("score", 0)
    expect = notes.get("expected_outcome") or notes.get("description", "")
    body = "".join(run_block(r, i + 1, len(runs), configs) for i, r in enumerate(runs))
    return (f'<details class="case" id="{esc(case["name"])}"{"" if passed else " open"}>'
            f'<summary><span class="name">{esc(case["name"])}</span> {pill(passed, "đạt hết", "có chỗ hỏng")}'
            f' <span class="muted">{score:.0%} phép chấm đạt</span></summary>'
            f'<dl class="block"><dt>Người dùng gõ</dt><dd>{esc(case.get("promptMarkdown", "").strip())}</dd>'
            f'<dt>Phải xảy ra, và người duyệt cần xem</dt><dd>{esc(expect)}</dd></dl>{body}</details>')


def free_checks(root):
    script = root / "tests" / "cad.sh"
    if not script.exists():
        return None
    done = subprocess.run(["bash", str(script)], capture_output=True, text=True)
    return done.returncode == 0, (done.stdout + done.stderr).strip()


STYLE = """
/* Layout: one reading column. The register of cases comes first, each case's sheet below it. */
:root {
  --bg: #f3f5f8; --surface: #ffffff; --paper: #ffffff; --fg: #16202a; --muted: #586674; --line: #d3dae1; --code: #edf0f4;
  --accent: #1c5ea6; --good: #17734a; --good-bg: #e1f2e8; --bad: #b0271f; --bad-bg: #fbe8e6;
  --display: "Space Grotesk", "Segoe UI", system-ui, sans-serif;
  --body: Inter, "Segoe UI", system-ui, sans-serif;
  --mono: ui-monospace, "SF Mono", Menlo, Consolas, monospace;
}
@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) {
  --bg: #0f141a; --surface: #171e26; --fg: #e5eaf0; --muted: #9ba8b5; --line: #2a3440; --code: #1c242e;
  --accent: #82b4ec; --good: #62cf95; --good-bg: #143324; --bad: #ff8d83; --bad-bg: #3b1b18; color-scheme: dark } }
:root[data-theme="dark"] {
  --bg: #0f141a; --surface: #171e26; --fg: #e5eaf0; --muted: #9ba8b5; --line: #2a3440; --code: #1c242e;
  --accent: #82b4ec; --good: #62cf95; --good-bg: #143324; --bad: #ff8d83; --bad-bg: #3b1b18; color-scheme: dark }
body { background: var(--bg); color: var(--fg); font: 15px/1.55 var(--body); padding-block: 28px 56px;
  padding-left: max(16px, env(safe-area-inset-left, 0px)); padding-right: max(16px, env(safe-area-inset-right, 0px)); }
.wrap { max-width: 960px; margin-inline: auto; display: grid; gap: 28px; }
.wrap > * { min-width: 0; }
h1, h2, h3, h4 { font-family: var(--display); margin: 0; text-wrap: balance; line-height: 1.2; }
h1 { font-size: 28px; } h2 { font-size: 19px; } h4 { font-size: 14px; margin-top: 18px; }
p { margin: 0; } a { color: var(--accent); }
.muted { color: var(--muted); } .label { font-size: 12px; color: var(--muted); letter-spacing: .04em; text-transform: uppercase; }
header, section { display: grid; gap: 10px; }
.tiles { display: grid; grid-template-columns: repeat(auto-fit, minmax(210px, 1fr)); gap: 12px; }
.tile { background: var(--surface); border: 1px solid var(--line); padding: 14px 16px; display: grid; gap: 2px; }
.tile strong { font: 600 26px/1.2 var(--display); font-variant-numeric: tabular-nums; }
.scroll { overflow-x: auto; }
table { border-collapse: collapse; width: 100%; background: var(--surface); }
th, td { border: 1px solid var(--line); padding: 8px 10px; text-align: left; vertical-align: top; }
th { font: 600 12px var(--body); color: var(--muted); letter-spacing: .04em; text-transform: uppercase; }
td.num { font-variant-numeric: tabular-nums; white-space: nowrap; }
.pill { display: inline-block; padding: 1px 8px; border: 1px solid currentColor; font-size: 12px; font-weight: 600; white-space: nowrap; }
.pill.good { color: var(--good); background: var(--good-bg); } .pill.bad { color: var(--bad); background: var(--bad-bg); }
.note { padding: 8px 12px; border: 1px solid var(--line); background: var(--surface); } .note.bad { color: var(--bad); }
details.case { background: var(--surface); border: 1px solid var(--line); padding: 0 16px 16px; }
details.case > summary { cursor: pointer; padding: 14px 0; display: flex; flex-wrap: wrap; gap: 8px 12px; align-items: baseline; }
summary:focus-visible { outline: 2px solid var(--accent); outline-offset: 2px; }
details.case > summary::before { content: "▸"; color: var(--muted); }
details.case[open] > summary::before { content: "▾"; }
.name { font: 600 17px var(--display); }
dl.block { display: grid; grid-template-columns: minmax(120px, 190px) minmax(0, 1fr); margin: 0; border: 1px solid var(--line); }
dl.block dt, dl.block dd { margin: 0; padding: 8px 10px; border-bottom: 1px solid var(--line); }
dl.block dt { font-size: 12px; color: var(--muted); letter-spacing: .04em; text-transform: uppercase; border-right: 1px solid var(--line); }
dl.block dt:last-of-type, dl.block dd:last-of-type { border-bottom: 0; }
@media (max-width: 560px) { dl.block { grid-template-columns: 1fr; } dl.block dt { border-right: 0; border-bottom: 0; padding-bottom: 0; } }
ul.graders { list-style: none; margin: 8px 0 0; padding: 0; display: grid; gap: 8px; }
details.rubric { margin: 4px 0 0; } details.rubric summary { cursor: pointer; font-size: 13px; color: var(--muted); }
details.rubric p { font-size: 13px; color: var(--muted); max-width: 70ch; }
.reply, pre { margin: 8px 0 0; padding: 12px; background: var(--code); border: 1px solid var(--line);
  white-space: pre-wrap; overflow-wrap: anywhere; max-height: 460px; overflow: auto; }
pre { font: 13px/1.5 var(--mono); } code { font: 13px var(--mono); overflow-wrap: anywhere; }
figure.file { margin: 10px 0 0; } figure.file img { background: var(--paper); border: 1px solid var(--line); }
.pair { display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 10px; } .pair > div { min-width: 0; }
ul.plain { margin: 0; padding-left: 20px; max-width: 72ch; }
"""

UNTOUCHED = [
    "Phần vẽ bằng CADCraft. Các ca thử chạy không có lệnh shell, nên không lần nào dựng ra file DXF.",
    "Một file do skill tạo, mở trong AutoCAD thật. Việc này cần một kiến trúc sư và phiếu duyệt bản vẽ.",
    "Hội thoại nhiều lượt. Mỗi ca chỉ có một lượt, các ca nối tiếp dùng một dự án dựng sẵn.",
    "Tra cứu trên mạng. Các ca thử chạy không có mạng, nên chỉ thử được việc Claude nói thật về mức chắc.",
]


def page(result, checks):
    cases = result.get("cases", [])
    total = result.get("aggregates", {})
    root = pathlib.Path(result.get("suite", {}).get("root", ROOT))
    rows = "".join(
        f'<tr><td><a href="#{esc(c["name"])}">{esc(c["name"])}</a></td>'
        f'<td>{esc(frontmatter(root / c.get("dir", "") / "prompt.md").get("description", ""))}</td>'
        f'<td class="num">{c.get("aggregates", {}).get("score", 0):.0%}</td>'
        f'<td>{pill(all(r.get("passed") for r in c.get("arms", {}).get("with", [])) and bool(c.get("arms", {}).get("with")), "đạt hết", "có chỗ hỏng")}</td></tr>'
        for c in cases)
    if checks is None:
        free_tile, free_body = "không chạy", '<p class="muted">Không tìm thấy tests/cad.sh.</p>'
    else:
        free_tile = re.sub(r"(\d+) passed, (\d+) failed, (\d+) skipped", r"\1 đạt, \2 hỏng, \3 bỏ qua",
                           checks[1].splitlines()[-1] if checks[1] else "không có kết quả")
        free_body = f"<pre>{esc(checks[1])}</pre>"
    minutes = result.get("durationSeconds", 0) / 60
    return f"""<title>Kết quả thử i:cad</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&family=Space+Grotesk:wght@600&display=swap">
<style>{STYLE}</style>
<div class="wrap">
<header>
  <h1>Kết quả thử i:cad</h1>
  <p class="muted">Chạy lúc {esc(str(result.get("startedAt", "?"))[:16].replace("T", " "))} UTC ·
  Claude Code {esc(str(result.get("claudeVersion", "?")))} ·
  {len(cases)} ca, mỗi ca {max((len(c.get("arms", {}).get("with", [])) for c in cases), default=0)} lần chạy</p>
</header>
<div class="tiles">
  <div class="tile"><span class="label">Hành vi trong hội thoại</span>
    <strong>{total.get("casesPassed", 0)}/{total.get("casesTotal", len(cases))} ca đạt hết</strong>
    <span class="muted">{total.get("overallScore", 0):.0%} phép chấm đạt</span></div>
  <div class="tile"><span class="label">Kiểm không tốn tiền</span>
    <strong>{esc(free_tile)}</strong>
    <span class="muted">cấu trúc skill và trình kiểm DXF</span></div>
  <div class="tile"><span class="label">Lần chạy này</span>
    <strong>${result.get("costUsd", 0):.2f}</strong>
    <span class="muted">{minutes:.0f} phút</span></div>
</div>
<section>
  <h2>Các ca thử hành vi</h2>
  <div class="scroll"><table>
    <tr><th>Ca</th><th>Thử điều gì</th><th>Điểm</th><th>Kết quả</th></tr>{rows}
  </table></div>
  <p class="muted">Một ca đạt khi mọi phép chấm của nó đạt. Phép chấm bằng máy đếm việc Claude đã làm.
  Phép chấm bằng tiêu chí do một Claude khác bỏ ba phiếu, hai phiếu đạt là đạt.</p>
</section>
<section>
  <h2>Từng ca: Claude đã nói gì và ghi gì</h2>
  {"".join(case_block(c, root) for c in cases)}
</section>
<section>
  <h2>Kiểm không tốn tiền</h2>
  {free_body}
</section>
<section>
  <h2>Bộ thử này chưa chạm tới</h2>
  <ul class="plain">{"".join(f"<li>{esc(line)}</li>" for line in UNTOUCHED)}</ul>
</section>
</div>
"""


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("result", help="aggregate-result.json, or the file given to --json")
    ap.add_argument("-o", "--output", help="default: review.html next to the result file")
    args = ap.parse_args()
    source = pathlib.Path(args.result)
    try:
        result = json.loads(source.read_text(encoding="utf-8"))
    except (OSError, ValueError) as err:
        print(f"không đọc được {source}: {err}", file=sys.stderr)
        return 2
    out = pathlib.Path(args.output) if args.output else source.with_name("review.html")
    out.write_text(page(result, free_checks(ROOT)), encoding="utf-8")
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
