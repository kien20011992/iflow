# Làm việc với CADCraft

Đọc file này lần đầu vẽ trong một phiên. CADCraft là chương trình vẽ 2D mã
nguồn mở, có giao diện dòng lệnh `cadcraft-cli` và một MCP server cho agent.
Tên lệnh của nó là tên lệnh AutoCAD viết thường.

CADCraft ra bản mới vài ngày một lần và không hứa giữ nguyên tên lệnh hay
tham số. Vì vậy **danh mục lệnh của bản đang cài thắng mọi điều ghi trong
file này**. Mỗi dòng dưới đây mang một nhãn nguồn:

- **[tài liệu]**: theo tài liệu chính thức trong repo `storytold/cadcraft`
  (`README.md`, `docs/mcp.md`, `docs/cli.md`, `docs/control-protocol.md`,
  `docs/customization.md`, `docs/gaps.md`, `docs/file-format-parity.md`).
- **[bản 0.20.0]**: một phiên làm việc đã gặp ở bản 0.20.0, chưa thử lại ở
  bản sau.
- **[chưa thử]**: suy ra, phải chạy thử rồi mới tin.

## Tìm CADCraft

Thử theo thứ tự: `cadcraft-cli`, `cadcraft.cli` (khi cài qua snap), đường dẫn
người dùng đưa. Ghi lại phiên bản.

Không tìm thấy thì không tự tải hay cài. Nói một câu bằng lời thường: máy
chưa có chương trình vẽ, nên file bản vẽ phải chờ, còn các việc trước đó vẫn
làm tiếp. Chỉ khi người dùng hỏi cách cài mới nêu các đường cài chính thức:
snap, Homebrew, gói `.deb`, AppImage, flatpak trên trang phát hành. Không file
DXF nào được coi là đã giao khi công cụ chưa chạy thật.

## Dò bản đang cài

Làm một lần cho mỗi phiên bản, ghi kết quả vào `cadcraft-<phiên-bản>.md`
trong thư mục dự án. Phiên bản đang cài khác với file ghi chép thì dò lại.
Phiên bản đã có nhãn trong file này thì chỉ thử những lệnh sẽ dùng mà file
chưa ghi.

1. Lưu danh mục lệnh: `cadcraft-cli commands --compact`. Mỗi mục có id, bí
   danh và mô tả tham số. [tài liệu]
2. Lưu `cadcraft-cli help run` và `cadcraft-cli help convert`. Tài liệu trên
   web không liệt kê đủ cờ. [tài liệu]
3. Từ danh mục, xác nhận tên và tham số thật của từng lệnh sẽ dùng: nét,
   đường nhiều đoạn, cung, tròn, chữ, mẫu tô, block và chèn block, các loại
   kích thước, kiểu kích thước, kiểu chữ, layer, kiểu nét, đơn vị, lưu, kiểm
   lỗi, và các lệnh đo. Lệnh nào không có thì ghi "không có ở bản này".
4. Dựng bản thử ở mục cuối file, ghi cái gì chạy, cái gì chạy có lưu ý, cái
   gì không chạy.

Không chép tên tham số từ trí nhớ hay từ file này vào `build.py`. Chép từ
danh mục vừa lưu.

## Hai cách gọi

**Dòng lệnh, dùng để dựng và kiểm.** Một lần chạy dựng cả bản vẽ:

```
cadcraft-cli run --cmd 'id {json}' --cmd 'id {json}' … --save out.dxf
cadcraft-cli run out.dxf --cmd 'shapes {…}'
cadcraft-cli info out.dxf
```

- Mỗi `--cmd` in một dòng JSON kết quả ra stdout. Lỗi và cảnh báo ra stderr.
  Mã thoát 0 là xong, 1 là lệnh hỏng, 2 là gõ sai cờ hoặc JSON và chưa làm
  gì. [tài liệu]
