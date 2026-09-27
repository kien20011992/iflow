# Shape — the three stages

Contents: 0. Working draft and the two run paths · 1. Stage 1 — explore the
picture · 2. Stage 2 — decision session · 3. Stage 3 — cut slices ·
4. Decision rights. Every agent this file spawns follows
[agents.md](agents.md).

Enter `EnterPlanMode` the moment a new topic starts — even when every
expected slice is research: every i:flow program ends with a product
written into the repo, so the slice table is a genuinely native executable
plan. Its approval gate follows the one rule in SKILL.md's Layer 2. A stage
starts only when the user has locked the previous one.

## 0. Working draft and the two run paths

The plan file is Shape's accumulating draft. Its title names the work in
the user's own words, with no prefix. Its body puts the reader's part
first — the picture draft,
from stage 3 the slice table and run order,
and the decisions, each written the moment it settles — and the working
part last: the research notes (one subsection per researched zone), then
the zone map (each zone with its state and, once one exists, its
leaning). The state block for the next session closes the file, nothing
after it: its own heading in the user's language, then exactly two lines,
`Shape draft: <topic>` and, right below it, `Repo: <repo path>` — the only
lines Draft recovery reads.

**Draft recovery** (when no dossier exists): run
`grep -A1 '^Shape draft: ' ~/.claude/plans/*.md` — each hit's next line
is that draft's `Repo:`; a `Repo:` anywhere else in a file is prose. Keep
the drafts whose `Repo:` matches the current repo, then keep only those
whose `Shape draft:` topic is the topic at hand.
Exactly one survivor is the draft; several, or a survivor you are unsure
of, is one `AskUserQuestion` naming each candidate plus "none of these" —
recency alone must never pick, or a same-repo draft on another topic
imports its decisions into this one. No survivor means Shape starts fresh,
in silence: candidates the topic filter already threw out are not worth a
question — asking whether to recover a draft on another subject wastes the
user's turn.
If one is chosen: copy its decisions and research notes into this
session's draft, and bring its picture draft, zone map and — when stage 3
had begun — its unapproved slice table along as starting points,
reconciled against the decisions.
A previous session's leanings are not state — re-confirm
each with the user as it gets used; research notes are distilled fact —
they carry over as-is, and map links to them keep working. Never keep
working in the old plan file: two parallel drafts drift apart. Recovery is
best-effort — nothing found means Shape restarts fresh, not an error.

**The two run paths.** When plan mode is not in use — declined or
unavailable — Shape still runs all three stages with these substitutions
(everything else in this file applies unchanged to both paths):

| Thing | Plan-mode path | No-plan-mode path |
|---|---|---|
| Working draft | native plan file | `docs/shape/<slug>/shape.md`, born from the first exploration round; its next-action line reads "Continue Shape: …" |
| Research notes | subsections of the draft's research notes | `docs/research/<topic-slug>/<zone-slug>.md` files, written directly |
| Zone map | last in the plan file's body | in shape.md's state block until birth |
| Recovered draft sections | copied into the plan file | materialized straight into the docs files above |

Leanings inside a draft shape.md follow the same re-confirm rule as
recovered drafts.

## 1. Stage 1 — explore the picture

Work as two partners: the picture sharpens through two-way discussion, not
through a chain of rounds the model runs by itself; research via subagents
and the web serves the discussion, never substitutes for it.

**An i:explore dossier first.** Before the opening round, read the
i:explore dossier on this topic in `docs/research/*/explore.md`, if one
clearly matches (ask when several fit). Its confirmed findings seed the
picture draft; whatever it flags as unconfirmed enters the draft as a
leaning to re-confirm, as in Draft recovery — never as a decision.

**Opening round** produces two things: a draft of the picture, however
rough, and the **zone map** — the essential axes the picture cannot stand
on until they settle (programming: architecture, stack, approach, scope;
research: the main strands), one or two lines per zone: what it is, and
what settling it would change in the picture or the slice table. A zone's
code is shorthand for the map, not a name the user knows: everywhere
outside the map itself — the position line above all — write the code with
its short name attached ("Z5 product shape"), and never write a code that
has no entry on the map yet. The map is born from an **opening sweep** of
the axes: scan the repo, the surrounding ecosystem, and how others solve
this class of problem — inline by default; delegate directions to Explore
agents (in parallel, one turn) when they would genuinely see more than
recall does. Candidate zones come back with a one-line why, no depth;
merge them into the map and name where they came from. Sweep results need
no file.

