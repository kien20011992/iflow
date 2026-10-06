# The dossier — templates and rules

Contents: 1. Principles · 2. Label contract table · 3. Birth checklist ·
4. Template iflow.md · 5. Template slice file and NN identity rules ·
6. Research-slice source discipline.

## 1. Principles

- `iflow.md` is the single source of truth for the whole program's state,
  born the moment the slice table is approved. The dossier is the task's
  directory `docs/iflow/<topic-slug>/`, with `docs/iflow/` at the
  repository's git root (the project directory outside git): `iflow.md`,
  one `NN-<name>.md` per slice, `evidence/NN-<name>/` per slice, and
  `research/`. `<topic-slug>` throughout this skill is that directory's
  name, `<slug>-<id>`: the topic in kebab-case, then four hex characters
  from `openssl rand -hex 2`, so two programs on one topic never collide
  and the user can name a task by its id. A dossier is born in the task
  directory the user names — by id, name or path — else in a new one;
  never in an existing directory picked by guessing that it is the same
  task. Other skills the user points at this task write their own
  subdirectories there (`explore/`, `how/`, `game/`, notes in `research/`)
  and never touch this skill's
  files. The resume hook reads only the `docs/iflow/*/iflow.md` files that
  carry the `<!-- generated-by: iflow/2 -->` marker. The plan
  file (`~/.claude/plans/…`) is a per-session working copy outside the repo
  and may be cleaned up — never point to it as a source of truth.
- `Current slice:` names the slice whose row status is `doing` — starting
  with its two-digit NN — and reads `—` exactly when no row is `doing`. A
  finished program writes `Overall status: done`, `Current slice: —`, and
  a `Next action:` pointing at the summary instead of a step to run. When
  these lines change is SKILL.md's invariant 2.

## 2. Label contract table

These exact strings are the contract the resume hook and the checker read;
write them character for character.

| String (exact) | Where it lives |
|---|---|
| `Overall status:` — values `running` \| `done` | state block, first status line |
| `Current slice:` | state block |
| `Next action:` | state block |
| Slice statuses `todo` \| `doing` \| `done` \| `needs-redo` \| `retired` | last cell of slice-table rows `\| NN \| …`, read only below `Overall status:` |
| `<!-- generated-by: iflow/2 -->` | state block; marks the file as an i:flow dossier |
| `NN-<name>.md` | dossier directory |

## 3. Birth checklist (the moment the slice table is approved)

1. Materialize research notes: every subsection of the draft's research
   notes becomes a file `docs/iflow/<topic-slug>/research/<zone-slug>.md`;
   a name already taken there gets a new one — never overwrite a note
   another run wrote.
2. Create `iflow.md` per §4, distilled from the approved plan and the
   draft, with `Next action:` set to the first slice; what was explored
   LINKS to the research docs (never re-paste their content), and the
   sources list those doc paths. Never copy the plan wholesale. Each
   assumption approved with the table becomes one line in the decisions,
   marked as approved with the table.
3. Create one slice file per slice, opening with its charter.
4. Seed each slice file's notes: every deliberately-left-open item from
   Shape relevant to that slice gets one line saying, in the user's words,
   that it was left open while shaping; a left-open item relevant to no
   slice goes into iflow.md's section on what was explored — nothing may
   drop.
5. Run the checker per SKILL.md's invariant 2, then the quality test: read
   iflow.md alone, as a stranger would; it must say which slice is running,
   what the next action is and what has been decided, and every research
   note must exist as a file linked from iflow.md's body. A missing answer
   means the dossier is not done.
6. Retire the draft: in this session's draft and in any draft it was
   recovered from, the `Shape draft: <topic>` line becomes
   `Shape draft done: <topic>`, the words i:lite uses, so no later draft
   recovery offers a Shape whose program already has a dossier.

## 4. Template `docs/iflow/<topic-slug>/iflow.md`

Reader's part first, state block last — nothing follows it, and progress
lives only there. `<…>` names a section's role, never its heading.

````markdown
# <the program, named in the user's language>

<once done: the closing summary per SKILL.md's Finishing>

## <the picture>

<why this program exists, scope, what "done" looks like, the fate of every
left-open and cut zone>

## <the slices, in run order>

<per slice: plain name, goal as what the user will see, product, link to
its file; then why this order>

## <the decisions>

- <date> — <one line per decision, with the reason when it is expensive to
  rebuild>

## <what was explored>

<a few lines per zone under its plain name: what was seen, the leaning,
what it means for slicing; link research docs in research/; findings
that belong to no slice>

## <sources>

<documents, paths, URLs used — with confidence tier where it matters>

## <state block, for the next session>

<!-- generated-by: iflow/2 -->

> AGENT: continuing from this file? Load the `i:flow` skill first (read
> its SKILL.md wherever it is installed), then follow the Next action
> below. Facts live in this directory, not in conversational memory.

Overall status: running
Current slice: —
Next action: <one runnable imperative sentence>

| # | File | Type | Needs first | Status |
|---|------|------|-------------|--------|

<!-- Overall status: running | done. Type: build | research. Status: todo | doing | done | needs-redo | retired -->
````

## 5. Template slice file and NN identity rules

File name: `NN-<name>.md`. **NN identity rules:** two digits from 01, in run order at
first approval. NN is a permanent identity — rebuilding the table may
retire an old number or append new ones, never reuse or renumber; slice
files keep their names.

The charter — the paragraph under the title — is immutable after
creation; everything that arrives later goes into the notes, the last
section.

````markdown
# <the slice, named in the user's language>

<the charter, one paragraph of short sentences, one idea each: the goal
(research: the question answered), the product — an executed plan | a
finished document about … — and the slices it needs first>

## <approved plan>

<build: written right after the plan passes its gate, as step 2 of
SKILL.md's build cycle says. Verification reads from here, not from
memory; a session resuming mid-slice continues from these steps.>

## <result>

<build: after verify, with the contents step 5 of SKILL.md's build cycle
lists>

<research: the finished document replaces the two sections above>

## <notes>

<everything arriving after the charter was written, one line each: items
left open while shaping (seeded at creation), findings sent over from
other slices. Read all of it when this slice starts.>
````

## 6. Research-slice source discipline

- Tier every significant source: official / primary / secondary /
  listing-grade; record the tier in the sources when confidence matters.
- A number that carries a conclusion must be checked verbatim against a
  primary source, or confirmed by two independent sources. A number that
  only passed through one summary or one secondary source is an estimate —
  label it as an estimate everywhere it appears.
- Conflicting sources stay visibly in conflict in the document; never
  silently pick a side.
- Keep evidence taken from sources clearly separate from your own
  synthesis.
