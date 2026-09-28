---
name: debug
description: >-
  Investigate an observable defect from an independent context: reproduce it,
  find the first bad commit, test a named suspect, or prove its cause; the fix
  stays with the caller. Open it before investigating on your own whenever the
  user reports a wrong value, a crash or hang, a red or flaky test, a
  slowdown, a production or end-user report, a job that "ran" but left nothing
  behind, or a breakage after a change ("từ hôm qua tự dưng …") — in code, in
  a service, or on the user's own machine (driver, display, input method).
  Even when put casually: "check cho anh vì sao …", "kiểm tra xem có đúng do X
  không", "điều tra xem vì sao …", "xem giúp anh chậm / lag do đâu", "why is
  this happening". Prefer it over engineering:debug unless the user explicitly
  asks to fix it in the same go. Not for adding a feature, a review sweep, a
  cause already proven, or explaining a design nobody claims is broken
  (i:explore / learn). Runs in a fresh fork: pass the symptom, how to see it,
  what it should do, and what changed last in the arguments.
argument-hint: "[symptom · how to see it · what it should do · what changed last · what is asked, if less than a cause]"
context: fork
background: false
---

# i:debug — reproduce it, then prove the cause both ways

`$ARGUMENTS` carries the symptom and, where the caller has them, the mission,
how to see it, what should have happened, a suspect, what changed last and
what is already ruled out. Whatever it does not carry is resolved by the rules
below, never guessed.

Default to proving the cause. When the caller asks for less than a cause — a
reproduction, the first bad commit, a verdict on a named suspect — stop there,
with the same report.

This run owns the diagnosis and its evidence. The fix belongs to the caller:
the conversation that invoked this run, or the i:flow slice it came from.
Nothing is changed for keeps here — not code, not a live system, not a
dossier. Everything below is a delta from your defaults; where nothing is
said, your defaults are right.

## Commitment — settled before the target is opened

Before the target is read, write down and keep: what was observed, verbatim;
what should have happened instead and where that expectation comes from; how
often and under what conditions; when it last behaved correctly. That last
point is the cheapest cut there is: the diff from then to now — the working
tree against HEAD when the tree is dirty — is measured before anything else
is read.

- **Source** — a commitment that already exists: the sentence the caller
  states, docs, a schema, an API contract, the written description of a
  process, a test that was green, an i:flow dossier's picture (the body of
  its shape.md). Never how the target behaves today, never what merely
  seems reasonable. A crash,
  a hang, data loss, or an unhandled error the target itself raises is a
  defect without any of those.
- **Precedence** — the caller's sentence outranks every other commitment;
  docs, a schema or a contract outrank a test that was green. A commitment
  overridden that way is named in the report.
- **Gap** — nothing states the correct behaviour, or a disagreement nothing
  above settles: name both sides. This run ends there, blocked, naming the
  exact `/i:debug <symptom · expectation>` call that resumes it, carrying
  every field the original argument had and what this run ruled out.
- **Match** — behaviour that matches the commitment is not a defect. The
  match is measured, not read: run the class of input the commitment names,
  not only the caller's one example, and a member that misses it is a defect
  this run keeps. Otherwise say which — a misunderstanding is i:explore's,
  a wish is a feature and i:flow's — in one line and end.

## What is already in hand

| In hand | Reproduction | Proof both ways comes from |
|---|---|---|
| A red test or a failing command | Exists: run it once to confirm, then shrink it while the defect survives | Putting the cause back and running it again |
| Only a trace — log lines, a production report, a case that went wrong | The captured occurrence with its evidence trail; make a local one only when one input or one request does it | Once a local reproduction exists, the first row applies; otherwise a toggle the target already owns — a flag, a config, a rollback — named as the next step, never operated by this run on a live system; until it runs, the cause is a hypothesis |
| A cause the caller names | A hypothesis, tested first and like any other | The row that fits the symptom |
| An intermittent or quantitative defect — flaky, slow | A number over N runs | Both tests measured over the same N |
| A step people follow went wrong | The written procedure against the record of that case | Named as the next step; until it runs, a hypothesis |

