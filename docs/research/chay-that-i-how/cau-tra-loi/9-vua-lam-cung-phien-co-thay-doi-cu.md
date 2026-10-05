# Ca 9: hỏi "vừa làm gì" ngay trong phiên Claude vừa sửa code, trên cây có sẵn thay đổi cũ

- **Câu hỏi gõ vào:** `/i:how vừa làm gì vậy?`
- **Tình trạng repo lúc hỏi:** bản sao sạch ở commit 854968e; trước đó thêm tay một dòng ghi chú vào README.md (thay đổi cũ), rồi trong cùng phiên Claude được nhờ đổi giới hạn cắt dòng của hook từ 200 xuống 160 ký tự
- **Bản i:how được nạp:** bản commit 8601457, giống bản hiện tại

Phần dưới là nguyên văn câu trả lời cuối của lần chạy, không sửa chữ nào. Đường dẫn trong `/tmp` mà câu trả lời nhắc tới đã bị xóa sau lần chạy.

---

**Thay đổi chưa commit: một dòng trong `hooks/iflow-resume.sh`, cộng một ghi chú trong `README.md`.**

Hook nhắc việc dở của i:flow giờ cắt mỗi dòng nó in ra ở 160 ký tự, thay vì 200 như trước. Hook này là script Claude Code tự chạy mỗi lần mở phiên. Nó đọc những hồ sơ i:flow còn dở trong repo rồi in vài dòng nhắc bạn đang làm tới đâu.

Bên `README.md` có thêm dòng "Ghi chú tạm: nhớ viết thêm mục FAQ cho README." Dòng này đã có trước khi tôi bắt đầu, là ghi chú của bạn, nên tôi không giảng thêm.

### Ví dụ

Lan mở lại Claude Code trong một repo có hồ sơ i:flow làm dở. Hồ sơ là file `docs/shape/<tên>/shape.md`, nơi i:flow ghi tiến độ. Trong hồ sơ có dòng `Next action:` ghi bước kế tiếp, và dòng này dài 208 ký tự:

> Next action: viết plan cho slice 03, thêm bước gửi email xác nhận khi Lan bấm Đăng ký, kiểm lại link hết hạn sau 24 giờ, rồi chạy lại toàn bộ test của luồng đăng ký trước khi đánh dấu slice là done trong bảng

Tôi lấy hàm cắt dòng ra từ hai bản: bản đã commit và bản đang sửa. Rồi tôi chạy cả hai trên đúng dòng này (đã chạy). Đây là phần cuối của dòng mà Lan thấy:

```
bản cũ (200):  …trước khi đánh dấu slice là done tr …[truncated]
bản mới (160): …rồi chạy lại toàn bộ test của luồng đăn …[truncated]
```

Với bản mới, Lan mất thêm khoảng nửa câu cuối.

### Từng bước khi hook chạy

1. **Claude Code gọi hook lúc mở phiên.** `hooks/hooks.json` gắn hook vào sự kiện `SessionStart`. Sự kiện này xảy ra khi mở phiên mới, chạy tiếp phiên cũ, gõ `/clear`, nén hội thoại hoặc fork (đọc từ code). Hook tìm `docs/shape/*/shape.md` ở gốc repo git. Nó chỉ nhận những file có dấu `<!-- generated-by: iflow/2 -->`.

2. **Hook chọn dòng để in.** Hàm `pointers` (`hooks/iflow-resume.sh:38`) lấy hai dòng `Current slice:` và `Next action:` trong hồ sơ. Hook còn chạy checker, tức script `skills/flow/scripts/check-dossier.sh`, để kiểm hồ sơ có đúng mẫu không. Khi checker báo hồ sơ hỏng, hook in thêm lời báo của checker, có dấu ⚠ ở đầu (`:76`). Cả hai loại dòng đều đi qua cùng một hàm cắt (đọc từ code).

3. **Hàm `capped` cắt dòng dài. Lần này chỉ đổi chỗ này.** Nó nằm ở `hooks/iflow-resume.sh:32`. Dòng nào dài hơn 160 ký tự thì hàm giữ 160 ký tự đầu, rồi gắn thêm ` …[truncated]`. Trước đây con số là 200.
   - Hàm đếm theo ký tự, không đếm theo byte. Chữ "ố" tính là 1 ký tự chứ không phải 3, nên hàm không bao giờ cắt đôi một chữ tiếng Việt (theo chú thích trong file, và test có kiểm điều này).
   - Con số 160 tính luôn cả nhãn `Next action: `, dài 13 ký tự. Nên phần nội dung thật sự hiện ra chỉ còn 147 ký tự (đọc từ code).
   - Hàm cắt để làm gì: theo chú thích trong file, cái gì hook lấy từ file trong repo rồi in ra đều phải có giới hạn. Nhờ vậy, một hồ sơ có dòng dài bất thường không làm ngập màn hình lúc mở phiên.
   - Vì sao là 160: bạn yêu cầu ở lượt trước mà không nói lý do.
   - Vì sao trước là 200: không chỗ nào ghi. Con số này có từ commit đầu tiên `3d96a15`, và commit message không nhắc tới nó. Tôi tìm thêm trong `docs/research/` và trong những file plan ở `~/.claude/plans/` có nhắc tới hook này, cũng không thấy.

4. **Test vẫn qua vì không kiểm con số.** Đoạn `tests/run.sh:306-317` dựng một dòng `Next action:` gồm 300 chữ "ố". Test chỉ kiểm hai điều: dòng in ra có chữ `truncated`, và vẫn là UTF-8 hợp lệ. Lượt trước tôi chạy cả bộ test, kết quả là `36 passed, 0 failed` (đã chạy). Lời chú thích ở dòng 306 vẫn ghi "cut at 200 characters", giờ đã sai. Tôi để nguyên vì bạn dặn chỉ sửa đúng một dòng.

### Những gì chưa nói tới

Tôi chưa giảng phần còn lại của hook. Đó là cách hook xử lý hồ sơ hỏng (nó giấu dòng `Next action`) và cách nó xử lý khi checker không chạy được. Lần này hai chỗ đó không đổi. Cũng chưa có test nào ghim con số 160: đổi thành 100 hay 500 thì test vẫn qua.

Câu hỏi đầu tiên: hồ sơ của Lan có dòng `Next action:` mà phần nội dung dài đúng 150 ký tự. Lần mở phiên tới, Lan sẽ thấy dòng đó ra sao, và vì sao?
