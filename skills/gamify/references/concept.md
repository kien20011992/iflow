# Giai đoạn 2 — Concept: ba cách khoác game lên bản đồ kỹ năng, người dùng chọn một

**Đây là gì.** Sau khi bản đồ kỹ năng được duyệt, skill lấy ba khung khác
nhau trong [thu-vien-khung.md](thu-vien-khung.md), khoác mỗi khung lên bản
đồ thành một "concept": thế giới, vai, người dẫn, một phiên chơi trông thế
nào, và cái gì trong game là cái gì trong việc thật. Người dùng đọc ba
concept, chọn một, chỉnh một vòng, khoá. Concept đã khoá là cái mọi
dungeon, quest, cấp sau này phải theo; đổi concept sau khoá là làm lại từ
giai đoạn này.

**Vì sao ba, vì sao khác khung.** Một khung cho mọi việc là cách phiên bản
trước làm, ra game chán. Ba concept cùng một khung thì chọn cũng như không.
Ba khung khác nhau cho người dùng thấy việc của mình có thể là chuỗi đền,
là sân săn, hay là hầm bốc ngẫu nhiên — và chọn cái mình muốn sống trong
đó nhiều tháng.

**Thư viện là điểm xuất phát, không phải hàng rào.** Khung có sẵn giúp
vòng đầu ra nhanh và có nền nghiên cứu. Người dùng không ưng cả ba là
chuyện bình thường của một cuộc trò chuyện, không phải lỗi của ai và không
phải tổn thất: vòng sau lấy từ bất kỳ thể loại game dựng bài bản nào
(xem "Khi người dùng không ưng"). Cái cố định là luật mọi khung phải mang
và phép kiểm khớp, không phải danh sách khung.

