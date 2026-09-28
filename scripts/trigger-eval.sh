#!/usr/bin/env bash
# trigger-eval.sh <skill> <eval.json> [--runs N] [--jobs N] [--model M] [--out FILE]
#
# Measures whether a skill's description makes Claude open the skill on its
# own. For every query in <eval.json> it runs `claude -p <query>` N times
# (default 3) and counts the runs in which the first assistant turn called
# the Skill tool with `i:<skill>` (or Read this repo's skills/<skill>/SKILL.md).
# A query "fires" when at least half of its runs triggered. A query passes
# when firing matches its `should_trigger` flag.
#
# <eval.json> is a JSON array of {"query": "...", "should_trigger": true|false}
# — the same shape Anthropic's skill-creator uses, so those tools still work
# on the file.
#
# Each run loads THIS working tree via --plugin-dir and disables the
# installed copy of the plugin for that session only (--settings), so the
# description under test is the one on disk here, not the one in the plugin
# cache, and nothing in the user's settings.json is touched. The session runs
# in an empty temp directory: no project CLAUDE.md, no dossier for the resume
# hook to announce; user-level settings and every other skill stay in place so
# competing skills compete as they do for real. The session is killed as soon
# as a Skill call or a result event appears in the stream, so the decision
# is observed and nothing after it runs — a `context: fork` skill never
# gets to do real work; --max-turns 1 is the backstop.
#
# Cost: (queries × runs) sessions of `claude -p`, ~5–10 s each, run --jobs
# (default 4) at a time. --model is passed through only when given; the
# default is whatever the user's settings pick, which is what they experience.
#
# Output: one line per query, `PASS|FAIL k/N yes|no <query>`, followed by
# `-> other: <skill>xC` when some run opened another skill instead — the
# competitor a description must beat — then totals. --out writes the same
# numbers as JSON. A query with any run that showed neither a Skill call nor
# a result event (timeout, crash) is ERROR, never PASS. Exit 0 when every query passes,
# 1 when any fails or errors, 2 on usage error or a user-invoked-only skill.
set -uo pipefail

repo="$(cd "$(dirname "$0")/.." && pwd)"
runs=3
jobs=4
model=""
out=""

usage() {
  echo "usage: $0 <skill> <eval.json> [--runs N] [--jobs N] [--model M] [--out FILE]" >&2
  exit 2
}

