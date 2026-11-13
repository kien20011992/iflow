# Khuôn bảng số `cad-params/1`

Bảng số (`params.json`) ghi phương án đã chọn thành số, đủ để dựng lại bản
vẽ mà không cần hội thoại. Mọi dự án, cả bốn loại công trình, dùng chung
một khuôn này. Thư viện vẽ, trình kiểm và sơ đồ duyệt đều đọc đúng khuôn này,
nên bảng số sai khuôn thì không dựng.

Kiểm một bảng số:

```
python3 ${CLAUDE_SKILL_DIR}/scripts/params_check.py params.json
```

Exit 0 là sạch. Mỗi lỗi in đường dẫn tới chỗ hỏng, ví dụ
`floors.L2.openings[2].wall: không có tường "wZ" ở floors.L2`. Dòng `XEM`
là cảnh báo, không chặn. Ba bảng mẫu nằm ở `tests/cad/bang-so/` của repo
plugin: nhà phố ba tầng, chung cư chín tầng, khách sạn B&B.

## Luật chung

- Mọi kích thước là milimét nguyên, và bề rộng, chiều cao, mặt bậc, cỡ
  cột, tỷ lệ phải lớn hơn 0. Chỉ ba khoá được có số lẻ:
  `need_area` (m²), `value` (chỉ tiêu khu đất) và `north_deg` (độ).
- Số suy ra bằng phép chia, như chiều cao một bậc thang, không ghi vào bảng.
- Mỗi đối tượng được mang `by` để nói số do ai đưa: `user`, `model` (AI
  chọn) hoặc `default` (lấy mặc định). Không có `by` nghĩa là người dùng
  đưa. Mục đang chờ người dùng chọn mang `"pending": true`. `note` là ghi
  chú tự do.
- Một khoá không được viết hai lần trong cùng một bảng: JSON chỉ giữ lần
  sau, nên script báo lỗi thay vì im lặng bỏ lần trước.
- Tên khoá viết tiếng Anh. Tên phòng và ghi chú viết bằng ngôn ngữ của
  người dùng.

## Điểm: tên trục cộng khoảng lệch

Trong phần nhà, mọi vị trí viết bằng tên trục, không viết tọa độ trần. Một
điểm là hai cặp, phương x rồi phương y:

```json
[["2", -200, -1500], ["E", 0]]
```

Nghĩa là: trục 2 lùi 200 rồi lùi thêm 1500, nằm trên trục E. Các khoảng
lệch cộng dồn, nên ghi được cả cách suy ra số: "mặt trong tường bao 200,
rồi 1500 bề rộng WC". Dời một trục thì mọi thứ bám theo.

Ranh đất là ngoại lệ: nó không nằm trên lưới, nên viết bằng tọa độ trần
`[x, y]` trong cùng hệ tọa độ với lưới.

## Các phần của bảng

| Phần | Bắt buộc | Chứa gì |
|---|---|---|
| `schema` | có | Luôn là `"cad-params/1"`. Script từ chối bản khác. |
| `project` | có | `name`; `type` là `house`, `apartment`, `hotel` hay `apartment_building`; `depth` là `construction` (gần thi công) hay `scheme` (phương án); `scale`. |
| `site` | trừ căn hộ | Khu đất. Xem dưới. |
| `grid` | có | `x` và `y`, mỗi bên là bảng tên trục → tọa độ. |
| `levels` | có | Danh sách tầng từ dưới lên. |
| `types` | có | Loại tường, ô cửa, thang, cột. |
| `floors` | có | Đối tượng của từng tầng. |
| `clusters` | không | Cụm đặt tên được, dùng lại nhiều lần. |
| `placements` | không | Đặt cụm lên nhiều tầng cùng lúc. |
| `sections` | không | Đường cắt của mặt cắt. |
| `drawings` | có | Danh mục hình sẽ vẽ, kèm gốc của từng hình. |
| `rules` | không | Mã các dòng luật áp dụng. |
| `structure` | không | Số kết cấu để vẽ mặt cắt. Xem dưới. |
| `law_inputs` | không | Số luật cần mà bản vẽ không cho. Xem dưới. |

### Khu đất

```json
"site": {
  "outline": [[0, -3000], [5000, -3000], [5000, 17000], [0, 17000]],
  "setbacks": [{"edge": 0, "mm": 3000}, {"edge": 2, "mm": 2000}],
  "front_edge": 0, "north_deg": 0, "ground_elevation": -300,
  "limits": [{"name": "density_max_pct", "value": 60, "by": "user"}]
}
```

