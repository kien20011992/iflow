# Thư viện khung — bốn cách biến một việc khó thành game

**Đây là gì.** Một "khung" là bộ xương của một game đã được dựng bài bản:
người chơi lặp lại việc gì mỗi phiên, cái gì mở ra cái gì, thua thì mất gì
giữ gì, và thế giới đó nghe như thế nào. Giai đoạn concept lấy ba khung
khác nhau ở đây, khoác lên bản đồ kỹ năng của việc thật, ra ba concept cho
người dùng chọn. Khung không lấy từ gu người chơi; lấy từ bộ game tham chiếu
đã nghiên cứu ở chương trình trước (`docs/shape/game-hoa-viec-kho/` slice
01–03 trong vault Notebooks), vì đó là game dựng bài bản mà người dùng thấy
hấp dẫn.

**Nguồn và giới hạn.** Vòng lặp, hình tiến trình, thất bại của mỗi khung
rút từ ba case study trên. Ba case study **không bàn kiểu đặt tên**; mục
"Tông và kiểu đặt tên" là tổng hợp từ game gốc, không phải kết luận nghiên
cứu — coi là gợi ý phong cách, không phải luật.

**Thêm khung sau này:** chép đúng tám mục có nhãn của một khung dưới đây,
điền cho game mới, thêm vào cuối. `check-skill.sh` đếm heading `## Khung N`
và soi đủ tám nhãn.

## Luật mọi khung phải mang

Rút từ case study, không phụ thuộc khung nào. Giai đoạn slice (kế hoạch
gamemaster, từng dungeon) phải thoả hết:

- **Bài kiểm cố định để quay lại so** (Tree Sentinel của Elden Ring): một
  bộ đề niêm phong không đổi, đánh định kỳ, lần đầu thua là bình thường.
- **Lượt mất được, kho không mất** (Shiren; Pokémon "ngất chứ không chết"):
  một lượt ≤ 1 giờ, thua lượt là mất cái của lượt đó, không đụng vào cái đã
  tích (sổ hiểu biết, đồ đã rèn, cấp đã lên).
- **Làm lại ngay trong buổi ở tầng tay** (Celeste): thao tác vài giây thì
  sai là thử lại tức thì; lỗi tay run, công cụ trục trặc không tính là nước
  đi sai.
- **Ngẫu nhiên ở đề, không ở điểm** (Tetris): bốc ngày, bốc tình huống;
  chấm theo chuẩn cố định.
- **Dừng sạch** (Animal Crossing): hết việc trong ngày là "xong rồi, mai
  gặp", không "còn một bài nữa thôi"; nghỉ một tuần quay lại vẫn vào được,
  không phạt.
- **Hạn chót biết trước, kết chặng trao năng lực chứ không trao điểm, người
  chơi là người lên lịch trong hạn** (Persona).
- **Làng – hang – boss – về làng** (Dragon Quest): mỗi chặng có nơi về an
  toàn, nguồn hỏi, cửa ải; đích lớn treo ở chân trời, không nằm trong danh
  sách việc.
