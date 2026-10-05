# Ca 1: hỏi "vừa làm gì" khi repo đang có thay đổi chưa commit

- **Câu hỏi gõ vào:** `/i:how vừa làm gì vậy?`
- **Tình trạng repo lúc hỏi:** repo plugin trên nhánh main, đang có phần i:how chưa commit (4 file sửa, thư mục skills/how mới) và các thư mục nháp backup/, docs/ chưa được git theo dõi
- **Bản i:how được nạp:** bản viết đầu tiên, trước sáu chỗ sửa

Phần dưới là nguyên văn câu trả lời cuối của lần chạy, không sửa chữ nào. Đường dẫn trong `/tmp` mà câu trả lời nhắc tới đã bị xóa sau lần chạy.

---

**Thay đổi chưa commit trên `main`:** bạn thêm skill mới `i:how` (thư mục `skills/how/`, 2 file, 220 dòng, chưa `git add`) và sửa 4 file để plugin khai báo nó (8 dòng thêm, 7 dòng bớt).

Plugin `i` giờ có bảy skill. Gõ `/i:how <câu hỏi>` thì Claude tìm đoạn code hoặc thay đổi mà câu hỏi nhắm tới, giảng từng phần kèm lý do, rồi hỏi ngược lại cho tới khi bạn tự kể lại được. Câu trả lời bạn đang đọc chính là `i:how` đang chạy. Nên tôi lấy luôn lượt này làm ví dụ xuyên suốt: bạn gõ `/i:how vừa làm gì vậy?` khi `main` có 4 file đang sửa và 8 thư mục chưa track.

Có vài thư mục chưa track không thuộc thay đổi này: `backup/`, 4 thư mục trong `docs/research/`, `docs/review/` và `docs/shape/got-flow/`. Đó là ghi chép và bản sao lưu từ 21/09 đến 02/10.

### 1. Khai báo skill để Claude Code nhận ra nó

- `.claude-plugin/plugin.json:3-4` là file mô tả plugin, Claude Code đọc khi cài hoặc cập nhật. Version lên `1.12.0` (trước là `1.11.1`), và mô tả có thêm "(i:how)". `.claude-plugin/marketplace.json:3,11` thêm `i:how` vào hai dòng liệt kê skill.
- `skills/how/SKILL.md:13` có dòng `disable-model-invocation: true`. Claude Code thấy dòng này thì giấu mô tả skill khỏi model. Kết quả là Claude không bao giờ tự mở `i:how`, phải gõ `/i:how` nó mới chạy.
- Lý do chỉ cho gọi tay nằm trong memory `explicit-call-over-auto-trigger`, ghi ngày 05/10 lúc làm i:test. Theo memory đó, bạn thích tự gọi tên skill. Còn mỗi lần nới mô tả để skill tự bật lại tốn một lượt đo 60 phiên. Memory dặn thay vào đó thêm một dòng README chỉ cách gọi. `README.md:13` làm đúng vậy: "Call it by name: `/i:how vừa làm gì vậy?`".
- `README.md:19` thêm `how` vào danh sách skill mà `scripts/trigger-eval.sh` từ chối đo. Script này đo xem mô tả có khiến Claude tự mở skill không. **Đã chạy** `scripts/trigger-eval.sh how evals/smoke.json`: thoát mã 2, in ra "how is user-invoked only (disable-model-invocation: true): Claude never sees its description, so there is nothing to measure". Script dừng trước khi gọi `claude -p`, nên lệnh này không tốn gì.
- Lên 1.12.0 chứ không lên 1.11.2 là **tôi suy ra** từ lịch sử. Commit `fae8c2f` thêm tính năng (làn fast) thì tăng số giữa. Commit `854968e` chỉ sửa thì tăng số cuối.

### 2. Tìm đúng thứ câu hỏi nhắm tới (mục 1, `skills/how/SKILL.md:27`)

Skill chia câu hỏi làm ba loại:

