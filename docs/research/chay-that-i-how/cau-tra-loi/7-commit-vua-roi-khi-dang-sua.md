# Ca 7: hỏi "commit vừa rồi" khi repo đang có thay đổi chưa commit

- **Câu hỏi gõ vào:** `/i:how commit vừa rồi xử lý những gì, vì sao?`
- **Tình trạng repo lúc hỏi:** repo plugin trên main, đang có phần i:how chưa commit; commit cuối là 854968e
- **Bản i:how được nạp:** bản đã có sáu chỗ sửa, chưa có dòng về lịch sử phiên

Phần dưới là nguyên văn câu trả lời cuối của lần chạy, không sửa chữ nào. Đường dẫn trong `/tmp` mà câu trả lời nhắc tới đã bị xóa sau lần chạy.

---

Commit `854968e` (hôm nay, 14:17) sửa 2 file: `skills/test/SKILL.md` và `.claude-plugin/plugin.json`.

Commit này gọt i:test, skill viết test mới trong một context riêng chưa từng thấy code. Nó bỏ năm chỗ lặp lại luật đã có, gom một đoạn về chỗ sớm hơn, chặn một chỗ dễ hiểu sai ở chế độ "chỉ xem", rồi nâng bản lên 1.11.1.

Vì sao: lý do ghi trong lịch sử phiên đã làm commit này (khoảng 14:04–14:16). Bạn nhờ một agent Fable soát độc lập xem i:test có bị phức tạp hóa không. Agent đề xuất cắt khoảng 15–20% chữ. Claude chỉ nhận những chỗ cắt mà không đổi kết quả lượt chạy nào, tức khoảng 2,5% (từ 1.862 xuống 1.816 từ). Bạn trả lời "Đồng ý". Nguyên tắc đứng sau là CLAUDE.md của repo: "mỗi luật chỉ viết ở một chỗ".

Mọi điều dưới đây tôi đọc từ file, lịch sử git và lịch sử phiên. Tôi không chạy gì.

**Ví dụ xuyên suốt.** Lan có app với form đăng ký ở `src/auth`. Lan gõ `/i:test e2e đăng ký và đăng nhập`. i:test đi qua năm bước theo thứ tự: tìm phạm vi, ghi kết quả mong đợi, chọn loại test, chạy, báo cáo. Commit sửa ở cả năm bước.

**1. Tìm phạm vi: bỏ hai câu** (`skills/test/SKILL.md:49-55`)

Cần biết trước: i:flow chia việc lớn thành từng phần nhỏ gọi là slice, ghi trong hồ sơ `docs/shape/<tên>/shape.md`. Dòng `Current slice:` trong hồ sơ cho biết slice nào đang làm. Khi không ai nêu phạm vi, i:test lấy slice đó làm phạm vi.

- Câu "Never pick a dossier by fuzzy match" (đừng chọn hồ sơ theo tên na ná) bị bỏ. Câu ngay sau đã nói chính xác phải đọc hồ sơ nào: hồ sơ bên gọi nêu tên, không có thì tìm `docs/shape/*/shape.md` ở gốc repo, nhiều hồ sơ cùng có slice đang làm thì hỏi lại. Không còn chỗ nào phải đoán, nên câu cấm đoán thành thừa (theo lịch sử phiên).
- Câu "Say so when an explicit scope lands off the active slice" cũng bị bỏ. Câu này bắt i:test nói ra khi phạm vi người dùng nêu nằm ngoài slice đang làm. Lan đã gõ "đăng ký và đăng nhập" thì Lan biết mình xin gì. Câu này còn bắt i:test đi lục hồ sơ tìm slice, dù phạm vi đã rõ (theo lịch sử phiên).

**2. Ghi kết quả mong đợi: đổi tiêu đề, gom đoạn "Per scenario" về đây** (`skills/test/SKILL.md:57-65`)

Đây là lõi của i:test. Trước khi đọc code, nó ghi ra code phải làm gì, dựa trên tiêu chí của người dùng, hồ sơ và tài liệu. Nếu đọc code trước, test dễ khẳng định đúng cái code đang làm, kể cả khi code sai.

