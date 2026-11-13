# Thang điểm chung cho mọi đề

Thang này chấm một vòng dựng bản vẽ của i:cad trên bất kỳ đề nào, để điểm của
các đề, các vòng và các phiên bản skill so được với nhau. Nó thay thang riêng
của đề Quinta Monroy ([cham-quinta-monroy.md](cham-quinta-monroy.md), giữ làm
lịch sử).

Tổng 100 điểm, bốn phần:

| Phần | Điểm | Ai chấm | Viết từ đâu |
|---|---|---|---|
| A. File dùng được | 25 | máy, qua `diem_may.py` | các trình kiểm của skill |
| B. Cách vẽ | 30 | agent chấm, nhìn ảnh | quy ước nghề và TCVN, do một agent chưa đọc skill viết |
| C. Phương án | 30 | agent chấm | riêng từng đề, viết cùng lúc với đề, trước khi chạy |
| D. Quy trình | 15 | agent chấm, đọc file | các bước của skill mà người dùng nhìn thấy |

Mỗi mục chấm một trong ba mức: đủ điểm, nửa điểm, không điểm. Mỗi điểm phải
kèm bằng chứng: tên file và dòng, hoặc tên ảnh và chỗ trên ảnh. Không có bằng
chứng thì không điểm. Người chấm phần B, C, D là một agent chưa đọc skill, theo
prompt [cham.md](cham.md).

## A. File dùng được: 25 điểm, máy chấm

Chạy `uv run tests/cad/loop/diem_may.py <file.dxf> <params.json> --build <build.py>`.
Script chạy năm trình kiểm và đổi kết quả ra điểm theo luật sau:

| # | Mục | Điểm | Đủ điểm khi | Nửa điểm khi |
|---|---|---|---|---|
| A1 | Bảng số qua `params_check.py` | 4 | Không lỗi khuôn. | — |
| A2 | File qua `dxf_check.py` | 7 | Mọi phép đạt. | Không phép nào trượt nhưng còn phép "cần xem". |
| A3 | File khớp bảng số qua `plan_check.py` | 6 | Mọi phép đạt. | Không phép nào trượt nhưng còn phép "cần xem". Bảng số hỏng (A1 bằng 0) thì không kiểm được: 0 điểm. |
| A4 | Luật qua `luat_check.py` | 4 | Không phép nào trượt. "Cần xem" không trừ điểm: nó thường là số đầu vào chưa có, không phải hình sai. Bảng số hỏng thì 0 điểm, như A3. | — |
| A5 | Audit của CADCraft | 4 | 0 lỗi. CADCraft chạy mà không ra số lỗi đọc được thì 0 điểm. Máy không có CADCraft thì mục này chưa chạy. | — |

Điểm A là tổng điểm các mục đã chạy, trên tổng điểm tối đa của chính các mục
đó; không quy đổi. Máy thiếu CADCraft cho điểm trên 21, không so được với điểm
trên 25: chấm một đợt trên máy có CADCraft. Một trình kiểm treo quá 15 phút thì
mục của nó 0 điểm. File đầu vào không đọc được thì script dừng với mã 2, không
cho điểm.

Script còn báo **tỷ lệ dòng `build.py` vẽ ngoài thư viện**: số dòng của
`build.py` dự án không có trong `skills/cad/lib/build_mau.py`, kèm số dòng của
thư viện bị bỏ đi. Con số này báo
riêng, không cộng vào điểm: nó cho biết thư viện đủ dùng tới đâu cho đề đó.

## B. Cách vẽ: 30 điểm

Danh mục này do một agent chưa đọc skill viết ngày 2026-11-13, từ quy ước nghề và tiêu chuẩn Việt Nam về trình bày bản vẽ xây dựng (TCVN 5570:2012, 6083:2012, 5671:2012, 7:1993, 5705:1993, 4614:2012, 4608:2012, 8-40:2003). Viết như vậy để skill không tự chấm mình: đừng sửa danh mục cho khớp với skill. Muốn đổi một mục thì nhờ lại một agent chưa đọc skill, kèm lý do.

Phần B không hỏi thiết kế hay hay dở. Nó hỏi: một kiến trúc sư Việt Nam nhìn vào hình có thấy được vẽ đúng quy ước nghề không. Khung tên, mã số tờ và mẫu trình bày của văn phòng không nằm trong phần này.

