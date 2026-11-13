# Từ cách xếp đã chọn tới file DXF

Đọc file này trước khi làm sản phẩm 5 đến 7: bảng số, bản kiểm, bản vẽ và
danh sách giao. Cách gọi CADCraft nằm ở [cadcraft.md](cadcraft.md).

Nguyên tắc xuyên suốt: mọi tọa độ trong sơ đồ và bản vẽ được tính từ bảng
số. Không con số hình học nào được gõ tay trong script. Muốn đổi bản vẽ thì
sửa bảng số rồi dựng lại toàn bộ.

## Cách vẽ: mặc định và lúc hỏi

Hỏi các mục dưới đây khi bắt đầu làm bảng số, bằng một câu nêu các mặc định
và mời sửa chỗ khác. Người dùng không phải người trong nghề thì không hỏi:
dùng mặc định và liệt kê chúng khi xin duyệt bảng số. Câu trả lời ghi vào
nhóm "cách vẽ của văn phòng" trong `project.md`.

| Mục | Mặc định khi người dùng không nói |
|---|---|
| Đơn vị và tỷ lệ | Milimét, vẽ 1:1 trong không gian mô hình. Mặt bằng tỷ lệ 1:100. |
| Trục | Đặt ở tim cột và tim tường chịu lực. Một phương đánh số, phương kia đánh chữ. |
| Kích thước | Đo trên tường thô, không tính lớp trát. Ô cửa đo theo mép lỗ mở. |
| Diện tích phòng | Đo lọt lòng giữa các mặt tường thô, không trừ cột nhô vào phòng. |
| Bề dày tường | Theo thông lệ xây ở nơi xây, tra và ghi nguồn. Không có mặc định chung. |
| Layer, màu, độ dày nét | Bộ mặc định ở cuối mục này. Văn phòng có bảng riêng thì dùng bảng đó. |
| Font chữ | Một font TrueType Unicode có dấu của ngôn ngữ dùng trên bản vẽ, mặc định Arial. Kiểu chữ ghi tên file kèm đuôi, ví dụ `arial.ttf`: AutoCAD đọc tên không đuôi như một font SHX. |
| File mẫu | Không có. Khung tên và trang in để người dùng làm trong AutoCAD. |

Mặc định nào mâu thuẫn với một số người dùng đã đưa thì mặc định nhường. Ví
dụ: trục ở tim tường bao làm nhà rộng hơn lô đất người dùng nêu. Khi đó chỗ
ấy thành một lựa chọn phải hỏi, theo mục "Asking" trong SKILL.md.

Bộ layer mặc định. Mỗi đối tượng nằm đúng một layer và không có gì ở layer
`0`. Độ dày nét đặt ngay trên layer, để bản in không phụ thuộc vào màu. Văn
phòng in theo bảng nét gắn với màu thì màu phải theo bảng của họ.

| Layer | Chứa gì | Kiểu nét | Dày (mm) | Màu |
|---|---|---|---|---|
| `A-GRID` | Trục và vòng tên trục. | Chấm gạch | 0,18 | Đỏ |
| `A-WALL` | Tường bị cắt. | Liền | 0,50 | Trắng |
| `A-COLS` | Cột và kết cấu bị cắt, kể cả phần tô đặc của chúng. | Liền | 0,50 | Trắng |
| `A-DOOR` | Cửa đi và cung mở. | Liền | 0,25 | Lục |
| `A-GLAZ` | Cửa sổ. | Liền | 0,25 | Lam nhạt |
| `A-STRS` | Thang, mũi tên hướng lên, nét cắt thang. | Liền | 0,25 | Vàng |
| `A-FLOR` | Nét nhìn thấy phía dưới: bậc cấp, mép sàn, thiết bị vệ sinh. | Liền | 0,18 | Lam |
| `A-OVHD` | Thứ ở phía trên mặt cắt: mép mái, dầm, ô trống. | Đứt | 0,18 | Tím hồng |
| `A-FURN` | Đồ đạc. | Liền | 0,13 | Lam |
| `A-PATT` | Mẫu tô vật liệu của sàn, đất, vật liệu ốp. Không dùng cho tường và cột. | Liền | 0,13 | Tím hồng |
| `A-DIMS` | Kích thước. | Liền | 0,18 | Đỏ |
| `A-TEXT` | Tên phòng, diện tích, ghi chú, cao độ. | Liền | 0,18 | Trắng |
| `A-FUTR` | Phần dành cho đợt xây sau, nếu có. | Đứt | 0,18 | Tím hồng |
| `A-RAIL` | Lan can, tay vịn. | Liền | 0,25 | Vàng |
| `S-CUTS` | Trong mặt cắt: sàn, dầm, mái, móng bị cắt. | Liền | 0,50 | Trắng |
| `A-ELEV` | Trong mặt cắt và mặt đứng: thứ nhìn thấy phía sau mặt cắt. | Liền | 0,18 | Lam |
| `C-TOPO` | Mặt đất và đất bị cắt. | Liền | 0,35 | Lục |
| `A-ANNO` | Nhãn cửa, ký hiệu cao độ, ký hiệu mặt cắt, mũi tên chỉ bắc. | Liền | 0,18 | Trắng |
| `C-PROP` | Ranh đất và đường lùi. | Hai chấm gạch | 0,25 | Lục |
| `X-AREA` | Đường bao phòng chỉ để đo diện tích. Đặt không in trên layer. | Liền | — | Vàng |

