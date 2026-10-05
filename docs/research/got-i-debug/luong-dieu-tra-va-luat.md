# Luồng điều tra và luật của i:debug, thử qua sáu lần chạy

Ghi chép lúc rà i:debug ngày 2026-10-05, trên commit `854968e` (bản 1.11.1). Số dòng tính theo `skills/debug/SKILL.md` lúc đó. Đây là những gì đã thấy, không phải quyết định.

Điểm: luồng 6, luật 7. Thứ tự điều tra (ghi kỳ vọng trước, rồi xem cái gì đã đổi, rồi tái hiện, rồi chứng minh hai chiều) chạy tốt với test đỏ và với lỗi do flow hay lite chuyển sang. Với lỗi production và lỗi trên máy người dùng thì vấp. Các luật phòng thủ nhắm đúng chỗ và đáng giữ.

## Debug được gọi cho loại lỗi nào

Không luật nào trong thân skill có sự cố hay bài đo đứng sau. `evals/debug.json` chỉ đo skill có được mở không, và lần chạy bị cắt ngay khi skill được gọi, nên thân skill chưa bao giờ được chạy thử. Hai lần sửa luật có ghi nguồn gốc đều đến từ các lượt rà, không phải từ lần chạy thật.

Vì vậy "hay gặp" ở đây được đoán theo 11 câu đo "nên mở". Năm câu là lỗi production hay dịch vụ. Hai câu là máy của người dùng (bộ gõ fcitx5 trong WezTerm, Edge tự tắt). Một câu là test chập chờn trên CI, một câu nêu sẵn nghi phạm (Redis), một câu là "hỏng từ hôm qua", một câu là job báo chạy xong mà không để lại gì. Chỉ một câu là test đỏ có runner. Trong khi đó thân skill viết quanh test đỏ và git.

## Sáu lần chạy đã thử

1. "Test `checkout.spec` đỏ từ hôm qua, hôm kia còn xanh."
2. Flow chuyển sang một test đỏ mà thay đổi của phần việc không giải thích được.
3. Lite chuyển sang, từ một lượt làn nhanh có nhiều giả định đã duyệt.
4. Chỉ có log: "khách báo đơn hàng bị trừ tiền hai lần".
5. "Trang dashboard chậm, tuần trước còn nhanh."
6. "Từ hôm qua bộ gõ tiếng Việt không gõ được trong terminal."

## Chỗ hở và chỗ vướng

- **Hai câu tự mâu thuẫn về điểm còn tốt (lần 1, 5, 6).** Một câu bảo đọc diff từ lúc còn tốt trước mọi thứ khác. Câu sau bảo diff chỉ dùng khi điểm tốt đã đo được. "Hôm kia còn xanh" là nhớ chứ chưa đo, nên model phải đoán. Cụm "the working tree against HEAD when the tree is dirty" còn đọc được thành "chỉ xem cây làm việc", bỏ qua commit hôm qua. Lần deploy, gói cài hay cấu hình máy thì không hiện trong git.
- **Thu nhỏ test trước khi dùng diff (lần 1–3).** Mỗi lần thu nhỏ là một lần sửa file test của bên gọi rồi phải hoàn nguyên, trong khi diff hai ngày thường đã khoanh vùng xong.
- **Không phát lại được từ log (lần 4).** Luật chỉ cho tái hiện tại chỗ khi một input hay một request gây ra lỗi. Trừ tiền hai lần đến từ retry hay hai request đồng thời, nên debug bỏ qua cách phát lại rẻ trong môi trường cô lập và chỉ báo giả thuyết.
- **Hai lối ra cho cùng một trạng thái (lần 4).** Hàng "chỉ có log" trong bảng và đoạn "không tái hiện được" đều kết thúc bằng giả thuyết, nhưng nói theo hai cách. Model không rõ bước "đo những điều kiện khác nhau giữa nơi hỏng và ở đây" có áp dụng không.
- **Máy của người dùng không được che (lần 6).** Luật cấm thử trên "hệ thống thật hay dữ liệu dùng chung". Máy người dùng không thuộc hai loại đó, nên fork có thể khởi động lại fcitx5, sửa dotfile hay hạ cấp gói. Ảnh chụp bốn lệnh git để hoàn nguyên thì không che những thứ này.
- **Con số chỉ hồi một phần (lần 5).** Bỏ truy vấn N+1 đưa trang từ 4,2 s về 1,5 s, trong khi tuần trước là 0,8 s. "Giải thích mọi phần của triệu chứng" được đọc theo phần chứ không theo độ lớn, nên báo "đã chứng minh" và 0,7 s còn lại không ai nhắc.

