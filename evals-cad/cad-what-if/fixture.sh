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
 "schema": "cad-params/1",
 "project": {
  "name": "Nhà phố Hải Châu",
  "type": "house",
  "depth": "construction",
  "scale": 100
 },
 "site": {
  "outline": [
   [
    0,
    0
   ],
   [
    5000,
    0
   ],
   [
    5000,
    18000
   ],
   [
    0,
    18000
   ]
  ],
  "setbacks": [
   {
    "edge": 0,
    "mm": 0,
    "by": "model"
   },
   {
    "edge": 1,
    "mm": 0,
    "by": "model"
   },
   {
    "edge": 2,
    "mm": 0,
    "by": "model"
   },
   {
    "edge": 3,
    "mm": 0,
    "by": "model"
   }
  ],
  "front_edge": 0,
  "north_deg": 90
 },
 "grid": {
  "x": {
   "1": 0,
   "2": 5000
  },
  "y": {
   "A": 0,
   "B": 5000,
   "C": 8000,
   "D": 13000,
   "E": 18000
  }
 },
 "levels": [
  {
   "name": "L1",
   "elevation": 0,
   "height": 3300,
   "kind": "ground"
  },
  {
   "name": "L2",
   "elevation": 3300,
   "height": 3300,
   "kind": "typical"
  },
  {
   "name": "L3",
   "elevation": 6600,
   "height": 3300,
   "kind": "typical"
  },
  {
   "name": "Mái",
   "elevation": 9900,
   "height": 0,
   "kind": "roof"
  }
 ],
 "types": {
  "walls": {
   "ext": {
    "thickness": 220
   },
   "int": {
    "thickness": 110
   }
  },
  "openings": {
   "D9": {
    "kind": "door",
    "width": 900,
    "height": 2200
   },
   "D8": {
    "kind": "door",
    "width": 800,
    "height": 2200
   },
   "S": {
    "kind": "shutter",
    "width": 3000,
    "height": 2800
   }
  }
 },
 "floors": {
  "L1": {
   "walls": [
    {
     "id": "wA",
     "type": "ext",
     "from": [
      [
       "1",
       0
      ],
      [
       "A",
       0
      ]
     ],
     "to": [
      [
       "2",
       0
      ],
      [
       "A",
       0
      ]
     ],
     "align": "left"
    },
    {
     "id": "wE",
     "type": "ext",
     "from": [
      [
       "1",
       0
      ],
      [
       "E",
       0
      ]
     ],
     "to": [
      [
       "2",
       0
      ],
      [
       "E",
       0
      ]
     ],
     "align": "right"
    },
    {
     "id": "w1",
     "type": "ext",
     "from": [
      [
       "1",
       0
      ],
      [
       "A",
       0
      ]
     ],
     "to": [
      [
       "1",
       0
      ],
      [
       "E",
       0
      ]
     ],
     "align": "right"
    },
    {
     "id": "w2",
     "type": "ext",
     "from": [
      [
       "2",
       0
      ],
      [
       "A",
       0
      ]
     ],
     "to": [
      [
       "2",
       0
      ],
      [
       "E",
       0
      ]
     ],
     "align": "left"
    },
    {
     "id": "wB",
     "type": "int",
     "from": [
      [
       "1",
       0
      ],
      [
       "B",
       0
      ]
     ],
     "to": [
      [
       "2",
       0
      ],
      [
       "B",
       0
      ]
     ],
     "align": "center"
    },
    {
     "id": "wC",
     "type": "int",
     "from": [
      [
       "1",
       0
      ],
      [
       "C",
       0
      ]
     ],
     "to": [
      [
       "2",
       0
      ],
      [
       "C",
       0
      ]
     ],
     "align": "center"
    },
    {
     "id": "wD",
     "type": "int",
     "from": [
      [
       "1",
       0
      ],
      [
       "D",
       0
      ]
     ],
     "to": [
      [
       "2",
       0
      ],
      [
       "D",
       0
      ]
     ],
     "align": "center"
    }
   ],
   "rooms": [
    {
     "id": "r1",
     "name": "Khách và để xe",
     "at": [
      [
       "1",
       2500
      ],
      [
       "A",
       2500
      ]
     ],
     "use": "shared",
     "need_area": 20
    },
    {
     "id": "r2",
     "name": "Thang và giếng trời",
     "at": [
      [
       "1",
       2500
      ],
      [
       "B",
       1500
      ]
     ],
     "use": "circulation"
    },
    {
     "id": "r3",
     "name": "Bếp ăn",
     "at": [
      [
       "1",
       2500
      ],
      [
       "C",
       2500
      ]
     ],
     "use": "shared",
     "need_area": 18
    },
    {
     "id": "r4",
     "name": "Phòng ngủ ông bà và vệ sinh",
     "at": [
      [
       "1",
       2500
      ],
      [
       "D",
       2500
      ]
     ],
     "use": "private",
     "need_area": 15
    }
   ],
   "openings": [
    {
     "id": "o1",
     "wall": "wA",
     "type": "S",
     "offset": 1000,
     "by": "model"
    },
    {
     "id": "o2",
     "wall": "wB",
     "type": "D9",
     "offset": 2000,
     "hinge": "start",
     "swing": "left",
     "by": "model"
    },
    {
     "id": "o3",
     "wall": "wC",
     "type": "D9",
     "offset": 2000,
     "hinge": "start",
     "swing": "left",
     "by": "model"
    },
    {
     "id": "o4",
     "wall": "wD",
     "type": "D8",
     "offset": 2000,
     "hinge": "start",
     "swing": "left",
     "by": "model"
    }
   ]
  }
 },
 "drawings": [
  {
   "id": "plan:L1",
   "origin": [
    0,
    0
   ]
  }
 ],
 "rules": []
}
JSON
