#!/usr/bin/env bash
# check-pointers.sh [skill-dir] — mechanical guard for a skill's own cross-file
# pointers. Read-only. Prints one line per violation. Exit 0 = clean, 1 = not.
#
# Gathering each rule into one home left pointers behind in every other place,
# so a renamed file or a renumbered section now rots silently. This checks the
# three pointer forms a skill uses:
#   1. markdown links   [text](file.md) or (file.md#anchor) → file must exist
#   2. §N / section N   → target file must have a "## N." heading
#   3. <File>'s Layer N → that file must have a "## Layer N" heading
#
# Form 2 resolves its target from what sits immediately around the reference:
# "state.md §4" or "section 1 of shape.md" point at the named file, a bare
# "§4" points at the file being scanned. Merely mentioning another file
# elsewhere on the line does not retarget it. Every message prints the target
# it resolved to, so a wrong guess is visible rather than silent.
#
# Deliberately NOT checked: quoted section names ("Approved plan", "Result",
# …) and re-copied rule text. Both need a hand-kept registry of valid names,
# which this program rejected on purpose.
set -u

dir="${1:-$(cd "$(dirname "$0")/.." && pwd)}"
fail=0
checked=0
say() { printf 'check-pointers: %s\n' "$1"; fail=1; }

NAMES='SKILL|shape|state|agents'

# path_of <bare-name.md> — where that skill file lives
path_of() {
  case "$1" in
    SKILL.md) printf '%s\n' "$dir/SKILL.md" ;;
    *)        printf '%s\n' "$dir/references/$1" ;;
  esac
}

# target_for <before> <after> <self> — which file a §N/section N refers to
target_for() {
  local before="$1" after="$2" self="$3" n
  n=$(printf '%s' "$before" | grep -oE "($NAMES)\.md'?s?[[:space:]]*$" | grep -oE "($NAMES)\.md" || true)
  if [ -z "$n" ]; then
    n=$(printf '%s' "$after" | grep -oE "^[[:space:]]*of[[:space:]]+\[?($NAMES)\.md" | grep -oE "($NAMES)\.md" || true)
  fi
  if [ -n "$n" ]; then path_of "$n"; else printf '%s\n' "$self"; fi
}

nfiles=0
for f in "$dir/SKILL.md" "$dir"/references/*.md; do
  [ -f "$f" ] || continue
  nfiles=$((nfiles + 1))
  fdir=$(dirname "$f")
  rel=${f#"$dir"/}

  # --- form 1: markdown links to .md files, fragment tolerated
  while IFS=: read -r ln target; do
    [ -n "${target:-}" ] || continue
    checked=$((checked + 1))
    case "$target" in http*) continue ;; esac
    target=${target%%#*}
    [ -f "$fdir/$target" ] ||
      say "$rel:$ln link '$target' resolves to nothing ($fdir/$target)"
  done <<EOF
$(grep -noE '\[[^]]*\]\([^)]+\.md(#[^)]*)?\)' "$f" |
  sed -E 's/^([0-9]+):.*\(([^)]+)\)$/\1:\2/')
EOF

  # --- form 2: §N and "section N", target read from the immediate context
  while IFS= read -r ln; do
    [ -n "${ln:-}" ] || continue
    line=$(sed -n "${ln}p" "$f")
    rest="$line"
    while :; do
      tok=$(printf '%s' "$rest" | grep -oiE '(§|section )[0-9]+' | head -1 || true)
      [ -n "$tok" ] || break
      before=${rest%%"$tok"*}
      after=${rest#*"$tok"}
      rest="$after"
      num=$(printf '%s' "$tok" | grep -oE '[0-9]+')
      checked=$((checked + 1))
      tgt=$(target_for "$before" "$after" "$f")
      grep -qE "^## $num\." "$tgt" ||
        say "$rel:$ln '$tok' points at $(basename "$tgt"), which has no '## $num.' heading"
    done
  done <<EOF
$(grep -niE '(§|section )[0-9]+' "$f" | cut -d: -f1)
EOF

  # --- form 3: <File>'s Layer N — the file is named in the match itself
  while IFS=: read -r ln name num; do
    [ -n "${num:-}" ] || continue
    checked=$((checked + 1))
    tgt=$(path_of "$name.md")
    grep -qE "^## Layer $num" "$tgt" ||
      say "$rel:$ln 'Layer $num' points at $name.md, which has no '## Layer $num' heading"
  done <<EOF
$(grep -noE "($NAMES)\.md's Layer [0-9]+" "$f" |
  sed -E "s/^([0-9]+):($NAMES)\.md's Layer ([0-9]+)$/\1:\2:\3/")
EOF
done

if [ "$nfiles" -eq 0 ]; then
  say "no SKILL.md or references/*.md under $dir"
elif [ "$fail" -eq 0 ]; then
  printf 'check-pointers: %d pointers checked in %d files, all resolve\n' "$checked" "$nfiles"
fi
exit $fail
