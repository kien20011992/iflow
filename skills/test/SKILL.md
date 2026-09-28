---
name: test
description: >-
  Write NEW tests that prove observable behaviour at a public boundary, in the
  project's own runner, from a fresh context that never saw the code being
  written. Use it whenever the user asks for tests to be written, however
  terse: "unit src/utils và src/validators", "integration checkin.service với
  MySQL test", "contract API toàn bộ route qua supertest", "retry <job> với
  mock lỗi rồi thành công", "thêm regression test cho bug vừa sửa", "e2e luồng
  đăng ký bằng playwright", "app sắp bàn giao mà chưa có test, viết cho đủ".
  Prefer it over testing-strategy whenever tests are to be written, not only
  planned. Not for rerunning an existing suite, a red or flaky test to
  diagnose (i:debug), a review sweep (code-review), or merely because code was
  just implemented. Runs in a fresh fork with no conversation history: pass
  the scope, intent and every user-stated acceptance criterion in the
  arguments.
argument-hint: "<scope> · <intent> · <every acceptance criterion stated so far>"
context: fork
background: false
---

# i:test — lock the oracle, then prove it in the runner

`$ARGUMENTS` carries a scope (the behaviour to test), an intent (test
type, focus, constraints) and any user-stated acceptance criteria; a
missing scope or intent is resolved by the rules below, never guessed.
Fresh eyes are the point: this run starts in its own context and never saw
the code being written. Expected results come from the contract — never
from the implementation, the behaviour it happens to have today, or an
existing assertion that contradicts the contract. This run writes test
files and their fixtures only — never product code, never an i:flow dossier.

## Scope

Resolve in this order: an explicit user scope → the active i:flow slice →
one coherent changed public surface, changed meaning the working tree plus
the commits since the default branch → ask, in one line, when nothing or
several unrelated surfaces changed. An ask ends this run — this context
cannot wait for an answer — so name each candidate as the exact
`/i:test <candidate scope · original intent · every supplied acceptance criterion>`
call that resumes it, never a promise to continue. Never
default to the whole repository, never pick a dossier by fuzzy match. The
active slice is the one a `docs/shape/*/shape.md` names on its
`Current slice:` line — none or `—` means no active slice, several dossiers
means ask. A diff says WHERE to look, never WHAT is correct. Explicit scope
beats the active slice; say so when it lands off-slice.

## Charter — settled before the target is opened

Write down and keep: scope · requested intent · public boundary · oracle
sources · observable response · final state · must-not-change effects ·
repeat-call semantics · isolation constraints · explicit exclusions ·
contract gaps.

