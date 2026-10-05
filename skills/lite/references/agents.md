# Agents — the few rules that matter

- Never pass a `name` when calling the Agent tool: with agent teams
  enabled, a named subagent becomes a teammate instead of returning a
  result.
- No agent's output may live only in the conversation: the substance of
  every return lands in the file its work fed — a research note, the zone
  map, the plan. Raw agent output is never pasted into user-facing
  documents. Never instruct an agent to read the i:lite skill files.
- At most 3 agents per fan-out, and 0 is the correct number when the
  facts are already in hand. An empty or off-task return gets one retry
  with a tightened prompt; a second failure falls back to the inline
  lane, recorded in one line where the work lands.
