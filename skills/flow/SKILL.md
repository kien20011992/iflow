---
name: flow
description: >-
  Shape a large or still-unsettled undertaking into user-approved vertical
  slices, then execute them one by one — code slices through plan mode,
  research slices as documents in the repo — tracked in
  docs/shape/<topic>/shape.md. Use it whenever the request spans several
  coupled pieces or has no clear start yet, however terse: "review toàn bộ …
  rồi tối ưu", "làm lại hoàn toàn / nâng cấp toàn diện X: a, b, c", "tìm mọi
  cách để …", "research X rồi dựng thành tool/repo chạy được", "viết bộ tài
  liệu về toàn bộ luồng …", a migration across api + app + admin — and
  whenever the user resumes such work ("hôm trước dừng ở …, giờ làm nốt").
  Prefer it over brainstorming when more than one deliverable is involved. Not
  for a single task one plan covers (thêm một tính năng nhỏ, sửa một hàm),
  pure understanding with no repo deliverable (i:explore), a defect (i:debug)
  or new tests (i:test).
argument-hint: "<topic to shape, or dossier to resume>"
disable-model-invocation: true
---

# i:flow — shape, then slice

Two layers. The Shape layer turns a large or ambiguous request into a
user-approved table of vertical slices; the slice loop executes the slices
one by one until done. Core invariant: **facts live in files, not in
conversational memory** — during Shape they live in the working draft
(the plan file itself, including its research notes — never a
second draft file alongside it), after the table is approved they live in
the dossier, and research notes become `docs/research/<topic-slug>/*.md`
files at dossier birth.

Language: protocol skeletons — file names, the state-block labels in
references/state.md §2 and the draft's two lines in references/shape.md §0,
this skill's own files — are English. Everything
else a document holds, headings included, and every word spoken to the
user follow the user's language. A sentence the user has to look up is a
failed sentence: the protocol's private vocabulary — terms like slice,
Charter, birth checklist, ripe, finding, Mid-flight, and zone codes —
stays in this skill's own files and the state block; in documents and in
chat, say the plain thing instead, or introduce the term right where it
is first used.

Agents: the few rules for putting one to work — never passing a `name`,
condensed returns that land in files, the ≤3 ceiling — live in
[references/agents.md](references/agents.md). Read it in the turn you are
actually about to spawn something, in either layer — not at session start,
where there may be nothing to spawn at all.

Each rule has exactly one home and every other place points at it. After
editing this skill's own files, run
`${CLAUDE_SKILL_DIR}/scripts/check-pointers.sh` — it catches pointers left
aiming at a file or section that no longer exists.

## The dossier

A topic's dossier lives at `docs/shape/<topic-slug>/`: `shape.md` plus one
`slice-NN-<name>.md` per slice. What `shape.md` is authoritative for, its
templates, the label contract table, the birth checklist, and the quality
test all live in
[references/state.md](references/state.md) — read it before first creating
or updating a dossier in a session.

Resolve in this order: the user names a dossier → the dossier active in the
conversation → a `docs/shape/*/shape.md` matching the topic → none yet:
weigh it per "Too light for slices?" under Layer 1 first; if it goes on,
attempt draft recovery (see "Draft recovery" in
[references/shape.md](references/shape.md)), else start Shape fresh.

If shape.md already exists: read it and continue from the next-action line
it records. Never re-ask what it already records; never make the user
re-approve what was approved.

## After a compaction

Whatever layer is running, before the next exchange re-read
`${CLAUDE_SKILL_DIR}/SKILL.md`, the reference governing that layer, and
the authoritative files for the active work:

- during Shape: [references/shape.md](references/shape.md) and the
  working draft;
- while creating or repairing a dossier:
  [references/state.md](references/state.md) and shape.md;
- during a slice: shape.md and the current slice file.

The compaction summary is a pointer, not a source of truth; facts live in
those files. During Shape no dossier exists yet, on either run path, so
the resume hook stays silent: this rule is the only reload. If the draft's
path was lost, recover it per "Draft recovery" in
[references/shape.md](references/shape.md).

If the next slice is large, offer a new session in one sentence (the
resume hook re-points the dossier), without pressing.

## Layer 1 — Shape

**Too light for slices?** This skill is invoked by hand, so a new topic is
weighed first, from the request alone — before reading any reference,
entering plan mode or scanning the repo. When one plan covers it — one
task, one deliverable, nothing worth approving on its own — that turn is
one line in the user's language: the reason, then `/i:lite <task>`
(`/i:lite fast <task>` when the direction is already settled). Nothing
else — no picture draft, no zone map, no other question — then stop for
the user's call. Unsure means not too light: go on to Shape. Say it once,
never again mid-way.

