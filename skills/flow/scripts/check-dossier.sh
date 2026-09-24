#!/usr/bin/env bash
# check-dossier.sh <dossier-dir> — mechanical guard for an i:flow dossier.
# Read-only. Prints one line per violation. Exit 0 = clean, 1 = violations.
# Label strings: the contract table in references/state.md §2 is the single
# definition — change there and here together.
set -u

dir="${1:?usage: check-dossier.sh <dossier-dir>}"
f="$dir/shape.md"
fail=0
say() { printf 'check-dossier: %s\n' "$1"; fail=1; }

if [ ! -f "$f" ]; then
  say "missing shape.md in $dir"
  exit 1
fi

# The marker is what says "this file speaks the contract". Missing it is a
# violation to report, not a cue to guess at some other set of labels.
grep -q '<!-- generated-by: iflow/2 -->' "$f" ||
  say "missing '<!-- generated-by: iflow/2 -->' marker"
L_STATUS='Overall status:'; L_SLICE='Current slice:'
V_RUNNING='running'; V_DOING='doing'
V_ROW='todo|doing|done|needs-redo|retired'
V_END='done|retired'; V_RETIRED='retired'
L_NEXT='Next action:'

val() { # val <label> — value of first line starting with label, trimmed
  awk -v lab="$1" 'index($0, lab)==1 {
    v=substr($0, length(lab)+1); gsub(/^[ \t]+|[ \t]+$/, "", v); print v; exit
  }' "$f"
}

status=$(val "$L_STATUS")
slice=$(val "$L_SLICE")
next=$(val "$L_NEXT")

if ! grep -q "^$L_STATUS" "$f"; then
  say "missing line '$L_STATUS'"
elif [ "$status" != "$V_RUNNING" ] && [ "$status" != "done" ]; then
  say "'$L_STATUS' has invalid value '$status'"
fi
grep -q "^$L_SLICE" "$f" || say "missing line '$L_SLICE'"
if ! grep -q "^$L_NEXT" "$f"; then
  say "missing line '$L_NEXT'"
else
  case "$next" in
    ''|'—'|'-'|'...'|'…'|TBD|tbd) say "'$L_NEXT' is empty or a placeholder ('$next')" ;;
  esac
fi

# Slice-table rows: "| NN | ... | status |" — status is the last cell.
rows=$(awk -F'|' '/^\|[ \t]*[0-9][0-9][ \t]*\|/ {
  nn=$2; st=$(NF-1)
  # a dossier may bold or backtick its cell values — strip decoration
  gsub(/^[ \t*`]+|[ \t*`]+$/, "", nn); gsub(/^[ \t*`]+|[ \t*`]+$/, "", st)
  print nn "\t" st
}' "$f")

dups=$(printf '%s\n' "$rows" | awk -F'\t' '$1!="" {c[$1]++} END {for (n in c) if (c[n]>1) printf "%s ", n}')
[ -n "$dups" ] && say "duplicate slice numbers in the table: $dups"

doing_rows=""
while IFS="$(printf '\t')" read -r nn st; do
  [ -n "$nn" ] || continue
  if ! printf '%s' "$st" | grep -qxE "$V_ROW"; then
    say "slice $nn has invalid status '$st'"
  fi
  [ "$st" = "$V_DOING" ] && doing_rows="$doing_rows $nn"
  if [ "$st" != "$V_RETIRED" ] && ! ls "$dir"/slice-"$nn"-*.md >/dev/null 2>&1; then
    say "slice $nn has no file slice-$nn-*.md in $dir"
  fi
  if [ "$status" = "done" ] && ! printf '%s' "$st" | grep -qxE "$V_END"; then
    say "overall status is done but slice $nn is '$st'"
  fi
done <<EOF
$rows
EOF

set -- $doing_rows
[ "$#" -gt 1 ] && say "multiple slices are '$V_DOING':$doing_rows (at most one may run)"

cur_nn=""
malformed=0
case "$slice" in
  ''|'—'|'-') : ;;
  *)
    cur_nn=$(printf '%s' "$slice" | grep -oE '^[0-9][0-9]' || true)
    if [ -z "$cur_nn" ]; then
      malformed=1
      say "'$L_SLICE' value '$slice' must start with a two-digit slice number, or be '—'"
    fi
    ;;
esac
if [ "$status" = "done" ] && [ -n "$cur_nn" ]; then
  say "overall status is done but '$L_SLICE' still names $cur_nn (a finished program reads '—')"
elif [ -n "$cur_nn" ]; then
  cur_st=$(printf '%s\n' "$rows" | awk -F'\t' -v nn="$cur_nn" '$1==nn {print $2; exit}')
  if [ -z "$cur_st" ]; then
    say "'$L_SLICE' names $cur_nn but the slice table has no such row"
  elif [ "$cur_st" != "$V_DOING" ]; then
    say "'$L_SLICE' names $cur_nn but its row status is '$cur_st' (expected '$V_DOING')"
  fi
elif [ "$malformed" -eq 0 ] && [ -n "$doing_rows" ]; then
  say "'$L_SLICE' is '—' but row(s)$doing_rows are '$V_DOING'"
fi

exit $fail
