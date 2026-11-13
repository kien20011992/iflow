# Vòng lặp vẽ của i:cad

Ba bước lặp lại tới khi bản vẽ không còn chỗ hỏng do skill:

1. **Thực thi.** Một agent chưa thấy hội thoại dựng bản vẽ theo skill. Prompt là `prompt.md`, thay `{SKILL}` bằng đường dẫn `skills/cad`, `{WORK}` bằng một thư mục tạm mới, `{BRIEF}` bằng nội dung một file đề bài trong thư mục này.
2. **Duyệt.** Phiên chính làm theo `review.md` trên chính file agent dựng.
3. **Sửa.** Sửa đúng chỗ theo loại lỗi, chạy `tests/cad.sh`, ghi một dòng vào `rounds.md`.

Đề bài trong thư mục này chỉ là đề có đủ số để đi thẳng tới bản vẽ. Không đưa vào đây số đo chép từ bản vẽ của một công trình có thật, kể cả khi bản vẽ đó dùng để so cách vẽ.
