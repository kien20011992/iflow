#!/usr/bin/env bash
# check-skill.sh [skill-dir] — kiểm cơ học skill i:gamify v2, không tốn API.
# Read-only. In một dòng mỗi vi phạm. Exit 0 = sạch, 1 = không, 2 = không
# tìm thấy thư mục hay thiếu file bắt buộc.
#
# Kiểm những thứ một lần sửa tay dễ làm lệch mà không ai thấy:
#   1. frontmatter SKILL.md có name/description/argument-hint, và KHÔNG có
#      context: fork (skill cần AskUserQuestion, fork không có)
#   2. mọi link markdown [..](file) trong SKILL.md và references/ trỏ tới file
#      có thật
#   3. references/tim-hieu.md có đủ năm heading trục và mục mẫu plan.md
#   3b. references/thu-vien-khung.md có ≥ 4 khung, mỗi khung đủ 8 nhãn mục,
#      mục Hàng cấm với 4 gạch đầu dòng; references/concept.md có ba mục cổng
#   3c. references/vong-slice.md có hai mục đọc mỗi slice; ke-hoach-gamemaster.md
#      có Bước A và mẫu gamemaster.md đủ 9 mục đánh số với Bảng từ vựng ở
#      mục 7; sau-dungeon.md có ba mục đọc sau dungeon cuối;
#      khuon-file.md và quan-tro.md trỏ tới bảng từ vựng
#   3d. references/slate.md có ba mục: Máy chấm, Hợp đồng kết quả, Cảm giác game
#   3e. references/luat-van-phong.md đủ 18 điều A1–A6, B1–B9, C1–C3 + mục D;
#      references/khuon-file.md có mục cho 8 file
#   3f. references/quan-tro.md (chế độ play, mỗi lần chơi) đủ 6 mục và
#      quan-tro-moc.md (chấm bài kiểm, qua vùng) đủ 2 mục; SKILL.md trỏ tới
#      quan-tro.md
#   4. references/quy-trinh.md còn đủ 32 mã [1]..[32] (danh sách kiểm nền
#      của skill)
#   5. SKILL.md không có chữ "commit" và không trỏ tới file của skill i:flow
#      (skill này đi lộ trình riêng, không nạp skill khác)
# Mỗi slice của chương trình v2 thêm file tham chiếu mới thì thêm vào REQ và
# một khối kiểm riêng ở dưới.
set -u
export LC_ALL=C.UTF-8

dir="${1:-$(cd "$(dirname "$0")/.." && pwd)}"
[ -d "$dir" ] || { echo "check-skill: không có thư mục $dir"; exit 2; }
skill="$dir/SKILL.md"
th="$dir/references/tim-hieu.md"
tv="$dir/references/thu-vien-khung.md"
cc="$dir/references/concept.md"
vs="$dir/references/vong-slice.md"
sl="$dir/references/slate.md"
lv="$dir/references/luat-van-phong.md"
kf="$dir/references/khuon-file.md"
qt="$dir/references/quy-trinh.md"
qtro="$dir/references/quan-tro.md"
khg="$dir/references/ke-hoach-gamemaster.md"
sd="$dir/references/sau-dungeon.md"
qmoc="$dir/references/quan-tro-moc.md"
REQ=("$skill" "$th" "$tv" "$cc" "$vs" "$sl" "$lv" "$kf" "$qt" "$qtro" "$khg" "$sd" "$qmoc")
for f in "${REQ[@]}"; do
  [ -f "$f" ] || { echo "check-skill: thiếu file bắt buộc ${f#$dir/}"; exit 2; }
done

fail=0
say() { printf 'check-skill: %s\n' "$1"; fail=1; }

# 1. frontmatter — chỉ đọc khối giữa hai dòng --- đầu file
fm="$(awk 'NR==1 && $0!="---"{exit} NR>1 && $0=="---"{exit} NR>1{print}' "$skill")"
[ -n "$fm" ] || say "SKILL.md không mở bằng khối frontmatter ---"
grep -q '^name: gamify$' <<<"$fm"      || say "frontmatter thiếu 'name: gamify'"
grep -q '^description:' <<<"$fm"           || say "frontmatter thiếu 'description'"
grep -q '^argument-hint:' <<<"$fm"         || say "frontmatter thiếu 'argument-hint'"
grep -qE '^context:[[:space:]]*["'"'"']?fork' <<<"$fm" && say "frontmatter có 'context: fork' — skill sẽ mất AskUserQuestion"

