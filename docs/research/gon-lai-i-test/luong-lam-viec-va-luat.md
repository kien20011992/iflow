# Luồng làm việc và các luật của i:test

Ghi chép lúc rà i:test ngày 2026-10-01, trên bản 1.8.0 của plugin. Số dòng tính theo `skills/test/SKILL.md` lúc đó. Đây là những gì đã thấy, không phải quyết định. Các mục đã sửa nằm trong commit nâng plugin lên bản 1.9.0.

i:test đi theo thứ tự: tìm phạm vi, ghi kết quả mong đợi trước khi đọc code, đọc code tìm rủi ro, chọn loại test, viết test theo lối của dự án, chạy, rồi báo cáo. Bản rà đi bộ qua ba lần chạy thường:

1. Người dùng gõ `/i:test unit src/utils và src/validators` trong repo Node dùng jest. Biến thể: "thêm regression test cho bug vừa sửa" ngay sau khi sửa, không có hồ sơ i:flow.
2. i:flow gọi i:test giữa một phần việc, truyền đường dẫn hồ sơ, trọng tâm và ràng buộc.
3. "App sắp bàn giao mà chưa có test, viết cho đủ."

## Điểm

| Tiêu chí | Điểm |
|---|---|
| Lời dặn rõ, có lý do | 6 |
| Định dạng đầu ra rõ | 6 |
| Kín trong lần chạy thường | 5 |
| Không thừa, không thiếu | 5 |
| Luồng làm việc với người tự nhiên | 6 |
| Báo cáo dễ hiểu với người đọc | 4 |

Điểm 5–6 nghĩa là có ít nhất một chỗ làm lần chạy thường đi sai. Điểm 4 nghĩa là nhiều chỗ.

## Bốn chỗ làm lần chạy thường đi sai

**Không có cách phân xử test sai hay sản phẩm sai.** Dòng 144–147 chỉ nói "lỗi của test thì sửa, lỗi của sản phẩm thì giữ câu kiểm". Không có tiêu chí để biết đỏ là lỗi nào. Model có cửa gọi một giá trị sai là "lỗi của test", rồi đổi giá trị mong đợi cho khớp output. Test xanh khoá luôn bug, và người dùng không biết.

**"Lần chạy đầu là bằng chứng" đá với "sửa rồi chạy lại".** Dòng 142–144 lấy lần chạy đầu làm bằng chứng, ngay sau đó dòng 144–145 cho sửa test rồi chạy lại. Báo cáo có thể dẫn output của lần chạy mà test còn lỗi.

**Regression test cho bug vừa sửa không có đường đi.** Chủ plugin làm thẳng trên nhánh main. Bản sửa đã commit thì "các commit kể từ nhánh mặc định" rỗng, model hỏi lại và lượt chạy kết thúc. Nếu tìm được phạm vi thì hành vi đúng lại không có trong lời gọi, mà diff thì bị cấm làm căn cứ. Lượt chạy chỉ ra một khoảng trống.

**Báo cáo giấu lỗi xuống cuối và nói từ riêng.** Dòng 167–170 đặt mục lỗi tìm được ở cuối danh sách, bắt dùng nhãn "Oracle sources", "Verified invariants", "Contract or harness gaps", và không nói rằng bộ test giờ đỏ. Người dùng đọc "Contract gap" tưởng API có lỗi, trong khi nghĩa thật là "chưa ai nói hành vi đúng, bạn quyết". Họ bỏ qua, và hành vi đó ra mắt mà không có test.

## Chỗ mơ hồ

- Chữ "charter" mang hai nghĩa: bước ghi kết quả mong đợi của chính i:test, và đoạn mở đầu file phần việc của i:flow. Câu "map back to a charter invariant" ở dòng 70 có thể bị hiểu theo nghĩa thứ hai, đẩy phần lớn rủi ro thành khoảng trống.
- Dòng 60 loại mọi "code comments" khỏi căn cứ, còn dòng 57 nhận "public docs … exported contracts". JSDoc của hàm được export nằm giữa hai bên. Với repo chỉ có JSDoc, lần chạy thứ nhất hoặc ra toàn khoảng trống, hoặc model đọc thân hàm rồi lấy hành vi hiện tại làm kỳ vọng.
- "Settled before the target is opened" không làm được khi chữ ký và thân hàm nằm chung một file.
- Đoạn "Called from i:flow … return those same items" có thể khiến model chép lại hồ sơ.

## Luật viết hai, ba lần

- Không sửa code sản phẩm, không sửa hồ sơ: dòng 31, 146–147, 177–178.
- Không xoá hay nới câu kiểm: dòng 132 và 156.
- Thứ không bao giờ là căn cứ: dòng 28–30 và 58–60.
- Câu kiểm cũ trái hợp đồng: dòng 29–30 và 134–135.
- Hợp đồng im lặng thì báo khoảng trống: dòng 60–61 và 171–172.
- Đoạn E2E (dòng 96–103) lặp bốn vế đã có ở chỗ khác.
- Đặt tên theo dự án: dòng 118–119 và 130–131.
- Chỉ dùng công cụ dự án đã có: dòng 88 và 127.
- Câu thứ ba của đoạn gom nhóm test là phần bù của câu đầu.

Một cặp trông như lặp nhưng không phải: bốn mục giữa của danh sách ghi kết quả mong đợi (dòng 51–52) và đoạn "Per scenario" (dòng 110–114). Bản thứ nhất được trả lời trước khi đọc code, bản thứ hai lúc viết test. Cắt bản thứ nhất sẽ đẩy việc đặt kỳ vọng về sau lúc đã đọc code, đúng thói quen skill muốn chặn.

## Luật cho ca hiếm

- Chế độ "chỉ nhìn từ ngoài" (strict black-box, dòng 74–78): chỉ chạy khi người dùng yêu cầu, chiếm năm dòng.
- Đoạn phân loại lỗi import (dòng 147–153): phần lớn lỗi import là do test tự viết sai đường dẫn; nhánh lỗi thuộc sản phẩm hiếm.
- Luật giữ chế độ chạy song song mặc định (dòng 119–121): chỉ ảnh hưởng tốc độ.
- "Its lane for generated tests" (dòng 131): ít dự án có thư mục riêng cho test sinh tự động.
- Đoạn khôi phục dependency (dòng 123–130): lệnh `npm ci` xoá sạch `node_modules` đang dùng. Ca hiếm, vì context tách biệt chạy trong cùng thư mục với phiên chính, nơi dependency thường đã có.