### Cách cho điểm

Mỗi mục được 3 điểm, 1,5 điểm hoặc 0 điểm. Đạt đúng câu "đủ điểm khi" thì được 3. Đạt câu "nửa điểm khi" thì được 1,5. Thấp hơn nữa thì 0.

Có hai mục chỉ áp cho một số hồ sơ: mục 8 (cầu thang, đường dốc, thang máy) và mục 9 (ký hiệu cải tạo). Mục nào không áp thì bỏ hẳn, và điểm phần B được quy lại theo số mục còn lại:

> Điểm B = (tổng điểm đạt) ÷ (3 × số mục được áp) × 30, làm tròn đến 0,5.

Ví dụ: một căn hộ cải tạo không có cầu thang thì chấm 9 mục. Nếu đạt 22,5 trên 27 thì điểm B là 22,5 ÷ 27 × 30 = 25.

Nhiều mục nói đến kích thước "trên giấy". Cách quy đổi: lấy kích thước trong file DXF (đơn vị mm, biến `$INSUNITS` = 4) chia cho mẫu số tỷ lệ của hình. Ví dụ: một vòng tròn trục bán kính 400 mm trong file, ở hình tỷ lệ 1:100, là bán kính 4 mm trên giấy (đường kính 8 mm). Nếu hình không ghi tỷ lệ thì không quy đổi được, và mục 10 đã bị trừ điểm vì chuyện đó.

Chuẩn thay đổi theo độ sâu hồ sơ. Nhà ở và căn hộ ở mức gần thi công phải đạt thêm những phần ghi "ở hồ sơ gần thi công". Khách sạn và tòa chung cư ở mức phương án thì không bị đòi những phần đó.

### Mười mục

Mức chắc của nguồn ghi trong ngoặc: **gốc** là đã đọc chữ của chính tiêu chuẩn. **Thuật lại** là chỉ đọc qua trang tóm tắt, qua dự thảo, hoặc chỉ đọc phần phạm vi. **Thông lệ** là cách làm của nghề, không có văn bản.