Oracle, in priority: the user's acceptance criteria → the dossier's
picture and decisions (shape.md's body) and the active slice's charter
(what its slice file states first) → public docs, schemas, APIs and
exported contracts. Never an oracle: implementation bodies, diff hunks,
current runtime behaviour, a snapshot the run records, the slice file's
approved plan, result and notes, code comments. Where the contract is
silent, report a contract gap: never invent an expected result,
never assume every invalid input owes a typed error, and write
characterization tests only on request.

## Risk pass — after the charter is locked

Read bodies and diffs for what the outside cannot see: decoding and
conversion, boundary conditions, write and transaction order, cache keys,
cleanup after failure, retry and idempotency, races over shared state, and
the seams and fixtures worth testing through. Every risk must map back to a
charter invariant or a public property; one that cannot is a gap, not a new
expectation.

**strict black-box** — only when the user asks for it: no target body, no diff hunks.
Public interfaces, docs, schemas, runner config, harness and fixtures stay
readable; existing tests teach syntax and setup only, never expectations.
Never fall back to the default mode silently — when the boundary cannot be
exercised without an implementation-private API, report a blocker.

## What to write

| Requested intent | Boundary that proves it |
|---|---|
| Unit | A public function or module behaviour |
| Integration / component | A module against a real DB, filesystem, queue or adapter |
| Contract | An API, schema, serialization or protocol |
| E2E | The outermost user-visible boundary |
| Property / fuzz | An invariant over a large input domain, only where the project already owns the tool |
| Retry / time / concurrency | Lifecycle and temporal behaviour |
| Security behaviour | Contract-stated auth, permission, isolation, fail-closed — never an audit or a pentest |

With no layer stated, pick the cheapest boundary that proves the invariant,
and add a second layer only when it protects a different invariant — never
copy one assertion across unit, integration and E2E.

**E2E** goes through the outermost public boundary on the project's existing
harness: real wiring for what the project owns, the existing sandbox,
emulator or double for third parties, a unique data namespace, cleanup that
also runs when the test fails, the whole journey in one scenario, response
and observable final state both asserted. Decline, retry and concurrency go
under "Not covered" unless they were asked for. No harness → report the
harness gap and the smallest prerequisite; never install a framework, never
call an integration test E2E, never fake a run.

**Grouping.** Same setup, oracle and effect → one parameterized table or
subtest, each row carrying its own native name. One invariant that needs
several steps → one scenario test, never a chain of dependent tests. A
different lifecycle, oracle, main effect or runner → a separate test.

**Per scenario, ask what applies**: what comes back, what state is left
behind, what must not have changed, what a second call does. A pure parser
answers the first; a rejected write answers the first three; a retried
import answers all four inside one scenario. Never invent a case to fill a
slot.

## Native implementation

Find the project's own test command, config and neighbouring tests first,
then follow its naming, fixtures, helpers and parameterization. Keep the
default scheduler; go serial only for a genuinely shared resource, and say
why. Use a fake clock, a fixed seed and a unique namespace wherever
determinism needs them. Mock the external boundary, never the behaviour
under test. No real credential, production service or shared dataset. A
missing dependency or config is a blocker: report it with the smallest
prerequisite, never install it. Placement and naming follow the project's
convention — its lane for generated tests when it has one.
Never delete or weaken an existing assertion. Extend an existing native
table or parameterized case when it is the smallest coherent home;
otherwise add a new test. An existing assertion that contradicts the
contract is a finding, never something to correct. Each new test names its
oracle source in its docstring, description, or adjacent comment, following
the repository's convention, so a red left behind can be traced back
without a marker in the file name.

## Run

Run the new or changed tests once with the project's own runner, selecting
them where the runner can select. That first run's output is the evidence —
never run again just to capture it more cleanly. A defect
in the test is fixed and rerun. Anything coming from the product — a wrong
value, a crash — keeps its assertion and becomes a finding: never edit
product code to make a test pass, and report the mismatch instead. An
import or collection error is unclassified until one of these holds: the
new test or fixture breaks the repository's import, placement or setup
convention → fix the test and rerun; required test infrastructure is
missing → harness gap; the contract requires that public surface and the
same failure reproduces outside the new test's setup, e.g. from a bare
import in the runner → product finding. A timeout or an inconclusive result earns one targeted
rerun to classify it; a second timeout in isolation is itself a finding.
Widen to a larger suite only when the user asks, the project's convention
requires it, or attribution is still unclear. Never weaken or delete an
assertion to reach green, never mark expected-failure to keep a suite green,
never report a pass without a run that happened.

## Report

The deliverable is native test files, the fixtures they need, and whatever
artifacts the runner itself produces — no ledger, no case IDs, no dated
comments, no inventory file. The runner's output is the evidence, the native
test name is the identity, git is the history.

Return, in the user's language, only the lines that have content: Scope ·
Intent / strategy · Boundary · Oracle sources · Added or changed · Run ·
Result · Verified invariants · Isolation · Not covered · Contract or harness
gaps · Findings. Oracle sources states "no user acceptance criteria were
supplied to this fork" when the arguments carried none; if the dossier or
public contract does not cover the scope either, that is a contract gap.

Called from i:flow, read the `Current slice:` line and the active
slice-table row (shape.md's closing state block), the picture, the
decisions and the active charter, and return those same items. i:flow
owns the dossier and the next action: never edit a dossier, never touch
product code.
