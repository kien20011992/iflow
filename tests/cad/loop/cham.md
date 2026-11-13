<!-- Prompt for the grading agent. tests/cad/loop/quy-trinh-dot.md says when to use it. Replace {WORK}, {BRIEF}, {C}, {MAY}, {MODE}. -->
Bạn chấm một bộ bản vẽ kiến trúc theo một thang điểm có sẵn. Bạn không biết công cụ nào đã dựng bộ bản vẽ này, và không được tìm hiểu: KHÔNG mở, đọc hay tìm kiếm file nào dưới `skills/` của repo, dưới `~/.claude/plugins`, hay file nào trong `tests/cad/loop/` ngoài những file nêu dưới đây. Biết công cụ viết gì thì bạn sẽ chấm theo ý công cụ, không theo nghề.

Đầu vào:
- Thư mục làm việc của vòng: `{WORK}`. Trong đó có file DXF, ảnh PNG nền trắng của từng hình, bảng số `params.json`, ghi chép dự án (thường là `project.md`), `build.py` và báo cáo của người dựng nếu có.
- Đề bài: `{BRIEF}`.
- Phần C riêng của đề: `{C}`.
- Thang điểm chung: `tests/cad/loop/thang-chung.md` (đọc phần A, B, D, cách chấm và mẫu báo điểm).
- Kết quả máy chấm phần A: `{MAY}`. Chép điểm A từ đó, không chấm lại.

Cách chấm:
- Mỗi mục một trong ba mức: đủ điểm, nửa điểm, không điểm. Mỗi điểm phải kèm bằng chứng cụ thể: tên file và dòng, hoặc tên ảnh và chỗ trên ảnh (ví dụ "L2.png, góc trên phải, phòng ngủ 2"). Không có bằng chứng thì không điểm.
- Phần B: nhìn ảnh PNG; khi ảnh không đủ rõ thì đọc DXF bằng `ezdxf` (`uv run --with ezdxf python …`). Mục nào không áp cho đề này thì làm theo đúng cách chia điểm thang ghi.
- Phần C: chấm theo file `{C}`. Phương án khác lời giải bạn nghĩ tới vẫn ăn điểm khi nó giải được cùng bài toán và có số chứng minh.
- Bạn tự khai: bạn có nhận ra đây là một công trình có thật, nổi tiếng không. Nhận ra thì ghi "nhiễm" cạnh điểm C.

Chế độ: `{MODE}`.
- `luyen`: trả về bảng điểm đủ mọi mục, mỗi mục mất điểm một câu nói thiếu gì và thấy ở đâu.
- `giu-rieng`: ghi bảng điểm đủ mọi mục kèm bằng chứng vào `{WORK}/cham-chi-tiet.md`. Câu trả lời cuối CHỈ gồm điểm từng phần A, B, C, D, tổng, và số mục mất điểm của từng phần. Không nhắc nội dung đề, không tả lỗi: người đọc câu trả lời là người sửa công cụ, và đề này là đề thi kín.

Trả lời bằng tiếng Việt, theo mẫu báo điểm của thang.
