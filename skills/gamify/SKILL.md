---
name: gamify
description: >-
  Turn one hard, long-haul pursuit — learning to trade, mastering a keyboard
  layout, any skill that takes months — into a game a Claude session runs as
  game master and narrator. Build mode shapes the game with the user in
  approved slices under docs/games/<slug>/; play mode runs one session. Use it
  whenever the user names a skill they want to practise over months and wants
  it to feel like a game, however terse: "học trading theo ICT", "luyện gõ
  phím nhanh, làm thành game đi", "game hoá việc luyện X" — and for "play
  <game-dir>", "chơi tiếp / tiếp tục <game>" (by directory or by the game's
  own name), or fixing or extending one. Not for a short task, a pursuit with
  no learnable skill, a study plan or tutoring without a game (learn),
  building a video game as software (i:flow), or a discussion about why games
  are engaging (i:explore).
argument-hint: "[<pursuit> | play <game-dir> | <game-dir> thêm dungeon: … | <game-dir> sửa: …]"
disable-model-invocation: true
---

# i:gamify — build the game, then run it

Nothing here changes product code. Everything below is a delta from
your defaults; where nothing is said, your defaults are right.

This skill never loads or reads another skill's files; what it needs is in
its own `references/`. The one exception: the
skills the `Artifact` tool itself requires before a page is written
(`artifact-design`, `artifact-capabilities`) are loaded exactly as that
tool says — the page's shared record cannot be written without them.

**After a compaction**, before the next exchange, re-read what the mode
in progress runs on. Build mode: the game's `gamemaster/plan.md` and the
reference of the stage in progress,
as named under Build mode below. Play mode:
[references/quan-tro.md](references/quan-tro.md) and only the game files
it lets play mode read — never `gamemaster/plan.md`. The compaction
summary is a pointer; the facts are in those files.

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
| `boss/` | only the playable page | the sealed fixed-test set (`set.json`); the narrator reads the *scores* the page saves, never the set |
| `gamemaster.md` | narrator only | the hidden plan: every quest, dungeon and level tied to a real sub-skill and a measurable sign, the referee rules, and the **vocabulary table** — the one place every name of this game is declared |
| `slate/` | build mode; play mode runs it | the game's machine: data, the scoring engine built from the rules of `gamemaster.md`, and the source of the playable page — the page scores instantly, the narrator only reads its results; the page's name inside the game is the concept's own |
| `tools.md` | the user as designer | what the machine is made of and how to refresh it, plus whatever is still only proposed |
| `gamemaster/` | build mode; the user reads `plan.md` | `plan.md`: a body for the user (axes, skill map, concept, decisions, one section per built part), then a state block — status, next step, slice table — always last |

The player follows `world.md` and the narrator's voice; the narrator opens
the rest when the game says so.

