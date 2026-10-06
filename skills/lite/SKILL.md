---
name: lite
description: >-
  Shape one task whose direction is not settled yet: map the open
  questions, research them, decide with you, then build and prove one
  plan. For work with several parts worth approving one by one, use
  /i:flow. `fast` skips the discussion when the direction is already
  clear: the plan lists every choice made for you, so you can reject any
  before work starts. Research notes go to docs/iflow/<task>/research/.
argument-hint: "[fast] <task>"
disable-model-invocation: true
---

# i:lite — shape, then one plan

One task, one plan. i:lite runs i:flow's Shape stages 1–2 — or skips them
on the user's word — then writes ONE consolidated plan, passes it through
the gate, builds it and proves it. Core invariant: **facts live in files,
not in conversational memory** — during the run they live in the working
draft (the plan file, including its research notes and decisions), and
research notes, when the run has any, become
`docs/iflow/<topic-slug>/research/*.md` files at the plan's first step;
the plan itself stays in the plan file.

**Hard rule.** i:lite never creates or edits i:flow's files in a task
directory — `iflow.md`, the `NN-<name>.md` slice files, `evidence/` — and
never cuts the work into slices; it may add notes to that directory's
`research/`, where a name already taken gets a new one — never overwrite a
note another run wrote. Work that outgrows one plan is
`/i:flow`'s — see "Too big for one plan?" below.

**Where files go.** `docs/` and `assets/` here sit at the repository's git
root (the working directory outside git). When the user's request asks for
its result packaged as a document, that document goes to
`assets/iflow/<topic-slug>.md` — a directory `assets/iflow/<topic-slug>/`
when it is several files or a web page. `<topic-slug>` is the existing
`docs/iflow/*` directory on this task when there is one — above all the
one holding the i:explore dossier that seeded the run — else the task's
own slug.