- Đọc file mà phải bỏ sót thứ gì thì mã thoát vẫn là 0. Phải đọc `skipped` và
  `readNotes` trong kết quả `info`. [tài liệu]
- Bản vẽ mới phải mở bằng cờ `--metric`. Không có cờ này thì bản vẽ theo hệ inch. [bản 0.20.1]
- Giá trị `"{last}"` trong tham số được thay bằng mã của đối tượng mà lệnh trước vừa tạo, ví dụ `"handles": ["{last}"]` để tô chính đường vừa vẽ. [bản 0.20.1]
- Một lần chạy 406 `--cmd` dựng và lưu được hai mặt bằng. Một lệnh sai giữa
  chuỗi làm dừng cả lần chạy, mã thoát 1, không lưu file. [bản 0.20.1]
- `cadcraft-cli info` luôn có khoá `skipped`; đọc `skipped.count`, đừng xét
  khoá có mặt hay không. [bản 0.20.1]
- Đường lui khi `--cmd` không chịu nổi: ghi cùng danh sách lệnh thành file
  script, mỗi dòng một `id {json}`, chạy bằng `--script-file`. [tài liệu cho
  định dạng, chưa thử cho việc dừng khi lỗi]

**MCP server, dùng để xem nhanh trong hội thoại.** Không bắt buộc. Người dùng
đăng ký một lần: `claude mcp add cadcraft -- cadcraft-cli mcp`. Các tool:
`execute {command, params}`, `list_commands {filter}`, `inspect_drawing`,
`query_entities`, `find_text`, `render`, `new_drawing`, `open`, `save`.
[tài liệu] Bản vẽ trong phiên MCP không phải file đã lưu, nên bằng chứng kiểm
luôn lấy từ file DXF mở lại. Gọi `execute` phải dùng đúng khoá `command`. Sai
khoá thì lệnh treo ở dấu nhắc. [bản 0.20.0]

## Lệnh đo

Chạy được qua `--cmd` của dòng lệnh trên file đã lưu, và qua `execute` của MCP.
[bản 0.20.1] Lệnh đọc chữ ở dòng lệnh tên là `texts`.

| Lệnh | Trả gì | Phải đọc thêm gì |
|---|---|---|
| `shapes` | Chu vi, diện tích, tâm, chỗ tự cắt, đỉnh trùng của các hình khép kín. | `skipped` và `selfCheck`. |
| `loops` | Vòng khép kín ghép từ các nét rời, chuỗi hở kèm độ hở, điểm rẽ nhánh. | Có `capped` thì kết quả không dùng được. |
| `find_text` | Chữ, điểm đặt, cỡ, góc, kiểu, layer. | — |
| `usage` | Layer, block, kiểu chữ, kiểu nét đang dùng và không dùng. | `incomplete`. |
| `query_entities` | Đối tượng theo loại, layer hoặc vùng. | Mỗi trang 500 đối tượng, `count` là tổng. |
| `inspect_drawing` | Số đối tượng, phạm vi, layer, kiểu, block. | `skipped`, `readNotes`. |

Lệnh `entities {"type": "DIMENSION"}` trả số đo thật (`measurement`), hai điểm
gốc và chữ gõ đè của từng kích thước. [bản 0.20.1] Khi cần một trình đọc thứ
hai, đọc bằng `ezdxf` trong một môi trường ảo
riêng, vì Python hệ thống thường chặn cài thêm thư viện. [bản 0.20.0]
`ezdxf audit` cũng là trình đọc độc lập để thử xem file có đọc được ngoài
CADCraft không.

## Lưu và xuất ảnh

- CADCraft ghi được DXF 2000 đến 2018. Lệnh lưu nhận phiên bản và dạng nhị
  phân hay chữ. [tài liệu] Tên tham số chính xác lấy từ danh mục. Sau khi
  lưu, kiểm `$ACADVER` trong file là `AC1032`.