**A game has a machine.** Whenever the pursuit can be simulated from data
(price history, a text corpus, a puzzle set), the game gets a playable
page that draws the exercise, takes the player's moves as clicks, scores
them at once against machine-computed answers, and shows the kill, the
combo, the miss the moment they happen. The narrator never scores by hand
and the player never copies numbers into chat. Only when nothing about the
pursuit can be computed does the game fall back to files and reported
numbers — then `plan.md`'s state block carries the line `Máy: không —
<why>`, and `run-check.sh` stops asking for `slate/` and `boss/`. How the
machine is built — the scoring engine, the page and its result contract —
is in [references/slate.md](references/slate.md).

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
the shape of the page's shared record, the banned mechanics. The vocabulary
is every name — the page, the narrator, the unit of one session, the fixed
test, every move with its code — invented at the concept stage and declared
once in `gamemaster.md` section 7. The references' worked example is the
first game built with this skill (a forex game: "the Slate", the narrator
Ilo, a "night", the Guardian, Shrines, Sight and Lure); those names are
examples, never defaults — a new game uses one only if its own concept
calls for it.

## Dispatch on `$ARGUMENTS`

Read the argument once and take exactly one branch:

1. `play <game-dir>`, where `<game-dir>` is a directory that exists under
   `docs/games/` → **play mode**: read
   [references/quan-tro.md](references/quan-tro.md) and run it as written;
   it names the only files play mode reads and writes. `play` followed by
   anything that is not an existing game directory — "play piano", "play
   the guitar" — is a pursuit name: branch 4.
2. `<game-dir> thêm dungeon: …` or `<game-dir> sửa: …` → **extend / fix**:
   read `gamemaster/plan.md` and run the "Sửa và mở rộng" section of
   [references/vong-slice.md](references/vong-slice.md) as written.
3. `<game-dir>` that already holds `gamemaster/plan.md` → **resume build**:
   read that file and continue from its `Việc kế tiếp:` line; if it names a
   slice, run that slice.
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
written: three entry conditions, then five fixed axes settled with the
user — the real pursuit as a researched **skill map**, the player, the
consequence-free practice ground, what the referee can measure, and the
horizon. The skill map passes an approval gate before anything else
happens. The stage ends when the approved map and the other four axes are
in `docs/games/<slug>/gamemaster/plan.md`; go straight on to stage 2 in the
same run unless the user stops you.

### Stage 2 — concept

Read [references/concept.md](references/concept.md) and run it as written,
with the frame library [references/thu-vien-khung.md](references/thu-vien-khung.md)
open beside it. The user's picture decides the road: their own concept when
they described one, otherwise three deliberately different frames from the
library. However many exchanges it takes, the user is finding their
picture — follow them, do not push a library frame back.

The stage ends when `plan.md` holds "Concept đã khoá" with the full
this-is-that table; go straight on to stage 3 in the same run unless the
user stops you. After the lock, changing the concept means redoing this
stage — say so once when locking.

### Stage 3 — the slice loop

Read [references/vong-slice.md](references/vong-slice.md) and run it as
written: the optional mechanics, then `gamemaster.md` written from its
template and approved in plain words — approving it is approving "the plan
laid down from the start" — then the slice table in `plan.md`'s state
block. The rules in `gamemaster.md` must be machine-checkable where the
game has a machine: each one names the data it reads and the tolerance it
allows.

Then run the slices in order, one `doing` at a time, each through the
approval gate of `vong-slice.md`, and stop only when the user stops you or
a slice's check fails twice. Slices 02 and 03 are technical work the user
has nothing to adjust in, so they share one gate: one plan in plain words
(data source, what the page shows, what it saves), one approval, build
both, one check; the table still lists them as two rows.

- **Slice 02 — data + scoring engine:** the "Máy chấm" section of
  [references/slate.md](references/slate.md); skipped only when nothing
  about the pursuit can be computed ("A game has a machine" above).
- **Slice 03 — the playable page:** "Hợp đồng kết quả" and "Cảm giác game"
  in the same file; write the page's URL into `gamemaster.md` section 7.
- **Slice 04 — dungeon 1**, then one slice per further dungeon: build the
  player files from [references/khuon-file.md](references/khuon-file.md);
  run `scripts/run-check.sh <game-dir>` until clean; run the five-question
  test of `luat-van-phong.md` section D with a fresh reader; for dungeon 1,
  hand the game to the user for session 1 in play mode and record in
  `plan.md` whether they wanted session 2.

Stage 3 ends when every dungeon slice in the table is `done` or the user
stops; `Việc kế tiếp` then points at slice `tools.md`.

### Stage 4 — `tools.md`

Run the "Slice `tools.md`" section of `vong-slice.md` as written; each
tool the user picks becomes a new numbered slice.

### Stage 5 — final check

Run the "Kiểm cuối" section of `vong-slice.md` as written: all six checks
pass → `plan.md` reads "chơi được — hoàn tất"; any fail → a decision line
and the related slice `needs-redo`.

## Play mode

The playable page runs each session: it points at each button, scores at
once, shows the hit, says its own opening and closing line. The Claude
session is the same narrator *between* sessions, under the game's own
names, and never repeats what the page already said. The whole protocol —
what it reads and writes, how it speaks, what to do when there is no
shared record — is [references/quan-tro.md](references/quan-tro.md).

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
  player-facing file, and for what the narrator says.
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
resume it (dispatch branch 3); it does not (an older or unrelated
directory) → ask once whether to use a different slug or to overwrite.
"Overwrite" never deletes: the existing files move into
`docs/games/<slug>/_v1/` first, so the top level holds only the new game's
files and nothing is lost. Never overwrite silently. Create the directory
only after the entry conditions pass.

## Language

The game's content follows the user's language. File names inside a game are the fixed English
game terms of the table above, whatever the content language. Tell the user
plain things: the words "trục", "bản đồ kỹ năng", "cổng duyệt" are this
skill's own — say what they mean where they are first used. The body of
`plan.md` is the user's: write it by `~/.claude/rules/docs.md`; slice,
trục, cổng duyệt, giai đoạn live only in its state block.

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
