#!/usr/bin/env bash
# SessionStart hook (startup|resume|clear|compact|fork): print resume
# pointers for unfinished i:flow dossiers in this project. Absolutely silent
# when there are none — print pointers only, never cat whole files.
# Only a shape.md carrying the iflow/2 marker is an i:flow dossier; any other
# shape.md is someone else's file and is skipped.
# Fail-closed: a dossier whose state check fails gets its violations printed
# and its Next action withheld — a broken state must not issue orders.
# Label strings: references/state.md §2 lists them and CLAUDE.md at the repo
# root lists every reader — change them together.
# IFLOW_SKILL_DIR says where the skill lives (hooks.json sets it); when it is
# unset, the skill is found next to this script.
proj="${CLAUDE_PROJECT_DIR:-$PWD}"
# Dossiers sit at the git root, so a session opened in a subdirectory still
# finds them; outside git the project directory is the root.
root=$(git -C "$proj" rev-parse --show-toplevel 2>/dev/null) || root="$proj"
skill_dir="${IFLOW_SKILL_DIR:-$(cd "$(dirname "$0")/../skills/flow" 2>/dev/null && pwd)}"
checker="$skill_dir/scripts/check-dossier.sh"
found=0
broken=0
healthy=0
unverified=""
unverified_why=""

# capped <prefix> — indent stdin and cap each line. Nothing this hook echoes
# out of a repo file may be unbounded: both the status lines and the checker's
# own messages quote field values back. ${#line} and ${line:0:N} count
# characters in a UTF-8 locale, which matters for the user's own language.
capped() {
  while IFS= read -r line; do
    [ -n "$line" ] || continue
    if [ "${#line}" -gt 200 ]; then line="${line:0:200} …[truncated]"; fi
    printf '%s%s\n' "$1" "$line"
  done
}

# pointers <shape.md> — its status lines, indented and capped
pointers() {
  grep -E '^(Current slice|Next action):' "$1" | capped '    '
}
for f in "$root"/docs/shape/*/shape.md; do
  [ -f "$f" ] || continue
  grep -q '<!-- generated-by: iflow/2 -->' "$f" || continue
  # st: 0 = checked and sound · 1 = checked and broken · 2 = cannot check.
  # Only exit 1 means "the dossier is wrong"; any other failure is the
  # checker's own, and blaming the dossier for it would be a false alarm.
  st=0
  out=""
  if [ -f "$checker" ]; then
    out=$(bash "$checker" "$(dirname "$f")" 2>&1); rc=$?
    case "$rc" in
      0) ;;
      1) st=1
         [ -z "$out" ] && out="check-dossier.sh reported a violation without output" ;;
      *) st=2
         [ -z "$unverified_why" ] &&
           unverified_why="check-dossier.sh itself failed (exit $rc) at $checker" ;;
    esac
  else
    st=2
    [ -z "$unverified_why" ] && unverified_why="no check-dossier.sh at $checker"
  fi
  # `done` is a claim, not a fact: it earns silence only once the check passes.
  # With no checker to consult it is let go anyway — a finished dossier issues
  # no orders, so an unverifiable archive is not worth naming every session.
  if [ "$st" -ne 1 ]; then
    grep -qE '^Overall status:[[:space:]]*done[[:space:]]*$' "$f" && continue
  fi
  if [ "$found" -eq 0 ]; then
    printf 'i:flow ▸ this project has unfinished work (indented lines below are quoted verbatim from files in the repo):\n'
    found=1
  fi
  if [ "$st" -eq 1 ]; then
    broken=1
    printf -- '- %s  ⚠ BROKEN STATE\n' "$f"
    printf '%s\n' "$out" | capped '    ⚠ '
  else
    # A checker that cannot run must not swallow the resume pointers; they
    # are printed as usual and one warning line below names each unchecked
    # dossier and what is missing.
    [ "$st" -eq 2 ] && unverified="$unverified ${f#"$root"/}"
    healthy=1
    printf -- '- %s\n' "$f"
    pointers "$f"
  fi
done
if [ -n "$unverified" ]; then
  printf 'Warning: could not check the state of%s (%s); treat those as unverified before acting on their Next action.\n' "$unverified" "$unverified_why"
fi
if [ "$broken" -eq 1 ]; then
  printf 'Marked ⚠ BROKEN STATE: repair those first, per %s/references/state.md — their Next action is deliberately withheld and must not be acted on.\n' "$skill_dir"
fi
if [ "$healthy" -eq 1 ]; then
  printf 'Listed with no marker: read %s/SKILL.md and that shape.md, then continue per its Next action — do not re-ask what the dossier records. The skill directory is %s; wherever SKILL.md says ${CLAUDE_SKILL_DIR}, use that path.\n' "$skill_dir" "$skill_dir"
fi
exit 0