Cạnh số `i` đi từ điểm `i` tới điểm `i+1` của `outline`. `north_deg` là góc
của hướng bắc, tính bằng độ từ chiều dương trục x, ngược chiều kim đồng hồ.
`ground_elevation` là cao độ sân so với sàn tầng một. Khu đất có sẵn trong
một file DXF thì thay `outline` bằng `"from_dxf": "<đường dẫn>"`.

### Tầng

```json
"levels": [
  {"name": "L1", "elevation": 0, "height": 3600, "kind": "ground"},
  {"name": "L2", "elevation": 3600, "height": 3300, "kind": "typical"}
]
```

`kind` là `basement`, `ground`, `typical` hay `roof`. Tầng trên nằm đúng
chỗ tầng dưới kết thúc: cao độ của nó bằng cao độ cộng chiều cao của tầng
dưới. Script báo lỗi khi hai số lệch nhau.

### Loại

```json
"types": {
  "walls": {"ext": {"thickness": 200}, "virtual": {"thickness": 0}},
  "openings": {"P1": {"kind": "door", "width": 800, "height": 2200},
               "V1": {"kind": "window", "width": 1200, "height": 1400, "sill": 900}},
  "stairs": {"T1": {"kind": "u_turn", "flight_width": 900, "tread": 260, "gap": 100}},
  "columns": {"C1": {"size": [200, 300]}}
}
```

Tường bề dày 0 là ranh ảo giữa hai phòng thông nhau: script dò phòng coi nó
là tường, script vẽ tường bỏ qua nó. Loại ô cửa là `door`, `window`,
`shutter` (cửa cuốn) hay `opening` (ô trống). Hồ sơ `construction` cần chiều
cao của mọi ô cửa và cao bệ của cửa sổ; hồ sơ `scheme` chỉ cần bề rộng.
Thang là `straight`, `u_turn` hay `l_turn`.

### Đối tượng trong một tầng

Mỗi tầng trong `floors` có các danh sách sau, danh sách nào trống thì bỏ.
Mọi đối tượng, trừ lần đặt cụm, có `id` không trùng trong tầng đó và có
`phase`:

| `phase` | Nghĩa | Ví dụ |
|---|---|---|
| `new` (mặc định) | Xây mới. | Nhà xây mới. |
| `existing` | Có sẵn, giữ lại. | Cột và hộp kỹ thuật của căn hộ cải tạo. |
| `demolish` | Có sẵn, phá bỏ. | Vách cũ trong căn hộ cải tạo. |
| `future` | Xây sau. | Phần mở rộng của nhà xây dần. |

| Danh sách | Trường | Ghi chú |
|---|---|---|
| `walls` | `from`, `to`, `type`, `align` | `align`: `center` canh tim; `left` hay `right` là tường nằm bên trái hay bên phải đường từ `from` tới `to`. |
| `columns` | `type`, `at` | `at` là tâm cột. |
| `openings` | `wall`, `type`, `offset`, `hinge`, `swing` | `offset` tính từ đầu `from` của tường tới mép ô cửa. `hinge`: bản lề ở phía `start` hay `end`. `swing`: cánh mở về bên `left` hay `right` của tường. |
| `stairs` | `type`, `start`, `dir`, `turn`, `up_to`, `risers` | `start` là mép bậc đầu, phía tường. `dir`: `+x`, `-x`, `+y`, `-y`. `up_to`: tên tầng trên, hoặc `next` khi thang nằm trong cụm đặt lên nhiều tầng. `risers`: số bậc cao mỗi tầng. |
| `rooms` | `name`, `at`, `use`, `need_area` | `at` là một điểm nằm trong phòng; đường bao do script dò từ tường. `use`: `private`, `shared`, `wet`, `service`, `circulation`, `outdoor`. `need_area`: diện tích đề yêu cầu, m². |
| `shafts` | `kind`, `from`, `to` | Hộp kỹ thuật hình chữ nhật: `lift`, `duct`, `garbage`, `other`. |
| `voids` | `from`, `to`, `floor` | Giếng trời hay ô thông tầng; `floor` là `none` hay `glass`. |
| `parking` | `vehicle`, `count`, `from`, `to` | Một khu đỗ xe hình chữ nhật: `car` hay `motorbike`, kèm số chỗ. |
| `furniture` | `block`, `at`, `rotate` | Tên block trong thư mục block của skill. |
| `railings` | `points` | Lan can, một đường gấp khúc. |
| `placements` | `cluster`, `at`, `rotate`, `mirror` | Đặt một cụm vào tầng này. Xem dưới. |
| `outside` | `what`, `near` | Thứ khuôn không tả được. Xem dưới. |