- **Bạn chỉ rõ phạm vi** (một file, commit, nhánh): skill lấy đúng thứ đó, nhưng kiểm nó có thật trước.
- **"Vừa làm gì":** đang ở nhánh phụ thì lấy mọi commit từ lúc tách khỏi nhánh chính, cộng phần chưa commit. Đang ở nhánh chính thì lấy các file đang sửa, không có thì lấy commit cuối. File chưa track chỉ được tính khi file đang sửa nhắc tới nó, hoặc nó là code chạy thật. Ghi chép và bản sao lưu chỉ được nhắc tên trong một dòng.
- **Hỏi về một tính năng:** skill đổi câu hỏi thành từ khóa theo cách code viết, như tên hàm, chữ trên giao diện, thông báo lỗi. Nó tìm trong code, xếp chỗ bắt đầu chạy (route, handler, hook) lên trên docs và test, rồi lần lịch sử bằng `git log -S`.

Tìm xong thì có bốn cách xử lý. Ra một thứ thì dòng đầu gọi tên nó. Ra vài thứ thì hỏi bạn chọn một. Không ra gì thì nói đã tìm chữ nào ở đâu và xin gợi ý, không được giảng theo phỏng đoán. Thay đổi quá lớn thì lượt đầu chỉ tóm tắt, chia phần để bạn chọn chỗ đi sâu.

Ví dụ lượt này: `main` là nhánh chính và có 4 file đang sửa, nên skill lấy 4 file đó. `skills/how/` chưa track nhưng README nhắc tới `i:how`, nên cũng được tính vào. `backup/` là bản sao lưu nên chỉ được nhắc một dòng ở đầu.

### 3. Lục lý do đã được ghi lại (mục 2, `:76`)

Skill phải tìm lý do có sẵn trước khi tự suy, theo thứ tự này:

1. Chính hội thoại đang diễn ra.
2. Hồ sơ i:flow trong `docs/shape/*/`.
3. File plan của plan mode trong `~/.claude/plans/`, gồm cả khối kết quả mà i:lite ghi dưới plan.
4. Ghi chép trong `docs/research/`.
5. Commit message, mô tả PR, chú thích và test nằm cạnh code.

Mỗi lý do phải kèm nguồn trong nửa câu. Lý do tự suy thì ghi "tôi suy ra". Bản ghi nói một đằng mà code làm một nẻo thì phải nói thẳng ra.

`i:how` đọc hồ sơ i:flow, nên `CLAUDE.md:24` thêm nó vào danh sách skill đọc hồ sơ. Trước đây câu đó chỉ có i:debug và i:test. Lý do nằm ngay trong `CLAUDE.md`: tên các mục trong hồ sơ là thứ nhiều skill cùng dựa vào. Ai đổi tên một mục mà quên một skill đang đọc nó, thì skill đó đọc hụt mà không ai hay.

Ví dụ lượt này: tôi không tìm thấy bản ghi nào cho `i:how`. `docs/shape/` chỉ có hồ sơ `got-flow` từ 28/09. Plan mới nhất (`hashed-discovering-goblet.md`, 15:04 hôm nay) là đợt rà sáu skill cũ, không nhắc `i:how`. `docs/research/` cũng không có. Vì vậy lý do trong bài này lấy từ memory, từ `CLAUDE.md` và từ chính SKILL.md, chỗ nào tự suy thì có ghi rõ.

### 4. Giảng, và vẽ trang khi chữ không đủ (mục 3–4, `:97`, `references/page.md`)

Mỗi lượt giảng đi theo thứ tự cố định:

1. Câu trả lời, một hai câu.
2. Từ 3 đến 7 phần, cắt theo logic chứ không theo file, xếp theo thứ tự chạy. Mỗi phần có `file:dòng`, lý do kèm nguồn, và trước đây ra sao.
3. Một ví dụ có tên người và giá trị thật, đi xuyên qua mọi phần.
4. Còn thiếu gì chưa giảng.

