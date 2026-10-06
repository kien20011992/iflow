# iflow

Claude Code plugin `i` — seven skills, invoked as `/i:<name>`:

| Skill | Use it for |
|---|---|
| `i:flow` | Shape a large or unsettled undertaking into approved vertical slices, then run them; state lives in `docs/iflow/<topic>-<id>/iflow.md`, and the finished result is copied to `assets/iflow/`. Every task directory ends in a short id, so you can point any skill at a task by it ("nhiệm vụ a7f3"); no skill joins an existing task directory on its own. `/i:flow fast <topic>` skips the discussion and goes straight to the list of parts for your approval. User-invoked only; recommends `/i:lite` when one plan is enough. |
| `i:lite` | Settle one unclear task with you, then build and prove it under a single plan you approve; `/i:lite fast <task>` skips the discussion. For several parts approved one by one, use `i:flow`. User-invoked only. |
| `i:debug` | Reproduce a defect and prove its cause from a fresh context; the fix stays with the caller. |
| `i:test` | Write new tests in the project's own test runner; expected results come from your requirements and docs, and are written down before the code is read. `/i:test <scope> · only what is missing` lists what has no test yet and writes nothing. |
| `i:explore` | Understand an unfamiliar topic layer by layer before deciding anything. |
| `i:gamify` | Turn a months-long pursuit into a game a Claude session runs. User-invoked only. |
| `i:how` | Learn how this repo's code works or what a recent change did, part by part with the reason behind each part, then answer its questions until you can explain it yourself; draws a page when a picture explains better. Call it by name: `/i:how vừa làm gì vậy?`, `/i:how luồng đăng ký chạy thế nào?`. Reads only. User-invoked only. |

A `SessionStart` hook prints resume pointers for unfinished `i:flow` dossiers in the current project, and stays silent when there are none.

## Trigger eval

`scripts/trigger-eval.sh <skill> <eval.json>` measures whether a skill's description makes Claude open it unprompted: every query in the JSON array (`{"query", "should_trigger"}`) runs through `claude -p` three times against this working tree (`--plugin-dir`, installed copy disabled for the session), and a query passes when it fires on at least half the runs exactly if `should_trigger` says so. `evals/<skill>.json` holds each skill's set and `evals/smoke.json` is a three-query set for `debug` (`scripts/trigger-eval.sh debug evals/smoke.json`); add `--out results.json` to keep the numbers. Skills marked `disable-model-invocation: true` (flow, lite, gamify, how) show Claude no description, so the script refuses them; `evals/flow.json` and `evals/gamify.json` stay for the day auto-invocation is turned back on. Cost: queries × runs sessions of `claude -p`; a positive hit on a `context: fork` skill (i:debug, i:test) is cut short as soon as the Skill call is seen, so its fork does no real work.

## Install

```
claude plugin marketplace add kien20011992/iflow
claude plugin install i@iflow
```

Update after a new push: `claude plugin marketplace update iflow && claude plugin update i@iflow`, then restart the session.
