#!/usr/bin/env bash
# run-check.sh <game-dir> — kiểm cấu trúc một game v2 (docs/games/<slug>), không tốn API.
# Read-only. In một dòng mỗi vi phạm. Exit 0 = sạch, 1 = không, 2 = thiếu thư mục/file bắt buộc.
#
# Kiểm bảy điều máy kiểm được của khuôn (references/khuon-file.md); phần "hiểu
# được không" là việc của phép thử năm câu với người đọc mới, không phải script:
#   1. đủ file: world.md, quests.md, character.md, journal.md, gamemaster.md,
#      ít nhất một dungeons/NN-*.md; boss/set.json và slate/index.html trừ khi
#      gamemaster/plan.md có dòng `Máy: không` (game không mô phỏng được)
#   2. world.md có đúng 10 heading '## ' theo thứ tự, không thừa không thiếu
#   3. mỗi dungeons/NN-*.md có đúng 4 heading '## ' theo thứ tự, và tên vùng của
#      nó được world.md hoặc quests.md nhắc
#   4. mọi tên ở cột trái "Bảng tra tên" của world.md có mặt trong gamemaster.md
#   5. file người chơi thuần game: không "ngoài đời"/"kỹ năng" (chung), không từ
#      trong dòng "Từ cấm ở file người chơi:" của gamemaster.md mục 8 (riêng từng
#      game, người dựng liệt kê tên lĩnh vực/kỹ năng thật), không tên kiểu
#      "Bác/Ông/Bà/Chú/Cô + Tên"
#   6. gamemaster.md đủ 9 mục đánh số
#   7. boss/set.json là object có mảng "items" đúng bằng số đề ở dòng "Bộ đề:" của
#      gamemaster.md mục 4 (khuon-file.md §boss/)
set -u
export LC_ALL=C.UTF-8

dir="${1:?usage: run-check.sh <game-dir>}"
[ -d "$dir" ] || { echo "run-check: không có thư mục $dir"; exit 2; }
fail=0
say() { printf 'run-check: %s\n' "$1"; fail=1; }

# 1. đủ file — game "không máy" (plan.md có dòng `Máy: không`) thì không đòi slate/ và boss/
machine=1
grep -qE '^[-* ]*Máy:[[:space:]]*không' "$dir/gamemaster/plan.md" 2>/dev/null && machine=0
req=(world.md quests.md character.md journal.md gamemaster.md)
[ "$machine" -eq 1 ] && req+=(boss/set.json slate/index.html)
for f in "${req[@]}"; do
  [ -f "$dir/$f" ] || { echo "run-check: thiếu file bắt buộc $f"; exit 2; }
done
dungeons=()
for f in "$dir"/dungeons/[0-9][0-9]-*.md; do [ -f "$f" ] && dungeons+=("$f"); done
[ "${#dungeons[@]}" -gt 0 ] || { echo "run-check: thiếu dungeons/NN-*.md"; exit 2; }

# 2. world.md — đúng 10 heading, đúng thứ tự (so nguyên chuỗi: bắt cả thừa, thiếu, sai thứ tự)
want=('## Đây là game gì' '## Bạn là ai' '## Bắt đầu thế nào' '## Lần chơi đầu tiên' '## Một lần chơi'
      '## Hôm nào mệt' '## Bài kiểm cố định' '## Các vùng' '## Điều game không có' '## Bảng tra tên')
[ "$(grep -E '^## ' "$dir/world.md")" = "$(printf '%s\n' "${want[@]}")" ] ||
  say "world.md phải có đúng 10 heading '## ' theo thứ tự: ${want[*]}"

# 3. dungeon — đúng 4 heading theo thứ tự, được nhắc
dwant=('## Vào vùng' '## Chiêu trong vùng' '## Qua vùng' '## Lần đọc đầu')
for d in "${dungeons[@]}"; do
  base=$(basename "$d")
  [ "$(grep -E '^## ' "$d")" = "$(printf '%s\n' "${dwant[@]}")" ] ||
    say "$base phải có đúng 4 heading '## ' theo thứ tự: ${dwant[*]}"
  # tiêu đề dạng "# Vùng 1 — the Plateau": tên vùng là phần sau dấu gạch dài; không có gạch thì lấy cả dòng
  title=$(grep -m1 -E '^# ' "$d" | sed -E 's/^# *//; s/^.*— *//')
  if [ -n "$title" ]; then
    grep -qF "$title" "$dir/world.md" "$dir/quests.md" 2>/dev/null || say "$base: tên vùng '$title' không được world.md hay quests.md nhắc"
  else
    say "$base không có dòng tiêu đề '# …'"
  fi