- Từ bản 2007 chữ mới được lưu UTF-8. Bản thấp hơn dùng bảng mã cũ, nên chữ
  có dấu không được lưu dưới 2007. [tài liệu]
- Ảnh nền trắng có độ dày nét: lệnh `plot {"path": "x.png", "device":
  "CADCraft PNG", "fit": true, "plotArea": "extents" | "window", "window":
  [[x0,y0],[x1,y1]], "lineweights": true}`. `--export` và `convert` không có
  tuỳ chọn nền. [bản 0.20.1] Ảnh ra khổ A4 300 dpi, 3508×2480 (ngang) hoặc
  2480×3508 (đứng). [bản 0.20.1]
- Ảnh PNG bỏ phần mảnh của một đường nhiều đoạn có cả đoạn rộng. File vẫn
  đủ. [bản 0.20.1]
- Xuất ảnh nhanh: `--export` hoặc lưu tới đường dẫn `.png`, `.pdf`, `.svg`. PNG
  2400×1600, `--window` cắt đúng một vùng. Tool `render` nhận nền
  (`white`, `dark`, `paper`) và bảng nét (`monochrome.ctb`). [tài liệu]
- Ảnh PNG hiện chữ số kích thước, tô đặc và nét đứt. Nền mặc định là nền tối.
  [bản 0.20.1] Ở bản 0.20.0 một phiên làm việc từng thấy ảnh thiếu các thứ
  này, nên vẫn đừng kết luận bản vẽ sai chỉ từ một ảnh thiếu.
- Máy không có font của kiểu chữ thì ảnh vẽ bằng font nét của CADCraft, và
  ký tự có dấu lấy từ một font khác nên trông lệch. File vẫn ghi đúng tên
  font. [bản 0.20.1] Xem ảnh để soát hình, đừng dùng nó để soát chữ.

## Bẫy đã biết