- Tiêu đề cũ là "written before any body is read", nghĩa là ghi trước khi đọc bất kỳ thân hàm nào. Lan xin hai khu vực, và i:test làm lần lượt từng khu vực. Sang "đăng nhập" thì code "đăng ký" đã đọc rồi, nên tiêu đề cũ không giữ được. Tiêu đề mới "before the code under test is read" chỉ đòi chưa đọc code của khu vực đang test (theo lịch sử phiên).
- Đoạn "Per scenario" trước nằm ở mục What to write, ngay trên đoạn Grouping. Với mỗi kịch bản, nó hỏi lại bốn câu: trả về gì, để lại trạng thái gì, cái gì không được đổi, gọi lần hai thì sao. Bốn câu này đã có trong danh sách ở mục Expectations. Commit chuyển phần ví dụ và câu "Never invent a case to fill a slot" lên ngay sau danh sách đó, rồi xóa đoạn cũ (theo lịch sử phiên).

Áp vào Lan: kịch bản "đăng ký bằng email đã có" cần ba thứ. Màn hình báo email đã dùng. Không có tài khoản mới nào được tạo. Tài khoản cũ còn nguyên. Câu "gọi lần hai thì sao" không áp dụng ở đây, nên không bịa ra một ca để lấp chỗ.

Chỗ này từng được cân trong lần gọt ngày 2/10. Theo file plan ngày đó (`~/.claude/plans/optimized-seeking-bird.md`), danh sách ở Expectations không được cắt. Lý do là danh sách ấy được trả lời trước khi đọc code, còn "Per scenario" trả lời sau. Cắt bản trước sẽ dời việc đặt kỳ vọng ra sau lúc đọc code. Commit này giữ bản trước, chỉ bỏ bản sau, nên không vi phạm điều ngày 2/10 lo.

**3. Test E2E: bỏ hai cụm, giữ luật dọn dữ liệu** (`skills/test/SKILL.md:112-117`)

Test E2E (đầu-cuối) đi đúng đường người dùng thật đi: mở trang, điền form, bấm nút. Đoạn này bỏ hai cụm:

- "response and observable final state both asserted", tức kiểm cả phản hồi lẫn trạng thái cuối. Hai thứ này đã nằm trong danh sách ở Expectations (theo lịch sử phiên).
- "a unique data namespace", tức mỗi lần chạy dùng vùng dữ liệu riêng, ví dụ mọi user test mang tiền tố `e2e-7f3a-`. Theo lịch sử phiên, cụm này đã có ở mục Native implementation, câu `skills/test/SKILL.md:127`.

Cụm "cleanup that also runs when the test fails" được cố ý giữ lại (theo lịch sử phiên). Claude hay đặt lệnh dọn dữ liệu ở cuối thân test. Giả sử test của Lan tạo user `lan-test@example.com` rồi đỏ ở bước thứ ba. Khi đó lệnh dọn ở cuối không bao giờ chạy. User ấy nằm lại trong DB, và lần chạy sau đăng ký trùng email thì hỏng.

**Chỗ hai bản ghi nói ngược nhau.** File plan ngày 2/10 đã cân việc cắt "a unique data namespace" khỏi đoạn E2E và quyết định giữ. Lý do ghi ở đó: cụm này "giữ cho bước dọn dẹp không xoá dữ liệu có sẵn", không trùng với câu namespace ở Native implementation. Câu ở dòng 127 nói namespace "wherever determinism needs them", tức để test chạy lần nào cũng ra cùng kết quả. Câu đó không nói gì về chuyện bảo vệ dữ liệu có sẵn.

Tôi suy ra một ca hỏng cụ thể: test của Lan dọn bằng lệnh "xóa mọi user có email đuôi `@example.com`". Test vẫn chạy ổn định, nhưng có thể xóa luôn user mà đồng nghiệp tạo trong DB dev dùng chung. Phiên hôm nay không nhắc lại lý do của ngày 2/10. Agent Fable bị cấm đọc file plan và ghi chú cũ, còn Claude chỉ nói cụm này "đã có ở chỗ khác". Đưa cụm này trở lại hay không là việc bạn quyết.

