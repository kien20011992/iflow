# iflow

Claude Code plugin `i` — six skills, invoked as `/i:<name>`:

| Skill | Use it for |
|---|---|
| `i:flow` | Shape a large or unsettled undertaking into approved vertical slices, then run them; state lives in `docs/shape/<topic>/shape.md`. User-invoked only; recommends `/i:lite` when one plan is enough. |
| `i:lite` | Shape one unsettled task into a single plan, then build and prove it — no slices, no dossier; `/i:lite fast <task>` skips the shaping. User-invoked only. |
| `i:debug` | Reproduce a defect and prove its cause from a fresh context; the fix stays with the caller. |
| `i:test` | Write new tests at a public boundary, contract locked before the code is read. |
| `i:explore` | Understand an unfamiliar topic layer by layer before deciding anything. |
| `i:gamify` | Turn a months-long pursuit into a game a Claude session runs. User-invoked only. |

A `SessionStart` hook prints resume pointers for unfinished `i:flow` dossiers in the current project, and stays silent when there are none.

## Trigger eval

`scripts/trigger-eval.sh <skill> <eval.json>` measures whether a skill's description makes Claude open it unprompted: every query in the JSON array (`{"query", "should_trigger"}`) runs through `claude -p` three times against this working tree (`--plugin-dir`, installed copy disabled for the session), and a query passes when it fires on at least half the runs exactly if `should_trigger` says so. `evals/<skill>.json` holds each skill's set and `evals/smoke.json` is a three-query set for `flow` (`scripts/trigger-eval.sh flow evals/smoke.json`); add `--out results.json` to keep the numbers. Cost: queries × runs sessions of `claude -p`; a positive hit on a `context: fork` skill (i:debug, i:test) is cut short as soon as the Skill call is seen, so its fork does no real work.

## Install

```
claude plugin marketplace add kien20011992/iflow
claude plugin install i@iflow
```

Update after a new push: `claude plugin marketplace update iflow && claude plugin update i@iflow`, then restart the session.
