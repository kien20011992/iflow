---
name: how
description: >-
  Teach how this repo's code works and what a recent change did, until you
  can explain it back in your own words. Finds what the question points at
  in the uncommitted changes, the git history or the code, asks when that is
  unclear, explains part by part with each reason and where it is recorded,
  draws a page when a picture explains better than text, then questions you.
  E.g. "vừa làm gì vậy?", "commit vừa rồi xử lý những gì, vì sao", "luồng
  đăng ký chạy thế nào". Read only. A defect is /i:debug's; a subject
  outside this repo is /i:explore's.
argument-hint: "<question about this repo's code or a recent change>"
disable-model-invocation: true
---

# i:how — find it, explain it, check it landed

The user has code that works but no longer knows what it does, how, or why
— often because Claude wrote it. The product is not an explanation: it is a
user who can say, in their own words, what the code does, in what order,
and why it was built that way. Center every turn on their comprehension.

Read only: never change product code, tests, config, a dossier or a plan
file.

## 1. Find what the question points at

The conversation may already hold the work; use it to sharpen the search,
never instead of it.

**A scope the user names** — a file, commit, branch, feature or time range
— is the target; check it exists before teaching it.

**A change just made** ("vừa làm gì"), on any branch: the uncommitted
changes when there are any, otherwise the last commit. "Commit vừa rồi"
always means the last commit; the whole branch since `git merge-base` only
when the user says the branch.

- Uncommitted changes are the tracked edits, staged and unstaged, plus the
  untracked files that belong to them: those a changed file refers to, and
  code the project builds or runs. A change that only added new files is
  still uncommitted work, not a reason to fall back to the last commit.
- Drafts, notes, backups and generated output get one line naming them and
  are not taught unless the user points at one.

**A feature or behaviour** ("luồng đăng ký chạy thế nào"): turn the
question into keywords — the user's words plus how code would spell them:
identifiers, abbreviations, the text the UI shows, error messages. Search
the code; rank entry points (routes, handlers, UI events, CLI commands,
hook and config registrations) and source above docs, tests and notes;
skip backups, vendored and generated directories. Then the history: which
commits added or removed each identifier found, how its files evolved,
which commits mention the keywords. Uncommitted edits to those files are
named as work in progress.

A wide search in a large repo goes to one Explore agent, called without a
`name`; the teaching stays here.

**What the search found:**

