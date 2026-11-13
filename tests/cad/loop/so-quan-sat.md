# Sổ quan sát của i:cad

Mỗi vòng chạy thử chỉ ghi vào đây, không sửa skill ngay. Việc sửa đi theo đợt,
theo [quy trình đợt](quy-trinh-dot.md). Mỗi lỗi một dòng. Gặp lại lỗi cũ ở
một loại công trình khác thì thêm loại đó vào cột "Loại công trình" của chính
dòng cũ, không viết dòng mới. Nhờ vậy điều kiện "lặp ở hai loại công trình"
đọc được ngay trên sổ.

Cột "Đưa về lớp" là đề nghị lúc ghi, theo thứ tự ưu tiên của quy trình đợt:
phép kiểm, hàm thư viện, block hay file mẫu, bảng số, chữ phán đoán. Dòng chỉ
đúng với một đề thì ghi "để người dùng chỉnh". Cột "Đợt" để trống tới khi một
đợt xử lý dòng đó; khi đó ghi số đợt và kết quả (sửa, bỏ, để người dùng chỉnh).

Loại công trình viết tắt: NO nhà ở, CH căn hộ, KS khách sạn, TC tòa chung cư.

| Mã | Vòng hay nguồn | Đề | Loại công trình | Thấy gì | Đưa về lớp | Đợt |
|---|---|---|---|---|---|---|
| 1 | Eval slice 06, ca `cad-owner-assumed` | ca eval nhà chưa đo | NO | Danh sách việc cần đo nằm trong hồ sơ dự án, không nằm trong tin nhắn trả lời, nên phép chấm "đưa danh sách cần đo" hỏng một lần; chạy lại thì đạt. | chữ phán đoán (lời đáp phải nói điều chủ nhà cần làm, không chỉ ghi vào file) | |
| 2 | Vòng 1–3 | `hue-2-tang.md` | NO | Chữ trong ảnh PNG vẽ bằng font nét vì máy chạy không có Arial, nên không soát được chữ đè bằng mắt. | môi trường thử (cài font hoặc chọn font có sẵn cho ảnh), không phải lỗi skill | |
| 3 | Vòng 1–9 | mọi đề | NO | Chưa kiến trúc sư nào mở file trong AutoCAD: chưa biết kích thước có bám hình khi kéo giãn và file có mở sạch không. | người duyệt ngoài (phiếu duyệt AutoCAD), không có lớp nào của skill thay được | |
| 4 | Vòng 8; thư viện slice 04 | `pho-5x20-3-tang.md` | NO | Lan can một nét tay vịn, sàn kính, cửa cuốn đã có hàm và block trong thư viện nhưng chưa vòng agent nào dựng lại bằng chúng. | kiểm lại ở vòng sau, chưa cần sửa | |
| 5 | Vòng 9 | `quinta-monroy.md` | NO | Agent nhận ra công trình nổi tiếng nên phần phương án bị "nhiễm", không dùng để so. | bộ đề (đề viết bởi người chưa đọc skill, không nổi tiếng) | |
| 6 | Vòng 9 | `quinta-monroy.md` | NO | Chưa vòng nào vẽ lại dự án nhiều căn theo cách đặt cụm lặp (ba khối liền nhau, lối vào mọi căn). | kiểm lại ở vòng sau trên một đề nhiều căn | |
| 7 | Bài dựng thật slice 04 | bảng mẫu nhà phố, chung cư | NO, TC | Mẫu tô đất ANSI31 của mặt cắt luôn ra "chưa vẽ: cần người mở AutoCAD xem lại". | người duyệt ngoài; nếu AutoCAD hiện sai thì sửa block hay file mẫu | |
| 8 | Chấm thử thang chung, slice 09 | `pho-5x20-3-tang.md` (bản dựng thư viện) | NO | Tường trên mặt bằng chỉ có hai nét viền, lòng trắng; chỉ cột được tô. Mặt cắt tô một màu cho cả tường xây lẫn bê tông. | hàm thư viện (tô tường bị cắt; mẫu khác cho hai vật liệu) | |
| 9 | Chấm thử thang chung, slice 09 | như trên | NO | Mỗi mặt bằng dùng bốn cấp dày nét (0,50 / 0,25 / 0,18 / 0,13); TCVN 6083 nói 2–3 cấp. | file mẫu (bảng layer) | |
| 10 | Chấm thử thang chung, slice 09 | như trên | NO | Chữ bị đè mà `dxf_check.py` không bắt: nét chú dẫn chữ WC cắt qua "3,00 m²"; mũi tên đè ký hiệu "1-1" ở đầu đường cắt; nét đường cắt qua tên phòng; trên mặt cắt chữ "Thang" bị tay vịn cắt, "15000" bị trục cắt. | phép kiểm (đường dẫn, mũi tên mặt cắt, nét trên mặt cắt) rồi hàm thư viện | |
| 11 | Chấm thử thang chung, slice 09 | như trên | NO | Giếng trời chỉ có lan can ở cạnh dọc; cạnh ở trục C mở thẳng ra sảnh thang không lan can, cả trên mặt bằng lẫn mặt cắt. | phép kiểm (mép sàn hở phải có lan can) và bảng số | |
| 12 | Chấm thử thang chung, slice 09 | như trên | NO | Thang không ghi tổng số bậc và chiều cao bậc; số bậc trên mặt bằng chạy 1–18 nên dễ đọc là 18 bậc thay vì 20. Không có chấm tròn ở bậc đầu; nét ngắt vế là đoạn thẳng chứ không dích dắc. | hàm thư viện (ký hiệu thang) | |
| 13 | Chấm thử thang chung, slice 09 | như trên | NO | Đường cắt mặt cắt là nét mảnh đều, không đậm hai đầu. Diện tích phòng không gạch dưới. Số bậc cao 1,8 mm trên giấy, dưới 2 mm. | hàm thư viện và file mẫu | |
| 14 | Chấm thử thang chung, slice 09 | như trên | NO | Hồ sơ gần thi công thiếu kích thước trong phòng, kích thước lỗ cửa trong nhà và bảng thống kê cửa. | hàm thư viện (kích thước trong phòng, bảng cửa) | |

