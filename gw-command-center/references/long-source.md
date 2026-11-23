# Long-source rule: the one rule every whole-source read follows

Created 2026-11-23 (Scott ruling R42: "Yes, add it"). Content Forge TRANSCRIPT MODE and `/gw-film-study-brief` read this file. When the rule changes, change it here, then bump the plugin version. Nothing else in the plugin should restate it.

Why: a model uses the start and the end of a long input best and the middle worst. Instructions placed above a long source get recalled worse. Copying the passages out first, then writing from them, cut errors on long documents. Evidence: `Gridiron Warrior/External Library/AI/2026-11-21-context-windows-long-documents-brief.md`.

## When it applies

Any source long enough that the task would otherwise sit above it: a podcast, Film Study, or Press Box transcript, a corpus-query file, any source read end to end to write from. It does not apply to a short note or a bounded daily delta.

## The rule

1. **Transcript first.** Read the whole source before you start the task. Do not skim the middle.
2. **Task last.** When you hand the source to a sub-agent, put the source first, inside `<document>` tags, and the instructions and question after it.
3. **Pull quotes before drafting.** Copy every passage you will use, word for word, into a quotes list. Include every number with its context. Then write only from that list.