## Sản phẩm 5: bảng số

`params.json` ghi cách xếp đã chọn thành số. Nó phải đủ để một người khác
dựng lại đúng bản vẽ mà không cần hội thoại.

Các nhóm phải có:

- **Tỷ lệ** của bản vẽ, ví dụ 100.
- **Danh mục hình** sẽ vẽ: mặt bằng tầng nào, mặt cắt qua đâu, mặt đứng nào.
- **Đất:** đường ranh, các khoảng lùi, cạnh nào là mặt trước, hướng bắc. Cải
  tạo thì nhóm này là đường bao nhà có sẵn.
- **Trục:** tên và tọa độ theo hai phương.
- **Cao độ:** từng sàn, chiều cao tầng, chiều cao thông thủy, mái.
- **Loại tường:** tên và bề dày.
- **Từng tầng:** các đoạn tường (loại, từ giao trục nào tới giao trục nào,
  canh theo tim hay mép), cột, ô cửa (thuộc đoạn tường nào, cách mốc bao
  nhiêu, rộng, cao, cao bệ, loại, chiều mở), thang (vị trí, số bậc, rộng mặt
  bậc, rộng vế, hướng lên), khu ướt, phòng (tên, đường bao, diện tích cần).
- **Gốc của từng hình** trong không gian mô hình (`sheet`), tính theo luật
  khoảng cách giữa các tầng ở sản phẩm 7. `check.py` tách từng hình theo gốc
  này, không theo tọa độ của `build.py`.
- **Layer và font.**

Khuôn minh hoạ. Tên khoá viết tiếng Anh và nhất quán trong một dự án. Tên
phòng và ghi chú viết bằng ngôn ngữ của người dùng:

```json
{
  "scale": 100,
  "drawings": ["plan:L1", "plan:L2"],
  "sheet": {"plan:L1": [0, 0], "plan:L2": [20000, 0]},
  "site": {"outline": [], "setbacks": {}, "front": "A", "north_deg": null},
  "_note": "north_deg: góc của hướng bắc, tính bằng độ từ chiều dương trục x, ngược chiều kim đồng hồ",
  "grid": {"x": {"1": 0, "2": 3600}, "y": {"A": 0, "B": 4200}},
  "levels": {"L1": 0, "L2": 3300},
  "wall_types": {"ext": 220, "int": 110},
  "floors": {"L1": {"walls": [], "columns": [], "openings": [],
                    "stairs": [], "rooms": []}},
  "layers": {}, "font": "Arial"
}
```

Luật ghi bảng số:

- Mọi kích thước nhập vào là milimét nguyên. Số suy ra bằng phép chia, như
  chiều cao một bậc thang, không ghi vào bảng: script tính từ chiều cao tầng
  và số bậc.
- Số phụ người dùng không nêu thì lấy mặc định sau, ghi `"by": "default"`:
  chiếu nghỉ sâu bằng bề rộng vế thang; cửa đi mở vào phòng mà nó dẫn tới,
  cửa ra ngoài nhà mở vào trong, trừ cửa trên lối thoát nạn;
  má tường hai bên ô cửa ít nhất 100. Má không đủ 100 thì hạ bề rộng cửa một
  bậc (900 xuống 800), ghi `"by": "model"` và nêu khi xin duyệt.
- Kích thước người dùng nêu mà không nói đo tới tim hay tới mặt tường, đo
  lọt lòng hay theo trục, là một lựa chọn phải hỏi, không tự chọn. Ví dụ:
  "cách trục 2 đúng 2000", "vệ sinh 1500×2000".
- Vị trí ghi bằng tên trục cộng khoảng lệch, không ghi tọa độ trần. Nhờ vậy
  dời một trục thì mọi thứ bám theo. Vách không nằm trên trục thì ghi bằng
  khoảng cách tới mặt một bức tường, ví dụ "cách mặt trong tường trục 2 một
  khoảng 1100".
