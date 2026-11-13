---
description: A what-if question must be answered with what it would cost to redo, and must change nothing in the project.
expected_outcome: "Câu hỏi thêm một tầng chỉ được trả lời bằng cái giá phải trả, không được ghi hay sửa gì trong dự án. Người duyệt xem thêm: danh sách việc phải làm lại có đúng và đủ không."
max_turns: 25
timeout_seconds: 600
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit]
append_system_prompt: "This session has no shell and no web tools. For a new project id, choose four hex characters yourself. The drawing tool CADCraft is not installed on this machine. The working directory is the project root: docs/iflow/ belongs there."
---

/i:cad nha-pho-hai-chau a1b2: hay là thêm một tầng nữa thì sao?
