# Giai đoạn 3 — Vòng slice: kế hoạch gamemaster trước, rồi từng dungeon

**Đây là gì.** Concept đã khoá là cái vỏ. Giai đoạn này dựng cái ruột: một
kế hoạch thật, ghi rõ chiêu nào luyện kỹ năng nào, lên cấp bằng con số gì,
thua thì mất gì, bài kiểm cố định chấm bằng gì. Kế hoạch đó là
`gamemaster.md`, người chơi không mở, người dẫn đọc mỗi phiên. Duyệt xong
kế hoạch thì cắt game thành các slice: mỗi dungeon một slice, chơi được
ngay từ dungeon đầu.

**Vì sao kế hoạch đi trước dungeon.** Người dùng đòi "kế hoạch định từ
đầu": mỗi quest, mỗi cấp phải nối với một kỹ năng con ngay lúc thiết kế,
không phải bịa dần khi dựng từng dungeon. Nên duyệt gamemaster = duyệt kế
hoạch, rồi mới có dungeon.

**Luật viết.** Cả gamemaster.md lẫn lời trình cho người dùng theo
"Write for understanding" của SKILL.md.

## Vào giai đoạn

- `plan.md` phải có mục "Concept đã khoá". Chưa có thì quay về giai đoạn 2.
- Đặt `Trạng thái: đang dựng — giai đoạn: slice`, `Việc kế tiếp: hỏi cơ
  chế tuỳ chọn rồi viết gamemaster.md`.

## Bước A — kế hoạch gamemaster (slice 01 của mọi game)

1. **Hỏi cơ chế tuỳ chọn** bằng một `AskUserQuestion` riêng, `multiSelect`,
   bốn món của [thu-vien-khung.md](thu-vien-khung.md) với mô tả điền cho
   việc này, "(gợi ý)" ở món hợp khung. Đây là câu duy nhất của bước A dùng
   tool; hỏi trước khi viết vì mỗi món chọn thành một luật trong file.
   Người dùng không trả lời thì ghi "không chọn" và đi tiếp.
2. **Viết `docs/games/<slug>/gamemaster.md`** theo mẫu ở cuối file này.
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
   thang là quyết định giữa chừng (xem "Sửa và mở rộng").

## Bảng slice của game (bước B)

Ghi vào khối trạng thái ở cuối `plan.md` (mẫu ở `tim-hieu.md`), không vào
thân bài; mẫu cố định, không tự thêm loại slice khác:

| # | Slice | Dạy gì (dòng # bản đồ) | Hạn dự kiến | Trạng thái |
|---|---|---|---|---|
| 01 | Kế hoạch gamemaster | — | (ngày duyệt) | done |
| 02 | Dữ liệu + máy chấm (`slate/`): dữ liệu thật, luật mục 2 và 4 thành code, mô phỏng, key bài kiểm cố định | — | — | todo |
| 03 | Trang chơi (`slate/index.html`, tên trong game theo bảng từ vựng): chơi được, bấm là chấm, trúng/sót hiện ngay, lưu kết quả theo hợp đồng `slate.md` | — | — | todo |
| 04 | Dungeon 1 + luật một phiên + bài kiểm lần 0 | <dòng #> | <ngày> | todo |
| 05 | Dungeon 2 | <dòng #> | <ngày> | todo |
| … | Dungeon N | … | … | todo |
| 0N+1 | `tools.md`: tả hệ thống đã dựng và cách làm mới, cộng phần còn đề xuất | — | — | todo |
| 0N+2 | Kiểm cuối | — | — | todo |

Hai slice máy (02, 03) chỉ bỏ khi việc thật không mô phỏng được từ dữ
liệu — khi đó ghi dòng `Máy: không — <lý do>` vào khối trạng thái của
plan.md (run-check.sh đọc dòng này để bỏ kiểm `slate/` và `boss/`), và
dungeon chạy trên file + số báo tay.

- Trạng thái: `todo` / `doing` / `done` / `needs-redo` / `retired`. Đúng
  một slice `doing` mỗi lúc; hai dòng `Trạng thái:`, `Việc kế tiếp:` của
  plan.md trỏ vào slice đó. Ghi ngay lúc đổi: bắt đầu slice là một lần
  ghi (hàng `doing`, `Việc kế tiếp` là bước đầu của nó), và `Việc kế tiếp`
  đổi ở mỗi bước của cổng duyệt dưới đây.
