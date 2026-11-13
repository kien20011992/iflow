# Bộ đề của vòng lặp vẽ

Hai bộ đề, dùng khác nhau (luật đầy đủ ở [quy trình đợt](../quy-trinh-dot.md)):

- **`luyen/`, bộ luyện.** Được xem kỹ từng lỗi; là nguồn của
  [sổ quan sát](../so-quan-sat.md).
- **`giu-rieng/`, bộ giữ riêng.** Đề thi kín, dùng để quyết giữ hay bỏ một đợt
  sửa. Người sửa skill không mở các file trong thư mục này và không đọc chi
  tiết lỗi của chúng; chỉ xem điểm và số mục mất điểm theo phần. Đề nào bị đọc
  thì chuyển sang `luyen/`, ghi vào [bảng điểm](../bang-diem.md), và nhờ một agent
  chưa đọc skill viết đề mới thay.

Mỗi đề là hai file: `<tên>.md` là đề, `<tên>.c.md` là phần C "Phương án" của
[thang chung](../thang-chung.md), viết cùng lúc với đề và trước khi chạy. Con số
trong đề (kể cả số "chủ đầu tư đã thống nhất với phòng cháy") là dữ liệu của
chủ đầu tư, không phải luật: luật nằm trong bảng luật của skill.

Bảy đề `can-ho-2pn-cai-tao`, `khach-san-lo-pho`, `nha-o-xa-hoi-9-tang` và bốn
đề giữ riêng do một agent chưa đọc skill viết ngày 2026-11-13. Ba đề `hue-2-tang`,
`pho-5x20-3-tang`, `quinta-monroy` là đề của chín vòng đầu; `pho-5x20-3-tang`
có phần C viết sau khi đề đã chạy, nên điểm C của nó chỉ dùng trong bộ luyện.
`quinta-monroy` chấm phần C theo [thang riêng của nó](../cham-quinta-monroy.md),
và agent dựng đã nhận ra công trình, nên điểm C của nó luôn "nhiễm".

## Đề phủ những trục nào

| Đề | Bộ | Loại công trình | Mới hay cải tạo | Hình học | Tầng nổi / hầm | Dạng đầu vào |
|---|---|---|---|---|---|---|
| hue-2-tang | luyện | nhà ở | mới | vuông góc | 2 / 0 | đề chữ |
| pho-5x20-3-tang | luyện | nhà ở | mới | vuông góc | 3 / 0 | đề chữ, có trục |
| quinta-monroy | luyện | nhà ở nhiều căn | mới | vuông góc | 3 / 0 | đề chữ |
| can-ho-2pn-cai-tao | luyện | căn hộ | cải tạo nội thất | vuông góc | 1 / 0 | đề chữ kèm số đo hiện trạng |
| khach-san-lo-pho | luyện | khách sạn | mới | vuông góc | 8 / 0 | đề chữ |
| nha-o-xa-hoi-9-tang | luyện | tòa chung cư | mới | vuông góc | 9 / 0 | đề chữ |
| nha-pho-cu-cai-tao | giữ riêng | nhà ở | cải tạo, giữ một phần kết cấu | có cạnh xiên | 4 / 0 | đề kèm bảng số đo hiện trạng |
| can-ho-goc-hai-tang | giữ riêng | căn hộ | hoàn thiện căn bàn giao thô | có tường cong | 2 / 0 | đề chữ kèm số đo |
| khach-san-3-sao | giữ riêng | khách sạn | mới | có cạnh xiên | 12 / 1 | đề chữ kèm toạ độ góc lô |
| chung-cu-cao-tang-2-ham | giữ riêng | tòa chung cư | mới | vuông góc | 22 / 2 | đề chữ |

Bộ giữ riêng phủ những trục bộ luyện chưa có: cạnh xiên, tường cong, tầng hầm,
nhà trên 10 tầng, căn hai tầng, và đầu vào là bảng số đo hiện trạng.
