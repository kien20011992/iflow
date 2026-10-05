# Ca 3: cố ý trả lời sai câu hỏi cuối của ca 2

- **Câu hỏi gõ vào:** `Có, nó viết test E2E cho luồng tải đơn hàng, và nếu test hỏng thì nó dọn dữ liệu nhờ luật đó.`
- **Tình trạng repo lúc hỏi:** chạy tiếp đúng phiên của ca 2
- **Bản i:how được nạp:** bản viết đầu tiên, trước sáu chỗ sửa

Phần dưới là nguyên văn câu trả lời cuối của lần chạy, không sửa chữ nào. Đường dẫn trong `/tmp` mà câu trả lời nhắc tới đã bị xóa sau lần chạy.

---

**Commit `854968e`, phần 4: chế độ "chỉ cho biết còn thiếu test nào".**

Phần đúng: bạn hiểu đúng luật ở `:114`. Một test E2E hỏng giữa chừng vẫn phải dọn dữ liệu nó đã tạo.

Phần sai: lượt đó i:test không viết test E2E nào. Bạn đã đọc lệnh như một lời nhờ viết test, nhưng lệnh có cụm "chỉ cho biết còn thiếu test nào". Cụm này bật chế độ "Only what is missing" (`:107-110`). Ở chế độ này i:test không viết test nào và cũng không chạy test nào. Chữ "e2e" trong lệnh chỉ cho biết loại test cần xét. Nó không biến lượt đó thành lượt viết test. Không có test nào chạy thì luật dọn dẹp ở `:114` không bao giờ được dùng tới.

Tên chế độ dễ gây hiểu nhầm. "Only what is missing" nghe như "chỉ viết phần còn thiếu", nhưng thật ra nó nghĩa là "chỉ liệt kê phần còn thiếu". Plan rà soát cũng lo đúng chỗ này. Mục T2 của plan đề xuất viết lại câu đó "cho khỏi khớp nhầm lời xin viết test".

Giải thích lại bằng ví dụ khác. Bạn nhờ thợ "xem giúp xe còn thiếu đồ bảo dưỡng nào". Thợ đưa lại tờ giấy ghi "thiếu lọc gió, má phanh mòn". Thợ không thay gì và cũng không chạy thử xe. Câu dặn "thay hỏng thì nhớ lau dầu tràn" không dùng tới, vì chẳng ai thay gì cả.

Áp vào code (đọc từ code). Minh gõ `/i:test e2e luồng đăng ký · chỉ cho biết còn thiếu test nào`. i:test làm ba bước:

1. Viết ra các kỳ vọng của luồng đăng ký. Ví dụ: "email trùng thì báo lỗi", "đăng ký xong thì nhận email xác nhận".
2. Đối chiếu từng kỳ vọng với các test có sẵn. Luật ở `:136-140` chỉ tính một test cũ là "đã kiểm đủ" khi lệnh test thường ngày bắt test đó phải pass, và test đó kiểm đúng kỳ vọng ấy: cùng chỗ gọi, cùng điều kiện, cùng kết quả.
3. Dừng lại. Không tạo file test mới, không chạy lệnh test nào. Bản báo cáo là toàn bộ kết quả. Kỳ vọng nào chưa có test thì vào mục "Not covered", kèm loại test cần viết để kiểm nó (`:179-181`). Ví dụ: "đăng ký xong nhận email xác nhận: chưa có test, cần một test E2E qua form đăng ký". Chữ "e2e" trong lệnh chỉ xuất hiện ở lời gợi ý này, không thành file test nào.

Phần "không viết" đã có từ trước commit này. Commit chỉ chốt thêm phần "không chạy".

Câu hỏi mới. Minh gõ hai lệnh chỉ khác nhau một cụm:

- (a) `/i:test luồng đăng ký · chỉ cho biết còn thiếu test nào`
- (b) `/i:test luồng đăng ký`

Repo đã có test `rejects duplicate email`, và test này kiểm đủ kỳ vọng "email trùng thì báo lỗi". Với mỗi lệnh, i:test có chạy test `rejects duplicate email` không, và vì sao?