Otherwise the topic enters Shape: before anything else, read
[references/shape.md](references/shape.md) and follow its three stages —
it owns the plan-file conventions, the two run paths (plan mode /
no-plan-mode), the stage rules, and decision rights.

If mid-Shape the need collapses to pure understanding with no repo
deliverable, hand off to i:explore instead of shaping.

The moment the slice table passes its gate: create the dossier per the
birth checklist in [references/state.md](references/state.md), then enter
the slice loop within the same turn.

## Layer 2 — the slice loop

Invariants:

1. Re-read shape.md before starting and right after finishing each slice.
2. Update the current-slice and next-action lines in shape.md the moment
   the next action changes, not at slice end. The next-action line is one
   runnable imperative sentence. Once the dossier stops changing — after a
   lone edit, or at the end of a burst of them such as the birth
   checklist — run `${CLAUDE_SKILL_DIR}/scripts/check-dossier.sh
   <dossier-dir>` and fix what it reports. One run per burst, in the
   foreground: it is read-only and returns in well under a second, so
   backgrounding it only risks losing the answer.
3. Mirror the slice table into the todo list so the user sees progress;
   shape.md stays the single source of truth — on divergence, shape.md
   wins.
4. Work only the chosen slice. A finding belonging to another slice gets
   one line in that slice file's notes; one belonging to no slice gets
   one line in shape.md's section on what was explored — nothing may drop.
   Then return.
5. Verification evidence (scripts, screenshots, command output) must live
   inside the repo — e.g. `docs/shape/<topic-slug>/evidence/` — never in a
   session scratchpad, which dies with the session.

**The approval gate.** Every plan i:flow puts to the user — the slice table
that closes Shape, and each build slice's plan — passes the plan-mode
approval button when plan mode is in use, and one `AskUserQuestion` on the
plan's own content when it is not. Until a plan passes its gate, work
toward it is read-only: nothing is created, changed, installed, migrated
or deployed — no file, dependency, database, external service or
deployment. The only writes meanwhile: during Shape, the working
draft and, on the no-plan-mode path, its research-note files; once the
dossier exists, also the dossier's own files, as this skill directs. Plan
mode enforces this on its own path; on the other, only this rule does.
Nothing else about the cycle changes with the path. This is the only
definition of the gate; everywhere else points here.

**Build slices** run a plan cycle:

1. `EnterPlanMode` when plan mode is in use; explore only within the
   slice's scope (deep code reading happens now, not earlier); reconcile
   against the slice's charter and notes. Heavy reading may be
   delegated to Explore agents under
   [references/agents.md](references/agents.md) — returns condensed, their
   count declared in the result; writing code is never delegated: the main
   agent owns every edit.
2. Write the plan. Every plan put to the gate must have as its FIRST step:
   record into the slice file's approved-plan section a 3–7 line summary
   of the approved plan (what changes, proven by what at which boundary,
   deliberately skipping what) followed by the plan's steps as a numbered
   list, one line each — never the plan's prose; and as its LAST step, in the user's
   language, all four of: run the review gate if this slice changed code,
   write the slice's result, update shape.md (mark slice NN done, set the
   next action to the next slice), then re-read shape.md — and, if
   the conversation has been compacted since `${CLAUDE_SKILL_DIR}/SKILL.md`
   was last read, or the slice cycle cannot be recited from memory, follow
   "After a compaction" above; when unsure, follow it — and start that
   slice per this skill.
   A slice that changes code lists in its plan the tests covering that
   change; a repo with no test command of its own gets one built by the
   same plan.
3. After approval: verify with real commands, checked against the slice
   file's approved-plan section, not against memory. When the proof
   boundary is the running app, `/run` is that command.
   When the repo has a test command, the proof includes one run of the
   whole suite by default; a narrower run holds only when the approved
   plan named it with what it leaves out and why — the user accepted that
   at the gate, the model never narrows the proof on its own. A red run
   is a failed proof. A red this slice's own
   change caused is fixed here, a red in a test i:test wrote takes the
   rule in "Tests from i:test", any other red takes invariant 4 and stays
   in the suite only by the user order in "Tests from i:test". A red this
   slice caused whose cause the failure output and the change just made do
   not explain goes to `/i:debug <the red output · the proof it breaks ·
   the dossier's shape.md path · the active slice file>` before any fix: it
   proves the cause, changes nothing, and the fix stays here under the
   approved plan. This is the only home of the whole-suite rule and of the
   i:debug lane; everywhere else points here.
   Running a suite that already exists is this cycle's own work with the
   project's runner, never a trip through i:test.
