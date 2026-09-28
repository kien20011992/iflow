# Ghi chú cho người bảo trì plugin i

File này chỉ được nạp khi bạn, hoặc Claude, làm việc trong repo plugin. Người dùng plugin không bao giờ thấy nó. Vì vậy mọi lời dặn dành cho người sửa skill đặt ở đây, không đặt trong file skill.

Chạy `tests/run.sh` sau mỗi lần sửa hook hoặc checker của i:flow. Lệnh này dựng hồ sơ mẫu trong thư mục tạm, rồi kiểm cả hook lẫn checker.

Trong một skill, mỗi luật chỉ viết ở một chỗ, chỗ khác thì trỏ về đó. Sau mỗi lần sửa file của một skill, chạy `skills/flow/scripts/check-pointers.sh <thư-mục-skill>`, ví dụ `skills/flow/scripts/check-pointers.sh skills/lite`. Script này bắt những lời trỏ đang chỉ vào file hoặc mục không còn tồn tại.

## Nhãn trong hồ sơ i:flow và ai đọc chúng

Các chuỗi liệt kê ở §2 của `skills/flow/references/state.md` là hợp đồng giữa bốn thứ: mẫu hồ sơ (state.md §4 và §5), hook `hooks/iflow-resume.sh`, checker `skills/flow/scripts/check-dossier.sh` và `tests/run.sh`.

Muốn đổi một chuỗi thì sửa cả bốn nơi trong cùng một commit. Checker chỉ bắt được chỗ lệch giữa mẫu và chính nó. Còn nếu hook lệch, chỉ `tests/run.sh` mới phát hiện ra.

| Chuỗi | Ai đọc, đọc để làm gì |
|---|---|
| `Overall status:` (`running` hoặc `done`) | **Checker** kiểm giá trị có hợp lệ không. **Hook** không nhắc tới hồ sơ `done`, trừ khi checker báo nó hỏng. Hồ sơ `done` cũng được bỏ qua khi không tìm thấy checker hoặc checker tự lỗi, vì hồ sơ đã xong thì không còn việc gì để nhắc. |
| `Current slice:` | **Hook** in dòng này ra. **Checker** đối chiếu nó với trạng thái các hàng trong bảng slice. |
| `Next action:` | **Hook** in dòng này ra, nhưng giấu đi khi checker báo hồ sơ hỏng. **Checker** kiểm dòng này không rỗng và không phải chữ giữ chỗ. |
| Trạng thái hàng (`todo`, `doing`, `done`, `needs-redo`, `retired`) | **Checker** kiểm giá trị hợp lệ, bảng có ít nhất một hàng, và mỗi hàng chưa `retired` đều có file slice. |
| `<!-- generated-by: iflow/2 -->` | **Hook** chỉ đọc những `shape.md` có dấu này. File mất dấu sẽ bị hook bỏ qua hoàn toàn, không báo gì. **Checker** báo khi thiếu dấu. |
| `slice-NN-<name>.md` | **Checker** kiểm mỗi hàng có file tương ứng. |

Ngoài hook và checker, i:debug và i:test cũng đọc hồ sơ của i:flow. Hai skill này đọc theo vai trò các mục: bức tranh, quyết định, charter, plan đã duyệt, kết quả, ghi chú, và các cột của bảng slice. Đổi vai trò hay tên một mục thì phải xem lại cả hai skill.

## Lite cần đồng bộ tay

i:lite chép gần nguyên văn ba chỗ của i:flow: `skills/flow/references/shape.md`, `agents.md`, và vài đoạn trong SKILL.md (cổng duyệt, chứng minh, báo cáo). Hai bên không có script canh lệch.

Mỗi lần đổi một đoạn bên flow mà lite có bản chép, hãy ghi một dòng vào danh sách dưới đây. Đồng bộ xong thì xóa dòng đó.

- `skills/lite/references/shape.md` §0–§2 và §4 cần theo bản mới của `skills/flow/references/shape.md`, do slice 02 của chương trình `docs/shape/got-flow/` sửa (các mã `sh-*`, `cc-3`, `cc-10`, `cc-11`, `st-5`, `st-6`, `st-7` trong `muc-da-duyet.md`). Những chỗ lite cố ý khác flow thì giữ nguyên: lite có đường "fast", có trạng thái trục "hoãn vào phần giả định của plan", và giai đoạn 3 của lite ra một plan duy nhất.
- `skills/lite/references/agents.md` cần theo `skills/flow/references/agents.md` (các mã `cc-4a`, `cc-13`, `st-7`).
- `skills/lite/SKILL.md`: hai phần "luật ngôn ngữ" và "đoạn Agents" cần theo bản mới của flow (các mã `sh-B4`, `sh-B16`, `sh-D1`). Dòng gọi `../flow/scripts/check-pointers.sh` thì chuyển vào file này, như flow đã làm (mã `md-2`).
- `skills/lite/SKILL.md`, ba phần "The gate", "Build and prove" và "Mid-flight decisions" cần theo slice 03 của cùng chương trình:
  - câu hỏi duyệt hết giờ hoặc bị từ chối thì không tính là duyệt (`cc-12`);
  - bỏ câu "the only definition" (`md-3`);
  - test đỏ có từ lần chạy mốc thì ghi lại một lần, không làm fail (`loop-3`);
  - `/code-review` chạy nền, phải chờ kết quả (`cc-7`);
  - kết quả review đòi lệch khỏi plan thì cần người dùng quyết trước (`ex-A1`);
  - chỉ chép bước vào todo list khi có công cụ task list (`cc-5`).
