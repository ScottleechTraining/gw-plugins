---
name: gw-ask
model: sonnet
description: "Ask the GW second brain any question. Searches wiki + Voice Corpus, answers with citations to specific pages, flags gaps as stub candidates. Use when Scott asks 'what do I know about X', 'what have I said about X', or 'ask the brain'."
---

# /gw-ask [question]

1. Parse the question into 2-4 search terms plus close synonyms.
2. Grep `Gridiron Warrior/wiki/` (all folders) and `Gridiron Warrior/Voice Corpus/` for matches. Never read External Library unless Scott explicitly says so.
3. Read the top matching pages fully. Follow wikilinks one hop when they answer the question.
4. Answer in under 200 words, in plain language. Every claim cites its page like: (concepts/minimal-effective-dose).
5. End with two lines:
   - SOURCES: the pages used.
   - GAP: if the brain had no good answer, name the missing concept page and offer to create the stub.
