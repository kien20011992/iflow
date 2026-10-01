# Slate — cái máy của game: máy chấm và trang chơi

**Đây là gì.** "Slate" là tên kỹ thuật của skill cho phần máy của một game:
dữ liệu thật, máy chấm biến luật `gamemaster.md` thành code, và trang chơi
mà người chơi bấm vào. Người dẫn không chấm tay; người chơi không chép số
vào chat. Thư mục luôn là `slate/` cho đồng nhất, nhưng **tên trang trong
game do concept đặt** và ghi ở bảng từ vựng (`gamemaster.md` mục 7); file
người chơi và lời người dẫn chỉ dùng tên đó.

**Khi nào game có máy.** Khi việc thật mô phỏng được từ dữ liệu: giá lịch
sử, kho văn bản, bộ đề, bản nhạc MIDI, log gõ phím. Không mô phỏng được thì
game chạy trên file và số báo tay, và `plan.md` ghi rõ vì sao.

**Đơn vị đề.** Máy chấm làm việc trên *đề*: một đơn vị dữ liệu người chơi
xử lý trong một lần chơi (forex: một ngày giá cũ; gõ phím: một đoạn văn;
đàn: một câu nhạc). Tên đề trong game do bảng từ vựng đặt; ở đây gọi chung
là đề.

## Máy chấm

Nguyên tắc (ví dụ và con số trong ngoặc là của game forex, không phải
chuẩn):

- **Hàm thuần từ luật.** Mỗi dòng của bảng nối trong `gamemaster.md` thành
  một hàm nhận đơn vị dữ liệu và trả kết quả; không đọc file, không mạng,
  không trạng thái ẩn. Trang chơi dùng lại đúng định nghĩa đó (viết lại
  bằng JS, cùng hằng số), nên hàm phải đơn giản đủ để viết hai lần không
  lệch.
- **Hằng số ở đầu file, chú thích "ước lượng".** Mọi sai số, ngưỡng, hệ số
  của gamemaster.md nằm một chỗ.
- **Đổi số hay luật** — hiệu chỉnh sau bài kiểm lần 0, nhánh `sửa:`, chiêu
  mới của dungeon thêm — đi đủ năm bước, theo thứ tự: sửa gamemaster.md;
  sửa hằng số hay luật ở đây, và luật đổi đáp án hay có chiêu mới thì tính
  lại `key` cho mọi đề đang có, kể cả đề trong `boss/set.json`, giữ nguyên
  đề và seed; sửa bản JS trên trang; xuất lại
  `data/fixtures.json` và chạy đối chiếu hai bản; đăng lại trang ở URL của
  mục 7 (cập nhật artifact cũ, sổ chung giữ nguyên). Thiếu một bước là
  trang, nơi chấm thật, vẫn chấm theo số cũ mà không ai thấy.
- **Đáp án tính trước theo đề.** `key(đề)` trả một JSON: mọi đáp án máy tìm
  được; trang chơi chỉ so, không tính lại phần nặng. Chỉ phần phụ thuộc nước
  đi của người chơi là tính lúc chơi (forex: điểm vào, stop, đích).
- **Mô phỏng ở độ phân giải nhẹ, luật hoà bất lợi.** Khi hai kết quả xảy
  ra trong cùng một bước dữ liệu, tính kết quả bất lợi cho người chơi và
  nói rõ luật đó. Không bao giờ thưởng nhầm.
- **Test mỗi luật một fixture** (`unittest`, không phụ thuộc ngoài): giá
  trị đúng ở ngưỡng và ngay dưới ngưỡng. Fixture phải giống dữ liệu thật ở
  chỗ luật nhạy (forex: nến phẳng thân 0 làm "thân trung vị" vô nghĩa).
- **Dữ liệu giữ lại chỉ là thứ trang chơi cần.** Mỗi đề một JSON nhỏ; dữ
  liệu thô tải về xử lý xong thì bỏ. Nguồn tải có giới hạn tần suất → tải
  chậm rãi, cache, chờ lỗi rồi thử lại, chạy nền, chạy lại là tiếp tục.
- **Bài kiểm cố định chọn máy và niêm phong.** Seed cố định, tiêu chí ghi
  trong gamemaster.md mục 4 (số đề, đề có gì, rải thế nào); đề chọn rồi loại
  khỏi kho thường; người chơi chỉ thấy "đề số N". Kết quả là
  `boss/set.json`: `{"seed": n, "items": [ {n, key, …} × <số đề mục 4> ]}`.
