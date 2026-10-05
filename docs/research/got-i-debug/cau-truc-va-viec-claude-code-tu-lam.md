# Cấu trúc của i:debug và những việc Claude Code đã tự làm

Ghi chép lúc rà i:debug ngày 2026-10-05, trên commit `854968e` (bản 1.11.1). Đây là những gì đã thấy, không phải quyết định.

Điểm cấu trúc: 8. Frontmatter hợp lệ và trường nào cũng có việc. Một file 179 dòng là đúng dạng cho skill chạy trong fork. Thân skill không tả lại cách fork chạy. Ngoài một câu ("Everything below is a delta from your defaults"), không câu nào chỉ lặp việc model vốn tự làm.

## Frontmatter

- **Không có trường `agent:`**, nên skill chạy như agent general-purpose, có mọi công cụ dành cho subagent. Không subagent nào có `AskUserQuestion` hay `EnterPlanMode`, nên debug không hỏi được người dùng. Mọi chỗ hở phải trả về bên gọi.
- **`background: false` là trường thật.** Nó chỉ đi với `context: fork`, mặc định là `true`, cần Claude Code từ bản 2.1.218. Nó bắt lượt gọi chờ kết quả và giữ đủ bộ công cụ. Cần giữ, vì flow và lite gọi debug "trước khi sửa" và cần câu trả lời ngay trong lượt đó.
- **`argument-hint`** chỉ hiện lúc gõ lệnh. Tài liệu không nói model có thấy nó hay không (chưa kiểm được). Vì vậy câu cuối của description ("pass the symptom, how to see it…") là chỗ duy nhất chắc chắn đến được model gọi skill, và phải giữ.
- **Description** dài 1.031 ký tự. Claude Code cắt danh sách skill ở 1.536 ký tự nên không bị cắt. Đặc tả Agent Skills ghi giới hạn 1.024. Cụm "from an independent context" lặp ý "Runs in a fresh fork" ở cuối. Bỏ cụm đó tiết kiệm khoảng 7 token mỗi lượt nhưng phải đo lại trigger, nên chưa đáng làm.

## Fork nhận được gì

Fork không nhận lịch sử chat. Nó nhận thân skill (đã thay `$ARGUMENTS` bằng đối số), system prompt của general-purpose, mọi tầng CLAUDE.md (kể cả `~/.claude/CLAUDE.md` và các rule của người dùng), ảnh chụp git status, và các skill qua công cụ Skill. Nó không nhận output style và auto memory. Vì vậy luật báo cáo của debug phải tự đứng được, không trông vào output style của người dùng.

## Hai chỗ cấu trúc làm báo cáo sai

- **`$ARGUMENTS` xuất hiện hai lần** (dòng 25 và dòng 137). Claude Code thay chỗ giữ chỗ này bằng toàn bộ đối số, nên đối số bị dán hai lần vào prompt. Lần thứ hai rơi ngay giữa câu phân biệt ngôn ngữ của người gọi với ngôn ngữ của log được dán vào. Khi flow hay lite gọi, đối số mở đầu bằng cả đoạn log đỏ.
- **Status thiếu giá trị cho bốn kết cục.** Khi hành vi khớp cam kết ("không phải lỗi"), báo cáo không có giá trị Status nào, và câu "in one line and end" đọc thành chỉ một dòng, không nguồn, không phép đo. Ở ba chế độ nhẹ hơn (chỉ tái hiện, tìm commit đầu tiên gây lỗi, xét một nghi phạm), "proven" không nói đã chứng minh cái gì, nên bên gọi hiểu thành đã chứng minh nguyên nhân.

## Trông như lặp việc có sẵn nhưng nên giữ

- "Never guessed": fork không có lịch sử chat, nên đoán là việc nó sẽ làm nếu không bị cấm.
- Đo diff từ điểm còn tốt trước mọi thứ: fork nhận git status nhưng không nhận diff, và thói quen của model là đọc code trước.
- Bisect trong worktree riêng có kiểm đỏ/xanh trước: để tự nhiên, model bisect ngay trong cây đang sửa dở của bên gọi.
- "Symptom disappearing is not proof" và phép "trả lại": mặc định là dừng ở thay đổi đầu tiên làm triệu chứng biến mất.
- "Nơi trạng thái sai được tạo ra": mặc định là thêm một chốt kiểm ở chỗ crash.
- Bốn lệnh git và cấm `checkout`/`restore`/`stash`: checkpoint của Claude Code không che thay đổi qua Bash, còn `/rewind` là công cụ của người dùng chứ không phải của fork.
- "No ledger, no case IDs": chính ví dụ prompt nghiên cứu của Anthropic bảo Claude giữ file ghi chép giả thuyết, mà file đó sẽ làm hỏng phép so cây làm việc lúc báo cáo.
- "Never weaken, skip or rewrite a check": Anthropic ghi nhận Claude đôi khi quá chú tâm làm cho test qua.

## Nguồn

code.claude.com/docs/en/skills; code.claude.com/docs/en/sub-agents; platform.claude.com, mục agent-skills best-practices và prompting best-practices (official, đọc 2026-10-05 qua agent). Chuyện `$ARGUMENTS` bị thay ở mọi chỗ xuất hiện là suy từ biểu thức thay thế trong bản 2.1.289; tài liệu không nói rõ.
