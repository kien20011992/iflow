# Từ cách xếp đã chọn tới file DXF

Đọc file này trước khi làm sản phẩm 5 đến 7: bảng số, bản kiểm, bản vẽ và
danh sách giao. Cách gọi CADCraft nằm ở [cadcraft.md](cadcraft.md).

Nguyên tắc xuyên suốt: mọi tọa độ trong sơ đồ và bản vẽ được tính từ bảng
số. Không con số hình học nào được gõ tay trong script. Muốn đổi bản vẽ thì
sửa bảng số rồi dựng lại toàn bộ. Cách vẽ (cửa, thang, kích thước, nhãn,
mặt cắt) nằm trong thư viện `lib/` của skill, có bài tự thử; file này chỉ
giữ phần phán đoán: hỏi gì, kiểm gì, giao gì.

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
| Layer, màu, độ dày nét | Bộ mặc định trong file mẫu của skill, `assets/mau.dxf` (danh sách `LAYERS` trong `assets/dung_mau.py`). Văn phòng có bảng riêng thì dùng bảng đó. |
| Font chữ | Một font TrueType Unicode có dấu của ngôn ngữ dùng trên bản vẽ, mặc định Arial. Kiểu chữ ghi tên file kèm đuôi, ví dụ `arial.ttf`: AutoCAD đọc tên không đuôi như một font SHX. |
| File mẫu | `assets/mau.dxf` của skill. Văn phòng có file mẫu riêng thì thay vào đó. Khung tên và trang in để người dùng làm trong AutoCAD. |

Mặc định nào mâu thuẫn với một số người dùng đã đưa thì mặc định nhường. Ví
dụ: trục ở tim tường bao làm nhà rộng hơn lô đất người dùng nêu. Khi đó chỗ
ấy thành một lựa chọn phải hỏi, theo mục "Asking" trong SKILL.md.

## Sản phẩm 5: bảng số

`params.json` ghi cách xếp đã chọn thành số, theo khuôn `cad-params/1` ở
[bang-so.md](bang-so.md), và phải qua `scripts/params_check.py` trước khi
xin duyệt. Nó phải đủ để một người khác dựng lại đúng bản vẽ mà không cần
hội thoại.

Phán đoán khi ghi bảng số:

- Số phụ người dùng không nêu thì lấy mặc định, ghi `"by": "default"`:
  chiếu nghỉ sâu bằng bề rộng vế thang; cửa đi mở vào phòng mà nó dẫn tới,
  cửa ra ngoài nhà mở vào trong, trừ cửa trên lối thoát nạn; má tường hai
  bên ô cửa ít nhất 100. Má không đủ 100 thì hạ bề rộng cửa một bậc (900
  xuống 800), ghi `"by": "model"` và nêu khi xin duyệt.
- Kích thước người dùng nêu mà không nói đo tới tim hay tới mặt tường, đo
  lọt lòng hay theo trục, là một lựa chọn phải hỏi, không tự chọn. Ví dụ:
  "cách trục 2 đúng 2000", "vệ sinh 1500×2000".
- Chỉ hỏi những số mà hình trong danh mục dùng tới. Danh mục chỉ có mặt bằng
  thì chưa cần cao cửa, cao bệ cửa sổ, mái hay `structure`.
- Số nào đọc từ phác thảo mà không chắc thì hỏi lại, không đoán rồi im.
- Thứ khuôn không tả được (tường cong, thang xoắn, ram dốc) không ép vào:
  ghi một dòng `outside`, để nó được đánh dấu và giao lại.
- Một file dùng một tỷ lệ. Chi tiết tỷ lệ lớn hơn, như thang 1:50, thuộc
  phần để lại cho người dùng. Cỡ chữ và khoảng cách chú thích tính từ tỷ lệ
  trong thư viện (`PAPER` trong `lib/lenh.py`), không nhập tay.

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

### Dựng

Chép `lib/build_mau.py` vào thư mục dự án thành `build.py`, rồi chỉ sửa phần
riêng của dự án; giữ nguyên đầu file, chỗ nó tìm thư viện. Chạy
`CAD_SKILL_DIR=<thư mục skill> python3 build.py params.json out/<tên>-NN.dxf --png`:
mỗi lần dựng một file mới, số NN tăng dần, không ghi đè file đã giao. Lần
chạy in danh sách "Chưa vẽ"; danh sách đó đi vào phần thứ hai hay thứ ba
của danh sách giao.

Việc nào do hàm nào làm, để biết sửa ở đâu khi một hình sai:

| Việc | Hàm |
|---|---|
| Khối tường, đường bao và diện tích phòng | `hinh.Cells`, `hinh.room_outline` |
| Cửa đi, cửa sổ, cửa cuốn, nhãn cửa | `mat_bang.ve_o_cua`, `mat_bang.nhan_cua` |
| Tên và diện tích phòng, cả khi phải đặt ngoài nhà có đường dẫn | `mat_bang.ten_phong`, `mat_bang.ten_phong_ngoai` |
| Ba hàng kích thước, trục và vòng tên trục | `mat_bang.hang_kich_thuoc`, `mat_bang.truc` |
| Thang, giếng trời, lan can, hộp kỹ thuật, đồ đạc và thiết bị | `ky_hieu.thang`, `gieng_troi`, `lan_can`, `hop_ky_thuat`, `do_dac` |
| Cao độ sàn, mũi tên bắc, đường cắt trên mặt bằng | `ky_hieu.cao_do`, `huong_bac`, `duong_cat` |
| Mặt cắt | `mat_cat.mat_cat` |
| Trải cụm đặt lặp, tách tường theo giai đoạn | `bang_so.Floor` |
| Vẽ tường phá, tường xây sau | `mat_bang.tuong_giai_doan` |