- **Nghi thức nhỏ khi qua bài, im lặng ở chỗ khác** (FromSoftware "Great
  Enemy Felled"; Mario): khoảnh khắc được đánh dấu, còn lại không nhạc.
- **Không ngôn từ phán xét lối rẽ** (Celeste đổi "Cheat Mode" thành "Assist
  Mode"): lối quan sát, lối chậm, lối hoãn có tên trung tính.

## Khung 1 — Đền thử thách

**Game gốc:** The Legend of Zelda, kể cả Breath of the Wild.

**Vòng lặp một phiên:** vào một đền, nhận một vật phẩm mới, đền hỏi "giải
được không?" bằng chuỗi câu đố xây đúng trên vật phẩm vừa nhận; ra khỏi
đền, dùng vật phẩm đó tìm đường tới đền kế. Chuỗi hứng thú: đồi che cây
cầu, cầu che ngọn tháp — luôn thấy một thứ ở xa để đi tới.

**Hình tiến trình:** mỗi đền = một kỹ năng; vật phẩm nhận ở cuối đền mở
đền sau và mở lại chỗ cũ từng bí (rương ở nơi đã qua). Lâu đài cuối thấy
được từ khắp bản đồ ngay từ đầu. Sau đền khó có một đoạn đi trơn, không leo
thang liên tục.

**Thất bại:** trong đền, sai câu đố chỉ tốn thời gian thử lại; không mất
vật phẩm đã có. Ra khỏi đền bất kỳ lúc nào, quay lại đúng phòng đang dở.

**Tông và kiểu đặt tên:** fantasy phương Tây sáng, có chút cổ; tên tiếng
Anh ghép danh từ: *Shrine of Still Water*, *Tower of the First Gate*,
*Sheikah Slate*, *Hyrule Field*, *Great Fairy Fountain*. Người dẫn kiểu
lão giả hay linh hồn giữ đền, nói ngắn, đặt câu hỏi hơn là giảng.

**Hợp với việc:** kỹ năng **tuần tự** — mỗi chặng dạy đúng một thứ và kiểm
bằng chính thứ đó; kỹ năng sau cần kỹ năng trước (cột "Học sau" của bản đồ
có chuỗi dài).

**Cách ánh xạ bản đồ kỹ năng:** mỗi dòng bản đồ có "Học sau" → một đền,
xếp theo chuỗi; vật phẩm cuối đền = năng lực mới được gọi tên trong game
(ví dụ "kính nhìn thấy vết nứt" cho kỹ năng nhận ra FVG); dấu hiệu đo được
= câu đố cuối đền (bộ đề niêm phong); quest = từng phòng trong đền; cấp
không có, tiến trình đo bằng số đền đã mở và vật phẩm trong túi.

**Nhược điểm điển hình:** việc có nhiều kỹ năng song song thì chuỗi đền
thành hàng thẳng gượng; người chơi kẹt ở một đền là kẹt cả game — phải có
đền phụ hoặc "đi trơn" để rẽ; dễ viết đền như bài giảng nếu quên rằng đền
chỉ hỏi, không giảng.

## Khung 2 — Thợ săn

**Game gốc:** Monster Hunter.

**Vòng lặp một phiên:** nhận một quest ≤ 1 giờ, săn một con quái, nhặt vật
liệu, về làng rèn đồ, nhận quest khó hơn. Săn lại cùng con bằng một vũ khí
khác thì cách chơi khác hẳn. Con quái đầu là "quái dạy" với đòn báo trước
rõ.

**Hình tiến trình:** nhân vật không có cấp; chỉ số nằm ở vũ khí và giáp, là
dấu tích của con đã săn ("vòng thành tựu"). Hạng thợ săn chỉ mở quest khó
hơn. Bùa ngẫu nhiên ép đổi build. Không có bảng "mạnh nhất".

**Thất bại:** thua quest mất vật phẩm đã tiêu và tiền thưởng của quest đó,
giữ vật liệu đã nhặt dọc đường. Người mới và cựu binh cùng một sân.

**Tông và kiểu đặt tên:** hoang dã, thủ công, chút Nhật; tên quái là từ
ghép tự chế nghe như tên loài: *Rathalos*, *Anjanath*, *Zinogre*; vũ khí
gọi theo loại: *Great Sword*, *Insect Glaive*; làng và sân săn: *Astera*,
*Ancient Forest*, *Wildspire Waste*. Người dẫn kiểu Handler / thợ rèn của
làng.

**Hợp với việc:** kỹ năng **song song trên cùng một sân** — cùng một đoạn
thị trường (cùng ngày, cùng biểu đồ) mà đổi "vũ khí" (một khung thời gian,
một kiểu vào lệnh, một công cụ) là bài khác; tiến bộ ở tay, không ở chỉ số.

**Cách ánh xạ bản đồ kỹ năng:** mỗi dòng bản đồ không có "Học sau" hoặc
cùng bậc → một loại quái (kỹ năng nhận ra thanh khoản = một loài, nhận ra
FVG = loài khác); mỗi cách làm (khung 5m / 15m; setup A / B) = một vũ khí;
dấu hiệu đo được = vật liệu rơi ra khi săn thành công (so đáp án đúng bao
nhiêu = nhặt được bao nhiêu); đồ rèn = năng lực đã chứng minh; bộ đề niêm
phong = quái "khảo hạch" lên hạng.

**Nhược điểm điển hình:** không có cấp nên người chơi mới có thể không thấy
mình đang tiến; hệ đồ rèn dễ phình thành bảng kiểm kê khô; việc có kỹ năng
tuần tự chặt thì "săn con nào cũng được" là sai.

## Khung 3 — Hầm ngẫu nhiên

**Game gốc:** Shiren the Wanderer (Mystery Dungeon).

**Vòng lặp một phiên:** từ làng xuống hầm; hầm sinh ngẫu nhiên mỗi lần,
một lần ~1 giờ; chết thì về làng, tay trắng, xuống lại. "RPG chơi được
1000 lần."

**Hình tiến trình:** không cày cấp; cái tích là hiểu biết (sổ ghi điều
hiểu ra sau mỗi lần) và kho ở làng, cửa hàng to dần, tiến độ kịch bản giữ.
Càng đi càng biết hầm, không phải càng mạnh.

**Thất bại:** mất sạch đồ mang trong hầm, về số không; không mất kho làng,
không mất sổ. Một giờ là "đủ để tiếc, đủ để chấp nhận".

**Tông và kiểu đặt tên:** Nhật cổ, lữ khách, tối giản; tên tiếng Anh hoặc
tên ngắn viết Latin mang âm Nhật: *Table Mountain*, *Koppa* (bạn đồng
hành), *Kobamis* (làng), *Fay's Final Puzzle*, *Warehouse*. Người dẫn kiểu bạn đồng hành nhỏ
đi cùng, nói ít, nhắc luật.

**Hợp với việc:** việc mà **đề phải ngẫu nhiên** và lặp nhiều lần (bốc một
ngày bất kỳ để tua), lượt phải mất được; tiến bộ là biết đọc tình huống,
không phải nhớ đáp án.

**Cách ánh xạ bản đồ kỹ năng:** mỗi lần tua một ngày bốc ngẫu nhiên = một
lần xuống hầm; tầng hầm = các bước trong một setup trọn (tầng 1 đánh dấu
cấu trúc, tầng 2 thanh khoản, … tầng cuối vào lệnh); chết = sai chuẩn ở
tầng nào thì dừng ở tầng đó, về làng; kho làng = sổ hiểu biết + đồ đã
kiếm được ở các lần xuống trước; bộ đề niêm phong = "hầm khảo hạch" tầng cố
định; dấu hiệu đo được = xuống tới tầng mấy, đúng bao nhiêu ở mỗi tầng.

**Nhược điểm điển hình:** về số không nhiều lần có thể nản nếu kho làng
không lớn lên thấy được; tầng hầm ánh xạ thành các bước setup dễ thành hàng
thẳng; việc không có nguồn đề ngẫu nhiên thì khung này rỗng.

## Khung 4 — Vùng đất đổ nát

**Game gốc:** FromSoftware — Elden Ring, Dark Souls, Sekiro.

**Vòng lặp một phiên:** đi từ điểm nghỉ (Site of Grace) tới cửa boss, chết,
hồi sinh ngay cửa boss, chạy lại (ngắn dần nhờ cửa tắt mở ra), đọc "tell"
năm pha của đòn boss, thắng, "Great Enemy Felled", cửa mở khu mới. Im lặng
sau boss là phần thưởng.

**Hình tiến trình:** bản đồ vòng lặp, đi sâu mở cửa tắt về điểm nghỉ; boss
chặn khu; một boss cố định đứng ngay đầu game (Tree Sentinel) không thắng
nổi lúc mới vào, vài giờ sau thắng với gần đúng đồ cũ — thước đo tiến bộ
không đổi. Bỏ qua boss cũng là quyền.

**Thất bại:** chết mất hết "souls" đang cầm nhưng để vết máu, chạm lại là
lấy đủ; chết lần hai mới mất hẳn. Boss đầu có cửa hông để chạy. Bài đầu
dạy thái độ bằng sắp đặt, không bằng lời: thua được, bỏ qua được, quan sát
trước khi ra tay.

**Tông và kiểu đặt tên:** trầm, cổ, đổ nát, ít lời; tên tiếng Anh cổ kính
hoặc ghép danh: *Site of Grace*, *Stakes of Marika*, *Tree Sentinel*,
*Firelink Shrine*, *Undead Burg*, *Limgrave*. Không nhạc ngoài boss. Người
dẫn kiểu người giữ lửa hay hiệp sĩ già, nói một câu rồi thôi.

**Hợp với việc:** **phán đoán trong bất định** — mỗi tình huống có "tell"
báo trước phải học đọc (chuỗi quét thanh khoản → displacement → gãy cấu
trúc → FVG là năm pha của một đòn); thất bại nhiều lần trước cùng một bài
là bình thường; cần một thước cố định để thấy mình khá lên.

**Cách ánh xạ bản đồ kỹ năng:** một setup trọn = một boss với các pha là
các dòng bản đồ (đọc cấu trúc, thanh khoản, FVG, MSS); chạy lại = tua lại
cùng ngày; điểm nghỉ = làng/bến an toàn có sổ; Tree Sentinel = bộ đề niêm
phong đánh lần 0 rồi định kỳ; cửa tắt = kỹ năng con đã chắc nên rút bớt
bước; dấu hiệu đo được = boss gục ở pha mấy.

**Nhược điểm điển hình:** tông trầm không hợp mọi người và dễ thành nặng
nếu người dẫn nói nhiều; "chết nhiều là bình thường" cần được sắp đặt
ngay bài đầu, không thì người mới bỏ; ít cấp/đồ nên tiến bộ phải hiện ở
thước cố định, đòi kế hoạch gamemaster chặt.

## Hàng cấm — luật cứng ở mọi game

Bốn cơ chế không bao giờ vào game, dù người dùng xin:

- **May mắn ở điểm** — phá thang đo; ngẫu nhiên chỉ ở đề.
- **Chuỗi ngày liên tiếp** — đo công sức, không đo năng lực; đứt chuỗi thì
  bỏ luôn.
- **Bảng xếp hạng** — bẽ mặt kéo dài.
- **Tiền ở điểm hay phần thưởng** — lãi lỗ, quy đổi ra tiền, mồi bằng
  tiền: hết muốn chiến đấu.

Hàng "bắt buộc" của phiên bản trước (ràng buộc tài nguyên mỗi lượt, ngẫu
nhiên ở đề, lối rẽ không bẽ mặt, bài kiểm niêm phong, cốt truyện có người
dẫn) đã nằm trong "Luật mọi khung phải mang" ở trên. Thi đua và đồng đội
không dựng được một mình; bù bằng bài kiểm cố định và kho.

## Cơ chế tuỳ chọn — hỏi ở cổng khoá concept

Bốn món, người dùng chọn không hay nhiều; concept ghi món nào hợp khung và
đánh dấu "(gợi ý)":

| Cơ chế | Tác dụng | Tác dụng phụ | Hợp khung |
|---|---|---|---|
| Giới hạn thời gian ghi chuẩn (N phút / N giây trước khi tua) | Ép quyết định, chặn phân tích quá lâu | Hại nếu lọt sang trận thật; chỉ áp ở vùng luyện | Hầm ngẫu nhiên, Vùng đất đổ nát |
| Một từ trạng thái đầu lượt + ô kỷ luật | Nhận ra mình đang ở trạng thái nào trước khi làm; đối thủ là chính mình | Thành tự trách nếu người dẫn bình luận — người dẫn chỉ ghi | Mọi khung |
| Việc phụ che nhau (làm A mới hiện B) | Không xếp hàng thẳng, cho phép rẽ | Sa đà — đó là mục đích | Đền thử thách, Thợ săn |
| Gửi ba dòng cuối ngày cho một người ngoài | Trọng tài thứ hai; khó tự nới luật | Cần người thật | Mọi khung |