Language: protocol skeletons — file names, the draft's two lines in
references/shape.md §0, this skill's own files — are English. Everything
else a document holds, headings included, and every word spoken to the
user follow the user's language, in words the user never has to look up:
the protocol's private vocabulary — terms like zone, lane, picture draft,
zone map, the zone states, fresh-eyes pass, stranger read, ripe,
Mid-flight — stays in
this skill's own files and the state block; in documents and in chat, say the plain thing
instead, or introduce the term right where it is first used. A zone code
is shorthand for the zone map: anywhere outside the map — the position
line above all — write it with its short name attached ("Z5 product
shape"), and never write a code the map does not have yet.

Agents: follow [references/agents.md](references/agents.md) whenever you
put one to work.

## Starting a run

The user's arguments: a first word `fast` selects the fast lane; the rest
is the task.

1. Weigh the request first, per "Too big for one plan?" below.
2. Enter `EnterPlanMode` unless plan mode is already on. Declined or
   unavailable → the no-plan-mode path under "The two run paths" in
   [references/shape.md](references/shape.md).
3. Attempt draft recovery, then open the working draft — both per
   "Working draft and the two run paths" in
   [references/shape.md](references/shape.md).

## After a compaction

Before the next exchange, re-read the active plan file, and while stages
1–2 are running also `${CLAUDE_SKILL_DIR}/references/shape.md`. The
compaction summary is a pointer, not a source of truth; facts live in
those files. If the draft's path was lost, recover it per "Draft recovery"
in [references/shape.md](references/shape.md).

## Two lanes

**Full lane** (default): stages 1–2 per
[references/shape.md](references/shape.md) — read it before the opening
round.

**Fast lane** (`fast`): stages 1–2 are skipped on the user's word, never on
the model's. In order, before the gate:

1. The deep read (below), seeded by an i:explore dossier when one matches
   (per "An i:explore dossier first" in
   [references/shape.md](references/shape.md)), then the plan; each axis
   the deep read finds enters the assumptions with its leaning. Research
   only under the two conditions of "Zone research" in
   [references/shape.md](references/shape.md), into the draft's research
   notes under its source discipline.
2. The gate. A rejection that names an assumption ("discuss X", "bàn X")
   opens stage 1 with the draft plan as the starting picture and the map
   already split: X in discussion, every other assumption deferred to the
   plan's assumptions; the run continues as the full lane.

## The plan

**Deep read.** After the lock (full lane) or at the start (fast lane), read
the code within the locked scope, or the task's scope in the fast lane —
this is where how-to detail comes from.
Heavy reading may be delegated to Explore agents; writing code is never
delegated: the main agent owns every edit.

**Too big for one plan?** Weighed twice, raised at most once per run. At
the start, from the request alone — before plan mode, any reference or any
scan: when the request itself names several increments each worth
approving on its own, the whole turn is one line: the reason, then
`/i:flow <task>` (`/i:flow fast <task>` in the fast lane) — i:flow cuts the
work into parts approved one by one;
then stop for the user's call. Unsure means go on. At the plan: when the
picture shows work that will not finish in one session, or several
increments each worth approving on its own, say so at the top of the plan
with the reason and recommend `/i:flow` (`/i:flow fast` in the fast lane);
the user decides at the gate. A
user who stays with i:lite has that choice written into the draft's
decisions as soon as the draft exists — approving a plan that carries the
recommendation is that choice — and this run does not raise it again.

**Contents.** Written into the plan file right after the picture, ahead of
the decisions:

- FIRST step: re-read `${CLAUDE_SKILL_DIR}/SKILL.md` if it is no longer in
  context (a compaction, or a context cleared on approval); rewrite each
  decision line in the draft the plan departs from; then write each
  research-notes subsection, if any, to
  `docs/iflow/<topic-slug>/research/<zone-slug>.md`.
- What changes; how we will know it works where a user or another system
  sees it — which tests, which run, or the running app; and what is
  deliberately left out. A change to code lists the tests covering it and
  the test run that is the proof — the whole suite unless a narrower run is
  named with what it leaves out and why; a repo with no test command of its
  own gets one built by the same plan.
- The assumptions: every choice the user did not make explicitly — a
  recovered draft's leanings included — one line each: what was chosen,
  the main alternative, and what changing it would change, readable
  without the code so the user can veto it at the gate. The user's own
  words at invocation are decisions, not assumptions.
- A plan that departs from a decision already recorded in the draft says
  so at the gate; the FIRST step above rewrites that line.
- LAST step, one plain line: finish the proof, review, write the result
  below this plan, report — per "Build and prove".

**The gate.** The plan passes the plan-mode approval button when plan mode
is in use, and one `AskUserQuestion` on the plan's own content when it is
not; a question that times out or is denied is not approval — stop there.
Until it passes, the run is read-only: nothing is created, changed,
installed, migrated or deployed — no file, dependency, database, external
service or deployment — except the working draft.

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

## Build and prove

1. Re-read the plan file; when a task-list tool is available, mirror its
   steps into it. The plan file is the source of truth — on divergence, it
   wins.
2. When the repo has a test command, run the whole suite once before the
   first change and write each red by name, or "green", into the plan
   file. Those reds are reported, never fixed here, and fail no proof.
3. Verify with real commands against the approved plan in the plan file,
   not against memory: run the proof it names, never a narrower one. When
   the proof is the running app, `/run` is that command. Any other red
   fails the proof. One this change caused is fixed here; when the failure
   output and the change just made do not explain it, it goes to
   `/i:debug <the red output · the proof it breaks · the active plan
   file>` before any fix — the fix stays here under the approved plan. One
   this change did not cause is reported, not touched.
4. Review — only when code changed (research notes and the plan file are
   not code): run `/code-review` at level medium over the files this run
   touched. Wait for its findings; a review still running is not one that
   could not run. A finding whose fix stays
   within the approved plan is fixed and re-verified; any other finding is
   reported. A review that could not run is reported and does not block.
5. Close: write the completion block right after the plan in the plan
   file — its own heading, holding the facts "The report" lists; then
   retire the `Shape draft: <topic>` line to `Shape draft done: <topic>`,
   in this draft and in any draft it recovered from; then the report.

**Mid-flight decisions.** An explicit order is a decision; a question or
praise is not. Write the decision into the plan file's decisions first,
touch code after. If it changes what the approved plan does, rewrite the
plan and pass the gate again.

## The report

The run ends with one report in chat, the same facts as the completion
block:

- First, one sentence: what now works differently, whether it passed, and
  what the approved proof left unproven, if anything.
- Evidence: each command run and what its output means ("212 tests, 0
  failed"), not pasted logs; any baseline red still red.
- The review's outcome: the files handed to it, and what came back —
  findings, clean, or could not run.
- Divergence from the approved plan.
- When the proof went through i:debug: its status, cause or gap,
  reproduction and decisive evidence.
- The research files written.

When the run changed code, close with one line: this change has not passed
`/security-review`, run it BEFORE pushing.