- Phòng ghi tên và một điểm nằm trong phòng. Đường bao phòng do script dò
  từ tường, không ghi tay. Hai phòng thông nhau không có tường ngăn, như sảnh
  và sảnh thang, thì bảng số ghi một đường ranh ảo giữa chúng, như một đoạn
  tường bề dày 0. Script dò phòng coi nó là tường; script vẽ tường bỏ qua nó.
  Đường này chỉ nằm trên `X-AREA` và không in.
- Thang ghi riêng số bậc cao (bằng chiều cao tầng chia cao bậc) và số mặt
  bậc. Thang thẳng có số mặt bậc ít hơn số bậc cao một bậc. Thang có chiếu
  nghỉ thì mỗi vế ít hơn một bậc.
- Mỗi số không do người dùng đưa mang khoá `"by"`: `"model"` khi AI chọn,
  `"default"` khi lấy mặc định. Mục đang chờ người dùng chọn mang
  `"pending": true`.
- Chỉ hỏi những số mà hình trong danh mục dùng tới. Danh mục chỉ có mặt bằng
  thì chưa cần cao cửa, cao bệ cửa sổ hay mái.
- Số nào đọc từ phác thảo mà không chắc thì hỏi lại, không đoán rồi im.

**Cỡ chú thích không nhập tay.** Mỗi cỡ bằng chiều cao muốn có trên giấy
nhân với tỷ lệ. Mặc định trên giấy, đổi được trong bảng số: chữ thường
2,5 mm (cả chữ cao độ), số bậc thang 1,8 mm, tên phòng và chữ trong vòng
tên trục 3,5 mm, tiêu đề hình 5 mm, khoảng cách giữa các hàng kích
thước 8 mm, vòng tên trục đường kính 8 mm. Ở tỷ lệ 1:100, chữ thường cao
250 đơn vị. Kiểu kích thước giữ giá trị theo milimét giấy và đặt hệ số
chung bằng tỷ lệ. Độ thưa nét đứt (biến `LTSCALE`) khởi đầu bằng một phần
năm tỷ lệ, tức 20 ở 1:100, rồi nhìn ảnh mà chỉnh.

Một file dùng một tỷ lệ. Chi tiết tỷ lệ lớn hơn, như thang 1:50, thuộc phần
để lại cho người dùng.

### Sơ đồ cho người duyệt

`preview.py` đọc `params.json` và sinh `preview.svg`, chỉ dùng thư viện
chuẩn của Python. Sơ đồ có:

- Đường ranh đất và phần phải lùi.
- Tường, cột, ô cửa có chiều mở, thang có hướng lên.
- Tên trục và khoảng cách giữa các trục.
- Tên phòng, diện tích và kích thước lọt lòng của từng phòng.
- Thước tỷ lệ và mũi tên chỉ bắc. Chưa biết hướng bắc thì ghi "chưa có".
- Màu khác cho mục đang chờ người dùng chọn và cho số AI tự chọn.

Sơ đồ không phải bản vẽ. Nó để người duyệt chỉ vào một trục hay một phòng và
nói "dời cái này".

Trước khi cho người dùng xem, tự nhìn sơ đồ một lần để bắt chữ tràn khỏi
phòng, cánh cửa chắn lối, hình đè nhau. Máy không có công cụ đổi SVG thành
ảnh thì kiểm bằng số ngay trong script (bề rộng chữ so với bề rộng phòng,
cung mở cửa so với ô cửa bên cạnh), và nói với người dùng là sơ đồ chưa được
nhìn bằng mắt.

## Sản phẩm 6: bản kiểm

Làm trên bảng số và sơ đồ, trước khi xin duyệt bảng số. Kết quả đi kèm lời
xin duyệt. Mỗi phép kiểm ghi một dòng: đạt, không đạt, hoặc chưa kiểm được vì
thiếu gì.

- **Vừa đất.** Phủ bì của nhà, tính cả bề dày tường, nằm trong phần được xây.
- **Lối vào từng phòng.** Mọi phòng tới được từ lối đi chung mà không phải
  xuyên một phòng riêng tư khác.
- **Đặt đồ.** Đồ lớn nhất của từng phòng có vừa không, còn lối đi quanh nó
  không.
- **Cửa.** Cánh mở có đụng đồ, đụng cánh khác, chắn lối không. Má tường hai
  bên ô cửa còn đủ rộng để xây không.
- **Cửa sổ.** Ô nào nằm trên tường sát đất người khác, và luật nơi xây nói gì
  về việc đó.
- **Đi thử.** Từ cửa vào tới từng phòng qua đâu. Đường mang đồ, đường của
  khách, đường của người già có phải băng qua chỗ riêng tư không.
