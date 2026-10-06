---
name: flow
description: >-
  Shape a large or still-unsettled undertaking into user-approved vertical
  slices, then execute them one by one — code slices through plan mode,
  research slices as documents in the repo — tracked in
  docs/iflow/<topic>-<id>/iflow.md. Use it whenever the request spans several
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

Two layers. Shape turns a large or ambiguous request into a user-approved
table of vertical slices; the slice loop executes them one by one until
done. Core invariant: **facts live in files, not in conversational
memory**. During Shape they live in the working draft — the plan file
itself, research notes included, never a second draft file beside it.
Once the table is approved they live in the dossier, and the research
notes become `docs/iflow/<topic-slug>/research/*.md` files at dossier
birth.

Language: protocol skeletons — file names, the state-block labels in
references/state.md §2, the draft's two lines in references/shape.md §0,
this skill's own files — are English. Everything else a document holds,
headings included, and every word spoken to the user follow the user's
language, in words the user never has to look up. This skill's private
vocabulary — the terms its files use as headings, bold leads and state
names — stays in its files and the state block; in documents and in
chat, say the plain thing or introduce the term where it is first used.
A zone code is shorthand for the zone map: outside the map, write it with
its short name ("Z5 product shape"), and never a code the map lacks.

Agents: follow [references/agents.md](references/agents.md) whenever you
put one to work.

## The dossier

A topic's dossier is `docs/iflow/<topic-slug>/`: `iflow.md` plus one
`NN-<name>.md` per slice. [references/state.md](references/state.md)
holds its templates, the label contract, the birth checklist and the
quality test — read it before first creating or updating a dossier in a
session.

A first word `fast` calls the fast lane (shape.md §5); the rest is the
topic. Resolve in this order: the user names a dossier → the dossier
active in the conversation → a `docs/iflow/*/iflow.md` matching the topic
→ an unfinished Shape on this topic, found per "Draft recovery" in
[references/shape.md](references/shape.md) and resumed with no new "Too
light for slices?" weighing → none: weigh it per "Too light for slices?"
under Layer 1, and if it goes on, start Shape fresh.

If iflow.md exists: read it and the slice file its `Current slice:` names,
then continue from its `Next action:`. Never re-ask what it records;
never make the user re-approve what was approved.

## After a compaction

Before the next exchange, re-read `${CLAUDE_SKILL_DIR}/SKILL.md` and the
files holding the active work: during Shape,
[references/shape.md](references/shape.md) and the working draft; once a
dossier exists, iflow.md and the current slice file, plus
[references/state.md](references/state.md) while creating or repairing
it. The compaction summary is a pointer, not a source of truth.

## Layer 1 — Shape

**Too light for slices?** A new topic is weighed from the request alone,
before plan mode or any repo scan. When one plan covers it — one task,
one deliverable, nothing worth approving on its own — the whole turn is
one line in the user's language: the reason, then `/i:lite <task>`
(`/i:lite fast <task>` when the user called `fast` or the direction is
already settled); then stop for the user's call. Unsure means not too
light. Say it once, never again mid-way.

Otherwise read [references/shape.md](references/shape.md) first and
follow its three stages, or its fast lane when the user called `fast`.

## Layer 2 — the slice loop

Invariants:

1. Re-read iflow.md before starting and right after finishing each slice.
2. `Current slice:` and `Next action:` change the moment the next action
   changes, not at slice end; `Next action:` is one runnable imperative
   sentence ("EnterPlanMode for slice 03, explore only within X").
   Starting a slice is ONE write — the row goes `doing`, `Current slice:`
   names it, `Next action:` becomes its first step — made before
   `EnterPlanMode`; finishing one is likewise ONE write. A hook runs
   `${CLAUDE_SKILL_DIR}/scripts/check-dossier.sh` after every Edit or
   Write to iflow.md: fix what it reports before going on; a write made
   through Bash runs the checker by hand. Every write leaves the dossier
   consistent: a slice's file exists before its row does.
3. When a task-list tool is available, mirror the slice table into it so
   the user sees progress; iflow.md stays the single source of truth — on
   divergence, iflow.md wins.
4. Work only the chosen slice. A finding belonging to another slice gets
   one line in that slice file's notes; one belonging to no slice gets one
   line in iflow.md's section on what was explored — nothing may drop.
   Then return. While plan mode is on, carry such lines in the plan; its
   FIRST step writes them.
5. Verification evidence (scripts, screenshots, command output) lives in
   the repo, in `docs/iflow/<topic-slug>/evidence/NN-<name>/` — never in
   the session scratchpad, which is cleaned up. Evidence is never deleted,
   trimmed, overwritten or replaced by a summary; a second attempt writes
   beside the first under new names. Keeping it out of git is the user's
   `.gitignore` call, not this skill's.

**The approval gate.** Every plan i:flow puts to the user — the slice
table that closes Shape, and each build slice's plan — passes the
plan-mode approval button when plan mode is in use, and one
`AskUserQuestion` on the plan's own content when it is not; a question
that times out or is denied is not approval — stop there. Until a plan
passes its gate, work toward it is read-only: nothing is created,
changed, installed, migrated or deployed — no file, dependency, database,
external service or deployment. The only writes meanwhile: during Shape,
the working draft; once the dossier exists, also the dossier's own files,
as this skill directs. The line after the plan's last step also tells the
user, in their language, that approving with the context cleared is safe
and worth it when the conversation before this gate was long: the plan's
FIRST step re-reads what the next step needs.

