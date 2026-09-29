# Chạy thử ba tình huống thường gặp, và đọc hồ sơ thật

Ghi chép lúc rà i:explore ngày 2026-09-29, trên bản 1.5.0 của plugin. Số dòng tính theo file lúc đó. Đây là những gì đã thấy, không phải quyết định. Quyết định cuối cùng và các mục đã sửa nằm trong commit nâng i:explore lên bản 1.6.0.

Agent chạy thử skill qua ba tình huống. Tình huống một là người mới hỏi chuyện mua đất nền ngoại ô để xây nhà. Tình huống hai là bàn chuyện self-host Postgres trong một repo, rồi chuyển sang làm. Tình huống ba là hôm sau quay lại chuyện đất nền. Agent cũng đọc hồ sơ thật `~/explore-thu/docs/research/giac-ngu-met-buoi-sang/explore.md` và hai lượt chạy thử cũ trong `~/ambient-review/explore-ab-2026-09-24/blind4/`. Hai lượt cũ chạy trước commit 14eaeee, nhưng câu chữ phần chat không đổi từ đó.

Điểm: lời dặn rõ và có lý do 7, định dạng đầu ra 6, kín trong lượt thường 5, không thừa không thiếu 6, luồng với người 7, dễ đọc với người 6.

Năm lỗ gây sai trong lượt thường:

1. **Hôm sau không tìm lại được hồ sơ đã chốt.** dossier.md:19 chỉ tìm hồ sơ "active". Người dùng nói "đủ rồi, chốt lại" thì hồ sơ đổi sang `ready`. Hôm sau họ quay lại, model không nhận file cũ và tạo hồ sơ thứ hai cùng chủ đề.
2. **Kết luận không có chỗ.** dossier.md:156 trỏ tới "what may be relied on" như thể có một mục riêng, nhưng mục đó đã bị bỏ ở commit 14eaeee. Kết luận nằm rải trong phần dạy, người đọc phải đọc hết mới thấy. Hồ sơ giấc ngủ có mục "Kết luận đến lúc này" là do model tự thêm, skill không yêu cầu.
3. **Tầng cuối có thể mất.** dossier.md:41 nói dạy xong một tầng chưa phải lúc ghi hồ sơ. Người dùng đọc xong tầng cuối rồi tắt máy thì tầng đó không được lưu. Hôm sau model gợi ý lại đúng phần đã dạy.
4. **Hỏi câu sổ sách giữa lúc dạy.** Ngoài repo git, dossier.md:11 bắt hỏi "bạn để hồ sơ khám phá ở đâu". Chuyện đời sống thường rơi vào trường hợp này.
5. **Không biết chỉ đường sang bước làm.** i:flow và i:lite chỉ người dùng gọi được, model không tự mở được. i:explore chỉ nhắc i:flow trong description, không nhắc i:lite. Khi người dùng muốn bắt tay làm, model hoặc thử gọi i:flow rồi bị từ chối, hoặc chỉ gợi ý bản nặng.

Chữ riêng của skill lọt ra chat và ra giấy. SKILL.md:40 bảo "State the seat…", nên lượt chạy cũ in ra "Mình sẽ ngồi ở vị trí người tư vấn…". Những chữ khác cũng lọt ra: "Bản đồ các vùng", "vùng A", "Tầng 1", "Đã giao", "chặn nhiều kết luận nhất", và mục "Những gì đã thay đổi… Chưa có.". Lượt đầu còn liệt kê các vùng hai lần: một lần trong bản đồ (phần 2 của tầng), một lần trong "ta đang ở đâu" (phần 3). Phần đầu hồ sơ giấc ngủ đọc tốt, nhưng agent cho rằng nhờ luật viết tài liệu chung của chủ plugin (`~/.claude/rules/docs.md`) chứ không nhờ skill.

Chỗ thừa trùng với agent chấm cấu trúc: các bước cập nhật hồ sơ lặp phần "Quality test"; luật "nói hồ sơ ở đâu" viết hai lần; "correction signals" ở hai mục; `status` ở cả frontmatter lẫn khối trạng thái; "prefer official or primary sources" lặp luật bậc nguồn; câu hỏi bị lờ thì "goes into the map" trong khi bản đồ chỉ giữ trạng thái vùng.

Tình huống hiếm, mặc định loại: luật đổi tên slug; "a material correction to the dossier itself"; "hand the chair to a specialist"; hỏi nhiều câu liên tiếp trước tầng đầu; nhắc lại vai và "done" khi tiếp tục; người cài plugin mà không có `~/.claude/rules/docs.md`.