- **Thang.** Số bậc nhân cao bậc bằng chiều cao tầng. Mặt bậc bằng chiều dài
  vế chia số mặt bậc của vế. Mặt bậc và cao bậc nằm trong giới hạn của luật
  nơi xây; chưa tra được luật thì dùng thông lệ: mặt bậc từ 250, hai lần cao
  bậc cộng mặt bậc từ 550 tới 650. Khoảng đầu phía trên thang đủ cao. Lỗ
  thang ở sàn trên khớp vị trí thang ở sàn dưới. Thang quay đầu: đầu vế cuối
  phải chạm một mặt sàn ở tầng trên, không đâm vào tường hay lỗ sàn. Thang
  không đạt mà số đó do
  người dùng đưa thì không vẽ tiếp: báo bằng số và hỏi, theo luật "không tự
  lật quyết định" trong SKILL.md. Bảng số đã duyệt cũng vậy: quay lại lần
  duyệt thứ hai, kèm một hai cách sửa đã tính bằng số (chiếu nghỉ sâu hơn,
  bớt bậc mỗi vế, dời tường).
- **Chồng tầng.** Khu ướt, cột, tường chịu lực các tầng thẳng nhau. Tường
  tầng trên có thứ gì đỡ bên dưới.
- **Sáng và gió.** Phòng nào không có cửa ra ngoài, và nó được thông gió
  bằng gì.
- **Luật.** Dò lại từng ràng buộc đã ghi ở sản phẩm 2: lùi, diện tích phủ,
  chiều cao, diện tích và bề rộng tối thiểu, lối thoát. Khi sản phẩm 2 được
  bỏ qua vì người dùng tự giữ, chỉ dò những ràng buộc tra nhanh được và báo,
  không chặn.
- **Sổ.** Tính lại tổng diện tích sàn và chi phí theo bảng số hiện tại.

Phép kiểm không đạt mà sửa được bằng một số AI có quyền chọn thì sửa bảng số
và báo. Phép kiểm không đạt chạm tới thứ người dùng đã đưa hoặc đã chốt thì
theo luật "không tự lật quyết định" trong SKILL.md.

## Sản phẩm 7: bản vẽ và danh sách giao

### Một hình mặt bằng phải có gì

- Tường và cột bị cắt, nét đậm nhất. Mặt cắt ngang quy ước ở độ cao khoảng
  ngang ngực, nên cửa sổ bị cắt qua.
- Ranh đất và đường lùi trên `C-PROP`, khi bảng số có nhóm đất.
- Trục có vòng tên ở hai đầu. Vòng tên dùng nét liền, kể cả khi nằm trên
  layer nét chấm gạch. Vòng tên nằm ngoài cùng, ngoài cả hàng kích thước
  và ranh đất.
- Cột tô đặc. Tường để trống, trừ khi văn phòng tô tường. Phần tô nằm cùng
  layer với hình nó tô. Khi nhà có hai loại tường, như tường bê tông chịu
  lực hay ngăn cháy và tường xây gạch hoặc blốc, hai loại khác nhau bằng
  mẫu tô trên `A-PATT`, và ghi chú chung nói mẫu nào là loại nào.
- Cửa đi có cánh và cung mở đúng chiều, kèm nhãn trong vòng tròn nhỏ (P1,
  P2…). Cửa sổ có ký hiệu riêng và nhãn (V1, V2…). Cùng loại cùng nhãn.
  Nhãn cửa đi nằm trong chính phòng mà cánh mở vào, ngoài tầm quét của cánh:
  thử cạnh má cửa phía bản lề, rồi má bên kia, rồi thẳng ra trước cửa, và
  lấy chỗ đầu tiên không đụng tường, đồ đạc hay chữ. Cả ba chỗ đều vướng,
  như trong một phòng vệ sinh hẹp, thì đặt nhãn phía ngoài cửa, sát má. Nhãn cửa sổ nằm phía
  trong nhà. Vòng nhãn đường kính 6 mm giấy, chữ 2,5 mm. Khoảng hở giữa khung
  nhãn và khung tên phòng, nhãn khác hay số kích thước ít nhất một cỡ chữ
  theo cả hai phương. Đặt tên phòng trước, nhãn cửa tránh nó; nhãn cửa vẫn
  không có chỗ thì mới dời tên phòng.
- Má tường hai bên ô cửa đo từ mặt cột khi có cột, không từ mặt tường.
- Cửa cuốn vẽ hai nét mảnh song song giữa bề dày tường, nét đứt cho hộp
  cuốn phía trong, nhãn riêng (C1). Cao mặc định 2800, ghi `"by": "default"`.
