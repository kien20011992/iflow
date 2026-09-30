# Giai đoạn 1 — Tìm hiểu: từ một việc khó ra bản đồ kỹ năng được duyệt

**Đây là gì.** Giai đoạn đầu của chế độ dựng game. Trước khi nghĩ tới bất kỳ
game nào, skill phải biết việc thật gồm những kỹ năng con nào và cái nào đo
được, người chơi đứng ở đâu, luyện ở đâu mà không mất gì, quản trò chấm được
gì, và đích lớn là gì. Năm thứ đó là **năm trục**, cố định cho mọi việc.
Sản phẩm của giai đoạn là file `docs/games/<slug>/gamemaster/plan.md` với
bản đồ kỹ năng đã được người dùng duyệt. Mọi thứ ở giai đoạn sau (concept,
quest, dungeon, cấp) đều suy ra từ bản đồ này, nên bản đồ sai thì cả game
sai — vì thế duyệt bản đồ là cổng bắt buộc, không bỏ được.

**Vì sao phải hỏi và tra cứu thay vì tự viết.** Chặng tự chia mà không có
bản đồ thì nhiệm vụ không ai biết luyện cái gì. Người mới học cũng không tự
kể được kỹ năng con
— đó chính là lý do họ đi học. Nên bản đồ lấy từ giáo trình (nếu người dùng
có) cộng tra cứu, rồi người dùng duyệt.

## Điều kiện vào

Ba câu, sai một thì dừng, nói rõ việc phải làm trước, và **không tạo thư
mục** nào:

1. Việc kéo dài từ ba tháng trở lên và có kỹ năng để khá lên? (Việc chỉ cần
   ý chí, không có kỹ năng, thì game không giúp.)
2. Dựng được sân luyện không hậu quả — thử sai mà không mất tiền thật, uy
   tín thật, cơ hội thật? (Forex: bar replay, tài khoản demo. Gõ phím: trang
   luyện gõ. Không có gì tương đương thì phải dựng trước khi làm game.)
3. Đặt được chuẩn trước khi hành động — "tôi sẽ làm X vì thấy Y" — để soi
   lại biết mình đọc sai ở đâu?

Ba câu này không hỏi thẳng: câu 1 và 3 suy từ tên việc, câu 2 suy từ câu
trả lời về sân luyện ở lượt 1 (xem "Cách chạy"). Chỉ khi suy không ra thì
hỏi một câu ở lượt 1.

## Năm trục

Mỗi trục: hỏi gì, khi nào coi là đóng, ghi gì vào `plan.md`. Trục nào người
dùng trả lời trọn trong một câu thì đóng ngay, không hỏi thêm.

### Trục 1 — Việc thật: bản đồ kỹ năng

**Hỏi:** người dùng có giáo trình, khoá học, sách nào đang theo không (tên;
đường dẫn hoặc URL nếu có). Đây là câu hỏi duy nhất của trục này; phần còn
lại là tra cứu. Tra cứu chỉ bắt đầu sau khi trục 4 đã đóng, vì cột "dấu
hiệu đo được" phải viết theo kênh báo cáo đã biết — không thì bảng được
duyệt xong lại phải sửa.

**Rút bản đồ:**

- Có giáo trình → mục lục giáo trình là gốc: mỗi mục lớn thường là một kỹ
  năng con hoặc một cụm. Tra cứu web để bù những gì giáo trình không nói:
  dấu hiệu đo được của từng kỹ năng con, thứ tự người ta thường học, kỹ
  năng nào phải có trước kỹ năng nào.
- Không giáo trình → tra cứu web lộ trình phổ biến của lĩnh vực (giáo trình
  chuẩn, lộ trình được nhiều nguồn nhắc). Lĩnh vực có nhiều trường phái
  (trading là ví dụ) thì hỏi lại người dùng theo trường phái nào trước khi
  tra cứu, vì bản đồ chung chung sẽ không khớp.
- Mỗi con số hay thứ tự lấy từ tra cứu ghi tầng nguồn: **giáo trình chính
  chủ** / **nguồn thứ cấp** / **ước lượng** (khi chỉ có một nguồn tóm tắt
  hoặc do mô hình suy ra). Ước lượng ghi rõ là ước lượng ở mọi chỗ nó xuất
  hiện.

**Bản đồ là một bảng 6–12 dòng**, mỗi dòng một kỹ năng con:

| Kỹ năng con | Giỏi nghĩa là làm được gì (nhìn thấy được) | Dấu hiệu đo được | Học sau | Nguồn |
|---|---|---|---|---|

- *Kỹ năng con*: tên gọi thường, bằng ngôn ngữ của việc thật (chưa phải tên
  trong game).
- *Giỏi nghĩa là*: một hành động cụ thể, quan sát được, ví dụ "đánh dấu
  vùng giá quan trọng trên biểu đồ 15 phút trong 30 giây".
