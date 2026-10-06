# Giai đoạn 3 — Vòng slice: kế hoạch gamemaster trước, rồi từng dungeon

**Đây là gì.** Concept đã khoá là cái vỏ. Giai đoạn này dựng cái ruột: một
kế hoạch thật, ghi rõ chiêu nào luyện kỹ năng nào, lên cấp bằng con số gì,
thua thì mất gì, bài kiểm cố định chấm bằng gì. Kế hoạch đó là
`gamemaster.md`, người chơi không mở, người dẫn đọc mỗi phiên. Duyệt xong
kế hoạch thì cắt game thành các slice: mỗi dungeon một slice, chơi được
ngay từ dungeon đầu.

**Luật viết.** Cả gamemaster.md lẫn lời trình cho người dùng theo
"Write for understanding" của SKILL.md.

**File này giữ phần đọc ở mọi slice.** Bước A (slice 01) và mẫu
`gamemaster.md` ở [ke-hoach-gamemaster.md](ke-hoach-gamemaster.md); slice
`tools.md`, kiểm cuối, sửa và mở rộng ở [sau-dungeon.md](sau-dungeon.md),
đọc khi tới lúc.

## Vào giai đoạn

- `plan.md` phải có mục "Concept đã khoá". Chưa có thì quay về giai đoạn 2.
- Đặt `Trạng thái: đang dựng — giai đoạn: slice`, `Việc kế tiếp: hỏi cơ
  chế tuỳ chọn rồi viết gamemaster.md`.

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
   hai việc. Một, soát mã nguồn trang có đủ bốn điều đầu của mục "Cảm giác
   game" trong `slate.md` — kẻ địch hiện sau khi khoá đáp án, hình của thứ
   người chơi đặt, boss có thanh máu, tiếng và chuyển động — và có thật mọi
   thứ file người chơi và mục 2, 7
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

