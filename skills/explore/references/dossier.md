# Durable Exploration Dossier

Use the dossier as a self-contained knowledge artifact and as cold-start memory
for a future context. Keep one living dossier per exploration. Integrate and
rewrite it at milestones; do not append a transcript or create a new checkpoint
file for every update.

## Resolve the dossier

Use the first applicable choice:

1. Reuse the dossier path explicitly supplied by the user.
2. Reuse the active dossier already established in the conversation.
3. Search `docs/ambient/*/explore.md` for an active dossier matching the topic.
   Reuse a single clear match. Ask only when several plausible matches make the
   choice unsafe.
4. At the first milestone, create
   `docs/ambient/<concise-topic-slug>/explore.md`.

Use a stable, lowercase, hyphenated topic slug. Do not rename the dossier when
the title evolves unless the user requests it or the original path becomes
materially misleading.

## Recognize milestones

Checkpoint when any of these occurs:

- a layer has been delivered and the map beneath it has changed;
- a major zone has been explored to a useful conclusion;
- evidence materially reframes the original question;
- the user confirms an important need, choice, constraint, or conclusion;
- the discussion is about to descend into a substantially different zone;
- the exploration is pausing, handing off, or finishing.

Do not checkpoint for greetings, minor corrections, isolated examples, or
routine follow-up questions. A material correction to the dossier itself is an
exception and must be recorded immediately.

## Update as an integrated document

At every checkpoint:

1. Read the current dossier when it exists.
2. Reconcile it with the conversation and newly checked sources.
3. Rewrite affected sections so the whole document reflects the current
   understanding.
4. Preserve useful detail, reasoning, examples, disagreements, and source
   context. Remove superseded claims or move them into the evolution section
   when the change itself matters.
5. Keep confirmed user needs distinct from expert recommendations and from
   open hypotheses.
6. Record enough continuation state for a new agent to resume without the chat.
7. Re-read the result and resolve internal contradictions before announcing
   the checkpoint.

A conclusion that depends on an unconfirmed assumption must carry that
assumption inline where the conclusion is stated, not only where the
assumption was declared. A reader who takes away only the conclusion must take
away its weakest leg with it.

Do not turn the dossier into a conversation log. Attribute an idea to the user
or expert only when authorship affects whether it is confirmed.

## Metadata

Begin with this YAML frontmatter:

```yaml
---
ambient_step: explore
topic: <current human-readable topic>
primary_domain: <primary domain>
status: active
updated: <YYYY-MM-DD>
---
```

Use only `active` or `ready` for status. Keep `active` until the user confirms
that the dossier is an adequate handoff for the next step.

Before setting `status: ready`, enumerate every user-owned unknown and every
load-bearing inference still unconfirmed, and put each one to the user
individually. Whatever the user does not confirm stays flagged, and every
conclusion depending on it is marked blocked. Documents produced downstream
must import these flags, never strip them.

## Required information

Keep these information roles, adapting headings to the subject when natural:

### Current position

Provide a compact cold-start block near the top:

- current focus and the layer most recently delivered;
- expert lens;
- what the user needs this for and what decision waits on it;
- what has been confirmed;
- working hypotheses or recommendations not yet confirmed;
- the map of zones still open, and which decision each feeds;
- the best next descent point.

### The user and their need

Record what is known about the person, kept separate from what is known about
the subject:

- what they intend to do with the understanding;
- the decision waiting on it, if any;
- what they already knew coming in, and the vocabulary they use;
- the resolution they work at — whole landscape or the detail of one part;
- correction signals received, and how the reading of their need changed.

Mark each item as confirmed by the user or inferred by the expert, and never
silently promote an inference. A fresh agent that restores only the subject
matter will reproduce whatever mismatch made the correction necessary.

### Framed idea or question

State the evolved question and why it is being explored. Preserve important
changes from the original framing.

### Knowledge map

Show the zones and how they relate: which decision each feeds, which have been
descended into, which remain closed and why. Include only zones that are
relevant, explored, or intentionally queued.

### Developed understanding

Write the substantive teaching and research developed so far, organized by the
layers actually delivered. Preserve explanations, comparisons, examples,
trade-offs, failure modes, and uncertainty needed to understand the subject
without the chat.

### Discussion synthesis

Record the questions that materially changed or deepened the exploration and
the resulting understanding. Summarize the reasoning; do not reproduce turns.

### Corrections and evolution

Record discarded misconceptions, overturned assumptions, meaningful
disagreements, and why the understanding changed. Omit trivial wording fixes.

This section is append-mostly: a recorded correction signal is never deleted
or weakened by a later rewrite. Losing it re-instates the original misreading
in every future session.

### Emerging needs

Separate:

- needs explicitly confirmed by the user;
- needs still being inferred or tested;
- expert recommendations and their rationale;
- rejected or deferred directions and why.

Never promote an inference or recommendation into a confirmed need.

### Open frontier

List unresolved zones, missing evidence, and what each could change. Name the
single question currently blocking the most conclusions and who owns the
answer. Identify the recommended next descent when appropriate.

### Sources

Link directly to the important sources. For each source, state what it
supports, record the access date when freshness matters, and tier it:
official, primary, secondary, or listing-grade.

A number that carries a conclusion must be verified verbatim against a primary
source, or corroborated by two independent sources. A figure that has only
passed through a summarizer or a single secondary source is an estimate and
must be labeled as one — in the dossier and wherever it is repeated. Keep
known conflicts or limitations visible, and distinguish source evidence from
expert synthesis.

### Downstream handoff

While active, explain what later steps could already use and what remains too
uncertain. When ready, state the informed needs, conclusions, constraints,
evidence base, and intentionally open questions that the next step receives —
with every unconfirmed flag carried along.

## Quality test

Before announcing a checkpoint, verify that a fresh agent could answer all of
these from the dossier alone:

- What is being explored, and through which expert lens?
- What does the user need this for, and what decision is waiting on it?
- Which layers has the user received, and what can they now decide that they
  could not at the start?
- What has been confirmed, proposed, corrected, rejected, or left open?
- Which evidence supports the important claims, and at what source tier?
- Which single question is blocking the most conclusions, and who owns it?
- Where should the next descent resume?

If any answer depends on chat history, strengthen the dossier before treating
the checkpoint as complete.
