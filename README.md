# iflow

Claude Code plugin `i` — seven skills, invoked as `/i:<name>`:

| Skill | Use it for |
|---|---|
| `i:flow` | Shape a large or unsettled undertaking into approved vertical slices, then run them; state lives in `docs/iflow/<topic>-<id>/iflow.md`, and the finished result is copied to `assets/iflow/`. Every task directory ends in a short id, so you can point any skill at a task by it ("nhiệm vụ a7f3"); no skill joins an existing task directory on its own. `/i:flow fast <topic>` skips the discussion and goes straight to the list of parts for your approval. User-invoked only; recommends `/i:lite` when one plan is enough. |
| `i:lite` | Settle one unclear task with you, then build and prove it under a single plan you approve; `/i:lite fast <task>` skips the discussion. For several parts approved one by one, use `i:flow`. User-invoked only. |
| `i:debug` | Reproduce a defect and prove its cause from a fresh context; the fix stays with the caller. |
| `i:test` | Write new tests in the project's own test runner; expected results come from your requirements and docs, and are written down before the code is read. With no scope named it tests what just changed, up to three unrelated surfaces one after another. `/i:test <scope> · only what is missing` lists what has no test yet and writes nothing. |
| `i:explore` | Understand an unfamiliar topic layer by layer before deciding anything. |
| `i:gamify` | Turn a months-long pursuit into a game a Claude session runs. User-invoked only. |
| `i:how` | Learn how this repo's code works or what a recent change did, part by part with the reason behind each part, then answer its questions until you can explain it yourself; draws a page when a picture explains better. Call it by name: `/i:how vừa làm gì vậy?`, `/i:how luồng đăng ký chạy thế nào?`. Reads only. User-invoked only. |

A `SessionStart` hook prints resume pointers for unfinished `i:flow` dossiers in the current project, and stays silent when there are none. A `PostToolUse` hook runs the dossier checker after every `Edit` or `Write` to a `docs/iflow/*/iflow.md` and hands any violation back to Claude; it ignores every other file.

## Keeping the context small

`i:flow` and `i:gamify` keep every fact the next step needs in files, so the conversation before a gate can be thrown away once the gate passes:

- `i:flow`: at the plan-mode approval prompt pick the option that clears the context; every plan it submits reminds you of this. The next step re-reads its SKILL.md and the dossier (`docs/iflow/<topic>-<id>/iflow.md` plus the slice file) and continues. Worth it when the conversation before the gate was long: the Shape discussion, or the slices already built.
- `i:gamify`: between two slices type `/clear`, then `/i:gamify <game> dựng tiếp`; between two play sessions, `/clear` then `/i:gamify <game> chơi tiếp`. Both resume from `gamemaster/plan.md`.

`i:lite` has one plan, and the context before its gate is mostly the code reading its build still needs, so clearing gains nothing there. `i:debug` and `i:test` already start from an empty context (`context: fork`). `i:how` and `i:explore` are dialogues: clearing loses the thread, so leave them alone.

## Behaviour evals

`claude plugin eval` runs the cases under `evals/*/` (each a `prompt.md` plus `graders/`) in a fresh headless session with only this plugin loaded, and grades what the run did. The four cases check behaviour that ends on its own, because a headless run cannot pass an approval gate:

| Case | What must happen |
|---|---|
| `flow-too-light` | `/i:flow` on a one-plan task answers with one line pointing at `/i:lite` and writes nothing. |
| `lite-too-big` | `/i:lite` on a request naming several parts to approve one by one answers with one line pointing at `/i:flow` and writes nothing. |
| `flow-fast-to-gate` | `/i:flow fast` on a fixture repo writes a draft carrying `Shape draft:`, `Repo:` and a slice table, edits no code and creates nothing under `docs/` before the gate. Plan mode is unavailable headless, so the case tells the session its plans directory is `.plans`. |
| `flow-resume-dossier` | `/i:flow nhiệm vụ a7f3` on a fixture dossier reads `iflow.md` and the slice file `Current slice:` points at, asks nothing, and starts no new Shape. |

Run them from the plugin root; `--scaffold` lets the two fixture cases build their repo, `--allow-tools Write` lets the draft be written, `--ablation none` skips the no-plugin baseline these cases do not need:

```
claude plugin eval . --scaffold --allow-tools Write --ablation none --no-publish
```

Each case runs three times by default (`--runs 1` while iterating); one full run is about twelve sessions. Results land in `evals/results/`, which is gitignored. `Bash` is not granted: the OS sandbox it needs is refused on a machine without `socat`, and none of the cases needs it.

## Trigger eval

`scripts/trigger-eval.sh <skill> <eval.json>` measures whether a skill's description makes Claude open it unprompted: every query in the JSON array (`{"query", "should_trigger"}`) runs through `claude -p` three times against this working tree (`--plugin-dir`, installed copy disabled for the session), and a query passes when it fires on at least half the runs exactly if `should_trigger` says so. `evals/<skill>.json` holds each skill's set and `evals/smoke.json` is a three-query set for `debug` (`scripts/trigger-eval.sh debug evals/smoke.json`); add `--out results.json` to keep the numbers. Skills marked `disable-model-invocation: true` (flow, lite, gamify, how) show Claude no description, so the script refuses them; `evals/flow.json` and `evals/gamify.json` stay for the day auto-invocation is turned back on. Cost: queries × runs sessions of `claude -p`; a positive hit on a `context: fork` skill (i:debug, i:test) is cut short as soon as the Skill call is seen, so its fork does no real work.

## Install

```
claude plugin marketplace add kien20011992/iflow
claude plugin install i@iflow
```

Update after a new push: `claude plugin marketplace update iflow && claude plugin update i@iflow`, then restart the session.
