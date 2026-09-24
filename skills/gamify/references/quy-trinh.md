# Quy trình mười hai bước — biến một việc khó dài hạn thành game

Sao từ `docs/shape/game-hoa-viec-kho/slice-05-quy-trinh-tong-quat.md` (vault
Notebooks) ngày 2026-09-14, cập nhật cùng ngày theo take 2 của quy trình (cốt
truyện đầy đủ; văn phong tự giải nghĩa), rút gọn phần giải thích, giữ nguyên
bước, đầu ra và điều kiện qua bước. Đổi quy trình thì đổi cả hai chỗ bằng tay;
không có cơ chế tự đồng bộ. Ba mươi hai điều kiện [1]–[32] ở cuối file là danh
sách kiểm; bảng đối chiếu cho biết điều nào gắn vào bước nào.

## Trong v2

Từ phiên bản 2 của skill, file này là **danh sách kiểm**, không còn là quy
trình chạy tuần tự. Skill chạy theo ba giai đoạn (tìm hiểu → concept →
vòng slice, xem SKILL.md); mỗi bước dưới đây đã có chỗ trong giai đoạn nào
đó, và 32 điều ở cuối là thứ kế hoạch gamemaster và từng dungeon phải thoả.

| Bước cũ | Ở v2 nằm ở |
|---|---|
| 0 điều kiện vào, 2 nước đi nhỏ nhất, 5 thang đo | giai đoạn tìm hiểu (`tim-hieu.md`: điều kiện vào, trục thước đo, bản đồ kỹ năng) |
| 1 đích lớn viết một lần rồi cất | trục chân trời của tìm hiểu; chép một lần vào mục 1 của `gamemaster.md` |
| 7 cốt truyện, 11 menu cơ chế | giai đoạn concept (`concept.md`: bản tả, cổng khoá); cơ chế tuỳ chọn hỏi ở bước A của vòng slice |
| 3 ràng buộc, 4 thất bại, 6 trục thời gian, 8 chặng, 9 hạn, 12 quản trò | `gamemaster.md` mục 3–7 (`vong-slice.md`) |
| 10 mười giờ đầu | dungeon 1 (slice 04 của game, sau hai slice máy: dữ liệu + máy chấm, trang chơi) |

32 điều chia hai nhóm khi kiểm: **nhóm kế hoạch** — [3] [4] [5] [9] [11]
[12] [14] [17] [18] [19] [20] [23] [24] [25] [26] [29] [30] — phải thoả
ngay trong `gamemaster.md` (mục 9 của file đó ghi điều nào thoả bởi mục
nào); **nhóm dungeon** — [1] [2] [6] [7] [8] [10] [13] [15] [16] [21] [22]
[27] [28] [31] [32] — kiểm khi dựng từng dungeon. Phần dưới đây giữ nguyên
văn từ v1 để tra.

Năm bộ phận của một game, mỗi bộ phận trả lời một lý do người ta bỏ cuộc:

| Bộ phận | Trả lời cho |
|---|---|
| Ba chân | Vì sao muốn chơi: nước đi hiện hệ quả ngay; ít luật mà nhiều nước đi hay; thấy rõ mình khá lên theo năng lực |
| Nền thất bại | Vì sao thua không đuổi đi |
| Trục thời gian | Vì sao mệt mà mai vẫn mở: lượt, nghỉ, dừng, quay lại |
| Khung chặng | Vì sao không bị đích lớn đè |
| Quản trò | Vì sao tự chơi một mình mà không tự lừa |

Hai điều cấm xuyên suốt: tiền không nằm trong kế hoạch (thang điểm không gắn
lãi lỗ, phần thưởng không quy ra tiền, không cơ chế nào lấy tiền làm mồi); mục
tiêu lớn không phải thành phần phân tích (viết một lần rồi cất).

Một luật văn phong xuyên suốt (14/09): **mọi tên, bảng, con số tự giải nghĩa
ngay tại chỗ xuất hiện đầu** — nó là gì trong việc thật, người chơi làm gì với
nó. Không dòng thông số trơ. Bảng nào cũng có câu dẫn trước bảng. Áp cho hồ sơ
và cho mọi file quản trò sinh ra sau này.

## Bước 0 — Kiểm điều kiện vào

Ba câu, sai một thì dừng:

