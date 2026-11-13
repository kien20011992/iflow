# Duyệt một vòng của vòng lặp vẽ

Người duyệt là phiên chính, không phải agent đã vẽ. Đọc báo cáo của agent, rồi tự làm bốn việc dưới đây trên chính file của vòng đó.

1. Chạy lại `skills/cad/scripts/dxf_check.py` trên file DXF cuối. Đừng chép kết quả từ báo cáo.
2. Mở ảnh PNG nền trắng của từng tầng và soát theo danh sách "Một hình mặt bằng phải có gì" trong `skills/cad/references/ve.md`: mục nào có, mục nào thiếu, mục nào sai.
3. So cách vẽ với bản vẽ mẫu của văn phòng, nếu có: nét, nhãn, ký hiệu, cách ghi kích thước. Chỉ so cách vẽ, không so con số của một ca có đáp án.
4. Xếp mỗi chỗ hỏng vào đúng một loại rồi mới sửa:
   - skill thiếu hoặc sai luật → sửa file của skill;
   - trình kiểm báo sai hoặc bỏ sót → sửa `dxf_check.py` và thêm một bản vẽ có lỗi cài sẵn vào bài tự thử;
   - CADCraft làm khác tài liệu → sửa `cadcraft.md`, kèm nhãn phiên bản;
   - agent làm kém mà skill đã nói rõ → không sửa gì, ghi lại.

Sau khi sửa: chạy `tests/cad.sh`, ghi một dòng vào `rounds.md` (vòng mấy, file nào, sửa gì, còn gì), rồi chạy vòng sau với cùng đề bài. Dừng khi một vòng không còn chỗ hỏng loại một, hai hoặc ba nào, hoặc khi hai vòng liền không giảm được số chỗ hỏng.
