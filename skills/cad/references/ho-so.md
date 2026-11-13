# Thư mục dự án và file `project.md`

Đọc file này khi lập một dự án mới hoặc mở lại một dự án cũ.

## Thư mục

`docs/iflow/<tên-dự-án>-<id>/cad/`. `<tên-dự-án>` là tên người dùng gọi dự
án. Họ không đặt tên thì lấy loại công trình và nơi xây, viết thường không
dấu, nối bằng gạch ngang, ví dụ `quan-ca-phe-da-lat`. `<id>` là bốn ký tự từ
`openssl rand -hex 2`, để người dùng gọi dự án bằng id. Skill này chỉ ghi
trong `cad/`. Không đặt dự án mới vào một thư mục có sẵn vì đoán là cùng
việc.

| File | Là gì | Sinh ra khi nào |
|---|---|---|
| `project.md` | Điều đang biết, quyết định, câu còn hỏi, trạng thái. | Đầu lượt đầu, ngay từ đề bài, trước khi tra cứu. |
| `layouts.json`, `layout-<tên>.svg` | Số của từng cách xếp đang so, và sơ đồ đúng tỷ lệ của từng cách. | Khi làm sản phẩm 4. |
| `params.json` | Bảng số của cách xếp đã chọn. | Khi làm sản phẩm 5. |
| `preview.py`, `preview.svg` | Script sinh sơ đồ và sơ đồ đúng tỷ lệ cho người duyệt. Script chỉ đọc `layouts.json` hoặc `params.json`, không chứa số hình học nào. | Từ sản phẩm 4. Sơ đồ sinh lại mỗi lần số đổi. |
| `phieu.json` | Phiếu đề bài: các số của đề bài và nguồn của chúng, theo khuôn ở [phieu.md](phieu.md). `project.md` vẫn ghi mọi dữ kiện; phiếu chép lại số để máy kiểm. | Đầu lượt đầu, cùng `project.md`. Dự án cũ chưa có thì thôi. |
| `build.py` | Bản chép của `lib/build_mau.py` trong skill, chỉ sửa phần riêng của dự án. | Khi làm sản phẩm 7. |
| `check.py` | Chỉ khi dự án có phép kiểm riêng mà `dxf_check.py` và `plan_check.py` không làm. | Khi cần. |
| `out/<tên>-NN.dxf` và ảnh | Mỗi lần dựng một số NN mới. Không ghi đè file đã giao. | Mỗi lần dựng. |
| `review.md` | Phiếu duyệt bản vẽ, người dùng điền sau khi mở file trong AutoCAD. | Khi giao. |
| `cadcraft-<phiên-bản>.md` | Ghi chép dò CADCraft của bản đang cài. | Lần đầu vẽ, và khi phiên bản đổi. |

Một sản phẩm ngắn hơn chừng 40 dòng nằm ngay trong `project.md`. Dài hơn,
hoặc không phải chữ, thì thành file riêng bên cạnh và bảng trạng thái trỏ
tới.

**File nào thắng.** Quyết định trong `project.md` thắng `params.json`. Hai
bên lệch thì sửa bảng số theo quyết định, rồi dựng lại. `params.json` thắng
mọi file dựng ra từ nó.

## Ghi lúc nào

Ghi trong chính lượt mà điều đang biết, một quyết định, một câu hỏi hay một
trạng thái thay đổi. Ghi trước, làm sau. Lượt không đổi gì thì không ghi.

Mỗi lần ghi, viết lại phần bị chạm để file nói bức tranh hôm nay như thể
viết một lần. Không để lại dấu vết kiểu "trước đây là…", trừ lựa chọn đã bỏ
trong dòng quyết định.

Một kết luận đứng trên giả định chưa xác nhận phải mang giả định đó ngay tại
chỗ nó được nêu.

## Mẫu `project.md`

Tiêu đề viết bằng ngôn ngữ của người dùng và nói đúng thứ mục đó chứa. Tên
trong ngoặc nhọn là vai trò, không phải nhãn. Các nhãn trong khối trạng thái
cuối file giữ nguyên tiếng Anh.

