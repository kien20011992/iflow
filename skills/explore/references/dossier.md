# Durable Exploration Dossier

Use the dossier as a self-contained knowledge artifact and as cold-start memory
for a future context. Keep one living dossier per exploration. Integrate and
rewrite it as it changes; do not append a transcript or create a new file for
every update.

## Resolve the dossier

`docs/research/` below is the one at the root of the current git
repository, or in the working directory outside git.

Use the first applicable choice:

1. Reuse the dossier path explicitly supplied by the user.
2. Reuse the active dossier already established in the conversation.
3. Search `docs/research/*/explore.md` for a dossier matching the topic,
   `active` or `ready`; continuing a `ready` one sets it back to `active`.
   Reuse a single clear match. Ask only when several plausible matches make
   the choice unsafe.
4. Otherwise create `docs/research/<concise-topic-slug>/explore.md` with the
   first layer, beside any research notes i:flow keeps on the same topic.

Use a stable, lowercase, hyphenated topic slug. Do not rename the dossier when
the title evolves unless the user asks.

## When to write

Update the dossier in the same turn whenever a layer, a term or distinction
taught in passing, or a confirmation changes what it holds — the
understanding, a zone's status, an open question, a correction. A turn that
changes nothing in it — a greeting, a question you ask, an isolated
example — writes nothing.

## Update as an integrated document

At every update, reconcile the dossier with the conversation and newly
checked sources, and rewrite the affected sections so the whole document
reflects the current understanding: keep useful detail, reasoning,
examples, disagreements, and source context; remove superseded claims or
move them into the evolution section when the change itself matters. Then
re-read the result and resolve internal contradictions.

A conclusion that depends on an unconfirmed assumption must carry that
assumption inline where the conclusion is stated, not only where the
assumption was declared. A reader who takes away only the conclusion must take
away its weakest leg with it.

Attribute an idea to the user or expert only when authorship affects whether
it is confirmed.

## Metadata

Begin with this YAML frontmatter:

```yaml
---
topic: <current human-readable topic>
status: active
updated: <YYYY-MM-DD>
---
```

Use only `active` or `ready` for status. Keep `active` until the user confirms
that the dossier is an adequate handoff for the next step; a direct request to
hand off, finish, or mark it ready is that confirmation.

In the handoff response, set `status: ready` and present the unconfirmed
inferences that a conclusion or a downstream step depends on as one compact
batch. Do not wait for another reply, and do not put the whole ledger to the
user. Whatever the user does not confirm stays flagged, and every conclusion
depending on it stays marked blocked; `ready` with flags and intentionally
open questions is normal. If the user answers the batch later, record the
confirmations and clear the flags.

## Required information

The user reads this file first, without the chat; a future agent resumes
from it second. So the body comes first and one compact state block comes
last. Each piece of state lives fully in exactly one section; other sections
may point to it or state its consequence, never reproduce it. Keep these
roles, in this order, under headings in the user's language that say what
each section holds:

### What the user now understands

The body of the document and the first thing after the title. It opens with
the current conclusions — what may be relied on, each carrying its weakest
leg as the rule above requires. Then comes the teaching and research in the
order it was delivered, each part under a heading that says what it is
about: explanations, comparisons, examples, trade-offs, failure modes, and
the uncertainty needed to understand the subject without the chat. A short
clarifying turn that taught something — a term, a distinction — is recorded
too, under the part it belongs to. This is the exploration's product; never
cut it to a quota.

### What changed along the way

Only the questions, disagreements, and discoveries that changed the framing,
the map, or a conclusion — and why. Leave the section out until something
has changed. This section is append-mostly: a recorded correction signal is
never deleted or weakened by a later rewrite, because losing it re-instates
the original misreading in every future session.

### Open questions

Unresolved zones, missing evidence, and unconfirmed inferences, each with
what it could change and who owns the answer. Put first the question whose
answer would change the most conclusions, and say what it would change.
This is the working queue and the fence that keeps an unknown from becoming
a fact.

### Sources

An appendix. Link the sources that matter; for each, state what it supports,
the access date when freshness matters, and its tier: official, primary,
secondary, or listing-grade. A number that fails SKILL.md's number check is
labeled an estimate here too. Keep known conflicts visible, and distinguish
source evidence from expert synthesis. When nothing was checked, say so in
one line rather than omitting the section.

### State for the next session

The agent's block, last in the file and compact. Three parts, labeled like
the headings above — in the user's language, by what each holds; the bold
names below are roles, not labels:

**Where we are.** Four lines, each a pointer, none a copy: the evolved
question and the expert lens serving it; the aim the exploration serves,
and, when it is a decision, whether it is on the table yet; the most
recently delivered part and the recommended next descent; the flags
downstream must carry, by reference to the open questions.

**Who the user is.** Kept separate from the subject, each item marked
confirmed by the user or inferred by the expert, never silently promoted:
what they intend to do with the understanding and the aim it serves; what
they knew coming in, the vocabulary they use, the resolution they work at;
needs — confirmed, still inferred, recommended by the expert with
rationale, rejected or deferred and why; corrections to how you work, such
as "shorter answers".

**Status of each part of the subject.** The single place a zone's status
lives. One table row per zone that is relevant, explored, or intentionally
queued: the aim it serves, its status (open, in progress, closed), a
one-line verdict pointing to its conclusion in the body, and the open
dependency blocking it, if any.

## Quality test

When the dossier is created and at handoff, verify that the user could read
the body cold and act on it, and that a fresh agent could answer all of
these from the dossier alone:

- What is being explored, and through which expert lens?
- What does the user need this for, and what aim is the exploration
  serving?
- Which layers has the user received, and what can they now decide or
  understand that they could not before?
- What has been confirmed, proposed, corrected, rejected, or left open?
- Which evidence supports the important claims, and at what source tier?
- Which open question would change the most conclusions, and who owns it?
- Where should the next descent resume?

If any answer depends on chat history, strengthen the dossier before moving
on.