| Thứ | Điều đã biết | Làm gì |
|---|---|---|
| Màu layer | Nhận tên màu như `White`, `Red`, và nhận cả số màu như 7, 8. [bản 0.20.1] | Dùng số màu khi cần màu không có tên. |
| Độ dày nét của layer | `layer.new` nhận `lineweight` theo milimét và `linetype`. Kiểu nét phải nạp trước bằng lệnh `linetype`. [bản 0.20.1] | Đặt cả hai ngay khi tạo layer. |
| Cung | Góc đầu và cuối tính bằng độ. [bản 0.20.0] | — |
| Tạo block | `block` mặc định `keep: "convert"`, biến hình gốc thành một bản chèn ở toạ độ gốc. [bản 0.20.1] | Tạo block từ hình vừa vẽ thì đặt `keep: "delete"`. |
| Tự cắt | `shapes` coi hai cạnh chạm nhau tại một đỉnh là `selfIntersection`. [bản 0.20.1] | Tách thành hai đường. |
| Mở SVG | Mở một file `.svg` thì mọi chữ bị bỏ ("texts left out"), chỉ còn hình. `convert x.svg x.png` cũng bỏ chữ và ra nền tối; muốn nền trắng thì mở SVG rồi gọi `plot`. [bản 0.20.1] | Xem sơ đồ duyệt qua CADCraft chỉ để soát hình; chữ kiểm bằng số trong `preview.py`. |
| Đỉnh và tên block | Ở `entities`, đỉnh đường nhiều đoạn là `{"x","y"}`, không phải mảng; tên block ở `geometry.block`. [bản 0.20.1] | — |
| Tên trường trả về | Ở `entities`, điểm chèn của block nằm ở `geometry.insert`, điểm đo của kích thước ở `p13`, `p14`, số đo ở `measurement`. `info` trả `extents`. [bản 0.20.1] | — |
| Dời chữ kích thước | `dimtedit {at}` với `DIMTMOVE` mặc định kéo cả đường kích thước theo. [bản 0.20.1] | Đặt `DIMTMOVE` bằng 2 trong kiểu kích thước. |
| Khổ ảnh | `plot` với `fit` mặc định dùng giấy ngang. [bản 0.20.1] | Ảnh một tầng đứng thì thêm `landscape: false`. |
| Lọc đối tượng | `entities` lọc theo tên DXF (`INSERT`, `LINE`) nhưng trả tên khác (`Block Reference`, `Line`). Đầu mút nét ở `geometry.a`, `geometry.b`; đỉnh đường nhiều đoạn ở `vertices[].p`. [bản 0.20.1] | — |
| Font trong ảnh | `--fontalt` với một font TrueType có trên máy không đổi chữ trong ảnh khi file đã ghi tên font: ảnh vẫn vẽ bằng font nét. [bản 0.20.1] | Soát chữ đè bằng `dxf_check.py`, không bằng ảnh. |
| Chữ một dòng | `text` không nhận `style`, dùng kiểu chữ hiện hành; `mtext` nhận `style`. [bản 0.20.1] | Đặt kiểu chữ hiện hành trước khi viết `text`, hoặc dùng `mtext`. |
| Kích thước bám hình | `dimlinear` có `p1`, `p2` trùng đỉnh hình thì tự gắn liên kết với hình đó. [bản 0.20.1] | Lấy điểm đo từ chính đỉnh tường, cột. |
| Canh chữ nhiều dòng | `mtext` nhận `attach` từ 1 tới 9: 1 trên trái, 2 trên giữa, 3 trên phải, 4 giữa trái, 5 chính giữa, 6 giữa phải, 7 dưới trái, 8 dưới giữa, 9 dưới phải. [bản 0.20.1] | — |
| Lệnh không có kết quả | `layer.new`, `layer.current`, `layer.set`, `ltscale`, `properties.set` không in dòng nào. `block` trả `{"block", "insert": null}`, không có mã đối tượng. [bản 0.20.1] | Đếm dòng kết quả thì đừng tính các lệnh này. |
| Tên kiểu nét | `linetype {"load": "*"}` nạp cả thư viện. Nét đứt là `HIDDEN` hoặc `DASHED`, chấm gạch là `CENTER`, hai chấm gạch là `PHANTOM`. [bản 0.20.1] | — |
| Kiểu kích thước | `dimstyle` nhận thẳng tên biến `DIM*` (`DIMSCALE`, `DIMTSZ`, `DIMTXSTY`, `DIMTMOVE`…). Kết quả `dimlinear` có `geometry.assoc`, `defpt`, `kind.linear.rotation`. Kích thước đứng dùng `rotation: 90`. [bản 0.20.1] | — |
| Kết quả `audit` và chữ kích thước | `audit` trả `{errors, fixed, issues, message}`. Ở `entities`, kích thước có `textMid`, chỗ chữ số thật sự nằm. `saveas` có thêm cờ `portableFonts`. [bản 0.20.1] | Dùng `textMid` để biết số nào bị đẩy ra ngoài. |
| Tên công cụ | `find_text`, `query_entities`, `inspect_drawing` là tên tool MCP. Ở dòng lệnh là `texts`, `entities`, `cadcraft-cli info`. [bản 0.20.1] | Dùng tên theo cách đang gọi. |
| Đổi thuộc tính từng đối tượng | `properties.set` đổi kiểu nét của một đối tượng, `layer.set {plot: false}` tắt in một layer. [bản 0.20.1] | Dùng cho vòng tên trục và `X-AREA`. |
| Kiểu chữ TrueType | `style` báo `trueType: false` cho cả `Arial` lẫn `arial.ttf`. [bản 0.20.1] | Tin tên font ghi trong file, không tin cờ này. |
| Lệnh từ chương trình | Không bao giờ mở hộp thoại, chạy với mặc định. [tài liệu] | Truyền đủ mọi tham số cần. |
| Chú thích tự co giãn theo tỷ lệ | Còn thiếu nhiều phần, và đọc lẫn với AutoCAD. [tài liệu] | Không dùng. Cỡ chữ tính từ tỷ lệ. |
| Block động | Chưa tạo được. [tài liệu] | Mỗi cỡ cửa một block thường. |
| Kiểu nét có hình | Phần hình bị bỏ khi nạp. [tài liệu] | Chỉ dùng nét liền, đứt, chấm gạch. |

