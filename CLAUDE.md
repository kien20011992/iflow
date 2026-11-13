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

Ngoài hook và checker, i:debug, i:test và i:how cũng đọc hồ sơ của i:flow. Mỗi thư mục nhiệm vụ mang một id ngắn ở đuôi tên (`<việc>-a7f3`, bốn ký tự hex từ `openssl rand -hex 2`), và chỉ khi người dùng gọi tên nhiệm vụ đó thì skill khác mới ghi vào cùng thư mục, không skill nào tự đoán "cùng việc" để chui vào. Khi được gọi, i:lite ghi `research/`, i:explore ghi `explore/`, i:how ghi `how/`, i:gamify ghi `game/`, i:cad ghi `cad/`; đổi tên một thư mục con hay cách đặt tên thư mục thì sửa skill ghi nó và state.md §1. Ba skill này đọc theo vai trò các mục: bức tranh, quyết định, charter, plan đã duyệt, kết quả, ghi chú, và các cột của bảng slice. Đổi vai trò hay tên một mục thì phải xem lại cả ba skill. i:how còn đọc khối kết quả mà i:lite ghi dưới plan, nên đổi khối đó cũng phải xem lại i:how. i:debug còn đọc bức tranh, phần nói plan sẽ đổi gì, các quyết định và giả định đã duyệt trong file plan của i:lite, nên đổi vai trò các phần đó cũng phải xem lại i:debug.

## i:flow và i:lite độc lập, không đồng bộ

i:lite ra đời từ i:flow nên nhiều đoạn hai bên giống nhau (`references/shape.md`, `agents.md`, luật ngôn ngữ, cổng duyệt, lần đọc lạ, quyết định giữa chừng). Từ 2026-10-07 hai skill chạy song song: sửa một bên thì **không** chép sang bên kia, không có danh sách phải đồng bộ, không có module chung. Mỗi skill tự đứng với file của nó, và được phép đi khác nhau theo thời gian. Muốn một thay đổi có ở cả hai thì sửa cả hai trong cùng commit và nói rõ trong message, đó là việc có chủ ý, không phải nghĩa vụ.

## Sửa i:gamify

Sau mỗi lần sửa gamify, chạy `skills/gamify/scripts/check-skill.sh`. Script này kiểm cấu trúc của skill mà không tốn API: frontmatter, lời trỏ, tiêu đề các mẫu, tám nhãn của mỗi khung, 18 điều văn phong, 32 điều thiết kế.

- Gamify chạy trong hội thoại chính vì cần `AskUserQuestion`, mà fork không có công cụ này. Đừng thêm `context: fork` vào frontmatter.
- Ba file tham chiếu giữ phần chỉ đọc một lần, để hai file đọc đi đọc lại nhẹ đi: `ke-hoach-gamemaster.md` (bước A và mẫu gamemaster, chỉ slice 01), `sau-dungeon.md` (slice `tools.md`, kiểm cuối, sửa và mở rộng), `quan-tro-moc.md` (chấm bài kiểm và qua vùng, vài tuần một lần). Phần đọc mỗi slice ở `vong-slice.md`, phần đọc mỗi lần chơi ở `quan-tro.md`, kể cả luật "khi nào bảo đánh" vì mọi phiên đều cần nó. Đừng gộp lại; check-skill.sh kiểm đủ các mục ở từng file.
- Khung mới thêm vào cuối `references/thu-vien-khung.md`, đủ tám mục có nhãn. Script đếm heading `## Khung N` và soi đủ tám nhãn.
- SKILL.md viết tiếng Anh, các file tham chiếu viết tiếng Việt.
- Giữ SKILL.md của gamify dưới 5.000 token (hiện khoảng 15 KB). Sau khi nén hội thoại, skill không tự đọc lại SKILL.md mà trông vào việc Claude Code tự gắn lại file dưới ngưỡng này; file dài quá ngưỡng thì phần cuối, gồm các luật chung, bị cắt.

## Sửa i:cad

Sau mỗi lần sửa, chạy `tests/cad.sh`: không tốn API, mất vài giây. Nó kiểm các hợp đồng nêu dưới đây, mọi lời trỏ (qua `check-pointers.sh`), và trình kiểm DXF. Trước khi tag bản mới, hoặc sau khi đổi một luật của cad, chạy thêm `tests/cad/run-evals.sh --runs 1`: sáu phiên thật, một lần chạy tốn khoảng 3 đô. Script đó dựng `review.html` trong `evals-cad/results/<thời-điểm>/`, đọc trang này rồi mới kết luận. Trong các file của cad đừng viết lời trỏ kiểu "§N": script sẽ tìm heading `## N.` mà cad không dùng. Trỏ bằng link markdown và tên mục.