- **Bộ ca kiểm chung cho hai bản.** Máy Python xuất `data/fixtures.json`
  (hằng số + mỗi ca: đầu vào, đầu ra) từ chính các fixture của test; bản
  JS trên trang chạy cùng bộ ca lúc nạp trang (hay trong test riêng) và
  phải trả y hệt. Lệch một ca là lệch luật, không đưa trang ra. Script
  đối chiếu nằm ở `slate/tests/` của game, không ở thư mục tạm, vì mỗi lần
  đổi số phải chạy lại nó.
- **Đọc mắt một đề thật trước khi tin máy.** In một đề quanh chỗ máy chấm
  và tự đọc. Test khoá luật đã viết, không khoá luật viết thiếu.
- **Máy không phải chân lý.** Lĩnh vực có chỗ là phán đoán thì máy và
  người lệch nhau ở vài ca; gamemaster.md nói rõ đó là "luật của <tên
  trang>", và người chơi thấy lệch thì ghi sổ, người dẫn chuyển vào
  plan.md, không sửa luật giữa vùng.

## Chấm đúng lúc

Chấm đúng chưa đủ: trang còn phải chấm **đúng lúc**, và không phá cái người
chơi đang nhìn. Test và đối chiếu hai bản xanh hết vẫn không bắt được ba
lỗi dưới; người chơi thì thấy ngay, và bỏ dở.

- **Một nước đi chỉ được chấm khi nó không đổi được nữa.** Nước đi tốn
  nhiều thao tác mà chấm ngay ở thao tác đầu là báo hỏng oan: gõ "tiếng"
  tốn bảy phím, chấm ở phím thứ ba thì mọi chữ có dấu đều đỏ. Tìm mốc
  "xong" của nước đi trong lĩnh vực đó — hết âm tiết, thả chuột, chốt lệnh
  — rồi chấm ở đó. Điểm cuối lượt tính lại từ log thô vẫn đúng nên test
  không thấy gì; chỉ người chơi thấy.
- **Đề người chơi đang nhìn không bao giờ bị ghi đè bằng cái họ vừa nhập.**
  Hiện cái họ nhập ở chỗ khác, hoặc chỉ hiện sau khi nước đi đã chấm xong.
  Ghi đè là lấy mất bản đồ giữa lúc họ đang đi theo nó.
- **Thao tác lùi phải lùi đúng đơn vị mắt thấy.** Một lần bấm xoá thì mất
  một đơn vị người chơi nhìn thấy, không phải một thao tác bên trong:
  "người" là 5 chữ nhưng 8 phím, lùi theo phím thì bấm 5 cái từ chưa hết,
  giữ lùi thì trôi qua cả dấu cách sang từ trước. Và lùi qua một thứ vốn
  đúng để với tới chỗ sai phía trước là cách sửa, không phải lỗi — chỉ thứ
  vốn sai mới tính hỏng; cái giá của việc lùi đã nằm ở nhịp và ở số lần lùi.

## Hợp đồng kết quả

Trang lưu bằng capability `db` của Artifact (`capabilities: {db: {}}`);
chế độ play đọc và ghi bằng tool `ArtifactData` với URL của artifact.
Không có `db` (người xem không đăng
nhập, hay bị từ chối) thì trang lưu localStorage và hiện nút "Sao chép cho
người dẫn": người chơi dán JSON vào phiên, người dẫn đọc y như đọc từ db.

Hợp đồng có **phần khung** (giống mọi game, chế độ play và script kiểm bám
vào) và **phần riêng** (từng game khai báo ở bảng từ vựng của
`gamemaster.md` mục 7). Tên bộ sưu tập và tên trường khung là mã, người
chơi không thấy; trang hiện chúng bằng tên trong game.

