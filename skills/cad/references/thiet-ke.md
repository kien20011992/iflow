# Từ đề bài tới các cách xếp

Đọc file này trước khi làm sản phẩm 1 đến 4: nhu cầu, giới hạn có sẵn, phép
tính sổ, các cách xếp. File không chứa con số của luật nào. Nó nói phải tìm
loại thông tin gì, hỏi ai, lúc nào, và mỗi sản phẩm phải bày ra cái gì.

## Tra gì, hỏi gì, lúc nào

Luật, khí hậu và cách xây của đúng nơi xây là dữ kiện chính. Nơi khác chỉ để
so sánh và phải ghi rõ là so sánh.

Mỗi sản phẩm tra và hỏi đúng thứ nó cần, lúc bắt đầu làm nó. Không quét hết
ngay từ đầu.

| Làm sản phẩm | Tra | Hỏi người dùng |
|---|---|---|
| 1, nhu cầu | Luật riêng của loại công trình: phòng bắt buộc, diện tích tối thiểu. | Ai dùng, bao nhiêu người, có người già, trẻ nhỏ hay người đi xe lăn không. Một ngày ở đó diễn ra thế nào. Vài năm nữa có đổi không. |
| 2, giới hạn, khi xây mới | Luật quy hoạch áp cho lô: lùi, phần đất được phủ, số tầng và chiều cao. Luật mở cửa về phía đất người khác. Nắng, gió, mưa, ngập của nơi xây. Thiên tai của vùng: động đất, bão, và sóng thần với nơi ven biển, kèm luật thiết kế cho nó. Khí hậu cũng cần nguồn, không chỉ ước. | Hình lô đất có kích thước từng cạnh theo giấy tờ, hướng bắc, cạnh nào giáp đường và đường rộng bao nhiêu, bên kia mỗi cạnh còn lại là gì, đất cao hay thấp hơn đường. Giấy ghi chỉ tiêu riêng của lô, nếu có. |
| 2, giới hạn, khi cải tạo | Luật cho việc đổi công năng, nếu có đổi. | Bản vẽ hoặc số đo nhà đang có: tường và cột nào chịu lực, dầm ở đâu, chiều cao từng tầng, vị trí ống nước và hộp kỹ thuật, cửa sổ hiện có. |
| 3, tính sổ | Đơn giá xây của nơi đó và năm đó. | Có bao nhiêu tiền cho phần xây, xây một đợt hay nhiều đợt, khi nào cần xong. |
| 4, cách xếp | Kích thước thang, lối thoát, chiếu sáng và thông gió theo luật. Thông lệ xây tại chỗ: tường bằng gì dày bao nhiêu, khung chịu lực và nhịp cột thường gặp, chiều cao tầng quen dùng. | Thứ tự ưu tiên khi hai nhu cầu đụng nhau. |

Tra tới khi sản phẩm đang làm có đủ căn cứ cho từng dòng của nó, hoặc khi đã
thử ba cách tìm khác nhau cho một điều mà không ra. Điều tra không ra thành
một dòng trong phần còn phải tra, và sản phẩm vẫn được bày ra với mức chắc
ghi rõ.

Luật hỏi:

- Không hỏi điều đề bài đã nói. Không hỏi điều tra được.
- Số tròn trong đề bài ("lô 5×18 m") được ghi là người dùng nói và dùng
  ngay. Khi một ngưỡng của luật phụ thuộc vào số đó, xin thêm số theo giấy
  tờ.