Cannot reproduce here → first measure the conditions that differ between
where it fails and here; then every conclusion carries that flag, and the
deliverable is the leading hypothesis, labelled as one, plus what would
settle it. No observable symptom in the argument and none from the target's
own runner → end with the resume call; never sweep the repository for
something wrong.

Reproduction and both tests run only where they are reversible and isolated —
never on a live system or a shared dataset. Instruments are the target's own
first: its runner, its logs, the record its process already keeps; `/run`
when the boundary is the app. A profiler, debugger, tracer or sanitizer when
those cannot separate the hypotheses that remain. `git bisect run` with the
reproduction command is the measurement on the time axis — always in a
separate `git worktree`, removed before the report. That worktree carries
none of the main tree's installed dependencies or build output, so the
command must go red on the bad end and green on the good end inside it
before the bisect starts.

## Prove it in both directions

The symptom disappearing is not proof. A cause is named only when all three
hold:

- **Remove it** — remove or correct the suspected cause and the symptom
  goes.
- **Put it back** — and the symptom returns: the only test separating the
  cause from a change that merely coincided.
- **Accounts for everything** — the cause explains every part of the
  symptom. A fragment that survives removing the cause is a second defect:
  one line under Not explained with its own `/i:debug` call. A fragment
  that goes with it but is not explained means the wrong cause.

A cause may be a set — several factors needed at once, so removing any one
makes it go. Name the set.

Name **where the wrong state is created**, not merely where it shows: a
check at the crash site hides the defect and leaves the source free to do it
again.

Changing the target in order to measure is an instrument, not a fix:
allowed, and put back before the report. Before the first change, record
`git rev-parse HEAD`, `git status --porcelain`, `git diff` and
`git diff --cached`; at report time all four must match, and that match is
the evidence that the target stands as it was found. Put back means
reversing this run's own edits: `git checkout`, `git restore` and `git stash`
also take the caller's uncommitted hunks in that file, so they are never the
way back, and a file this run did not change is never restored. Reversal is
an exact-match edit whose old text is what this run inserted: a file that no
longer matches is reported under Working tree, never overwritten.

## Report

In the language the caller wrote `$ARGUMENTS` in — not that of a pasted trace
— only the lines that have content: Status — proven, hypothesis or blocked ·
Symptom · Where the expectation comes from · Reproduction · Ruled out, and by
what · Cause · Evidence · Where it is created · Not explained · Working tree ·
Next step.

Evidence is the real output of the commands that ran; the report and the
target's own artifacts are the record — no ledger, no case IDs, no inventory
of what was tried.

**Next step** is runnable, chosen by size:

- The fix sits inside the proven cause → the diff this run applied for the
  remove-it test, verbatim, when that diff is the fix and not an instrument —
  a disabled cache proves a cause and fixes nothing — otherwise the change to
  make and where. Either one is checked against the whole commitment written
  down at the start, not only the symptom that surfaced; what it leaves
  uncovered is said there, never implied covered. With it, the reproduction
  command that re-proves it; when the target is code with a runner and no
  existing test already pins the commitment, add `/i:test <scope · the
  reproduction as the case · the commitment as the oracle>`.
- The fix is larger than the cause — restructuring, several concerns, a
  class of defect rather than one instance → `/i:flow <the diagnosis>`.

The same defect seen elsewhere gets one line; fixing those is the caller's
decision.

Called from i:flow, read the dossier the caller names — its
`Current slice:` line, the picture and decisions in its shape.md's body,
and the active slice's charter (what its slice file states first) — for
the commitment, and return these same items.

## Never

Never act on a hypothesis before a reproduction exists or the cannot-reproduce
flag is raised. Never explain WHY before a measurement has narrowed WHERE.
Never change two things between two measurements. Never re-check a place a
measurement has already cleared — for an intermittent defect, cleared means
over N runs, not once. Never weaken, skip or rewrite a check to
make a red go away. Never let a reading of the target stand in for a
measurement.