Ô cửa chỉ trỏ được tới tường trong cùng tầng, hay cùng cụm. Script báo lỗi
khi ô cửa không lọt trong tường của nó với má 100 mỗi bên. Phép đo này tính
từ hai đầu tường, chưa trừ bề dày tường vuông góc; trình kiểm đọc DXF đo lại
trên hình thật.

### Cụm và lần đặt cụm

Cụm là một nhóm đối tượng đặt tên được, dùng lại nhiều lần: căn hộ mẫu,
phòng khách sạn mẫu, lõi thang, cả một tầng điển hình. Mỗi cụm có lưới riêng
và các danh sách y như một tầng:

```json
"clusters": {
  "can-2N": {"grid": {"x": {"a": 0, "b": 7200}, "y": {"m": 0, "h": 8400}},
             "walls": [], "openings": [], "rooms": []}
}
```

Một lần đặt cụm ghi cụm nào, gốc `(0, 0)` của cụm rơi vào điểm nào, xoay
`rotate` (0, 90, 180, 270 độ) và lật `mirror` (`none`, `x` lật trái phải,
`y` lật trên dưới). Lật trước, xoay sau, rồi dời tới `at`.

- Đặt trong một tầng hay một cụm khác: ghi trong `placements` của nơi đó.
  Ví dụ tầng điển hình đặt sáu căn mẫu, căn phía bắc lật `y`.
- Đặt lên nhiều tầng: ghi trong `placements` ở gốc bảng, kèm `levels`.
  Ví dụ một tầng điển hình đặt lên L2 tới L8 là một dòng.

Cụm được chứa cụm khác, nhưng không được chứa chính nó, trực tiếp hay qua
cụm khác. Tường bao giữa hai căn kề nhau nằm ở tầng điển hình, không nằm
trong cụm căn, để hai căn không mỗi bên một bức tường.

### Thứ khuôn không tả được

Khuôn không có tường cong, thang xoắn, ram dốc, sân vườn theo ranh xiên. Thứ
như vậy không ép vào khuôn. Ghi một dòng trong `outside`:

```json
{"id": "x1", "what": "Lối xe xuống hầm (ram dốc)", "near": [["9", 3000], ["A", -3000]]}
```

Thư viện vẽ một đám mây đánh dấu ở `near` kèm `what`, và đưa dòng đó vào
danh sách giao cho người dùng. Script kiểm in mỗi dòng `outside` thành một
cảnh báo, để biết bao nhiêu phần sẽ bị giao lại. Thêm một loại đối tượng mới
vào khuôn là việc của một đợt sửa skill, không phải của một dự án.

### Số luật cần mà bản vẽ không cho

```json
"law_inputs": {"fire_resistance": {"value": "II", "by": "user"}, "s_class": {"value": "S0", "by": "user"},
               "fire_height_mm": {"value": 7200, "by": "model"}, "people_per_floor": {"value": 6, "by": "model"}}
```

Các khoá: `fire_resistance` bậc chịu lửa (I tới V), `s_class` cấp nguy hiểm
cháy kết cấu (S0 tới S3), `fire_height_mm` chiều cao phòng cháy chữa cháy,
`people_per_floor`, `area_kind` (`new` khu mới, `existing` khu hiện hữu),
`road_area_level_or_above` (đường giáp lô từ cấp khu vực trở lên), `road_width_m`,
`volume_m3` (khối tích nhà; nhà riêng lẻ dưới 7 tầng chỉ theo QCVN 06 khi
từ 5.000 m³ hay cao PCCC từ 25 m), `sprinkler`, `submit_date` (ngày nộp, chọn dòng luật còn hiệu lực). Thiếu khoá
nào thì phép kiểm luật cần nó báo "cần xem", không đoán.

Cụm mang `kind` để phép kiểm luật biết nó là gì: `unit` (một căn hộ),
`room` (một phòng khách sạn), `floor`, `core`, `other`; kèm `unit_type`
(ví dụ `"2N"`) khi là căn hay phòng.

### Số kết cấu để vẽ mặt cắt

```json
"structure": {"slab": {"value": 100, "by": "default"}, "beam": {"value": [200, 300], "by": "default"}}
```

Các khoá: `slab` bề dày sàn, `beam` [rộng, cao] của dầm, `parapet` cao tường
chắn mái, `footing_depth` và `footing_width` của móng, `stair_waist` bề dày
bản thang, `rail_height` cao lan can. Mọi số là ước để vẽ; kỹ sư tính. Thiếu
khoá nào thì thư viện lấy mặc định và ghi vào danh sách giao.

