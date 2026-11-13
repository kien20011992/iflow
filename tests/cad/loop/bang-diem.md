# Bảng điểm

Mỗi lần chấm một dòng, theo [thang chung](thang-chung.md). Cột "Skill" là
commit của repo lúc chạy. Đề giữ riêng chỉ ghi điểm, không ghi lỗi. Độ lệch
giữa hai lần chạy cùng một đề ghi ở mục "Nhiễu" bên dưới.

| Ngày | Skill | Đề | Bộ | Lần | A /25 | B /30 | C /30 | D /15 | Tổng | Ngoài thư viện | Ghi chú |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 2026-11-13 | (slice 09, trước commit) | pho-5x20-3-tang | luyện | chạy thử thang | 25 | 16,5 | 24,5 | 0 | 66 | 0 % | Chạy thử chuỗi chấm trên bản dựng thư viện slice 04, không phải một vòng skill: D bằng 0 vì không có hội thoại hay ghi chép dự án. Không dùng để so. |
| 2026-11-13 | 3058fc4 | nha-pho-cu-cai-tao | giữ riêng | 1 | 15,5 | 12 | 13 | 9,5 | 50 | 4 % | Phần chưa vẽ 17 (46 % số thứ bảng số đòi vẽ); plan_check trượt gross, reach. |
| 2026-11-13 | 3058fc4 | nha-pho-cu-cai-tao | giữ riêng | 2 | 15,5 | 13,5 | 13,5 | 8 | 50,5 | 4 % | Phần chưa vẽ 16 (43 %); plan_check trượt gross. |
| 2026-11-13 | 3058fc4 | chung-cu-cao-tang-2-ham | giữ riêng | 1 | 8 | 21,5 | 6,5 | 13 | 49 | 0 % | Phần chưa vẽ 12 (3 %); chữ không có chỗ 82 (22 %); dxf_check, plan_check, luat_check cùng trượt. |
| 2026-11-13 | 3058fc4 | chung-cu-cao-tang-2-ham | giữ riêng | 2 | 8 | 16,5 | 11,5 | 11,5 | 47,5 | 0 % | Phần chưa vẽ 7 (2 %); chữ không có chỗ 203 (59 %); ba trình kiểm cùng trượt. |

## Nhiễu

Đo ngày 2026-11-13, skill `3058fc4`, mỗi đề hai lần:

| Đề | Chênh A | Chênh B | Chênh C | Chênh D | Chênh tổng | Chênh phần chưa vẽ | Chênh chữ không có chỗ |
|---|---|---|---|---|---|---|---|
| nha-pho-cu-cai-tao | 0 | 1,5 | 0,5 | 1,5 | 0,5 | 3 điểm % | 0 |
| chung-cu-cao-tang-2-ham | 0 | 5 | 5 | 1,5 | 1,5 | 1 điểm % | 37 điểm % |

Đọc: phần A (máy chấm) không nhiễu. Phần B và C do agent chấm có thể lệch tới 5 điểm giữa hai lần chạy cùng một đề, dù tổng chỉ lệch 0,5–1,5. Vì vậy một đợt sửa chỉ được coi là đổi phần B hay C khi lệch quá 5 điểm, hay khi chạy mỗi đề nhiều lần hơn. Số chữ không có chỗ dao động rất mạnh; đừng dùng nó để giữ hay bỏ một đợt.
