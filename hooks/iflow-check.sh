#!/usr/bin/env bash
# PostToolUse hook (Edit|Write): when the file just written is an i:flow
# dossier's iflow.md, run the dossier checker on it and hand its violations
# back to Claude. Silent in every other case.
# Exit 2 is the only exit that shows stderr to Claude after a tool ran; it
# does not undo the write. Exit 0 output goes to the debug log only.
# Only an iflow.md carrying the iflow/2 marker is an i:flow dossier; any
# other iflow.md is someone else's file and is skipped, as iflow-resume.sh
# does. Label strings: references/state.md §2 lists them and CLAUDE.md at
# the repo root lists every reader — change them together.
# IFLOW_SKILL_DIR overrides where the skill lives (tests/run.sh sets it);
# unset, the skill is found next to this script.
input=$(cat)
# The first unescaped "file_path" key is tool_input.file_path: tool_input
# precedes tool_response in the event, and a "file_path" inside a content
# string arrives escaped as \"file_path\".
path=$(printf '%s' "$input" |
  grep -oE '(^|[^\\])"file_path"[[:space:]]*:[[:space:]]*"([^"\\]|\\.)*"' | head -1 |
  sed -E 's/^.*"file_path"[[:space:]]*:[[:space:]]*"//; s/"$//')
case "$path" in
  /*) ;;
  *) path="${CLAUDE_PROJECT_DIR:-$PWD}/$path" ;;
esac
case "$path" in
  */docs/iflow/*/iflow.md) ;;
  *) exit 0 ;;
esac
[ -f "$path" ] || exit 0
grep -q '<!-- generated-by: iflow/2 -->' "$path" || exit 0
skill_dir="${IFLOW_SKILL_DIR:-$(cd "$(dirname "$0")/../skills/flow" 2>/dev/null && pwd)}"
checker="$skill_dir/scripts/check-dossier.sh"
if [ ! -f "$checker" ]; then
  printf 'iflow-check: no check-dossier.sh at %s; run it by hand on %s\n' "$checker" "$(dirname "$path")" >&2
  exit 0
fi
out=$(bash "$checker" "$(dirname "$path")" 2>&1); rc=$?
# The checker quotes field values from the file; cap each line as
# iflow-resume.sh does, so a runaway value cannot flood the context.
capped() {
  while IFS= read -r line; do
    [ -n "$line" ] || continue
    if [ "${#line}" -gt 200 ]; then line="${line:0:200} …[truncated]"; fi
    printf '    %s\n' "$line"
  done
}
case "$rc" in
  0) exit 0 ;;
  1) { printf 'i:flow ▸ %s fails its state check; fix this before going on:\n' "$path"
       printf '%s\n' "$out" | capped; } >&2
     exit 2 ;;
  *) printf 'iflow-check: check-dossier.sh itself failed (exit %s) on %s; run it by hand\n' "$rc" "$path" >&2
     exit 0 ;;
esac
