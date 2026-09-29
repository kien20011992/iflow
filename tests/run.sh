#!/usr/bin/env bash
# tests/run.sh — regression tests for the i:flow resume hook, the dossier
# checker and the pointer checker. Every fixture is built in a throwaway temp directory;
# nothing outside it is touched. Exit 0 = every case passed.
set -u
export LC_ALL=C.UTF-8 # the hook caps lines by character, which needs UTF-8

root=$(cd "$(dirname "$0")/.." && pwd)
checker="$root/skills/flow/scripts/check-dossier.sh"
hook="$root/hooks/iflow-resume.sh"
skill="$root/skills/flow"
tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT
pass=0
fail=0

# mk <dossier-dir> — shape.md from stdin, plus one slice file per table row
mk() {
  mkdir -p "$1"
  cat > "$1/shape.md"
  grep -oE '^\| [0-9]{2} ' "$1/shape.md" | tr -dc '0-9\n' | while read -r nn; do
    : > "$1/slice-$nn-x.md"
  done
}

# check <name> <exit> <must-match> <must-not-match> -- <command…>
# An empty pattern skips that test; '.' as must-not-match means "no output".
check() {
  local name=$1 want=$2 has=$3 hasnt=$4 out rc why=""
  shift 5
  out=$("$@" 2>&1)
  rc=$?
  [ "$rc" -eq "$want" ] || why="exit $rc, want $want"
  if [ -n "$has" ] && ! printf '%s' "$out" | grep -qE -- "$has"; then
    why="${why:+$why; }missing /$has/"
  fi
  if [ -n "$hasnt" ] && printf '%s' "$out" | grep -qE -- "$hasnt"; then
    why="${why:+$why; }unwanted /$hasnt/"
  fi
  if [ -z "$why" ]; then
    pass=$((pass + 1))
  else
    fail=$((fail + 1))
    printf 'FAIL %s: %s\n' "$name" "$why"
    printf '%s\n' "$out" | sed 's/^/    | /'
  fi
}

gitrepo() { git -c init.defaultBranch=main init -q "$1"; }
hook_in() { env CLAUDE_PROJECT_DIR="$1" IFLOW_SKILL_DIR="$skill" bash "$hook"; }

M='<!-- generated-by: iflow/2 -->'
HEAD='| # | File | Type | Needs first | Status |
|---|------|------|-------------|--------|'

# ---- checker ---------------------------------------------------------------

mk "$tmp/c1" <<EOF
# Program
$M
Overall status: running
Current slice: —
Next action: EnterPlanMode for slice 01.
$HEAD
| 01 | slice-01-x.md | build | — | todo |
EOF
check "checker: healthy dossier" 0 '' '.' -- bash "$checker" "$tmp/c1"

mk "$tmp/c2" <<EOF
$M
Overall status: Running
Current slice: —
Next action: EnterPlanMode for slice 01.
$HEAD
| 01 | slice-01-x.md | build | — | todo |
EOF
check "checker: invalid status value" 1 "invalid value 'Running'" '' -- bash "$checker" "$tmp/c2"

mk "$tmp/c3" <<EOF
$M
Current slice: —
Next action: EnterPlanMode for slice 01.
$HEAD
| 01 | slice-01-x.md | build | — | todo |
EOF
check "checker: missing Overall status reports only that" 1 \
  "missing line 'Overall status:'" 'slice rows|slice table' -- bash "$checker" "$tmp/c3"

mk "$tmp/c4" <<EOF
$M
Overall status: running
Next action: Continue slice 01.
$HEAD
| 01 | slice-01-x.md | build | — | doing |
EOF
check "checker: missing Current slice reports only that" 1 \
  "missing line 'Current slice:'" "is '—' but" -- bash "$checker" "$tmp/c4"

mk "$tmp/c5" <<EOF
$HEAD
| 01 | slice-01-x.md | build | — | todo |
$M
Overall status: running
Current slice: —
Next action: EnterPlanMode for slice 01.
EOF
check "checker: table above the status line" 1 \
  "no slice rows below 'Overall status:'" 'sits above' -- bash "$checker" "$tmp/c5"

mk "$tmp/c6" <<EOF
$M
Overall status: running
Current slice: —
Next action: Continue slice 01.
$HEAD
| 01 | slice-01-x.md | build | — | doing |
EOF
check "checker: doing row but no current slice" 1 "is '—' but" '' -- bash "$checker" "$tmp/c6"