- *Dấu hiệu đo được*: thứ quản trò chấm được từ cái người chơi báo về —
  con số chép từ màn hình, kết quả so với đáp án niêm phong, ảnh. "Cảm thấy
  tự tin hơn" không phải dấu hiệu.
- *Học sau*: kỹ năng con nào phải có trước; "—" nếu vào thẳng được.
- *Nguồn*: giáo trình chính chủ (ghi mục/bài) / nguồn thứ cấp (ghi tên) /
  ước lượng.

**Cổng duyệt (bắt buộc):** đưa bảng cho người dùng bằng một
`AskUserQuestion` với ba nhánh: duyệt nguyên / sửa (người dùng nói dòng nào
sai, thiếu gì) / làm lại theo nguồn khác. Sửa xong đưa lại một lần. Chỉ khi
người dùng duyệt thì trục mới đóng. Không được đi sang giai đoạn sau với bản
đồ chưa duyệt.

**Ghi:** bảng đã duyệt và danh sách nguồn (kèm tầng) vào `plan.md`.

### Trục 2 — Người chơi

**Hỏi:** trình độ hiện tại với việc này (mới hoàn toàn / đã học lý thuyết
chưa luyện / đã luyện tới đâu, nói cụ thể); số phút ổn định mỗi ngày dành
được (con số thật, không phải mong muốn).

**Không hỏi** người chơi thích game gì (SKILL.md, Rules).

**Đóng:** khi có hai con số/đoạn trên. **Ghi:** hai dòng.

### Trục 3 — Sân luyện

**Hỏi:** công cụ nào cho phép thử sai mà không mất tiền thật, uy tín thật,
cơ hội thật (tên công cụ, bản miễn phí hay trả phí, giới hạn đã biết); có
dữ liệu nào sẵn để làm bộ đề niêm phong không (kho biểu đồ cũ, bộ đề gõ,
bài tập có đáp án).

**Đóng:** khi có tên công cụ và biết dữ liệu làm đề lấy từ đâu. Nếu người
dùng không chắc công cụ có làm được điều cần (ví dụ bản miễn phí có tua được
khung thời gian đó không), ghi lại là "chưa kiểm, kiểm ở phiên đầu" — không
tra cứu thay, vì giới hạn tài khoản là thứ chỉ người dùng thấy.

**Ghi:** công cụ, giới hạn, nguồn dữ liệu làm đề, điều chưa kiểm.

### Trục 4 — Thước đo

**Hỏi:** khi chơi, người chơi báo được gì cho quản trò: con số chép từ màn
hình (số nào), ảnh chụp, kết quả so với đáp án đã niêm phong, hay chỉ lời tự
kể. Câu này quyết định cột "dấu hiệu đo được" của bản đồ có đứng được không:
dấu hiệu nào không lấy được từ kênh báo cáo thì phải đổi dấu hiệu hoặc đổi
kênh.

**Đóng:** khi biết người chơi gửi gì, dạng gì. Trục này hỏi ở lượt 2,
**trước** khi rút bản đồ: cột "dấu hiệu đo được" viết theo kênh này, nên
bảng đưa duyệt đã là bảng cuối, không phải sửa sau khi duyệt. Dòng nào chỉ
tự khai được thì ghi rõ "không làm điều kiện lên cấp".

**Ghi:** kênh báo cáo (người chơi gửi gì, dạng gì) và dòng nào của bản đồ
chỉ tự khai.

### Trục 5 — Chân trời

**Hỏi:** đích lớn, một câu, không có tiền, không có con số — "tôi muốn trở
thành người … / làm được …". Người dùng thường trả lời có tiền hoặc có số
("kiếm 1000 USD/tháng"); khi đó hỏi lại một lần: đằng sau con số đó là năng
lực gì.

**Đóng:** khi có một câu đúng dạng. **Ghi:** dòng `Đích lớn:` ở đầu `plan.md`, và
từ đây không nhắc lại ở bất kỳ file nào của game — nó là cái neo, được cất
đi.

## Cách chạy

1. Đọc `$ARGUMENTS`. Cái gì đã có ở đó thì không hỏi.
2. **Lượt 1** — một `AskUserQuestion`, đúng bốn câu: (a) trình độ hiện tại
   (trục 2); (b) phút ổn định mỗi ngày (trục 2); (c) sân luyện — công cụ
   nào, và dữ liệu làm bộ đề lấy từ đâu, gộp trong một câu (trục 3); (d)
   có giáo trình đang theo không (trục 1). Câu nào `$ARGUMENTS` đã trả
   lời thì thay bằng câu điều kiện vào còn mờ, nếu có.
3. Suy ba điều kiện vào từ tên việc và câu (c). Sai một → dừng, nói việc
   phải làm trước, không tạo thư mục, báo cáo và kết thúc.