| # | Tên | Đủ 3 điểm khi | Được 1,5 điểm khi | Cách nhận ra | Nguồn và mức chắc |
|---|---|---|---|---|---|
| 1 | Đường nét: độ dày và kiểu nét | Trên mọi mặt bằng và mặt cắt cần đạt cả hai điều. Thứ nhất, đường bao phần bị mặt phẳng cắt đi qua (tường, cột, sàn, dầm) dày khoảng gấp đôi trở lên so với nét phần nhìn thấy (đồ đạc, bậc, mép sàn), và mỗi hình dùng 2 đến 3 cấp dày. Thứ hai, trục và đường tim là nét gạch dài–chấm mảnh, phần bị khuất (dầm, mép mái hay ban công tầng trên, vì kèo) là nét đứt mảnh, chỗ ngắt hình là nét dích dắc, còn đường kích thước, đường dóng, đường chú dẫn và nét gạch vật liệu là nét liền mảnh. Các nét gạch phải hiện ra đúng là gạch trên ảnh. | Chỉ đạt một trong hai điều trên. Hoặc đạt cả hai nhưng sai ở một nhóm bộ phận, ví dụ đồ đạc vẽ dày bằng tường, hay mép ban công tầng trên vẽ nét liền. | **Ảnh:** phóng to chỗ tường gặp đồ đạc rồi so bề dày nét. Nhìn đường trục và mép mái xem có ra gạch không. **DXF:** đọc lineweight của thực thể (mã nhóm 370), nếu là BYLAYER thì đọc của layer, hoặc đọc bề rộng polyline. Nếu mọi nét đều để mặc định thì ảnh sẽ ra một nét đều, không đạt. Kiểu nét: đọc thuộc tính linetype của thực thể hay layer, bảng LTYPE, `$LTSCALE` và ltscale riêng. Quy một nhịp gạch ra giấy: cỡ vài mm đến khoảng 20 mm thì mắt thấy được là gạch (thông lệ). | TCVN 6083:2012 mục 4.3–4.5 (độ dày 1:2:4, mỗi hình 2–3 loại nét, phần cắt dày hơn phần nhìn), 4.9c, 6.1 (gốc). TCVN 5570:2012 mục 3.2, Bảng 1 (gốc; cột chiều rộng nét bị mất khi trích). TCVN 5671:2012 mục 3.2.5, 3.2.11 (gốc). |
| 2 | Tô hay gạch phần bị cắt, ký hiệu vật liệu | Phần bị cắt của tường, cột, sàn, dầm trên mặt bằng và mặt cắt được tô đặc hoặc gạch bằng nét mảnh nghiêng (thường 45°). Khoảng cách giữa hai đường gạch từ 0,7 mm trở lên trên giấy. Hai bộ phận liền nhau mà khác vật liệu thì khác hướng hay khác mẫu gạch. Mẫu nào ngoài tiêu chuẩn thì có chú giải. Ở hồ sơ gần thi công, mặt cắt phải phân biệt được ít nhất tường xây với bê tông cốt thép. | Có tô hoặc gạch nhưng thiếu ở một loại hình (mặt bằng có mà mặt cắt không). Hoặc vùng gạch tràn hay hở khỏi đường bao. Hoặc gạch dày đến mức thành mảng xám. Hoặc ở hồ sơ gần thi công mọi vật liệu cùng một mẫu. | **Ảnh:** vùng bị cắt phải khác hẳn vùng nhìn thấy. **DXF:** thực thể HATCH (hoặc SOLID) có biên kín trùng đường bao tường. Đọc tên mẫu, góc, tỷ lệ mẫu, rồi quy khoảng cách đường gạch ra giấy. Kiểm biên trong `hatch.paths`. | TCVN 7:1993 mục 1.2, 1.3, 2.1, 2.2, 2.4 (gốc; các hình ký hiệu không xem được). TCVN 5671:2012 mục 3.2.5 (tường chịu lực tô đen hoặc gạch chéo), 4.1, 4.3 (gốc). TCVN 6083:2012 mục 4.6 (gốc). |
| 3 | Hệ trục định vị và hướng Bắc | Mỗi mặt bằng và mặt cắt có lưới trục. Đầu trục có vòng tròn đơn. Trục ghi số Ả Rập tăng từ trái sang phải, trục ghi chữ in hoa tăng từ dưới lên, không dùng chữ I và O. Vòng tròn có đường kính 6 mm trên giấy nếu tỷ lệ nhỏ hơn 1:200, 8 mm nếu từ 1:200 đến 1:100, 10 mm nếu lớn hơn 1:100. Một trục mang cùng tên trên mọi hình. Có kích thước giữa các trục. Mặt bằng tổng thể hay tầng 1 (với căn hộ: mặt bằng căn) có mũi tên chỉ hướng Bắc. Căn hộ cải tạo dùng trục của tòa nhà, hoặc trục tạm có ghi rõ (thông lệ). | Có trục và vòng tròn nhưng sai một quy ước: thứ tự, dùng I hay O, tên trục không khớp giữa mặt bằng và mặt cắt, thiếu kích thước trục, hoặc thiếu hướng Bắc. Hoặc chỉ một số hình có trục. | **Ảnh:** vòng tròn quanh mép hình. Đọc thứ tự ký hiệu. **DXF:** CIRCLE (hoặc INSERT một khối) nằm ở đầu mỗi đường kiểu nét trục, bên trong có TEXT hay ATTRIB. Bán kính chia mẫu số tỷ lệ phải ra 3, 4 hoặc 5 mm. So tên trục và khoảng cách trục giữa các hình. | TCVN 5570:2012 mục 4.1, 4.2, 4.3 (Bảng 2), 4.5, 4.6 (gốc). TCVN 5671:2012 mục 3.1 (hướng Bắc trên mặt bằng hiện trạng), 3.2.7, 3.2.14 (gốc). |
| 4 | Ghi kích thước | Bên ngoài mỗi mặt bằng có ba chuỗi kích thước: mảng tường và lỗ cửa, khoảng cách trục, tổng chiều dài. Số ghi bằng mm, nằm giữa và phía trên đường kích thước, không bị nét nào cắt qua. Các đoạn trong một chuỗi cộng lại đúng bằng số tổng. Mỗi số ghi khớp với khoảng cách đo được trên hình. Đầu mút là gạch chéo hoặc mũi tên, dùng thống nhất. Ở hồ sơ gần thi công có thêm kích thước hai chiều trong từng phòng và kích thước lỗ cửa. | Có chuỗi kích thước nhưng thiếu một trong ba lớp. Hoặc có tối đa 2 chỗ số bị đè, cộng không khớp, hay ghi khác số đo. Hoặc ở hồ sơ gần thi công thiếu kích thước trong phòng. | **Ảnh:** dải số quanh mép hình. Cộng thử một chuỗi. **DXF:** thực thể DIMENSION. So `get_measurement()` với chữ hiện ra: nếu chữ bị gõ đè và khác số đo thì tính là lỗi. Đường kích thước là nét mảnh. Gạch chéo 45° ở đầu mút là thông lệ của bản vẽ xây dựng. | TCVN 5671:2012 mục 2.4, 2.5, 3.2.4, 3.2.7, 3.2.9 (gốc). TCVN 5705:1993 mục 2.1.1, 2.2.1–2.2.3, 2.3.2 (gốc; tiêu chuẩn này viết cho bản vẽ kỹ thuật nói chung theo ISO R129, không riêng xây dựng). Gạch chéo: thông lệ. |
| 5 | Cao độ | Có mốc ±0.000. Mọi cao độ đều ghi bằng mét với ba chữ số thập phân và có ký hiệu cao độ: sàn các tầng trên mặt bằng; sàn, mái, đỉnh công trình trên mặt cắt và mặt đứng. Một sàn mang cùng một giá trị trên mọi hình. Hiệu cao độ của hai sàn kề nhau bằng chiều cao tầng ghi trên mặt cắt. Căn hộ cải tạo lấy ±0.000 là mặt sàn hoàn thiện của căn và ghi rõ điều đó (thông lệ). | Có cao độ nhưng thiếu ở một loại hình, ví dụ mặt bằng không ghi cao độ sàn. Hoặc có một chỗ không khớp giữa các hình. | **Ảnh:** ký hiệu cao độ đi kèm số dạng +3.300. **DXF:** TEXT hay MTEXT có dạng ±số.ba-số, hoặc INSERT khối cao độ. Trên mặt cắt, chênh tọa độ Y giữa hai ký hiệu (mm) chia 1000 phải bằng chênh hai số ghi. | TCVN 5671:2012 mục 2.5, 2.7, 3.2.4, 3.2.7, 4.1, 4.2.1, 5.1.2 (gốc). Hình dạng ký hiệu cao độ: thông lệ. |
| 6 | Mặt cắt: đường cắt, tên hình, độ khớp | Mỗi mặt cắt có đường cắt trên mặt bằng. Đường cắt vẽ nét gạch dài–chấm, hai đầu đậm. Mũi tên hướng nhìn vuông góc với đường cắt. Hai đầu mang cùng một cặp ký hiệu (A–A hay 1–1), trùng với tên hình mặt cắt. Đường cắt đi qua cầu thang (nếu có) hoặc qua cửa sổ và không gian đặc trưng. Bộ phận bị cắt trên hình mặt cắt nằm đúng chỗ đường cắt đi qua trên mặt bằng. | Có mặt cắt nhưng sai một chỗ: thiếu đường cắt trên mặt bằng, tên không khớp, hướng nhìn ngược với hình, hoặc một bộ phận lệch chỗ. | **Ảnh:** tìm ký hiệu ở hai đầu đường cắt trên mặt bằng, rồi tìm tiêu đề "MẶT CẮT A-A". **DXF:** đường kiểu nét gạch chấm có hai đoạn đầu dày hơn, cộng TEXT ký hiệu. So khoảng cách trục và vị trí tường hay cửa bị cắt giữa mặt bằng và mặt cắt. | TCVN 5671:2012 mục 2.9 (gốc: mặt phẳng cắt vẽ nét gạch dài–chấm đậm, cắt qua chỗ đặc trưng như cửa sổ, cầu thang). TCVN 8-40:2003 điều 4 (đặt tên bằng cặp chữ in hoa cạnh mũi tên: đọc được một câu gốc, phần còn lại qua tóm tắt, nên tính là thuật lại). |
| 7 | Cửa đi và cửa sổ | Trên mặt bằng, tường được ngắt tại mỗi lỗ cửa. Cánh cửa đi vẽ mở 90° có cung tròn, hoặc mở 30° hay 45° không cung, đúng phía bản lề và đúng chiều mở. Cửa lùa, cửa xếp, cửa cuốn có ký hiệu riêng. Cửa sổ hiện là một ô trong tường với nét khung và kính mảnh, khác hẳn một đoạn tường đặc. Ở hồ sơ gần thi công, mỗi cửa có mã loại (ví dụ Đ1, S2) tra được trong bảng thống kê cửa. | Có ký hiệu nhưng một số cửa thiếu chiều mở. Hoặc một số cửa sổ vẽ như tường liền. Hoặc ở hồ sơ gần thi công thiếu mã cửa hay thiếu bảng thống kê. | **Ảnh:** mặt bằng. **DXF:** ARC có tâm ở bản lề, bán kính bằng bề rộng cánh, góc quét 90° (thường nằm trong một INSERT khối cửa; đọc tên khối và thuộc tính). Không có đường tường nào chạy qua lỗ cửa. | TCVN 6083:2012 mục 5.1–5.4 (gốc). TCVN 4614 Bảng 2, Bảng 3: ký hiệu cửa sổ, cửa đi; từ tỷ lệ 1:50 trở lên vẽ đúng khuôn cánh (thuật lại: đọc từ bản dự thảo soát xét, bản 2012 mới đọc phần phạm vi). TCVN 5671:2012 mục 3.2.4, 3.2.9, 3.2.13 (gốc). |
| 8 | Cầu thang, đường dốc, thang máy. *Chỉ áp khi trong phạm vi vẽ có ít nhất một trong ba thứ này. Không áp thì bỏ mục và quy điểm như phần "Cách cho điểm".* | Trên mặt bằng: bậc vẽ nét mảnh. Mũi tên liền chỉ hướng đi lên đặt giữa vế thang, bắt đầu bằng một chấm tròn ở bậc đầu. Ở các tầng dưới, vế thang bị cắt có nét ngắt dích dắc. Ở tầng trên cùng, vế thang vẽ trọn. Đường dốc có mũi tên kèm độ dốc. Thang máy là một ô có hai đường chéo. Ở hồ sơ gần thi công thêm: bậc đánh số từ 1 ở dưới lên, có bề rộng vế và kích thước bậc. | Có bậc và mũi tên nhưng thiếu một quy ước: không có chấm đầu, không có nét ngắt, hoặc mũi tên ngược chiều đi lên. Hoặc số bậc trên mặt bằng khác số bậc trên mặt cắt. | **Ảnh:** mặt bằng các tầng và mặt cắt qua thang. **DXF:** một nhóm đoạn thẳng song song cách đều (các bậc), polyline mũi tên, CIRCLE nhỏ ở đầu mũi tên. Đếm số bậc trên mặt bằng và trên mặt cắt. Chiều cao tầng chia số bậc phải ra chiều cao bậc ghi trên hình. | TCVN 6083:2012 mục 4.9, 4.10 (gốc). TCVN 4614 Bảng 4: chấm nhỏ ở bậc đầu, cắt ở cao 1 m, mũi tên tầng trên cùng vẽ tới mép thang, ký hiệu thang máy (thuật lại: đọc từ dự thảo). TCVN 5671:2012 mục 3.2.9, 4.3 (gốc). |
| 9 | Ký hiệu cải tạo. *Chỉ áp khi hồ sơ là cải tạo: căn hộ cải tạo, hoặc nhà ở cải tạo. Không áp thì bỏ mục và quy điểm như phần "Cách cho điểm".* | Ba loại tường được vẽ khác nhau theo một quy ước dùng chung cho mọi hình: tường giữ nguyên, tường phá dỡ (thường nét đứt), tường xây mới (thường tô hay gạch đặc). Lỗ mở mới và lỗ bít lại có ký hiệu riêng. Trên bản vẽ có chú giải các ký hiệu đó. | Chỉ phân biệt được hai trong ba loại tường. Hoặc thiếu chú giải. Hoặc chỉ một hình phân biệt, còn hình khác vẽ lẫn. | **Ảnh:** so mặt bằng hiện trạng, mặt bằng phá dỡ và mặt bằng xây mới. **DXF:** ba nhóm tường tách nhau theo layer, kiểu nét hay mẫu HATCH. Tường phá dỡ có kiểu nét đứt. | TCVN 4614:2012 mục 1.2f "Ký hiệu các bộ phận cần sửa chữa" (gốc, đọc ở phần phạm vi). Hình ký hiệu cụ thể: tường hiện trạng, tường mới, tường phá bỏ, lỗ mới, lỗ bít (thuật lại: đọc từ Bảng 6 của dự thảo). |
| 10 | Chữ trên hình: tên hình, tỷ lệ, tên và diện tích phòng | Mỗi hình có tên (ví dụ "MẶT BẰNG TẦNG 2", "MẶT CẮT A-A") kèm tỷ lệ thuộc dãy chuẩn (1:20, 1:50, 1:100, 1:200, 1:500, 1:1000…). Mỗi phòng có tên đặt trong phòng và diện tích m² có gạch dưới. Trên giấy, chữ cao từ 2 mm trở lên và số kích thước từ 2,5 mm trở lên. Mỗi hình dùng không quá 4 cỡ chữ. Chữ tiếng Việt hiện đủ dấu. Không chữ nào bị nét vẽ hay chữ khác đè lên. | Thiếu một phần: ví dụ có tên phòng mà không có diện tích, hay vài hình thiếu tỷ lệ. Hoặc có 1 đến 3 chỗ chữ bị đè hay mất dấu. | **Ảnh:** tiêu đề dưới mỗi hình, chữ trong từng phòng. Phóng to những chỗ dày nét. **DXF:** chiều cao TEXT hay MTEXT chia mẫu số tỷ lệ, so với 2 và 2,5 mm. Đếm số cỡ chữ khác nhau trên mỗi hình. Khung bao chữ (ezdxf.bbox) không được giao với nét khác hay chữ khác. Font chữ phải có glyph tiếng Việt. Nếu có đường bao phòng thì so diện tích ghi với diện tích tính từ đường bao. | TCVN 5671:2012 mục 2.6 kèm chú thích 2 (ghi tỷ lệ cạnh hình), 2.8, 3.2.4 (gốc). TCVN 4608:2012 mục 1.3 và chú thích (chữ không nhỏ hơn 2 mm, không quá 4 khổ chữ; gốc, đọc ở phần phạm vi). TCVN 5705:1993 mục 2.3.1 (gốc). TCVN 6003-2:2012 về tên và số phòng (thuật lại, mới đọc phạm vi). Chữ hiện đủ dấu: thông lệ. |