- Thang có đủ bậc và số thứ tự bậc. Số đánh theo mặt bậc, từ 1 ở chân thang,
  chiếu nghỉ không có số. Tầng có chân thang: vẽ bậc tới nét cắt chéo trên
  `A-STRS`, phần phía trên nét cắt vẽ trên `A-OVHD`, mũi tên chữ "lên"; chữ đặt cạnh mũi tên, không chạm nét cắt chéo. Tầng
  có đầu thang: vẽ đủ cả hai vế bằng nét liền, mũi tên chữ "xuống". Thang hai
  vế quay đầu chia bậc đều cho hai vế, số bậc vế hai đánh tiếp số vế một.
  Tầng vừa có đầu thang lên vừa có chân thang lên tầng trên: vế lên vẽ tới
  nét cắt, phần dưới lỗ sàn là vế xuống, ghi cả "lên" và "xuống".
  Phần thừa giữa hai vế là khe thang, không phải tường. Nét cắt chéo đặt ở
  khoảng một phần ba vế đầu. Tầng có đầu thang vẽ lan can dọc mép sàn quanh
  lỗ thang. Chiếu nghỉ là một mảng liền, kể cả khi nó gấp chữ L: không có
  nét nào cắt ngang giữa mảng.
- Thiết bị vệ sinh (bồn cầu, chậu rửa, chỗ tắm) và thiết bị bếp (bàn bếp,
  chậu rửa). Đồ đạc chính của phòng (giường, bàn ăn, ghế) trên `A-FURN`, để
  người xem thấy phòng dùng được.
- Tên phòng và diện tích là MTEXT canh giữa (một hoặc hai MTEXT khi hai
  dòng khác cỡ), điểm đặt nằm trong đường bao phòng. Ước bề rộng chữ bằng
  số ký tự nhân 0,7 lần cao chữ, đúng hệ số `dxf_check.py` dùng. Chữ không vừa lòng phòng trừ 2 mm giấy mỗi
  bên thì xuống dòng, rồi mới hạ cỡ, không dưới 2,5 mm giấy. Khối hai dòng
  mà tràn phòng hoặc đụng đồ thì quay về một dòng cỡ nhỏ. Vẫn không vừa thì
  quay chữ theo cạnh dài của phòng, đọc từ dưới lên hoặc từ phải sang. Quay
  rồi vẫn tràn thì đặt trong phòng lớn kề bên, hoặc ngoài nhà ở chỗ không
  có đường gióng kích thước, nối về phòng bằng một đoạn thẳng (`LINE`) có
  một đầu nằm trong phòng. Không co chữ dưới 2,5 mm. Ô thang riêng là một
  phòng: ghi "Thang" và diện tích. Chữ không nằm
  trong tầm quét của cánh cửa và không đè đồ đạc. Số diện tích tính từ chính đường bao sẽ vẽ, `check.py` so lại với số
  CADCraft đo trên file.
- Ba lớp kích thước ngoài nhà, từ trong ra. Hàng trong: từ trục tới mép ô
  cửa, qua ô cửa, tới trục kế tiếp, ngắt tại mọi trục, đo theo trục chứ không
  theo mặt tường. Hàng giữa: từng trục. Hàng ngoài: tổng. Mỗi hàng khép kín
  từ đầu tới cuối, không chừa khoảng hở. Bề dày tường không ghi trong chuỗi
  mà ghi một lần trong ghi chú chung dưới tên hình, ví dụ "tường bao 220,
  tường ngăn 110".
- Phương nào chỉ có hai trục thì hàng trục trùng hàng tổng: bỏ hàng trục.
- Đặt ba hàng ở mọi cạnh có ô cửa. Cạnh không có ô cửa chỉ cần hàng trục và
  hàng tổng, và mỗi phương ít nhất một cạnh có hàng. Hàng đầu cách mặt nhà
  15 mm giấy. Số không vừa khoảng giữa hai đường gióng thì dời (`dimtedit`)
  ra ngoài một đường gióng, vẫn nằm trong khoảng trống giữa hai hàng, không
  nằm trên nét của hàng bên cạnh. Không hàng nào cắt ranh đất: khi ranh nằm giữa mặt nhà và hàng
  ngoài cùng, đặt hàng đầu cách ranh 10 mm giấy về phía ngoài. Ranh trùng mặt
  nhà thì không phải dời. Đường gióng được phép cắt ranh.
- Kích thước bên trong chỉ cho vị trí vách và cửa mà ba lớp ngoài không nói
  được, mỗi thứ một lần. Đặt dọc mặt tường của phòng rộng nhất có thể, không
  đè thang, đồ đạc hay tên phòng. Không đặt chuỗi kích thước trong ô nhỏ hơn
  1,5 m: số cần ghi mà chỉ nằm trong ô nhỏ thì đặt thành một kích thước đơn
  ở cạnh ngoài gần nhất của nhà. Vị trí cửa sát cột thì ghi bằng má tường
  trong bảng cửa, không ghi bằng một chuỗi số quanh cột.
