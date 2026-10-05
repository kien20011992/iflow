# i:debug so với i:flow, i:lite và i:test

Ghi chép lúc rà i:debug ngày 2026-10-05, trên commit `854968e` (bản 1.11.1). Số dòng tính theo `skills/debug/SKILL.md` lúc đó. Đây là những gì đã thấy, không phải quyết định. Các mục đã sửa nằm trong cùng lượt sửa i:debug, ghi ở file plan của lượt đó.

i:debug được sửa lần cuối ngày 28/9 (commit `2a8e122`). Từ 29/9 đến 5/10, flow, lite và test qua các đợt gọt và đổi khá nhiều chỗ mà debug cũng có: cách viết báo cáo, cách trình bằng chứng, cách chuyển việc sang skill khác, cách đọc hồ sơ của bên gọi. Việc đối chiếu hỏi một điều: chỗ nào debug dùng toàn phần hay một phần luật của mấy skill kia mà đã bị bỏ lại. Chỗ giống hệt thì bỏ qua.

Điểm: 5. Chỗ nối thì chạy được: flow và lite truyền sang những thứ debug đọc được, và báo cáo của debug có đủ bốn thứ hai bên ghi lại (trạng thái, nguyên nhân hoặc chỗ hở, cách tái hiện, bằng chứng quyết định). Nhưng mọi đoạn về báo cáo, bằng chứng và chuyển việc đều viết trước các đợt gọt.

## Đã khớp, bỏ qua

- Lời gọi của flow (`/i:debug <the red output · the proof it breaks · the dossier's shape.md path · the active slice file>`, flow SKILL.md:189-191) và của lite (`/i:debug <the red output · the proof it breaks · the active plan file>`, lite SKILL.md:151-152) đều cho debug đủ thứ nó cần.
- Debug viết báo cáo bằng ngôn ngữ người gọi, giống test.
- Khi bị chặn, debug trả lại đúng lệnh `/i:debug <…>` để chạy tiếp, cùng cách với `/i:test <…>`.
- Luật "so cây làm việc với HEAD khi cây đang có sửa đổi" đặt thay đổi của phần việc vừa làm lên đầu. Test có luật phạm vi khác ("cây làm việc cộng các commit từ nhánh mặc định"), nhưng chép sang debug sẽ làm mất đúng cái ưu tiên đó, nên không chép.

## Bị bỏ lại sau các đợt gọt

| Chỗ | Bên kia làm gì bây giờ | Debug đang làm gì |
|---|---|---|
| Báo cáo | test bắt nói bằng lời thường, nhãn là vai trò chứ không phải tiêu đề, từ riêng của skill nói bằng nghĩa của nó (test SKILL.md:189-192) | Chỉ quy định ngôn ngữ; nhãn tiếng Anh như "Gap", "commitment" lọt vào câu trả lời tiếng Việt |
| Thứ tự báo cáo | test và lite để điều quan trọng nhất lên đầu | Nguyên nhân đứng thứ sáu, sau triệu chứng, nguồn kỳ vọng, cách tái hiện, những gì đã loại |
| Bằng chứng | flow và lite: lệnh kèm dòng kết quả chính, không dán log | "the real output of the commands", dễ thành dán nguyên log |
| Chuyển việc | flow đẩy việc vừa một plan về `/i:lite` (flow SKILL.md:88-95); explore chọn giữa `/i:lite` và `/i:flow` | Mọi bản sửa lớn và mọi mong muốn tính năng đều sang `/i:flow`, nên người dùng mất một lượt bị đẩy về `/i:lite` |
| Đọc hồ sơ bên gọi | test bỏ câu "return those same items" ở commit `c574d59` | Vẫn giữ, mời chép lại bức tranh, quyết định, mục tiêu phần việc vào mọi báo cáo; luật chỉ đọc bị viết hai lần |
| Phần chưa phủ | test: liệt kê như việc người dùng quyết, không bao giờ nói là đủ | "said there, never implied covered", để bên gọi tự quyết lặng lẽ |
| Gọi i:test | test nhận `<scope · intent · criteria>`, chỉ tính test mà lệnh test thường bắt phải qua và khẳng định trọn kỳ vọng | Truyền chữ nội bộ "oracle", không truyền nguồn của kỳ vọng, và một test có liên quan lỏng lẻo cũng đủ chặn lời gọi |

## Một chỗ hở mới thấy khi đối chiếu

Khi không có gì nói hành vi đúng là gì, debug dừng và đưa lệnh `/i:debug <symptom · expectation>` để chạy tiếp. Debug do model tự gọi được, nên hội thoại gọi có thể tự điền "expectation" rồi gọi lại. Làm vậy thì lách qua luật thứ bậc nguồn kỳ vọng, và debug "chứng minh" một lỗi theo kỳ vọng mà người dùng chưa từng nói. Người dùng sẽ không nhận ra. Test đặt chỗ hở cùng loại thành câu hỏi người dùng phải trả lời (test SKILL.md:182-183). Đặt như vậy còn làm flow dừng tự chạy tiếp, vì flow chỉ dừng khi cần người dùng quyết.

## Gọi từ i:lite

Plan của lite không có đoạn mục tiêu phần việc như hồ sơ flow. Kết quả người dùng đã duyệt nằm ở phần "plan sẽ đổi gì và biết nó chạy đúng bằng gì". Ở làn nhanh, bức tranh mỏng, và phần lớn lựa chọn nằm trong các giả định đã duyệt. Nếu debug chỉ đọc bức tranh và quyết định, một lỗi ở hành vi được giả định sẽ thành báo "bị chặn, không có kỳ vọng" sai.

## Chờ i:how

Debug chuyển "hiểu nhầm" sang i:explore. Một "lỗi" hoá ra là thiết kế thường là hiểu nhầm code của chính repo, mà i:explore tự loại việc trong repo. Skill mới `skills/how/` (chưa commit lúc ghi) dạy cách code repo chạy. Khi nó vào repo, lối này nên chuyển sang `/i:how`.

## Nguồn

Đọc trực tiếp `skills/flow/SKILL.md`, `skills/lite/SKILL.md`, `skills/test/SKILL.md`, `skills/debug/SKILL.md`; `git log -p --since=2026-09-24 -- skills/flow skills/lite skills/test` (primary).
