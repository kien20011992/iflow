# Ca 8: hỏi về một dòng code

- **Câu hỏi gõ vào:** `/i:how dòng 32 của hooks/iflow-resume.sh làm gì vậy?`
- **Tình trạng repo lúc hỏi:** bản sao sạch ở commit 854968e
- **Bản i:how được nạp:** bản commit 8601457, giống bản hiện tại

Phần dưới là nguyên văn câu trả lời cuối của lần chạy, không sửa chữ nào. Đường dẫn trong `/tmp` mà câu trả lời nhắc tới đã bị xóa sau lần chạy.

---

**Dòng 32 của `hooks/iflow-resume.sh`**, nằm trong hàm `capped` (dòng 29–35).

Dòng này cắt bớt mọi dòng dài quá 200 ký tự trước khi hook in ra, rồi gắn thêm đuôi ` …[truncated]` để người đọc biết dòng đã bị cắt. Hook này chạy mỗi khi mở phiên Claude Code. Những gì nó in ra được đưa vào đầu context của Claude.

**Ví dụ.** Lan đang làm dở một việc bằng i:flow. File `docs/shape/dang-ky/shape.md` có dòng `Next action:` dài 300 ký tự, vì Lan lỡ dán cả một đoạn log vào. Lan mở phiên mới. Hook không in đủ 300 ký tự mà chỉ in 200 ký tự đầu, kèm ` …[truncated]`.

## Đường đi của dòng đó trong hook

1. **Dòng được đưa vào `capped`.** Hàm này đọc từng dòng một. Có hai chỗ gọi nó. Một là `pointers()` ở dòng 39: hàm này lấy hai dòng `Current slice:` và `Next action:` trong shape.md. Hai là dòng 76: chỗ này đưa vào lời báo lỗi của `check-dossier.sh`, script kiểm tra hồ sơ i:flow có hợp lệ không. Dòng `Next action:` của Lan đi vào qua chỗ thứ nhất.

2. **Dòng 31 bỏ qua dòng rỗng.**

3. **Dòng 32 cắt.** `${#line}` là độ dài của dòng. `${line:0:200}` lấy 200 ký tự đầu. Cần để ý một chỗ: con số 200 tính trên cả dòng, gồm luôn nhãn `Next action: ` dài 13 ký tự, vì grep trả về nguyên dòng.
   *Đã chạy:* tôi chép hàm `capped` ra rồi đưa vào dòng `Next action:` theo sau là 300 chữ "ố". Dòng in ra dài đúng 217 ký tự: 4 dấu cách thụt đầu dòng, 200 ký tự giữ lại, và 13 ký tự của ` …[truncated]`. Dòng kết thúc bằng `ốốốốốốốố …[truncated]`. Thử với câu ngắn `Next action: viết test cho form đăng ký` thì câu đi qua nguyên vẹn.

4. **Dòng 33 in ra, thêm phần thụt đầu dòng.** Phần thụt do chỗ gọi truyền vào. Dòng 39 truyền 4 dấu cách, dòng 76 truyền `    ⚠ `.

## Vì sao cần cắt

*Theo chú thích ở dòng 25–27 của chính file:* hook không được in ra thứ gì dài vô hạn lấy từ file trong repo. Cả dòng trạng thái lẫn lời báo của checker đều trích lại nội dung người ta viết vào hồ sơ.

*Tôi suy ra từ code:* lý do giới hạn quan trọng là hook chạy ở mọi lần mở phiên, chạy tiếp phiên cũ, `/clear` và nén hội thoại (dòng 2). Một dòng dài bất thường vì thế sẽ chiếm chỗ trong context của Claude ở mọi phiên. Dòng 70 cũng nói rõ phần thụt đầu dòng là "trích nguyên văn từ file trong repo", tức là nội dung hook không kiểm soát được.

Vì sao chọn đúng 200 thì không có ghi chép nào. Commit `3d96a15` thêm dòng này cùng lúc với cả plugin, và commit message không giải thích.

## Ký tự hay byte

Chú thích ở dòng 27–28 có lưu ý thêm. `${#line}` và `${line:0:N}` chỉ đếm theo ký tự khi locale là UTF-8. Locale là thiết lập ngôn ngữ của máy, bash dựa vào nó để biết một chữ chiếm mấy byte. Chữ "ố" chiếm 3 byte.

- *Đã chạy với locale UTF-8* (`en_US.UTF-8`, locale của máy này): bash cắt đúng chỗ giữa hai chữ, kết quả vẫn là UTF-8 hợp lệ.
- *Đã chạy cùng dòng đó với `LC_ALL=C`:* bash đếm theo byte, nên chỗ cắt ở byte thứ 200 rơi vào giữa một chữ "ố". Byte cuối cùng trước đuôi là `0xE1`, tức byte đầu của chữ bị cắt dở. `iconv` báo kết quả không còn là UTF-8 hợp lệ.

Vì vậy chú thích mới nói chuyện này "quan trọng với ngôn ngữ của người dùng". Hồ sơ viết tiếng Việt thì gần như dòng nào cũng có chữ nhiều byte. `tests/run.sh:306–317` kiểm đúng chuyện này: test tạo một dòng `Next action` gồm 300 chữ "ố", rồi kiểm dòng in ra có `truncated` và vẫn là UTF-8 hợp lệ.

Các lần chạy thử chỉ ghi file vào `/tmp`. `git status` trước và sau giống nhau, nên repo không bị đổi gì.

## Chưa giảng tới

Tôi chưa nói về cách hook chọn hồ sơ nào để in (dòng 41–68), cũng chưa nói về nhánh xử lý hồ sơ hỏng (dòng 73–76). Nếu muốn xem tiếp, nhánh hồ sơ hỏng là nơi `capped` được dùng lần thứ hai.

---

**Câu hỏi:** Lan sửa lại để phần nội dung sau `Next action: ` dài đúng 195 ký tự. Hook in nguyên dòng hay cắt bớt, và vì sao?