- Ký hiệu cao độ sàn so với mốc không, dạng tam giác kèm số. Sân, hành lang
  chung và mọi mặt sàn khác cao độ cũng có ký hiệu riêng.
- Ký hiệu vị trí mặt cắt, mũi tên chỉ bắc, tên hình kèm tỷ lệ. Chưa biết
  hướng bắc thì ghi một dòng "hướng bắc: chưa có" thay cho mũi tên.
- Thứ ở phía trên mặt cắt vẽ nét đứt.
- Phần dành cho đợt xây sau, trên `A-FUTR`: vách, cửa và đồ đạc giả định vẽ
  nét đứt, tên phòng kèm chữ "(mở rộng sau)" và diện tích. Người xem phải
  thấy được căn nhà lúc xong, không chỉ một khung trống.

**Dự án nhiều căn lặp lại.** Mặt bằng vẽ một đoạn dãy đủ thấy nhịp lặp: ít
nhất ba căn hoặc ba khối liền nhau trên cùng lưới trục, một ở trạng thái lúc
giao, một đã mở rộng xong. Mọi căn có lối vào vẽ được trên mặt bằng, kể cả
thang ngoài hay hành lang chung dẫn lên căn trên. Bảng số mô tả một khối và
số lần lặp; `build.py` chèn khối đó theo bước lặp, khối đã mở rộng thêm lớp
`A-FUTR` vẽ như phần đã xây. Sơ đồ toàn khu nằm ở sản phẩm 4, không trong
file này.

Các tầng đặt cạnh nhau trong không gian mô hình, cách đều, cùng một gốc trục
tương đối. Ảnh mỗi tầng cắt khung theo phạm vi của chính tầng đó cộng vùng
kích thước và tên trục, rồi nới khung cho đúng tỷ lệ khổ giấy của ảnh. Khung
khác tỷ lệ giấy thì lệnh in tự nới ra và lấn sang tầng bên. Khoảng cách giữa
gốc hai tầng ít nhất bằng bề rộng của khung đã nới, cộng 2000. Ví dụ: nhà
sâu 15 m in trên A4 đứng thì khung cao chừng 26000, rộng chừng 18400, nên
hai tầng cách nhau ít nhất 20400.

### Một hình mặt cắt phải có gì

Mặt cắt và mặt đứng chỉ vẽ khi có trong danh mục hình. Mọi cao độ lấy từ bảng
số. Bảng số khi đó có thêm: bề dày sàn, cỡ dầm, cao độ đỉnh cửa đi, bệ và đỉnh
cửa sổ, cao tường chắn mái, chiều sâu móng. Số nào người dùng không nêu thì
lấy theo thông lệ nơi xây, ghi `"by": "default"`. Móng và dầm là ước để vẽ,
kỹ sư sẽ tính.

- Đường cắt vẽ trên mặt bằng, kèm mũi tên chỉ hướng nhìn và tên (1-1). Hai
  thứ cần cắt qua không nằm trên một đường thẳng thì cắt gãy khúc, và chỗ gãy
  vẽ rõ trên mặt bằng. Đường cắt không chạy qua tên phòng hay số trên mặt
  bằng; dời chữ, không dời đường cắt. Thứ nằm phía trước một đoạn cắt gãy thì
  không vẽ trong mặt cắt.
- Thứ bị cắt nét đậm, tô đặc hoặc mẫu tô: sàn, dầm dưới sàn tại mỗi trục,
  tường, mái, móng, đất. Dưới mỗi tường bị cắt có một móng vẽ giản lược theo
  chiều sâu móng của bảng số, kể cả khi đường cắt không qua cột. Thứ nhìn thấy phía sau nét mảnh trên `A-ELEV`: cửa,
  cửa sổ, tường xa. Không vẽ phòng thành những hộp chữ nhật khép kín.
- Hướng nhìn của mặt cắt là phía có nhiều thứ người thợ cần thấy: thang,
  cửa, giếng trời. Mũi tên trên mặt bằng chỉ đúng hướng đó.
- Thang trong mặt cắt có đủ bậc, chiếu nghỉ và bản thang. Lan can vẽ bằng
  một nét tay vịn song song bản thang, cao 900 đo thẳng đứng từ mũi bậc, và
  nét đứng ở hai đầu; không vẽ từng thanh, không để nét lan can cắt nhau.
- Sàn kính và mái kính vẽ hai nét mảnh sát nhau trên `A-GLAZ`, kèm ghi chú,
  không tô như sàn bê tông.