- SKILL.md viết tiếng Anh, các file tham chiếu viết tiếng Việt. Giữ SKILL.md dưới 18.000 byte (khoảng 5.000 token; `tests/cad.sh` kiểm con số này, hiện khoảng 16 KB), vì sau khi nén hội thoại Claude Code chỉ gắn lại phần dưới ngưỡng này.
- Cad chạy trong hội thoại chính vì cần `AskUserQuestion` và sống bằng hỏi đáp. Đừng thêm `context: fork`. Đừng thêm `allowed-tools`: quyền cấp qua trường này mất ở tin kế tiếp của người dùng.
- Đừng kèm MCP server của CADCraft hay thư mục `bin/` vào plugin. Server của plugin khởi động ở mọi phiên, nên máy chưa cài CADCraft sẽ thấy lỗi kết nối cả ở phiên chỉ dùng i:flow.
- Skill chưa chứa con số của luật nào: mỗi dự án tự tra luật theo nơi xây, cho tới khi bảng luật có nguồn, ngày đọc và mức chắc ra đời. Lệnh CADCraft chỉ nằm trong thư viện vẽ `skills/cad/lib/` và `assets/dung_mau.py`, đã chạy thật trên bản ghi trong `references/cadcraft.md`; chữ của skill không chép lệnh. Đổi bản CADCraft thì chạy lại `tests/cad.sh` (bài dựng thật) trước khi tin thư viện.
- Mỗi dòng trong `references/cadcraft.md` mang nhãn nguồn: `[tài liệu]`, `[bản X]` hoặc `[chưa thử]`. Khi một phiên chạy thật xác nhận hay bác một dòng, sửa dòng đó và đổi nhãn thành phiên bản đã chạy. Đừng thêm dòng không có nhãn.
- Skill có năm lớp, mỗi lớp một chỗ: chữ quy trình (`SKILL.md`), chữ phán đoán (`references/`), thư viện vẽ (`lib/` với file mẫu và block trong `assets/`, dựng lại bằng `assets/dung_mau.py`), trình kiểm (`scripts/dxf_check.py` cho file với chính nó, `scripts/plan_check.py` cho file với bảng số, `scripts/params_check.py` cho khuôn bảng số `cad-params/1`, `scripts/cua_vao.py` cho phiếu đề bài `cad-brief/1` và mọi đầu vào), và dữ liệu từng dự án. Mỗi trình kiểm có bài tự thử trong `tests/cad/`; thêm một phép kiểm thì thêm một bản có lỗi cài sẵn. Trình kiểm không dùng chung code tính hình với thư viện, kể cả khi hai bên trông lặp nhau: dùng chung thì một lỗi tính hình tự chứng minh mình đúng.
- `build.py` của dự án là bản chép của `lib/build_mau.py`. Một hình sai vì cách vẽ thì sửa hàm, block hay file mẫu kèm bài thử trong `tests/cad/lib_selftest.py`, không thêm câu vào `references/ve.md`. Bài dựng thật `tests/cad/lib_build_test.py` dựng ba bộ mẫu qua CADCraft và chạy cả ba trình kiểm; nó tự bỏ qua trên máy không có CADCraft.
- Skill đổi theo đợt, không vá sau mỗi vòng thử: vòng thử ghi vào `tests/cad/loop/so-quan-sat.md`, đợt sửa theo `tests/cad/loop/quy-trinh-dot.md` và chỉ được giữ khi điểm trên bộ đề giữ riêng (`tests/cad/loop/de/giu-rieng/`, đề thi kín: đừng mở) không tụt theo `tests/cad/loop/thang-chung.md`.
- Chưa có hook hay checker cho `project.md`. Chỉ thêm khi chạy thật cho thấy Claude hay quên đánh dấu `recheck`.

Các ca thử hành vi nằm ở `evals-cad/`, tách khỏi `evals/` để lệnh eval chung của repo không tốn thêm tiền:

- Hai ca `cad-late-fact` và `cad-what-if` dùng chung một dự án dựng sẵn, chép thành hai file `fixture.sh`. Sửa một bên thì sửa bên kia. Đổi một nhãn của khối trạng thái hay một từ trạng thái trong SKILL.md thì sửa cả fixture. `tests/cad.sh` bắt cả hai chỗ lệch.
- Ca mới nên cài một lỗi biết trước, ví dụ nhà rộng hơn đất hoặc phòng không có lối vào, rồi chấm việc Claude có gọi tên lỗi đó không. Đáp án biết trước thì phép chấm không phụ thuộc vào gu của người chấm.
- Tiêu chí cho phép chấm bằng Claude phải nói được bằng một việc cụ thể thấy trong lời đáp. Tiêu chí kiểu "lời lẽ dễ hiểu" cho kết quả nhiễu: người chấm từng coi cả "cửa đi, cửa sổ" là từ chuyên môn.
- Một phép chấm hỏng thuộc một trong ba loại, phân loại xong mới sửa: skill sai, phép chấm sai, hoặc môi trường thử sai. Ví dụ của từng loại: skill liệt kê tên gói cài đặt cho một chủ nhà; một tiêu chí hiểu "số tầng được phép" là hỏi lại "số tầng muốn xây"; phiên thử bị từ chối quyền ghi nên phép chấm "có file dự án" hỏng oan.
- Mỗi ca phải ghi `Write` và `Edit` trong `allowed_tools`, kể cả ca đòi không ghi gì. Thiếu thì lệnh ghi bị từ chối và phép chấm đạt hay hỏng vì lý do không liên quan tới skill.

Những điều chưa được chạy thật khi skill ra đời, xoá từng dòng khi đã kiểm: kích thước có bám hình khi kéo giãn trong AutoCAD không; một file do skill tạo có mở sạch trong AutoCAD không; luật tính lại việc phải làm có trụ được trong một dự án thật không.

Mục "Khi tiền không đủ cho công trình hoàn chỉnh" trong `references/thiet-ke.md` viết từ bản tóm tắt của một bộ quy tắc đã hiệu chuẩn trên ca Quinta Monroy. File gốc của bộ quy tắc đó chưa được đối chiếu. Khi có file gốc, so lại mục này.

Hiệu chuẩn skill bằng một ca có kết quả đã biết thì theo bốn luật, và trạng thái của ca nằm ở thư mục của ca, không nằm trong skill:

1. Agent chạy thử chỉ nhận đề bài và thông tin đầu vào, không nhận kết quả, không mở thư mục chứa bản vẽ gốc.
2. Mọi thứ đưa cho agent làm đầu vào phải suy ra được từ đề bài và tra cứu. Đầu vào chép số từ kết quả thì phép so thành tự chấm bài mình.
3. Kết quả gốc chỉ được chỉ ra chỗ lệch. Hướng sửa skill phải suy lại từ đầu vào và tra cứu. Chỗ lệch thuộc một trong ba loại: skill thiếu hoặc sai luật, agent làm kém, hoặc vùng tự do của bài toán. Loại thứ ba không được vá: đừng ép skill sinh đúng lựa chọn của tác giả gốc.
4. Một luật chỉ được thêm vào skill khi nó đứng được trên vài ca khác loại. Luật chỉ đúng cho một loại công trình thì nằm trong một mục có điều kiện áp dụng ghi rõ.

## Commit và push

Trong repo này Claude tự commit khi xong một thay đổi, không cần hỏi trước. Push thì người bảo trì tự gõ.

Mỗi commit là một thay đổi trọn vẹn, kể được bằng một câu, ví dụ "flow: hook kiểm hồ sơ sau mỗi lần ghi". Đừng commit lặt vặt. Sửa chính tả, viết lại câu vừa thêm, vá chỗ mà `tests/run.sh` hay `check-pointers.sh` vừa báo trong chính thay đổi đó thì gộp vào commit trước bằng `git commit --amend`, không tạo commit mới. Nội dung đã khác thì sửa message theo.

Chỉ amend hay gộp những commit chưa lên remote, tức những commit mà `git log @{u}..HEAD` còn liệt kê. Commit đã push thì để nguyên, vì sửa nó buộc phải force push và lịch sử trên GitHub sẽ lệch với bản đã kéo về máy khác. Commit do người bảo trì tự tạo thì hỏi trước khi gộp hay sửa message.

Trước khi đề nghị push, đọc lại chuỗi commit chưa push như người xem lịch sử sau này. Hai commit cùng nói về một việc thì gộp làm một. Commit cần gộp nằm ngay trước thì dùng amend. Commit nằm xa hơn thì `git commit --fixup <sha>` rồi `git rebase --autosquash @{u}`. Muốn gộp tất cả thành một thì `git reset --soft @{u}` rồi commit lại với message mới. Cả ba cách đều giữ nguyên file, chỉ đổi cách chia commit.

Việc được giao xong, commit đã gọn, test đã chạy thì đề nghị push ngay, không đợi hỏi. In `git log @{u}..HEAD --oneline` và `git diff @{u} --stat`, nói một câu đợt này đổi gì, rồi đưa lệnh để người bảo trì tự gõ, sau đó khởi động lại phiên:

```
! git push origin main && claude plugin marketplace update iflow && claude plugin update i@iflow
```