Gì kiểm được rẻ và an toàn thì phải chạy, rồi dán output thật vào, ghi rõ "đã chạy" hay "đọc từ code". Trước lần chạy đầu và sau lần chạy cuối đều ghi `git status`. Lệnh nào để lại file đổi thì phải báo, không được hoàn tác bằng `git checkout`, `git restore` hay `git stash`. Cấm chạy vào hệ thống thật, dữ liệu thật hay API mất tiền, và cấm cài thêm gì.

Trang hình chỉ dùng cho bốn loại nội dung: luồng có rẽ nhánh hoặc nhiều bên tham gia, so sánh trước và sau, biểu đồ, hoặc ảnh. Có tool `Artifact` thì đăng thành trang riêng trên claude.ai. Code cần giữ kín thì ghi ra file HTML trên máy. Trang không đặt câu hỏi nào, câu hỏi chỉ nằm trong chat.

Ví dụ lượt này: tôi chạy ba lệnh, và `git status` trước với sau giống hệt nhau. Thay đổi lần này là một danh sách luật, không có luồng rẽ nhánh, nên không vẽ trang.

### 5. Hỏi lại xem bạn hiểu chưa, rồi kết thúc (mục 5–6, `:136`)

Giảng xong hết mới hỏi. Mỗi tin nhắn chỉ một câu hỏi mở, kiểu câu không trả lời được bằng cách chép lại bài. Có bốn kiểu:

- Đoán trước: "gửi form hai lần thì sao?"
- Phá thử: "xóa dòng này thì hỏng gì?"
- Mở rộng: "muốn thêm X thì sửa ở đâu?"
- Lần đường đi: "email đi qua những chỗ nào?"

Câu trả lời đầu tiên cho biết trình độ của bạn. Đúng thì các câu sau ít hơn mà khó hơn. Sai thì skill chỉ đúng chỗ hiểu lệch và giảng lại bằng ví dụ khác. Skill không dùng câu hỏi có sẵn đáp án, vì theo SKILL.md đáp án có sẵn thì đoán mò được. Nó cũng không hỏi "hiểu chưa?". Bạn nói "thôi" là dừng ngay.

Lúc kết thúc, skill liệt kê phần chưa giảng và điều chỉ đọc mà chưa chạy, rồi để bạn tự quyết thế là đủ hay chưa. Nghi có lỗi thì nó chỉ sang `/i:debug`. Muốn sửa thì `/i:lite`. Hành vi chưa có test thì `/i:test`. Bài giảng chỉ được ghi vào `docs/how/<chủ-đề>.md` khi bạn bảo giữ lại.

### Đã kiểm tới đâu

**Đã chạy:**
- `skills/flow/scripts/check-pointers.sh skills/how` báo "2 pointers checked in 2 files, all resolve". Nghĩa là link từ SKILL.md sang `references/page.md` trỏ đúng file.
- `jq` đọc được cả hai file JSON, ra version `1.12.0`.
- Lệnh trigger-eval ở phần 1 từ chối đúng như README mô tả.

**Chỉ đọc từ code:** phần 2 đến 5. Skill có làm đúng như mô tả không thì hiện chỉ có lượt này làm chứng.

**Một chỗ README và skill nói khác nhau:** `README.md:13` ghi "Reads only". Nhưng `references/page.md` cho phép ghi `docs/how/<chủ-đề>.md` khi bạn yêu cầu, và ghi file HTML vào thư mục tạm. `SKILL.md:23` nói chính xác hơn: chỉ cấm sửa code, test, config, hồ sơ và plan.

**Chưa giảng:** chi tiết trang hình phải có những gì, và luật dùng từ chuyên môn trong mục 3. Muốn đi sâu thì nên bắt đầu từ phần 2, phần có nhiều nhánh nhất.

---

Câu hỏi: giả sử bạn commit hết thay đổi này, kể cả `skills/how/`, rồi gõ ngay `/i:how vừa làm gì vậy?` trên `main`. Lần này skill sẽ lấy gì để giảng, và `backup/` có được giảng không?
