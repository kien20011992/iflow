# Cấu trúc skill và những việc Claude Code tự làm

Ghi chép lúc rà i:explore ngày 2026-09-29, trên bản 1.5.0 của plugin. Số dòng tính theo file lúc đó. Đây là những gì đã thấy, không phải quyết định. Quyết định cuối cùng và các mục đã sửa nằm trong commit nâng i:explore lên bản 1.6.0.

Điểm: mô tả kích hoạt 8, chia file chính và file tham chiếu 6, việc đáng viết script 9, dùng đúng cơ chế sẵn có 6.

Mô tả kích hoạt (description) nói rõ skill làm gì và khi nào dùng. Nó dài 936 ký tự, dưới ngưỡng 1.024 của hướng dẫn chính thức, và bộ eval trong repo (`evals/explore.json`) đạt 10/10 cả chiều nên kích hoạt lẫn chiều không nên. Câu mẫu "tôi đang nghĩ đến việc …" hơi rộng, nhưng eval chưa bắt được lần kích hoạt nhầm nào.

SKILL.md nặng khoảng 2.000 token (ước từ 8.101 byte), dưới ngưỡng 5.000 nên Claude Code gắn lại nguyên văn sau khi nén hội thoại. Còn `dossier.md` thì không được gắn lại.

Những gì agent tìm thấy, chia theo loại:

- **Hai chỗ tự mâu thuẫn.** SKILL.md:81-83 bảo vị trí cuối mỗi tầng "read from" bản đồ trong hồ sơ, nhưng ở tầng đầu hồ sơ chưa có. dossier.md:41 lại nói thêm một vùng vào bản đồ chưa phải lúc ghi hồ sơ. Chỗ thứ hai: dossier.md:107 bảo mỗi thông tin chỉ nằm một mục, trong khi "correction signals" được ghi ở cả hai mục (dòng 123-127 và 164-167).
- **Luật kiểm con số nằm sai file.** Luật "con số mang kết luận phải khớp nguyên văn nguồn gốc, hoặc có hai nguồn độc lập" chỉ nằm trong `dossier.md`. Mà model chỉ đọc file đó từ lần ghi hồ sơ đầu tiên, nên tầng đầu, thường nhiều số nhất, có thể đưa số chưa kiểm như sự thật.
- **Tả lại việc model tự làm.** Gồm năm câu: đọc hồ sơ trước khi sửa (dossier.md bước 1), dùng lại đường dẫn người dùng đưa (dossier.md:17-18), xem repo trước (SKILL.md:59), điều kiện tách agent (SKILL.md:62-64), và các bước 3, 5, 6, 7 của quy trình cập nhật, vốn lặp lại phần "Quality test".
- **Lặp.** Luật "nói hồ sơ ở đâu" có ở cả SKILL.md:143 lẫn dossier.md:47. Ba câu về hỏi ý kiến (SKILL.md:102, 105-106, 117-118) nhắc lại dòng 92-93. Hai câu "đừng chép lại thân bài" (dossier.md:156, 172) nhắc lại dòng 107. Câu "tài liệu hạ nguồn phải giữ cờ" (dossier.md:100) trùng việc flow và lite đã tự làm.
- **Trường không ai đọc.** `skill:` và `primary_domain:` trong frontmatter của hồ sơ: không hook, script hay skill nào đọc hai trường này (đã grep).
- **Hai điểm dễ gây sai mà agent gắn cờ.** Thứ nhất, skill không nói gì khi plan mode đang bật: lúc đó ghi file bị chặn. Thứ hai, hồ sơ luôn nằm ở `docs/research/` của repo git hiện tại, kể cả khi chủ đề là sức khỏe của bố mà phiên lại mở trong repo công việc.

Tình huống hiếm, mặc định loại: dossier.md dài 192 dòng mà không có mục lục; điều kiện đổi tên slug "materially misleading". Agent này xếp việc tiếp tục một hồ sơ đã `ready` vào tình huống hiếm, nhưng hai agent kia coi đó là lượt thường, và lần sửa này đã nhận nó.

Nguồn: code.claude.com/docs/en/skills và /permission-modes (chính thức); platform.claude.com agent-skills best-practices (chính thức); hai ghi chép cũ trong `docs/research/` (thứ cấp, nội bộ).