```markdown
---
project: <tên dự án bằng lời người dùng>
status: active
updated: <YYYY-MM-DD>
---
# <tên dự án>

## <Đang ở đâu>
Hai đến bốn câu: thiết kế gì, cho ai, ở đâu, đã chốt gì, đang chờ gì.

## <Điều đã chốt>
- <chọn gì>. <người dùng nói | người dùng giao AI chọn>. Dựa trên: <căn cứ>.
  Đã bỏ: <lựa chọn kia>, vì <lý do>.

## <Điều đang biết>
### <Loại công trình và nơi xây>
### <Người dùng công trình và nhu cầu>
### <Đất hoặc phần nhà có sẵn>
### <Luật, khí hậu, địa hình nơi xây>
### <Tiền và thời hạn>
### <Cách vẽ của văn phòng>
### <Phác thảo hoặc ý tưởng của người dùng>
- <nội dung>. <mức chắc>.

## <Các sản phẩm đã làm>
Mỗi sản phẩm một mục con, đặt tên theo thứ nó chứa. Sản phẩm dài hoặc không
phải chữ thì mục con chỉ có một dòng trỏ tới file.

## <Còn phải hỏi, còn phải tra>
- <câu hỏi>. Đổi được gì. Ai trả lời được: <người dùng | tra tiếp>.
  Đang tạm tính thế nào.

## <Nguồn>
- <tên văn bản hoặc đường dẫn>. Chống đỡ cho điều gì. Ngày đọc.

## <Trạng thái cho phiên sau>
| # | Product | Status | Where | Weakest ground |
|---|---|---|---|---|
| 1 | <tên sản phẩm bằng lời thường> | missing | — | — |

Next action: <một câu mệnh lệnh làm được ngay>
Drawing tool: <tên lệnh và phiên bản tìm thấy | not installed>
Working with this user: <điều họ đã dặn về cách làm>
```

## Mức chắc của một điều đang biết

Mỗi dòng mang đúng một trong năm mức, xếp từ chắc xuống yếu:

- **Người dùng nói.** Lời của chính họ, kể cả đề bài lúc gọi skill.
- **Văn bản gốc.** Đã mở chính văn bản và đọc được điều khoản. Kèm tên văn
  bản, điều khoản, ngày đọc. Với luật và quy chuẩn, ghi đã kiểm còn hiệu lực
  ở đâu: cơ quan ban hành hoặc cơ sở dữ liệu pháp luật chính thức. Chưa kiểm
  thì ghi "chưa kiểm hiệu lực".
- **Nguồn thuật lại.** Bài báo, bài tư vấn, trang tổng hợp nói về một văn
  bản hay một số liệu mà chưa mở được bản gốc. Kèm đường dẫn và ngày đọc.
- **Thông lệ hoặc mặc định.** Cách làm quen thuộc của nghề ở nơi xây, hoặc
  mặc định của skill. Không phải luật.
- **AI ước lượng.** Điều AI biết hoặc tính ra mà chưa có nguồn. Kèm một vế
  "sai thì đổi gì".

Điều AI biết khá chắc, như hướng nắng theo vĩ độ hay mùa mưa của một vùng,
thì ghi là AI ước lượng và dùng, không để trống. "Chưa tìm được" chỉ dành cho
điều đã tra mà không ra và AI cũng không biết. Điều chưa tra tới ghi "chưa
tra". Cả hai thành một dòng trong phần còn phải hỏi, còn phải tra.

Số đo của thế giới thật (đất, nhà có sẵn, nền đất) không có mức ước lượng:
ô "đang tạm tính" của câu hỏi về chúng ghi "không tạm tính". Ngoại lệ duy
nhất là khi người dùng ra lệnh cứ vẽ, theo mục "Asking" trong SKILL.md. Khi
đó mỗi số đặt tạm được ghi "giả định theo lệnh người dùng", câu hỏi về nó
vẫn nằm trong phần còn phải hỏi, và mọi sản phẩm đứng trên nó mang chữ "giả
định".

Chỉ lời của chính người dùng mới nâng một suy đoán lên thành "người dùng
nói": điều họ tự nêu, câu trả lời khẳng định, hoặc một mệnh lệnh. Câu hỏi,
lời nước đôi, lời khen và im lặng thì không.

## Bảng trạng thái

Bảng dựng lúc lập dự án từ bảy sản phẩm trong SKILL.md, tên sản phẩm viết
bằng lời thường của người dùng. Cột "Weakest ground" ghi căn cứ kém chắc
nhất mà sản phẩm đang đứng trên, và ghi `—` khi sản phẩm chưa làm. Đây là
danh sách phải đọc ra trước mỗi lần xin duyệt.

`Next action:` đổi ngay khi việc kế tiếp đổi, không đợi cuối lượt. Khi đang
chờ người dùng, nó nói đang chờ câu trả lời nào và việc gì làm được trong
lúc chờ. Dự án đã giao xong thì `status: done` ở đầu file và `Next action:`
trỏ tới danh sách giao.

## Kiểm trước khi rời file

Một người chưa thấy hội thoại đọc file từ trên xuống phải trả lời được:

- Đang thiết kế gì, cho ai, ở đâu.
- Điều gì đã chốt, và lựa chọn nào đã bỏ.
- Điều gì là sự thật có nguồn, điều gì là ước lượng.
- Còn thiếu thông tin gì, ai có nó.
- Việc kế tiếp là gì.

Câu nào phải mở lại hội thoại mới trả lời được thì file chưa xong.
