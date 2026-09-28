---
name: lite
description: >-
  Shape one task whose direction is not settled yet: map the open
  questions, research them, decide with you, then build and prove one
  plan. No slices, no dossier; research notes go to docs/research/.
  `fast` skips the shaping and goes straight to a plan that lists its
  assumptions for you to veto at the gate.
argument-hint: "[fast] <task>"
disable-model-invocation: true
---

# i:lite — shape, then one plan

One task, one plan. i:lite runs i:flow's Shape stages 1–2 — or skips them
on the user's word — then writes ONE consolidated plan, passes it through
the gate, builds it and proves it. Core invariant: **facts live in files,
not in conversational memory** — during the run they live in the working
draft (the plan file, including its research notes and decisions), and
research notes become `docs/research/<topic-slug>/*.md` files at the plan's
first step.

**Hard rule.** i:lite never creates or edits anything under `docs/shape/`,
and never cuts the work into slices. Work that outgrows one plan is
`/i:flow`'s — see "Too big for one plan?" below.

Language: protocol skeletons — file names, the draft's two lines in
references/shape.md §0, this skill's own files — are English. Everything
else a document holds, headings included, and every word spoken to the
user follow the user's language. A sentence the user has to look up is a
failed sentence: the protocol's private vocabulary — terms like lane,
fresh-eyes pass, ripe, and zone codes — stays in this skill's own files
and the zone map; in documents and in chat, say the plain thing instead,
or introduce the term right where it is first used.

Agents: the few rules for putting one to work — never passing a `name`,
condensed returns that land in files, the ≤3 ceiling — live in
[references/agents.md](references/agents.md). Read it in the turn you are
actually about to spawn something.

After editing this skill's own files, run
`${CLAUDE_SKILL_DIR}/../flow/scripts/check-pointers.sh ${CLAUDE_SKILL_DIR}`
— i:flow's checker, pointed at this directory.

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

If mid-run the need collapses to pure understanding with no repo
deliverable, hand off to i:explore instead.

## After a compaction

Before the next exchange, re-read this SKILL.md and the active plan file.
If stages 1–2 are still running, also re-read
[references/shape.md](references/shape.md). The compaction summary is a
pointer, not a source of truth; facts live in those files. i:lite never
has a dossier, so no resume hook fires: this rule is the only reload. If
the draft's path was lost, recover it per "Draft recovery" in
[references/shape.md](references/shape.md).

## Two lanes

**Full lane** (default): stages 1–2 per
[references/shape.md](references/shape.md) — read it before the opening
round. Its opening round may recommend going straight to the plan when the
zones are already clear; the user decides.

**Fast lane** (`fast`): stages 1–2 are skipped on the user's word, never on
the model's. In order, before the gate:

1. Scan the repo within the task's scope. Research only under the two
   conditions of "Zone research" in
   [references/shape.md](references/shape.md); notes go into the draft's
   research notes under the same source discipline.
2. The deep read (below), then write the plan. Its assumptions section
   names every axis that would have been a zone and the choice taken for
   it — the user must be able to veto an assumption at the gate without
   reading code.
3. Fresh-eyes pass on the draft plan: hand the task and the draft plan to
   one subagent to read as a stranger and name missing axes, wrong
   assumptions and unproven claims; otherwise take the pass yourself,
   deliberately. Fold what holds into the plan; list each rejected
   candidate in one line among the assumptions.
4. The gate. A rejection that names a zone ("discuss X", "bàn X") opens
   stage 1 with the draft plan as the starting picture; the run continues
   as the full lane.

## The plan

**Deep read.** After the lock (full lane) or the scan (fast lane), read the
code within the locked scope — stage 1 stopped at what comparing options
needed, so this is where how-to detail comes from. Heavy reading may be
delegated to Explore agents under
[references/agents.md](references/agents.md); returns come back condensed,
and their count goes in the report.

**Too big for one plan?** Weighed twice, raised at most once per run.
At the start, from the request alone — before plan mode, any reference or
any scan: when the request itself names several increments each worth
approving on its own, that turn is one line in the user's language, the
reason and then `/i:flow <task>`. Nothing else, then stop for the user's
call. Unsure means go on. At the plan: when the picture shows work that
will not finish in one session, or several increments each worth
approving on its own, say so at the top of the plan with the reason and
recommend `/i:flow`; the user decides at the gate. A user who chose to
stay with i:lite at the start has that choice written into the draft's
decisions the moment the draft opens, so neither the plan nor a later
session raises it again. Handing over loses no decision, research note,
picture or draft plan: the plan file is i:flow's draft format, and
i:flow's draft recovery carries all four across.

