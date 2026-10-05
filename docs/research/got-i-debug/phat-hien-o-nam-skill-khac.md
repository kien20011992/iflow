# Những gì thấy ở năm skill kia khi rà i:debug

Ghi chép ngày 2026-10-05, trên commit `854968e` (bản 1.11.1). Số dòng tính theo repo lúc đó. Lượt rà này ban đầu bị hiểu nhầm phạm vi thành cả plugin, nên ba agent đã rà luôn flow, lite, test, explore, gamify và phần chung của plugin. Sau đó một agent thứ tư đọc danh sách như người lạ, mở từng file kiểm câu thay thế. Phạm vi được sửa lại thành chỉ i:debug, nên **không mục nào dưới đây được làm**. Ghi lại để các đợt rà sau khỏi phải tìm lại. Đây là những gì đã thấy, không phải quyết định. Mã ở đầu mỗi mục giữ nguyên để đối chiếu.

Kết luận chung: phần phình sau các đợt gọt phần lớn là đáng. Làn nhanh của flow, luật phạm vi của test trên nhánh main, các bản sửa gamify 1.8.0 đều chữa lỗi đã gặp thật. Thứ không đáng nằm ở vài chỗ mâu thuẫn, một chốt an toàn bị lỡ bỏ, và đoạn chép lặp giữa SKILL.md với file tham chiếu.

| Skill | Đồng bộ với flow | Cấu trúc | Luồng chính | Luật |
|---|---|---|---|---|
| flow | 7 | 7 | 7 | 6 |
| lite | 8 | 8 | 8 | 7 |
| test | 8 | 7 | 7 | 7 |
| explore | 8 | 8 | 8 | 8 |
| gamify | 8 | 7 | 7 | 6 |
| phần chung | — | 6 | — | — |

## Nên làm sớm nhất

- **T1, i:test lỡ bỏ một chốt chống mất dữ liệu.** Commit `854968e` bỏ "a unique data namespace" khỏi đoạn E2E, giữ "cleanup that also runs when the test fails". Test dọn dẹp mà không có vùng dữ liệu riêng thì có thể xoá dữ liệu local của người dùng (đã kiểm bằng `git show 854968e`). Câu đề xuất cho test SKILL.md:127: "Use a fake clock, a fixed seed and a unique namespace wherever determinism needs them; a test that writes to a real store writes inside its own namespace, and its cleanup removes only what it created."
- **P1, hook nhắc chạy tiếp đang ra lệnh.** `hooks/iflow-resume.sh` in "read … SKILL.md and that shape.md, then continue per its Next action" ở mọi lần mở phiên, kể cả phiên mở để làm việc khác trong repo có chương trình đang dở. Đề xuất đổi thành câu điều kiện: "To resume one listed with no marker: …" và "Marked ⚠ BROKEN STATE: their Next action is deliberately withheld and must not be acted on; before resuming one, repair it per …". Mẫu mà `tests/run.sh` tìm vẫn khớp.
- **F4, flow có một cái test đỏ đi hai đường.** Bước 3 của chu trình dựng (flow SKILL.md:184-188) đã định đường cho mọi cái đỏ. Đoạn "Tests from i:test" (flow SKILL.md:269-272) lại đưa cái đỏ không ai nhận sang i:debug. Đề xuất cắt câu ở dòng 269-272.
- **GB1, gamify tự mâu thuẫn trước mặt người dùng.** Báo cáo cuối liệt kê "which frames were offered in each round", trong khi `concept.md:79` cấm nhắc số vòng với người dùng. Đề xuất: "which frames were offered and why".

## i:flow

- F1 — "this rule is the only reload" (SKILL.md:83-84) sai, vì Claude Code tự gắn lại SKILL.md sau compaction. Lite đã bỏ câu này ở `eccfde2`. Đề xuất chỉ giữ "The compaction summary is a pointer, not a source of truth."
- F2 — danh sách từ nội bộ không được nói với người dùng (SKILL.md:37-38) thiếu từ của vòng định hình: lane, picture, zone map, the zone states, fresh-eyes pass. Dòng vị trí cuối mỗi lượt định hình có thể lộ nhãn như "understood-leaning-recorded".
- F3 — lúc kết thúc chương trình, flow chạy lại cả bộ test ngay sau khi phần việc cuối vừa chạy cả bộ. Đề xuất: chỉ chạy lại khi code đổi sau lần chạy cả bộ gần nhất. Đây là đổi hành vi.
- F5 — điều kiện gọi i:test có vế thứ ba là trường hợp con của vế hai; hai chữ "never" lặp description của i:test.
- F6 — "it proves the cause, changes nothing" lặp description của i:debug; dùng câu của lite.
- F7 — "a fresh agent reading shape.md alone" dễ hiểu thành lệnh mở subagent mỗi lần tạo hồ sơ (4–6 phút). Đề xuất tự đọc lại như người lạ, giữ tên "the quality test" vì SKILL.md trỏ tới nó.
- F8, F9 — hai chỗ lặp trong `shape.md` và `state.md`. Lưu ý từ lượt soát: câu về con số trong `state.md` §6 bắt buộc kiểm nguồn, câu trong `shape.md` chỉ dạy dán nhãn; đừng thay câu này bằng câu kia.
- F10 — "giữa chừng chỉ còn nhu cầu hiểu thì chuyển i:explore" (cả flow và lite): hiếm, người dùng thấy ngay, description của explore đã phủ.
- F11 — "plan cycle" và "build cycle" là một thứ hai tên.

