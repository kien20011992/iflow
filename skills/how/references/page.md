# The page, and keeping the lesson

## Where the page goes

When the `Artifact` tool is available, publish the page with it: a private
page on claude.ai, built under that tool's own rules and the skills it
names. Publishing sends the excerpts on the page off this machine: when
the user has said the code is confidential, write a local file instead.

Without the tool: one self-contained HTML file in the session's scratchpad
directory — no network requests, readable in light and dark — and give its
full path.

## What the page must carry

The native rules make it a good page; these make it teach:

- At the top: the target, worded as in chat, and the one- or two-sentence
  answer.
- The picture that earned the page:
  - a flow: one column per actor (the person, the screen, the server, the
    database, an outside service), steps top to bottom in the order they
    happen, each branch labelled with its condition ("sai mật khẩu");
  - a comparison: before and after side by side, the difference marked;
  - a chart: one sentence beside it saying what the numbers mean in
    practice.
- Each step opens to its plain explanation, the real code copied verbatim
  with `file:line`, the reason with its source, and the real output where
  it was run.
- The example from chat, with the same names and values.
- A short glossary of the terms of art the page uses.

One name per thing, the same on the page and in chat. The page asks no
questions: they stay in chat. In chat, give the link or path and at most
two sentences; never retell the page.

## Keeping the lesson

Only when the user asks to keep it. Write `docs/how/<topic-slug>.md` in the
user's language, for a reader who has not seen the chat:

1. What the code does and why: the answer, the parts in the order they
   run, the example, each reason with its source. A flow goes in as a
   Mermaid block, which GitHub and most editors draw.
2. What is still open: points not settled, reasons only inferred, claims
   only read and not run.
3. Sources: commits, files, plans and notes the lesson rests on.

A second lesson on the same topic updates that file rather than starting
another. Say the file's full path when it is written.
