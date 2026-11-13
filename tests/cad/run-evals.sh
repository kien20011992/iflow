#!/usr/bin/env bash
# tests/cad/run-evals.sh [claude plugin eval flags] — the paid checks for i:cad.
# Runs the behaviour cases in evals-cad/ against this working tree, then builds
# review.html beside the run's report.html. Every argument is passed on:
#   tests/cad/run-evals.sh --runs 1                  one run per case
#   tests/cad/run-evals.sh --runs 1 --case cad-brief one case
# Exits with the eval's own status (1 when a case scored below the threshold).
set -u
root="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$root" || exit 2

# --scaffold: two cases build a fixture project. --allow-tools: the cases write
# the project file. --keep-temp: review.py reads each run's trace from there.
claude plugin eval . --eval-dir evals-cad --scaffold --allow-tools Write Edit \
  --ablation none --no-publish --keep-temp "$@"
status=$?

latest=$(ls -d evals-cad/results/*/ 2> /dev/null | tail -1)
if [ -n "$latest" ] && [ -f "${latest}aggregate-result.json" ]; then
  python3 tests/cad/review.py "${latest}aggregate-result.json"
else
  echo "no result to review under evals-cad/results/" >&2
fi
exit $status
