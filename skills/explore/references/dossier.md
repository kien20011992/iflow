# Durable Exploration Dossier

Use the dossier as a self-contained knowledge artifact and as cold-start memory
for a future context. Keep one living dossier per exploration. Integrate and
rewrite it at milestones; do not append a transcript or create a new checkpoint
file for every update.

## Resolve the dossier

Use the first applicable choice:

1. Reuse the dossier path explicitly supplied by the user.
2. Reuse the active dossier already established in the conversation.
3. Search `docs/research/*/explore.md` for an active dossier matching the topic.
   Reuse a single clear match. Ask only when several plausible matches make the
   choice unsafe.
4. At the first milestone, create
   `docs/research/<concise-topic-slug>/explore.md`, beside any research notes
   i:flow keeps on the same topic.

Use a stable, lowercase, hyphenated topic slug. Do not rename the dossier when
the title evolves unless the user requests it or the original path becomes
materially misleading.

## Recognize milestones

Checkpoint when any of these occurs:

- a zone has been explored to a useful conclusion;
- evidence materially reframes the original question;
- the user confirms a constraint, decision, or conclusion that changes the map
  or what the handoff will carry;
- the discussion is about to descend into a substantially different zone;
- the exploration is pausing, handing off, or finishing.

Delivering a layer or adding a zone to the map is not a milestone by itself;
it waits for the next one. Do not checkpoint for greetings, minor
corrections, isolated examples, routine follow-up questions, or small
confirmations. A material correction to the dossier itself is the exception
and is recorded immediately.

Say where the dossier is when it is created and at handoff. Do not announce
routine checkpoints.

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
7. Re-read the result and resolve internal contradictions before treating
   the checkpoint as complete.

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
skill: explore
topic: <current human-readable topic>
primary_domain: <primary domain>
status: active
updated: <YYYY-MM-DD>
---
```

Use only `active` or `ready` for status. Keep `active` until the user confirms
that the dossier is an adequate handoff for the next step; a direct request to
hand off, finish, or mark it ready is that confirmation.

In the handoff response, set `status: ready` and present the unconfirmed
inferences that a conclusion or a downstream step depends on as one compact
batch — the only place several questions share a message. Do not wait for
another reply, do not ask one by one, and do not put the whole ledger to the
user. Whatever the user does not confirm stays flagged, and every conclusion
depending on it stays marked blocked; `ready` with flags and intentionally
open questions is normal. If the user answers the batch later, record the
confirmations and clear the flags. Documents produced downstream must import
these flags, never strip them.

## Required information

The user reads this file first, without the chat; a future agent resumes
from it second. So the body comes first and one compact state block comes
last. Each piece of state lives fully in exactly one section; other sections
may point to it or state its consequence, never reproduce it. Keep these
roles, in this order, with headings adapted to the subject:

### What the user now understands

The body of the document and the first thing after the title. The teaching
and research in the order it was delivered, each part under a heading that
says what it is about: explanations, comparisons, examples, trade-offs,
failure modes, and the uncertainty needed to understand the subject without
the chat. A short clarifying turn that taught something — a term, a
distinction — is recorded too, under the part it belongs to. This is the
exploration's product; never cut it to a quota.

### What changed along the way

Only the questions, disagreements, and discoveries that changed the framing,
the map, or a conclusion — and why. Do not summarize every exchange. This
section is append-mostly: a recorded correction signal is never deleted or
weakened by a later rewrite, because losing it re-instates the original
misreading in every future session.

### Open questions

Unresolved zones, missing evidence, and unconfirmed inferences, each with
what it could change and who owns the answer. Name the single question
currently blocking the most conclusions. This is the working queue and the
fence that keeps an unknown from becoming a fact.

### Sources

An appendix. Link the sources that matter; for each, state what it supports,
the access date when freshness matters, and its tier: official, primary,
secondary, or listing-grade. A number that carries a conclusion must be
verified verbatim against a primary source, or corroborated by two
independent sources; otherwise it is an estimate and is labeled as one here
and wherever it is repeated. Keep known conflicts visible, and distinguish
source evidence from expert synthesis. When nothing was checked, say so in
one line rather than omitting the section.

### State for the next session

The agent's block, last in the file and compact. Three parts:

**Where we are.** Four lines, each a pointer, none a copy: the evolved
question and the expert lens serving it; the decision waiting on the
exploration and whether it is on the table yet; `status` (`active` or
`ready`), the most recently delivered part, and the recommended next descent;
the flags downstream must carry, by reference to the open questions. Do not
list here what was delivered, what may be relied on, or what is still open —
each already lives in its own section.

**Who the user is.** Kept separate from the subject, each item marked
confirmed by the user or inferred by the expert, never silently promoted:
what they intend to do with the understanding and the decision waiting on
it; what they knew coming in, the vocabulary they use, the resolution they
work at; needs — confirmed, still inferred, recommended by the expert with
rationale, rejected or deferred and why; correction signals received and how
the reading of their need changed. A fresh agent that restores only the
subject matter will reproduce whatever mismatch made a correction necessary.

**The map.** The single place a zone's status lives. One table row per zone
that is relevant, explored, or intentionally queued: the decision it feeds,
its status (open, in progress, closed), a one-line verdict pointing to its
part of the body, and the open dependency blocking it, if any. Do not
restate the body here.

## Quality test

Before treating a checkpoint as complete, verify that the user could read
the body cold and act on it, and that a fresh agent could answer all of
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
