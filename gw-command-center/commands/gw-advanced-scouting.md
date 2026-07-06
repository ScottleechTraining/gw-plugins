---
name: gw-advanced-scouting
model: opus
description: "Build an Advanced Scouting deep-dive resource: corpus + NotebookLM research synthesized into a 3-5k word cited reference page at the insiders-resource standard (hamstring-resource / gps-for-football pattern), shipped as an unlisted noindex page under /tools/ for the Insiders community. Research and build only - never deploys, never publishes."
---

# /gw-advanced-scouting [topic] - Insiders Deep-Dive Resource Builder

Scott invokes this when he wants an Advanced Scouting report ("build an advanced
scouting report on contact prep"). The output is a rich, cited, single-topic
reference page like the two originals: /tools/hamstring-resource/ (the template
origin, built 2026-05-28) and /tools/gps-for-football/ (2026-06-06). These live
in the Advanced Scouting section of the Insiders community, shared by unlisted URL.

The formula that makes these pages work: research states the fact, Scott tells
you what to do Monday, and a URI war story proves he lives it.

## Paths

- Page output: `D:\Claude Projects\websites\scottleechtraining.com	ools\<slug>\index.html`
- Design system (REUSE, never fork): `websites\scottleechtraining.com	ools\_shared\gw-tools.css` + `insiders-resource.css` + `insiders-resource.js`
- Template origin to study: `websites\scottleechtraining.com	ools\hamstring-resource\index.html`
- Research audit trail: `D:\Claude Projects\Gridiron Warrior\Deliverables\_corpus-queries\YYYY-MM-DD-<slug>.md`
- Wiki log line: `Gridiron Warrior\wiki\log.md`

## Phase 0 - Dedup gate

List existing deep-dive pages (folders under tools\ whose index.html links
insiders-resource.css). If the topic is already covered, stop and say so.
Check the freebie ledger (`Deliverables\_systemeviewreebie-state.json`)
for killed adjacent assets - killed stays dead unless Scott revives.

## Phase 1 - Research (mine first, write second - never start from a blank page)

1. Run the `/gw-everything-on <topic>` process - it writes the corpus-query
   audit trail (themes + by-source verbatim excerpts) that later gets committed
   alongside the page. This mines wiki, Voice Corpus, External Library metadata,
   screenshots, and daily seeds in one sweep.
2. Query NotebookLM "S&C Master Resource" on the topic (notebook_list ->
   notebook_query). Failure is not fatal - proceed corpus-only and note it.
3. Read the wiki concept pages the corpus query surfaced, plus related
   summaries (film-study, podcast).
4. Mine Voice Corpus for URI war stories on the topic - at least one verbatim
   Scott story MUST anchor the page (this is what makes it his and not a textbook).
5. Quarantine: External Library content contributes ideas and metadata via the
   corpus query only. Never quote external creators as Scott. Peer-reviewed
   sources get cited by name; practitioner sources get chips, kept separate.

## Phase 2 - Synthesis (the skeleton, top to bottom)

insiders-hero (stamp + h1 + one-line scope + Updated date) -> hero-quote
(Scott-voice thesis in one breath) -> read-guide (how to use this page + jump
links) -> tab-row anchor nav (6-10 anchors, uppercase label + small subtitle)
-> gw-card "The 90-Second Teaching" (the whole idea before the depth) ->
numbered h2 sections -> glossary (dl.glossary) -> Deeper Reading (source-list
chips, practitioner) -> References (ref-list, numbered academic w/ PubMed
links) -> "Talk About It Inside" Insiders CTA -> gw-footer ("Keep the Fire
Burning. - Leech" + "for educational use by coaches, not medical advice").

Section archetype menu (pick 6-10 per topic): the-problem, fundamentals/anatomy,
mechanism (two-column grid), evidence (research-card stack, one study per card),
testing/protocols (protocol-detail cards with meta-row), programming (phased
protocol-grid tables), return-to-play/red-flags (rtp-stages + grade-table),
vendor/budget tables, the-AD-pitch (Scott-voice selling the resource-ask),
FAQ/objections (details accordions).

Scale target: 3-5k words, 8-9 academic references, 6-10 anchor sections.

Citation rules: every quantitative claim carries an inline cite-ref chip
[n] anchored to the numbered ref-list, or a named author inline. No naked stats.
Full academic citations: authors, title, journal, year, PubMed link.

Voice rules: plain-language section intros in Scott's register (short sentences,
second person, tough love); one fact-box stat punch per major section; at least
one scott-quote URI war story; signature phrases where natural; NO em-dashes
anywhere; banned-word list from root CLAUDE.md.

## Phase 3 - Build

- New folder `tools\<slug>\index.html`, linking the three _shared assets.
  Use the existing component classes - do not invent new CSS unless a genuinely
  new component is needed (add it to the page, not the shared files).
- `<meta name="robots" content="noindex, nofollow">` - these pages are unlisted,
  shared by URL inside the Insiders community only. No Kit gate, no paywall JS.
- Print-friendly (the shared print rules handle it; add print buttons on
  protocol sections). data-parallax on hero cards.
- Page HTML lands around 35-60KB.

## Phase 4 - Verify (mandatory, look with your own eyes)

Serve via a local http.server on a FRESH port (file:// breaks the /tools/_shared
absolute paths) and playwright (`python`, not python3): desktop + 375px mobile
screenshots, LOOK at them; click 3 tab anchors and confirm scroll targets exist;
confirm every cite-ref [n] resolves to a ref-list id; confirm robots meta;
run scriptsoice_check.py on the extracted page text - must exit 0.
Kill the server when done.

## Phase 5 - Deliver (nothing ships itself)

1. Commit (main repo, no push): the page folder + the corpus-query audit md +
   one wiki log.md line (`YYYY-MM-DD /gw-advanced-scouting: <slug>`).
2. Report to Scott: the future URL (https://scottleechtraining.com/tools/<slug>/),
   a section map, citation count, the war story used, and the reminder that
   DEPLOY IS HIS BUTTON (netlify deploy --prod from the site folder).
3. Offer (do not do unasked): a locked "Insider's Vault" row on tools/index.html
   for public window-shopping, and a note to add the URL to the Advanced
   Scouting section on Thinkific.

## Hard rules

- Never deploy, publish, email, commit to gw-plugins, or touch Kit.
- Never quote External Library creators as Scott (attribution rules apply).
- Every quantitative claim cited. No em-dashes. No banned words.
- One page per topic - if the topic is too broad for 5k words, tell Scott to
  split it rather than shipping a shallow survey.
