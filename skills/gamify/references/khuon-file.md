# Khuôn tám file của một game

**Đây là gì.** Mỗi game là một thư mục `docs/games/<slug>/` với đúng bộ file
dưới đây, tên file cố định bằng tiếng Anh (từ ngữ game), nội dung theo ngôn
ngữ người dùng. Người chơi chỉ cần theo `world.md` và lời người dẫn trên
trang chơi; các file khác mở khi game bảo. `run-check.sh <game-dir>` kiểm
phần máy kiểm được của khuôn này; phép thử năm câu (`luat-van-phong.md` mục
D) kiểm phần còn lại.

**Khung và từ vựng.** Khuôn này là *khung*: tên file, thứ tự mục, cái gì
phải có. Mọi *tên* — trang chơi, người dẫn, đơn vị một lần chơi, bài kiểm
cố định, nơi trao chiêu, tài nguyên, từng chiêu — là của riêng game, đặt ở
giai đoạn concept và ghi một lần ở bảng từ vựng (`gamemaster.md` mục 7).
File này gọi chúng bằng từ khung trong ngoặc nhọn, kiểu `<người dẫn>`,
`<lần chơi>`; khi dựng thì thay bằng tên của game. Ví dụ trong file này lấy
từ game forex đầu tiên (trang "Slate", người dẫn Ilo, lần chơi là một
"đêm", bài kiểm Guardian, nơi trao chiêu Shrine, chiêu Sight / Lure) và chỉ
là ví dụ.

**Ba luật đứng trên khuôn.** (1) "Write for understanding" của SKILL.md.
(2) File người chơi thuần game: không "ngoài đời là", không tên kỹ năng thật,
không tên lĩnh vực; mỗi tên game kèm **việc tay trên trang**. (3) 18 điều
của [luat-van-phong.md](luat-van-phong.md): mở khi viết, không đợi lúc
kiểm; mã trong ngoặc ở dưới (A3, B6…) trỏ vào đó.

| File | Ai đọc | Ai ghi | Trần |
|---|---|---|---|
| `world.md` | người chơi, đọc trước lần chơi đầu | người dựng (skill) | 180 dòng |
| `dungeons/NN-<tên>.md` | người chơi, khi vào vùng | người dựng | 80 dòng mỗi vùng |
| `quests.md` | người chơi, khi muốn biết đang có việc gì | `<người dẫn>` | bảng |
| `character.md` | người chơi | `<người dẫn>` | bảng |
| `journal.md` | người chơi đọc lại; người dẫn dùng để ứng biến kết vùng | `<người dẫn>`, từ sổ chung của trang | mỗi lần chơi một khối |
| `boss/` | không ai mở ngoài trang | máy (script trong `slate/`) | `set.json` + `README.md` |
| `gamemaster.md` | người dẫn, mỗi phiên | người dựng; người dẫn chỉ ghi ghi chú | 9 mục (`vong-slice.md`) |
| `slate/` | trang chơi | người dựng | `index.html` + nguồn |

## `world.md` — mười mục, đúng thứ tự

Heading cố định bằng chữ trung tính (script kiểm đúng chữ); thân mục dùng
tên của game. Heading giữ chữ khung (vùng, lần chơi) mà game gọi khác thì
chỗ đầu tiên nói một lần "vùng ở đây là phòng", "một lần chơi ở đây là
một đêm", rồi cả file chỉ dùng chữ của game:

1. `## Đây là game gì` — ba tới năm câu: game là gì, chơi mỗi ngày bao lâu, điều khác thường của riêng game này: việc tay mà game khác không bắt làm (forex: gọi đỉnh đáy trên một ngày cũ trước khi nó chạy lại). "Không tiền, không xếp hạng" để ở mục 9.
2. `## Bạn là ai` — vai, `<người dẫn>` (tên + một câu), ẩn dụ trung tâm (ví dụ forex: Slate sống lại ngày cũ; Shrine trao Rune). Giới thiệu ẩn dụ ở đây trước khi mục nào dùng nó (C1).
3. `## Bắt đầu thế nào` — mở trang nào, `<người dẫn>` dẫn lần chơi đầu, không cần đọc gì khác trước; giữa các lần chơi gặp `<người dẫn>` trong chat bằng `/i:gamify play <thư mục game>`, chơi xong nói "xong" (B6); hai thứ đừng mở, `gamemaster.md` và `boss/`, vì mở là lộ đề và luật chấm của chính mình (A1).
4. `## Lần chơi đầu tiên` — việc tay theo thứ tự, kể cả `<bài kiểm>` lần 0.
5. `## Một lần chơi` — kể theo thời gian: các khúc, mỗi khúc mấy phút và để làm gì (A3, B2); kênh: trang ghi gì, người chơi gõ gì, `<người dẫn>` đọc gì (B5, B6).
6. `## Hôm nào mệt` — ba lối rẽ tên trung tính; nghỉ không phạt + hệ quả hạn nói thật (B8).
7. `## Bài kiểm cố định` — heading chung cho mọi game; tên riêng của bài kiểm trong game này (Guardian, Tree Sentinel…) đứng trong câu đầu của mục. Nó là gì, đánh khi nào, lên cấp nghĩa là gì; đứng trước mục vùng vì vùng nhắc tới nó (A4).
8. `## Các vùng` — câu "lần đọc đầu chỉ cần vùng 1"; vùng 1 một đoạn bằng chữ (cảnh, nơi trao chiêu, qua vùng được gì); các vùng sau mỗi vùng một dòng trong bảng hạn cuối mục (tên, một câu cảnh, hạn; chưa nói chiêu), bảng "để tra, không cần nhớ" (A5).
9. `## Điều game không có` — tiền, xếp hạng, đếm ngày, phạt.
10. `## Bảng tra tên` — hai cột: tên trong game → việc tay trên trang (C2). Mọi tên riêng ở `world.md` phải có ở đây, và phải có mặt trong `gamemaster.md`; tên chỉ có ở một file vùng thì giải nghĩa ngay tại chỗ (C2).

Một câu hạ gánh đứng ngay trước mục 5 (A6): "Bạn không cần thuộc luật: `<người dẫn>` giữ luật và nhắc lúc chơi."

## `dungeons/NN-<tên>.md` — bốn mục

1. `## Vào vùng` — cảnh khi tới, một đoạn; không lộ biến cố mở (`<người dẫn>` kể).
2. `## Chiêu trong vùng` — heading chung; mỗi chiêu (và nơi trao nó, nếu concept có): việc tay trên trang, thế nào là trúng, và giới hạn mấy lần một lần chơi nếu có.
3. `## Qua vùng` — điều kiện bằng lời (`<bài kiểm>` cuối vùng đạt gì), hạn ngày (trễ hạn thì sao đã nói ở mục "Hôm nào mệt" của `world.md`, không nhắc lại); phần thưởng bằng lời (chiêu hay nơi trao chiêu kế mở, một `<phần thưởng cốt truyện>`).
4. `## Lần đọc đầu` — hai ba câu: chỉ cần nhớ gì.

Tên file: `NN` hai chữ số theo thứ tự đường tiến trình của gamemaster.md mục 6, tên kebab-case tiếng Anh (`01-the-plateau.md`). Dungeon thêm sau nối số mới.

## `quests.md`

Câu dẫn một dòng rồi bảng: `Nhiệm vụ | Làm gì | Trạng thái (mở / xong)`. Người dẫn mở dòng mới khi một chiêu hay nơi trao chiêu mở, đóng khi xong. Tối đa năm dòng mở cùng lúc.

## `character.md`

Bảng một cột giá trị: Tên (người chơi đặt ở lần chơi đầu hoặc "chưa nhớ"), Vùng, Ngày đầu (D0), Hạn vùng, Chiêu đã mở, Cấp từng chiêu, các bộ đếm mà bảng từ vựng khai báo (ví dụ forex: Chuỗi, Kill), Số lần chơi, `<bài kiểm>` gần nhất (ngày + hai số có nhãn), `<phần thưởng cốt truyện>` đã có. Người dẫn ghi sau `<bài kiểm>` và khi qua vùng.