mk "$tmp/c7" <<EOF
Overall status: running
Current slice: —
Next action: EnterPlanMode for slice 01.
$HEAD
| 01 | slice-01-x.md | build | — | todo |
EOF
check "checker: missing marker" 1 'marker' '' -- bash "$checker" "$tmp/c7"

mk "$tmp/c8" <<EOF
$M
Overall status: done
Current slice: —
Next action: Read the summary at the top of this file.
$HEAD
| 01 | slice-01-x.md | build | — | done |
| 02 | slice-02-x.md | build | — | retired |
EOF
check "checker: done with a retired row" 0 '' '.' -- bash "$checker" "$tmp/c8"

# A retired row needs no file; any other row does.
mk "$tmp/c9" <<EOF
$M
Overall status: running
Current slice: —
Next action: EnterPlanMode for slice 01.
$HEAD
| 01 | slice-01-x.md | build | — | todo |
| 02 | slice-02-x.md | build | — | retired |
EOF
rm "$tmp/c9"/slice-0[12]-x.md
check "checker: row without its slice file" 1 'slice 01 has no file' 'slice 02' -- bash "$checker" "$tmp/c9"

mk "$tmp/c10" <<EOF
$M
Overall status: running
Current slice: —
Next action: EnterPlanMode for slice 01.
$HEAD
| 01 | slice-01-x.md | build | — | todo |
| 01 | slice-01-x.md | build | — | todo |
EOF
check "checker: duplicate slice numbers" 1 'duplicate slice numbers in the table: 01' '' -- bash "$checker" "$tmp/c10"

mk "$tmp/c11" <<EOF
$M
Overall status: running
Current slice: —
Next action: EnterPlanMode for slice 01.
$HEAD
| 01 | slice-01-x.md | build | — | in progress |
EOF
check "checker: invalid row status" 1 "slice 01 has invalid status 'in progress'" '' -- bash "$checker" "$tmp/c11"

mk "$tmp/c12" <<EOF
$M
Overall status: running
Current slice: 01 a
Next action: Continue slice 01.
$HEAD
| 01 | slice-01-x.md | build | — | doing |
| 02 | slice-02-x.md | build | — | doing |
EOF
check "checker: two rows doing" 1 'multiple slices are' '' -- bash "$checker" "$tmp/c12"

mk "$tmp/c13" <<EOF
$M
Overall status: running
Current slice: 01 a
Next action: Continue slice 01.
$HEAD
| 01 | slice-01-x.md | build | — | todo |
EOF
check "checker: current slice row is not doing" 1 "names 01 but its row status is 'todo'" '' -- bash "$checker" "$tmp/c13"

mk "$tmp/c14" <<EOF
$M
Overall status: running
Current slice: 03 c
Next action: Continue slice 03.
$HEAD
| 01 | slice-01-x.md | build | — | todo |
EOF
check "checker: current slice has no row" 1 'names 03 but the slice table has no such row' '' -- bash "$checker" "$tmp/c14"

mk "$tmp/c15" <<EOF
$M
Overall status: running
Current slice: slice 01
Next action: Continue slice 01.
$HEAD
| 01 | slice-01-x.md | build | — | doing |
EOF
check "checker: malformed current slice" 1 'must start with a two-digit slice number' '' -- bash "$checker" "$tmp/c15"

# Seen in a real dossier: marked done while its last slice still runs.
mk "$tmp/c16" <<EOF
$M
Overall status: done
Current slice: 01 a
Next action: Read the summary at the top of this file.
$HEAD
| 01 | slice-01-x.md | build | — | doing |
EOF
check "checker: done with a row still doing" 1 "overall status is done but slice 01 is 'doing'" '' -- bash "$checker" "$tmp/c16"
check "checker: done with a current slice" 1 "overall status is done but 'Current slice:' still names 01" '' -- bash "$checker" "$tmp/c16"

mk "$tmp/c17" <<EOF
$M
Overall status: running
Current slice: —
Next action: TBD
$HEAD
| 01 | slice-01-x.md | build | — | todo |
EOF
check "checker: placeholder next action" 1 "'Next action:' is empty or a placeholder" '' -- bash "$checker" "$tmp/c17"

# ---- pointer checker -------------------------------------------------------

