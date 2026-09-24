---
name: gamify
description: >-
  Turn one hard, long-haul pursuit — learning to trade, mastering a keyboard
  layout, any skill that takes months — into a game that a Claude session runs
  as game master and narrator. Build mode first explores the pursuit with the
  user (skill map, player, practice ground, measures, horizon), then offers
  three game concepts drawn from well-built reference games, then builds the
  game in user-approved slices: the hidden game-master plan first, then one
  playable dungeon at a time, then a tool proposal. Play mode leads the player
  through a session. Use when the user names a difficult long-term pursuit and
  wants it made playable, wants to play a game under docs/games/, or wants to
  extend or fix one. Not for short tasks or pursuits with no learnable skill.
argument-hint: "[<pursuit> | play <game-dir> | <game-dir> thêm dungeon: … | <game-dir> sửa: …]"
---

# i:gamify — build the game, then run it

Nothing here changes product code. Everything below is a delta from
your defaults; where nothing is said, your defaults are right.

This skill runs in the main conversation, never a forked context: it asks
the user with `AskUserQuestion`, and a fork has no such tool. Do not add
`context: fork` to the frontmatter. It never loads or reads another skill's
files; what it needs is in its own `references/`.

## Where a game lives

One directory per game, `docs/games/<slug>/`, named with real game
vocabulary because the player is a gamer. Which `docs/games/`: the one in
the current working directory when it exists; otherwise ask once where
the user keeps their games and use that path for the whole run.

| Path | Who opens it | What it is |
|---|---|---|
| `world.md` | player | the one file a player may read: the world, their role, the narrator, how to start |
| `quests.md` | player, written by the narrator | quests currently open |
| `dungeons/NN-<name>.md` | player | one dungeon = one stage with a known deadline and a boss |
| `character.md` | player, written by the narrator | level, unlocked skills, gear |
| `journal.md` | written by the narrator | the log |
| `boss/` | nobody — only the playable page reads it | the sealed fixed-test set, machine-built (`set.json`); the narrator reads the *scores* the page saves, never the set |
| `gamemaster.md` | narrator only | the hidden plan: every quest, dungeon and level tied to a real sub-skill and a measurable sign, the referee rules, and the **vocabulary table** — the one place every name of this game is declared |
| `slate/` | build mode; play mode runs it | the game's machine: data, the scoring engine that turns the rules of `gamemaster.md` into code, and the source of the playable page that the player actually plays in — the page scores instantly, the narrator only reads its results. `slate/` is the skill's fixed directory name; the page's name inside the game is the concept's own |
| `tools.md` | the user as designer | what the machine is made of and how to refresh it, plus whatever is still only proposed |
| `gamemaster/` | build mode only | the design dossier: `plan.md` (state, the five explored axes, the skill map, decisions) and, from stage 3 on, the slice table and slice files |

The player follows `world.md` and the narrator's voice; the narrator opens
the rest when the game says so. Player-facing files are pure game: no
sentence in them names a real-life skill — all of that lives in
`gamemaster.md`.

**A game has a machine.** Whenever the pursuit can be simulated from data
(price history, a text corpus, a puzzle set), the game gets a playable
page that draws the exercise, takes the player's moves as clicks, scores
them at once against machine-computed answers, and shows the kill, the
combo, the miss the moment they happen. The narrator never scores by hand
and the player never copies numbers into chat. A game that is only files
plus a chat is the previous version of this skill, and the user found it
"giống hệt ver trước, chẳng có tí sáng tạo hay tự động gì". Only when
nothing about the pursuit can be computed does the game fall back to
files and reported numbers — then `plan.md` carries the line `Máy: không —
<why>` under "Sân luyện", and `run-check.sh` stops asking for `slate/` and
`boss/`. How
the machine is built — the scoring engine, the page and its result
contract — is in [references/slate.md](references/slate.md).

**Runtime this skill assumes.** `AskUserQuestion` for the approval gates;
the `Artifact` tool to publish the page with the `db` capability, and
`ArtifactData` to read what it saved; `python3` and a browser on the
user's machine for the engine and the page. Without `Artifact`, the page
is a local `slate/index.html` the user opens in a browser and it saves to
localStorage; without `ArtifactData`, results reach the narrator by the
"Sao chép cho người dẫn" button and a pasted JSON (`quan-tro.md`, last
section). Without `AskUserQuestion`, ask the same gate in plain words.