## Phân loại từng luật

| Luật | Phân loại |
|---|---|
| Đối số, "không bao giờ đoán" | Đáng giữ: fork không có lịch sử chat |
| Hỏi ít hơn nguyên nhân thì dừng ở đó | Đáng giữ (câu đo Redis) |
| Việc sửa là của bên gọi; không thay đổi gì vĩnh viễn | Đáng giữ, phòng thủ |
| "Everything below is a delta from your defaults" | Không đổi kết quả nào |
| Ghi kỳ vọng trước, cắt theo thời gian | Đáng giữ, nhưng tự mâu thuẫn (xem trên) |
| Nguồn kỳ vọng | Đáng giữ |
| Thứ bậc nguồn | Hiếm, nhưng giữ: chặn một kết quả sai người dùng không thấy |
| Chỗ hở và lệnh chạy tiếp | Đáng giữ: fork không hỏi được |
| Khớp cam kết thì không phải lỗi | Đáng giữ |
| Bảng "đã có gì trong tay", bốn hàng đầu | Đáng giữ |
| Hàng "quy trình người làm bị sai" | Hiếm: không câu đo nào thuộc loại này |
| Không tái hiện được | Đáng giữ, nhưng lối ra trùng hàng "chỉ có log" |
| Không có triệu chứng nào | Hiếm: chỉ chạy khi gọi `/i:debug` trống; nhưng là chỗ duy nhất cấm quét cả repo |
| Chỉ thử ở nơi đảo ngược được, cô lập | Phòng thủ, đáng giữ |
| Dụng cụ của chính hệ thống trước, `/run` | Đáng giữ |
| Câu profiler/debugger | Nói khi nào được dùng dụng cụ ngoài; giữ |
| Bisect trong worktree riêng, kiểm đỏ/xanh trước | Phòng thủ, đáng giữ |
| Bỏ ra rồi trả lại | Đáng giữ: phép duy nhất tách nguyên nhân khỏi trùng hợp |
| Giải thích hết mọi phần; nguyên nhân có thể là một nhóm | Đáng giữ |
| Chỉ nơi trạng thái sai được tạo ra | Đáng giữ |
| Ảnh chụp bốn lệnh git và hoàn nguyên đúng chữ | Phòng thủ: giữ thay đổi chưa commit của bên gọi |
| Danh sách dòng báo cáo, bằng chứng | Chữ cho người đọc: chỉ thắt lại |
| Bước kế tiếp | Đáng giữ |
| Khối "Never" | Đáng giữ: mỗi luật chặn một lỗi điều tra hay gặp |

## Nên giữ dù trông nặng

- Ảnh chụp bốn lệnh git và cách hoàn nguyên đúng chữ: flow và lite không commit giữa chừng, nên phép thử "bỏ ra" sửa đúng vào phần việc chưa commit của bên gọi.
- Bisect trong worktree riêng, kiểm đỏ ở đầu hỏng và xanh ở đầu tốt trước: worktree không có dependency đã cài thì mọi commit đều ra "hỏng".
- Tên công tắc (cờ, cấu hình, rollback) chỉ được nêu ra, không bao giờ tự bật trên hệ thống thật.
- "Tắt cache chứng minh nguyên nhân nhưng không sửa gì": chặn việc đưa một dụng cụ đo thành bản sửa.
- Đo qua N lần, và "đã loại" nghĩa là loại qua N lần: lỗi chập chờn và lỗi chậm.

## Nguồn

Đọc trực tiếp `skills/debug/SKILL.md`; `git log -p -- skills/debug`; `evals/debug.json`, `evals/smoke.json`; transcript lượt rà cũ của commit `27e8926` (primary).
