# Ca 2: hỏi "vừa làm gì" trên bản sao sạch

- **Câu hỏi gõ vào:** `/i:how vừa làm gì vậy?`
- **Tình trạng repo lúc hỏi:** bản sao của repo ở commit 854968e, không có thay đổi nào
- **Bản i:how được nạp:** bản viết đầu tiên, trước sáu chỗ sửa

Phần dưới là nguyên văn câu trả lời cuối của lần chạy, không sửa chữ nào. Đường dẫn trong `/tmp` mà câu trả lời nhắc tới đã bị xóa sau lần chạy.

---

**Commit `854968e`** (14:17 hôm nay, 2 file): commit này dọn lại file hướng dẫn của i:test, skill viết test mới, và nâng phiên bản plugin lên 1.11.1. Nó không thêm việc mới nào cho i:test. Nó chỉ dời một luật về đúng chỗ, bỏ vài câu được cho là nói trùng, và gỡ một chỗ hai luật mâu thuẫn nhau.

File bị sửa là `skills/test/SKILL.md`. File này không phải code chạy được: Claude đọc nó mỗi khi có người gõ `/i:test`, rồi làm theo. Vì vậy mọi nhận định dưới đây đều là **đọc từ diff**, không có gì để chạy thử.

**Lý do lấy từ đâu.** Tôi không thấy plan hay ghi chú nào viết riêng cho commit này. `docs/research/gon-lai-i-test/` và plan `optimized-seeking-bird.md` thuộc lần gọt i:test trước, bản 1.9.0. Nên lý do chính lấy từ commit message. Chỗ nào tôi tự suy ra thì tôi ghi rõ. Lúc 15:04, tức là sau commit này, có một plan rà soát cả plugin: `~/.claude/plans/hashed-discovering-goblet.md`, vẫn là bản nháp. Plan này nhận xét về commit, tôi nêu ở phần 3 và 4.

**Ví dụ dùng xuyên suốt:** Lan có hàm `importOrders()`. Hàm đọc file CSV đơn hàng rồi ghi vào database, gặp lỗi mạng thì thử lại. Lan gõ `/i:test importOrders`.

### 1. Luật "mỗi kịch bản kiểm những gì" dời lên mục Kỳ vọng

Ở `skills/test/SKILL.md:62-65`. Trước khi đọc code, i:test phải viết ra danh sách kỳ vọng. Danh sách gồm: gọi hàm thì nhận lại gì, dữ liệu còn lại thế nào, cái gì không được đổi, gọi lần hai thì ra sao. Trước commit, câu "mỗi kịch bản chỉ giữ những ô áp dụng được" nằm ở mục "What to write", cách danh sách đó cả trang. Giờ câu này nằm ngay sau danh sách.

Áp vào ví dụ của Lan:
- Kịch bản "import file hợp lệ" cần hai ô: hàm trả về gì, và database có thêm những đơn nào.
- Kịch bản "import lại đúng file đó lần hai" cần đủ bốn ô. Ô cuối là lần hai không được tạo đơn trùng.
- Một hàm chỉ đổi chuỗi thành ngày thì chỉ cần ô "trả về gì".

Câu "Never invent a case to fill a slot" vẫn giữ: đừng bịa kịch bản chỉ để có đủ bốn ô.

Lý do theo commit message là "fold the per-scenario effects into the expectations". Ý tôi suy ra: luật về cách viết kỳ vọng nên nằm cạnh chỗ viết kỳ vọng.

Tên mục cũng đổi, từ "before any body is read" thành "before the code under test is read" (`:57`). Commit message không nói lý do. So chữ thì bản mới hẹp hơn: chỉ cấm đọc code đang được test, chứ không cấm mọi thứ có phần thân.

### 2. Bỏ ba câu, commit message gọi là "nói trùng"

Lý do theo commit message là "drop rules that repeat others". Tôi kiểm từng câu:

- **"Never pick a dossier by fuzzy match"** (trước ở `:49`): đừng chọn hồ sơ bằng cách đoán tên gần đúng. Hồ sơ ở đây là thư mục `docs/shape/<tên>/`, nơi i:flow ghi việc lớn đang làm dở. Câu ngay sau đã chỉ rõ đường: lấy hồ sơ người gọi nêu tên, không có thì lấy `docs/shape/*/shape.md`. Đường đã cụ thể như vậy thì không còn gì để đoán. Câu này trùng thật (tôi suy ra).
- **"Called from i:flow, return this same report…"** (cuối file cũ): khi i:flow gọi thì vẫn trả cùng báo cáo, hồ sơ và bước tiếp theo là việc của i:flow. Câu này cũng trùng thật. `:31` đã cấm i:test sửa hồ sơ, còn `skills/flow/SKILL.md:268` đã ghi rằng i:flow tự tóm kết quả và tự quyết bước tiếp theo.
- **"Say so when an explicit scope lands off the active slice"** (trước ở `:55`): khi người dùng chỉ định một phần code nằm ngoài phần việc i:flow đang làm dở, i:test phải nói ra. Tôi tìm trong cả repo và **không thấy chỗ nào khác nói câu này**. Vậy câu này bị bỏ hẳn chứ không phải trùng, khác với lời commit message. Ví dụ: Lan đang làm dở phần "thanh toán" trong i:flow mà gõ `/i:test importOrders`. Bản cũ sẽ báo "phạm vi này nằm ngoài phần việc đang làm". Bản mới thì im lặng.

