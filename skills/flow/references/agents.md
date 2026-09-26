# Agents — the few rules that matter

Both layers use these when putting an agent to work; read this in the turn
you are about to spawn one.

- Never pass a `name` when calling the Agent tool — with agent teams
  enabled, a named subagent launches as a teammate whose result never
  returns to the caller. To continue a finished agent, use SendMessage
  with its agent ID.
- Delegation exists to protect the main context: heavy reading goes to
  read-only Explore agents, and returns come back condensed, never as raw
  dumps.
- No agent's output may live only in the conversation: the substance of
  every return lands in the file its work fed — a research note, a
  result section, the map. Raw agent output is never pasted into
  user-facing documents. Never instruct an agent to read the i:flow skill
  files.
- At most 3 agents per fan-out, and 0 is the correct number when the
  facts are already in hand. An empty or off-task return gets one retry
  with a tightened prompt; a second failure falls back to the inline
  lane, recorded in one line where the work lands.
