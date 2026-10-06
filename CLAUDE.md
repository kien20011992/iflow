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
| `<!-- generated-by: iflow/2 -->` | **Hook** chỉ đọc những `docs/iflow/*/iflow.md` có dấu này. File mất dấu sẽ bị hook bỏ qua hoàn toàn, không báo gì. **Checker** báo khi thiếu dấu. |
| `NN-<name>.md` | **Checker** kiểm mỗi hàng có file tương ứng. |

Ngoài hook và checker, i:debug, i:test và i:how cũng đọc hồ sơ của i:flow. Cùng thư mục nhiệm vụ đó, i:lite ghi `research/`, i:explore ghi `explore/`, i:how ghi `how/`, i:gamify ghi `game/`; đổi tên một thư mục con thì sửa skill ghi nó và state.md §1. Ba skill này đọc theo vai trò các mục: bức tranh, quyết định, charter, plan đã duyệt, kết quả, ghi chú, và các cột của bảng slice. Đổi vai trò hay tên một mục thì phải xem lại cả ba skill. i:how còn đọc khối kết quả mà i:lite ghi dưới plan, nên đổi khối đó cũng phải xem lại i:how. i:debug còn đọc bức tranh, phần nói plan sẽ đổi gì, các quyết định và giả định đã duyệt trong file plan của i:lite, nên đổi vai trò các phần đó cũng phải xem lại i:debug.

## Lite cần đồng bộ tay

i:lite chép gần nguyên văn ba chỗ của i:flow: `skills/flow/references/shape.md`, `agents.md`, và vài đoạn trong SKILL.md (luật ngôn ngữ, cổng duyệt, soát trước cổng, chứng minh, review, Mid-flight decisions, định nghĩa giả định). Hai bên không có script canh lệch. Khi đồng bộ, so từng đoạn: bản của lite là bản của flow, trừ những chỗ lite cố ý khác dưới đây. Đừng chép đè lên các chỗ này.

- Lite không có slice, và không bao giờ sửa file của flow trong thư mục nhiệm vụ (`iflow.md`, `NN-<name>.md`, `evidence/`). Giai đoạn 3 ra một plan duy nhất.
- Lite không có hồ sơ, không có hook. Một lượt dở chỉ chạy tiếp được nhờ khôi phục bản nháp. Khi khôi phục, mọi lựa chọn trong một plan chưa được duyệt vẫn chỉ là giả định.
- Lite bật plan mode ở bước 2 của SKILL.md, nên shape.md của lite không có câu `EnterPlanMode` ở đầu như flow.
- Cả hai bên có làn `fast` để người dùng bỏ phần bàn, nhưng mỗi bên một bản. Bản của flow nằm ở mục 5 của `skills/flow/references/shape.md`. Bản của lite nằm ở mục "Two lanes" trong SKILL.md của lite, không nằm trong shape.md, nên đừng chép mục 5 sang shape.md của lite. Cả hai làn fast đều mồi từ hồ sơ i:explore khi có. Hai bản khác nhau ở hai chỗ. Lite đọc sâu code rồi viết một plan, còn flow chỉ quét repo rồi cắt bảng slice, để dành phần đọc sâu cho plan của từng slice. Khi người dùng bác một giả định ở nút duyệt, lite chia bản đồ như vòng mở đầu, còn flow giữ các giả định còn lại trong bảng slice.
- Lite có thêm lối nhảy thẳng sang plan khi không điểm nào đáng quyết. Khi nhảy thẳng, hướng đang nghiêng của mỗi điểm vào phần giả định của plan. Điểm giao cho model quyết cũng được báo trong phần giả định, còn flow báo trong bức tranh.
- Vòng mở đầu được chia bản đồ: điểm rẻ và dễ quay lại thì hoãn vào phần giả định của plan (trạng thái "deferred to the plan's assumptions"). Người dùng quyết các điểm đó ở bước duyệt. Vì vậy nút "Lock" cũng được bỏ khi các điểm hoãn đến từ việc chia bản đồ.
- Chữ nói về slice trong bản flow được đổi thành lời của lite, ví dụ "the plan's innards" và "the deep read".
- Mục "Zone research" của lite giữ nguyên bậc nguồn và luật con số tại chỗ, vì lite không có state.md để trỏ như flow.
- Ghi chép nghiên cứu, khi có, được ghi ra `docs/iflow/<nhiệm-vụ>/research/` ở bước đầu của plan. Flow ghi lúc tạo hồ sơ.
- Bằng chứng của lite nằm trong khối kết quả ở file plan; lite không có luật "bằng chứng nằm trong repo" của flow.
- Hết lượt, lite ghi khối kết quả vào file plan, rồi đổi dòng `Shape draft:` thành `Shape draft done:`. Flow đổi dòng này lúc tạo hồ sơ.
- Sau khi nén hội thoại, lite không đọc lại SKILL.md, vì SKILL.md của lite nhỏ hơn ngưỡng 5.000 token mà Claude Code tự gắn lại. Flow vẫn đọc lại, vì SKILL.md của flow sát ngưỡng. Riêng bước ĐẦU của plan lite vẫn đọc lại SKILL.md khi nó không còn trong context, để phủ trường hợp xoá context lúc duyệt.
- Kết quả review mà cách sửa lệch khỏi plan thì lite chỉ báo lại. Lite không chép luật "hỏi người dùng trước" của flow (`ex-A1`).
- Lite cân "quá lớn cho một plan?" hai lần, lúc nhận yêu cầu và lúc viết plan; flow chỉ cân một lần lúc nhận. Chạy tiếp một bản nháp ở phiên sau, lite vẫn cân lại; lite không chép cách flow bỏ qua bước cân này (`sh-A2`).
- Lần chạy mốc của lite diễn ra mỗi lượt, ngay trước thay đổi đầu tiên, và ghi vào file plan. Test đỏ mới mà thay đổi không gây ra thì chỉ báo lại. Flow ghi mốc một lần vào iflow.md.
- Lite không có mục "Tests from i:test" và không tự gọi i:test.

Mỗi lần đổi một đoạn bên flow mà lite có bản chép, hãy ghi một dòng vào danh sách dưới đây. Đồng bộ xong thì xóa dòng đó.

Hiện chưa có dòng nào: lite đã khớp flow 2.0.0 ở bản 2.0.0.

## Sửa i:gamify

Sau mỗi lần sửa gamify, chạy `skills/gamify/scripts/check-skill.sh`. Script này kiểm cấu trúc của skill mà không tốn API: frontmatter, lời trỏ, tiêu đề các mẫu, tám nhãn của mỗi khung, 18 điều văn phong, 32 điều thiết kế.

- Gamify chạy trong hội thoại chính vì cần `AskUserQuestion`, mà fork không có công cụ này. Đừng thêm `context: fork` vào frontmatter.
- Khung mới thêm vào cuối `references/thu-vien-khung.md`, đủ tám mục có nhãn. Script đếm heading `## Khung N` và soi đủ tám nhãn.
- SKILL.md viết tiếng Anh, các file tham chiếu viết tiếng Việt.
- Giữ SKILL.md của gamify dưới 5.000 token (hiện khoảng 15 KB). Sau khi nén hội thoại, skill không tự đọc lại SKILL.md mà trông vào việc Claude Code tự gắn lại file dưới ngưỡng này; file dài quá ngưỡng thì phần cuối, gồm các luật chung, bị cắt.
