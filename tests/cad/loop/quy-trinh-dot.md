# Đổi i:cad theo đợt

Skill không đổi sau mỗi vòng thử. Mỗi vòng chỉ ghi lỗi vào
[sổ quan sát](so-quan-sat.md); cứ vài vòng thì sửa một đợt, và đợt đó chỉ được
giữ khi điểm trên bộ đề giữ riêng không tụt. Lý do: chín vòng đầu vá chữ sau
mỗi vòng, và hai lần luật mới đá luật cũ (vòng 4 bỏ đoạn bề dày tường khỏi
chuỗi kích thước làm hỏng luật "chuỗi khép kín"; vòng 8 gỡ hai luật khoảng
cách tầng chọi nhau). Lỗi của một đề cũng bị vá thành luật chung.

## Một vòng thử

1. Một agent chưa thấy hội thoại dựng bản vẽ theo skill, với một đề trong
   [bộ luyện](de/README.md). Prompt là [prompt.md](prompt.md).
2. Phiên chính duyệt theo [review.md](review.md) và ghi mỗi lỗi một dòng vào
   sổ quan sát. Không sửa gì.
3. Chấm theo [thang chung](thang-chung.md) nếu cần điểm của vòng đó.

## Khi nào sửa một đợt

Sau khoảng ba vòng luyện. Hoặc ngay lập tức khi có lỗi làm file hỏng hay mở
không được: lỗi đó sửa một mình, thành một đợt riêng.

## Sáu bước của một đợt

1. **Gom** mọi dòng của sổ có cột "Đợt" còn trống.
2. **Đưa mỗi dòng về đúng một lớp**, theo thứ tự ưu tiên dưới đây. Dòng chỉ
   đúng với một đề thì ghi "để người dùng chỉnh" vào cột "Đợt" và không sửa.
3. **Sửa**, rồi chạy `tests/cad.sh` (bài tự thử của thư viện và các trình
   kiểm). Một phép kiểm mới đi kèm một bản có lỗi cài sẵn; một hàm sửa đi kèm
   bài thử trong `tests/cad/lib_selftest.py`.
4. **Chạy bộ đề giữ riêng**, mỗi đề một lần, chấm bằng thang chung.
5. **Giữ hay bỏ cả đợt.** Giữ khi tổng điểm không giảm quá mức nhiễu và không
   mục máy chấm nào (phần A) tụt. Ngược lại bỏ cả đợt: `git revert` các commit
   của đợt, ghi lý do vào cột "Đợt".
6. **Ghi** phiên bản skill (commit) và điểm vào [bảng điểm](bang-diem.md).

## Thứ tự ưu tiên khi đưa một lỗi về lớp

1. Lỗi đo được trên file thì thành **phép kiểm** trong `skills/cad/scripts/`.
2. Lỗi cách vẽ thì sửa **hàm thư viện**, **block** hay **file mẫu**.
3. Lỗi vì bảng số thiếu một trường thì sửa **khuôn bảng số**.
4. Chỉ khi ba cách trên không làm được mới thành **chữ** trong `references/`.

Một câu chữ mới phải qua hai cửa: lỗi đã gặp ở ít nhất hai loại công trình
(đọc ở cột "Loại công trình" của sổ), và câu đó đã thử trên một đề khác với đề
làm lộ ra lỗi.

## Bộ đề giữ riêng là đề thi kín

Với đề giữ riêng, người sửa skill chỉ xem điểm và số lỗi theo nhóm (A, B, C,
D), không đọc chi tiết lỗi, không mở bản vẽ. Đọc chi tiết rồi sửa theo thì đề
đó thành đề luyện, và điểm trên nó không còn nói gì về đề mới. Khi chuyện đó
xảy ra, chuyển đề sang `de/luyen/`, ghi vào bảng điểm, và nhờ một agent chưa
đọc skill viết đề mới thay chỗ.

## Nhiễu

Cùng một đề chạy hai lần không ra cùng một điểm. Trước khi dùng điểm để giữ
hay bỏ một đợt, chạy mỗi đề giữ riêng hai lần để đo độ lệch đó, ghi vào bảng
điểm. Chênh lệch giữa hai đợt nhỏ hơn độ lệch đo được thì coi là bằng nhau.
