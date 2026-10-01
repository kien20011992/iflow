# Đọc lại danh sách sửa i:test như người lạ

Ghi chép lúc rà i:test ngày 2026-10-01, trên bản 1.8.0 của plugin. Sau khi ba lượt soi gom được danh sách sửa, một agent chưa thấy hội thoại đọc lại danh sách đó cùng `skills/test/SKILL.md`. Nó hỏi ba điều: lý do sửa có đúng không, câu mới có làm mất một luật phòng thủ không, và các câu mới có đá nhau sau khi áp tất cả không. Các mục cuối cùng nằm trong commit nâng plugin lên bản 1.9.0.

Bản đầu của danh sách sai ở sáu chỗ. Cả sáu đã được sửa trước khi đưa ra duyệt.

## Sáu chỗ bản đầu làm sai

**Câu phân xử test đỏ để hở đúng cửa nó muốn đóng.** Bản đầu xếp "đọc sai hợp đồng" vào lỗi của test. Thấy test đỏ, model có thể "đọc lại" hợp đồng rồi đổi giá trị mong đợi theo output. Cùng lúc, bản đầu của luật không nới câu kiểm lại cấm luôn việc sửa một câu kiểm mới viết quá tay, ví dụ tự bịa ra đòi lỗi có kiểu. Model chỉ còn hai đường: phạm luật, hoặc giữ câu kiểm bịa và báo nó là lỗi sản phẩm. Qua i:flow thì tệ hơn, vì flow sửa code theo mọi test đỏ của i:test. Bản sửa: test sai là khi chuẩn bị, fixture hay import sai, hoặc giá trị mong đợi đòi nhiều hơn điều căn cứ nói; sửa nó về đúng lời căn cứ, không bao giờ theo output.

**Rút gọn đoạn lỗi import làm mất một điều kiện.** Bản đầu bỏ điều kiện "hợp đồng có nêu module đó". Test import một đường dẫn model tự đoán thì import trần cũng hỏng y hệt, và lỗi bị báo nhầm là lỗi sản phẩm. Qua i:flow, phần việc sẽ tạo ra module cho khớp đường dẫn đoán.

**"Lần chạy sau lần sửa cuối" không nói lần nào.** Lần chạy lại sau timeout cũng là "sau lần sửa cuối". Nếu lần đó xanh, báo cáo ghi qua, và test chập chờn lọt vào bộ test. Bản sửa thêm chữ "đầu tiên".

**"Một vùng dữ liệu riêng" của E2E không trùng chỗ khác.** Dòng 121 chỉ đòi vùng riêng "ở chỗ cần để chạy ổn định". Vùng riêng trong E2E là để bước dọn dẹp không xoá dữ liệu có sẵn, tức luật chặn mất dữ liệu. Bản sửa giữ nó lại.

**Câu tìm phần việc đang chạy dùng hai chữ "none" cho hai thứ,** và hỏi lại cả khi người dùng đã nêu rõ phạm vi. Máy có hai hồ sơ đang chạy thì `/i:test unit src/utils` kết thúc bằng một câu hỏi thừa.

**Hai mục về báo cáo đá nhau.** Một mục bảo nói thay từ riêng của skill, mục kia vẫn liệt kê đúng các nhãn đó. Model sẽ chép nhãn ra. Bản sửa nói rõ các nhãn là vai trò, không phải tiêu đề.

## Hai lỗ ba lượt soi trước bỏ sót

- Với yêu cầu "viết cho đủ cả app", báo cáo "thêm 40 test, xanh" mà không kể phần nào còn chưa có test. Người dùng tưởng đã đủ.
- Bước tìm phạm vi đọc nội dung diff trước khi ghi kết quả mong đợi. Với regression test trên nhánh chính, commit cuối chính là bản sửa bug, nên test sẽ khẳng định đúng cái bản sửa làm thay vì cái đúng.

## Hai điểm chủ plugin quyết

**Lời chú thích trên đầu hàm có được làm căn cứ không.** Lý do nên nhận: với rustdoc, TypeDoc, Sphinx hay godoc, lời chú thích của hàm được export chính là tài liệu công khai được xuất bản. Nhận bản HTML mà từ chối chính chữ đó trong mã nguồn là tự mâu thuẫn. Lý do nên dè chừng: khi i:flow vừa viết một hàm mới kèm chú thích, nhận chú thích đó là để test kiểm code theo lời người viết tự tả, mất đi cái nhìn độc lập của i:test. Chủ plugin chọn đường giữa: nhận, trừ khi chính thay đổi đang được test viết ra lời chú thích đó.

**Chế độ chỉ nhìn từ ngoài.** Bỏ hẳn thì người dùng vẫn có thể ghi "black-box" vào ràng buộc, mà không có luật thì bước tìm rủi ro vẫn đọc thân hàm, và báo cáo không nói ra. Chủ plugin chọn rút còn một câu, giữ lời hứa không lén quay lại đọc code.

## Đề xuất đã cân và không nhận

- Hồ sơ i:flow khác làm căn cứ khi phạm vi nằm ngoài phần việc đang chạy: ca hiếm, cần hai chương trình cùng chạy.
- Đổi chữ "invariant" ở dòng 92–93 và 106: từ quen với model; báo cáo đã được dặn nói thay.
- Thêm câu "lần chạy lại mà xanh thì báo là chập chờn": chữ "đầu tiên" đã chặn.
- `npm ci` xoá các package cài bằng `npm link`, báo cáo tiếng Anh khi lời gọi không có chữ tiếng Việt, bản sửa bug trải nhiều commit: ca hiếm, không đổi.