### 3. Test E2E bớt hai yêu cầu, chỉ giữ việc dọn dẹp khi test hỏng

Ở `:112-117`. Test E2E là test đi từ lớp ngoài cùng, giống người dùng thật bấm nút.

- **Bỏ** "a unique data namespace": mỗi lần chạy dùng một vùng dữ liệu riêng. Ví dụ mọi đơn do test tạo đều có mã bắt đầu bằng `test-run-42-`.
- **Bỏ** "response and observable final state both asserted": lúc nào cũng phải kiểm cả kết quả trả về lẫn dữ liệu còn lại. Phần 1 giờ lo việc này theo từng kịch bản.
- **Giữ** "cleanup that also runs when the test fails": test hỏng giữa chừng vẫn phải dọn. Commit message nhấn riêng ý này: "keep cleanup on failure".

**Chỗ bản ghi và code lệch nhau.** Commit coi vùng dữ liệu riêng là trùng với `:127`, "a unique namespace wherever determinism needs them". Nhưng dòng 28 của plan rà soát ghi: "Commit gần nhất của i:test lỡ bỏ chốt 'vùng dữ liệu riêng' của E2E: test dọn dẹp có thể xoá nhầm dữ liệu của chính người dùng." Lý do là `:127` chỉ đòi vùng riêng khi cần chạy lại ra cùng kết quả, chứ không đòi vì an toàn dữ liệu.

Với Lan: test E2E tải file lên, xong dọn bằng lệnh "xóa mọi đơn tạo hôm nay". Nếu có vùng riêng, test chỉ xóa đơn `test-run-42-*`. Nếu không, test xóa luôn mấy đơn Lan vừa nhập tay vào database dev trên máy.

`:128-129` vẫn cấm dùng "shared dataset", tức dữ liệu dùng chung với người khác. Nên theo tôi suy ra, rủi ro chỉ còn ở dữ liệu riêng của Lan. Plan rà soát đề xuất thêm vào `:127` một câu: test ghi vào nơi lưu dữ liệu thật thì ghi trong vùng riêng, và chỉ dọn những gì nó tạo ra. Đề xuất này chưa được đưa vào file.

### 4. Chế độ "chỉ cho biết còn thiếu test nào" không chạy gì nữa

Ở `:107-110` và `:152`. Đây là chế độ người dùng chỉ hỏi còn thiếu test nào, chứ không nhờ viết test. Mục riêng của chế độ này ghi "write and run nothing" từ trước. Nhưng commit `81368d4` (13:50 hôm nay) thêm vào mục Run một câu: chạy cả những test cũ được tính là đã kiểm đủ. Từ lúc đó hai luật mâu thuẫn nhau: một luật bảo không chạy gì, luật kia bảo chạy test cũ.

Commit này thêm "Outside Only what is missing" vào đầu mục Run, nghĩa là luật chạy test không áp cho chế độ này. Lý do theo commit message là "run nothing in only-what-is-missing".

Plan rà soát (mục T2) muốn làm cách khác: viết lại đoạn của chế độ này để nó dừng hẳn trước bước chạy, rồi cắt cụm "Outside Only what is missing" vừa thêm. Đề xuất này cũng chưa được đưa vào file.

### 5. Số phiên bản

`.claude-plugin/plugin.json:3` đổi từ 1.11.0 lên 1.11.1, chỉ tăng số cuối. Theo cách đánh số phiên bản thông dụng, số cuối tăng là sửa vặt, không thêm tính năng (tôi suy ra).

### Còn lại

- Không nhận định nào ở trên chạy thử được. Tôi chỉ chạy `skills/flow/scripts/check-pointers.sh skills/test`, script mà CLAUDE.md dặn chạy sau mỗi lần sửa skill. Kết quả: `0 pointers checked in 1 files, all resolve`. File không trỏ sang file nào khác nên script không có gì để soát. Kết quả này không chứng minh các luật đúng. Thư mục làm việc không đổi sau khi chạy.
- Tôi chưa giảng phần i:test mà commit không đụng tới: bước soi rủi ro, cách viết test cho hợp dự án, mẫu báo cáo.
- Nên xem kỹ phần 3 trước, vì đó là chỗ plan rà soát cho rằng commit đã bỏ nhầm.

Câu hỏi để kiểm lại: tuần sau có người gõ `/i:test e2e luồng tải đơn hàng · chỉ cho biết còn thiếu test nào`. Theo bản mới, i:test có viết test E2E nào không? Và luật "test hỏng vẫn phải dọn" ở `:114` có tác dụng gì trong lượt đó?
