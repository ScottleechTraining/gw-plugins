---
name: gw-ask
model: claude-opus-5-5
description: "Ask the GW second brain any question. Searches wiki + Voice Corpus, answers with citations to specific pages, flags gaps as stub candidates. Use when Scott asks 'what do I know about X', 'what have I said about X', or 'ask the brain'."
---

# /gw-ask [question]

1. Parse the question into 2-4 search terms plus close synonyms.
2. Grep `Gridiron Warrior/wiki/` (all folders) and `Gridiron Warrior/Voice Corpus/` for matches. Never read External Library unless Scott explicitly says so.
3. Read the top 5 matching pages fully. Follow wikilinks one hop when they answer the question.
4. Answer in under 200 words, in plain language. Every claim cites its page like: (concepts/minimal-effective-dose).
   - Label every cited passage current Scott practice, historical practice, external evidence, generated synthesis or unresolved. When two current rules disagree, return both and one question, not a choice.
   - A page with `status: draft-pending-scott` is not live yet. Cite it only as generated synthesis, unapproved.
5. End with two lines:
   - SOURCES: the pages used.
   - GAP: if the brain had no good answer, name the missing concept page and offer to create the stub.
6. If the answer is worth keeping, save it as a stub. A stub is a wiki page that goes live only after Scott approves it (ruling R7, 2026-11-18).
   - Write it to the right wiki folder (`concepts/`, `entities/` or `summaries/`). Frontmatter: `title`, `type`, `status: draft-pending-scott`, `origin: gw-ask`, `created: YYYY-MM-DD`. Body: the answer with its citations.
   - Do not add it to `wiki/index.md`. Do not log it. Do not add a line to `open-rulings.md`.
   - Add one last line to the reply: `STUB: wiki/<folder>/<slug>.md goes live when you say approve.`
7. When Scott says approve: set `status: stub`, add the page to `wiki/index.md`, and append a `query` entry to `wiki/log.md`. When he says toss: delete the stub file.

Deliver the answer plus the closing lines. Nothing else: no live wiki pages, no content drafts, no follow-on commands. If the answer needs three sentences, write three.