### Những chỗ còn chưa chắc

**TCVN 4614:2012**, về ký hiệu cửa, cầu thang và các bộ phận cần sửa chữa, mới chỉ đọc được phần phạm vi. Các hình ký hiệu chi tiết lấy từ bản dự thảo soát xét mà Viện Kiến trúc Quốc gia công bố năm 2025. Phạm vi của bản dự thảo trùng với bản 2012, nhưng các góc mở cửa hay các mũi tên cầu thang vẫn có thể khác bản 2012 đôi chút. Vì vậy mục 7, 8 và 9 nên chấm dễ khi ký hiệu chỉ lệch về hình vẽ mà vẫn đúng ý (có chiều mở, có hướng lên, phân biệt được tường phá và tường mới).

**Gạch chéo ở đầu đường kích thước và hình dạng ký hiệu cao độ** là thông lệ nghề. Tiêu chuẩn về ghi kích thước đọc được (TCVN 5705:1993) viết cho bản vẽ kỹ thuật nói chung. Nó nói về mũi tên và dấu chấm, không nói về gạch chéo.

**Chiều rộng nét cụ thể** (ví dụ nét đậm bao nhiêu mm) bị mất khi trích bảng của TCVN 5570:2012. Vì vậy mục 1 chấm theo tỷ lệ dày giữa các nét (1:2:4 theo TCVN 6083:2012), không chấm theo số mm.

