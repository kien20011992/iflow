#!/usr/bin/env bash
# tests/cad.sh — the free checks for i:cad: no API call, a few seconds.
#   1. the skill's files keep the contracts its eval fixtures and the
#      maintainers' notes in CLAUDE.md rely on;
#   2. every cross-file pointer resolves (check-pointers.sh);
#   3. the DXF checker still names each planted defect (needs uv or ezdxf);
#   4. the number-table checker passes the three sample tables and names
#      each planted defect;
#   5. the table-against-drawing checker passes a sound drawing and names
#      each planted defect (needs uv or ezdxf).
# Prints one line per check. Exit 0 = nothing failed.
set -u
root="$(cd "$(dirname "$0")/.." && pwd)"
skill="$root/skills/cad"
evals="$root/evals-cad"
pass=0; fail=0; skipped=0
ok()   { printf 'ok    %s\n' "$1"; pass=$((pass + 1)); }
bad()  { printf 'FAIL  %s\n' "$1"; fail=$((fail + 1)); }
skip() { printf 'skip  %s\n' "$1"; skipped=$((skipped + 1)); }
has()   { if grep -qE -- "$2" "$1"; then ok "$3"; else bad "$3"; fi; }
lacks() { if grep -qE -- "$2" "$1"; then bad "$3"; else ok "$3"; fi; }

tmp="$(mktemp -d)"; trap '/bin/rm -rf "$tmp"' EXIT
awk '/^---$/ { n++; next } n == 1' "$skill/SKILL.md" > "$tmp/frontmatter"

# --- the skill's own files
has   "$tmp/frontmatter" '^name: cad$' 'SKILL.md is named cad'
has   "$tmp/frontmatter" '^disable-model-invocation: true$' 'SKILL.md is user-invoked only'
lacks "$tmp/frontmatter" '^(context|allowed-tools):' 'SKILL.md runs in the main conversation, with no tool pre-grant'

size=$(wc -c < "$skill/SKILL.md")
if [ "$size" -le 18000 ]; then ok "SKILL.md is $size bytes, under the 18000 kept after a compaction"
else bad "SKILL.md is $size bytes, over 18000: its tail is cut after a compaction"; fi

rows=$(grep -cE '^\| [1-7] \| ' "$skill/SKILL.md")
if [ "$rows" -eq 7 ]; then ok 'SKILL.md lists seven products'
else bad "SKILL.md lists $rows products, expected seven"; fi

for word in missing done approved recheck skipped; do
  has "$skill/SKILL.md" "\`$word\`" "SKILL.md names the status $word"
done
for label in 'Next action:' 'Drawing tool:'; do
  has "$skill/SKILL.md" "$label" "SKILL.md uses the state label $label"
  has "$skill/references/ho-so.md" "^$label" "the project template carries $label"
done

if grep -q 'scripts/dxf_check\.py' "$skill/SKILL.md" && [ -f "$skill/scripts/dxf_check.py" ]
then ok 'SKILL.md points at the DXF checker, and the checker exists'
else bad 'SKILL.md and scripts/dxf_check.py no longer match'; fi

if grep -q '§' "$skill"/SKILL.md "$skill"/references/*.md; then
  bad 'a cad file points with §N, which check-pointers.sh reads as a numbered heading'
else ok 'no cad file points with §N'; fi

# Every row of the two tables of known CADCraft facts says where the fact came from.
unlabelled=$(awk '
  /^## / { on = ($0 ~ /^## (Bẫy đã biết|Rủi ro khi mở trong AutoCAD)/) }
  on && /^\| / && !/^\| Thứ / && !/^\|---/ && !/\[(tài liệu|bản [0-9.]+|chưa thử)/ { print }
' "$skill/references/cadcraft.md")
if [ -z "$unlabelled" ]; then ok 'every known-fact row in cadcraft.md carries its source label'
else bad "cadcraft.md has rows without a source label: $unlabelled"; fi

# --- the eval cases
fixture="$evals/cad-late-fact/fixture.sh"
has "$fixture" '^Next action:' 'the eval fixture carries Next action:'
has "$fixture" '^Drawing tool:' 'the eval fixture carries Drawing tool:'
odd=$(grep -E '^\| [0-9] \| ' "$fixture" | awk -F'|' '{ gsub(/ /, "", $4); print $4 }' |
  grep -vxE 'missing|done|approved|recheck|skipped')
if [ -z "$odd" ]; then ok 'the eval fixture uses only the five statuses'
else bad "the eval fixture uses unknown statuses: $odd"; fi
if diff <(grep -v 'fixture.sh is' "$fixture") <(grep -v 'fixture.sh is' "$evals/cad-what-if/fixture.sh") > /dev/null
then ok 'the two copies of the eval fixture are the same'
else bad 'cad-late-fact/fixture.sh and cad-what-if/fixture.sh have drifted apart'; fi
for prompt in "$evals"/cad-*/prompt.md; do
  case_name=$(basename "$(dirname "$prompt")")
  # A case that cannot write passes "no file" graders for the wrong reason.
  has "$prompt" '^allowed_tools: .*Write.*Edit' "$case_name may write and edit"
done

# --- pointers
if out=$(bash "$root/skills/flow/scripts/check-pointers.sh" "$skill" 2>&1); then ok "$out"
else bad "$out"; fi

# --- the two DXF-reading checkers against planted defects (need uv or ezdxf)
ezdxf_selftest() {  # $1 = label, $2 = self-test script
  local runner
  if command -v uv > /dev/null 2>&1; then runner=(uv run -q "$2")
  elif python3 -c 'import ezdxf' 2> /dev/null; then runner=(python3 "$2")
  else skip "$1 self-test: needs uv, or a python3 with ezdxf"; return; fi
  if out=$("${runner[@]}" 2>&1); then
    ok "$1 self-test: $(printf '%s\n' "$out" | tail -1)"
  else
    printf '%s\n' "$out" | sed 's/^/      /'
    bad "$1 self-test"
  fi
}
ezdxf_selftest 'DXF checker' "$root/tests/cad/dxf_check_selftest.py"
ezdxf_selftest 'table-against-drawing checker' "$root/tests/cad/plan_check_selftest.py"

# --- the number-table checker against the samples and planted defects
if out=$(python3 "$root/tests/cad/params_check_selftest.py" 2>&1); then
  ok "number-table checker self-test: $(printf '%s\n' "$out" | tail -1)"
else
  printf '%s\n' "$out" | sed 's/^/      /'
  bad 'number-table checker self-test'
fi

printf '%d passed, %d failed, %d skipped\n' "$pass" "$fail" "$skipped"
[ "$fail" -eq 0 ]
