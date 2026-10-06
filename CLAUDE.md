# Ghi chú cho người bảo trì plugin i

File này chỉ được nạp khi bạn, hoặc Claude, làm việc trong repo plugin. Người dùng plugin không bao giờ thấy nó. Vì vậy mọi lời dặn dành cho người sửa skill đặt ở đây, không đặt trong file skill.

Trước khi tag một bản mới, hoặc sau khi đổi một luật của flow hay lite, chạy bộ eval hành vi trong README (`claude plugin eval . --scaffold --allow-tools Write --ablation none`). Nó tốn tiền thật, khoảng mười hai phiên mỗi lần chạy đủ, nên không chạy sau mỗi lần sửa chữ. Một case chỉ kiểm được hành vi tự kết thúc: phiên headless không bấm được nút duyệt, nên không có case nào đi qua cổng.

Chạy `tests/run.sh` sau mỗi lần sửa hook hoặc checker của i:flow. Lệnh này dựng hồ sơ mẫu trong thư mục tạm, rồi kiểm cả hai hook lẫn checker.

Ba mục của flow chỉ dùng về cuối vòng slice (Redoing a slice, Tests from i:test, Finishing) nằm ở `skills/flow/references/closing.md`, không nằm trong SKILL.md, để SKILL.md của flow dưới hẳn ngưỡng 5.000 token mà Claude Code gắn lại sau khi nén hội thoại; nếu để trong SKILL.md thì chính ba mục ở đuôi này là phần bị cắt. Đừng gộp lại.

Trong một skill, mỗi luật chỉ viết ở một chỗ, chỗ khác thì trỏ về đó. Sau mỗi lần sửa file của một skill, chạy `skills/flow/scripts/check-pointers.sh <thư-mục-skill>`, ví dụ `skills/flow/scripts/check-pointers.sh skills/lite`. Script này bắt những lời trỏ đang chỉ vào file hoặc mục không còn tồn tại.

## Nhãn trong hồ sơ i:flow và ai đọc chúng

Các chuỗi liệt kê ở §2 của `skills/flow/references/state.md` là hợp đồng giữa năm thứ: mẫu hồ sơ (state.md §4 và §5), hook `hooks/iflow-resume.sh` lúc mở phiên, hook `hooks/iflow-check.sh` sau mỗi lần Edit hay Write vào `docs/iflow/*/iflow.md`, checker `skills/flow/scripts/check-dossier.sh` và `tests/run.sh`.

Muốn đổi một chuỗi thì sửa cả năm nơi trong cùng một commit. Checker chỉ bắt được chỗ lệch giữa mẫu và chính nó. Còn nếu hook lệch, chỉ `tests/run.sh` mới phát hiện ra. Hook check không đọc nhãn nào trực tiếp: nó chỉ xem dấu `iflow/2` rồi gọi checker, và in vi phạm ra stderr với exit 2 để Claude Code đưa lại cho Claude ngay sau lần ghi. Vì thế thứ tự ghi hồ sơ phải giữ nó nhất quán sau mỗi lần ghi: file slice có trước, hàng trong bảng có sau (state.md §3, SKILL.md invariant 2).

| Chuỗi | Ai đọc, đọc để làm gì |
|---|---|
| `Overall status:` (`running` hoặc `done`) | **Checker** kiểm giá trị có hợp lệ không. **Hook** không nhắc tới hồ sơ `done`, trừ khi checker báo nó hỏng. Hồ sơ `done` cũng được bỏ qua khi không tìm thấy checker hoặc checker tự lỗi, vì hồ sơ đã xong thì không còn việc gì để nhắc. |
| `Current slice:` | **Hook** in dòng này ra. **Checker** đối chiếu nó với trạng thái các hàng trong bảng slice. |
| `Next action:` | **Hook** in dòng này ra, nhưng giấu đi khi checker báo hồ sơ hỏng. **Checker** kiểm dòng này không rỗng và không phải chữ giữ chỗ. |
| Trạng thái hàng (`todo`, `doing`, `done`, `needs-redo`, `retired`) | **Checker** kiểm giá trị hợp lệ, bảng có ít nhất một hàng, và mỗi hàng chưa `retired` đều có file slice. |
| `<!-- generated-by: iflow/2 -->` | **Cả hai hook** chỉ đọc những `docs/iflow/*/iflow.md` có dấu này. File mất dấu sẽ bị hook bỏ qua hoàn toàn, không báo gì. **Checker** báo khi thiếu dấu. |
| `NN-<name>.md` | **Checker** kiểm mỗi hàng có file tương ứng. |

