---
name: flow
description: >-
  Shape a large or still-unsettled undertaking into user-approved vertical
  slices, then execute them one by one — code slices through plan mode,
  research slices as documents in the repo — tracked in
  docs/iflow/<topic>/iflow.md. Use it whenever the request spans several
  coupled pieces or has no clear start yet, however terse: "review toàn bộ …
  rồi tối ưu", "làm lại hoàn toàn / nâng cấp toàn diện X: a, b, c", "tìm mọi
  cách để …", "research X rồi dựng thành tool/repo chạy được", "viết bộ tài
  liệu về toàn bộ luồng …", a migration across api + app + admin — and
  whenever the user resumes such work ("hôm trước dừng ở …, giờ làm nốt").
  Prefer it over brainstorming when more than one deliverable is involved. Not
  for a single task one plan covers (thêm một tính năng nhỏ, sửa một hàm),
  pure understanding with no repo deliverable (i:explore), a defect (i:debug)
  or new tests (i:test).
argument-hint: "[fast] <topic to shape, or dossier to resume>"
disable-model-invocation: true
---

# i:flow — shape, then slice

Two layers. The Shape layer turns a large or ambiguous request into a
user-approved table of vertical slices; the slice loop executes the slices
one by one until done. Core invariant: **facts live in files, not in
conversational memory** — during Shape they live in the working draft
(the plan file itself, including its research notes — never a
second draft file alongside it), after the table is approved they live in
the dossier, and research notes become `docs/iflow/<topic-slug>/research/*.md`
files at dossier birth.

Language: protocol skeletons — file names, the state-block labels in
references/state.md §2 and the draft's two lines in references/shape.md §0,
this skill's own files — are English. Everything
else a document holds, headings included, and every word spoken to the
user follow the user's language, in words the user never has to look up:
the protocol's private vocabulary — terms like slice, Charter, birth
checklist, ripe, finding, Mid-flight, zone, lane, picture draft,
fresh-eyes pass, stranger read and the zone states such as "understood (leaning
recorded)" — stays in this skill's own files and
the state block; in documents and in chat, say the plain thing instead, or
introduce the term right where it is first used. A zone code is shorthand
for the zone map: anywhere outside the map — the position line above all —
write it with its short name attached ("Z5 product shape"), and never write
a code the map does not have yet.

Agents: follow [references/agents.md](references/agents.md) whenever you
put one to work.

## The dossier

A topic's dossier lives at `docs/iflow/<topic-slug>/`: `iflow.md` plus one
`NN-<name>.md` per slice. What `iflow.md` is authoritative for, its
templates, the label contract table, the birth checklist, and the quality
test all live in
[references/state.md](references/state.md) — read it before first creating
or updating a dossier in a session.

A first word `fast` calls the fast lane (shape.md §5); the rest is the
topic.
Resolve in this order: the user names a dossier → the dossier active in the
conversation → a `docs/iflow/*/iflow.md` matching the topic → an unfinished
Shape on this topic, found per "Draft recovery" in
[references/shape.md](references/shape.md) — resume it, with no new
"Too light for slices?" weighing → none: weigh it per "Too light for
slices?" under Layer 1, and if it goes on, start Shape fresh.

If iflow.md already exists: read it and the slice file its `Current slice:`
names, then continue from the next-action line it records. Never re-ask
what it already records; never make the user re-approve what was approved.

## After a compaction

Before the next exchange, re-read `${CLAUDE_SKILL_DIR}/SKILL.md`, the
reference governing the running layer, and the files that hold the active
work:

- during Shape: [references/shape.md](references/shape.md) and the
  working draft;
- while creating or repairing a dossier:
  [references/state.md](references/state.md) and iflow.md;
- during a slice: iflow.md and the current slice file.

The compaction summary is a pointer, not a source of truth.

## Layer 1 — Shape

**Too light for slices?** A new topic is weighed from the request alone,
before entering plan mode or scanning the repo. When one plan covers it —
one task, one deliverable, nothing worth approving on its own — the whole
turn is one line in the user's language: the reason, then `/i:lite <task>`
(`/i:lite fast <task>` when the user called `fast` or the direction is
already settled); then stop
for the user's call. Unsure means not too light. Say it once, never again
mid-way.

Otherwise the topic enters Shape: before anything else, read
[references/shape.md](references/shape.md) and follow its three stages, or
its fast lane when the user called `fast`.

## Layer 2 — the slice loop

Invariants:

