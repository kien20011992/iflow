# Sau dungeon cuối — slice `tools.md`, kiểm cuối, sửa và mở rộng

Đọc file này khi mọi dungeon đã `done` (hai slice cuối của bảng), hoặc
khi SKILL.md gọi nhánh `thêm dungeon:` / `sửa:`. Cổng duyệt của từng slice
ở `vong-slice.md`; mẫu `gamemaster.md` ở `ke-hoach-gamemaster.md`.

## Slice `tools.md` (sau dungeon cuối)

`tools.md` là file cho người dùng ở vai người thiết kế, không phải người
chơi: cái máy của game làm bằng gì, làm mới thế nào, và cái gì mới chỉ là
đề xuất. Viết khi mọi slice dungeon đã `done`, hoặc khi người dùng gọi
`<game-dir> sửa: viết tools.md`. Ba mục, mỗi mục mở bằng một câu nói nó là
gì:

1. `## Máy đã dựng` — bảng `File | Làm gì | Làm mới bằng lệnh nào`: nguồn
   dữ liệu và lệnh tải lại; máy chấm và lệnh chạy test; lệnh xuất
   fixtures; lệnh dựng và publish lại trang; bộ đề niêm phong và luật
   "không sinh lại giữa vùng". Lệnh chép nguyên từ script thật, đã chạy
   một lần.
2. `## Đề xuất` — tối đa ba công cụ chưa dựng, mỗi cái ba dòng: đo thêm
   được gì (dòng # bản đồ), tốn bao nhiêu (giờ), đổi gì cho người chơi.
   Không đề xuất thứ chỉ hay mà không nối với một dòng bản đồ.
3. `## Người dùng chọn` — hỏi bằng lời thường "dựng cái nào, hay không
   cái nào?"; mỗi cái chọn thành một slice mới nối số vào bảng slice, chạy
   qua cổng duyệt của `vong-slice.md` như thường. Không chọn thì ghi "không" và slice này
   `done`.

## Kiểm cuối (slice cuối của bảng)

Chạy khi mọi slice khác `done`. Không viết gì mới; chỉ soát và ghi. Sáu
điều, mỗi điều một dòng đạt/không kèm bằng chứng thật (output lệnh, ngày
phiên chơi):

1. `run-check.sh <game-dir>` (lệnh ở SKILL.md) sạch.
2. Test máy chấm xanh và bộ ca fixtures hai bản (Python, JS) khớp.
3. Mọi dungeon trong bảng slice `done`, mỗi cái có "Kết quả" trong plan.md;
   mọi dòng Ghi chú từ phiên chơi đã có quyết định.
4. Phép thử năm câu với người đọc mới qua trên bộ file người chơi hiện tại.
5. Cổng vui (ở "Cổng duyệt" của `vong-slice.md`) của dungeon 1: năm câu đều "có", mỗi câu tính lần trả lời gần
   nhất của nó, hoặc người dùng miễn (ghi nguyên văn). Còn câu "không", hoặc chưa hỏi, là không
   đạt: slice 03 (trang) hay 04 (dungeon 1) `needs-redo` tuỳ họ chê gì.
6. `gamemaster.md` không còn số "(ước lượng)" nào chưa hiệu chỉnh sau bài
   kiểm cố định lần 0; còn thì liệt kê và ghi lý do. Lần 0 chưa đánh thì
   ghi "chờ lần 0": không tính là trượt, không đánh `needs-redo`.

Đạt cả sáu → hai dòng trạng thái của plan.md thành `Trạng thái: chơi được — hoàn tất`
/ `Việc kế tiếp: chơi; sửa hay thêm dungeon gọi nhánh sửa`. Không đạt →
điều nào không đạt thành một dòng Quyết định và slice liên quan
`needs-redo`; kiểm cuối vẫn `todo`.

## Sửa và mở rộng

Nhánh `<game-dir> thêm dungeon: …` và `<game-dir> sửa: …` của SKILL.md chạy
đúng ba mục dưới đây; người dùng nói muốn gì khi gọi, skill không tự suy.

- **Thêm dungeon** (kỹ năng mới): thêm dòng vào bản đồ kỹ năng nếu là kỹ
  năng con mới (người dùng duyệt phần thêm); thêm hàng vào đường tiến
  trình của gamemaster.md ở chỗ trống, nhận hạn riêng; thêm hàng vào bảng
  slice với số mới; rồi chạy như một slice dungeon thường qua "Cổng duyệt"
  của `vong-slice.md`. Chiêu mới thì
  kế hoạch slice nói luôn nó chấm thế nào; duyệt xong mới thêm dòng ở mục
  2, 3, 7 của gamemaster.md (mẫu ở `ke-hoach-gamemaster.md`) và đổi máy
  theo gạch "Đổi số hay luật" của `slate.md`.
- **Sửa** (game không hiệu quả): ghi dòng Quyết định vào plan.md trước
  (sửa gì, vì sao, bằng chứng từ nhật ký hay lời người dùng). Đổi số hay
  luật chấm thì chỉ đi gạch "Đổi số hay luật" của `slate.md`, không dựng
  lại dữ liệu, không bốc lại đề; sửa khác thì đánh `needs-redo` slice liên
  quan và chạy lại nó qua "Cổng duyệt" của `vong-slice.md`.
- **Đổi concept** sau khoá = làm lại từ giai đoạn 2; bảng slice cũ
  `retired` toàn bộ.

