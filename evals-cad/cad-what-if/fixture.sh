#!/usr/bin/env bash
# A town-house project stopped just before drawing: layout chosen by the
# user, number table approved, the plot's planning paper still missing.
# cad-late-fact/fixture.sh is the original of this file — change both together.
set -e
d=docs/iflow/nha-pho-hai-chau-a1b2/cad
mkdir -p "$d"
cat > "$d/project.md" <<'MD'
---
project: Nhà phố Hải Châu
status: active
updated: 2026-11-10
---
# Nhà phố Hải Châu

## Đang ở đâu
Nhà phố ba tầng xây mới trên lô 5×18 m ở phường Hải Châu, Đà Nẵng, cho gia
đình năm người. Cách xếp và bảng số đã được duyệt. Đang chờ máy có công cụ vẽ
để dựng bản vẽ.

## Điều đã chốt
- Thang và giếng trời đặt ở giữa nhà. Người dùng nói. Dựa trên: nhà sâu 18 m
  bị kẹp hai bên, cần sáng ở giữa. Đã bỏ: thang dồn cuối nhà, vì phòng giữa
  nhà tối.
- Phòng ngủ ông bà và vệ sinh riêng ở tầng 1, phía sau. Người dùng nói. Dựa
  trên: ông bà không leo thang. Đã bỏ: phòng ông bà ở tầng 2.
- Ba tầng, mỗi tầng cao 3300. Người dùng nói.

## Điều đang biết
### Loại công trình và nơi xây
- Nhà phố xây mới, phường Hải Châu, Đà Nẵng. Người dùng nói.
### Người dùng công trình và nhu cầu
- Năm người: ông bà, hai vợ chồng, một con 8 tuổi. Người dùng nói.
- Một ô tô, hai xe máy. Người dùng nói.
### Đất
- Lô 5×18 m, cạnh 5 m giáp đường, mặt đường hướng đông. Người dùng nói, chưa
  có giấy tờ.
- Hai cạnh dài và cạnh sau giáp nhà hàng xóm. Người dùng nói.
### Luật, khí hậu, địa hình nơi xây
- Lô không quá 90 m² được xây phủ hết đất. Nguồn thuật lại, chưa mở văn bản
  gốc.
- Đang tính xây hết chiều sâu 18 m, không lùi phía sau. AI ước lượng. Sai thì
  chiều sâu nhà và ô phòng phía sau phải đổi.
### Tiền và thời hạn
- 2,5 tỷ đồng cho phần xây. Người dùng nói.
### Cách vẽ của văn phòng
- Milimét, tỷ lệ 1:100, font Arial, layer mặc định. Mặc định.

## Các sản phẩm đã làm
### Danh sách phòng
| Phòng | Cần | Từ đâu |
|---|---|---|
| Phòng khách và chỗ để xe, tầng 1 | 20 m² | Người dùng nói |
| Bếp và ăn, tầng 1 | 18 m² | Thông lệ |
| Phòng ngủ ông bà, tầng 1 | 12 m² | Người dùng nói |
| Vệ sinh ông bà, tầng 1 | 3 m² | Thông lệ |
| Ba phòng ngủ ở tầng 2 và 3 | 12 m² mỗi phòng | Người dùng nói |
### Phép tính sổ
Cần khoảng 210 m² sàn. Được xây 90 m² mỗi tầng, ba tầng là 270 m². Vừa.
### Bảng số
Nằm ở `params.json`. Tầng 1 từ trước ra sau: khách và để xe (trục A–B, sâu
5 m), thang và giếng trời (B–C, sâu 3 m), bếp ăn (C–D, sâu 5 m), phòng ngủ ông
bà cùng vệ sinh (D–E, sâu 5 m, lọt lòng 4,56 × 4,73 m, tức 21,5 m²).

## Còn phải hỏi, còn phải tra
- Thông tin quy hoạch của lô: khoảng lùi, số tầng. Đổi được chiều sâu nhà. Ai
  trả lời được: người dùng. Đang tạm tính: xây hết 18 m.

## Nguồn
- Bài tư vấn về mật độ xây dựng nhà ở riêng lẻ, đọc 2026-11-08. Chống đỡ cho
  việc xây phủ hết lô 90 m².

## Trạng thái cho phiên sau
| # | Product | Status | Where | Weakest ground |
|---|---|---|---|---|
| 1 | Danh sách phòng | approved | file này | — |
| 2 | Phần được xây | done | file này | Chưa có thông tin quy hoạch của lô |
| 3 | Phép tính sổ | approved | file này | Đơn giá là ước lượng |
| 4 | Các cách xếp | approved | file này | — |
| 5 | Bảng số | approved | params.json | Chiều sâu 18 m là ước lượng |
| 6 | Bản kiểm | done | file này | — |
| 7 | Bản vẽ | missing | — | — |

Next action: Chờ máy có CADCraft rồi dựng bản vẽ từ params.json.
Drawing tool: not installed
Working with this user: trả lời ngắn, nêu con số.
MD
cat > "$d/params.json" <<'JSON'
{
  "scale": 100,
  "drawings": ["plan:L1", "plan:L2", "plan:L3"],
  "site": {"outline": [[0, 0], [5000, 0], [5000, 18000], [0, 18000]],
           "setbacks": {"front": 0, "rear": 0, "left": 0, "right": 0},
           "front": "A", "north_deg": 90},
  "grid": {"x": {"1": 0, "2": 5000},
           "y": {"A": 0, "B": 5000, "C": 8000, "D": 13000, "E": 18000}},
  "levels": {"L1": 0, "L2": 3300, "L3": 6600, "roof": 9900},
  "wall_types": {"ext": 220, "int": 110},
  "floors": {"L1": {"rooms": [
    {"name": "Khách và để xe", "bay": ["1-2", "A-B"], "required_area": 20},
    {"name": "Thang và giếng trời", "bay": ["1-2", "B-C"]},
    {"name": "Bếp ăn", "bay": ["1-2", "C-D"], "required_area": 18},
    {"name": "Phòng ngủ ông bà và vệ sinh", "bay": ["1-2", "D-E"], "required_area": 15}
  ]}},
  "font": "Arial"
}
JSON