Một hình sai vì cách vẽ thì sửa hàm, block hay file mẫu, kèm bài thử trong
`tests/cad/lib_selftest.py`, không thêm câu chữ vào file này.

**Phán đoán thư viện không làm thay.** Các chọn lựa này nằm trong bảng số,
nên phải nghĩ trước khi ghi:

- Hướng nhìn của mặt cắt (`sections[].look`) là phía có nhiều thứ người thợ
  cần thấy: thang, cửa, giếng trời. Mặt cắt nên qua thang.
- Dự án nhiều căn lặp lại: danh mục hình cho thấy một đoạn dãy đủ thấy nhịp
  lặp, ít nhất ba căn hoặc ba khối liền nhau trên cùng lưới trục, một ở
  trạng thái lúc giao và một đã mở rộng xong (phần mở rộng là `phase:
  future`). Mọi căn có lối vào vẽ được, kể cả thang ngoài hay hành lang
  chung dẫn lên căn trên.
- Gốc các hình (`drawings[].origin`) cách nhau đủ xa để ảnh của hình này
  không lấn sang hình kia: ít nhất bề rộng hình cộng hai bên hàng kích
  thước và vòng trục, cộng 2000. Ví dụ nhà sâu 15 m ở 1:100 thì hai tầng
  đặt cạnh nhau cách nhau ít nhất chừng 22000; ở 1:200 gấp đôi phần chú
  thích.
- Văn phòng in theo bảng nét gắn với màu thì màu layer theo bảng của họ:
  thay file mẫu, không sửa từng bản vẽ.

**Thứ thư viện chưa vẽ.** Thư viện không vẽ được thì không vẽ tay trong
`build.py`: để nguyên đám mây đánh dấu, đưa vào danh sách giao, và ghi vào sổ
quan sát cho đợt sửa skill sau. Hôm nay thư viện chưa có: tường xiên và cong,
thang chữ L, mặt cắt cắt ngang một vế thang, mặt đứng, lan can quanh lỗ thang
ở tầng trên cùng, mái kính trên mặt cắt, mẫu tô phân biệt hai loại tường.

### Kiểm file

Ba trình kiểm, đều đọc file đã lưu bằng một chương trình không phải thư viện
vẽ:

| Trình kiểm | Kiểm gì |
|---|---|
| `scripts/dxf_check.py` | File với chính nó: phiên bản, đơn vị, layer `0`, chữ có dấu, font, kích thước khớp hình và các hàng khép, tường khép kín, diện tích ghi khớp đường bao, chữ đè chữ, chữ đè đồ đạc và tầm quét cửa, chữ nằm trên nét kích thước hay đường cắt. |
| `scripts/plan_check.py` | File với bảng số: ô cửa đủ và đúng chỗ, mỗi phòng một đường bao, diện tích so với nhu cầu, phòng cộng tường bằng phủ bì, cột và khu ướt chồng tầng, thang đi được, cánh cửa không vướng đồ, tới được mọi phòng, không xuyên phòng riêng. |
| `audit` của CADCraft | Lỗi cấu trúc file. |

`check.py` của dự án chỉ còn cho phép kiểm thật sự riêng của dự án đó. Phép
nào không chạy được thì ghi "chưa kiểm được" và đưa mục đó vào phần thứ hai
của danh sách giao. Không ghi "đạt" cho thứ chưa đo.

Ảnh xuất ra dùng để người duyệt nhìn, không phải bằng chứng về dữ liệu.
Máy không có font của bản vẽ thì ảnh vẽ chữ rộng hơn thật. Chữ trông chạm
nhau trên ảnh mà `dxf_check.py` cho đạt thì không sửa theo ảnh: ghi vào phần
thứ hai của danh sách giao, để người dùng xem lại trong AutoCAD. Trước khi
cho người dùng xem, tự nhìn ảnh một lần: chữ đè nhau, nét sai kiểu, hình
trống. Chỗ mắt thấy sai mà máy không bắt là một dòng cho sổ quan sát.

Bản vẽ là chỗ xin duyệt thứ ba trong SKILL.md.

### Giao

Lưu DXF phiên bản 2018, dạng chữ, kiểu chữ dùng font Unicode đã chọn. Cả hai
điều kiện đều cần để chữ có dấu không vỡ.

Giao file kèm danh sách ba phần:

1. **Đã làm và đã đo lại.** Từng mục kèm con số đo từ file: diện tích từng
   phòng, số cửa, tổng các chuỗi kích thước.
2. **Đã làm nhưng cần mắt người trong AutoCAD.** Những thứ chưa kiểm được,
   những số còn là giả định hoặc do AI chọn, các mục rủi ro trong
   [cadcraft.md](cadcraft.md) có mặt trong bản vẽ, và các dòng "Chưa vẽ" của
   `build.py` (đám mây trên bản vẽ chỉ chỗ cần người vẽ tiếp).
3. **Chưa làm.** Khung tên, trang in và bảng nét in, bảng thống kê, chi tiết
   tỷ lệ lớn, kết cấu và hệ thống kỹ thuật tính toán.

Kèm phiếu duyệt: chép [phieu-duyet.md](phieu-duyet.md) vào thư mục dự án
thành `review.md`, điền sẵn tên file, và mời người dùng điền sau khi mở file
trong AutoCAD. Phiếu điền xong quay về là sự thật mới của dự án: mục nào
"không" thì ghi vào ghi chép CADCraft và sửa ở lần dựng sau.

Kèm một câu nói rõ: sau khi sửa tay, dựng lại từ bảng số sẽ không mang theo
phần sửa đó.