## `journal.md`

Mở đầu hai câu: sổ này `<người dẫn>` ghi từ trang, bạn không phải chép; cuối mỗi vùng `<người dẫn>` đọc lại để kể bạn đã đi qua vùng đó thế nào (B2). Thêm một câu nói số dạng a/b trong khối là trúng trên số đã đặt. Rồi mỗi lần chơi một khối, mẫu sinh từ bảng từ vựng và chép vào `gamemaster.md` mục 7:

````markdown
## <Lần chơi> N — <ngày thật> · <đề> <id mờ>
- <mỗi chiêu đã mở, một cụm, ngăn bằng ·>: <tên chiêu> <trúng>/<đặt>, sót <n>
- <trường riêng đọc ra chữ theo bảng từ vựng, nếu có>
- Ghi chú: "<dòng người chơi gõ>" (hoặc —)
- <người dẫn>: <một câu>
````

Ví dụ forex: `## Đêm 3 — 24/09/2026 · ngày bốc 463e3b5f` / `- Sight 2/3, sót 4 · Lure 1/1, cắn 0` / `- Kiếm: chưa mở · chuỗi 1` / `- Ghi chú: —` / `- Ilo: …`.

Ngoài khối lần chơi, sổ có hai loại khối vùng do người dẫn ghi: `## Vùng N mở — <ngày>` chép nguyên biến cố mở của `gamemaster.md` mục 6 (≤ 6 dòng), và `## Vùng N qua — <ngày>` chép biến cố đóng người dẫn nói trong chat cùng `<phần thưởng cốt truyện>`. Hai khối này vừa để người chơi đọc lại, vừa là dấu cho người dẫn biết vùng đã mở hay đã qua; cách dùng ở `quan-tro.md`.

## `boss/`

`set.json` do máy sinh (script trong `slate/`), niêm phong: một object `{"seed": n, "items": [ {n, key, …} × <số đề> ]}`, số đề đúng bằng dòng "Bộ đề:" ở `gamemaster.md` mục 4 — `run-check.sh` đòi đúng dạng và đúng số đó. Không ai mở ngoài trang, kể cả người dẫn; `README.md` ba câu: đây là gì, ai mở (chỉ trang), người chơi đừng mở vì mở là hỏng thước đo của chính mình.

## `slate/`

Cái máy của game (`slate.md`). Trang artifact phải là **một** file, nên bản
sinh đôi bằng JS nằm ngay trong `index.html`, không có bước dựng trang:

| File | Làm gì |
|---|---|
| `engine.py` | Luật của `gamemaster.md` mục 2 thành code; hằng số ở đầu file. |
| `index.html` | Trang chơi, mang luôn bản JS của engine. |
| `cases.py` + `tests/` | Một ca kiểm mỗi luật, ở ngưỡng và ngay dưới ngưỡng. |
| `export_fixtures.py` | Xuất `data/fixtures.json` để hai bản engine đối chiếu. |
| script tải và dựng dữ liệu | → `data/` (đề + đáp án tính sẵn + `ids.json` bảng id mờ → đề thật). |
| script niêm phong bộ đề | → `boss/set.json`, seed cố định. |

File người chơi chỉ nhắc URL trang bằng tên trang trong game, không nhắc gì
bên trong `slate/`.

## `gamemaster.md`

Theo mẫu 9 mục ở `vong-slice.md`. Riêng mục 6 (đường tiến trình) mang **biến cố mở** mỗi vùng (≤ 6 dòng, trang kể khi người chơi vào vùng lần đầu) và **`<phần thưởng cốt truyện>`** (3 dòng, trao khi qua bài kiểm cuối vùng) — người chơi nghe lúc chơi, không đọc trước (C3). Mục 7 mang bảng từ vựng và mẫu khối journal ở trên. Mục 8 mang một dòng `Từ cấm ở file người chơi: a, b, c` — tên lĩnh vực và kỹ năng thật của game này (ví dụ forex: forex, EURUSD, ICT, thanh khoản, order block…); `run-check.sh` đọc dòng đó để soi file người chơi.