**Nét đường cắt mặt cắt:** TCVN 5671:2012 ghi "gạch dài – chấm đậm", còn trang tóm tắt TCVN 8-40:2003 ghi nét mảnh có hai đầu đậm. Mục 6 chấp nhận cả hai cách.

### Nguồn đã mở (ngày mở: 2026-11-13)

Tình trạng hiệu lực tra trên trang của Viện Tiêu chuẩn Chất lượng Việt Nam (VSQI). Mọi tiêu chuẩn dưới đây đều ghi "A – Còn hiệu lực".

| Nguồn | Đọc được gì | Mức chắc |
|---|---|---|
| https://tieuchuan.vsqi.gov.vn/tieuchuan/view?sohieu=TCVN+4614%3A2012 | Tình trạng, thay thế TCVN 4614:1988, phạm vi mục 1.1–1.2 (có "ký hiệu các bộ phận cần sửa chữa"); có kế hoạch soát xét | gốc (phần phạm vi) |
| Cùng trang VSQI, với `sohieu` = TCVN 5570:2012, TCVN 6083:2012, TCVN 5671:2012, TCVN 4608:2012, TCVN 8-20:2002, TCVN 8-40:2003, TCVN 8-50:2005, TCVN 7:1993, TCVN 7286:2003, TCVN 5705:1993, TCVN 5895:2012, TCVN 5896:2012, TCVN 6003-2:2012, TCVN 6077:2012, TCVN 5686:2012, TCVN 9256:2012 | Tình trạng hiệu lực, tên, tiêu chuẩn bị thay thế, phạm vi. Với TCVN 4608:2012, phạm vi có câu chữ không nhỏ hơn 2 mm và không quá 4 khổ chữ | gốc (phần phạm vi); thuật lại cho nội dung còn lại |
| https://luatminhkhue.vn/tieu-chuan-quoc-gia-tcvn-6083-2012-iso-7519-1991-ve-ban-ve-ky-thuat-ban-ve-xay-dung-nguyen-tac-chung-ve-trinh-bay-ban-ve-bo-cuc-chung-va-ban-ve-lap-ghep.aspx | Toàn văn mục 1–7 (nét, cầu thang, đường dốc, cửa, trần treo, mũi tên); các hình bị mất | gốc |
| https://luatminhkhue.vn/van-ban/tieu-chuan-quoc-gia-tcvn-5570-2012-ve-he-thong-tai-lieu-thiet-ke-xay-dung-ky-hieu-duong-truc-va-duong-net-trong-ban-ve.aspx | Toàn văn Bảng 1 (loại nét và phạm vi dùng) và mục 4 (trục); cột chiều rộng nét và các hình bị mất | gốc |
| https://luatminhkhue.vn/tieu-chuan-quoc-gia-tcvn-5671-2012-ve-he-thong-tai-lieu-thiet-ke-xay-dung-ho-so-thiet-ke-kien-truc.aspx | Toàn văn: quy định chung, mặt bằng, mặt cắt, mặt đứng, chi tiết | gốc |
| https://luatminhkhue.vn/van-ban/tieu-chuan-quoc-gia-tcvn-7-1993-ve-ky-hieu-vat-lieu.aspx | Toàn văn mục 1–2; hình các ký hiệu vật liệu bị mất | gốc |
| https://luatminhkhue.vn/van-ban/tieu-chuan-quoc-gia-tcvn-5705-1993-ve-quy-tac-ghi-kich-thuoc.aspx | Toàn văn mục 1–2 (đường dóng, mũi tên, chữ số kích thước) | gốc |
| https://vienkientrucquocgia.gov.vn/wp-content/uploads/2025/04/20.6.BanVeXD-KyHieu-4614-89.6.pdf | Dự thảo "Bản vẽ xây dựng – Ký hiệu trên bản vẽ – Phần 2: Các bộ phận cấu tạo ngôi nhà" (thay TCVN 4614): Bảng 1–6 kèm hình | thuật lại (đọc nguyên văn, nhưng là dự thảo chứ không phải bản 2012 đang hiệu lực) |
| https://hethongphapluat.com/tieu-chuan-viet-nam-tcvn-8-40-2003-iso-128-40-2001-ve-ban-ve-ky-thuat-nguyen-tac-chung-ve-bieu-dien-phan-40-quy-uoc-co-ban-ve-mat-cat-va-hinh-cat-do-bo-khoa-hoc-va-cong-nghe-ban-hanh.html | Một câu gốc của điều 4 (đặt tên mặt cắt bằng cặp chữ in hoa cạnh mũi tên) cùng phần tóm tắt; phần sau phải trả phí | thuật lại |
| https://caselaw.vn/van-ban-phap-luat/178260-quyet-dinh-so-3621-qd-bkhcn-ngay-28-12-2012-cua-bo-truong-bo-khoa-hoc-va-cong-nghe-cong-bo-tieu-chuan-quoc-gia | Danh mục các TCVN công bố theo Quyết định 3621/QĐ-BKHCN (28/12/2012) | thuật lại |

