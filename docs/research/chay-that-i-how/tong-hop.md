# i:how đã được chạy thật những ca nào, và ra sao

File này dành cho người sắp đánh giá hay sửa i:how mà chưa xem cuộc trao đổi lúc dựng nó. Ngày 05/10/2026, i:how được chạy thật chín lần trên chính repo plugin này. Lần nào nó cũng chọn đúng thứ cần giảng, và lần nào repo cũng y nguyên sau khi chạy. Nguyên văn câu trả lời của từng lần nằm trong thư mục `cau-tra-loi/`. Trang HTML mà skill dựng ở ca 6 là `trang-luong-hook.html`, ảnh chụp trang là `trang-luong-hook.png`.

Mỗi lần chạy là một phiên `claude -p` riêng, nạp plugin từ cây làm việc của repo và tắt bản plugin đã cài. Cách chạy lại nằm ở gần cuối file.

## Kết quả từng ca

| Ca | Hỏi gì, trong tình trạng nào | Mong đợi | Kết quả |
|---|---|---|---|
| 1 | Hỏi "vừa làm gì?" khi repo đang có phần i:how chưa commit, cùng các thư mục nháp `backup/` và `docs/` chưa được git theo dõi. | Skill giảng phần i:how, các thư mục nháp chỉ được nhắc một dòng. | Đúng như mong đợi. Skill còn chỉ ra README ghi "Reads only" trong khi skill được phép ghi trang và ghi bài giảng khi người dùng xin. |
| 2 | Hỏi "vừa làm gì?" trên bản sao sạch, commit cuối là `854968e`. | Skill giảng commit `854968e`. | Đúng như mong đợi. Skill đối chiếu commit với file plan rà soát và thấy commit đã bỏ mất luật "vùng dữ liệu riêng" của test E2E mà plan cảnh báo. |
| 3 | Cố ý trả lời sai câu hỏi cuối của ca 2, trong cùng phiên. | Skill chỉ ra chỗ hiểu lệch, giảng lại bằng ví dụ khác, rồi hỏi câu mới cùng kiểu, không khen không chê. | Đúng như mong đợi. Skill tách phần đúng và phần sai, giảng lại bằng ví dụ nhờ thợ xem xe còn thiếu đồ bảo dưỡng gì, rồi hỏi một câu so sánh hai lệnh. |
| 4 | Hỏi luồng của hook nhắc việc dở, bản skill đầu tiên. | Skill dựng trang vì luồng có nhiều nhánh. | Bài giảng đúng và tự chạy hook thật trong năm tình huống, nhưng không dựng trang. Luật dựng trang được sửa sau ca này. |
| 5 | Hỏi về phần thanh toán Stripe, thứ repo không có. | Skill nói đã tìm gì, ở đâu, rồi xin gợi ý. | Đúng như mong đợi. Skill liệt kê bảy từ khóa đã tìm trong code và lịch sử git, rồi xin đường dẫn project hoặc tên màn hình. |
| 6 | Hỏi lại luồng của hook sau khi sửa luật dựng trang. | Skill dựng trang và chỉ tóm tắt ngắn trong chat. | Đúng như mong đợi. Trang chia cột theo năm bên tham gia, có ô ba nhánh rẽ, bấm vào bước nào thì mở code thật và lý do. Chat chỉ có tóm tắt, đường dẫn trang và một câu hỏi. |
| 7 | Hỏi "commit vừa rồi" khi repo đang có phần i:how chưa commit. | Skill giảng commit cuối, không giảng phần đang sửa dở. | Đúng như mong đợi. Skill tự đọc lịch sử phiên cũ và tìm ra lý do thật của commit. Lúc đó skill chưa có luật nào về nguồn này, nên luật được thêm sau ca này. |
| 8 | Hỏi riêng một dòng code, dòng 32 của hook. | Skill trả lời ngay, không độn thành bài dài vô ích. | Đúng như mong đợi. Hai câu đầu trả lời thẳng. Skill chạy thử và tìm ra con số 200 tính cả nhãn `Next action: `, và chạy ở locale `C` thì hàm cắt đôi một chữ tiếng Việt. |
| 9 | Hỏi "vừa làm gì?" ngay trong phiên Claude vừa đổi giới hạn cắt dòng, trên cây có sẵn một dòng ghi chú cũ trong README. | Skill giảng phần Claude vừa sửa, ghi chú cũ chỉ được nhắc một dòng. | Đúng như mong đợi. Skill nói rõ dòng README "đã có trước khi tôi bắt đầu". Nó còn phát hiện chú thích trong `tests/run.sh` vẫn ghi "200" và không test nào giữ con số đó. |

