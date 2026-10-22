# Contributing research to ECHO-7

ECHO-7 is intended to be a traceable research database, not a pile of unsourced claims. Contributions should make it easier to investigate an event and understand exactly where each statement came from.

## Add a record

For the shared starter catalogue, edit `data/records.json`. The formal record schema is `data/record.schema.json`.

A record should have:
- A unique, stable `id`.
- A record `kind` (case, timeline, person, program, claim, source, community, document, report, media, or custom).
- A title, summary, year when known, and location when known.
- One or more source objects with the original URL and a descriptive title.
- `provenance`: where this entry came from and who compiled it, if known.
- `evidenceStatus`: what kind of material this is, not an overconfident verdict.

Use `year: 0` when a reliable year is not established. Do not infer a date or exact location from a vague account.

## Source and evidence labels

Prefer sources in roughly this order when they are available and relevant:
1. Original government documents, court or congressional records, logs, declassified files, and original video/audio.
2. Firsthand statements recorded close to the event.
3. Named witnesses' later interviews and testimony.
4. Credible journalism, academic analysis, and independent researchers who identify their sources.
5. Community posts, anonymous claims, and reposted material as leads to investigate.

This is not a rule that official sources are always correct or that community sources are always wrong. It is a reminder to record what kind of evidence supports each statement and how independently it can be checked.

## Keep claims separate from findings

- Write “the witness stated…” when recording testimony.
- Write “the document records…” when a document says something.
- Use “alleged,” “reported,” or “unverified” where appropriate.
- Do not convert a claim of recovered material into a verified recovery without independently traceable evidence.
- Record important alternative explanations and contradictions, not just evidence that supports a favored hypothesis.
- A witness's military, intelligence, scientific, or government background can be relevant context, but does not by itself verify every claim.

## Preserve provenance and attribution

- Link to the original source, not only a search result or aggregator, when possible.
- Keep the source's title and publisher clear; add publication and access dates when known.
- Avoid copying entire articles, books, databases, photographs, or transcripts without permission. Summarize in original wording and link to the source.
- If a source disappears, preserve its title, last-known URL, and a note that it was unavailable; do not present an archived copy as the original.
- Correct errors transparently rather than silently removing relevant context.

## Before merging a contribution

1. Check for duplicates by title, year, location, and witness.
2. Validate every source URL.
3. Make sure the summary distinguishes firsthand observation from interpretation and hearsay.
4. Confirm the source supports the statement attributed to it.
5. Identify what remains unknown and the next concrete research question.

## Current storage limitation

The live site is static GitHub Pages. Editing `data/records.json` changes the shared published catalogue through a repository commit. The website's “Add a research record” form currently saves to the current browser only; it does not create a repository commit or shared backend record. Never add GitHub tokens or private API keys to public browser code. A shared submission form requires an authenticated backend and a moderation workflow.