**Hai đường vào giai đoạn.** Người dùng có hình dung riêng về game (một
cơ chế, một cốt truyện, một cảm giác — "mỗi lệnh là tung một chiêu, có
kill thì có chữ hiện") thì đi **đường 2**: lấy concept của họ, không trình
thư viện. Không có hình dung thì đi **đường 1**: ba khung từ thư viện.
Lệnh "không lấy gu người chơi" chỉ áp cho nguồn khi người dùng không đưa
gì; người dùng đưa thì đó là quyết định của họ.

**Luật viết:** "Write for understanding" của SKILL.md, áp cả cho bản tả concept.

## Vào giai đoạn

- `plan.md` phải có bảng kỹ năng con "(đã duyệt <ngày>)". Không có thì quay
  về giai đoạn 1.
- Đặt `Trạng thái: đang dựng — giai đoạn: concept`, `Việc kế tiếp: viết ba
  concept và đưa người dùng chọn`.

## Chọn ba khung

Đọc bản đồ theo hai cột:

- Cột **Học sau** có chuỗi dài (dòng sau cần dòng trước) → việc có phần
  tuần tự → Đền thử thách hợp.
- Nhiều dòng cùng bậc, cùng làm trên một sân (cùng biểu đồ, cùng bộ đề) →
  song song → Thợ săn hợp.
- Cột **Dấu hiệu đo được** đòi đề ngẫu nhiên, tua nhiều lần → Hầm ngẫu
  nhiên hợp.
- Bản đồ có một "setup trọn" nhiều pha phải đọc tell → Vùng đất đổ nát hợp.

Chọn ba khung khớp nhất, **cố ý khác nhau**; ghi một dòng lý do mỗi khung.
Bốn khung đều khớp thì bỏ khung có nhược điểm nặng nhất với người chơi này
(ví dụ 20 phút/ngày thì lượt-1-giờ của Hầm ngẫu nhiên phải co lại — nói rõ
trong bản tả nếu vẫn chọn).

## Khi người dùng không ưng

Người dùng bác cả ba, hay nói "cho cái khác", "không thích", "chán": đi
đúng ba bước, bằng lời thường, không tool:

1. **Hỏi một câu xem trượt ở đâu**, gộp trong câu hỏi cuối lời trả lời:
   thế giới, cách chơi mỗi ngày, hay tông giọng? Người dùng trả lời thì
   vòng sau giữ phần họ không chê. Không trả lời mà chỉ bảo "khác đi" thì
   vòng sau đổi cả ba phần. Không hỏi họ thích game gì; nhưng nếu họ tự kể
   ("kiểu Guitar Hero ấy") thì đó là đường 2, đi theo họ.
2. **Lấy thể loại ngoài thư viện.** Bất kỳ thể loại game dựng bài bản nào
   có vòng lặp một phiên, hình tiến trình và cách thất bại rõ: nhịp điệu
   (Rhythm Heaven, Guitar Hero), bắn chữ (The Typing of the Dead), vườn và
   xây (Stardew Valley, Animal Crossing), đua với bóng ma của chính mình
   (Trackmania), xếp hình (Tetris), thám hiểm mở (Outer Wilds), quản lý
   (Papers, Please)… Ba concept vòng sau vẫn cố ý khác nhau và khác vòng
   trước; mỗi cái vẫn phải qua "Phép kiểm khớp" và mang đủ "Luật mọi khung
   phải mang" của thư viện. Hàng cấm không đổi.
3. **Ghi vào `plan.md`** mục "Concept đã trình": thêm dòng "vòng N" với ba
   tên mới và một dòng nói vòng trước trượt ở đâu theo lời người dùng. Khi
   khoá, dòng "Dựa trên" ghi "<thể loại> — <game gốc>". Không
   tự thêm khung vào `thu-vien-khung.md`; thư viện chỉ đổi khi người dùng
   bảo.

Không đếm vòng, không nhắc số vòng với người dùng. Việc chọn concept là
trò chuyện qua lại như hỏi đáp thường; skill đưa cái nhanh trước, người
dùng lái, skill theo.

## Đường 2 — người dùng đưa concept

Người dùng tả hình dung của họ. Trước khi viết gì, hỏi bằng lời thường
đúng hai điều, vì ca chạy thật đã hỏng ở đây: (1) cái họ tả là **đích**
(cái họ sẽ làm khi đã giỏi — "trading là battlefield") hay là **cách chơi
khi đang học**? Đích thì game này là phần trước đích, cần bối cảnh và
gameplay cùng thế giới với đích. (2) Trong hình dung đó, cái nào là cốt
lõi phải giữ (cảm giác tung chiêu, tiếng hô kill) và cái nào chỉ là ví dụ
(cốt truyện họ kể qua)? Rồi viết **một** concept: giữ cốt lõi, nối với bản
đồ kỹ năng bằng bảng cái-này-là-cái-này, cốt truyện theo gợi ý của họ
(hoặc hỏi họ thích lấy cảm hứng từ đâu). Trình, chỉnh tới khi khoá. Người
dùng hỏi "làm sao tốt nhất, hết cái dở" thì trả lời bằng cơ chế của chính
thể loại đó (MOBA: chiêu nhỏ giết lính, chiêu cuối mở theo cấp, mana),
không đổi sang khung thư viện.

## Mẫu bản tả concept

Viết cho người **chọn**. Hai lớp, lớp nào cũng theo luật "viết cho người
hiểu" ở trên.

**Lớp 1 — để chọn, tối đa 12 dòng, lời thường.** Bốn câu, đúng thứ tự:
- *Chơi là gì* — một hai câu, thế giới và vai, không quá ba tên riêng.
- *Một ngày trông thế nào* — từ lúc mở tới "xong rồi, mai gặp", bằng việc
  tay thật (khoanh gì, gõ gì, tua gì) chứ không bằng ẩn dụ.
- *Biết mình giỏi lên bằng gì* — bài kiểm cố định, cái gì mở ra.
- *Cái dở* — ít nhất hai, thật. Concept không có cái dở là chưa viết xong.

Đường 1: ba concept cùng khổ lớp 1, in liền nhau; một dòng cuối "Tôi
nghiêng về … vì …" nếu có. Đường 2: một concept.

**Lớp 2 — hậu trường, đưa khi người dùng đã nghiêng về một concept hoặc
hỏi thêm:**
- **Bảng cái-này-là-cái-này** — 5–8 dòng (đường 2 có thể dài hơn): `yếu tố
  game | dòng # bản đồ | nước đi thật`. Sau khi khoá, bảng chuyển vào
  `gamemaster.md`; file người chơi không bao giờ nhắc.
- **Tiến trình sơ bộ** — dungeon/quest chính theo thứ tự ↔ dòng #; boss =
  bộ đề niêm phong; cái gì mở cái gì.
- **Người dẫn** — tên, một câu tả, luật nói (bao nhiêu câu mỗi lượt).
- **Từ vựng của game** — tên do concept này đặt cho: trang chơi, một lần
  chơi (đêm / chuyến / hiệp…), đề (đơn vị người chơi xử lý mỗi lần), bài
  kiểm cố định, nơi trao chiêu (nếu có), tài nguyên giới hạn lượt (nếu
  có), phần thưởng cốt truyện khi qua vùng, và từng chiêu với mã ngắn.
  Sau khi khoá, danh sách này thành bảng từ vựng ở `gamemaster.md` mục 7,
  nguồn duy nhất cho mọi tên. Không mượn tên của game khác hay của ví dụ
  trong skill.
- **Luật tính điểm nếu concept có điểm/kill** — cái gì tính, cái gì không;
  may rủi phải tách khỏi tiến bộ (tiến bộ theo "chiêu sạch" = đúng lý,
  không theo kết quả giá).

Cả hai lớp không thiên vị trong lời.

## Phép kiểm khớp

Trước khi trình, soi từng concept: ba nước đi thật phải **thấy được** trong
bảng cái-này-là-cái-này và trong "Một phiên" — người chơi đọc xong biết
tay mình sẽ làm gì:

1. Hành động tay trên trang: người chơi bấm, kéo, gõ gì để làm việc thật
   (forex: đánh dấu mức giá trên biểu đồ tua; gõ phím: gõ chữ trên đường
   chạy).
2. Chuẩn đặt trước rồi mới làm: đánh dấu hay ghi "tôi nghĩ X" trước khi
   trang chạy, để so sau.
3. Kết quả tự vào sổ chung của trang; người chơi không chép số. Game không
   máy (plan.md ghi `Máy: không`) thì ghi rõ người chơi báo số nào, dạng gì.

Ẩn dụ che mất một trong ba là concept trượt: viết lại chỗ đó, không trình.
Kiểm thêm: tên riêng tiếng Anh (hoặc tên tự chế viết chữ Latin mang màu
game gốc), không tiếng Việt, mỗi tên lần đầu có nửa câu giải nghĩa; không
cơ chế trong hàng cấm; phiên vừa với phút/ngày của người chơi.

## Cổng chọn

Ca chạy thật cho thấy người dùng từ chối `AskUserQuestion` bốn lần liền
để nói tiếp: khi đang tìm hình dung, họ cần nói, không cần bấm. Vì thế:

0. Trước khi hỏi gì, ghi ngay mục "Concept đã trình" vào `plan.md` (một
   dòng mỗi concept) và đổi `Việc kế tiếp:` thành "người dùng đang chọn
   giữa A/B/C" — phiên bị cắt thì lần sau đọc lại được, không sinh lại ba
   concept khác. Sau mỗi vòng chỉnh, cập nhật dòng đó ("đang nghiêng về B,
   đổi người dẫn").
1. In bản tả (lớp 1) trong lời trả lời. Kết bằng **một câu hỏi bằng lời
   thường**: "Bạn nghiêng về cái nào, hay muốn nói thêm?" (đường 1) /
   "Khoá cái này, hay chỉnh gì?" (đường 2). Không dùng tool ở bước này.
2. Người dùng nói → chỉnh, đưa lớp 2 của concept họ nghiêng về, hỏi lại
   bằng lời. Bác cả ba → mục "Khi người dùng không ưng". Lặp tới khi họ
   nói "khoá" / "được" / "đúng rồi". Không đếm vòng, không coi vòng bị
   bác là tốn kém: người dùng đang tìm, đi theo họ.
3. Chỉ khi người dùng đã nói được và còn một lựa chọn rời nhau (ví dụ ba
   nhánh tên gọi), mới dùng một `AskUserQuestion` để chốt.
4. Không hỏi cơ chế tuỳ chọn ở đây: câu đó thuộc bước A của giai đoạn 3
   (`vong-slice.md`), hỏi một lần, bằng lời thường.

## Ghi vào `plan.md`

Chèn ngay trước khối trạng thái ở cuối file:

````markdown
## Concept đã trình (<ngày>)

- <Tên A> — <kiểu game — game gốc, hoặc "ý của bạn">: <một dòng, và vì sao bị bác nếu bị bác>
- …

## Concept đã khoá (<ngày>)

- Dựa trên: <tên khung — game gốc | "<thể loại> — <game gốc>" | "ý của bạn" + cảm hứng>
- Tên: <tên concept>
- Tông: <hai ba câu>
- Vai: <tên, một câu>; Người dẫn: <tên, một câu>
- Từ vựng: trang <tên>; một lần chơi = <tên>; đề = <tên>; bài kiểm = <tên>; nơi trao chiêu = <tên/—>; tài nguyên = <tên/—>; phần thưởng cốt truyện = <tên>; chiêu: <MÃ> <tên>, …
- Chỉnh so với bản trình: <gì, hoặc "khoá nguyên">
- Nhược điểm chấp nhận: <…>

Mỗi thứ trong game ứng với việc thật nào (bảng này chuyển vào
gamemaster.md khi dựng; file người chơi không nhắc):

| Yếu tố game | Dòng # bản đồ | Nước đi thật |
|---|---|---|

Tiến trình sơ bộ: <danh sách dungeon/quest ↔ dòng #; boss = bộ đề niêm phong>
````

Rồi: thêm tên game và một câu nó là gì vào đoạn mở đầu `plan.md`; dòng
Quyết định "<ngày> — Concept <tên> khoá; đổi concept là chọn lại từ đầu";
`Việc kế tiếp: bắt đầu giai đoạn slice`; và **đi tiếp giai
đoạn 3** ngay trong cùng lượt chạy (SKILL.md, Stage 3) trừ khi người dùng
bảo dừng.