Ngoài hook và checker, i:debug, i:test và i:how cũng đọc hồ sơ của i:flow. Mỗi thư mục nhiệm vụ mang một id ngắn ở đuôi tên (`<việc>-a7f3`, bốn ký tự hex từ `openssl rand -hex 2`), và chỉ khi người dùng gọi tên nhiệm vụ đó thì skill khác mới ghi vào cùng thư mục, không skill nào tự đoán "cùng việc" để chui vào. Khi được gọi, i:lite ghi `research/`, i:explore ghi `explore/`, i:how ghi `how/`, i:gamify ghi `game/`; đổi tên một thư mục con hay cách đặt tên thư mục thì sửa skill ghi nó và state.md §1. Ba skill này đọc theo vai trò các mục: bức tranh, quyết định, charter, plan đã duyệt, kết quả, ghi chú, và các cột của bảng slice. Đổi vai trò hay tên một mục thì phải xem lại cả ba skill. i:how còn đọc khối kết quả mà i:lite ghi dưới plan, nên đổi khối đó cũng phải xem lại i:how. i:debug còn đọc bức tranh, phần nói plan sẽ đổi gì, các quyết định và giả định đã duyệt trong file plan của i:lite, nên đổi vai trò các phần đó cũng phải xem lại i:debug.

## i:flow và i:lite độc lập, không đồng bộ

i:lite ra đời từ i:flow nên nhiều đoạn hai bên giống nhau (`references/shape.md`, `agents.md`, luật ngôn ngữ, cổng duyệt, lần đọc lạ, quyết định giữa chừng). Từ 2026-10-07 hai skill chạy song song: sửa một bên thì **không** chép sang bên kia, không có danh sách phải đồng bộ, không có module chung. Mỗi skill tự đứng với file của nó, và được phép đi khác nhau theo thời gian. Muốn một thay đổi có ở cả hai thì sửa cả hai trong cùng commit và nói rõ trong message, đó là việc có chủ ý, không phải nghĩa vụ.

## Sửa i:gamify

Sau mỗi lần sửa gamify, chạy `skills/gamify/scripts/check-skill.sh`. Script này kiểm cấu trúc của skill mà không tốn API: frontmatter, lời trỏ, tiêu đề các mẫu, tám nhãn của mỗi khung, 18 điều văn phong, 32 điều thiết kế.

- Gamify chạy trong hội thoại chính vì cần `AskUserQuestion`, mà fork không có công cụ này. Đừng thêm `context: fork` vào frontmatter.
- Ba file tham chiếu giữ phần chỉ đọc một lần, để hai file đọc đi đọc lại nhẹ đi: `ke-hoach-gamemaster.md` (bước A và mẫu gamemaster, chỉ slice 01), `sau-dungeon.md` (slice `tools.md`, kiểm cuối, sửa và mở rộng), `quan-tro-moc.md` (chấm bài kiểm và qua vùng, vài tuần một lần). Phần đọc mỗi slice ở `vong-slice.md`, phần đọc mỗi lần chơi ở `quan-tro.md`, kể cả luật "khi nào bảo đánh" vì mọi phiên đều cần nó. Đừng gộp lại; check-skill.sh kiểm đủ các mục ở từng file.
- Khung mới thêm vào cuối `references/thu-vien-khung.md`, đủ tám mục có nhãn. Script đếm heading `## Khung N` và soi đủ tám nhãn.
- SKILL.md viết tiếng Anh, các file tham chiếu viết tiếng Việt.
- Giữ SKILL.md của gamify dưới 5.000 token (hiện khoảng 15 KB). Sau khi nén hội thoại, skill không tự đọc lại SKILL.md mà trông vào việc Claude Code tự gắn lại file dưới ngưỡng này; file dài quá ngưỡng thì phần cuối, gồm các luật chung, bị cắt.
