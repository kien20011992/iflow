#!/usr/bin/env bash
# The calculator project plus a healthy i:flow dossier whose Next action starts slice 01.
set -e
mkdir -p app tests docs/iflow/may-tinh-a7f3
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
PY
printf '# calc\n\nA toy calculator. Run the tests with `python3 -m pytest`.\n' > README.md
cat > docs/iflow/may-tinh-a7f3/iflow.md <<'MD'
# Thêm phép nhân và phép chia vào máy tính

## Bức tranh

Máy tính hiện có cộng và trừ trong app/calc.py với test ở tests/test_calc.py. Chương trình thêm nhân và chia, mỗi phép một slice có test riêng. Xong khi cả hai phép chạy và test xanh.

## Các slice theo thứ tự chạy

1. Phép nhân: người dùng gọi mul(a, b) và được tích, có test. File: 01-nhan.md.
2. Phép chia: người dùng gọi div(a, b) và được thương, chia cho 0 báo lỗi, có test. File: 02-chia.md.

## Quyết định

- 2026-10-07 — Chia cho 0 ném ValueError, không trả None. Duyệt cùng bảng slice.

## Đã khảo sát

Hai hàm hiện có là hàm thuần, không phụ thuộc gì. Test dùng pytest.

## Nguồn

app/calc.py, tests/test_calc.py, README.md.

## Trạng thái cho phiên sau

<!-- generated-by: iflow/2 -->

> AGENT: continuing from this file? Load the `i:flow` skill first (read
> its SKILL.md wherever it is installed), then follow the Next action
> below. Facts live in this directory, not in conversational memory.

Overall status: running
Current slice: —
Next action: EnterPlanMode for slice 01, explore only within app/calc.py and tests/test_calc.py

| # | File | Type | Needs first | Status |
|---|------|------|-------------|--------|
| 01 | 01-nhan.md | build | — | todo |
| 02 | 02-chia.md | build | 01 | todo |

<!-- Overall status: running | done. Type: build | research. Status: todo | doing | done | needs-redo | retired -->
MD
cat > docs/iflow/may-tinh-a7f3/01-nhan.md <<'MD'
# Phép nhân

Thêm mul(a, b) vào app/calc.py trả về tích. Có test trong tests/test_calc.py. Không cần slice nào trước.

## Plan đã duyệt

## Kết quả

## Ghi chú

- Để ngỏ khi định hình: có nhận số thực hay chỉ số nguyên.
MD
cat > docs/iflow/may-tinh-a7f3/02-chia.md <<'MD'
# Phép chia

Thêm div(a, b) vào app/calc.py trả về thương; chia cho 0 ném ValueError. Có test. Cần slice 01 trước.

## Plan đã duyệt

## Kết quả

## Ghi chú
MD
git init -q && git add -A && git -c user.name=eval -c user.email=eval@example.com commit -qm init
