# Ca 6: hỏi lại luồng hook sau khi sửa luật dựng trang

- **Câu hỏi gõ vào:** `/i:how hook nhắc việc dở chạy thế nào?`
- **Tình trạng repo lúc hỏi:** bản sao sạch ở commit 854968e
- **Bản i:how được nạp:** bản đã có sáu chỗ sửa, chưa có dòng về lịch sử phiên

Phần dưới là nguyên văn câu trả lời cuối của lần chạy, không sửa chữ nào. Đường dẫn trong `/tmp` mà câu trả lời nhắc tới đã bị xóa sau lần chạy.

---

Hook `hooks/iflow-resume.sh` (đăng ký trong `hooks/hooks.json`) chạy mỗi khi một phiên Claude Code bắt đầu, kể cả sau `/clear` hay sau khi hội thoại bị nén. Nó tìm trong `docs/shape/` của repo những hồ sơ i:flow còn dở, rồi in cho Claude biết slice nào đang làm và việc tiếp theo là gì. Hồ sơ nào bị hỏng thì nó giấu việc tiếp theo đi và bảo Claude sửa hồ sơ trước. Không có việc dở thì nó không in gì.

Luồng này rẽ nhánh và đi qua năm bên, nên tôi vẽ thành trang HTML:
`/tmp/claude-1000/-home-neki-projects-personal-claude-plugin-iflow/292d60f3-407c-4910-abe3-580a5d19be44/scratchpad/hook-nhac-viec-do.html`

Trang đi theo ví dụ Lan quay lại làm tiếp "Luồng đăng ký" đang dở ở slice 02. Bấm vào từng bước để xem code thật, lý do kèm nguồn của nó, và output thật từ những lần tôi chạy hook trên một repo mẫu dựng trong thư mục tạm.

Có một chỗ tôi chạy thử thì thấy lạ. Khi biến `IFLOW_SKILL_DIR` (biến chỉ cho hook biết skill i:flow nằm ở đâu) trỏ sai, hook vẫn bảo Claude mở `SKILL.md` trong chính thư mục sai đó, mà ở đó không có file. Lúc cài plugin bình thường thì biến này luôn đúng, nên chỉ một bản cài đã hỏng mới gặp chuyện này.

`tests/run.sh` báo 36 passed, 0 failed. Không file nào trong repo bị đổi.

Đọc xong trang thì thử đoán xem. Lan làm xong cả hai slice, rồi tự sửa `shape.md` bằng tay nhưng gõ nhầm `Overall status: Done`, chữ D viết hoa. Sang phiên sau, hook sẽ in ra gì, và Claude sẽ làm gì?

---
Ngoài lề: MCP server `composio` cần cấp quyền thì mới dùng được. Bạn cấp quyền bằng `claude mcp` hoặc `/mcp` trong một phiên tương tác.
