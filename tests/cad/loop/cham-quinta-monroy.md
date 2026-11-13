# Thang điểm cho vòng chạy đề Iquique

Thang này viết trước khi chạy, để điểm không bị kéo theo kết quả. Agent dựng
bản vẽ không được đọc file này, không được xem bốn bản vẽ gốc.

Bốn bản vẽ gốc (mặt bằng tầng 1, 2, 3 và mặt cắt của công trình đã xây) nằm
ngoài repo, ở `~/projects/personal/docs/iflow/dxf-gan-production-ba76/explore/quinta-ref/`.
Chúng chỉ dùng để chấm phần B và phần C.

Tổng 100 điểm, chia bốn phần. Mỗi mục, kể cả phần D, chấm một trong ba mức: đủ
điểm, nửa điểm, không điểm. Mỗi điểm phải kèm bằng chứng: tên file, dòng, hoặc chỗ
trên ảnh. Không có bằng chứng thì không điểm.

## A. File dùng được: 20 điểm, máy đo

| # | Mục | Điểm | Đủ điểm khi | Nửa điểm khi |
|---|---|---|---|---|
| A1 | `dxf_check.py` | 8 | Mã thoát 0, không còn dòng "cần xem". | Mã thoát 0 nhưng còn dòng "cần xem". |
| A2 | Trình kiểm lỗi CADCraft | 4 | 0 lỗi. | Có lỗi nhưng tự sửa được. |
| A3 | `check.py` của dự án | 4 | Có, và không phép nào trượt. | Có nhưng còn phép trượt đã ghi vào danh sách giao. |
| A4 | Đủ hình | 4 | Mặt bằng mọi tầng của một cụm nhà lặp lại, và một mặt cắt ngang cụm. | Thiếu mặt cắt hoặc thiếu một tầng. |

## B. Cách vẽ so với bản vẽ gốc: 30 điểm, người chấm nhìn ảnh

Mỗi mục 3 điểm. Không đòi giống từng nét. Đòi bản vẽ nói được cùng điều mà
bản gốc nói, bằng ký hiệu người thợ đọc được.

| # | Bản gốc làm gì | Đủ điểm khi bản vẽ của skill |
|---|---|---|
| B1 | Lưới trục đều, có tên ở cả hai đầu. | Có lưới trục theo một khoảng lặp, tên trục hai đầu. |
| B2 | Kích thước nhiều lớp trên và dưới hình: tổng, trục, chi tiết tới mép tường và ô cửa. | Có ít nhất ba lớp, khép kín, ở hai cạnh đối nhau. |
| B3 | Tường bị cắt đậm, phân biệt kết cấu bê tông với tường blốc bằng mẫu tô. | Tường đậm, và kết cấu (cột, tường ngăn lửa) khác tường thường. |
| B4 | Phần mở rộng sau vẽ nét đứt, ghi chữ "phần mở rộng", kèm đồ đạc giả định nét đứt. | Phần mở rộng hiện rõ trên mọi tầng có nó, nét đứt, có ghi chú, và có đồ đạc giả định. |
| B5 | Cửa đi P, cửa sổ V có nhãn tròn; cửa có cánh và cung mở. | Đủ nhãn và cung mở. |
| B6 | Bếp và vệ sinh có thiết bị: bồn cầu, chậu rửa, chỗ tắm, bếp nấu, chậu bếp. | Đủ thiết bị ở mọi khu ướt. |
| B7 | Thang có số bậc; thang ngoài lên căn trên vẽ rõ. | Mọi thang có số bậc, hướng lên. |
| B8 | Cao độ sàn ghi trên mặt bằng (±0,00, −0,20). | Mỗi mặt bằng có cao độ sàn và sân. |
| B9 | Ký hiệu vị trí mặt cắt trên mặt bằng. | Có, và trùng chỗ mặt cắt thật. |
| B10 | Mặt cắt có dầm và sàn bị cắt, móng, đất, cao độ từng sàn, kích thước trục, tên từng không gian kể cả phần mở rộng. | Có ít nhất năm trong sáu thứ đó. |

Nửa điểm khi có thứ đó nhưng sai hoặc thiếu ở một phần hình.

## C. Phương án so với lời giải đã xây: 35 điểm, người chấm

Lời giải đã xây, để đối chiếu: nhà thấp tầng xếp thành dãy; mỗi khối có một
căn dưới (một tầng, mở rộng ngang ra khe đất bên cạnh) và một căn trên (hai
tầng, mở rộng vào khe trống trong khung nhà); phần giao là khoảng 36 m² với
kết cấu, bếp, vệ sinh, thang; phần còn lại là khe giữa các khối để dân tự
xây; các dãy quây quanh sân chung khoảng 20 hộ.