## i:lite

- L1 — làn nhanh của lite không đọc hồ sơ i:explore, trong khi explore khuyên `/i:lite fast` và làn nhanh của flow có đọc.
- L2 — câu "mất đường dẫn bản nháp thì khôi phục": flow đã cắt ở 1.4.0, lite còn.
- L3 — danh sách từ nội bộ thiếu "finding", "Mid-flight".
- L4, L5 — lặp trong "Too big for one plan?" và "Hard rule".
- L7 — lite chưa có luật của flow 1.11.0 "plan lệch một quyết định đã ghi thì nói ra ở cổng duyệt và viết lại dòng quyết định". Sau khi chốt, lần đọc code sâu có thể lặng lẽ lật một quyết định người dùng đã chốt.
- `CLAUDE.md` vẫn ghi "lite đã khớp flow 1.4.0 ở bản 1.5.0", cũ bảy bản.
- Giữ nguyên: khối kết quả trong file plan (CLAUDE.md ghi là chỗ cố ý khác flow).

## Phần chung của plugin

- P4 — `evals/flow.json`, `evals/gamify.json` không chạy được, vì script đo từ chối skill chỉ gọi tay. Git vẫn giữ nếu cần lại.
- P5 — `check-pointers.sh` nằm trong thư mục script của flow nhưng không skill nào gọi. Nếu dời ra `scripts/`, phải đổi dòng mặc định thư mục (dòng 23), vì mặc định đang là thư mục cha của chính nó.
- P6 — `hooks.json` truyền `IFLOW_SKILL_DIR` dù script tự tính được; giữ nhánh dự phòng trong script vì `tests/run.sh` dùng nó.
- Giữ: `scripts/trigger-eval.sh`. Lệnh có sẵn `claude plugin eval` đo được skill có mở không, nhưng chỉ nạp plugin đang đo, nên không đo được việc tranh nhau với các skill khác đang cài như engineering:debug hay testing-strategy.
- Giữ: README là văn bản cho người, không cắt.

## i:test

- T2 — chế độ "chỉ liệt kê chỗ thiếu test" (người dùng duyệt ngày 10-05) có điều kiện bật quá rộng: "xem service nào thiếu rồi viết test cho đủ" cũng khớp, và lần chạy đó sẽ không viết gì. Đề xuất: "when the intent asks only for a list of what has no test yet, not for tests to be written". Câu hiện tại còn đọc vấp: "a test that Native implementation counts".
- T3 — dòng "deliverable" lặp dòng 30-31.
- T4 — "Run · Result" chưa theo cách trình bằng chứng của flow (lệnh và ý nghĩa kết quả, không dán log).
- T5 — khi gọi thẳng, test tự đi tìm hồ sơ flow trong `docs/shape/`. Flow luôn nêu tên hồ sơ, nên nhánh này chỉ chạy khi gọi thẳng, và có thể giành phạm vi của "thêm regression test cho bug vừa sửa". Đổi hành vi.

## i:explore

- E1 — lời chuyển sang `/i:flow` chưa nhắc `fast`, trong khi làn nhanh của flow đọc hồ sơ explore.
- E2 — lúc khép lại chưa để "đủ hay chưa" cho người dùng quyết.
- E3 — mỗi lượt đọc lại cả hồ sơ; đề xuất chỉ đọc lại phần nói hay trỏ tới thứ vừa đổi. Đổi hành vi.
- E4, E5 — ba chỗ lặp trong `dossier.md`; câu "delta from your defaults".
- E6 — thiếu `argument-hint`.

## i:gamify

Luật của đợt gamify 30/9 là chỉ gọt, không đổi hành vi. Hầu hết phần thêm ở 1.8.0 sửa lỗi thấy thật trên game Keystage hoặc game forex.

- G1–G17 — chủ yếu là SKILL.md chép lại chữ đã có trong file tham chiếu. Lớn nhất: đoạn "Three approvals cover the build" (SKILL.md:153-159) lặp bước A.3–A.4 và C.2 của `vong-slice.md`. Có hai chỗ người đọc thấy: câu giữ chỗ ở mục ghi chú phiên chơi trong mẫu `plan.md` đã cũ (`tim-hieu.md:229`), và `tim-hieu.md:182-183` thiếu chữ "như". Lưu ý từ lượt soát: đề xuất rút luật "không hỏi gu game" thành "concepts come from the frame library" là sai, vì sau một vòng bị từ chối, concept đến từ thể loại ngoài thư viện.
- GB2 — báo cáo một dòng sau mỗi phần dựng không nêu chỗ chưa kiểm được như flow.
- GB3 — sau compaction chỉ đọc lại một file tham chiếu, trong khi luật của phần dựng trang nằm ở `slate.md`, của dungeon ở `khuon-file.md` và `luat-van-phong.md`.
- Danh sách B1–B19 cũ: gần hết đã làm ở 1.8.0. B5 còn mở. B18 (luật chỉ phục vụ game forex) còn, và lớn thêm một câu ở `vong-slice.md:145-146`.

## Nguồn

Ba agent đọc repo và `git log` (primary); tài liệu hooks và plugin-evals của Claude Code (official, agent đọc 2026-10-05); một agent soát danh sách đề xuất bằng cách mở từng file ở dòng được trích.
