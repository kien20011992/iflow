# iflow

Claude Code plugin `i` — five skills, invoked as `/i:<name>`:

| Skill | Use it for |
|---|---|
| `i:flow` | Shape a large or unsettled undertaking into approved vertical slices, then run them; state lives in `docs/shape/<topic>/shape.md`. |
| `i:debug` | Reproduce a defect and prove its cause from a fresh context; the fix stays with the caller. |
| `i:test` | Write new tests at a public boundary, contract locked before the code is read. |
| `i:explore` | Understand an unfamiliar topic layer by layer before deciding anything. |
| `i:gamify` | Turn a months-long pursuit into a game a Claude session runs. |

A `SessionStart` hook prints resume pointers for unfinished `i:flow` dossiers in the current project, and stays silent when there are none.

## Install

```
claude plugin marketplace add kien20011992/iflow
claude plugin install i@iflow
```

Update after a new push: `claude plugin marketplace update iflow && claude plugin update i@iflow`, then restart the session.
