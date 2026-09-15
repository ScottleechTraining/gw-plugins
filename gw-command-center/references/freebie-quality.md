# Freebie quality: the idea gate and the routing contract

Canonical home for the rules every freebie producer follows (`/gw-freebie-forge`, `/gw-nightly-forge` 3.5, `/gw-film-study-brief` step 6). Approved by Scott 2026-09-15 (concept-before-build: yes). Do not copy these rules into a command; link here.

Scott's switch: `Gridiron Warrior/Deliverables/_system/freebie-settings.json` (`concept_before_build`, `nightly_concept_cap`, `review_page`). Read it, never write it.

## What counts as a resource worth building

Scott's proven favorites (2026-09-15): In-Season Team Talk Builder, The Radar, Weight Room Clock, Program Audit, Team Speed Audit, Missed Lifts Decision Tree, Hydration Tracker. The pattern behind them, not a topic bias:

1. Immediate use: runs a session, helps a coach act now, or gives an athlete a useful activity.
2. Specific output: a talk, a sequence, a timer, a plan, a sorted grouping, an audit result, a concise reference.
3. Low burden: no new spreadsheet to maintain, no data-entry chore.
4. Repeat use: useful across sessions and seasons, not a one-time download.
5. Scott's coaching identity: his teaching and constraints, not generic template content.
6. Right format: interaction when input, action, timing, practice, or feedback improves the outcome; print when paper is the advantage. A clock or an athlete drill is real interaction without being a decision calculator. A useful checklist may stay a checklist.

## The gate: seven questions, all answered before anything is built

Run this AFTER the existing first filter (F3 `freebie: yes`, or the legacy 18/20). A yes there means evaluate, never build. Answer each in one line, in the concept card:

1. Who specifically needs this, and in what real moment?
2. What task or decision does it help them complete?
3. What does the coach input or do, and what concrete result comes out? For a reference: what will they look up, and when?
4. Why is this better as a reusable resource than a paragraph or a carousel slide?
5. Which existing asset is closest, and what meaningful gap remains? Check, in order: the public Toolbox and the Insiders rack (`websites/scottleechtraining.com/tools/index.html`), member downloads, `Deliverables/_system/review/freebie-known-resources.json` (Scott's delivered list and favorites), the catalog (`python -m scripts.gwqueue.freebie_catalog --preview`: Ideas, Ready, Library, Retired lanes), and killed variants in `freebie-state.json`.
6. Which exact vault source supports the mechanics, thresholds, and advice? (wiki concept page, Voice Corpus file, or dated NotebookLM brief; no number from memory)
7. Can a coach use it without an unreasonable new data-entry chore?

No score outranks a missing answer. A missing source (6), a killed equivalent (5), no practical payoff (2 or 3), or a job an existing tool already does (5) stops the build. A new name, new color, narrower anecdote, or seasonal wrapper is not novelty.

Before proposing anything new, name two relevant positive exemplars from the favorites or the Library and the nearest existing or killed neighbor. Say which useful mechanism is borrowed (the session-runner, the sort, the timer), not which tool is cloned.

## Bounded exploration

Privately compare up to three genuinely different approaches, typically: improve an existing tool, a new interaction or reference, no new asset. Do not force three when the source offers one or none. Recommend at most ONE. Put the rejected alternatives in two lines each under the concept card; never three cards.

Design lenses (prompts, not build orders): rehearsal (try a scenario, see the consequence), translation (turn a real schedule or constraint into a plan or a conversation artifact), observation (record the few things that lead to a decision), installation (help staff carry out one change), reuse (add the missing capability to an existing tool). Never promise injury prediction, invent a validated assessment, or generate unsupported prescriptions to make the interaction impressive. Program Audit is used better, never rebuilt.

## Outcomes, all valid

| Outcome | What you write |
|---|---|
| Propose new resource | Concept card (below). Nothing else overnight. |
| Improve an existing resource | Concept card naming the existing tool and the exact gap. |
| Point to an existing resource | One line in the content pack's receipt naming the tool. No card, no promo filler. |
| Research needed | One line in the receipt naming the missing source. No card. |
| No freebie warranted | One line in the receipt: "no freebie: <reason>". A zero-freebie night is a normal night. |

A killed equivalent is held for Scott's explicit revival even if the new version reads as a correction. Unknown source access means unverified, not "no overlap".

## Concept before build (Scott's yes, 2026-09-15)

- Unattended runs (nightly, any scheduled job) never build a tool. They write a concept card and stop. The card lands in the Ideas lane; Scott picks Build this on the review page; the build happens in a daytime session after that.
- At most `nightly_concept_cap` new concept cards per night (default 3). Unchanged sources and ideas Scott already passed on do not get a fresh card.
- A direct, explicit request from Scott at the terminal to build a named resource supplies concept authorization. It never supplies asset approval or publication.
- Never ask Scott a question during an overnight run. Queue the concept, the missing-source reason, or the no-freebie line and continue.

## Concept card format

Write `<topic folder>/<topic-slug>-freebie.md` (in `_inbox/<slug>/` for nightly picks, in the topic folder for Film Study, at `Deliverables/` root only when there is no topic folder). Frontmatter:

```markdown
---
title: "<resource name>"
topic_slug: <slug>
date: YYYY-MM-DD
stage: idea
format: interactive | pdf | reference
funnel_cta: Insiders | Contact Prep | Scores and Stops | GW 2.0 | GW Inseason | Summit
source: <absolute path of the source brief or pack>
knowledge_sources: [<wiki/voice/brief paths that carry every number>]
nearest_existing: <tool or asset name, or none>
exemplars: [<two favorites or Library items>]
pipeline: gw-freebie-forge
---
```

Body: the seven gate answers, one line each; what the coach puts in and gets out; what is genuinely new or which tool it improves; the borrowed mechanism; rejected alternatives (two lines each); open risks. Voice rules apply (no em-dashes, no banned words). The review page shows this text on the card.

## Routing contract (all producers)

- Interactive builds live at `Deliverables/projects/insiders-vault/incoming/<slug>/index.html`, one self-contained file, Toolbox standard (see `/gw-freebie-forge` Rule 4). `CONTENT.md` stays beside it as the edit and provenance record; it is never a second giveaway.
- The topic folder gets a pointer, `FREEBIE.md`, naming the build path and the resource name (`# Freebie for this pack: <name>`), plus a `## What it does` line. Pointers are never review cards.
- Nothing moves after it is registered. No copying an interactive folder into a topic folder. The catalog keys resources by a stage-independent path, so topic folders may move between `_inbox`, `ready`, and `archived` without losing decisions.
- Every build or concept card ends with the review page rebuild: `cd "C:/Claude Projects/Gridiron Warrior"` then `python -m scripts.gwqueue.build_freebie_review_page`.
- Approval of an idea is permission to build. Approval of an asset is not permission to distribute. Publishing to the Vault, Thinkific, Kit, or the site stays a separate Scott-triggered step.

## Standing laws still apply

The `/gw-freebie-forge` creation rules: dedup gate, format ladder (interactive default, list-shaped exception, no posters), knowledge-backed numbers, freshness test, Toolbox standard, ledger entry. Voice: `C:\Claude Projects\CLAUDE.md`. Content edit: `/gw-freebie-content`. The plan and its reconcile: `docs/superpowers/freebie-review/OPERATIONS.md`.
