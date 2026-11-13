---
description: A one-turn factual question gets a direct answer whose certainty is stated, and opens no project folder.
expected_outcome: "Một câu hỏi tra cứu được trả lời thẳng, nói rõ con số chắc tới đâu, và không lập thư mục dự án. Người duyệt xem thêm: con số đưa ra có đúng với quy chuẩn hiện hành không."
max_turns: 15
timeout_seconds: 400
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit]
append_system_prompt: "This session has no shell and no web tools. For a new project id, choose four hex characters yourself. The drawing tool CADCraft is not installed on this machine. The working directory is the project root: docs/iflow/ belongs there."
---

/i:cad nhà phố xây mới ở Đà Nẵng thì cầu thang trong nhà phải rộng tối thiểu bao nhiêu?