**Contents.** Written into the plan file right after the picture, ahead of
the decisions — the draft order in references/shape.md §0 — in the user's
language:

- FIRST step: write each research-notes subsection to
  `docs/research/<topic-slug>/<zone-slug>.md` — skipped when there are
  none, or on the no-plan-mode path, where they already are files.
- What changes, proven by what at which boundary, deliberately skipping
  what. A change to code lists the tests covering it and the test run that
  is the proof — the whole suite unless a narrower run is named with what
  it leaves out and why; a repo with no test command of its own gets one
  built by the same plan.
- The assumptions: every choice the user did not make explicitly — always
  present in the fast lane; in the full lane, for delegated zones and
  zones taken straight to the plan.
- LAST step, in this order: finish the proof; run and reconcile the
  review gate if code changed; write the completion block into the plan
  file right after the plan — its own heading in the user's language,
  holding pass or not, the commands run with their key output, the review
  gate's outcome, divergence from the approved plan, and the research
  files written; then retire the draft's marker — its `Shape draft:
  <topic>` line becomes `Shape draft done: <topic>`, which draft recovery
  no longer matches, so a finished run stops being a candidate while an
  interrupted one still is; then write the report in chat — per "Build
  and prove" and "The report" below. Interrupted before the completion
  block, the run stays recoverable; interrupted after it, the file already
  holds the whole result.

**The gate.** The plan passes the plan-mode approval button when plan mode
is in use, and one `AskUserQuestion` on the plan's own content when it is
not. Until it passes, no implementation file — code, configuration,
migration, test — is created or changed: the only writes are the working
draft and, on the no-plan-mode path, its research-note files. Plan mode
enforces this on its own path; on the other, only this rule does. This is
the only definition of the gate; everywhere else points here.

## Build and prove

1. Re-read the plan file and mirror its steps into the todo list. The plan
   file is the source of truth — on divergence, it wins.
2. Verify with real commands, checked against the approved plan in the
   plan file, not against memory. When the proof boundary is the running
   app, `/run` is that command. When the repo has a test command, the
   proof includes one run of the whole suite by default; a narrower run
   holds only when the approved plan named it with what it leaves out and
   why — the user accepted that at the gate, the model never narrows the
   proof on its own. A red run is a failed proof. A red this change caused
   is fixed here; when the failure output
   and the change just made do not explain it, it goes to
   `/i:debug <the red output · the proof it breaks · the active plan
   file>` before any fix — that skill proves the cause and changes
   nothing; the fix stays here under the approved plan. A red this change did not cause is reported, not
   touched. Running a suite that already exists is this skill's own work
   with the project's runner; independent new tests are `/i:test`'s, called
   by the user when they want them.
3. Review gate — only when code changed (research notes and the plan file
   are not code): run `/code-review` at level medium over the files this
   run touched. That skill forks its own reviewer, so wrapping it in an
   agent buys nothing. Reconciling the findings against the approved plan
   is the main agent's own work. Findings inside the plan's scope are fixed
   and re-verified; any other finding is reported. A gate that could not
   run is reported and does not block.

**Mid-flight decisions.** An explicit order is a decision; a question or
praise is not. Write the decision into the plan file's decisions first,
touch code after. If it changes what the approved plan does, rewrite the
plan and pass the gate again.

## The report

The run ends with one report in chat, in the user's language — the same
facts as the plan file's completion block, which serves resume and audit
while this report serves the user at the moment of completion. i:lite
creates no dossier or evidence directory in the repo.

- Pass or not.
- Evidence: the commands run and their key output.
- The review gate's outcome: the paths handed to it, and what came back —
  findings, clean, or could not run.
- Divergence from the approved plan.
- When the proof went through i:debug: its status, cause or gap,
  reproduction and decisive evidence.
- The research files written.

When the run changed code, close with one line: this change has not passed
`/security-review`, run it BEFORE pushing.