**Frame and vocabulary are two different things.** The frame is what every
game shares: the file names above, the nine sections of `gamemaster.md`,
the shape of the page's shared record, the banned mechanics. The
vocabulary is everything named — the unit of one play session, the page,
the narrator, the fixed test, the place that grants a move, the resource,
every move with its code — and it belongs to one game alone, invented at
the concept stage and declared once in the vocabulary table of
`gamemaster.md` section 7. The references use the first game built with
this skill (a forex game: "the Slate", the narrator Ilo, a "night", the
Guardian, Shrines, Sight and Lure) as their worked example. Those names are
examples, never defaults: a new game never inherits one of them unless its
own concept independently calls for it.

## Dispatch on `$ARGUMENTS`

Read the argument once and take exactly one branch:

1. `play <game-dir>`, where `<game-dir>` is a directory that exists under
   `docs/games/` → **play mode**: read
   [references/quan-tro.md](references/quan-tro.md) and run it as written.
   It reads only that file, the game's `gamemaster.md`, `character.md`,
   `quests.md` and `journal.md`, and the page's shared record through the
   `ArtifactData` tool; it touches `gamemaster/plan.md` only to append a
   note and `slate/data/ids.json` only to look an item up — never this build
   process, the other references, or `boss/`. `play` followed by anything that is not an
   existing game directory — "play piano", "play the guitar" — is a pursuit
   name: branch 4.
