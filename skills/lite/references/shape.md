# Shape — stages 1 and 2

Contents: 0. Working draft and the two run paths · 1. Stage 1 — explore the
picture · 2. Stage 2 — decision session · 3. Stage 3 — one plan ·
4. Decision rights. Every agent this file spawns follows
[agents.md](agents.md).

A stage starts only when the user has locked the previous one by direct
confirmation (section 4), or through a shortcut the user controls: the
`fast` lane in [SKILL.md](../SKILL.md), the opening round's jump (§1), or
the skipped "Lock" (§2's Close).

## 0. Working draft and the two run paths

The plan file is Shape's accumulating draft. Its title names the work in
the user's own words, with no prefix. Its body puts the reader's part
first — the picture draft, from stage 3 the plan itself, after the run its
completion block, and the decisions, each written the moment it settles —
and the working part last: the research notes, then the zone map. The
state block for the next session closes the file, nothing after it: its
own heading, then exactly two lines, `Shape draft: <topic>` and, right
below it, `Repo: <repo path>` — the only lines Draft recovery reads.
`<repo path>` is what `git rev-parse --show-toplevel` prints, or the
working directory outside git. The run's end (SKILL.md, Build and prove)
retires the first line to `Shape draft done: <topic>`, so only interrupted
runs remain candidates.

**Draft recovery** (at the start of a run): run
`grep -A1 '^Shape draft: ' ~/.claude/plans/*.md` — each hit's next line
is that draft's `Repo:`; a `Repo:` anywhere else in a file is prose. Keep
the drafts whose `Repo:` matches this session's `<repo path>`, then only
those whose `Shape draft:` topic is the topic at hand. Exactly one survivor
is the draft; several, or one you are unsure of, is one `AskUserQuestion`
naming each candidate plus "none of these" — recency alone must never pick,
or a same-repo draft on another topic imports its decisions into this one.
No survivor means Shape starts fresh, in silence. If one is chosen: copy
its decisions and research notes into this session's draft; bring its
picture draft, zone map and — when stage 3 had begun — its draft plan
along as starting points, reconciled against the decisions, keeping its
topic; from then on work only in this session's draft. A previous
session's leanings, and every choice in a plan not
approved at this run's gate, are not state — re-confirm each with the user
as it gets used; research notes carry over as-is.

**The two run paths.** When plan mode is not in use — declined or
unavailable — Shape still runs both stages. The only difference is the
working draft: a plan-format file the model writes itself at
`~/.claude/plans/iflow-<session-id>-<topic-slug>.md`, `<session-id>` being
`$CLAUDE_CODE_SESSION_ID`. Everything else in this file, research notes and
zone map included, applies to both paths.

## 1. Stage 1 — explore the picture

Work as two partners: the picture sharpens through two-way discussion, not
through a chain of rounds the model runs by itself; research via subagents
and the web serves the discussion, never substitutes for it.

**An i:explore dossier first.** If one in `docs/research/*/explore.md`
clearly matches the topic (ask when several fit), its confirmed findings
seed the picture draft and whatever it flags as unconfirmed enters as a
leaning to re-confirm, never as a decision.

**Opening round** produces two things: a draft of the picture, however
rough, and the **zone map** — the essential axes the picture cannot stand
on until they settle (programming: architecture, stack, approach, scope;
research: the main strands), one or two lines per zone: what it is, and
what settling it would change in the picture or the plan. The map is born
from an **opening sweep** of the axes: scan the repo, the surrounding
ecosystem, and how others solve this class of problem — inline by default,
or delegate directions to Explore agents; candidate zones come back with a
one-line why, no depth, and are merged into the map with their source
named.

Map hygiene: a zone that feeds neither the picture nor the plan stays off
the map; a zone suspected out-of-scope still goes on, flagged for the user
to confirm the cut; a zone discussion reveals is added to the map out loud.

**Floor control:** which zone opens is the user's call — the model
recommends which to discuss first, with a reason; after presenting one
zone's material, yield the floor. Calling several zones at once is one call
for the whole run: present them one per turn.

**Zone research:** research a zone only when BOTH hold, judged per zone:
(a) its options rest on facts not held with confidence — technology
comparisons, ecosystem state, competing libraries; (b) the agent has a path
to a better source than the caller's recall (web, official docs, primary
files). When only (a) holds, reason inline and label the output as
estimate. When both hold, do the research BEFORE presenting the zone's
material, delegating per angle. Distill the returns into a research note —
a subsection of the draft named after the zone, condensed, closing with a
sources list that records each significant source's tier (official /
primary / secondary / listing-grade). A number that carries a conclusion
but was checked neither verbatim against a primary source nor by two
independent sources is an estimate, labelled so wherever it appears. The
zone's material in conversation is drawn from this note, and the zone's
map entry links to it.

**Self-standing material** — written for someone who has not seen the
context: the options gathered, each opened from its general shape in plain
words, with enough reasoning, a sketch of how it would be done, strengths
and weaknesses, its cost in two parts — building it (mostly the AI's
work) and owning it afterwards (the human's: reading, review,
maintenance) — and the cost of reversal; pre-existing context (repo facts,
earlier decisions, terms of art) introduced in place on first use. Depth
stops at what comparing the options needs — how-to detail belongs to the
deep read in [SKILL.md](../SKILL.md); an example anchored in the problem is
always welcome, an example is not depth. Options must span different
angles — different premises, different solution families, including the
don't-build / defer / reuse-something angle when it is legitimate — at
least one representative option per angle; two options differing only in
detail within one angle are not two choices: a variant is named in one line
inside its angle's entry, dug into only when the user leans into that
angle.