1. Việc kéo dài từ ba tháng và có kỹ năng để khá lên?
2. Dựng được vùng luyện không hậu quả — thử sai mà không mất tiền thật, uy tín
   thật, cơ hội thật? Không có thì dừng quy trình và nói việc phải làm trước.
3. Đặt được chuẩn trước khi hành động — "tôi sẽ làm X vì thấy Y" — để soi lại
   biết mình đọc sai ở đâu?

**Đầu ra:** ba câu trả lời có; mô tả một dòng cho vùng luyện.
**Qua bước khi:** cả ba câu là có.

## Bước 1 — Viết đích lớn một lần, rồi cất

Một câu, không hơn, không có tiền, không có con số; ghi ở dòng "chân trời" đầu
hồ sơ. Từ đây không xuất hiện trong danh sách việc, thang điểm hay chặng nào.

**Đầu ra:** một câu ở dòng chân trời.
**Qua bước khi:** [26].

## Bước 2 — Nước đi nhỏ nhất và cách hiện hệ quả

Xác định "một nước đi": hành động nhỏ nhất mà sau vài phút biết được hệ quả và
truy được hệ quả về quyết định của mình. Ba việc con: đặt chuẩn trước mỗi nước
("làm X vì Y"; hệ quả so với chuẩn, không so với kết quả cuối); rút ngắn vòng
làm lại (làm lại ngay trong cùng buổi); tha thứ ở tầng tay (lỗi tay run, công
cụ trục trặc không tính là nước đi sai).

**Đầu ra:** định nghĩa một nước đi; mẫu dòng chuẩn; hệ quả hiện thế nào, sau
bao lâu.
**Qua bước khi:** [1] [2] [3].

## Bước 3 — Luật, ràng buộc, bộ công cụ để đổi

Viết bộ luật (≤5 luật; với việc thật thường chính là phương pháp làm việc).
Ràng buộc đủ chặt để mỗi nước đi là một thế lưỡng nan (Rogers: sân Tetris mười
ba cột thì "it's not a game"). Ngẫu nhiên ở đề, không ở điểm. Liệt kê ≥3 công
cụ hoặc ràng buộc để đổi khi một bài đã quen (cùng bài, khác vũ khí).

**Đầu ra:** bộ luật; cách bốc đề ngẫu nhiên; danh sách công cụ để đổi.
**Qua bước khi:** [11] [12] [13].

## Bước 4 — Thiết kế thất bại

Chuyện gì xảy ra khi thua, ở ba tầng nước đi / lượt / chặng. Phân định lượt
(mất được) và kho (không bao giờ mất). Mất mát có điều kiện: có đường chuộc nếu
quay lại kịp. Lối rẽ không bẽ mặt: hạ độ khó, hoãn, quay lại sau — với câu chữ
trung tính ghi sẵn.

**Đầu ra:** bảng hai cột lượt/kho; luật chuộc; danh sách lối rẽ và câu chữ.
**Qua bước khi:** [4] [6] [18].

## Bước 5 — Thang đo năng lực

Một bài kiểm cố định không đổi theo thời gian, quay lại đánh định kỳ (Tree
Sentinel). Cái tích qua các lượt là hiểu biết (sổ một dòng mỗi lượt) cộng một
kho nhỏ. Bằng chứng đã giỏi do quản trò cấp theo ngưỡng ghi sẵn, không tự cấp.
Không bảng xếp hạng.

**Đầu ra:** bài kiểm cố định và chu kỳ; mẫu sổ hiểu biết; danh sách vật trong
kho và điều kiện cấp.
**Qua bước khi:** [5] [9] [14].

## Bước 6 — Trục thời gian: lượt, nghỉ, dừng, quay lại