- Cửa đi và cửa sổ bị cắt hiện đúng cao độ bệ và đỉnh.
- Mặt đất ngoài nhà và cốt sân, kèm đất bị cắt dưới sàn tầng một. Đất bị
  cắt tô mẫu `EARTH` hoặc `ANSI31` trên `C-TOPO`. Mẫu có nét thuộc diện
  cần người mở AutoCAD xem lại, ghi vào phần thứ hai của danh sách giao.
- Ký hiệu cao độ cho mặt đất, từng sàn, đỉnh mái, đỉnh tường chắn mái.
- Kích thước đứng: chuỗi chiều cao từng tầng khép về tổng chiều cao, và chuỗi
  bệ, cửa, tường của mỗi ô cửa bị cắt. Chuỗi của ô cửa khép về chiều cao
  tầng chứa nó, đặt ngay cạnh hàng chiều cao tầng nên không cần hàng tổng
  riêng.
- Trục có vòng tên dưới hình, như trên mặt bằng, và hai hàng kích thước
  ngang dưới chân: từng trục và tổng.
- Mọi không gian bị cắt có tên, cả phần giao lẫn phần mở rộng sau. Cấu kiện
  bị cắt chính (dầm, sàn, tường) có ghi chú cỡ và vật liệu, kèm chữ "ước"
  khi kỹ sư chưa tính.
- Mặt cắt chạy ngang qua một vế thang thẳng: vế bị cắt vẽ thành mặt cắt
  ngang của bản thang tại chỗ cắt, phần vế phía sau vẽ nét mảnh trên
  `A-ELEV` từ chân tới đầu, kèm tay vịn.

### Dựng

`build.py` đọc `params.json`, tính mọi tọa độ, rồi gọi CADCraft một lần để
dựng và lưu. Thứ tự: thiết lập đơn vị, layer, kiểu chữ, kiểu kích thước,
block cửa → trục → tường và cột → cửa → thang → thiết bị và đồ đạc → mẫu tô → kích thước
→ chữ và ký hiệu.

- **Tường tính trước, không vẽ rồi cắt.** Mỗi đoạn tường là một hình chữ
  nhật theo tim hoặc mép và bề dày. Đầu tường canh tim kéo tới mặt xa của
  tường nó chạm, để góc không bị khía. Mỗi ô cửa là một hình chữ nhật cắt
  ngang tường. Tường còn lại là hợp các hình tường trừ các hình ô cửa và trừ
  cột. Hai mảng tường chỉ chạm nhau tại một góc là hai đường riêng, không
  gộp thành một đường chạm chính nó. Với mặt bằng
  vuông góc: lấy mọi tọa độ mép làm lưới, đánh dấu ô nào đặc, dò biên thành
  các đường bao khép kín. Tường xiên hoặc cong thì dùng thư viện hình học
  trong môi trường ảo riêng.
- Mỗi khối tường là một đường khép kín. Mẫu tô tường lấy chính đường đó làm
  biên.
- Cửa là block chèn vào khoảng hở. Mỗi bề rộng và mỗi phía bản lề một
  block, không chèn lật gương. Hình của block là một đường nhiều đoạn có
  cung, để lệnh tạo block gom được bằng một mã đối tượng.
- Mỗi phòng có một đường bao khép kín trên `X-AREA` để đo diện tích.
- Kích thước là đối tượng kích thước thật, bám hai điểm của hình. Không gõ
  đè chữ số.
- Mỗi lần dựng ra một file mới trong `out/`, số NN tăng dần.
- Hình học dùng chung cho `preview.py` và `build.py` (đường bao tường, đường
  bao phòng, vị trí cửa) nằm ở một file `plan.py`, để sơ đồ và bản vẽ không
  lệch nhau. `check.py` không được import file này.

### Kiểm file

`check.py` chạy trong một tiến trình mới, mở file DXF đã lưu và đo. Nó không
import `build.py` và không dùng tọa độ mà `build.py` đã tính. Số kỳ vọng lấy
từ nhu cầu đã duyệt và từ `params.json`.

