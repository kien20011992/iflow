# i:explore so với i:flow và i:lite

Ghi chép lúc rà i:explore ngày 2026-09-29, trên bản 1.5.0 của plugin. Số dòng tính theo file lúc đó. Đây là những gì đã thấy, không phải quyết định. Quyết định cuối cùng và các mục đã sửa nằm trong commit nâng i:explore lên bản 1.6.0.

Việc đối chiếu gồm hai phần. Phần thứ nhất: hồ sơ explore ghi ra có đúng dạng flow và lite đọc được không. Phần thứ hai: những luật chung ý có đi cùng hướng không. Chủ plugin đã quyết hai điều. Một: mỗi skill đứng riêng, không dùng module chung. Hai: chỗ explore giống flow mà đi hướng khác thì sửa theo flow, chỗ giống hệt thì bỏ qua.

Điểm: 6.

**Giống hệt flow, bỏ qua:**

- Đường dẫn hồ sơ trong repo tính từ gốc git.
- Thứ tự tìm hồ sơ: đường dẫn người dùng đưa, rồi hồ sơ đang mở trong hội thoại, rồi tìm theo chủ đề, hỏi khi có nhiều bản khớp.
- Tiếp tục hồ sơ cũ: đọc trước, không hỏi lại điều đã ghi.
- Bậc nguồn, luật con số, và luật để lộ nguồn mâu thuẫn. Explore tra rộng hơn một chút, và đó là cố ý, vì chủ đề đời sống cần.
- Hỏi để hiểu thì tự do. Xin quyết thì phải trải đủ nghĩa, được mất, và khả năng quay lại của từng nhánh.
- Người dùng chọn vùng mở tiếp, model chỉ đề xuất kèm lý do.
- Hồ sơ đặt phần cho người đọc lên trước, khối trạng thái xuống cuối.
- Đủ rõ để flow tách phần đã xác nhận khỏi phần chưa xác nhận.
- i:debug chỉ đường sang i:explore đúng một dòng.

**Giống mà đi hướng khác, sửa theo flow:**

| Chỗ | Flow làm gì | Explore đang làm gì |
|---|---|---|
| Lúc ghi file | Ghi mỗi điều ngay khi nó chốt | Đợi đến "mốc"; hồ sơ chỉ có từ mốc đầu |
| Chỗ để ngoài git | Dùng thư mục đang mở | Hỏi người dùng |
| Sau khi nén hội thoại | Đọc lại file tham chiếu và file đang làm | Không có luật |
| Dùng agent | Không truyền `name`, tối đa ba, kết quả vào file, thử lại một lần | Chỉ nói "hướng độc lập" |
| "Anh chọn giúp" | Là quyết định giao quyền, ghi lại, chọn công khai | Không có luật |
| Cái gì tính là xác nhận | Lời đồng ý hoặc lệnh; câu hỏi, lưỡng lự, lời khen, im lặng thì không | Chỉ nói "im lặng không phải đồng ý" |
| Bàn vòng vòng | Hai lượt không đổi được gì → hỏi ba nhánh | Câu hỏi bị lờ hai lần → lặng lẽ thành ẩn số |
| Trước khi chốt | Một lượt đọc như người lạ, tìm vùng còn thiếu | Không có |
| Trải phương án | Các nhánh khác góc nhìn, kể cả không làm hay chờ | Không yêu cầu |
| Chỉ đường sang skill kia | Một dòng: lý do, rồi lệnh cho người dùng gõ | Không có |
| Chữ riêng của skill | Chỉ dùng trong file skill, ra chat thì nói lời thường | Không có luật |
| Tên mục trong tài liệu | Theo ngôn ngữ người dùng, nói mục chứa gì | "headings adapted to the subject" |
| Dòng vị trí cuối lượt | Điều vừa đổi, vùng còn mở, đề xuất | Đường đã đi, vùng còn mở, đề xuất |

Chỗ i:lite `fast` không đọc hồ sơ explore được giải bằng câu chỉ đường mới ở cuối cuộc khám phá: đường dẫn hồ sơ nằm ngay trong lệnh người dùng gõ. Không phải sửa lite.

Chữ không ai đọc: câu "tài liệu hạ nguồn phải giữ cờ" (dossier.md:100), và hai trường `skill:`, `primary_domain:`.

Tình huống hiếm, mặc định loại: mở phiên từ thư mục con; lite chuyển sang explore khi plan mode đang bật; flow đọc nhầm một khuyến nghị thành phát hiện đã xác nhận.
