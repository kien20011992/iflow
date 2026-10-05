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
Expected results come from the contract, never from the implementation.
This run writes test files and their fixtures only — never product code,
never an i:flow dossier.

## Scope

Resolve in this order: an explicit user scope → the active i:flow slice →
one coherent changed public surface, changed meaning off the default branch
the working tree plus the commits since it; on the default branch the
working tree when it has changes, otherwise the last commit when the
request points at a change just made → ask, in one line, when nothing or
several unrelated surfaces changed. An ask ends this run, so name each
candidate — each changed surface, or when nothing changed the main public
modules and the whole repository — as the exact
`/i:test <candidate scope · original intent · every supplied acceptance criterion>`
call that resumes it, never a promise to continue. Never default to the
whole repository. A scope of several public surfaces — the whole
repository when the user names it — takes one surface at a time through
expectations, risk pass, tests and run until every surface is done; any
surface left without a test goes under Not covered with the specific
reason it could not be completed. The active slice is the one the
`Current slice:` line names in the dossier the caller names; `—` means
none, and a call that names no dossier has none. A diff says WHERE to look
— its file list and changed signatures; its hunks wait until the
expectations are written — never WHAT is correct.

## Expectations — written before any implementation body is read

Write down in this run's own working notes — never a file left behind —
and keep: scope · requested intent · public boundary · oracle
sources · observable response · final state · must-not-change effects ·
repeat-call semantics · isolation constraints · explicit exclusions ·
contract gaps. Per scenario, keep only the effects that apply: a pure
parser has a response alone; a rejected write adds its final state and
what must not change; a retried import needs all four, inside one
scenario. Never invent a case to fill a slot.

Oracle, in priority: the user's acceptance criteria → the dossier's
picture and decisions (shape.md's body) and the active slice's charter
(what its slice file states first) → public docs, schemas, APIs and
exported contracts, an exported symbol's signature, types and doc comment
included when the change under test did not write them. Never an oracle:
implementation bodies, diff hunks, current runtime behaviour, a snapshot
the run records, the slice file's approved plan, result and notes,
comments inside bodies. Where the contract is silent, report a contract
gap: never invent an expected result, never assume every invalid input
owes a typed error, and write characterization tests only on request.

## Risk pass — after the expectations are written

Read bodies and diffs for what the outside cannot see: decoding and
conversion, boundary conditions, write and transaction order, cache keys,
cleanup after failure, retry and idempotency, races over shared state, and
the seams and fixtures worth testing through. Every risk must map back to
an expected result or a public property; one that cannot is a gap, not a
new expectation.

**Strict black-box**, only when the user asks for it: skip the risk pass,
read no body or diff hunk, and report a boundary that needs a private API
as a blocker — never fall back silently.

## What to write

| Requested intent | Boundary that proves it |
|---|---|
| Unit | A public function or module behaviour |
| Integration / component | A module against a real DB, filesystem, queue or adapter |
| Contract | An API, schema, serialization or protocol |
| E2E | The outermost user-visible boundary |
| Property / fuzz | An invariant over a large input domain |
| Retry / time / concurrency | Lifecycle and temporal behaviour |
| Security behaviour | Contract-stated auth, permission, isolation, fail-closed — never an audit or a pentest |

With no layer stated, pick the cheapest boundary that proves the invariant,
and add a second layer only when it protects a different invariant — never
copy one assertion across unit, integration and E2E.

**Only what is missing**, when the intent asks only for a list of what has
no test yet, not for tests to be written: write and run nothing; match
each expectation against the existing tests by the already-covered rule
under Native implementation, and the report, saying plainly that nothing
was written or run, is the whole deliverable.

**E2E** runs on the project's existing harness: real wiring for what the
project owns, the existing sandbox, emulator or double for third parties,
cleanup that also runs when the test fails. Decline, retry and concurrency
go under "Not covered" unless they were asked for. No harness → a harness
gap; never call an
integration test E2E.

**Grouping.** Same setup, oracle and effect → one parameterized table or
subtest, each row carrying its own native name. One invariant that needs
several steps → one scenario test, never a chain of dependent tests.

## Native implementation

Follow the project's test config and neighbouring tests in placement,
naming, fixtures, helpers and parameterization.
Use a fake clock, a fixed seed and a unique namespace wherever determinism
needs them; a test that writes to a real store writes inside its own
namespace, and its cleanup removes only what it created. Mock the external
boundary, never the behaviour under test. No
real credential, production service or shared dataset. A dependency
already pinned in the project's manifest and lockfile may be restored with
the project's own recorded command (e.g. `npm ci`, `bundle install`,
`poetry install`) — never add a new dependency or framework, never edit a
manifest or lockfile, never fetch from outside the repo's declared
sources. Anything not already pinned, or missing config, is a blocker:
report it with the smallest prerequisite, never install it. Never delete
or weaken an existing assertion, nor a new one to reach green. An
expectation counts as already covered only when an existing test that the
normal test command requires to pass asserts it in full: at the same
public boundary, under the same conditions, on the same observable
result. An already covered expectation
gets no new test; otherwise extend an existing native table or
parameterized case when it is the smallest coherent home, or add a new
test. An existing assertion that contradicts the contract is a finding,
never something to correct. Each new test says in its docstring,
description or an adjacent comment, per the repository's convention,
what it expects and where that comes from —
quoting the user's criterion, or naming the document, dossier decision or
public symbol it relies on — so a red left behind can be traced back.

## Run

Outside Only what is missing, run the new or changed tests, and the
existing ones counted as already covered, with the project's own runner,
selecting them where the runner can select. The first run after your last
edit is the evidence — never run again just to capture it more cleanly. A
red is the test's own defect when its setup, fixture or import is wrong,
or its expected value claims more than its oracle source says: correct it
to the source's own words — never toward what the product returned — and rerun.
When the test matches its oracle and the product does not — a wrong value,
a crash — the assertion stays and the red is a finding. An import or
collection error is the test's own to fix unless the contract names that
public module and a bare import of it fails the same way in the runner —
then it is a product finding; missing test infrastructure is a harness
gap. A timeout or an inconclusive result earns one targeted rerun to
classify it; a second timeout in isolation is itself a finding. Widen to a
larger suite only when the user asks, the project's convention requires
it, or attribution is still unclear. Never mark expected-failure to keep a
suite green, never report a pass without a run that happened.

## Report

Beyond the test files, their fixtures and the runner's own artifacts,
nothing is left behind: no ledger, no case IDs, no dated comments, no
inventory file.

Return only the lines that have content, most important first: Findings,
each with the test's name, what its source says should happen, what
happened, and that the test stays red in the suite · Not covered, put as
the user's call whether to test it: every written expectation no new test
proves and no existing test already covers, each with why it was left and
the kind of test that would prove it — never a claim that the tests are
enough · Contract or harness gaps, each contract gap put as the question
the user must answer · Added or changed · Run and Result — each command
and what its output means, not a pasted log · Verified invariants, naming
the existing test where an expectation was already covered · Scope and
Intent / strategy, only where this run chose them rather than the
arguments, with why · Boundary ·
Oracle sources, saying plainly when the arguments carried no acceptance
criteria and where the expectations came from instead · Isolation. Write
it in the language the caller wrote `$ARGUMENTS` in and in plain words:
the names above are roles, not headings, and this skill's own terms —
oracle, invariant, boundary, harness, contract gap — are said by what
they stand for.