done

# 4. Bảng tra tên → gamemaster.md
names=$(awk '/^## Bảng tra tên/{on=1; next} on && /^\|/{print}' "$dir/world.md" | tail -n +3 | awk -F'|' '{gsub(/^[ \t`*]+|[ \t`*]+$/, "", $2); print $2}')
[ -n "$names" ] || say "world.md: Bảng tra tên rỗng hoặc không phải bảng"
while IFS= read -r n; do
  [ -n "$n" ] || continue
  grep -qF -- "$n" "$dir/gamemaster.md" || say "tên '$n' có ở Bảng tra tên nhưng không có trong gamemaster.md"
done <<<"$names"

# 5. thuần game — file người chơi (từ chung + từ cấm riêng của game, khớp cả từ, không phân biệt hoa thường)
players=("$dir/world.md" "$dir/quests.md" "$dir/character.md" "$dir/journal.md" "${dungeons[@]}")
banned='ngoài đời|kỹ năng'
extra=$(grep -m1 -E '^[-* ]*(\*\*)?Từ cấm ở file người chơi(\*\*)?:' "$dir/gamemaster.md" | sed -E 's/^[^:]*:[[:space:]]*//; s/[[:space:]]*,[[:space:]]*/|/g; s/[[:space:]]+$//')
[ -n "$extra" ] || say "gamemaster.md mục 8 thiếu dòng 'Từ cấm ở file người chơi: a, b, c' (tên lĩnh vực/kỹ năng thật của game này)"
[ -z "$extra" ] || banned="$banned|$extra"
hit=$(grep -n -i -w -E "$banned" "${players[@]}" 2>/dev/null | head -5)
[ -z "$hit" ] || { say "file người chơi có từ ngoài game (5 dòng đầu):"; printf '%s\n' "$hit" | sed 's/^/    /'; }
vn=$(grep -n -E '\b(Bác|Ông|Bà|Chú|Cô|Thím|Cậu) [A-ZĐ][a-zăâđêôơưáàảãạấầẩẫậắằẳẵặéèẻẽẹếềểễệíìỉĩịóòỏõọốồổỗộớờởỡợúùủũụứừửữựýỳỷỹỵ]+' "${players[@]}" 2>/dev/null | head -3)
[ -z "$vn" ] || { say "file người chơi có tên riêng tiếng Việt kiểu 'Bác + Tên':"; printf '%s\n' "$vn" | sed 's/^/    /'; }

# 6. gamemaster.md — 9 mục
for n in $(seq 1 9); do
  grep -qE "^## $n\. " "$dir/gamemaster.md" || say "gamemaster.md thiếu mục '## $n. …'"
done

# 7. boss/set.json — đúng số đề mà gamemaster.md mục 4 khai (bỏ qua khi không máy)
nG="không máy"
if [ "$machine" -eq 1 ]; then
nWant=$(awk '/^## 4\. /{on=1; next} /^## /{on=0} on' "$dir/gamemaster.md" | grep -m1 -oE 'Bộ đề:[^0-9]*[0-9]+' | grep -oE '[0-9]+$')
[ -n "$nWant" ] || say "gamemaster.md mục 4 thiếu dòng 'Bộ đề: <số đề>, …' (run-check đọc số đề ở đó)"
nG=$(python3 -c "import json,sys
try:
    g=json.load(open(sys.argv[1])); print(len(g['items']) if isinstance(g,dict) and isinstance(g.get('items'),list) else 'sai-dạng')
except Exception as e: print('lỗi-json')" "$dir/boss/set.json" 2>/dev/null || echo "lỗi-json")
case "$nG" in
  sai-dạng) say "boss/set.json phải là object {\"items\": [...]} (khuon-file.md §boss/)" ;;
  lỗi-json) say "boss/set.json không đọc được (JSON hỏng)" ;;
  *) [ -z "$nWant" ] || [ "$nG" = "$nWant" ] || say "boss/set.json có $nG đề, gamemaster.md mục 4 khai $nWant" ;;
esac
fi

if [ "$fail" -eq 0 ]; then
  echo "run-check: sạch — đủ file, world.md 10 heading, ${#dungeons[@]} dungeon, bảng tra tên khớp gamemaster, thuần game, gamemaster 9 mục, $([ "$machine" -eq 1 ] && echo "bài kiểm $nG đề" || echo "không máy")."
fi
exit "$fail"