| Phép kiểm | Bắt lỗi gì |
|---|---|
| Đếm đối tượng, phạm vi bản vẽ, ghi chú khi đọc file. | Đối tượng lạc ra xa, thứ bị rơi khi lưu rồi mở lại. |
| Diện tích và hình tự cắt của các đường khép kín. | Tường tự cắt, phòng lệch diện tích so với nhu cầu, số ghi trên hình khác số đo. |
| Chuỗi nét hở, chỉ trên layer mà mọi nét phải khép, như tường. | Hai nét tưởng chạm nhau mà hở. |
| Chữ: nội dung, cỡ, kiểu. | Phòng thiếu tên, cỡ chữ ngoài bộ cỡ đã suy, chữ mất dấu sau khi lưu. |
| Chữ nằm trên nét của kích thước khác hay trên đường cắt. `dxf_check.py` làm phép này. | Số bị đẩy ra khỏi khoảng hẹp rơi lên hàng bên cạnh, đường cắt chạy qua tên phòng. |
| Chữ đè chữ, và chữ đè đồ đạc, thiết bị hay tầm quét cửa: tên phòng, nhãn cửa, số kích thước, ước bề rộng theo font kiểu Arial. `dxf_check.py` làm hai phép này. | Số kích thước dính nhau, tên phòng đè nhãn. Ảnh không dùng được cho việc này khi máy thiếu font. Bản vẽ chỉ được trình duyệt khi phép này không còn dòng nào. |
| Layer, block, kiểu nét đang dùng. | Đối tượng ở layer `0`, block thừa, layer thiếu. |
| Đối tượng trong vùng của từng ô cửa. | Cửa lệch khỏi ô, số cửa khác bảng số. |
| Đồ đạc và thiết bị nằm trong tầm quét của cánh cửa: so khung từng block đồ với hình quạt của cánh. | Giường chắn cửa, cửa mở không hết. `dxf_check.py` không làm phép này. |
| Vị trí thang, khu ướt, cột giữa các tầng. | Chồng tầng lệch. |
| Số đo thật của từng kích thước, và tổng mỗi chuỗi nhỏ so với kích thước tổng. | Kích thước không khép, chữ số bị gõ đè. |
| Diện tích phòng cộng tường, cột và ô cửa bằng phủ bì nhà, từng tầng, sau khi trừ phần cột lồi vào phòng. | Phòng bị sót, tường bị đếm hai lần, ô cửa ăn vào cột. |
| Trình kiểm lỗi của CADCraft, và một trình đọc DXF độc lập. | File chỉ CADCraft đọc được. |
| Phòng ghi tên bằng đường dẫn: `dxf_check.py` lần theo đoạn thẳng từ trong phòng tới chữ. | Phòng không có số diện tích. Gọi `dxf_check.py` với layer mặc định; không đưa `A-WALL` vào `--object-layers`, vì chữ nào cũng nằm trong khung bao của khối tường. |

Hàng cuối của bảng có sẵn công cụ: script `dxf_check.py` của skill, đường dẫn
ở mục "Three approvals" trong SKILL.md. Nó đọc file bằng một thư viện không
phải CADCraft và soát phiên bản, đơn vị, layer `0`, chữ, kích thước, tường và
diện tích, mà không cần biết bảng số. `check.py` của dự án lo những phép cần
bảng số.

Phép nào công cụ đang cài không làm được thì ghi "chưa kiểm được" và đưa mục
đó vào phần thứ hai của danh sách giao. Không ghi "đạt" cho thứ chưa đo.

Ảnh xuất ra dùng để người duyệt nhìn, không phải bằng chứng về dữ liệu.
Máy không có font của bản vẽ thì ảnh vẽ chữ rộng hơn thật. Chữ trông chạm
nhau trên ảnh mà `dxf_check.py` cho đạt thì không sửa theo ảnh: ghi vào phần
thứ hai của danh sách giao, để người dùng xem lại trong AutoCAD. Trước
khi cho người dùng xem, tự nhìn ảnh một lần: chữ đè nhau, nét sai kiểu, hình
trống.

Bản vẽ là chỗ xin duyệt thứ ba trong SKILL.md.

### Giao

Lưu DXF phiên bản 2018, dạng chữ, kiểu chữ dùng font Unicode đã chọn. Cả hai
điều kiện đều cần để chữ có dấu không vỡ.

Giao file kèm danh sách ba phần:

1. **Đã làm và đã đo lại.** Từng mục kèm con số đo từ file: diện tích từng
   phòng, số cửa, tổng các chuỗi kích thước.
2. **Đã làm nhưng cần mắt người trong AutoCAD.** Những thứ chưa kiểm được,
   những số còn là giả định hoặc do AI chọn, và các mục rủi ro trong
   [cadcraft.md](cadcraft.md) có mặt trong bản vẽ.
3. **Chưa làm.** Khung tên, trang in và bảng nét in, bảng thống kê, chi tiết
   tỷ lệ lớn, kết cấu và hệ thống kỹ thuật tính toán.

Kèm phiếu duyệt: chép [phieu-duyet.md](phieu-duyet.md) vào thư mục dự án
thành `review.md`, điền sẵn tên file, và mời người dùng điền sau khi mở file
trong AutoCAD. Phiếu điền xong quay về là sự thật mới của dự án: mục nào
"không" thì ghi vào ghi chép CADCraft và sửa ở lần dựng sau.

Kèm một câu nói rõ: sau khi sửa tay, dựng lại từ bảng số sẽ không mang theo
phần sửa đó.
