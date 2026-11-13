# Vòng lặp vẽ của i:cad

Thư mục này giữ mọi thứ để thử i:cad trên đề thật và đổi skill theo đợt.
Bắt đầu từ [quy trình đợt](quy-trinh-dot.md): nó nói khi nào chạy, khi nào
sửa, khi nào giữ hay bỏ một đợt sửa.

- [prompt.md](prompt.md): prompt cho agent dựng bản vẽ. Thay `{SKILL}` bằng
  đường dẫn `skills/cad`, `{WORK}` bằng một thư mục tạm mới, `{BRIEF}` bằng
  nội dung một file đề.
- [review.md](review.md): phiên chính duyệt một vòng và ghi lỗi vào sổ.
- [so-quan-sat.md](so-quan-sat.md): sổ quan sát, mỗi lỗi một dòng.
- [thang-chung.md](thang-chung.md): thang điểm chung cho mọi đề;
  [cham.md](cham.md) là prompt cho agent chấm; `diem_may.py` chấm phần máy.
- [bang-diem.md](bang-diem.md): điểm theo phiên bản skill.
- [de/](de/README.md): bộ đề luyện và bộ đề giữ riêng.
- [rounds.md](rounds.md) và [cham-quinta-monroy.md](cham-quinta-monroy.md):
  lịch sử chín vòng đầu, chạy theo nhịp cũ (sửa sau mỗi vòng).

Đề trong thư mục này chỉ là đề có đủ số để làm phương án mà không phải hỏi
lại. Không đưa vào đây số đo chép từ bản vẽ của một công trình có thật, kể cả
khi bản vẽ đó dùng để so cách vẽ.