## Rủi ro khi mở trong AutoCAD

Chính dự án CADCraft ghi rằng họ chưa kiểm có hệ thống việc file của họ mở
sạch trong AutoCAD. [tài liệu] Mỗi mục dưới đây, nếu có mặt trong bản vẽ, đi
vào phần thứ hai của danh sách giao.

| Thứ | Điều đã biết | Làm gì |
|---|---|---|
| Cả file | AutoCAD LT 2026 từng treo với một file DXF 2000 của CADCraft, đã sửa. [tài liệu] | Lưu 2018. Việc đầu trong AutoCAD là chạy lệnh kiểm lỗi rồi lưu DWG. |
| Font | CADCraft chưa đọc font SHX, nên bề rộng chữ khác AutoCAD. [tài liệu] | Dùng font TrueType Unicode. Chừa lề quanh chữ, không đặt chữ vừa khít. |
| Mẫu tô | Thư viện có 23 mẫu riêng, khác bộ của AutoCAD. [tài liệu] | Ưu tiên tô đặc. Mẫu có nét thì ghi vào danh sách cần mắt người. |
| Bảng | Công thức và kiểu ô không đi theo file. [tài liệu] `ezdxf` đọc bảng ra 0 dòng. [bản 0.20.0] | Không dùng đối tượng bảng. |
| Kích thước | Ghi kèm block ẩn danh và liên kết với hình. [tài liệu] Kéo giãn trong AutoCAD có bám theo không. [chưa thử] | Ghi vào danh sách cần mắt người. |
| Chú thích có mũi tên kiểu mới | Vị trí chữ còn phải kiểm trong AutoCAD. [tài liệu] | Dùng chữ thường và nét dẫn. |
| In | Chưa đọc được bảng nét nhị phân của AutoCAD. [tài liệu] | Trang in để AutoCAD làm. |

## Bản thử đầu tiên trên một phiên bản mới

Dựng một file nhỏ có mỗi loại một đối tượng, rồi ghi kết quả từng dòng vào
file ghi chép:

1. Chạy không kèm file: bản vẽ mới có hệ mét không, đơn vị trong file lưu ra
   là gì.
2. Một khối tường khép kín, một mẫu tô đặc và một mẫu có nét. Lệnh tô nhận
   biên bằng mã đối tượng, danh sách điểm, hay điểm chọn bên trong.
3. Một block cửa và hai lần chèn.
4. Một kích thước ngang và một kích thước đứng với hệ số theo tỷ lệ.
5. Một dòng chữ có dấu bằng font TrueType, và một đoạn nét đứt với độ thưa đã
   đặt.
6. Lưu 2018, mở lại bằng một lần chạy khác, gọi từng lệnh đo và ghi tên các
   trường trả về.
7. Kiểm chữ có dấu còn nguyên sau khi mở lại.
8. Xuất PNG nền trắng và PDF. Ghi cái gì hiện ở ảnh nào.
9. Chạy trình kiểm lỗi của CADCraft và script kiểm DXF của skill. Cả hai
   phải báo không lỗi. Chỗ nào script báo sai trong khi file đúng thì ghi lại
   để sửa script.
10. Cố ý cho một lệnh sai tham số giữa chuỗi. Ghi lần chạy có dừng không và
    mã thoát là gì.

Phép thử cuối chỉ người làm được: mở file thử trong AutoCAD thật và điền
[phieu-duyet.md](phieu-duyet.md). Mời người dùng làm phép này một lần cho mỗi
dự án đầu tiên trên một phiên bản mới, và ghi kết quả họ báo vào file ghi
chép.
