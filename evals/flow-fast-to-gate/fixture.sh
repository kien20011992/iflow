#!/usr/bin/env bash
# A tiny calculator project: enough for an opening sweep, nothing to run.
set -e
mkdir -p app tests
cat > app/calc.py <<'PY'
def add(a, b):
    return a + b

def sub(a, b):
    return a - b
PY
cat > tests/test_calc.py <<'PY'
from app.calc import add, sub

def test_add():
    assert add(2, 3) == 5

def test_sub():
    assert sub(5, 3) == 2
PY
cat > README.md <<'MD'
# calc

A toy calculator. Run the tests with `python3 -m pytest`.
MD
git init -q && git add -A && git -c user.name=eval -c user.email=eval@example.com commit -qm init