4. Review gate — only when the slice changed code (dossier files and
   research documents are not code): run `/code-review` at level medium
   over the files this slice touched. That skill forks its own reviewer,
   so wrapping it in an agent buys nothing — the gate is ONE review job,
   not one agent. Reconciling the
   findings against the slice file's approved plan is the main agent's
   own work: it is the one that knows what was approved.
   Findings inside this slice's Charter are fixed here and re-verified;
   any other finding takes an existing lane (invariant 4, or Mid-flight
   decisions when it departs from the approved plan). A gate that could
   not run is recorded in the result and does not block the slice.
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
slice may delegate per formed question, under the rules in
[references/agents.md](references/agents.md).

**Auto-advance** — finishing a slice does not end the turn. After the
slice's result section is written (or once the research document is
complete): update shape.md, announce in exactly one line, then start the
next slice in the same turn — even when that means another trip through
the approval gate (its prompt is a legitimate gate, not a bug). Stop only
when a user decision is needed, a report you commissioned has not come
back yet, or every slice is done. Research documents need no user approval
before advancing — the one-line announcement with the file path suffices;
feedback arriving later follows Mid-flight decisions.

## Mid-flight decisions

An explicit order is a decision; a question or praise is not. Write the
decision into shape.md first, touch code after. If the decision changes
the slice table: rebuild the table from the current shape, re-submit it
for approval, then continue.

## Redoing a slice

Charter still right but the result overturned → mark the row "needs-redo":
the slice reruns the full cycle of its type; the reason goes into the
notes; loop-owned sections (approved plan, result) get fresh entries
headed as a second attempt, old ones stay as history. Charter wrong → not a redo:
retire NN (its row keeps status "retired") and cut a new slice with a new
number per the NN identity rules in
[references/state.md](references/state.md); name the retired slice in the
decision line.

Marking "needs-redo" changes the slice table, so it passes the Mid-flight
gate: a user order is a decision; if the model detects it itself, present
the evidence and re-submit the table. Finished slices that depend on it
(naming it in their "Needs first" column) do not flip automatically — list
each with a judgment of whether it is affected in the same re-submission;
those that flip also get "needs-redo" and rerun in the original order.

## Tests from i:test

i:test writes NEW independent coverage: it locks the contract as its
oracle in a context that never saw the code being written, then proves it
in the project's own runner. Call it only when the user asks for
independent tests, when an approved plan's verification needs coverage that
does not exist yet, or when a slice needs E2E, contract or adversarial
proof nothing covers. Never to run tests that already exist, never for a
document-only slice, never as an automatic second pass over verification
that already proved the slice.

The handoff is one plain sentence, not a schema: the slice and its dossier
path, the focus, the constraints, and that the dossier's picture and
decisions and the slice's charter are the oracle. Before the call, write every
decision changed in this conversation into the dossier: i:test runs in a
fresh fork and reads only the dossier and its arguments. What comes back — boundary, oracle
sources, the tests added, the command and its observed result, verified
invariants, gaps, findings — is condensed into the slice's result; the
next action stays this flow's own call. i:test edits neither the dossier
nor product code, and it names its tests by the project's own convention
rather than a marker of its own, so the result is where they are on record —
and each such test names its oracle source in its docstring or an adjacent
comment, which is
what identifies one that no result claims.

A red this flow cannot attribute — no result claims it and this slice's
own change never touched it — is judged against the contract before it is
filed anywhere: an unattributable red is more often one of those tests than
a broken one; when that judgement leaves the cause unexplained, take the
i:debug lane, per step 3 of the build cycle.

A red in one of those tests is a finding about the product, not a broken
test — equally so for a run the user commissioned in a separate session, in
parallel with development. Inside the current slice's Charter: fix the code
and re-verify. Outside it: the finding takes the lane of invariant 4, and
the test is skipped — the runner's own skip marker, never a throwaway
command-line flag — with a reason pointing at the line just written.
Leaving any red open on purpose — one of those tests or any other — takes
a user order (a Mid-flight decision) and skips the test the same way. Those
skips are this flow's only edits to such a test: never delete it, never
loosen its assertion. A
harness or contract gap i:test reported, for coverage the slice required,
blocks calling that slice a pass.

## Finishing

Before closing: one more whole-suite run, never narrowed, per step 3 of
the build cycle.
A red suite means not done — each red takes its lane there, and a slice
already reading done that has to carry a fix goes through "needs-redo"
above.
Finishing resumes once the suite is clean.

When every slice reads done: set the overall status line in shape.md to
done and summarize — each slice, its product, file paths, what was
deliberately left open — at the top of shape.md's body, above the
picture. When the program changed code, close with one
line: the program has not passed `/security-review`, run it BEFORE
pushing — its scope is everything since origin's default branch, so a
hole spanning two slices is invisible to any single slice's gate. This
is the end-of-program announcement.
