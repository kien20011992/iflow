# Kế hoạch gamemaster — bước A của vòng slice và mẫu `gamemaster.md`

Đọc file này ở slice 01 của mọi game, và khi nhánh "Thêm dungeon" của
`sau-dungeon.md` sửa mục 2, 3, 6, 7 của `gamemaster.md`. Các slice khác
đọc `vong-slice.md`.

## Bước A — kế hoạch gamemaster (slice 01 của mọi game)

1. **Hỏi cơ chế tuỳ chọn** bằng một `AskUserQuestion` riêng, `multiSelect`,
   bốn món của [thu-vien-khung.md](thu-vien-khung.md) với mô tả điền cho
   việc này, "(gợi ý)" ở món hợp khung. Đây là câu duy nhất của bước A dùng
   tool; hỏi trước khi viết vì mỗi món chọn thành một luật trong file.
   Người dùng không trả lời thì ghi "không chọn" và đi tiếp.
2. **Viết `docs/iflow/<slug>-<id>/game/gamemaster.md`** theo mẫu ở cuối file này.
   Mục 9 của mẫu lấy từ mục "Ba mươi hai điều kiện thiết kế" của
   [quy-trinh.md](quy-trinh.md): đọc mục đó trước khi điền.
   Mọi con số (ngưỡng, sai số, số đề, phút) phải có; số nào chưa có căn cứ
   thì ghi "(ước lượng — hiệu chỉnh sau bài kiểm lần 0)". Không để ô trống.
3. **Trình cho người dùng bằng lớp 1, lời thường, tối đa 18 dòng:** lên
   cấp bằng gì và ngưỡng lấy từ đâu; một phiên dài bao nhiêu, mấy lượt;
   thua thì mất gì giữ gì; bài kiểm cố định là gì, chấm bằng gì, dữ liệu
   từ đâu; điều gì còn là ước lượng; phần máy (slice 02–03): trang hiện
   gì, lưu gì. Kèm đường dẫn file để họ mở nếu muốn. Kết bằng câu hỏi bằng
   lời: "Duyệt kế hoạch này, hay chỉnh chỗ nào?"
4. Chỉnh theo lời họ, trình lại lớp 1 phần đã đổi, tới khi họ nói duyệt.
   Ghi dòng Quyết định vào plan.md: "<ngày> — gamemaster.md và phần máy
   duyệt", và ghi luôn "Kế hoạch đã duyệt" vào mục `## 02` và `## 03`.
   Duyệt gamemaster = duyệt "kế hoạch định từ đầu"; sau đó đổi ngưỡng hay
   thang là quyết định giữa chừng (xem "Sửa và mở rộng" ở `sau-dungeon.md`).

## Mẫu `gamemaster.md`

Tài liệu ẩn gộp luật quản trò. Người chơi không mở. Chế độ play đọc file
này mỗi phiên. Chín mục, đúng thứ tự, đúng số; mỗi bảng có câu dẫn nói nó
là gì.

````markdown
# Gamemaster — <tên game>

Người chơi không mở file này. Người dẫn đọc nó mỗi phiên và chấm theo nó,
không tự nới.

## 1. Chân trời

<một câu, chép đúng từ plan.md; không xuất hiện ở bất kỳ file người chơi nào>

## 2. Bảng nối

<câu dẫn: bảng này nối mỗi thứ trong game với một kỹ năng thật và luật máy chấm; máy chấm được dựng đúng theo cột cuối, nên cột đó phải tính được từ dữ liệu, không mơ hồ>

| Yếu tố game | Dòng # bản đồ | Nước đi thật trên trang (bấm gì, giới hạn mấy lần) | Dấu hiệu đo được | Luật máy chấm và sai số |
|---|---|---|---|---|

## 3. Thang

- Cấp mỗi kỹ năng con: 1–5. Lên cấp khi <dấu hiệu> đạt <ngưỡng> ở bài kiểm cố định (bảng dưới).
- Kỹ năng cuối (vào lệnh / tương đương) mở khi: <điều kiện>.
- Qua dungeon khi: <hạn> và <ngưỡng>; trao: <năng lực hay quyền mới, không điểm>.
- Cấp / điểm / chữ hiện chỉ là da; cái quyết định là bảng này.

| Kỹ năng con | Cấp 1 | Cấp 2 | Cấp 3 | Cấp 4 | Cấp 5 |
|---|---|---|---|---|---|

## 4. Bài kiểm cố định

- Bộ đề: <số đề>, mỗi đề là <gì>, đáp án máy tính từ <dữ liệu nào> theo luật mục 2.
- Nguồn dữ liệu: <nguồn, miễn phí hay không, đã kiểm tải chưa>; niêm phong ở `boss/`, người chơi không thấy đề nào là đề nào.
- Chu kỳ: đánh lần 0 ngày <…>, đánh lại <khi nào>; mỗi lần bốc <n> đề trong bộ.
- Sai số cho phép từng loại đáp án: <bảng>.