Một lượt trọn trong một giờ (Nakamura: "a reasonable amount of time to feel
regret yet accept it and move on"). Sau căng có thả được thiết kế trước; đoạn
thả là hệ quả của việc vừa qua được. Chỗ nghỉ là nơi dựng riêng, đi tới chứ
không rơi vào. Mỗi ngày một lượng việc hữu hạn; hết việc là chỗ dừng; nghỉ
không bị phạt, không chuỗi ngày. Cho dừng sạch, không kéo thêm một lượt.

**Đầu ra:** độ dài một lượt; mẫu một buổi (căng – thả – nghi thức kết); lượng
việc mỗi ngày; luật về nghỉ.
**Qua bước khi:** [15] [16] [17] [19] [20].

## Bước 7 — Chia chặng và dựng cốt truyện đầy đủ

Từ đích đã cất, vẽ ngược ra chuỗi chặng. Ba tầng lồng nhau: chặng nhỏ (vài giờ:
nơi an toàn, nguồn để hỏi, cửa ải); chặng trung (một kỹ năng: dạy, kiểm bằng
chính nó, chạy trơn); chặng lớn (một hạn chót, vài tuần; hạn đầu ngắn nhất). Ba
luật: hạn ghi rõ ngày từ đầu chặng; trễ hạn lùi một tuần không huỷ; kết chặng
trao công cụ hoặc quyền mới, rồi về làng, rồi mục tiêu kế lộ ra. Không xếp việc
thành hàng thẳng.

Rồi dựng **cốt truyện đầy đủ** lên chuỗi chặng — sáu thành phần bắt buộc:

1. **Thế giới**: ba tới năm câu tả thế giới và luật của nó, việc thật ánh xạ
   vào cái gì. Không kẻ thù có ý định.
2. **Vai của người chơi**: là ai, tới vì gì (không nhắc đích lớn); vẫn là
   người lên lịch trong hạn — đưa hạn và menu, không đưa lịch.
3. **Người dẫn**: quản trò có tên, một giọng nhất quán, một nét; không quá khứ
   dài.
4. **Biến cố mở và biến cố kết mỗi chặng lớn**: biến cố mở do người dẫn kể ngày
   đầu chặng (ba tới năm câu, viết sẵn); biến cố kết **mọc từ nhật ký và bài
   kiểm của chính người chơi**, người dẫn kể khi tới, **không viết sẵn** — đây
   là cách chống nguội mà slice 03 cảnh báo (cốt truyện tự viết thì biết trước).
5. **Mỗi tên kèm một hai câu tả** ngay dưới tên: tả cảnh **và** nói nó là gì
   trong việc thật, người chơi làm gì với nó. "Cảng nhà" đứng một mình là lỗi;
   "Cảng nhà — nơi mọi hoa tiêu bắt đầu: đứng trên bờ đá nhìn biển, chưa được
   ra khơi, tập gọi tên từng con sóng và viết ra hải luật của mình. Hai tuần
   đầu, chưa vào lệnh, chỉ nhận diện tình huống và viết bộ luật v1." là đúng.
6. **Đặt tên**: mỗi chặng lớn, chặng trung một tên trong thế giới đó.

**Đầu ra:** bản đồ chặng có tên, câu tả, hạn ngày, kỹ năng, cái được trao khi
kết; thế giới, vai, người dẫn; biến cố mở từng chặng viết sẵn, biến cố kết ghi
"mọc từ nhật ký — người dẫn kể khi tới".
**Qua bước khi:** [21] [22] [23] [24] [25] [28] [29] [30] [31] [32].

## Bước 8 — Mười giờ đầu, viết sau cùng

Chỉ làm sau bước 7. Mỗi buổi đầu theo bốn bước học – dùng – lật – chứng minh,
kết trong một buổi (Hayashida: mỗi màn "taught, developed, twisted and then
thrown away in about five minutes"). Bài đầu dạy thái độ, không dạy kỹ thuật:
thua được, bỏ qua được, quan sát trước khi ra tay. Đây là nơi duy nhất được
phép dễ hơn thật.

**Đầu ra:** kế hoạch mười giờ đầu: danh sách buổi, mỗi buổi bốn bước, buổi
đầu dạy thái độ gì.
**Qua bước khi:** [10].

## Bước 9 — Phần thưởng và nghi thức đánh dấu

Điền chỗ trống mà tiền để lại: nghi thức đánh dấu khoảnh khắc qua bài (một câu
cố định) và im lặng ở chỗ khác; khi qua **chặng lớn**, sau câu nghi thức là
biến cố kết do người dẫn kể từ nhật ký (bước 7, thành phần 4) — phần thưởng bằng
chuyện, không viết trước được; quyền mở chặng tiếp (thưởng phải có chỗ dùng);
bằng chứng đã giỏi (bước 5); cảm giác vừa đủ thắng (đến từ độ khó đúng); nhẹ
nhõm (bước 6). Cấm: xếp hạng, chuỗi ngày, mọi thứ quy ra tiền.

**Đầu ra:** câu nghi thức; bảng "qua bài X thì mở Y".
**Qua bước khi:** [7] [8] [32].

## Bước 10 — Quản trò

Quy định ai giữ luật, chấm, mở chặng, không cho tự nới luật. Mặc định là AI
trong phiên trò chuyện, nhận phần trọng tài, không nhận phần đồng đội. Quản trò
đồng thời là **người dẫn** (bước 7, thành phần 3): có tên, giọng nhất quán;
ngày đầu mỗi chặng lớn nói lời dẫn mở (biến cố mở) trước ba dòng, các ngày khác
đúng ba dòng. Bảy việc mỗi ngày: hiện ba dòng (hôm nay / hạn kế / một hai việc
gợi ý — bậc kế hiện, bậc cuối không, đích lớn không bao giờ); bốc đề ngẫu nhiên;
nhận chuẩn trước rồi chấm hệ quả so với chuẩn; giữ luật thất bại; cấp bằng chứng
đã giỏi đúng luật; nói câu nghi thức, câu kết ngày, và biến cố kết khi qua chặng
lớn; từ chối đổi luật giữa chặng. Hai chốt thêm: luật khoá trước khi chơi; dữ
liệu tự động khi có thể. Mọi file quản trò sinh ra (bộ đề, thống kê) mở đầu bằng
ba câu — đây là gì, dùng khi nào, vì sao có — và mỗi bảng có câu dẫn.

**Đầu ra:** hồ sơ giao việc cho quản trò; mẫu ba dòng; tên và giọng người dẫn.
**Qua bước khi:** [27] [31]; quản trò có đủ luật để chấm mà không phải hỏi.

## Bước 11 — Danh sách cơ chế để người chơi chọn

Bày bốn món khuếch đại (cốt truyện, tâm lý, tốc độ, may mắn) cộng yếu tố xã
hội thành danh sách; mỗi cơ chế ghi tác dụng, công dựng, tác dụng phụ; đánh dấu
gợi ý. Người chơi chọn. Danh sách nền ở mục "Cơ chế tuỳ chọn" của `thu-vien-khung.md`; điền cụ thể cho việc này.

**Đầu ra:** danh sách đã điền; kết quả chọn ghi vào hồ sơ.
**Qua bước khi:** người chơi đã chọn; không cơ chế bị cấm nào có trong hồ sơ.

## Bước 12 — Vòng hiệu chỉnh và la bàn xa

Luật chỉ đổi ở cuối chặng lớn, có ghi lý do, lên phiên bản. Tín hiệu trôi về
dễ: bài kiểm qua quá nhanh mà sổ không có gì mới; lối rẽ dùng liên tục; dòng
chuẩn ngày càng ngắn; hoãn hạn lần hai. La bàn xa: một tín hiệu ngoài game (với
việc có tiền: một thống kê dài hạn của vùng luyện, không phải lãi lỗ từng
lượt) đọc một lần ở cuối mỗi chặng lớn, để đổi hướng chặng sau, không đổi điểm
chặng vừa qua.

**Đầu ra:** lịch hiệu chỉnh gắn hạn chặng lớn; tín hiệu trôi; la bàn xa và cách
đọc.
**Qua bước khi:** có lịch hiệu chỉnh; la bàn xa ghi rõ chỗ đọc, lúc đọc, không
chạm thang điểm.

## Ba mươi hai điều kiện thiết kế

Ba mươi điều đầu từ ba tài liệu nghiên cứu case study (slice 01–03 của
dossier); hai điều cuối thêm ngày 14/09 theo quyết định của người dùng; mỗi
điều một câu.

1. [1] Một lượt luyện đủ ngắn để làm lại ngay trong cùng buổi.
2. [2] Kết quả lượt hiện rõ tới mức buộc phải nhìn, nhưng mất ít tới mức không
   đau.
3. [3] Có chuẩn đặt trước khi hành động, để soi lại biết mình đọc sai ở đâu.
4. [4] Thất bại không xoá tiến độ đã tích; chỉ tốn đúng cái vừa dùng.
5. [5] Có một bài kiểm cố định để quay lại so, thay cho điểm theo buổi.
6. [6] Có lối rẽ không bẽ mặt: hạ độ khó, hoãn, quay lại sau.
7. [7] Có nghi thức đánh dấu khoảnh khắc qua bài, và im lặng ở chỗ khác.
8. [8] Qua bài thì mở được chặng tiếp — phần thưởng phải có chỗ dùng.
9. [9] Bằng chứng đã giỏi do quản trò cấp, không tự cấp.
10. [10] Mười giờ đầu viết sau cùng, mỗi buổi theo học – dùng – lật – chứng
    minh, bài đầu dạy thái độ.
11. [11] Luật ít, nhưng ràng buộc đủ hẹp để mỗi lượt là một thế lưỡng nan.
12. [12] Ngẫu nhiên đặt ở đề bài, không đặt ở điểm.
13. [13] Bài đã quen thì đổi công cụ hoặc ràng buộc, không đổi bài.
14. [14] Cái tích qua các lượt là điều mình hiểu ra, cộng một kho nhỏ không bao
    giờ mất.
15. [15] Sau mỗi đoạn căng có đoạn thả được thiết kế trước, và đoạn thả là hệ
    quả của việc vừa qua được.
16. [16] Chỗ nghỉ là một nơi dựng riêng, dễ chịu — đi tới đó, không rơi vào đó.
17. [17] Một lượt trọn nằm trong một giờ: đủ để tiếc, đủ để chấp nhận.
18. [18] Phân định từ đầu cái thuộc lượt (mất được) và cái thuộc kho (không
    mất).
19. [19] Mỗi ngày một lượng việc hữu hạn; hết việc là chỗ dừng; nghỉ không bị
    phạt.
20. [20] Cho dừng sạch, không kéo thêm một lượt.
21. [21] Chặng nhỏ nhất có đủ ba thứ: nơi an toàn để về, nguồn để hỏi, cửa ải
    để thử.
22. [22] Mỗi chặng trung dạy đúng một thứ, kiểm bằng chính thứ đó, rồi cho chạy
    trơn một đoạn.
23. [23] Chặng lớn là một hạn chót, cỡ vài tuần; giữa hai hạn là việc thường
    ngày tự xếp; hạn đầu ngắn nhất.
24. [24] Hạn chót ghi rõ ngày từ đầu chặng; hạn bất định làm người chơi bỏ việc
    thường.
25. [25] Trễ hạn có lưới: lùi một tuần, không huỷ chặng.
26. [26] Đích lớn viết một lần, treo ở chân trời làm mốc nhìn, không nằm trong
    bất kỳ danh sách việc nào.
27. [27] Màn hình hằng ngày có ba dòng: hôm nay, hạn kế, một hai việc gợi ý.
    Bậc kế tiếp hiện, bậc cuối không.
28. [28] Không xếp việc thành hàng thẳng; để vài việc ở độ xa khác nhau và cho
    phép rẽ.
29. [29] Kết chặng trao một công cụ hoặc quyền mới, công cụ đó mở chặng sau và
    mở lại bài cũ; sau đó có chỗ về làng, rồi mục tiêu kế tiếp lộ ra.
30. [30] Vai của người chơi là người lên lịch trong hạn: quy trình đưa hạn và
    menu, không đưa lịch.
31. [31] Mỗi tên, bảng, con số trong hồ sơ và trong mọi file quản trò sinh ra
    tự giải nghĩa ngay tại chỗ xuất hiện đầu: nó là gì trong việc thật, người
    chơi làm gì với nó.
32. [32] Mỗi chặng lớn có một biến cố mở do người dẫn kể ngày đầu và một biến
    cố kết mọc từ nhật ký và bài kiểm của chính người chơi, không viết sẵn.

## Bảng đối chiếu điều kiện với bước

| Điều | Bước | Điều | Bước | Điều | Bước |
|---|---|---|---|---|---|
| [1] | 2 | [11] | 3 | [21] | 7 |
| [2] | 2 | [12] | 3 | [22] | 7 |
| [3] | 2 | [13] | 3 | [23] | 7 |
| [4] | 4 | [14] | 5 | [24] | 7 |
| [5] | 5 | [15] | 6 | [25] | 7 |
| [6] | 4 | [16] | 6 | [26] | 1 |
| [7] | 9 | [17] | 6 | [27] | 10 |
| [8] | 9 | [18] | 4 | [28] | 7 |
| [9] | 5 | [19] | 6 | [29] | 7 |
| [10] | 8 | [20] | 6 | [30] | 7 |
| | | | | [31] | 7, 10 |
| | | | | [32] | 7, 9 |

Bước 0, 11, 12 có điều kiện riêng ghi tại chỗ.