[[ $# -ge 2 ]] || usage
skill="$1"; eval_file="$2"; shift 2
while [[ $# -gt 0 ]]; do
  case "$1" in
    --runs)  [[ $# -ge 2 ]] || usage; runs="$2"; shift 2 ;;
    --jobs)  [[ $# -ge 2 ]] || usage; jobs="$2"; shift 2 ;;
    --model) [[ $# -ge 2 ]] || usage; model="$2"; shift 2 ;;
    --out)   [[ $# -ge 2 ]] || usage; out="$2"; shift 2 ;;
    *) usage ;;
  esac
done

[[ -d "$repo/skills/$skill" ]] || { echo "no such skill in $repo/skills: $skill" >&2; exit 2; }
# A user-invoked-only skill never shows Claude its description, so every
# positive query would FAIL for no reason. The flag is read from the YAML
# frontmatter only, never from the body.
if awk 'NR==1 {if ($0 != "---") exit; next} $0 == "---" {exit}
        /^disable-model-invocation:[[:space:]]*true[[:space:]]*$/ {found=1}
        END {exit !found}' "$repo/skills/$skill/SKILL.md"; then
  echo "$skill is user-invoked only (disable-model-invocation: true): Claude never sees its description, so there is nothing to measure" >&2
  exit 2
fi
[[ -f "$eval_file" ]] || { echo "eval file not found: $eval_file" >&2; exit 2; }
[[ "$runs" =~ ^[1-9][0-9]*$ && "$jobs" =~ ^[1-9][0-9]*$ ]] || usage
for tool in jq claude timeout; do
  command -v "$tool" >/dev/null || { echo "missing: $tool" >&2; exit 2; }
done
jq -e 'type=="array" and length>0 and all(.[]; (.query|type=="string") and (.should_trigger|type=="boolean"))' \
  "$eval_file" >/dev/null || { echo "eval file must be a non-empty array of {query, should_trigger}" >&2; exit 2; }

if [[ -n "$out" ]]; then
  : > "$out" || { echo "cannot write --out file: $out" >&2; exit 2; }
fi
eval_file="$(cd "$(dirname "$eval_file")" && pwd)/$(basename "$eval_file")"
n="$(jq 'length' "$eval_file")"
work="$(mktemp -d)"
trap 'rm -rf "$work"' EXIT
mkdir -p "$work/cwd" "$work/out"

# One session. Writes <out>.hit = 1|0, <out>.skills = every Skill the first
# turn opened, and <out>.err = 1 when neither a Skill call nor a result event
# was seen (timeout/crash before the decision). The session is killed the
# moment a Skill call or a result event shows up in the stream: the decision
# is made by then, and a `context: fork` skill (i:debug, i:test) must not get
# to run its real work inside the temp cwd.
run_one() {
  local i="$1" r="$2" q o pid waited=0
  q="$(jq -r ".[$i].query" "$EVAL_FILE")"
  o="$WORK/out/$i.$r"
  local -a extra=()
  [[ -n "$MODEL" ]] && extra=(--model "$MODEL")
  ( cd "$WORK/cwd" && exec env -u CLAUDECODE claude -p "$q" \
      --output-format stream-json --verbose --max-turns 1 \
      --plugin-dir "$REPO" \
      --settings '{"enabledPlugins":{"i@iflow":false}}' \
      ${extra[@]+"${extra[@]}"} ) > "$o.jsonl" 2> "$o.stderr" &
  pid=$!
  while kill -0 "$pid" 2>/dev/null; do
    if (( waited >= 180 )) \
       || grep -q '"type":"result"' "$o.jsonl" 2>/dev/null \
       || grep -q '"type":"assistant".*"name":"Skill"' "$o.jsonl" 2>/dev/null; then
      kill "$pid" 2>/dev/null || true; sleep 1; kill -9 "$pid" 2>/dev/null || true
      break
    fi
    sleep 1; (( waited++ )) || true
  done
  wait "$pid" 2>/dev/null || true
  jq -r 'select(.type=="assistant") | .message.content[]? | select(.type=="tool_use" and .name=="Skill")
         | (.input.skill // "") | split(" ")[0]' "$o.jsonl" 2>/dev/null | grep -v '^$' > "$o.skills" || true
  if grep -qx "i:$SKILL" "$o.skills" \
     || jq -e --arg p "skills/$SKILL/SKILL.md" 'select(.type=="assistant") | .message.content[]?
          | select(.type=="tool_use" and .name=="Read" and ((.input.file_path // "") | endswith($p)))' \
          "$o.jsonl" >/dev/null 2>&1; then
    echo 1 > "$o.hit"
  else
    echo 0 > "$o.hit"
    # Any Skill call is a complete observation of the decision, whichever
    # skill it named. Only a session that showed neither a Skill call nor a
    # result event says nothing about the description.
    if [[ ! -s "$o.skills" ]] && ! grep -q '"type":"result"' "$o.jsonl" 2>/dev/null; then
      echo 1 > "$o.err"
    fi
  fi
}
export -f run_one
export EVAL_FILE="$eval_file" WORK="$work" MODEL="$model" REPO="$repo" SKILL="$skill"

for ((i = 0; i < n; i++)); do
  for ((r = 1; r <= runs; r++)); do echo "$i $r"; done
done | xargs -P "$jobs" -L1 bash -c 'run_one "$@"' _

pass_yes=0; total_yes=0; pass_no=0; total_no=0; errors=0
rows="$work/rows.jsonl"; : > "$rows"
for ((i = 0; i < n; i++)); do
  q="$(jq -r ".[$i].query" "$eval_file")"
  expected="$(jq -r ".[$i].should_trigger" "$eval_file")"
  k=0; others=""; broken=0
  for ((r = 1; r <= runs; r++)); do
    (( k += $(cat "$work/out/$i.$r.hit") ))
    [[ -f "$work/out/$i.$r.err" ]] && { (( errors++ )); broken=1; }
    others+="$(grep -vx "i:$skill" "$work/out/$i.$r.skills" 2>/dev/null; true)"$'\n'
  done
  others="$(printf '%s' "$others" | grep -v '^$' | sort | uniq -c | awk '{printf "%s%sx%d", (NR>1?", ":""), $2, $1}')" 
  fired=false; (( 2 * k >= runs )) && fired=true
  verdict=FAIL; [[ "$fired" == "$expected" ]] && verdict=PASS
  # A run with no result event (timeout, crash, CLI down) says nothing about
  # the description; the query is ERROR, never a pass, so a dead CLI cannot
  # turn an all-negative eval set green.
  (( broken )) && verdict=ERROR
  if [[ "$expected" == true ]]; then
    (( total_yes++ )); [[ $verdict == PASS ]] && (( pass_yes++ ))
    want=yes
  else
    (( total_no++ )); [[ $verdict == PASS ]] && (( pass_no++ ))
    want=no
  fi
  printf '%s %d/%d %s %s\n' "$verdict" "$k" "$runs" "$want" "$q"
  [[ -n "$others" ]] && printf '   -> other: %s\n' "$others"
  jq -cn --arg q "$q" --argjson e "$expected" --argjson k "$k" --argjson n "$runs" --argjson f "$fired" \
    --arg v "$verdict" --arg o "$others" \
    '{query:$q, should_trigger:$e, triggered:$k, runs:$n, fired:$f, verdict:$v, other_skills:$o}' >> "$rows"
done

total=$(( total_yes + total_no )); passed=$(( pass_yes + pass_no ))
echo "should-trigger: $pass_yes/$total_yes  should-not: $pass_no/$total_no  total: $passed/$total  sessions-without-result: $errors"

if [[ -n "$out" ]]; then
  if jq -s --arg skill "$skill" --arg model "${model:-default}" --argjson runs "$runs" --argjson errors "$errors" \
    '{skill:$skill, model:$model, runs:$runs, sessions_without_result:$errors,
      summary:{should_trigger:{passed:(map(select(.should_trigger and .verdict=="PASS"))|length), total:(map(select(.should_trigger))|length)},
               should_not:{passed:(map(select((.should_trigger|not) and .verdict=="PASS"))|length), total:(map(select(.should_trigger|not))|length)}},
      queries:.}' "$rows" > "$out"; then
    echo "wrote $out"
  else
    echo "failed to write $out" >&2
  fi
fi

[[ $passed -eq $total ]]
