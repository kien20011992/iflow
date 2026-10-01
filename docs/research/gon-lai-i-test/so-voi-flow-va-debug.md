# i:test so với i:flow và i:debug

Ghi chép lúc rà i:test ngày 2026-10-01, trên bản 1.8.0 của plugin. Số dòng tính theo `skills/test/SKILL.md` lúc đó. Đây là những gì đã thấy, không phải quyết định. Các mục đã sửa nằm trong commit nâng plugin lên bản 1.9.0.

i:test được sửa lần cuối ở commit `27e8926` (28/9). Sau đó i:flow đổi nhiều lần, còn i:debug không đổi gì. Việc đối chiếu hỏi hai điều. Thứ nhất: i:test có còn đọc đúng hồ sơ mà i:flow ghi ra không. Thứ hai: những luật i:test có chung với flow hay debug có còn đi cùng hướng không. Chỗ giống hệt thì bỏ qua. Chỗ giống mà đi hướng khác thì sửa theo flow, hoặc theo debug với những gì riêng của skill chạy trong context tách biệt.

Điểm: 7. Không chỗ nào làm hỏng lần gọi thẳng `/i:test`. Lần gọi từ i:flow chỉ hỏng khi repo có hai chương trình i:flow cùng đang dở.

## Đã khớp, bỏ qua

- i:test đọc hồ sơ i:flow ở năm chỗ, và cả năm vẫn khớp mẫu hồ sơ hiện tại: dòng `Current slice:` với giá trị `—` nghĩa là không có phần việc nào đang chạy; hàng của phần việc nằm trong khối trạng thái cuối `shape.md`; bức tranh và các quyết định được tìm theo vai trò của mục, không theo tiêu đề; đoạn mở đầu file phần việc là mục tiêu của nó; plan đã duyệt, kết quả và ghi chú không được dùng làm căn cứ cho kết quả đúng.
- "No ledger, no case IDs" khớp i:debug.
- Khi bị chặn, i:test trả lại đúng lệnh `/i:test <…>` để chạy tiếp, cùng cách với `/i:debug <…>`.
- i:test chỉ chạy các test nó viết, còn i:flow tự chạy cả bộ test. Đây là chia việc có chủ ý: flow ghi rõ "chạy bộ test đã có không bao giờ đi qua i:test".
- Test đỏ do i:test viết là lỗi của sản phẩm. Flow đánh dấu bỏ qua bằng marker của runner, còn i:test cấm đánh dấu expected-failure. Hai bên làm hai việc khác nhau, không đá nhau.
- i:test không cần nhánh đọc file plan của i:lite, vì i:lite đã bỏ việc gọi i:test từ commit `eccfde2`.
- Câu "Everything below is a delta from your defaults" của i:debug: thêm vào i:test không sửa lỗi nào, nên không chép.

## Giống mà đi hướng khác

| Chỗ | Bên kia làm gì | i:test đang làm gì |
|---|---|---|
| Hồ sơ nào để đọc | debug đọc "the dossier the caller names" | Tự quét mọi `docs/shape/*/shape.md`, dù flow đã chỉ tên hồ sơ |
| Tìm `docs/shape/` ở đâu | flow tìm từ gốc git (commit `8f1792e`) | Tìm từ thư mục đang đứng |
| Ngôn ngữ của báo cáo | debug: ngôn ngữ người gọi dùng để viết `$ARGUMENTS` | "the user's language", trong khi context tách biệt không thấy người dùng |
| Từ riêng của skill | flow: chỉ dùng trong file skill, ra ngoài thì nói bằng lời thường (commit `446867c`) | Bắt dùng nhãn "Oracle sources", "Verified invariants", "harness", cả chữ "fork" với người dùng |

Hai chỗ khác làm lần gọi từ flow đi sai:

- Câu "no user acceptance criteria were supplied to this fork" in ra ở mọi lần flow gọi. Flow trao hồ sơ chứ không trao tiêu chí riêng, nên người đọc kết quả sau này hiểu nhầm là phần việc không có tiêu chí.
- Câu "Called from i:flow … return those same items" có thể khiến i:test chép lại bức tranh, quyết định và mục tiêu của phần việc về cho flow, trong khi flow không cần chúng.

## Phải giữ

Commit `446867c` của flow đã bỏ khỏi mục "Tests from i:test" hai thứ: danh sách những gì i:test trả về, và luật mỗi test ghi rõ căn cứ của nó. Từ đó i:test là nơi duy nhất giữ hai thứ này. Flow dựa vào lời ghi căn cứ trong mỗi test để xét một test đỏ không ai nhận. Vì vậy câu ở dòng 135–138 không được cắt, chỉ được viết lại cho rõ.

## Việc ngoài i:test

Hồ sơ `docs/shape/got-flow/` vẫn ghi lỗ "i:test chưa có nhánh cho i:lite". Lỗ này đã hết từ commit `eccfde2`. Cần sửa tay hoặc qua i:flow.