- Một giải pháp nêu sẵn trong đề bài ("ba tầng", "bốn phòng ngủ") được ghi
  là người dùng nói, rồi hỏi nhu cầu đứng sau nó ("vì sao ba tầng", "ai ngủ ở
  đâu"). Câu trả lời cho biết khi không vừa thì nên bớt gì.
- Câu hỏi về cách vẽ thuộc sản phẩm 5, xem [ve.md](ve.md).

## Chuẩn cho mọi thông tin tìm về

Một thông tin chỉ được giữ khi nó ràng buộc một quyết định, và phải ghi kèm
quyết định đó. Ví dụ: "nắng gắt buổi chiều đến từ hướng tây, nên mặt tây ít
cửa kính". Thông tin không đổi quyết định nào thì bỏ.

- Mỗi thông tin ghi nguồn, ngày đọc và một trong năm mức chắc, theo
  [ho-so.md](ho-so.md).
- Bản tóm tắt mà công cụ đọc web trả về chưa phải là đã đọc văn bản gốc. Muốn
  ghi mức "văn bản gốc" thì phải lấy được nguyên văn điều khoản: yêu cầu công
  cụ trích nguyên văn kèm số điều, hoặc tải file về đọc. Không lấy được thì
  mức chắc là "nguồn thuật lại".
- Số hiệu văn bản nhớ từ trước không phải nguồn. Phải mở ra đọc, và kiểm nó
  còn hiệu lực.
- Con số gánh một kết luận mang theo mức chắc của nó ở mọi nơi nó xuất hiện,
  kể cả trong tin nhắn và trên sơ đồ.
- Kích thước đất, hiện trạng nhà và nền đất không bao giờ được ước. Chúng chỉ
  đến từ người dùng.

Các hướng tra độc lập nhau có thể giao cho agent theo luật trong SKILL.md.

## Sản phẩm 1: nhu cầu

Bày ra một bảng phòng. Mỗi phòng một dòng:

- Tên phòng và ai dùng.
- Việc diễn ra trong phòng, và đồ đạc lớn nhất phải vừa.
- Diện tích hoặc kích thước cần, kèm nó đến từ đâu: luật, thông lệ, hay lời
  người dùng.
- Phòng nào nó phải gần, phòng nào phải xa.
- Điều kiện riêng: tầng trệt cho người già, ánh sáng tự nhiên, yên tĩnh.

Cuối bảng là tổng diện tích phòng, cộng phần cho lối đi, thang và tường. Tỷ
lệ cộng thêm là thông lệ, ghi rõ con số đã dùng.

Tách điều phải có khỏi điều muốn có, vì bước tính sổ sẽ cắt từ nhóm sau.

Khi chưa biết đủ về người dùng công trình, vẫn bày một bảng nháp từ đề bài và
ghi dòng nào là đoán. Người dùng sửa một bảng nháp nhanh hơn trả lời một dãy
câu hỏi.

Loại công trình có luật riêng thì luật đó thêm phòng bắt buộc và diện tích
tối thiểu theo đầu người vào bảng. Ghi rõ dòng nào do luật buộc.

## Sản phẩm 2: giới hạn có sẵn

**Khi xây mới**, bày ra phần được phép xây như một cái hộp bằng số:

- Hình lô đất, và phần còn lại sau khi trừ các khoảng phải lùi.
- Diện tích tối đa được phủ ở mặt đất.
- Số tầng hoặc chiều cao tối đa, và phần được vươn ra ngoài như ban công.
- Cạnh nào được mở cửa sổ, cạnh nào sát đất người khác.
- Lối vào cho người và xe.

Kèm theo đó là các ràng buộc từ khí hậu và địa hình, mỗi cái gắn với một
quyết định: mặt nào đón nắng gắt, gió mát đến từ đâu, nước mưa chảy về đâu,
nền phải cao hơn đường bao nhiêu.

**Khi cải tạo**, giới hạn là nhà đang có: thứ không dời được (tường và cột
chịu lực, dầm, hộp kỹ thuật, ống thoát), thứ dời được nhưng đắt (khu vệ sinh,
bếp), và thứ dời tự do.

Khi nhà chưa được đo, bản nháp đầu của sản phẩm này là một danh sách thứ cần
đo và chụp ảnh, làm được trong chừng mười phút, xếp theo mức nó đổi cách xếp:
kích thước bao, tường và cột bên trong, chỗ có ống nước, cửa và cửa sổ, chiều
cao trần, cạnh nào giáp đường và hai bên là gì.

Mỗi dòng trong sản phẩm này ghi mức chắc. Cái hộp tính từ luật chung khi chưa
có chỉ tiêu riêng của lô vẫn được bày ra, với chữ "ước lượng" ngay trên sơ
đồ.

## Sản phẩm 3: phép tính sổ

Viết phép tính ra, không chỉ kết quả:

- Diện tích cần (từ sản phẩm 1) so với diện tích được xây (diện tích phủ nhân
  số tầng, từ sản phẩm 2).
- Chi phí ước bằng diện tích sàn nhân đơn giá. Đơn giá phải có nguồn và năm.
  Không có nguồn thì ghi là ước lượng và nói khoảng dao động.
- Thời hạn, nếu người dùng có nêu.

Kết luận là một trong ba: vừa, vừa sát (nói rõ sát ở đâu), không vừa.

Không vừa thì dừng và hỏi ngay, trước khi nghĩ cách xếp nào. Bày các lối đi
kèm cái giá: bớt phòng nào trong nhóm "muốn có", thêm tầng, thêm tiền, hoặc
xây làm nhiều đợt. Không tự thu nhỏ phòng cho vừa mà không nói.

## Sản phẩm 4: các cách xếp

Làm theo ba việc, bày kết quả của từng việc.

**Một, quan hệ giữa các phòng, chưa có tường.** Mỗi phòng một hình, nối các
phòng phải gần nhau. Đánh dấu các cặp đối nghịch: chung và riêng, ướt và khô,
ồn và yên, sạch và bẩn. Vẽ đường đi chính: từ cửa vào tới từng nhóm phòng,
đường mang đồ, đường của khách.

**Hai, đặt những thứ khó dời.** Chúng quyết định mọi thứ còn lại, nên phải
tính kích thước trước khi chia phòng:

- **Thang.** Số bậc nhân chiều cao bậc phải bằng chiều cao tầng. Từ số bậc
  suy ra ô thang dài rộng bao nhiêu. Giới hạn của chiều cao bậc, bề rộng mặt
  bậc và bề rộng thang lấy từ luật nơi xây. Chưa tra ra thì chọn theo thông
  lệ, ghi là AI chọn, và đưa vào phần còn phải tra.
- **Khu ướt.** Bếp và vệ sinh các tầng nên chồng thẳng nhau để ống đi một
  trục.
- **Kết cấu.** Lưới cột hoặc tường chịu lực theo thông lệ nơi xây. Cỡ cột,
  dầm, sàn là ước theo thông lệ để vẽ, ghi rõ là ước, kỹ sư sẽ tính.
- **Nguồn sáng và gió.** Nhà sâu hoặc bị kẹp hai bên cần chỗ lấy sáng ở giữa.
- **Lối vào.**

**Ba, bày hai đến bốn cách xếp.** Chuẩn cho mỗi cách và cho cả bộ:

- Các cách khác nhau từ gốc: khác chỗ đặt thứ khó dời, khác cách tổ chức. Hai
  cách chỉ khác chi tiết tính là một cách có biến thể.
- Khi hợp lý, một cách là "làm ít hơn": giữ nguyên nhiều nhất, hoặc xây một
  phần trước.
- Mỗi cách đã qua phép tính sổ và các giới hạn trước khi được bày. Cách nào
  vướng thì không bày, hoặc bày kèm chỗ vướng ghi rõ.
- Trong mỗi cách, mọi phòng đều có lối vào mà không phải đi xuyên một phòng
  riêng tư khác.
- Mỗi cách có một sơ đồ đúng tỷ lệ, vài dòng lý do truy về sự thật đã ghi, và
  một dòng nói nó phải bỏ cái gì.
- Mỗi cách nói nó xử lý nắng, gió, mưa của nơi xây thế nào.
- Cả bộ được so trên cùng thước đo: diện tích từng phòng so với nhu cầu, phần
  trăm diện tích dùng được, chỗ nào sát hoặc vướng luật, ước chi phí.
- Nêu cách đang nghiêng về, kèm lý do gắn với hoàn cảnh của dự án. Không bày
  một dãy lựa chọn rồi để người dùng tự gánh.

Số của từng cách xếp ghi vào `layouts.json`, và sơ đồ sinh từ file đó, theo
[ho-so.md](ho-so.md).

Khi đất hoặc nhà có sẵn mới chỉ là giả định, không bày nhiều cách xếp đúng
tỷ lệ: hình trông chính xác hơn mức nó xứng đáng. Bày một sơ đồ chia khu thô,
mang chữ "giả định", kèm điều gì trong số đo thật sẽ đổi nó. Các cách xếp
đúng tỷ lệ chờ số đo. Ngoại lệ là khi người dùng ra lệnh cứ vẽ: các cách xếp
đúng tỷ lệ được bày, chữ "GIẢ ĐỊNH" nằm ngay trên mặt mỗi sơ đồ.

Dự án nhiều căn có hai cấp. `layouts.json` xếp các khối trên khu đất: số
khối, số căn, mật độ, phần trăm đất phủ, sân chung và lối đi. Mỗi cách xếp
còn có một khối mẫu đủ số để tính sổ. Cách được chọn đi vào `params.json`
dưới dạng một cụm đặt lặp, theo [bang-so.md](bang-so.md).

Chọn cách nào là chỗ xin duyệt thứ nhất trong SKILL.md.

Khi người dùng mang phác thảo riêng, sản phẩm này được bỏ qua và việc bắt đầu
ở bảng số, theo mục "Where to start" trong SKILL.md. Chỉ hỏi họ có muốn xem
thêm cách xếp khác không khi phác thảo vướng một giới hạn mà sửa nhỏ không gỡ
được, và hỏi đúng một lần.

## Khi tiền không đủ cho công trình hoàn chỉnh

Mục này chỉ áp khi phép tính sổ cho thấy tiền không đủ xây hết nhu cầu, và
người dùng chọn xây làm nhiều đợt hoặc để người ở tự hoàn thiện. Nhà ở xã hội
và nhà tự xây dần thường rơi vào đây. Các dự án khác bỏ qua mục này.

- Tính sổ ở hai mức: từng căn, và cả khu đất. Mọi khoản tiền của một căn,
  đất, hạ tầng, xây, đổi ra m² theo đơn giá có ghi nguồn, và so với diện tích
  đích. Phần dùng chung, như thang chung, hành lang, sàn ngăn giữa hai căn,
  tính theo đơn giá của chính nó rồi chia theo số căn dùng nó.
- Diện tích giao suy từ tiền xây chia đơn giá, không suy từ lưới trục. Lưới
  cho ra số lớn hơn thì đó là tiền thiếu: nêu số thiếu, và coi nó là câu hỏi
  chặn của lần duyệt thứ nhất. Khi người dùng ra lệnh cứ làm, ghi một lối ra
  tạm (thu nhỏ phần giao, thêm nguồn tiền, bớt căn) kèm chữ "chưa phải quyết
  định của người dùng".
- Sân chung nói rõ thuộc nhóm nào và bao nhiêu căn dùng nó.
- Không thu nhỏ căn nhà cho vừa tiền. Đích là căn nhà đủ chuẩn mà người ở
  muốn có về lâu dài. Mức tối thiểu của chương trình tài trợ chỉ là sàn.
- Thiết kế trạng thái hoàn chỉnh trước, rồi mới chọn phần xây đợt đầu.
- Đợt đầu xây phần mà người ở khó tự làm: kết cấu, thang, khu ướt, tường
  ngăn cháy, mái. Phần để lại là phần dễ tự làm.
- Kích thước ô để lại phải vừa với cách xây thông thường tại chỗ, vừa với kết
  cấu đã có, và đủ chuẩn phòng.
- Phần xây thêm về sau phải nằm trong giới hạn luật ngay từ đầu, để khi xây
  thì hợp lệ.
- Hình dạng đợt đầu phải tự giữ được khoảng chung: sân, lối đi, khoảng sáng.
  Không trông vào quy định cấm lấn chiếm.
- Khi đất đắt, xem cách chồng hoặc ghép nhiều loại căn để chia tiền đất.
- Bản vẽ ghi rõ cấu kiện chờ cho đợt sau, và nói đợt sau được làm gì.
- Nêu mọi đánh đổi: đợt đầu thiếu gì, ai gánh phần còn lại.