## Đếm lại các lần sửa của chín vòng đầu

Chín vòng đầu (ghi ở [rounds.md](rounds.md)) sửa tổng cộng 101 điều. Mỗi điều
được xếp vào lớp mà nó sẽ thuộc về nếu gặp lại hôm nay. Phép xếp do Claude làm
bằng tay, đọc từng điều một, nên vẫn là phán đoán; nhưng nó thay cho tỷ lệ ước
lượng lúc định hình chương trình.

| Lớp hôm nay | Số điều | Ví dụ |
|---|---|---|
| Cách vẽ: hàm thư viện, block, file mẫu | 57 | luật đặt ba hàng kích thước, nhãn cửa P/V, block cửa theo phía bản lề, móng dưới tường bị cắt |
| Phép kiểm | 17 | mười ba phép của `dxf_check.py`; phép cộng diện tích; phép kiểm thang đo mặt bậc |
| Ghi chép về CADCraft | 8 | lệnh `plot` cho ảnh nền trắng; `text` không nhận `style` |
| Chữ phán đoán | 10 | hỏi khi kích thước không nói lọt lòng hay theo tim; sổ tiền đổi mọi khoản ra m² |
| Bảng số | 6 | đường ranh ảo là tường bề dày 0; gốc từng hình ghi trong bảng số |
| Quy trình trong `SKILL.md` | 2 | bảng số đã duyệt mà thang không đạt thì quay lại lần duyệt thứ hai |
| Thang điểm | 1 | làm rõ ba mục của thang Quinta Monroy |

Hơn một nửa số điều đã sửa bằng chữ là cách vẽ. Từ slice 03, những điều đó
nằm trong thư viện vẽ: một lỗi cách vẽ giờ sửa một hàm kèm bài tự thử, không
thêm câu vào `references/ve.md`. Chỉ khoảng một phần mười thật sự là phán đoán
nghề cần nằm trong chữ.