Map hygiene: a zone that feeds neither the picture nor the slice table
stays off the map — pure understanding belongs to i:explore; a zone
suspected out-of-scope still goes on, flagged for the user to confirm the
cut. The map lives in the working draft; when discussion reveals a new
zone, add it to the map out loud.

**Floor control:** which zone opens is the user's call — the model
recommends which to discuss first, with a reason; after presenting one
zone's material, yield the floor. Calling several zones at once is one call
for the whole run: present them one per turn, naming what remains in the
position line.

**Zone research:** research a zone only when BOTH hold: (a) its options
rest on facts not held with confidence — technology comparisons, ecosystem
state, competing libraries; (b) the agent has a path to a better source
than the caller's recall (web, official docs, primary files). Both are
judged per zone — a familiar topic can still contain an unfamiliar zone.
When only (a) holds, reason inline and label the output as estimate. When
both hold, do the research BEFORE presenting the zone's material —
delegating per angle when agents are available. Distill the returns into
a research note (a subsection named after the zone, or its file on the
no-plan-mode path): content in the
user's language, condensed — pasting raw subagent output is banned —
closing with a sources list; a number that carries a conclusion follows the
light form of "Research-slice source discipline" in
[state.md](state.md): record the source tier, label estimates. The zone's
material in conversation is drawn from this note, and the zone's map entry
links to it. At dossier birth the notes become
`docs/research/<topic-slug>/` files — project knowledge that outlives the
Shape; a layer-2 research slice may dig past this option-comparison depth.

**Self-standing material** — written for someone who has not seen the
context: the options gathered, each opened from its general shape in plain
words, with enough reasoning, a sketch of how it would be done, strengths
and weaknesses, its cost split on two scales — build cost on the AI scale,
ownership cost afterwards on the human scale (reading, review,
maintenance) — and the cost of reversal; pre-existing context (repo facts,
earlier decisions, terms of art) introduced in place on first use. Depth
stops at what comparing the options needs — how-to detail belongs to layer
2; an example anchored in the problem is always welcome, an example is not
depth. Options must span different angles — different premises, different
solution families, including the don't-build / defer / reuse-something
angle when it is legitimate — at least one representative option per angle;
two options differing only in detail within one angle are not two choices:
a variant is named in one line inside its angle's entry, dug into only when
the user leans into that angle.

Known hard constraints are part of the material: using them to probe each
option (what it demands, where it snags) is description; adjudicating —
striking options off the menu, weaving options through unsettled zones —
is the decision session's job, and doing it early breeds confusion. A
reasoned recommendation is an opinion, not adjudication: push back
plainly — a reasoned menu is the method of discussion; what is forbidden is
bare options without reasoning that dump the burden of choice on the user.

**Ripeness and early locks:** trade prose until the zone is ripe — the user
pushes back, adds constraints only they know. A ripe zone is not locked on
the spot: its product is understanding plus a reasoned leaning, spoken
aloud into the zone's map entry, waiting for the decision session. Before
the session, only these paths enter the decisions: (1) an explicit user
order; (2) a choice the user raised themselves — discuss it right there,
lock it if they want; (3) a blocking decision — blocking means a NAMED zone
cannot present its material until this one settles (merely swinging a later
recommendation is not blocking); raise it early precisely because it
blocks, ask for the call only after enough discussion; (4) the stall valve
below.

**Position line** ends every exchange: what changed in the picture, the
zones whose state changed this exchange, the zones still open with their
state, and a recommendation for what comes next — steering stays in the
user's hands. Zone states: unopened / in discussion /
understood-leaning-recorded / locked early / suspected out-of-scope. Open
means unopened, in discussion, or suspected out-of-scope and not yet
confirmed; the settled zones live on the map, not in every line.
"Understood" is a verdict on the
exchange: a zone the user has not responded to on substance is at most "in
discussion". A small topic whose few zones are already clear may have its
opening round recommend going straight to the decision session.