- Số slice là danh tính: thêm dungeon sau thì nối số mới, không chen, không
  đánh lại số.
- Hạn dự kiến của dungeon = hạn ghi trong đường tiến trình của
  gamemaster.md (hạn đầu ngắn nhất, cỡ một tuần; các hạn sau vài tuần).

## Cổng duyệt (bước C — chạy từng slice)

Mỗi slice dungeon đi đúng năm bước:

1. **Đọc** plan.md (bảng slice, concept, mục Quyết định, mục Ghi chú từ
   phiên chơi, các dòng "chưa sửa" trong Kết quả của slice trước) và
   gamemaster.md (mục của dungeon này trong đường tiến trình).
2. **Kế hoạch slice, bằng lời thường, ≤ 12 dòng:** dungeon này dạy gì
   (dòng # nào), người chơi thấy gì khi vào, một phiên trong đó trông thế
   nào, bao lâu, boss là gì và chấm bằng gì, file nào sẽ sinh ra hay đổi.
   Hỏi bằng lời: "Duyệt hay chỉnh?" — `AskUserQuestion` chỉ khi có lựa chọn
   rời (ví dụ hai cách dựng boss). Dungeon 2 trở đi dựng liền: một kế
   hoạch cho cả nhóm, mỗi dungeon 2–3 dòng; người dùng nói "từng cái" thì
   trình từng dungeon. Duyệt xong, ghi ngay mục `## NN — <tên phần việc
   bằng lời thường>` với "Kế hoạch đã duyệt" (3–5 dòng) cho từng slice
   được phủ, chèn trước khối trạng thái, rồi mới dựng. Slice đã có dòng đó
   thì bỏ bước này, trừ khi nó quay lại vì `needs-redo`: khi đó trình phần
   làm lại (≤ 5 dòng) và hỏi duyệt.
3. **Dựng** đúng kế hoạch đã duyệt: file người chơi theo khuôn
   `khuon-file.md`, phần trang của dungeon này. Các đề ở `boss/` không đổi
   (niêm phong ở slice 02; game không máy thì dựng ở dungeon 1).
   `quests.md` chỉ viết ở dungeon 1; sau đó người dẫn mở dòng khi người
   chơi tới.
4. **Kiểm:** người đọc mới không ngữ cảnh đọc file người chơi "tính tới
   dungeon N", trả lời năm câu; script kiểm cấu trúc `run-check.sh` (lệnh
   ở SKILL.md, slice 04); và
   **cổng vui** dưới đây cho slice trang (03) và dungeon 1.

   Cổng vui — trang chấm đúng chưa phải là game. Claude không bấm được
   trang, nên người dùng là người trả lời. Giao phiên 1: ghi phần Kết quả
   đã có (người đọc mới, run-check) vào mục `## 04`, đặt `Việc kế tiếp:
   chờ phiên 1 — người dùng chơi bằng /i:gamify play <game>, rồi gọi
   /i:gamify <game> dựng tiếp để hỏi cổng vui`, và lượt dừng ở đây. Sau
   phiên 1 ở chế độ play, hỏi năm câu có/không bằng lời thường, ghi nguyên
   lời vào plan.md cùng một dòng Quyết định trả lời dòng ghi chú "phiên 1
   xong" (nêu ngày của nó); một "không" là chưa qua, slice 03 hay 04
   `needs-redo` tuỳ họ chê gì; làm lại xong chỉ hỏi lại những câu đã
   "không":
   1. Có lúc nào phải quyết định thật (chọn gì, đánh dấu đâu, đi tiếp hay
      dừng), hay chỉ làm theo lệnh?
   2. Bấm có thấy phản hồi ngay, bằng hình và tiếng?
   3. Có lúc căng và lúc thả trong cùng lần chơi?
   4. Chơi xong thấy thế giới đổi (cảnh, quái, thanh máu, chiêu mở), hay
      chỉ thấy số?
   5. Muốn mở lần nữa không?
   Trước khi giao trang, ở slice 03 và ở mọi slice đổi trang, Claude làm
   hai việc. Một, soát mã nguồn trang có đủ bốn thứ đầu (mục "Cảm giác
   game" của `slate.md`) và có thật mọi thứ file người chơi và mục 2, 7
   của gamemaster.md hứa trang hiện: chữ, màu, tiếng, nghi thức. Hai, **chạy chính
   đoạn chấm của trang ở ngoài trình duyệt** trên vài kiểu chơi thật —
   làm đúng hết, sai một nước, sai rồi lùi sửa — và đọc kết quả bằng mắt:
   đúng kỷ luật "đọc mắt một đề thật" của `slate.md`, nhưng cho đường nhập
   liệu. Lỗi ở đường nhập liệu thường lọt qua cả test lẫn soát mã, và lộ
   ngay ở bước này. Cả hai vẫn chỉ là soát, không phải bằng chứng; bằng
   chứng là lời người dùng.

   Hiệu chỉnh sau bài kiểm lần 0 — ở slice dungeon 1 khi sổ đã có lần 0,
   hoặc khi `dựng tiếp` gặp dòng ghi chú "lần 0 xong" của chế độ play:
   đọc `tests/<id>` của lần 0, đối chiếu từng số "(ước lượng)" ở
   gamemaster.md mục 2–4 với điểm thật (chiêu nào kịch cấp ngay lần 0 là
   ngưỡng lỏng; chiêu nào 0 điểm là sai số chặt hay trang chưa đo được);
   đổi số theo gạch "Đổi số hay luật" ở mục Máy chấm của `slate.md`, bỏ
   chữ "(ước lượng)" ở số đã sửa; trình ≤ 5 dòng "đổi số nào, từ đâu ra",
   ghi một dòng Quyết định, nêu ngày của dòng ghi chú nó trả lời nếu có. Cấp đã cấp ở lần 0 theo ngưỡng cũ thì chấm lại
   ngay, vì luật "cấp không tụt" chỉ áp từ sau hiệu chỉnh: đổi thang mục 3
   thì chấm từ `scores`; đổi luật hay sai số mục 2 thì cho máy chấm chấm
   lại nước đi `actions` của lần 0; không có nước đi thì giữ cấp và ghi lý
   do. Sổ chưa
   có lần 0 thì slice dungeon 1 vẫn `done` sau cổng vui; hiệu chỉnh chạy
   sau, khi `dựng tiếp` gặp dòng ghi chú "lần 0 xong" của chế độ play.
5. **Ghi** "Kết quả" (đạt/không, bằng chứng, lệch) vào mục `## NN` đã mở
   ở bước 2, viết cho người chưa xem chat; đổi trạng thái ở bảng trong
   khối cuối; `Việc kế tiếp` trỏ slice kế; báo một dòng: slice nào, đạt
   hay không, còn mấy slice. Mọi bước đều ghi ngay, nên phiên bị cắt giữa
   slice thì lần sau đọc plan.md là biết đang ở bước mấy.

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
   qua cổng duyệt như thường. Không chọn thì ghi "không" và slice này
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
5. Cổng vui của dungeon 1: năm câu đều "có", mỗi câu tính lần trả lời gần
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
  slice với số mới; rồi chạy như một slice dungeon thường. Chiêu mới thì
  kế hoạch slice nói luôn nó chấm thế nào; duyệt xong mới thêm dòng ở mục
  2, 3, 7 của gamemaster.md và đổi máy theo gạch "Đổi số hay luật" của
  `slate.md`.
- **Sửa** (game không hiệu quả): ghi dòng Quyết định vào plan.md trước
  (sửa gì, vì sao, bằng chứng từ nhật ký hay lời người dùng). Đổi số hay
  luật chấm thì chỉ đi gạch "Đổi số hay luật" của `slate.md`, không dựng
  lại dữ liệu, không bốc lại đề; sửa khác thì đánh `needs-redo` slice liên
  quan và chạy lại nó.
- **Đổi concept** sau khoá = làm lại từ giai đoạn 2; bảng slice cũ
  `retired` toàn bộ.

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