## Những điều các lần chạy cho thấy

**Tìm đúng thứ cần giảng.** Bốn tình huống của câu "vừa làm gì" đều ra đúng: có thay đổi chưa commit, cây sạch, hỏi "commit vừa rồi" khi đang có thay đổi, và cây lẫn thay đổi cũ với thay đổi mới. Ở ca 9, skill dùng hội thoại để tách thay đổi cũ ra, dù vẫn tự chạy `git status` và `git diff`. Nhờ tự chạy lại, nó thấy chú thích test đã cũ, điều mà hội thoại không hề biết.

**Lý do có ghi nguồn.** Mỗi lý do đều kèm nơi lấy ra: commit message, chú thích trong file, file plan, hoặc "tôi suy ra từ code". Khi không có ghi chép, skill nói thẳng là không có. Ví dụ ở ca 8 và 9, con số 200 có từ commit đầu tiên `3d96a15` và không ai ghi vì sao chọn số đó.

**Chạy thật thay vì đoán.** Ở các ca về hook, skill dựng một repo mẫu trong thư mục tạm, chạy hook thật rồi đưa output thật vào bài. Mỗi khẳng định được đánh dấu "đã chạy" hay "đọc từ code". Lần nào `git status` trước và sau cũng giống nhau.

**Vòng hỏi.** Bài nào cũng kết bằng đúng một câu hỏi mở thuộc loại đoán trước kết quả. Ca 3 cho thấy khi người dùng trả lời sai, skill sửa đúng chỗ hiểu lệch thay vì giảng lại từ đầu.

**Độ dài và chi phí.** Bài giảng trong chat dài từ khoảng 770 chữ (một dòng code) đến 1.600 chữ (một commit sửa nhiều luật). Khi có trang thì chat chỉ còn khoảng 300 chữ. Mỗi lần chạy mất từ 6 đến 21 lượt, tốn từ 0,3 đến 1,5 USD. Lần 21 lượt là ca 7, ca đọc lịch sử phiên cũ.

## Những gì chưa được chạy

- Công cụ Artifact chưa được thử. Các phiên `claude -p` không có công cụ này, nên ca 6 đi đường dự phòng là ghi file HTML vào thư mục tạm.
- Chưa có ca nào ra nhiều ứng viên để skill hỏi lại bằng `AskUserQuestion`. Công cụ này cũng không chạy được trong `claude -p`.
- Chưa thử trên nhánh phụ, chưa thử một thay đổi lớn tới mức skill phải đưa mục lục trước, và chưa thử ghi bài giảng vào `docs/how/` khi người dùng xin giữ lại.
- Ngoài ca 3, chưa chạy trọn một vòng hỏi nhiều lượt cho tới khi người dùng kể lại toàn bộ.

## Cách chạy lại

Chạy từ thư mục của repo cần hỏi, thay câu hỏi cho phù hợp:

```
env -u CLAUDECODE claude -p "/i:how vừa làm gì vậy?" --output-format json --max-turns 60 \
  --plugin-dir /home/neki/projects/personal/claude-plugin-iflow \
  --settings '{"enabledPlugins":{"i@iflow":false}}' \
  --allowedTools "Bash(git:*)" "Read" "Grep" "Glob" "Bash(ls:*)" "Bash(grep:*)"
```

Ca dựng trang cần thêm `"Write" "Bash(bash:*)" "Bash(mktemp:*)" "Bash(mkdir:*)" "Bash(cat:*)"` để skill ghi được trang và chạy hook trên repo mẫu. Muốn trả lời câu hỏi của skill thì chạy tiếp bằng `--resume <session_id>`, lấy `session_id` từ output JSON của lần trước. Các ca trên bản sao sạch dùng `git clone` của repo vào thư mục tạm.

## Bản skill mỗi ca đã nạp

Skill được sửa giữa các lần chạy, nên mỗi ca nạp một bản khác nhau:

- Ca 1 đến 5 chạy trên bản viết đầu tiên. Sau các ca này, agent đọc bằng mắt người lạ tìm ra sáu chỗ cần sửa: luật chọn thay đổi chưa commit, file plan của repo khác, điều kiện dựng trang, cách kết thúc vòng hỏi, số phần tối thiểu, và vị trí của ví dụ.
- Ca 6 và 7 chạy trên bản đã có sáu chỗ sửa đó, nhưng chưa có dòng cho phép đọc lịch sử phiên cũ.
- Ca 8 và 9 chạy trên bản của commit `8601457`. Tính đến commit `e05b658`, i:how chưa đổi gì so với bản này.