## 5. Luật một phiên

- Mỗi ngày: <n> lượt (ràng buộc tài nguyên: <tên trong game>); thời gian mỗi khúc: <mở / căng / thả / kết, phút>.
- Ba lối rẽ, tên trung tính: <quan sát / chậm / hoãn — tên trong game>.
- Dừng sạch khi hết việc; nghỉ không phạt; trễ hạn dungeon thì lùi một tuần, không huỷ.
- Sáu câu phải có trả lời: lượt thiếu có bù không; trạng thái ngoài danh sách thì sao; thời gian mỗi khúc có đủ khi <việc tay chậm nhất>; nhịp lượt các phiên sau khác phiên 1 thế nào; hạn khi nghỉ dài; lịch phiên so với hạn (mấy phiên/tuần là đủ).

## 6. Đường tiến trình

<câu dẫn>

| Dungeon | Dạy dòng # | Hạn | Boss (bài kiểm) | Biến cố mở (viết sẵn, ≤ 6 dòng) | Trao khi qua (chiêu / nơi trao chiêu mới + phần thưởng cốt truyện 3 dòng, viết sẵn) |
|---|---|---|---|---|---|
| … | … | … | … | … | … |
| (chỗ trống — dungeon thêm sau) | | | | | |

## 7. Luật quản trò

- Nói: <tối đa mấy câu mỗi lượt>; không bình luận lối rẽ; đọc ngưỡng từ file này.
- Đọc kết quả từ trang, không chấm tay. Phiên Claude ở chế độ play: URL trang (artifact) <ghi khi trang dựng xong, slice 03 của game; trước đó "chưa có">, sổ chung đọc bằng `ArtifactData` ở ba bộ sưu tập `sessions/<id>`, `tests/<id>`, `character/main`. Định dạng kết quả: Hợp đồng kết quả ở `slate.md` của skill. Ghi: `journal.md` <lúc nào, dòng gì>; `character.md` <khi nào đổi>; `quests.md` <khi nào mở/đóng>.
- Bảng từ vựng — nguồn duy nhất cho mọi tên của game này. Chế độ play, file người chơi và trang đều đọc từ đây; không tên nào từ game khác hay từ ví dụ trong skill được dùng lại nếu concept không tự sinh ra nó:

<câu dẫn: cột "khung" là khái niệm chung của skill, cột "trong game này" là tên concept đặt (tên riêng tiếng Anh không mạo từ; từ chỉ đơn vị như một lần chơi, đề là từ tiếng Việt của thế giới game; mỗi thứ một tên), cột cuối là việc tay hay cách đọc số ra chữ>

| Khung | Trong game này | Việc tay / đọc là |
|---|---|---|
| trang chơi | <tên> | <người chơi mở gì> |
| người dẫn | <tên> | <một câu về giọng> |
| một lần chơi | <đêm / chuyến / hiệp / …> | <dài bao nhiêu, đề là gì> |
| vùng | <vùng / phòng / tầng / …> | <khác chữ "vùng" thì `world.md` nói một lần ở mục Các vùng> |
| đề | <tên đơn vị dữ liệu người chơi xử lý> | <id mờ tra ở đâu> |
| bài kiểm cố định | <tên> | <đánh khi nào> |
| nơi trao chiêu | <tên, hoặc "—" nếu concept không có> | |
| tài nguyên giới hạn lượt | <tên, hoặc "—"> | <trường riêng trong sổ chung> |
| phần thưởng cốt truyện | <tên> | <trao khi qua vùng> |
| chiêu `<MÃ>` | <tên> | <bấm gì; `hits` đọc là …, `missed` đọc là …; trường riêng nếu có> |
| … | | |

- Mẫu khối journal một lần chơi (theo `khuon-file.md`, tên thay từ bảng trên): <chép mẫu đã điền>.
- Nghi thức: <câu / chữ hiện khi qua bài>; im lặng ở chỗ khác.
- Biến cố mở dungeon: viết sẵn ở mục 6; biến cố đóng: ứng biến từ journal.md, không viết sẵn.
- Bằng chứng đã giỏi: do người dẫn cấp theo ngưỡng mục 3, không tự cấp.

## 8. Cơ chế

- Chọn: <…>. Không chọn: <…>.
- Cấm, luôn: may mắn ở điểm; chuỗi ngày; xếp hạng; tiền ở điểm hay thưởng.
- Từ cấm ở file người chơi: <tên lĩnh vực và kỹ năng thật của game này, cách nhau bằng dấu phẩy — run-check.sh đọc dòng này>

## 9. Danh sách kiểm 32 điều

<câu dẫn: điều nào của quy-trinh.md thoả bởi mục nào; điều thuộc dungeon ghi "→ dungeon">

| Điều | Thoả bởi |
|---|---|
| [1] … [32] | mục … / → dungeon |
````