**Two valves, both measured on the picture draft:** (1) a round that could
not change at least one sentence of the draft did not budge; two such
rounds on the same zone → stop discussing, turn it into a decision via
`AskUserQuestion` with three branches: deliberately leave open / change
approach / narrow scope. (2) a finding that changes no sentence of the
draft belongs to a future slice's innards: save one line, return to the
picture — that depth belongs to layer 2.

## 2. Stage 2 — decision session, lock the picture

Propose the session once every zone on the map has a fate: understood or
locked early, or about to be named deliberately-left-open or cut from
scope — no zone disappears silently; cutting a zone is itself a session
decision. That fate check audits the listed zones, not the list itself — so
before proposing, one fresh-eyes pass asks which axes are missing: hand
the picture draft and the zone map to one subagent when one is available,
otherwise take the pass yourself, deliberately re-reading both as a
stranger would. Its candidates go to the user alongside the session
proposal. A candidate the user keeps enters the map as a zone (stage 1
reopens for it); a waved-off one still gets one line on the map, marked
waved-off.

The session gathers the leanings and only now adjudicates — eliminating,
ranking, weaving them on the concrete problem: ask via `AskUserQuestion` in
batches (at most four questions per call); the branches are the options
already discussed, the recommended option first with its context-anchored
reason; outcomes go into the decisions. If the user rejects a recommendation
mid-session, reopen that zone under stage-1 rules, then resume; recorded
decisions stand, except any whose premise the new outcome invalidates —
re-ask those.

Close: summarize the picture in one short block and ask two branches:
"Lock" — its description names the fate of every left-open and cut zone —
/ "Explore further" one named zone (default: the zone feeding the heaviest
still-unsteady decision). A free-text answer follows the direct-confirmation
rule in section 4. When the session left no zone waiting — every one of them
got its fate from a direct answer of the user's, right there — that "Lock"
branch is a gate asking what was just answered: skip it and carry the
picture into the slice table's own gate in stage 3, one approval for both.
Any zone still waiting keeps the two gates apart.

## 3. Stage 3 — cut slices from the locked picture

For research programs, slices are the topic's deep pieces; for programming,
successive increments of one working thing — never the layers of a
structure. Table columns: # / slice / goal / type (build or research) /
product / needs-first / status.

Four tests before presenting: (1) deletion test — remove a technical
detail from the slice description; if the locked goal still reads the same,
it was how-to (cut it — it belongs to a layer-2 plan); if the slice no
longer describes what was locked, it was scope (keep it). (2) no slice may
have "discover itself" as its goal — a research slice is valid once its
question has taken shape. (3) every dependency names a real slice and the
graph has no cycles. (4) value test — every build slice names an outcome
observable from outside its own code: something the user sees, or a system
behaviour you can command. One that cannot is an enabler: say so in plain
words in its goal cell — groundwork the user will not see by itself —
never in the status cell, whose values are a label contract; give the
reason it cannot ride inside a vertical increment in the slice file's
charter, not in the table cell — a reason needs a sentence, and a table
cell cannot hold one.

Submit the plan — the locked picture + the slice table + the run order —
through the approval gate defined in SKILL.md's Layer 2. Right after the
gate passes: birth checklist in [state.md](state.md), then the slice loop
in the same turn.

## 4. Decision rights

Questions run in two registers, with no cap on count:

- **Ask-to-understand — free.** Whatever the user knows and the model is
  assuming, ask instead of guessing. Inviting the user to call a direction
  in the position line is also free: picking a direction is cheap and
  reversible, not a decision request.
- **Decision request (select box) — gated.** Allowed only when the user has
  enough to decide: what each branch means, what choosing it costs and
  gains, whether it reverses. By default it waits for the decision session;
  mid-way it follows exactly the four early-lock paths of stage 1. Ground
  not yet laid means keep discussing instead of asking.
- **Delegation.** The user may delegate a zone for the model to decide —
  answers like "whichever", "you pick" ARE delegation, never an understood
  zone. The delegation is itself a decision, recorded in the decisions; a
  delegated zone is decided by the model at the decision session, announced
  in the closing summary block, never re-asked.
- **Direct confirmation.** Affirmative words in the user's language ("ok",
  "chốt", "đúng rồi") or an explicit imperative confirm; questions,
  comparisons, hedging language, praise, and silence do not.

**Agents.** Any delegation in this file follows the short rules in
[agents.md](agents.md).