2. `<game-dir> thêm dungeon: …` or `<game-dir> sửa: …` → **extend / fix**.
   Read `gamemaster/plan.md` and the "Sửa và mở rộng" section of
   [references/vong-slice.md](references/vong-slice.md) and run it as
   written: a fix is a decision line in `plan.md` first (what, why, the
   user's words as evidence), then the affected slice marked `needs-redo`
   and rerun through the slice gate; a new dungeon is a new skill-map row
   if needed (user approves), a new progression row in `gamemaster.md`, a
   new slice number, then an ordinary dungeon slice. The skill never
   infers what to change from the journal; the user says what they want
   when they call.
3. `<game-dir>` that already holds `gamemaster/plan.md` → **resume build**:
   read that file and continue from its `Việc kế tiếp:` line. Never re-ask
   what it records. A line that says "chờ giai đoạn concept" means stage 2
   starts now; "chờ giai đoạn slice" means stage 3 starts now. If the next
   step names a slice, run that slice.
4. Anything else → first rule out an existing game called by its **own
   name**, which is not its directory name: a game's directory is the
   pursuit ("go-phim-nhanh") while its name is the concept's
   ("Keystage"), so "tiếp tục keystage" must not start a second game.
   Fold the argument to a slug (see "Slug and directory") and look for
   `docs/games/<slug>/gamemaster/plan.md`; if that misses, search every
   `docs/games/*/gamemaster/plan.md` for a `- Tên: <argument>` line
   (the one concept lock writes, case-insensitive). Either hit is branch
   3 — say which directory it resolved to, then resume from that file.
   Only a miss on both is the name of a **new pursuit**: build mode from
   stage 1.

## Build mode

### Stage 1 — tìm hiểu

Read [references/tim-hieu.md](references/tim-hieu.md) and run it as
written. In short: check the three entry conditions; then settle five fixed
axes with the user — the real pursuit as a **skill map** (sub-skills, what
"good" looks like, a measurable sign for each, order, source), the player
(current level, steady minutes per day — never their taste in games), the
consequence-free practice ground, what the referee can actually measure from
what the player reports, and the horizon written once and put away. The
skill map is researched, not guessed: the user's own curriculum first when
one exists, then the web to fill what the curriculum does not say. The map
passes one `AskUserQuestion` approval gate before anything else happens.

The stage ends when the approved map and the other four axes are written
into `docs/games/<slug>/gamemaster/plan.md` with its `Trạng thái:` and
`Việc kế tiếp:` lines. Three to four exchanges is the normal cost; an axis
the user answers fully in one sentence closes at once. Then go straight on
to stage 2 in the same run unless the user stops you.

### Stage 2 — concept

Read [references/concept.md](references/concept.md) and run it as written,
with the frame library [references/thu-vien-khung.md](references/thu-vien-khung.md)
open beside it. Two roads, and the user's picture decides which: when the user has
described a game they want (a mechanic, a story, a feel), take **their**
concept, ask only what is horizon and what is play, and tie it to the map;
when they have not, pick three frames from the library that fit the shape
of the approved skill map and are deliberately unlike each other, and dress
each over the map. The library is a fast start, not a fence: when the user
turns all three down, ask in plain words what missed (world, daily play or
tone) and offer three more from any well-built genre — rhythm, arcade,
farming, racing, whatever fits — still under the same fit test and the
same rules every frame must carry. A rejected round is ordinary
conversation, never counted against the user or the skill. Either way a concept is written for the person
choosing, in two layers: first a short plain part — what playing is, one
day, how you know you are getting better, the catch — then the backstage
(this-is-that table tying game elements to skill-map rows and real moves,
rough progression, honest weaknesses) only once they lean toward it. Run
the fit test (the three real moves must be visible, names sparing and
explained, no banned mechanic); ask "lock or adjust?" in plain text; use
`AskUserQuestion` only for a real choice between discrete branches; adjust
until the user says lock.

The stage ends when `plan.md` holds "Concept đã khoá" with the full
this-is-that table; then go straight on to stage 3 in the same run unless
the user stops you. However many exchanges it takes, the user is finding
their picture — follow them, do not push a library frame back.
After the lock, changing the concept means redoing this stage — say so
once when locking.

### Stage 3 — the slice loop

Read [references/vong-slice.md](references/vong-slice.md) and run it as
written. In short: ask the optional mechanics once (the one
`AskUserQuestion` of this step); write `docs/games/<slug>/gamemaster.md`
from the template there — the hidden plan that ties every game element to
a skill-map row and a measurable sign, the level thresholds, the fixed
test and its tolerances, the session rules with the six known gaps
answered, the progression of every dungeon with a blank row for later
ones, the narrator's rules, the 32-condition checklist; explain it in
plain words in at most fifteen lines and ask "duyệt hay chỉnh?" in words;
adjust until approved; then write the game's slice table into `plan.md`
(game-master plan · data + scoring engine · the playable page · dungeon 1 ·
each further dungeon · tools · final check). Approving the plan is
approving "the plan laid down from the start". The rules in
`gamemaster.md` must be machine-checkable where the game has a machine:
each one names the data it reads and the tolerance it allows.

Then run the slices in order, one `doing` at a time, each through the
approval gate of `vong-slice.md` (plan in plain words, "duyệt hay chỉnh?",
build, check, record in `plan.md`), and stop only when the user stops you
or a slice's check fails twice. Slices 02 and 03 are technical work the
user has nothing to adjust in, so they share one gate: one plan in plain
words (data source, what the page shows, what it saves), one approval,
build both, one check; the table still lists them as two rows:

- **Slice 02 — data + scoring engine.** Follow the "Máy chấm" section of
  [references/slate.md](references/slate.md): real data fetched and cached
  under `slate/`, one pure function per row of the join table in
  `gamemaster.md` with its constants at the top, a fixture test per rule,
  precomputed keys per item, the sealed fixed-test set written to
  `boss/set.json` with exactly the item count section 4 declares, and one
  real item read by eye before the engine is trusted. Skipped only when
  nothing about the pursuit can be computed — then write `Máy: không —
  <why>` in `plan.md` and the dungeons run on files and reported numbers.
- **Slice 03 — the playable page.** Follow "Hợp đồng kết quả" and "Cảm
  giác game" in the same file: a page published as an artifact with the
  `db` capability, moves as clicks, instant scoring by the JS twin of the
  engine (same fixtures, same results), the shared record written exactly
  to the contract with the game's own codes and names, the story shown in
  the three places, enemies visible only after the answer is sealed, sound
  and motion on every hit. Write the page's URL into `gamemaster.md`
  section 7. A page that scores right but feels like the real-life task is
  not done.
- **Slice 04 — dungeon 1**, then one slice per further dungeon. Build the
  player files from [references/khuon-file.md](references/khuon-file.md)
  with the game's vocabulary in every body, the fixed headings only in the
  headings; run `scripts/run-check.sh <game-dir>` until clean; run the
  five-question test of `luat-van-phong.md` section D with a fresh reader;
  for dungeon 1, hand the game to the user for session 1 in play mode and
  record in `plan.md` whether they wanted session 2.

Stage 3 ends when every dungeon slice in the table is `done` or the user
stops; `Việc kế tiếp` then points at slice `tools.md`.

### Stage 4 — `tools.md`

Run the "Slice `tools.md`" section of `vong-slice.md` as written: what the
machine is made of and the exact commands that refresh it, at most three
proposed tools each tied to a skill-map row with its cost, and the user's
pick in plain words — each pick becomes a new numbered slice.

### Stage 5 — final check

Run the "Kiểm cuối" section of `vong-slice.md` as written: six checks with
real evidence, no new writing; all six pass → `plan.md` reads "chơi được —
hoàn tất"; any fail → a decision line and the related slice `needs-redo`.

## Play mode

The playable page runs the session: it points at each button, scores at
once, shows the hit, says its own opening and closing line. The Claude
session is the same narrator *between* sessions, under the game's own names
from the vocabulary table: it reads what the page saved, writes
`journal.md`, `character.md` and `quests.md`, turns the fixed test's scores
into levels by the ladder in `gamemaster.md`, tells the region's opening
event and the story reward, and never repeats what the page already
said. Three sources of truth, kept apart: the rules are `gamemaster.md`,
the results are the page's shared record, the log is the three player
files the narrator writes. The player only talks in chat; they are never
asked to copy numbers. One narrator sentence per turn plus at most one
line of instruction — the whole protocol, including what to do when there
is no shared record, is [references/quan-tro.md](references/quan-tro.md).

## Rules that hold in every mode

- **Pure game on the player's side.** `world.md`, `quests.md`, `dungeons/`,
  `character.md` never say what a quest trains in real life. The
  calculation is real and lives in `gamemaster.md`.
- **Names are English, styled after the frame's source game.** Characters,
  lands, items and moves get English names (or short coined names in Latin
  letters that carry the source game's flavour — *Koto*, *Rathalos*),
  never Vietnamese, never a real person's name.
- **Write for understanding — the core rule.** Proper names are in the
  frame's language, but sparingly: the first time a name appears it comes
  with a half-sentence saying what it is, and plain prose in the user's
  language carries everything else. A paragraph the reader cannot follow
  without holding a handful of new names in their head is wrong, however
  good the names are. This holds for concept descriptions, for every
  player-facing file, and for what the narrator says. The user's own
  words: "tên riêng nên dùng tiếng Anh, nhưng không lạm dụng, phải để
  người dùng hiểu nội dung một cách thông suốt."
- **Banned mechanics, always:** luck in a score; a counted daily streak; a
  leaderboard; money, profit or loss anywhere in scoring or rewards.
- **Every name is this game's own.** The concept stage invents the
  vocabulary; `gamemaster.md` section 7 declares it; the page, the player
  files and the narrator use only that. A name from the references' forex
  example appearing in a non-forex game is a defect, not a convention.
- **Never ask about the player's taste in games to generate concepts.**
  Left to itself, the skill draws concepts from the frame library, not
  from the player's favourites. But a picture the user volunteers — a
  mechanic, a story, a feel — is their decision and wins: that is road 2
  in `references/concept.md`, and there the skill may ask where they want
  the story's inspiration from.
- **Ask, never guess** what the user knows and you do not; **never re-ask**
  what `gamemaster/plan.md` already records.

## Slug and directory

`<slug>` is the pursuit in kebab-case, ASCII-folded, short. Two cases
when `docs/games/<slug>/` already exists: it holds `gamemaster/plan.md` →
that is a game this version built, resume it (dispatch branch 3); it does
not (a game from the previous version of this skill, or an unrelated
directory) → ask once whether to use a different slug or to overwrite.
"Overwrite" never deletes: the existing files move into
`docs/games/<slug>/_v1/` first, so the directory holds only v2 files at
the top level and nothing is lost. Never overwrite silently. Create the directory only after the entry
conditions pass — and create it then, not at the end: `plan.md` with its
two state lines is written as soon as the first exchange closes, so a cut
session resumes instead of re-asking.

## Language

This file is English; the references are Vietnamese; the game's content
follows the user's language. File names inside a game are the fixed English
game terms of the table above, whatever the content language. Tell the user
plain things: the words "trục", "bản đồ kỹ năng", "cổng duyệt" are this
skill's own — say what they mean where they are first used.

## Report

End the run with: the path of `gamemaster/plan.md`; for stage 1, which
axes closed from the user's answers and which needed research, and the
sources of the skill map with their tier (the user's curriculum / a
secondary source / an estimate); for stage 2, which frames were
offered in each round and why, which the user locked and what was adjusted; for stage 3,
which numbers in `gamemaster.md` are estimates to be recalibrated after
the fixed test's first run, what the slice table holds, and for each slice
run this session its check result (engine tests, fixture parity,
`run-check.sh`, the five-question test, the user's session-1 verdict);
for stages 4–5, the user's tool picks and the six check lines. No summary of the map or
the concept itself — the file is the summary.
