# The dossier — templates and rules

Contents: 1. Principles · 2. Label contract table · 3. Birth checklist ·
4. Template shape.md · 5. Template slice file and NN identity rules ·
6. Research-slice source discipline · 7. Quality test.

## 1. Principles

- `shape.md` is the single source of truth for the whole program's state,
  born the moment the slice table is approved (during Shape, the working
  draft lives in the plan file — except on the no-plan-mode path, where a
  draft shape.md plays that role; see references/shape.md). The native plan
  file (`~/.claude/plans/…`) is a per-session working copy outside the repo
  and may be cleaned up — never point to it as a source of truth, never copy
  a whole plan into the dossier (it will duplicate and drift). The dossier
  keeps only the two things most expensive to rebuild: approved intent and
  verified results.
- Update the `Current slice:` and `Next action:` lines the moment the next
  action changes, not at slice end. `Next action:` is always one runnable
  imperative sentence ("EnterPlanMode for slice 03, explore only within X"
  — reading it tells you exactly where the program stands), never a status
  description. (The checker script runs per the slice loop in SKILL.md and
  at step 6 of the birth checklist.)
- `Current slice:` names the slice whose row status is `doing` — starting
  with its two-digit NN — and reads `—` exactly when no row is `doing`. Starting a slice is therefore ONE
  write: the row goes `doing`, `Current slice:` names it, `Next action:`
  becomes its first step. A finished program writes `Overall status: done`,
  `Current slice: —`, and a `Next action:` pointing at the summary instead
  of a step to run. The checker enforces all of this.

## 2. Label contract table

These exact strings are a three-party contract. Changing any of them means
changing all three consumers in the same commit — the checker fails loudly
when they drift.

| String (exact) | Where it lives | Consumers |
|---|---|---|
| `Overall status:` — values `running` \| `done` | shape.md line 1 of status block | template §4 · hook `iflow-resume.sh` (lets a `done` dossier pass in silence only once the checker agrees) · `scripts/check-dossier.sh` |
| `Current slice:` | shape.md status block | template §4 · hook (prints it) · checker (cross-checks against slice-table statuses) |
| `Next action:` | shape.md status block | template §4 · hook (prints it) · checker (non-empty, non-placeholder) |
| Slice statuses `todo` \| `doing` \| `done` \| `needs-redo` \| `retired` | slice-table status column | template §4 · checker (valid-value set) |
| `<!-- generated-by: iflow/2 -->` | under the shape.md title | template §4 · checker (era detection) |

## 3. Birth checklist (the moment the slice table is approved)

1. Materialize research notes: every subsection under the draft's "Research
   notes" becomes a file `docs/research/<topic-slug>/<zone-slug>.md`
   (no-plan-mode path: the notes are already files — skip). This step has
   historically been skipped — do not skip it; the quality test checks it.
2. Create `shape.md` distilled from the approved plan and the draft: the
   locked picture (naming the fate of every left-open and cut zone),
   "Explored zones" fed from the zone map with each zone's leaning and
   LINKS to the research docs (never re-paste their content), "Sources"
   listing those doc paths, decisions, the slice table. Never copy the plan
   wholesale. No-plan-mode path: distill in place on the draft shape.md.
3. Create one slice file per slice, with its Charter.
4. Seed each slice file's "Pending notes": every deliberately-left-open
   item from Shape relevant to that slice gets one line marked "(from
   Shape)"; a left-open item relevant to no slice goes into "Explored
   zones" in shape.md — nothing may drop.
5. Set `Next action:` to the first slice.
6. Run `check-dossier.sh` on the dossier, then the quality test (§7),
   before leaving it.

## 4. Template `docs/shape/<topic-slug>/shape.md`

````markdown
# Shape: <topic name>
<!-- generated-by: iflow/2 -->

> AGENT: continuing from this file? Load the `i:flow` skill first (Skill
> tool, or read its SKILL.md wherever it is installed), then follow the
> Next action below. Facts live in this directory, not in conversational
> memory.

Overall status: running
Current slice: —
Next action: <one runnable imperative sentence>

<!-- Overall status values: running | done -->

## Locked picture

<the picture from the approved plan: why this program exists, scope, what
"done" looks like, the fate of every left-open and cut zone. Content in the
user's language.>

## Explored zones

<a few lines per zone: what was seen, the leaning, what it means for
slicing; link research docs in docs/research/<topic-slug>/>

## Sources

<documents, paths, URLs used — with confidence tier where it matters>

## Decisions

- <date> — <one line per decision, with the reason when it is expensive to
  rebuild>

## Slice table

| # | Slice | Goal | Type | Product | Needs first | Status |
|---|-------|------|------|---------|-------------|--------|

<!-- Type: build | research. Status: todo | doing | done | needs-redo | retired -->
````

## 5. Template slice file and NN identity rules

File name: `slice-NN-<name>.md`, created for every slice the moment the
table is locked. **NN identity rules:** two digits from 01, in run order at
first approval. NN is a permanent identity — rebuilding the table may
retire an old number or append new ones, never reuse or renumber; slice
files keep their names. The Charter is immutable after creation; everything
that arrives later goes into "Pending notes". A slice rerun under
"needs-redo" writes fresh "Approved plan" / "Result" entries suffixed
"(take 2)"; old entries stay as history.

Build slices use all four sections; research slices replace the last two
with the finished document body.

````markdown
# Slice NN — <name>

## Charter

- Goal: <one sentence>
- Product: <an executed plan | a finished document about …>
- Needs first: <other slices or —>

## Pending notes

<everything arriving after the charter was written, one line each: open
questions pushed down from Shape (seeded at creation, marked "(from
Shape)"), findings sent over from other slices. Read all of it when this
slice starts.>

## Approved plan

<3–7 lines, written right after the plan passes its gate: what changes,
proven by what at which boundary, deliberately skipping what. Verification
reads from here, not from memory.>

## Result

<after verify: pass or not, evidence (commands run + key output), the
review gate's outcome when the gate applied (findings / clean / could
not run), divergence from the approved plan>
````

## 6. Research-slice source discipline

- Tier every significant source: official / primary / secondary /
  listing-grade; record the tier in "Sources" when confidence matters.
- A number that carries a conclusion must be checked verbatim against a
  primary source, or confirmed by two independent sources. A number that
  only passed through one summary or one secondary source is an estimate —
  label it as an estimate everywhere it appears.
- Conflicting sources stay visibly in conflict in the document; never
  silently pick a side.
- Keep evidence taken from sources clearly separate from your own
  synthesis.

The "light form" used by Shape's zone research notes: record the source
tier, label estimates — the first two bullets only.

## 7. Quality test

Before leaving the dossier, a fresh agent reading shape.md alone must be
able to answer: which slice is running, what the next action is, and what
has been decided. Additionally: every research-notes subsection from Shape
exists as a file under `docs/research/<topic-slug>/` and is linked from
"Explored zones" or "Sources". Any missing answer means the file is not
done.
