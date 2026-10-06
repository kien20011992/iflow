# Later in the loop — redoing a slice, tests from i:test, finishing

These three parts of the slice loop are needed rarely or once: read the
part the moment SKILL.md points at it, not before. "Invariant 4",
"step 3", "Mid-flight decisions" and "Charter" below are SKILL.md's.

## Redoing a slice

A small finding inside a finished slice's Charter — a sentence to fix, a
line to restore — is not a redo: fix it at once, re-run that slice's
checks, and record it under the slice's result as a second attempt, one
line each; the table does not change. Charter still right but the result
overturned → the row becomes `needs-redo` and the slice reruns the full
cycle of its type; the reason goes into its notes, and its approved plan
and result get fresh entries headed as a second attempt, the old ones
kept. Charter wrong → not a redo: retire NN (`retired`) and cut a new
slice with a new number per the NN identity rules in
[state.md](state.md), its file created before its row; name the retired
slice in the decision line. Marking `needs-redo` edits the slice table,
so it is a Mid-flight decision — a user order, or evidence the model
presents with the re-submitted table, which lists each finished slice
naming it under "Needs first" with a judgment of whether it is affected;
affected ones also go `needs-redo` and rerun in the original order.

## Tests from i:test

i:test writes new independent tests from a fresh fork. Call it only when
the user asks for independent tests, or when an approved plan needs
coverage (unit, E2E, contract or adversarial) that nothing provides yet —
never as an automatic second pass over verification that already proved
the slice. Before the call, write every decision changed in this
conversation into the dossier: the fork reads only the dossier and its
arguments. The handoff is one plain sentence, not a schema: the slice and
its dossier path, the focus, the constraints, and that the dossier's
picture and decisions and the slice's charter are the oracle. Condense
what comes back into the slice's result; the next action stays this
flow's own call.

A red in one of those tests is a finding about the product, not a broken
test. One this slice's own change never touched is judged against the
contract first; a cause that leaves unexplained takes the i:debug lane of
step 3. Inside the current slice's Charter: fix the code and re-verify.
Outside it: the finding takes invariant 4 and the test is skipped. Leaving
any red open on purpose — one of those tests or any other — takes a user
order (a Mid-flight decision) and skips the test the same way. A skip
uses the runner's own skip marker, never a throwaway command-line flag,
with a reason pointing at the line just written; skips are this flow's
only edits to such a test — never delete it, never loosen its assertion.
A harness or contract gap, or an expectation i:test left uncovered, blocks
calling the slice a pass when the slice required that coverage.

## Finishing

When every slice reads done or retired: if code changed after the last
whole-suite run, run the whole suite once more, never narrowed, per step 3
of the build cycle. A red beyond those recorded at the baseline means not
done — each takes its lane there, and a slice already reading done that
has to carry a fix goes through "Redoing a slice" above; finishing resumes
once none is left.

Then write the summary — each slice, its product, file paths, what was
deliberately left open, and any baseline red still red — at the top of
iflow.md's body, above the picture, and copy the program's result to
`assets/iflow/` beside `docs/` at the same root: the summary alone as
`assets/iflow/<topic-slug>.md`; when the program also produced finished
documents (research slices, document part only) or a web page, a
directory `assets/iflow/<topic-slug>/` holding the summary and each of
them. It is a copy — the dossier stays as it is — and nothing already in
`assets/iflow/` is ever overwritten, not even this program's own earlier
copy: a later copy takes a new name beside it. Only once the copy exists,
set the overall status line in iflow.md to done and post the summary in
chat as the end-of-program announcement. When the program changed code,
it closes with one line: the program has not passed `/security-review`,
run it BEFORE pushing.