**4. Chạy test: chặn chế độ "chỉ xem" khỏi chạy** (`skills/test/SKILL.md:152`)

Chế độ "Only what is missing" nằm ở `skills/test/SKILL.md:107-110`. Lan gõ `/i:test only what is missing src/auth` để hỏi còn thiếu test nào. i:test không viết gì, không chạy gì. Nó chỉ đối chiếu từng kỳ vọng với test sẵn có rồi báo cáo.

Nửa tiếng trước commit này, commit `81368d4` sửa mục Run thành "chạy test mới, và cả test cũ được tính là đã kiểm". Đặt cạnh nhau thì hai câu kéo về hai hướng. Repo của Lan có sẵn `auth.spec.ts` kiểm "email trùng bị từ chối". Ở chế độ chỉ xem, mục Run bảo chạy test đó, còn câu của chế độ chỉ xem bảo không chạy gì.

Lúc làm `81368d4`, Claude cố ý không thêm câu chặn. Lý do là câu của chế độ chỉ xem đã nói "run nothing", và mỗi luật chỉ nên nằm một chỗ. Lần này hai lượt soát độc lập cùng chỉ ra chỗ ấy. Chỉ cần thêm cụm "Outside Only what is missing" là hết hiểu nhầm, nên Claude nhận (theo lịch sử phiên).

**5. Báo cáo: bỏ câu dành riêng cho i:flow** (cuối file, sau `skills/test/SKILL.md:192`)

Câu cuối cũ là: "Called from i:flow, return this same report; the dossier and the next action stay i:flow's." Lịch sử phiên nêu ba lý do câu này thừa. Đầu skill (`skills/test/SKILL.md:30-31`) đã cấm sửa hồ sơ i:flow. i:flow tự giữ quyền quyết bước tiếp theo. Context riêng vốn chỉ trả về được một báo cáo, nên ai gọi cũng nhận đúng báo cáo đó.

Trước nữa, câu này còn dài hơn ("… return those same items"). Ghi chú `docs/research/gon-lai-i-test/so-voi-flow-va-debug.md:31` cảnh báo bản dài có thể khiến i:test chép lại bức tranh và các quyết định trong hồ sơ, gửi ngược về cho i:flow. Commit `c574d59` ngày 2/10 rút câu này còn một dòng, và commit này bỏ hẳn.

**6. Số bản** (`.claude-plugin/plugin.json:3`): đổi từ 1.11.0 lên 1.11.1. Theo lịch sử phiên, bước này đi cùng lệnh push và `claude plugin update`, để máy bạn nhận bản gọt này. Tôi suy ra lý do chỉ tăng số cuối: commit không thêm tính năng nào.

**Còn lại để bạn quyết hoặc xem tiếp**

- Chuyện namespace ở phần 3 là chỗ duy nhất mà bản ghi cũ và code hiện tại nói ngược nhau.
- Commit này không chứa những đề xuất của agent Fable mà Claude bác, nên tôi chưa giảng. Ví dụ có một đề xuất sẽ đảo ngược đúng bản sửa phạm vi ở `d155930`. Chế độ Strict black-box cũng được giữ, vì bạn chưa quyết.
- Có một lệch nhỏ nằm ngoài commit. File plan gọt i:debug viết lúc 15:12 (`~/.claude/plans/hashed-discovering-goblet.md`, mục D4) ghi rằng i:test bỏ câu "Called from i:flow" ở `c574d59`. Thật ra `c574d59` chỉ rút ngắn câu đó, còn commit này mới bỏ hẳn.

Một câu hỏi để kiểm lại phần 1: Lan gõ `/i:test e2e đăng ký` đúng lúc hồ sơ i:flow đang ghi `Current slice: slice-03-thanh-toan`. Sau commit này, i:test lấy phạm vi nào, và báo cáo cuối có nhắc gì tới slice thanh toán không?
