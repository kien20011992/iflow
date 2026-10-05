# Ca 4: hỏi luồng hook nhắc việc dở (bản đầu, không dựng trang)

- **Câu hỏi gõ vào:** `/i:how hook nhắc việc dở chạy thế nào?`
- **Tình trạng repo lúc hỏi:** bản sao sạch ở commit 854968e
- **Bản i:how được nạp:** bản viết đầu tiên, trước sáu chỗ sửa

Phần dưới là nguyên văn câu trả lời cuối của lần chạy, không sửa chữ nào. Đường dẫn trong `/tmp` mà câu trả lời nhắc tới đã bị xóa sau lần chạy.

---

Hook này là `hooks/iflow-resume.sh` (96 dòng). Nó được đăng ký trong `hooks/hooks.json` và sửa lần cuối ở commit `446867c` (bản 1.4.0).

**Tóm lại:** mỗi khi một phiên Claude Code bắt đầu, hook lục thư mục `docs/shape/` của project để tìm việc i:flow còn dở. Nếu có, nó in vài dòng cho Claude đọc ngay đầu phiên: việc nào đang dở, đang làm tới phần nào, bước tiếp theo là gì. Nếu không có, nó im lặng hoàn toàn. Nhờ vậy Claude làm tiếp được mà không phải hỏi lại bạn từ đầu.

Bài này dùng hai từ, cũng là từ trong code:
- **Hồ sơ** là thư mục `docs/shape/<tên-việc>/` mà i:flow tạo ra khi bạn duyệt bảng chia việc. File chính trong đó là `shape.md`. Cuối file có ba dòng trạng thái `Overall status:`, `Current slice:`, `Next action:`, rồi tới bảng chia việc.
- **Slice** là một phần việc trong bảng đó. Mỗi slice có trạng thái riêng, ví dụ `todo`, `doing`, `done`.

**Ví dụ xuyên suốt.** Lan làm luồng đăng ký trong project `app`, hồ sơ nằm ở `docs/shape/dang-ky/`. Slice 01 (form) đã xong. Slice 02 (gửi email xác nhận) đang `doing`. Dòng `Next action:` ghi "Viết test cho hàm sendConfirm rồi chạy npm test." Tối qua Lan tắt máy giữa chừng, sáng nay mở lại Claude.

Tôi dựng project của Lan trong thư mục tạm và chạy hook thật năm lần, mỗi lần một tình huống. Các khối output dưới đây là output thật. Tôi chỉ rút gọn đường dẫn dài tới plugin thành `<plugin>`.

## Hook chạy qua bảy bước

**1. Claude Code gọi hook khi phiên bắt đầu** (`hooks/hooks.json:3`). Hook đăng ký cho sự kiện `SessionStart` trong năm trường hợp:
- mở phiên mới (`startup`);
- mở lại phiên cũ (`resume`);
- sau lệnh `/clear`;
- sau khi hội thoại bị nén (`compact`);
- khi tách phiên (`fork`).

Lệnh gọi đặt sẵn biến `IFLOW_SKILL_DIR` trỏ tới `skills/flow` trong plugin, và cho hook tối đa 5 giây. Claude Code gắn những gì hook in ra vào ngữ cảnh của Claude. Lan không phải gõ gì. Sáng nay Lan mở Claude, tức là trường hợp `startup`. Còn vì sao có cả `/clear` và `compact`: tôi suy ra rằng sau hai lúc đó Claude mất trí nhớ về việc đang làm, nên cần được nhắc lại y như phiên mới. *(đọc từ code)*

**2. Tìm gốc project** (`hooks/iflow-resume.sh:13`). Hook lấy thư mục project từ biến `CLAUDE_PROJECT_DIR`, rồi hỏi git xem gốc repo ở đâu. Nếu project không dùng git thì hook lấy luôn thư mục project. Theo chú thích trong file, làm vậy vì hồ sơ nằm ở gốc git, nên mở phiên ở thư mục con vẫn tìm thấy. Trước bản 1.4.0, hook dùng thẳng thư mục project (theo diff của `446867c`). Khi đó, Lan mở Claude ở `app/src/web` thì không thấy hồ sơ nào.