**The stranger read before a gate.** Only when (1) the plan's own steps
write or delete real data — a production or shared environment's, never
local or test data — call a paid API, deploy or migrate, and then only
over those steps; (2) the user asks for it; or (3) the user said the work
must be done carefully or matters, judged by what they meant, not by the
words alone — recorded as a decision. Then one general-purpose agent
(never a Plan agent) that has not seen the conversation, told to change
nothing, reads the task and the plan to name missing choices, wrong
assumptions and unproven claims; fold what holds into the plan and give
each rejected candidate one line in it. Otherwise the plan goes to its
gate at once, with one line after its last step telling the user, in
their language, to answer `soát` for that read; the answer runs it, then
the plan returns to the gate. Apart from this read and stage 2's
fresh-eyes pass on the picture, no agent reviews or designs a plan,
whatever plan mode suggests.

**Build slices** run the build cycle:

1. `EnterPlanMode` when plan mode is in use; explore only within the
   slice's scope (deep code reading happens now, not earlier); reconcile
   against the slice's charter, its notes and iflow.md's decisions — a
   plan that departs from a decision says so at its gate (a Mid-flight
   decision). Heavy reading may go to Explore agents; writing code is
   never delegated: the main agent owns every edit.
2. Write the plan. Its FIRST step: re-read `${CLAUDE_SKILL_DIR}/SKILL.md`
   if it is no longer in context (a compaction, or a context cleared on
   approval); record into the slice file's approved-plan section — the
   plan names that file — a 3–7 line summary (what changes, proven by
   what at which boundary, deliberately skipping what) and the plan's
   steps as a numbered list, one line each, never its prose; write the
   lines carried for other slices (invariant 4); rewrite each decision
   line in iflow.md the plan departs from; point `Next action:` at the
   plan's next step. Its LAST step: steps 4 and 5 below, then
   "Auto-advance". A slice that changes code lists in its plan the tests
   covering that change; a repo with no test command of its own gets one
   built by the same plan.
3. After approval: verify with real commands, checked against the slice
   file's approved-plan section, not against memory; `/run` is the
   command when the proof boundary is the running app. When the repo has
   a test command, the proof runs the whole suite by default; a narrower
   run holds only when the approved plan named it with what it leaves out
   and why — the model never narrows the proof on its own. The first
   build slice whose dossier records no baseline runs the whole suite
   once, right after approval and before any change, and records each
   red by name, or "green", in iflow.md's section on what was explored;
   those reds fail no later proof and need no skip. Any other red fails
   the proof and takes one lane:
   - caused by this slice's change → fixed here;
   - caused by it but not explained by the failure output and the change
     just made → `/i:debug <the red output · the proof it breaks · the
     dossier's iflow.md path · the active slice file>` before any fix; the
     fix stays here under the approved plan;
   - in a test i:test wrote → "Tests from i:test" in
     [references/closing.md](references/closing.md);
   - any other → invariant 4; it stays in the suite only by a user order,
     skipped as that part describes.
   Running a suite that already exists is this cycle's own work with the
   project's runner, never a trip through i:test.
4. Review gate — only when the slice changed code (dossier files and
   research documents are not code): run `/code-review` at level medium
   over the files this slice touched and wait for its findings — a review
   still running is not one that could not run. Reconcile each finding
   against the approved plan: a fix that would depart from it needs the
   user's decision first (Mid-flight decisions), recorded in the result;
   other findings inside this slice's Charter are fixed here and
   re-verified; any other takes invariant 4. A gate that could not run is
   recorded in the result and does not block the slice.
5. Write the result section: pass or not; evidence as commands + key
   output; when the review gate applied, the paths handed to it and what
   came back (findings, clean, or could not run); divergence from the
   approved plan; and, when the proof went through i:debug, its status,
   cause or gap, reproduction and decisive evidence.

**Research slices** skip plan mode: explore deeply within the slice's
scope; confer with the user only on something that would change the
slice's Charter or the document's main conclusion; then write the
finished document into the slice file, under the source discipline of
state.md §6. A research slice may delegate per formed question.

**Auto-advance** — finishing a slice does not end the turn. Once the
result section (or the research document) is written: update iflow.md
(slice NN done, next action at the next slice), re-read it (invariant 1),
announce in exactly one line which slice finished and whether it passed,
naming any gap its result records — for a research document, its file
path — then start the next slice in the same turn, even through another
approval gate. Advancing needs no approval; feedback arriving later
follows Mid-flight decisions. Stop only when a user decision is needed or
a report you commissioned has not come back; when every slice is done or
retired, read "Finishing" in
[references/closing.md](references/closing.md) and close the program in
the same turn.

## Mid-flight decisions

An explicit order is a decision; a question or praise is not. Write the
decision into iflow.md first, touch code after. If it changes the slice
table: rebuild the table from the current shape, re-submit it for
approval, then continue.

## Later in the loop

[references/closing.md](references/closing.md) holds the three parts
needed rarely or once; read the part when its moment comes, not before:
"Redoing a slice" when a finished slice's result is overturned or its
charter proves wrong; "Tests from i:test" when the user asks for
independent tests or an approved plan needs coverage nothing provides,
and for any red in a test i:test wrote; "Finishing" the moment every
slice reads done or retired.