1. Re-read iflow.md before starting and right after finishing each slice.
2. `Current slice:` and `Next action:` in iflow.md change the moment the
   next action changes, not at slice end; `Next action:` is one runnable
   imperative sentence ("EnterPlanMode for slice 03, explore only within
   X"). Starting a slice is ONE write — the row goes `doing`, `Current
   slice:` names it, `Next action:` becomes its first step — made and
   checked before `EnterPlanMode`.
   After each write to the dossier (a burst such as the birth checklist
   counts as one write), run
   `${CLAUDE_SKILL_DIR}/scripts/check-dossier.sh <dossier-dir>` in the
   foreground and fix what it reports.
3. When a task-list tool is available, mirror the slice table into it so
   the user sees progress; iflow.md stays the single source of truth — on
   divergence, iflow.md wins.
4. Work only the chosen slice. A finding belonging to another slice gets
   one line in that slice file's notes; one belonging to no slice gets
   one line in iflow.md's section on what was explored — nothing may drop.
   Then return. While plan mode is on, carry such lines in the plan; its
   FIRST step writes them.
5. Verification evidence (scripts, screenshots, command output) lives in
   the repo, in the slice's own `docs/iflow/<topic-slug>/evidence/NN-<name>/`
   — never in the session scratchpad, which is cleaned up. Keep all of it:
   evidence is never deleted, trimmed, overwritten or replaced by a
   summary — a second attempt writes beside the first, under new names;
   keeping it out of git is the user's `.gitignore` call, not this skill's.

**The approval gate.** Every plan i:flow puts to the user — the slice table
that closes Shape, and each build slice's plan — passes the plan-mode
approval button when plan mode is in use, and one `AskUserQuestion` on the
plan's own content when it is not; a question that times out or is denied
is not approval — stop there. Until a plan passes its gate, work toward it
is read-only: nothing is created, changed, installed, migrated or deployed
— no file, dependency, database, external service or deployment. The only
writes meanwhile: during Shape, the working draft; once the dossier exists,
also the dossier's own files, as this skill directs.

**The stranger read before a gate.** One general-purpose agent (never a
Plan agent) that has not seen the conversation reads a plan before its
gate only when (1) the plan's own steps write or delete real data, call
a paid API, deploy or migrate, and then, on that ground alone, the read
covers only those steps; (2) the user asks for it; or (3) the user said
the work must be done carefully or matters, judged by what they meant,
not by the words alone — a decision, recorded as such. Real data means a
production or shared environment's, never local or test data; migrate
likewise. Hand the
agent, told to change nothing, the task and the plan to name missing
choices, wrong assumptions and unproven claims; fold what holds into the
plan and give each rejected candidate one line in it. Otherwise the plan
goes to its gate at once, with one line after its last step telling the
user, in their language, to answer `soát` for an agent to read it; that
answer runs the read, then the plan returns to the gate. Apart from this
read and stage 2's fresh-eyes pass on the picture, no agent reviews or
designs a plan, whatever plan mode suggests.

**Build slices** run the build cycle:

1. `EnterPlanMode` when plan mode is in use; explore only within the
   slice's scope (deep code reading happens now, not earlier); reconcile
   against the slice's charter, its notes and iflow.md's decisions — a
   plan that departs from a decision says so at its gate (a Mid-flight
   decision). Heavy reading may be delegated to
   Explore agents; writing code is never delegated: the main agent owns
   every edit.
2. Write the plan. Every plan put to the gate must have as its FIRST step:
   re-read `${CLAUDE_SKILL_DIR}/SKILL.md` if it is no longer in context (a
   compaction, or a context cleared on approval); record into the slice
   file's approved-plan section — the plan names that file — a 3–7 line
   summary of the approved plan (what changes, proven by what at which
   boundary, deliberately skipping what) followed by the plan's steps as a
   numbered list, one line each — never the plan's prose; write the lines
   the plan carries for other slices (invariant 4); rewrite each decision
   line in iflow.md the plan departs from (step 1); and point
   `Next action:` at the plan's next step. As its LAST step: steps 4 and
   5 below, then "Auto-advance". A slice that changes code lists in its
   plan the tests covering that change; a repo with no test command of its
   own gets one built by the same plan.
3. After approval: verify with real commands, checked against the slice
   file's approved-plan section, not against memory. When the proof
   boundary is the running app, `/run` is that command. When the repo has
   a test command, the proof includes one run of the whole suite by
   default; a narrower run holds only when the approved plan named it with
   what it leaves out and why — the user accepted that at the gate, the
   model never narrows the proof on its own. The first build slice whose
   dossier records no baseline yet runs the whole suite once, right after
   approval and before any change, and records the outcome — each red by
   name, or "green" — in iflow.md's section on what was explored; those
   reds fail no later proof and need no skip. Any other red makes the proof
   fail. A
   red this slice's own change caused is fixed here; a red in a test i:test
   wrote takes "Tests from i:test"; any other red takes invariant 4 and
   stays in the suite only by a user order, skipped as "Tests from i:test"
   describes. A red this slice caused whose cause the failure output and
   the change just made do not explain goes to `/i:debug <the red output ·
   the proof it breaks · the dossier's iflow.md path · the active slice
   file>` before any fix; the fix stays here under the approved plan.
   Running a suite that already exists
   is this cycle's own work with the project's runner, never a trip through
   i:test.
4. Review gate — only when the slice changed code (dossier files and
   research documents are not code): run `/code-review` at level medium
   over the files this slice touched. Wait for its findings before writing
   the result; a review still running is not one that could not run. The
   main agent reconciles the findings against
   the slice file's approved plan: a finding whose fix would depart from
   the approved plan needs the user's decision first (Mid-flight
   decisions), and the result records it; other findings inside this
   slice's Charter are fixed here and re-verified; any other finding takes
   invariant 4. A gate
   that could not run is recorded in the result and does not block the
   slice.
5. Write the result section: pass or not, evidence as commands + key
   output, the review gate's outcome when the gate applied — the paths
   handed to it as well as what came back (findings, clean, or could not
   run), so a later reader can judge the coverage — divergence from the
   approved plan, and, when this slice's proof went through i:debug, its
   status, cause or gap, reproduction and decisive evidence.

**Research slices** skip plan mode: explore deeply within the slice's
scope; confer with the user only on something that would change the
slice's Charter or the document's main conclusion; then write the finished
document into the slice file. Source discipline per "Research-slice source
discipline" in [references/state.md](references/state.md). A research
slice may delegate per formed question.

**Auto-advance** — finishing a slice does not end the turn. After the
slice's result section is written (or the research document is complete):
update iflow.md (mark slice NN done, set the next action to the next
slice), re-read it (invariant 1), announce in exactly one line which slice
finished and whether it passed, naming any gap its result records — for a
research document, with its file path — then start the next slice in the
same turn, even through another approval gate. It needs no approval before
advancing; feedback arriving later follows Mid-flight decisions. Stop only
when a user decision is needed, a report you commissioned has not come
back yet, or every slice is done or retired.

## Mid-flight decisions

An explicit order is a decision; a question or praise is not. Write the
decision into iflow.md first, touch code after. If the decision changes
the slice table: rebuild the table from the current shape, re-submit it
for approval, then continue.

## Redoing a slice

A small finding inside a finished slice's Charter — a sentence to fix, a
line to restore — is not a redo: fix it at once, re-run that slice's
checks, and record it under the slice's result as a second attempt, one
line each; the table does not change. Charter still right but the result
overturned → the row becomes
"needs-redo" and the slice reruns the full cycle of its type; the reason
goes into its notes, and its approved plan and result get fresh entries
headed as a second attempt, the old ones kept as history. Charter wrong →
not a redo: retire NN (status "retired") and cut a new slice with a new
number per the NN identity rules in
[references/state.md](references/state.md); name the retired slice in the
decision line. Marking "needs-redo" edits the slice table, so it is a
Mid-flight decision — a user order, or evidence the model presents with
the re-submitted table, listing each finished slice that names it under
"Needs first" with a judgment of whether it is affected; affected ones
also go "needs-redo" and rerun in the original order.

## Tests from i:test

i:test writes new independent tests from a fresh fork. Call it only when
the user asks for independent tests, or when an approved plan needs
coverage (unit, E2E, contract or adversarial) that nothing provides yet —
never as an automatic second pass over verification that already proved
the slice. Before the call, write every
decision changed in this conversation into the dossier: the fork reads
only the dossier and its arguments. The handoff is one plain sentence,
not a schema: the
slice and its dossier path, the focus, the constraints, and that the
dossier's picture and decisions and the slice's charter are the oracle.
Condense what comes back into the slice's result; the next action stays
this flow's own call. A red in one of those tests that this slice's own
change never touched is judged against the contract first; if that leaves
its cause unexplained, it takes the i:debug lane of step 3.

A red in one of those tests is a finding about the product, not a broken
test. Inside the current slice's Charter: fix the code and re-verify.
Outside it: the finding takes invariant 4, and the test is skipped — the
runner's own skip marker, never a throwaway command-line flag — with a
reason pointing at the line just written. Leaving any red open on
purpose — one of those tests or any other — takes a user order (a
Mid-flight decision) and skips the test the same way. Those skips are this flow's only edits to such a test: never
delete it, never loosen its assertion. A harness or contract gap, or an
expectation i:test left uncovered, blocks calling the slice a pass when
the slice required that coverage.

## Finishing

When every slice reads done or retired: if code changed after the last
whole-suite run, run the whole suite once more, never narrowed, per step 3
of the build cycle.
A red beyond those recorded at the baseline means not done — each takes
its lane there, and a slice already reading done that has to carry a fix
goes through "needs-redo" above; finishing resumes once none is left.
Then write the summary — each slice, its product, file paths, what was
deliberately left open, and any baseline red still red — at the top of
iflow.md's body, above the picture, and copy the program's result to
`assets/iflow/` beside `docs/` at the same root: the summary alone as
`assets/iflow/<topic-slug>.md`; when the program also produced finished
documents (research slices) or a web page, a directory
`assets/iflow/<topic-slug>/` holding the summary and each of them — a
research slice's document part only, not its charter or notes. It is a
copy — the dossier stays as it is — and a later redo copies again over
this program's own earlier copy; a file there that this program did not
write is never overwritten: the copy takes a new name beside it. Only
once the copy exists, set the overall status line in iflow.md to done and
post the summary in chat as the end-of-program announcement.
When the program changed code,
it closes with one line: the program has not passed `/security-review`,
run it BEFORE pushing.
