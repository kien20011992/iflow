<!-- Prompt for one round of the drawing loop. tests/cad/loop/README.md says how to use it. -->
Bạn đóng vai một phiên Claude Code đang dùng skill `i:cad` để dựng một bản vẽ thật bằng CADCraft. Mục đích: xem lời hướng dẫn của skill có đủ để ra một file DXF tốt không. Làm ĐÚNG theo skill; chỗ nào skill không nói mà bạn phải tự nghĩ ra thì ghi lại.

Skill: `{SKILL}` (`${CLAUDE_SKILL_DIR}`). Đọc `SKILL.md`, rồi các file tham chiếu mà nó bảo đọc cho sản phẩm 5, 6, 7. KHÔNG sửa file nào của skill, không đọc file nào khác trong repo plugin. CADCraft đã cài: lệnh `cadcraft-cli`. `uv` có sẵn để chạy `scripts/dxf_check.py`.

Thư mục làm việc (ngoài git): `{WORK}`. Tạo nó và chỉ ghi trong đó.

Đề bài của kiến trúc sư. Coi như mọi lựa chọn đã được trả lời và bảng số đã được duyệt: đi thẳng tới sản phẩm 5, 6, 7 và dừng trước lần duyệt thứ ba.

{BRIEF}

Giới hạn khoảng 40 phút. Hết giờ mà chưa xong thì dừng ở mức đã có một file DXF chứa tối thiểu trục, tường, cột, cửa, thang, tên phòng kèm diện tích và ba hàng kích thước cho tầng đầu, rồi báo phần chưa làm.

Trả về, tiếng Việt, tối đa 70 dòng:
1. Đường dẫn đầy đủ của file DXF cuối, ảnh PNG nền trắng của từng tầng, `params.json`, `build.py`, `check.py`.
2. Output thật của `dxf_check.py`, của `check.py` và của trình kiểm lỗi CADCraft.
3. Bạn thấy gì khi tự nhìn ảnh: lỗi nhìn thấy, kể cả lỗi chưa sửa.
4. Những chỗ skill thiếu, sai hoặc buộc bạn phải đoán: file và mục nào, bạn đã làm gì, đề nghị sửa một câu. Xếp theo mức nặng. Đây là phần quan trọng nhất.
5. Lệnh hay tham số CADCraft nào chạy khác với điều `cadcraft.md` ghi.