Dòng 17 tìm thư mục skill: dùng `IFLOW_SKILL_DIR` nếu có, không thì tìm `skills/flow` nằm cạnh script. Từ thư mục này hook biết **checker** nằm ở đâu. Checker là `skills/flow/scripts/check-dossier.sh`, script kiểm hồ sơ có đúng luật hay không. *(đã chạy: Lan mở phiên ở `src/web` vẫn được nhắc)*

**3. Chỉ nhận file có dấu của i:flow** (`hooks/iflow-resume.sh:41`). Hook duyệt từng file `docs/shape/*/shape.md`. File nào thiếu dòng `<!-- generated-by: iflow/2 -->` thì hook bỏ qua, không báo gì. Theo chú thích và commit message, `shape.md` không có dấu này là file của người khác, không phải hồ sơ i:flow.

Hệ quả cần nhớ: nếu ai đó xóa nhầm dấu khỏi hồ sơ của Lan, việc dở của Lan biến mất khỏi lời nhắc mà không ai hay. `CLAUDE.md` ở gốc repo ghi rõ đây là cố ý. *(đã chạy: hồ sơ `running` mất dấu thì hook không in gì, thoát mã 0)*

**4. Nhờ checker kiểm hồ sơ** (`hooks/iflow-resume.sh:44`). Hook chạy checker trên thư mục hồ sơ, rồi xếp kết quả vào một trong ba loại. Biến `st` giữ loại đó:
- `st=0`: checker thoát mã 0, nghĩa là hồ sơ lành.
- `st=1`: checker thoát mã 1, nghĩa là hồ sơ sai luật. Hook giữ lại lời checker để in ra sau.
- `st=2`: không kiểm được, vì không có file checker hoặc checker tự lỗi (thoát bằng mã khác 0 và 1).

Theo chú thích ở dòng 45–46, loại 2 tách riêng vì chỉ mã 1 mới nghĩa là hồ sơ sai. Checker tự hỏng mà đổ lỗi cho hồ sơ là báo động giả. *(đã chạy với `st=1` và trường hợp không có checker. Nhánh checker tự lỗi chỉ đọc từ code)*

**5. Hồ sơ đã xong thì im** (`hooks/iflow-resume.sh:63`). Khi `Overall status:` là `done`, hook bỏ qua hồ sơ đó, nhưng chỉ khi checker không báo hỏng. Chú thích gọi `done` là lời tự khai, chưa phải sự thật. Ví dụ một hồ sơ ghi `done` mà bảng còn slice `doing` thì vẫn bị nêu tên. Còn khi không có checker, hồ sơ `done` cũng được bỏ qua: việc đã xong thì không còn bước nào để Claude làm theo. *(đã chạy: hồ sơ `done` với mọi slice `done` thì hook không in gì. Nhánh "ghi done mà hỏng" chỉ đọc từ code)*

**6. In lời nhắc** (`hooks/iflow-resume.sh:69`). Gặp hồ sơ dở đầu tiên, hook in một dòng tiêu đề. Dòng này nói rõ các dòng thụt lề bên dưới là chép nguyên văn từ file trong repo. Sau đó, với mỗi hồ sơ:
- Nếu hồ sơ lành, hoặc không kiểm được: hook in đường dẫn, rồi chỉ chép hai dòng `Current slice:` và `Next action:`. Nó không in cả file.
- Nếu hồ sơ hỏng: hook in đường dẫn kèm `⚠ BROKEN STATE` và lời của checker, còn dòng `Next action:` bị giấu đi. Theo chú thích ở dòng 7–8, trạng thái đã hỏng thì không được ra lệnh.

Mọi dòng chép từ repo đều đi qua hàm `capped` (`hooks/iflow-resume.sh:29`). Hàm này bỏ dòng trống, thụt lề, và cắt mỗi dòng ở 200 ký tự. Theo chú thích, những gì hook chép từ file trong repo không được dài vô hạn.