# One good and one broken pointer of each form: only the broken ones count.
pointers="$root/skills/flow/scripts/check-pointers.sh"
mkdir -p "$tmp/p1/references"
cat > "$tmp/p1/SKILL.md" <<'EOF'
See [ok](references/state.md) and [bad](references/nope.md).
Per state.md §1 and state.md §9.
Per shape.md's Layer 1 and shape.md's Layer 7.
EOF
printf '## 1. One\n' > "$tmp/p1/references/state.md"
printf '## Layer 1\n' > "$tmp/p1/references/shape.md"
check "pointers: broken link" 1 "link 'references/nope.md' resolves to nothing" "link 'references/state.md'" -- bash "$pointers" "$tmp/p1"
check "pointers: broken section number" 1 "'§9' points at state.md" "'§1'" -- bash "$pointers" "$tmp/p1"
check "pointers: broken layer" 1 "'Layer 7' points at shape.md" "'Layer 1'" -- bash "$pointers" "$tmp/p1"

# ---- hook ------------------------------------------------------------------

gitrepo "$tmp/g1"
mk "$tmp/g1/docs/shape/p" < "$tmp/c1/shape.md"
mkdir -p "$tmp/g1/sub/dir"
check "hook: running dossier is listed" 0 "g1/docs/shape/p/shape.md" '' -- hook_in "$tmp/g1"
check "hook: prints its Next action" 0 'Next action: EnterPlanMode for slice 01' '' -- hook_in "$tmp/g1"
check "hook: names the skill directory" 0 "directory is $skill" '' -- hook_in "$tmp/g1"
check "hook: finds the dossier from a subdirectory" 0 "g1/docs/shape/p/shape.md" '' -- hook_in "$tmp/g1/sub/dir"

gitrepo "$tmp/g2"
mk "$tmp/g2/docs/shape/q" < "$tmp/c7/shape.md"
check "hook: shape.md without the marker is ignored" 0 '' '.' -- hook_in "$tmp/g2"

gitrepo "$tmp/g3"
mk "$tmp/g3/docs/shape/r" < "$tmp/c2/shape.md"
check "hook: broken dossier is flagged" 0 'BROKEN STATE' 'Next action:' -- hook_in "$tmp/g3"

mk "$tmp/n1/docs/shape/p" < "$tmp/c1/shape.md"
check "hook: works outside git" 0 "n1/docs/shape/p/shape.md" '' -- hook_in "$tmp/n1"

gitrepo "$tmp/g4"
mk "$tmp/g4/docs/shape/d" < "$tmp/c8/shape.md"
check "hook: healthy done dossier stays silent" 0 '' '.' -- hook_in "$tmp/g4"

check "hook: missing checker still lists pointers" 0 "Next action: EnterPlanMode" 'state unverified' -- \
  env CLAUDE_PROJECT_DIR="$tmp/g1" IFLOW_SKILL_DIR="$tmp/nowhere" bash "$hook"
check "hook: missing checker gets one warning" 0 "no check-dossier.sh at $tmp/nowhere" '' -- \
  env CLAUDE_PROJECT_DIR="$tmp/g1" IFLOW_SKILL_DIR="$tmp/nowhere" bash "$hook"
# A checker that fails on one dossier only: the warning names that one.
mkdir -p "$tmp/fake/scripts"
printf 'case "$1" in *bad*) exit 2 ;; esac\nexit 0\n' > "$tmp/fake/scripts/check-dossier.sh"
gitrepo "$tmp/g6"
mk "$tmp/g6/docs/shape/good" < "$tmp/c1/shape.md"
mk "$tmp/g6/docs/shape/bad" < "$tmp/c1/shape.md"
check "hook: warning names only the unchecked dossier" 0 \
  'Warning: could not check the state of docs/shape/bad/shape.md \(' 'of docs/shape/good' -- \
  env CLAUDE_PROJECT_DIR="$tmp/g6" IFLOW_SKILL_DIR="$tmp/fake" bash "$hook"
check "hook: finds its skill without IFLOW_SKILL_DIR" 0 "directory is $skill" 'no check-dossier' -- \
  env -u IFLOW_SKILL_DIR CLAUDE_PROJECT_DIR="$tmp/g1" bash "$hook"

# A 300-character Vietnamese Next action is cut at 200 characters, whole.
long=$(printf 'ố%.0s' $(seq 300))
gitrepo "$tmp/g5"
sed "s/^Next action: .*/Next action: $long/" "$tmp/c1/shape.md" | mk "$tmp/g5/docs/shape/v"
line=$(hook_in "$tmp/g5" | grep 'Next action:')
if printf '%s' "$line" | grep -q 'truncated' &&
   printf '%s' "$line" | iconv -f UTF-8 -t UTF-8 >/dev/null 2>&1; then
  pass=$((pass + 1))
else
  fail=$((fail + 1))
  printf 'FAIL hook: long Next action is capped on a character boundary\n'
fi

printf '%d passed, %d failed\n' "$pass" "$fail"
[ "$fail" -eq 0 ]