# 2. link markdown → file tồn tại (bỏ link http)
while IFS= read -r line; do
  src="${line%%:*}"; target="${line#*:}"
  target="${target%%#*}"
  case "$target" in http://*|https://*|'') continue ;; esac
  base="$(dirname "$src")"
  [ -e "$base/$target" ] || say "link hỏng trong ${src#$dir/}: ($target)"
done < <(grep -oH '\]([^)]*)' "$skill" "$dir"/references/*.md | sed 's/:\](\(.*\))$/:\1/')

# 3. tim-hieu.md — năm trục, mục mẫu plan.md, và hai dòng trạng thái trong mẫu
for n in 1 2 3 4 5; do
  grep -q "^### Trục $n — " "$th" || say "tim-hieu.md thiếu heading '### Trục $n — …'"
done
grep -q '^## Mẫu `gamemaster/plan.md`' "$th" || say "tim-hieu.md thiếu mục '## Mẫu \`gamemaster/plan.md\`'"
grep -q '^Trạng thái: ' "$th"  || say "mẫu plan.md trong tim-hieu.md thiếu dòng 'Trạng thái: '"
grep -q '^Việc kế tiếp: ' "$th" || say "mẫu plan.md trong tim-hieu.md thiếu dòng 'Việc kế tiếp: '"

# 3b. thu-vien-khung.md — ≥ 4 khung, mỗi khung đủ 8 nhãn, Hàng cấm 4 dòng;
#     concept.md — ba mục cổng
khung_nums=$(grep -o '^## Khung [0-9]* — ' "$tv" | awk '{print $3}')
nkhung=$(printf '%s\n' "$khung_nums" | grep -c .)
[ "$nkhung" -ge 4 ] || say "thu-vien-khung.md có $nkhung khung, cần ít nhất 4 heading '## Khung N — …'"
dup=$(printf '%s\n' "$khung_nums" | sort | uniq -d | tr '\n' ' ')
[ -z "$dup" ] || say "thu-vien-khung.md có số khung trùng: $dup"
NHAN=('Game gốc' 'Vòng lặp một phiên' 'Hình tiến trình' 'Thất bại'
      'Tông và kiểu đặt tên' 'Hợp với việc' 'Cách ánh xạ bản đồ kỹ năng' 'Nhược điểm điển hình')
for n in $khung_nums; do
  # chỉ lấy khối của heading đầu tiên mang số n (trùng số đã báo ở trên)
  khung="$(awk -v n="$n" '$0 ~ "^## Khung " n " — " {if (seen) exit; seen=1; on=1; next} /^## /{on=0} on' "$tv")"
  for l in "${NHAN[@]}"; do
    grep -q "^\*\*$l:\*\*" <<<"$khung" || say "thu-vien-khung.md khung $n thiếu nhãn '**$l:**'"
  done
done
cam="$(awk '/^## Hàng cấm/{on=1; next} /^## /{on=0} on' "$tv")"
[ -n "$cam" ] || say "thu-vien-khung.md thiếu mục '## Hàng cấm'"
ncam=$(grep -c '^- \*\*' <<<"$cam")
[ "$ncam" -eq 4 ] || say "mục Hàng cấm có $ncam gạch đầu dòng in đậm, cần đúng 4"
for h in 'Mẫu bản tả concept' 'Phép kiểm khớp' 'Cổng chọn'; do
  grep -q "^## $h" "$cc" || say "concept.md thiếu mục '## $h'"
done

# 3c. vong-slice.md — hai mục đọc mỗi slice; ke-hoach-gamemaster.md — Bước A
#     và mẫu gamemaster.md 9 mục; sau-dungeon.md — ba mục sau dungeon cuối
for h in 'Bảng slice của game' 'Cổng duyệt'; do
  grep -q "^## $h" "$vs" || say "vong-slice.md thiếu mục '## $h'"
done
grep -q '^## Bước A' "$khg" || say "ke-hoach-gamemaster.md thiếu mục '## Bước A …'"
grep -q '^## Mẫu `gamemaster.md`' "$khg" || say "ke-hoach-gamemaster.md thiếu mục '## Mẫu \`gamemaster.md\`'"
# chỉ lấy phần trong khối ```` … ```` ngay sau heading, kẻo mục "## N." ở phần nối sau cũng được tính
mau="$(awk '/^## Mẫu `gamemaster.md`/{on=1; next} on && /^````/{if (seen) exit; seen=1; next} on' "$khg")"
for n in $(seq 1 9); do
  grep -q "^## $n\. " <<<"$mau" || say "mẫu gamemaster.md trong ke-hoach-gamemaster.md thiếu mục '## $n. …'"
done
grep -q 'Bảng từ vựng' <<<"$mau" || say "mẫu gamemaster.md trong ke-hoach-gamemaster.md thiếu 'Bảng từ vựng' ở mục 7 (nguồn tên của từng game)"
for h in 'Slice `tools.md`' 'Kiểm cuối' 'Sửa và mở rộng'; do
  grep -q "^## $h" "$sd" || say "sau-dungeon.md thiếu mục '## $h'"
done
grep -qi 'bảng từ vựng' "$kf" && grep -qi 'bảng từ vựng' "$qtro" || say "khuon-file.md hoặc quan-tro.md không trỏ tới bảng từ vựng"

# 3d. slate.md — ba mục
for h in 'Máy chấm' 'Hợp đồng kết quả' 'Cảm giác game'; do
  grep -q "^## $h" "$sl" || say "slate.md thiếu mục '## $h'"
done

# 3e. luat-van-phong.md — 18 điều + mục D; khuon-file.md — 8 file
for code in A1 A2 A3 A4 A5 A6 B1 B2 B3 B4 B5 B6 B7 B8 B9 C1 C2 C3; do
  grep -qE "^\*\*$code[ .(]" "$lv" || say "luat-van-phong.md thiếu điều $code"
done
grep -q '^## D\. ' "$lv" || say "luat-van-phong.md thiếu mục '## D. …' (vòng kiểm)"
for h in 'world.md' 'dungeons/NN' 'quests.md' 'character.md' 'journal.md' 'boss/' 'slate/' 'gamemaster.md'; do
  grep -qE "^## \`$h" "$kf" || say "khuon-file.md thiếu mục '## \`$h…'"
done

# 3f. quan-tro.md — 6 mục đọc mỗi lần chơi; quan-tro-moc.md — 2 mục đọc khi
#     có lần đánh mới hay tới hạn vùng; SKILL.md phải trỏ tới quan-tro.md
for h in 'Vào chế độ play' 'Mở phiên' 'Dẫn phiên' 'Bài kiểm cố định và cấp' 'Kết phiên' 'Không có sổ chung'; do
  grep -q "^## $h" "$qtro" || say "quan-tro.md thiếu mục '## $h'"
done
for h in 'Chấm bài kiểm cố định' 'Qua vùng'; do
  grep -q "^## $h" "$qmoc" || say "quan-tro-moc.md thiếu mục '## $h'"
done
grep -q 'references/quan-tro.md' "$skill" || say "SKILL.md không trỏ tới references/quan-tro.md (nhánh play)"
# ba file đọc-một-lần chỉ tới được qua lời trỏ trong hai file nóng; mất lời trỏ là mất cả mục
grep -q 'quan-tro-moc.md' "$qtro" || say "quan-tro.md không trỏ tới quan-tro-moc.md (chấm bài kiểm, qua vùng sẽ không bao giờ được đọc)"
grep -q 'ke-hoach-gamemaster.md' "$vs" || say "vong-slice.md không trỏ tới ke-hoach-gamemaster.md (bước A sẽ không bao giờ được đọc)"
grep -q 'sau-dungeon.md' "$vs" || say "vong-slice.md không trỏ tới sau-dungeon.md (tools.md, kiểm cuối sẽ không bao giờ được đọc)"

# 4. quy-trinh.md — 32 mã
for n in $(seq 1 32); do
  grep -q "^$n\. \[$n\] " "$qt" || say "quy-trinh.md thiếu điều kiện '$n. [$n] …' trong danh sách ba mươi hai"
done

# 5. hai điều SKILL.md không được có
grep -qi 'commit' "$skill" && say "SKILL.md chứa chữ 'commit'"
grep -q 'skills/flow' "$skill" && say "SKILL.md trỏ agent tới file của skill i:flow"

if [ "$fail" -eq 0 ]; then
  echo "check-skill: sạch — frontmatter, link, 5 trục + mẫu plan.md, $nkhung khung × 8 nhãn + Hàng cấm, 3 mục concept, 2 mục vòng slice + bước A với mẫu gamemaster 9 mục + 3 mục sau dungeon, 3 mục slate, 18 điều văn phong, khuôn 8 file, 6 + 2 mục quản trò, 32 mã."
fi
exit "$fail"
