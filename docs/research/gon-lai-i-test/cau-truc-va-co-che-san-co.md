# Cấu trúc của i:test và những gì Claude Code đã làm sẵn

Ghi chép lúc rà i:test ngày 2026-10-01, trên bản 1.8.0 của plugin. Số dòng tính theo `skills/test/SKILL.md` lúc đó. Đây là những gì đã thấy, không phải quyết định. Các mục đã sửa nằm trong commit nâng plugin lên bản 1.9.0.

Kết luận ngắn: cấu trúc của i:test đã đạt chuẩn. Phần đầu file hợp lệ và trường nào cũng có tác dụng. Để cả skill trong một file là đúng. Không có việc nào đáng viết thành script. Chỗ cắt được chỉ là ba câu tả lại việc Claude Code tự làm.

| Tiêu chí | Điểm |
|---|---|
| Description và cách kích hoạt | 8 |
| Chia file theo tầng | 9 |
| Việc lặp giao cho script | 9 |
| Dùng đúng cơ chế sẵn có của Claude Code | 8 |

Điểm 8 và 9 nghĩa là có lỗi nhỏ nhưng không làm lần chạy thường đi sai.

## Claude Code làm gì với một skill chạy dạng fork

Các điều dưới đây kiểm theo tài liệu chính thức (code.claude.com/docs/en/skills và code.claude.com/docs/en/sub-agents). Độ tin cao.

- `context: fork` không chép hội thoại sang. Claude Code dựng một subagent mới, mặc định loại `general-purpose`, không có lịch sử hội thoại. Subagent nhận nội dung SKILL.md làm lời dặn, có nạp `CLAUDE.md` và ảnh chụp `git status`.
- Mọi subagent đều không có `AskUserQuestion`, `EnterPlanMode` và `ExitPlanMode`. Vì vậy luật của i:test "hỏi lại là kết thúc lượt chạy, nên phải trả lại lệnh `/i:test …` để chạy tiếp" là đúng.
- `background` là trường có thật, chỉ có tác dụng khi đi cùng `context: fork`. Mặc định của nó là `true`, tức lượt gọi không chờ kết quả. `false` bắt lượt gọi chờ, và i:flow cần chờ để ghi kết quả vào phần việc. Vì vậy dòng `background: false` không thừa. Trường này cần Claude Code 2.1.218 trở lên; bản cũ hơn luôn chờ, kết quả như nhau.
- `$ARGUMENTS` được thay bằng phần bên gọi truyền vào.
- Subagent chạy tiền cảnh chuyển yêu cầu cấp quyền thẳng cho người dùng.

## Description

Description dài 897 ký tự, dưới trần 1.024 ký tự của hướng dẫn viết skill và trần 1.536 ký tự của danh sách skill. Câu đầu nói skill làm gì, phần sau nói khi nào dùng, kèm bảy câu mẫu tiếng Việt. Câu "Prefer it over testing-strategy whenever tests are to be written" là cần, vì description của `engineering:testing-strategy` có đúng cụm "write tests for". Câu cuối dặn bên gọi truyền phạm vi, ý định và mọi tiêu chí. Phải giữ câu này, vì context tách biệt không thấy hội thoại.

Lỗi nhỏ: chữ "fresh" xuất hiện hai lần; câu "Use it whenever" không viết ở ngôi thứ ba như hướng dẫn khuyên. Chưa đủ lý do để sửa, vì `evals/test.json` chưa từng lưu kết quả đo kích hoạt. Đổi description khi chưa có số đo thì có thể làm skill ít được mở hơn mà không ai biết.

## Một file hay chia nhiều file

File có 178 dòng, dưới mức 500 dòng mà hướng dẫn đặt ra. Với skill chạy dạng fork, SKILL.md là toàn bộ lời dặn của subagent. Tách một phần sang file tham chiếu chỉ thêm một lần đọc mà subagent có thể bỏ qua. Để một file là đúng.

## Câu tả lại việc Claude Code tự làm

- Dòng 27, "this run starts in its own context": fork tự dựng context riêng.
- Dòng 38–39, "this context cannot wait for an answer": subagent không có công cụ hỏi người dùng.
- Dòng 125–126, "through normal permission": hệ thống xin quyền tự lo.
- Dòng 164–165, "The runner's output is the evidence, the native test name is the identity, git is the history": câu giải thích lại lệnh cấm ngay trước nó.

## Câu phải giữ

Những câu sau chặn thói quen xấu khi viết test, đó là lý do i:test tồn tại. Không câu nào là việc Claude Code tự làm.

- Kết quả mong đợi lấy từ hợp đồng, không bao giờ từ code hay từ hành vi hiện tại.
- Diff chỉ nói chỗ cần nhìn, không nói cái gì đúng.
- Thứ tự căn cứ cho kết quả đúng, và danh sách những thứ không bao giờ là căn cứ.
- Không mặc định mọi đầu vào sai đều phải ném lỗi có kiểu.
- Mỗi rủi ro tìm được phải quy về một kết quả mong đợi đã ghi.
- Không chép một câu kiểm qua nhiều tầng test.
- Không xâu chuỗi các test phụ thuộc nhau.
- Mock ranh giới bên ngoài, không mock thứ đang được test.
- Câu kiểm cũ trái hợp đồng là một phát hiện, không phải thứ để sửa.
- Lỗi của sản phẩm thì giữ nguyên câu kiểm.
- Không đánh dấu expected-failure để bộ test xanh.