4. **Ghi `plan.md` ngay** — tạo `docs/games/<slug>/gamemaster/` (luật slug
   trong SKILL.md) và viết `plan.md` theo mẫu dưới với những gì đã có; dòng
   `Việc kế tiếp:` ghi "hỏi kênh báo cáo và chân trời, rồi tra cứu bản đồ".
   Phiên bị cắt ở đây thì lần sau gọi lại bằng thư mục là chạy tiếp, không
   hỏi lại.
5. **Lượt 2** — một `AskUserQuestion`, hai câu: kênh báo cáo (trục 4) và
   chân trời (trục 5; người dùng đưa số hoặc tiền thì hỏi lại một lần
   ngay trong câu này bằng nhánh "Other"). Ghi vào `plan.md`, đổi `Việc kế
   tiếp:` thành "tra cứu bản đồ kỹ năng".
6. **Tra cứu:** rút bản đồ theo trục 1, cột "dấu hiệu đo được" viết theo
   kênh báo cáo vừa đóng. Dùng web khi có; không có web thì viết từ hiểu
   biết của mô hình và ghi tầng "ước lượng" cho mọi dòng. Ghi bản nháp vào
   `plan.md` dưới heading `## Kỹ năng con cần luyện (chờ duyệt)` trước khi
   hỏi; giai đoạn 2 chỉ mở khi heading đã đổi thành "(đã duyệt <ngày>)".
7. **Lượt 3** — một `AskUserQuestion`, một câu: cổng duyệt bản đồ (duyệt
   nguyên / sửa / làm lại theo nguồn khác). Người dùng sửa → sửa rồi đưa
   lại một lần (lượt 4).
8. Đổi heading thành `## Kỹ năng con cần luyện (đã duyệt <ngày>)`, đổi `Việc kế tiếp:` thành "viết concept và
   đưa người dùng chọn", rồi **đi tiếp giai đoạn 2** ngay trong cùng lượt
   chạy (SKILL.md, Stage 2) trừ khi người dùng bảo dừng.

Ba lượt là chuẩn, bốn khi có sửa. Nhiều hơn năm lượt là dấu hiệu đang hỏi
thứ nên tra cứu, hoặc tra cứu thứ nên hỏi.

## Mẫu `gamemaster/plan.md`

Hồ sơ thiết kế; người chơi không mở, chế độ play chỉ chèn ghi chú. Người
dùng được đưa đường dẫn file này (SKILL.md, Report): thân bài viết cho họ
theo `~/.claude/rules/docs.md`, không slice, trục, cổng duyệt, giai đoạn,
khung. Khối `## Trạng thái để làm tiếp` luôn là mục cuối, chỗ duy nhất ghi
tiến độ; mục mới chèn ngay trước nó.

````markdown
# Kế hoạch game — <tên việc thật>

<hai ba câu cho người dùng mở lại file sau vài tuần: game luyện việc gì, cho ai; concept khoá rồi thì thêm tên game và một câu nó là gì>

Đích lớn: <một câu, không tiền, không số — viết một lần, không nhắc lại ở file nào khác>

## Người chơi

- Trình độ: <…>
- Phút mỗi ngày: <…>

## Sân luyện

- Công cụ: <tên, bản, giới hạn đã biết>
- Dữ liệu làm bộ đề niêm phong: <lấy từ đâu>
- Chưa kiểm: <điều gì, kiểm ở phiên nào>

## Thước đo

- Kênh báo cáo: <người chơi gửi gì, dạng gì>
- Chỉ tự khai (không làm điều kiện lên cấp): <dòng nào của bản đồ, hoặc "không có">

## Kỹ năng con cần luyện (đã duyệt <ngày>)

<câu dẫn: bảng này là gì, ai duyệt, dùng để suy ra gì>

| Kỹ năng con | Giỏi nghĩa là làm được gì | Dấu hiệu đo được | Học sau | Nguồn |
|---|---|---|---|---|
| … | … | … | … | … |

Nguồn:
- <giáo trình chính chủ: tên, mục/bài>
- <nguồn thứ cấp: tên, URL>
- <ước lượng: dòng nào, vì sao>

## Quyết định

- <ngày> — <một dòng, kèm lý do nếu đắt để dựng lại>

## Ghi chú từ phiên chơi

<người dẫn (chế độ play) nối một dòng khi người chơi xin nới luật hay báo máy chấm lệch: ngày + lời họ; không sửa luật giữa vùng>

## Trạng thái để làm tiếp

Trạng thái: đang dựng — giai đoạn: tìm hiểu
Việc kế tiếp: <một câu mệnh lệnh, ví dụ "tra cứu bản đồ kỹ năng" hay "viết concept và đưa người dùng chọn">

<!-- giai đoạn: tìm hiểu | concept | slice | chơi được. Sau thêm: `Máy: không — <lý do>` (nếu có), bảng slice. -->
````