### Tường theo giai đoạn

Tường `new` và `existing` vẽ trên `A-WALL`. Tường `demolish` vẽ nét đứt trên
`A-DEMO`, tường `future` nét đứt trên `A-FUTR`. Phòng và các phép kiểm tính
trên nhà sau khi làm xong: tường phá và tường xây sau không ngăn phòng, ô cửa
trên chúng không được vẽ.

### Mặt cắt và danh mục hình

```json
"sections": [{"name": "1-1", "look": "-x",
              "path": [[["2", -650], ["A", -500]], [["2", -650], ["E", 500]]]}],
"drawings": [{"id": "plan:L1", "origin": [0, 0]},
             {"id": "section:1-1", "origin": [66000, 0]}]
```

`look` là hướng nhìn của mặt cắt. Đường cắt có từ hai điểm trở lên; nhiều
hơn hai là cắt gãy. Mỗi hình trong `drawings` có `id` dạng `plan:<tầng>`,
`section:<tên>`, `elevation:<hướng nhìn>` (ví dụ `elevation:-y`) hay
`site`, và `origin` là gốc của hình đó trong không gian mô hình. Hình `site`
cần phần `site`. Hai hình cùng `id`, hay hai mặt cắt cùng tên, là lỗi.

## Bảng số hiện lên file DXF thế nào

Thư viện vẽ ghi file theo các điều dưới đây, và `scripts/plan_check.py` đọc
file theo đúng các điều đó để so với bảng số. Đổi một điều thì sửa cả hai
bên.

- Mỗi hình `plan:<tầng>` nằm ở `origin` của nó trong `drawings`: tọa độ
  trong file bằng tọa độ theo bảng số cộng gốc của hình.
- Mỗi phòng là một đường bao khép kín trên `X-AREA`, chứa điểm `at` của
  phòng.
- Mỗi ô cửa là một block chèn trên `A-DOOR` (cửa đi, cửa cuốn, ô trống)
  hay `A-GLAZ` (cửa sổ), có thuộc tính `ID` bằng id của ô cửa. Cửa đi chèn
  tại bản lề, trên mặt tường phía cánh mở; cánh là một cung trong block,
  tâm ở điểm chèn, bán kính bằng bề rộng cánh. Cửa sổ, cửa cuốn và ô trống
  chèn tại tâm ô cửa trên đường tim tường, xoay theo hướng tường và co
  giãn theo bề rộng ô cửa và bề dày tường. Trình kiểm đọc điểm chèn và cung
  cánh cửa, không đọc góc xoay.
- Đối tượng nằm trong một cụm đã đặt mang id mở rộng: mỗi lần đặt viết
  `tên-cụm#n`, nối bằng `/`, rồi tới id gốc. `n` là thứ tự của lần đặt trong
  danh sách `placements` chứa nó, đếm từ 0. Lần đặt ở gốc bảng thêm chữ `g`
  trước số, để không trùng với lần đặt trong tầng: `tên-cụm#g0`. Ví dụ cửa
  `d1` của căn đặt thứ tư trong tầng điển hình, tầng này lại là lần đặt đầu
  tiên ở gốc bảng: `tang-dien-hinh#g0/can-2N#3/d1`.
- Hình mặt cắt, mặt đứng và khu đất nằm ngoài vùng của mọi mặt bằng: vùng
  của một mặt bằng là khung bao tường và phòng của tầng đó, nới 1 m mỗi
  phía. Block ô cửa vẽ trên mặt đứng nằm ngoài vùng đó nên không bị đếm là
  ô cửa thừa.
- Mỗi cột là một đường khép kín trên `A-COLS`. Đồ đạc và thiết bị là block
  trên `A-FURN` hay `A-FLOR`.

## Script kiểm làm gì và không làm gì

Kiểm: đúng phiên bản; đủ phần bắt buộc theo loại công trình và độ sâu hồ
sơ; giá trị nằm trong danh sách cho phép; milimét nguyên; mọi tên trỏ tới
thứ có thật (trục, tầng, loại, tường của ô cửa, cụm của lần đặt, tầng của
hình); id, tên mặt cắt và hình không trùng; khoá không viết hai lần; cạnh ranh
đất được trỏ tới có thật; tầng xếp liền nhau; tường dài hơn 0; ô cửa lọt
tường; cụm không tự chứa mình.

Không kiểm: hình phòng, diện tích thật, đi lại, thang đi được. Những phép đó
cần hình đã dựng, nên thuộc trình kiểm đọc file DXF.