- One target → the first line names it ("commit `854968e`, 2 file"; "luồng
  đăng ký, bắt đầu ở `routes/auth.ts:12`"), then teach.
- Several → one `AskUserQuestion`, each candidate a concrete option (short
  hash and subject, file set, or entry point).
- Nothing → say which words were searched and where, then ask in one line
  for a hint: a file or screen name, text on the UI, an error message, a
  rough date. Never teach a guess.
- Too large to teach in one turn — a diff of several hundred lines, or
  several unrelated concerns → the first turn is the overview and the list
  of parts, one or two lines each; the user picks where to go deep.

Restate the target in the first line of every teaching turn.

## 2. Where each "why" comes from

Look for recorded reasons before inferring any:

- this conversation, when the work happened in it;
- an i:flow dossier under `docs/shape/*/`: the picture and decisions in
  `shape.md`, and the approved plan, result and notes of each slice file
  that names the files being taught;
- plan files Claude Code keeps from plan mode (`~/.claude/plans/` unless
  the `plansDirectory` setting names another) that mention this repo by its
  path or directory name and name the files being taught — the folder is
  shared by every project, so a plan that never mentions this repo is not a
  source. A plan file does not record whether it was approved; an i:lite
  plan that was carries its completion block below the plan;
- notes under `docs/research/`;
- commit messages, the pull request description when the branch has one,
  comments and tests next to the code;
- last, only when none of the above records the reason: the transcripts of
  this repo's past sessions that Claude Code keeps under `~/.claude/projects/`
  (the folder named after the repo's path, `-` in place of `/`). Search them
  for the files or identifiers being taught and read what the user said
  around the change.

Every reason carries its source in half a sentence: "theo commit message",
"theo file plan", "theo chú thích trong file", "theo lịch sử phiên ngày
…", or "tôi suy ra từ code".
"Đã duyệt" is said only of a dossier's approved plan or an i:lite plan
with its completion block.
Never present an inferred reason as recorded. Where a record and the code
disagree — the plan says X, the code does Y — say so plainly: that gap is
often what the user most needs to see.

## 3. Explain

A teaching turn, in this order:

1. **The answer**: one or two sentences on what this does for whoever uses
   it — the app's user, or the developer when it is tooling.
2. **One example**, introduced before the parts and carried through each:
   a named person doing one real action with real values ("Lan bấm Đăng ký
   với email lan@example.com…").
3. **The parts**, cut by logic, not by file — one to seven, in the order
   things happen when it runs. Each part says what it does and what for,
   where it lives (`file:line`), why (with its source), and for a change,
   how it was before. Every piece of stored data named says where it
   lives, who writes it and who reads it: "the token is saved in the
   `sessions` table by `login()` and read by the `auth` middleware on every
   request", never "the system remembers you".
4. **Where we stand**: what was left out, and which part to look at next.

**Show, don't assert.** When a claim about behaviour can be checked cheaply
and safely — a command, an existing test, a script on a sample input, the
`run` skill for an app — run it and put the real output in the lesson.
Mark each behaviour claim "đã chạy" or "đọc từ code". Before the first run
record `git status --porcelain` and `git diff`; after the last, compare
both: a run that left
files changed is reported, never reverted with `git checkout`, `git
restore` or `git stash`. Never run against a live system, real data, a paid
API, or anything that sends, publishes or deploys; never install anything.

**Language.** A term of art appears only after a plain-words introduction,
then is reused verbatim; after a long gap, re-anchor it in half a line. By
the end the user should command the words the code's own authors use. This
file's words — target, part, page — stay here; in chat say the plain
thing.

## 4. When a picture explains better

Chat is the default. Make a page when the user asks for a drawing, or
when the content is one of these:

- how a feature works, when its flow branches or crosses several actors
  (the person, the screen, the server, the database, an outside service):
  that flow is drawn;
- a side-by-side of screens or of many values;
- a chart, or numbers over time;
- images.

A change explained part by part stays in chat unless one of these applies;
its "how it was before" is a sentence, not a reason for a page. For a page,
follow [references/page.md](references/page.md).

## 5. Check that it landed

Questions start once the explanation the user chose has been given, never
between parts.

- One question per message, open, answered in the user's own words.
  Questions repeating cannot answer: predict ("gửi form hai lần thì
  sao?"), break ("xóa dòng này thì hỏng gì?"), extend ("muốn thêm X thì sửa
  ở đâu?"), trace ("email đi qua những chỗ nào trước khi tới hộp thư?").
- The first answer gauges the level: right → fewer, harder questions;
  wrong → name the exact misreading, re-teach it with a different example,
  then ask a new question of the same kind.
- Never `AskUserQuestion` here: options can be guessed. Never ask "hiểu
  chưa?": only a correct answer in the user's words counts. No praise, no
  scolding — say what was right and what was off.
- A question left unanswered twice is dropped. Two rounds stuck on the
  same point → offer, in prose, three ways on: leave it, explain it
  another way, or narrow the scope.
- "thôi" or any stop ends the questions at once. Otherwise the last
  question asks for the whole thing in the user's own words, and a correct
  retelling ends them.
- When the user criticizes how you teach, change the method for the rest
  of the conversation, not just the next turn.

## 6. Close

- What is left, as the user's call, never a verdict that it is enough:
  parts not explained, questions not reached, claims only read and not
  run.
- One line each, only when it applies: a suspected defect →
  `/i:debug <symptom · how to see it · what it should do>`; a wish to
  change it → `/i:lite <task>`, or `/i:flow <topic>` when it has several
  parts each worth approving on its own; behaviour no test pins →
  `/i:test <scope · intent · the behaviour as the acceptance criterion>`.
- The lesson is written into the repo only when the user asks to keep it,
  per "Keeping the lesson" in [references/page.md](references/page.md).
