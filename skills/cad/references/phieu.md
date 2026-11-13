# Phiếu đề bài `cad-brief/1` và cửa vào chuẩn

Skill chỉ nhận ba dạng đầu vào:

| Dạng | Dùng cho | Kiểm gì |
|---|---|---|
| Phiếu đề bài `phieu.json` | Mọi dự án | Đủ ô bắt buộc của loại công trình; số đo thế giới thật do người dùng đưa. |
| File DXF hình có sẵn | Khu đất có hình lạ; nhà hay căn hộ có sẵn | Đọc được, đơn vị milimét, ranh đất khép kín trên `C-PROP`, tường khép kín trên `A-WALL`. |
| Câu trả lời trong hội thoại | Bổ sung ô còn trống | Được ghi vào phiếu, rồi phiếu được kiểm lại. |

Ảnh, PDF, bản quét: AI đọc để hiểu bối cảnh và để biết hỏi gì, nhưng không
lấy số đo từ đó. Skill dừng và nói người dùng cần đưa gì thay vào: vẽ lại
ranh đất thành DXF trên layer `C-PROP`, hoặc điền kích thước từng cạnh vào
phiếu.

Kiểm một đầu vào, loại nào cũng vậy:

```
uv run ${CLAUDE_SKILL_DIR}/scripts/cua_vao.py <file>
```

Exit 0 là nhận, 1 là chặn kèm danh sách điều cần sửa, 2 là không đọc được.

## Một ô của phiếu

Mỗi ô là một bảng:

```json
"site": {"value": {"edges_mm": [5000, 20000, 5000, 20000]}, "by": "user", "source": "sổ đỏ, trang 2"}
```

- `by`: `user` khi người dùng đưa, `model` khi AI tra hay chọn. Ô AI tra từ
  luật hay nguồn ngoài ghi `source`.
- Ô chưa có ghi `{"pending": true}`. Ô bắt buộc còn `pending` thì phiếu bị
  chặn, và dòng chặn nói rõ ô đó cần gì.
- **Số đo thế giới thật không bao giờ do AI ước**: khu đất, bề rộng đường,
  file hiện trạng. Ba ô này mang `by: model` là phiếu bị chặn.

## Các ô

| Ô | Bắt buộc | Giá trị |
|---|---|---|
| `type` | có | `house`, `apartment`, `hotel` hay `apartment_building`. |
| `work` | có | `new` (xây mới) hay `renovation` (cải tạo). |
| `depth` | có | `construction` (gần thi công) hay `scheme` (phương án). |
| `place` | có | `{"province": …, "ward": …, "street": …}`; tỉnh không được trống. |
| `site` | trừ căn hộ | `{"edges_mm": [cạnh 0, cạnh 1, …]}` (ít nhất ba cạnh, milimét) hoặc `{"from_dxf": "<file>"}`. Số đo thế giới thật. |
| `street_edge` | không | Số của cạnh giáp đường. |
| `street_width_mm` | không | Bề rộng đường. Số đo thế giới thật. |
| `setbacks` | không | `[{"edge": số cạnh, "mm": khoảng lùi}]`. |
| `north` | không | Hướng của cạnh giáp đường (`east`, `south`…) hoặc góc độ. |
| `limits` | không | `{"density_max_pct", "far_max", "floors_max", "height_max_mm"}`, ô nào có thì ghi. |
| `budget` | không | `{"amount_vnd": số tiền, "phases": số đợt xây}`. |
| `rules` | không | Danh sách văn bản luật áp dụng. |

Phần riêng theo loại công trình, đều bắt buộc với loại đó:

| Loại | Ô | Giá trị |
|---|---|---|
| Nhà ở | `occupants` | Ai ở: `[{"who": …, "count": …}]`. |
| | `rooms_needed` | Các phòng cần có: `[{"room": …, "count": …, "area_m2"?: …}]`. |
| | `floors_wanted` | Số tầng mong muốn. |
| Căn hộ cải tạo | `existing_dxf` | File DXF căn hộ có sẵn. Số đo thế giới thật. |
| | `keep_untouched` | Phần không được đụng: `["cột", "hộp kỹ thuật", …]`. |
| | `rooms_needed` | Như nhà ở. |
| Khách sạn | `room_types` | `[{"type": …, "count": …, "area_m2"?: …}]`. |
| | `stars` | Hạng sao, số. |
| | `services` | Các khu dịch vụ: danh sách chữ. |
| Tòa chung cư | `unit_types` | `[{"type": …, "count" hoặc "share_pct": …, "area_m2"?: …}]`. |
| | `floors` | Số tầng nổi. |
| | `basements` | Số tầng hầm. |
| | `podium` | Khối đế: chữ mô tả, hoặc `"none"`. |

Ô không có trong hai bảng trên được giữ nhưng script báo "không thuộc phiếu",
để lỗi gõ tên ô không bị bỏ qua im lặng.

## File DXF hình có sẵn

- Đơn vị bản vẽ là milimét (`$INSUNITS` = 4).
- Ranh đất: đúng một đường nhiều đoạn khép kín trên `C-PROP`, không tự cắt.
- Nhà hay căn hộ có sẵn: các khối tường là đường khép kín trên `A-WALL`; cột,
  nếu có, trên `A-COLS`.
- File phải có ít nhất một trong hai thứ trên.

Phiếu trỏ tới file bằng `site.from_dxf` hay `existing_dxf`; script kiểm phiếu
không mở file đó, nên kiểm file riêng bằng cùng lệnh.
