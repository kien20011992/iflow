<!-- Prompt for one round of the drawing loop. tests/cad/loop/README.md says how to use it. Replace {SKILL}, {WORK}, {BRIEF}, {MODE} and {RETURN} with the text of one choice below. -->
Bạn đóng vai một phiên Claude Code đang dùng skill `i:cad` để dựng một bản vẽ thật bằng CADCraft. Mục đích: xem lời hướng dẫn của skill có đủ để ra một file DXF tốt không. Làm ĐÚNG theo skill; chỗ nào skill không nói mà bạn phải tự nghĩ ra thì ghi lại.

Skill: `{SKILL}` (`${CLAUDE_SKILL_DIR}`). Đọc `SKILL.md`, rồi các file tham chiếu mà nó bảo đọc cho các sản phẩm trong phạm vi dưới đây. KHÔNG sửa file nào của skill, không đọc file nào khác trong repo plugin. CADCraft đã cài: lệnh `cadcraft-cli`. `uv` có sẵn để chạy các trình kiểm trong `scripts/`.

Thư mục làm việc (ngoài git): `{WORK}`. Tạo nó và chỉ ghi trong đó.

Phạm vi của lượt này: {MODE}

<!-- Hai chế độ, chép đúng một câu vào {MODE}:
ve: Coi như mọi lựa chọn đã được trả lời và bảng số đã được duyệt: đi thẳng tới sản phẩm 5, 6, 7 và dừng trước lần duyệt thứ ba.
du: Đi đủ bảy sản phẩm. Mọi điều chủ nhà hay chủ đầu tư trả lời được thì coi như đề đã trả lời; điều đề không nói thì chọn một giả định, ghi rõ là giả định, rồi đi tiếp thay vì hỏi. Mỗi lần duyệt coi như người dùng chọn phương án bạn đề nghị. Dừng trước lần duyệt cuối, kèm danh sách việc còn lại cho người dùng.

Hai cách trả lời, chép đúng một câu vào {RETURN}:
luyen: bằng chính nội dung báo cáo đó.
giu-rieng: đúng một dòng, "xong" hay "hết giờ", kèm đường dẫn `{WORK}`; không nhắc nội dung đề, bản vẽ hay lỗi, vì người đọc câu trả lời là người sửa skill và đề này là đề thi kín.
-->

Đề bài:

{BRIEF}

Lần chạy `build.py` cuối cùng ghi cả output vào `{WORK}/build.log` (ví dụ `python3 build.py … 2>&1 | tee build.log`): danh sách "Chưa vẽ" ở cuối output là thứ được đếm. Giữ trong `{WORK}` file DXF cuối, ảnh PNG nền trắng của từng hình, `params.json`, `build.py` và ghi chép dự án.

Giới hạn khoảng 40 phút. Hết giờ mà chưa xong thì dừng ở mức đã có một file DXF chứa tối thiểu trục, tường, cột, cửa, thang, tên phòng kèm diện tích và ba hàng kích thước cho tầng đầu, rồi báo phần chưa làm.

Viết báo cáo dưới đây vào `{WORK}/bao-cao.md`, tiếng Việt, tối đa 70 dòng, rồi trả lời {RETURN}
1. Đường dẫn đầy đủ của file DXF cuối, ảnh PNG nền trắng của từng hình, `params.json`, `build.py`, `build.log`.
2. Output thật của các trình kiểm của skill (`dxf_check.py`, `plan_check.py`, `luat_check.py`) và của trình kiểm lỗi CADCraft.
3. Bạn thấy gì khi tự nhìn ảnh: lỗi nhìn thấy, kể cả lỗi chưa sửa.
4. Những chỗ skill thiếu, sai hoặc buộc bạn phải đoán: file và mục nào, bạn đã làm gì, đề nghị sửa một câu. Xếp theo mức nặng. Đây là phần quan trọng nhất.
5. Lệnh hay tham số CADCraft nào chạy khác với điều `cadcraft.md` ghi.
6. Bạn có nhận ra đề là một công trình có thật, nổi tiếng không. Có thì nói tên.