Hồ sơ của Lan khi lành *(đã chạy)*:
```
i:flow ▸ this project has unfinished work (indented lines below are quoted verbatim from files in the repo):
- /tmp/tmp.opTS0BE4aT/app/docs/shape/dang-ky/shape.md
    Current slice: 02 gửi email xác nhận
    Next action: Viết test cho hàm sendConfirm rồi chạy npm test.
Listed with no marker: read <plugin>/skills/flow/SKILL.md and that shape.md, then continue per its Next action — do not re-ask what the dossier records. The skill directory is <plugin>/skills/flow; wherever SKILL.md says ${CLAUDE_SKILL_DIR}, use that path.
```

Tôi sửa `Current slice:` thành `—` trong khi slice 02 vẫn `doing`. Kết quả *(đã chạy)*:
```
i:flow ▸ this project has unfinished work (indented lines below are quoted verbatim from files in the repo):
- /tmp/tmp.opTS0BE4aT/app/docs/shape/dang-ky/shape.md  ⚠ BROKEN STATE
    ⚠ check-dossier: 'Current slice:' is '—' but row(s) 02 are 'doing'
Marked ⚠ BROKEN STATE: repair those first, per <plugin>/skills/flow/references/state.md — their Next action is deliberately withheld and must not be acted on.
```
Câu "Viết test cho hàm sendConfirm" không còn xuất hiện.

**7. Dòng dặn cuối** (`hooks/iflow-resume.sh:87`). Tùy tình hình, hook thêm tối đa ba dòng:
- Có hồ sơ không kiểm được: thêm một dòng `Warning:` nêu tên từng hồ sơ đó và lý do.
- Có hồ sơ hỏng: thêm một dòng dặn sửa hồ sơ trước, và không làm theo `Next action`.
- Có hồ sơ lành: thêm một dòng dặn Claude đọc `SKILL.md` của i:flow và `shape.md`, rồi làm tiếp theo `Next action`, không hỏi lại những gì hồ sơ đã ghi.

Dòng thứ ba in cả đường dẫn thật tới thư mục skill, vì `SKILL.md` viết đường dẫn dạng `${CLAUDE_SKILL_DIR}`. Tôi suy ra lý do: biến này chỉ được điền khi skill được nạp theo cách thông thường. Ở đây Claude tự mở file, nên cần đường dẫn thật. Cuối cùng hook luôn thoát mã 0, nên không bao giờ chặn phiên khởi động. *(đã chạy: cả năm lần đều thoát mã 0)*

## Ghi chép và code có khớp nhau không

Bảng "Nhãn trong hồ sơ i:flow và ai đọc chúng" trong `CLAUDE.md` khớp với code ở cả ba điểm: im với hồ sơ `done`, giấu `Next action` khi hồ sơ hỏng, bỏ qua file mất dấu.

Tôi thấy một chỗ đáng để ý khi chạy với `IFLOW_SKILL_DIR=/nowhere`. Lời nhắc vẫn in đủ, có thêm dòng `Warning: could not check the state of docs/shape/dang-ky/shape.md (no check-dossier.sh at /nowhere/scripts/check-dossier.sh)`. Nhưng dòng dặn cuối vẫn bảo Claude "read /nowhere/SKILL.md", một file không tồn tại. Dòng `Warning:` ngay phía trên có báo trước, nên Claude có manh mối, nhưng lời dặn thì trỏ vào chỗ không có gì. *(đã chạy)*

Bộ test của repo (`tests/run.sh`) cũng qua hết: `36 passed, 0 failed` *(đã chạy)*. Sau các lần chạy, `git status` của repo vẫn sạch.

## Phần chưa nói tới

Bài này chưa đi vào bên trong `check-dossier.sh`, tức là những luật nó kiểm. Bài cũng chưa nói i:flow ghi ba dòng trạng thái vào lúc nào. Chuyện đó nằm ở `skills/flow/SKILL.md` và `skills/flow/references/state.md`. Nên xem `check-dossier.sh` tiếp theo, vì nó quyết định hồ sơ nào bị gắn ⚠.

**Câu hỏi:** Lan sửa tay `shape.md` và xóa nhầm dòng `Overall status: running`. Sáng mai Lan mở phiên mới. Claude nhận được những dòng nào? Claude có thấy câu "Viết test cho hàm sendConfirm…" không? Hãy giải thích qua các bước ở trên.