Những trang đã thử mở nhưng không đọc được: thuvienphapluat.vn (trả về 403) và vanbanphapluat.co (từ chối kết nối).

## C. Phương án: 30 điểm, riêng từng đề

Mỗi đề có một file `<tên-đề>.c.md` nằm cạnh đề, viết cùng lúc với đề và trước
khi chạy, để điểm không bị kéo theo kết quả. File đó có 4 đến 6 mục cộng lại
30 điểm. Mỗi mục có điểm, "đủ điểm khi", "nửa điểm khi" và "cách nhận ra trên
file"; viết thành bảng như mẫu dưới, hay mỗi mục một tiêu đề có số điểm trong
ngoặc, ví dụ "## 2. Mọi phòng ngủ có cửa sổ ra ngoài trời (6 điểm)":

| # | Mục | Điểm | Đủ điểm khi | Nửa điểm khi | Cách nhận ra trên file |
|---|---|---|---|---|---|
| C1 | (một bài toán của đề, ví dụ "giữ được kết cấu cũ") | | | | (ảnh nào, bảng nào, ghi chép nào) |

Mục C là bài toán của đề, không phải ý thích về hình thức. Một phương án khác
lời giải người viết đề nghĩ tới vẫn ăn điểm khi nó giải được cùng bài toán và
có số chứng minh.

