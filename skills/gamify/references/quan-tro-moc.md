# Chế độ play — mốc: chấm bài kiểm cố định và qua vùng

File của chế độ play, đọc thêm bên `quan-tro.md` khi sổ chung có lần
đánh mới, hoặc khi hôm nay tới "Hạn vùng" ở `character.md`. Luật khi nào
bảo đánh ở mục "Bài kiểm cố định và cấp" của `quan-tro.md`.

## Chấm bài kiểm cố định


Một lần đánh là **mới** khi ngày thật của `at` sau ngày ở dòng "<bài kiểm>
gần nhất" của `character.md`; dòng đó chưa có ngày thì mọi lần đánh đều
mới. Chấm từng lần đánh mới, theo thứ tự `at`:

1. Chỉ chấm chiêu **đã mở** (dòng "Chiêu đã mở" của `character.md`). Chiêu
   chưa mở có điểm trong doc thì bỏ qua, không nhắc.
2. Với mỗi chiêu đã mở, đọc thang ở `gamemaster.md` mục 3. Cột nào của
   `scores.<mã>` so với thang là do mục 3 ghi; mặc định trúng =
   `precision`, không sót = `recall`. Cấp mới = cấp cao nhất mà mọi cột mục
   3 đòi cùng đạt; cấp 1 khi có điểm (đã bấm). **Cấp không tụt:** thấp hơn
   cấp đang ghi thì giữ cấp cũ.
3. Chiêu cuối (nếu game có, mục 3 nói) mở khi điều kiện ở mục 3 thoả trong
   **cùng một lần** đánh.
4. Ghi: `character.md` dòng "Cấp" và "<bài kiểm> gần nhất" (ngày thật của
   `at` + hai số mỗi chiêu, mỗi số kèm tên `world.md` dùng, kiểu
   "23/09/2026 — <chiêu A> trúng 60 · không sót 40", không "60/40" trơ);
   `character/main` bằng `update` với `if_version` (`levels`,
   `unlocked`, trường riêng khi đổi); `quests.md` đóng dòng lần 0, hay dòng
   "bài kiểm cuối vùng" nếu có.
5. Nói một câu cấp, bằng tên chiêu và số cấp; không nói phần trăm trừ khi
   người chơi hỏi. Nếu vừa ghi `character/main`, dòng chỉ việc thêm "tải
   lại trang" — trang chỉ đọc nhân vật lúc nạp.

## Qua vùng

Điều kiện đọc ở `gamemaster.md` mục 3: tới hạn vùng **và** chiêu của vùng đạt
cấp qua vùng ở lần đánh cuối vùng. Kiểm ngay sau khi chấm một lần đánh mà
hôm nay ≥ hạn.

Qua: nói theo đúng thứ tự, trong một lượt —

1. **Biến cố đóng**, ứng biến 3–5 dòng từ các khối journal của vùng đó: lần
   chơi nào đáng nhớ, lần đánh cuối đổi so với lần 0 thế nào. Giọng của
   người dẫn, từ của trang, không tổng kết kiểu báo cáo.
2. **Phần thưởng cốt truyện** nguyên văn ba dòng từ `gamemaster.md` mục 6
   (tên của nó trong game ở bảng từ vựng).
3. Tên nơi trao chiêu mới mở (nếu game có), và một dòng chỉ việc: tải lại
   trang, mai vào vùng mới.

Ghi: `journal.md` khối `## Vùng N qua — <ngày thật>` gồm biến cố đóng và
phần thưởng cốt truyện đúng như đã nói; `character.md` (Vùng, Hạn vùng kế
theo mục 6, Chiêu đã mở, phần thưởng đã có); `character/main` (`region`,
`unlocked`); `quests.md` (đóng dòng vùng cũ, mở dòng cho mỗi chiêu hay nơi
trao chiêu mới). Vùng mới được **mở** ở phiên sau, bằng biến cố mở của nó
(mục "Mở phiên" của `quan-tro.md`, bước 5). Vùng kế có ở `gamemaster.md` mục 6 mà chưa có
file `dungeons/` thì vẫn nói và ghi biến cố đóng cùng phần thưởng (khối
`## Vùng N qua`), nhưng chưa ghi
phần còn lại; dòng chỉ việc: vùng kế chưa dựng, người dựng gọi
`/i:gamify <game> dựng tiếp`. Phiên đầu tiên sau khi file vùng kế có mặt
thì ghi nốt phần còn lại, rồi mở vùng mới như bước 5 của "Mở phiên" ở
`quan-tro.md`.

Chưa qua khi tới hạn: lùi hạn bảy ngày, một lần cho mỗi vùng — sửa "Hạn
vùng" ở `character.md`, ghi một dòng vào khối lần chơi gần nhất của journal;
vẫn chưa đủ sau lần lùi thì vùng kéo dài, không huỷ, không nhắc lại. Nghỉ
dài (khoảng cách giữa hai lần chơi liền nhau lớn hơn ngưỡng ở mục 5) → hạn
tự lùi đúng số ngày nghỉ, một lần, cùng cách ghi.