Không đòi trùng lời giải. Một phương án khác ăn điểm khi nó giải được cùng
bài toán và có số chứng minh.

| # | Mục | Điểm | Đủ điểm khi | Nửa điểm khi |
|---|---|---|---|---|
| C1 | Ở lại đất, đủ 100 hộ, nhà thấp tầng | 6 | Có sơ đồ xếp đủ 100 hộ trên 5.000 m², không quá 3 tầng, có số mật độ. | Đủ hộ nhưng phải lên cao tầng, hoặc thiếu sơ đồ. |
| C2 | Diện tích giao tính từ tiền | 5 | Diện tích giao suy ra từ 3.800 USD và một đơn giá có nguồn hay ước có ghi rõ. | Có con số nhưng không nói từ đâu. |
| C3 | Chỗ mở rộng nằm sẵn trong khung | 6 | Mỗi hộ có chỗ mở rộng tới 70–72 m² nằm trong khung đã xây hoặc trong khe đã chừa, không lấn sân chung, không cần kỹ sư. | Có chỗ mở rộng nhưng chỉ cho một số hộ, hoặc phải phá kết cấu. |
| C4 | Làm sẵn phần khó | 5 | Kết cấu, bếp, vệ sinh, thang, tường ngăn lửa giữa hai hộ đều nằm trong phần giao. | Thiếu một thứ. |
| C5 | Mỗi kiểu hộ đều mở rộng được | 5 | Hộ ở dưới và hộ ở trên đều có lối mở rộng riêng, kèm diện tích cuối của từng kiểu. | Chỉ một kiểu hộ mở rộng được. |
| C6 | Sân chung theo nhóm | 4 | Hộ gom thành nhóm quanh một sân chung, có số hộ mỗi nhóm. | Có sân nhưng không nói ai dùng. |
| C7 | Nơi xây được tra | 4 | Khí hậu, động đất, luật xây dựng Chile cho nhà ở xã hội được tra, có nguồn và mức chắc. | Có nêu nhưng là ước lượng không nguồn. |

Đề bài đã nói sẵn "giao nửa khó" và liệt kê phần khó, nên C2 và C4 một phần do
đề cho. Báo cáo điểm ghi riêng điểm C trừ C2 và C4 để thấy phần skill tự nghĩ.

## D. Quy trình của skill: 15 điểm, người chấm đọc file

| # | Mục | Điểm | Đủ điểm khi |
|---|---|---|---|
| D1 | `project.md` theo mẫu | 3 | Đủ mục, mỗi điều đang biết mang một trong năm mức chắc của skill: người dùng nói, văn bản gốc, nguồn thuật lại, thông lệ hoặc mặc định, AI ước lượng. Nhãn "giả định theo lệnh người dùng" cũng hợp lệ. |
| D2 | So nhiều cách xếp | 4 | Ít nhất hai cách xếp, mỗi cách có số và sơ đồ đúng tỷ lệ. |
| D3 | Sổ tiền | 3 | Đất, hạ tầng, xây dựng được tính ra m² và so với 70–72 m². |
| D4 | Câu hỏi và giả định | 2 | Mỗi điều phải hỏi được ghi kèm giả định đang dùng, không đoán rồi im. |
| D5 | Dừng đúng chỗ | 3 | Dừng trước lần duyệt thứ ba với danh sách việc còn lại cho người dùng. |

## Nhiễm lời giải

Agent tự khai ở cuối báo cáo nó có nhận ra công trình hay không. Nhận ra, hoặc
trong file có tên dự án, tên văn phòng, hoặc nguồn tra là bài viết về chính
công trình này, thì điểm phần C ghi kèm chữ "nhiễm" và không dùng để so với
vòng khác.

## Mẫu báo điểm

| Phần | Điểm | Trên |
|---|---|---|
| A. File dùng được | | 20 |
| B. Cách vẽ | | 30 |
| C. Phương án | | 35 |
| D. Quy trình | | 15 |
| Tổng | | 100 |
| C trừ C2, C4 | | 25 |

Mỗi mục mất điểm ghi một câu: thiếu gì, thấy ở đâu.

## Điểm các vòng đã chấm

| Vòng | A | B | C | D | Tổng | C trừ C2, C4 | Ghi chú |
|---|---|---|---|---|---|---|---|
| 9 | 16 | 22,5 | 25,5 nhiễm | 12 | 76 | 18 nhiễm | Chấm lại theo thang đã làm rõ A1, B4, D1; theo chữ cũ là 81,5. Agent nhận ra công trình. |