**Nhiễm lời giải.** Agent dựng bản vẽ và agent chấm cùng tự khai có nhận ra
công trình có thật nào không. Nhận ra, hoặc trong file có tên dự án, tên văn
phòng hay nguồn tra là bài viết về chính công trình đó, thì điểm C ghi kèm chữ
"nhiễm" và không dùng để so với vòng khác.

## D. Quy trình: 15 điểm

| # | Mục | Điểm | Đủ điểm khi | Nửa điểm khi |
|---|---|---|---|---|
| D1 | Ghi chép dự án | 3 | Có file ghi chép dự án; mỗi điều đang biết mang nguồn hay mức chắc (người dùng nói, văn bản gốc, nguồn thuật lại, thông lệ, ước lượng). | Có file nhưng một số điều không có nguồn. |
| D2 | Cân nhắc cách xếp | 4 | Đề để ngỏ cách xếp: ít nhất hai cách, mỗi cách có số và sơ đồ đúng tỷ lệ. Đề đã định sẵn cách xếp: giữ đúng đề và nói rõ chỗ nào phải tự quyết. | Có hai cách nhưng thiếu số hay sơ đồ; hoặc tự đổi điều đề đã định mà có nói lý do. |
| D3 | Chỉ tiêu so với đề | 3 | Có bảng diện tích từng phòng hay từng căn, diện tích sàn, mật độ, tầng cao, và so từng số với đề hay luật. | Có bảng nhưng không so. |
| D4 | Câu hỏi và giả định | 2 | Mỗi điều phải hỏi được ghi kèm giả định đang dùng, không đoán rồi im. | — |
| D5 | Dừng đúng chỗ | 3 | Dừng trước lần duyệt cuối với danh sách việc còn lại cho người dùng, gồm phần chưa vẽ được. | Có dừng nhưng danh sách thiếu phần chưa vẽ được. |

## Mẫu báo điểm

| Phần | Điểm | Trên | Số mục mất điểm |
|---|---|---|---|
| A. File dùng được | | 25 | |
| B. Cách vẽ | | 30 | |
| C. Phương án | | 30 | |
| D. Quy trình | | 15 | |
| Tổng | | 100 | |

Kèm một dòng: tỷ lệ dòng `build.py` vẽ ngoài thư viện. Với đề luyện, mỗi mục
mất điểm ghi thêm một câu: thiếu gì, thấy ở đâu. Với đề giữ riêng, chi tiết
nằm trong thư mục làm việc, người sửa skill không đọc (xem
[quy trình đợt](quy-trinh-dot.md)).