| Bộ sưu tập | Ai ghi | Trường khung (bắt buộc) | Phần riêng |
|---|---|---|---|
| `character/main` | **người dẫn** (Claude); trang chỉ đọc, trừ các bộ đếm | `region` (tên vùng hiện tại), `unlocked` (mảng mã chiêu bấm được; trang mở chiêu theo mảng này, không hard-code theo vùng), `levels` (cấp 1–5 mỗi mã, kể cả chiêu chưa mở), `sessions` (số lần chơi, trang tự đếm) | bộ đếm và giới hạn khác của game, ghi ở bảng từ vựng (forex: `mana_max`, `chain`, `kills`, `r_unlocked`) |
| `sessions/<id>` | trang, một doc mỗi lần chơi thường | `item_id` (id mờ của đề; đề thật tra ở `slate/data/ids.json`), `started_at`, `ended_at`, `summary` (mỗi mã chiêu đã bấm: `hits` trúng, `misses` sai, `missed` sót), `actions` (nước đi thô: bấm gì, ở đâu, lúc nào), `note` (một dòng người chơi gõ, có thể rỗng), `ended_by` | trường đo thêm của chiêu (forex: `W.lure_kills` mồi cắn, `R.casts / clean / kills / assists`), trạng thái cuối lần chơi (forex: `mana_left`, `chain_after`), dự đoán phụ (forex: `SKY.pick / answer / hit`) |
| `tests/<id>` | trang, một doc mỗi lần đánh bài kiểm cố định | `at` (giờ ISO lúc xong), `picks` (số đề bốc), `results` (từng đề: summary và `actions` nước đi thô, cùng hình với `sessions`), `scores` (mỗi mã chiêu: `precision` % trúng trên đặt, `recall` % trúng trên có, null khi không bấm) | cột điểm khác mà thang mục 3 dùng (forex: `R.clean_pct`, `SKY.pct` + `SKY.n`) |

Luật giữ cho hợp đồng đứng: trang chỉ ghi kết quả thô, mọi phán xét (cấp,
mở chiêu, qua vùng, phần thưởng cốt truyện) là của người dẫn theo
gamemaster.md; trang **không** tự lên cấp; id lần chơi = ngày thật + 4 ký
tự ngẫu nhiên; mọi số là số thô (đếm), phần trăm chỉ ở bài kiểm; không có
tiền ở đâu cả. Trường riêng nào trang ghi thì bảng từ vựng phải có, để
người dẫn biết đọc nó ra chữ gì.

## Cảm giác game

Trang chấm đúng, lưu đúng mà vẫn có thể cho cảm giác đang làm việc thật
chứ không phải đang chơi, với cốt truyện nằm ngoài lề. Một trang "chơi
được" chưa phải game; những điều dưới
đây là cái làm nó thành game, và trang của mọi game có máy phải có đủ. Hình
hài cụ thể (quái, bẫy, boss, hay thứ khác) là của concept đã khoá; ví dụ
trong ngoặc là của ca forex:

- **Kẻ địch nhìn thấy được, nhưng chỉ sau khi đáp án đã khoá.** Mỗi đáp
  án chính là một thứ đứng đúng chỗ đó trên màn (forex: con quái ở mỗi
  đỉnh đáy lớn); dấu trúng thì nó ngã, sót thì nó đứng nhìn người chơi.
  Hiện trước lúc niêm là lộ đáp án — luật cứng. Lúc tua, nó chỉ mọc sau khi
  cơ hội gọi đã qua (vài bước ân hạn), cùng lý do.
- **Thứ người chơi đặt phải có hình của việc nó làm.** (Forex: mồi là bẫy
  có răng, giá chạm là răng khép, có tiếng, có rung.) Không phải đường kẻ
  hay ô tick.
- **Bài kiểm cố định là boss có thanh máu.** Máu = tổng đáp án của bộ đề
  bốc ra (chỉ tính chiêu đã mở); mỗi cú trúng trừ một, có số bay lên. Máu
  là hình; điểm từng chiêu vẫn là số quyết định cấp, và trang nói rõ vậy.
- **Mọi cú trúng có tiếng và chuyển động; kill có hitstop.** Âm thanh tổng
  hợp bằng WebAudio (không file, không mạng), phát sau cú bấm đầu tiên; nút
  tắt tiếng trong menu; tôn trọng prefers-reduced-motion cho chuyển động.
- **Câu chuyện chạy ở ba chỗ:** màn dẫn nhập khi vào vùng (chữ là biến cố
  mở của gamemaster.md mục 6, nguyên văn, chia thẻ, xem lại được); một
  dòng cốt truyện mỗi đề (kho nhỏ, chọn theo đặc điểm đề và băm id để cùng
  đề luôn cùng dòng); người dẫn nói theo sự kiện trong lượt (kho câu, mỗi
  câu một lần mỗi lượt). Người dẫn trong chat không kể lại điều trang đã
  kể.
- **Không có sổ chung thì trang vẫn nhận được nhân vật:** ô dán JSON
  `character/main` trong menu, để cấp và chiêu mới người dẫn cấp tới được
  trang.