Known hard constraints are part of the material: using them to probe each
option — what it demands, where it snags — is description; adjudicating
waits for the decision session. A reasoned recommendation is not
adjudication: recommend and push back plainly; what is forbidden is bare
options without reasoning that dump the burden of choice on the user.

**Ripeness and early locks:** trade prose until the zone is ripe — the user
pushes back, adds constraints only they know. A ripe zone is not locked on
the spot: its product is understanding plus a reasoned leaning, spoken
aloud into the zone's map entry, waiting for the decision session. Before
the session, only these paths enter the decisions: (1) an explicit user
order; (2) a choice the user raised themselves — discuss it right there,
lock it if they want; (3) a blocking decision — blocking means a NAMED zone
cannot present its material until this one settles (merely swinging a later
recommendation is not blocking); raise it early, ask for the call only
after enough discussion; (4) the stall valve below.

**Position line** ends every exchange: what changed in the picture, the
zones whose state changed this exchange, the zones still open with their
state, and a recommendation for what comes next — steering stays in the
user's hands. Zone states: unopened / in discussion / understood (leaning
recorded) / locked early / delegated / suspected out-of-scope / deferred
to the plan's assumptions / left open / cut. Open means unopened, in discussion, or suspected
out-of-scope and not yet confirmed; the settled zones live on the map, not
in every line. "Understood" is a verdict on the exchange: a zone the user
has not responded to on substance is at most "in discussion".

A small topic whose few zones are already clear may have its opening round
recommend going straight to the decision session — or, when nothing on the
map is worth a decision, straight to the plan: each zone then enters the
plan's assumptions with the leaning taken. The opening round may also
recommend splitting the map: zones that are cheap and reversible are
deferred to the plan's assumptions with their leaning, marked so on the
map, and only the rest are discussed; the recommendation names each
deferred zone with its leaning in one line. The user's own words at
invocation count as direct decisions (early-lock path (1)) and are recorded
as such; the model's reading of them does not. When the recommendation is
the plan, that round also runs stage 2's fresh-eyes pass and lists its
candidates beside it: a kept candidate reopens stage 1 for it; otherwise
the picture rides the plan's gate, one approval for both. The user decides;
only a direct confirmation (section 4) takes any of these jumps.

**Two valves, both measured on the picture draft:** (1) two rounds on the
same zone that could not change a sentence of the draft → stop discussing
and turn it into an `AskUserQuestion` with three branches: deliberately
leave open / change approach / narrow scope. (2) A finding that changes no
sentence of the draft belongs to the plan's innards: save one line in the
draft's research notes and return to the picture.

## 2. Stage 2 — decision session, lock the picture

Propose the session once every zone on the map has a fate: understood,
locked early or delegated, deferred to the plan's assumptions, or about to
be named left open or cut from scope — no zone disappears
silently; cutting a zone is itself a session decision. A deferred zone is
not adjudicated in the session: the user rules on it at the gate. Before
proposing, one fresh-eyes pass asks which axes are missing: hand the
picture draft and the zone map to one subagent to read as a stranger. Its
candidates go to the user alongside the session proposal. A candidate the
user keeps enters the map as a zone (stage 1 reopens for it); a waved-off
one still gets one line on the map, marked cut (waved off).

The session gathers the leanings and only now adjudicates — eliminating,
ranking, weaving them on the concrete problem: ask via `AskUserQuestion` in
batches; the branches are the options already discussed, the recommended
one carrying its context-anchored reason; outcomes go into the decisions.
If the user rejects every branch of a question, reopen that zone under
stage-1 rules, then resume; recorded decisions stand, except any whose
premise the new outcome invalidates — re-ask those.

Close: summarize the picture in one short block and ask two branches:
"Lock" — its description names the fate of every left-open and cut zone —
/ "Explore further" one named zone (default: the zone feeding the heaviest
still-unsteady decision). A free-text answer follows the direct-confirmation
rule in section 4. When no zone is left waiting — every zone's fate came
from a direct answer of the user's, in the session, as an early lock or
when the map was split — skip "Lock": the picture rides the plan's gate,
one approval for both.

## 3. Stage 3 — one plan

After the lock: the deep read and ONE plan through the gate, per
[SKILL.md](../SKILL.md).

## 4. Decision rights

Four rules govern questions and answers; questions have no cap on count.

- **Ask-to-understand — free.** Whatever the user knows and the model is
  assuming, ask instead of guessing.
- **Decision request (select box) — gated.** Allowed only when the user has
  enough to decide: what each branch means, what choosing it costs and
  gains, whether it reverses. Before the decision session, only through the
  four early-lock paths of stage 1.
- **Delegation.** The user may delegate a zone for the model to decide —
  answers like "whichever", "you pick" ARE delegation, never an understood
  zone. The delegation is itself a decision, recorded in the decisions; the
  model decides the zone and announces it in the closing summary block —
  or, when the session is skipped, in the plan's assumptions — and never
  re-asks it.
- **Direct confirmation.** Affirmative words in the user's language ("ok",
  "chốt", "đúng rồi") or an explicit imperative confirm; questions,
  comparisons, hedging language, praise, and silence do not.
