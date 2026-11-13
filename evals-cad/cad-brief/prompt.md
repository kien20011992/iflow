---
description: A bare brief must open a project file, put a marked first cut on the table and ask only what blocks, without inventing the plot or asking an owner about drafting conventions.
expected_outcome: "Lượt đầu lập file dự án, bày bảng nháp có ghi chỗ nào là đoán, và chỉ hỏi vài điều chủ nhà trả lời được. Người duyệt xem thêm: bảng phòng nháp có hợp với một gia đình năm người không, có câu hỏi nào thừa hoặc thiếu không."
max_turns: 40
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit]
append_system_prompt: "This session has no shell and no web tools. For a new project id, choose four hex characters yourself. The drawing tool CADCraft is not installed on this machine. The working directory is the project root: docs/iflow/ belongs there."
---

/i:cad Thiết kế nhà phố 3 tầng, xây mới, trên lô đất 5×18 m ở phường Hải Châu, Đà Nẵng cho gia đình 5 người.
