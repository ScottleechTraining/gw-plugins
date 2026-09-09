# Visual Teaching (roadmap idea 4)

Installed in plugin 0.25.0 (2026-09-09). Editorial and layout reference for opted-in decks: Forge chooses a visual body slide only when a source-supported relationship (comparison, sequence, annotated example) teaches the decision more clearly than prose, and the builder translates the layout into the selected style pack. No new style pack, archetype, role, or schema field. Style-only rebuilds preserve both the saved text and the diagram's meaning; legacy decks are never retrofitted. The Codex proof renders (Oswald, document palette) live outside the plugin and are not production decks.

## A Visual Must Do a Job

Use a diagram when position, connection, sequence, or annotation makes the coaching decision easier to understand than a paragraph. Putting prose in rectangles is not automatically visual teaching. If removing the shapes loses no useful information, use simpler typography instead.

This module does not create a style pack or change the canonical archetypes. Choose the primary action and teaching structure first; choose a visual representation only when it clarifies that teaching. One important visual usually beats several competing diagrams on a slide.

## Selection Rules

| Question the reader needs answered | Format | Evidence required | Example delivered |
|---|---|---|---|
| What changes, and what stays the same? | Before/after comparison | Supported alternatives, one declared comparison dimension | Same three coaches; separate views versus shared reporting |
| What needs to happen before the next step? | Timeline or sequence | Supported order; actual durations only if measured or sourced | Four events before a proposed addition is discussed |
| What should I notice or enter here? | Annotated example | A real authorized artifact or clearly labeled illustration | Proposed-work report with four numbered fields |

Before drafting, finish: 'The reader will see [relationship] and use it to [decision].' Put the purpose and source reason in existing brief fields: append `visual: <comparison|sequence|annotated>; <relationship and decision>` to `brief.reason` after the approach clause, and let payoff name what the reader sees. Do not invent a new data schema merely to record a format preference. When no relationship earns a diagram, write nothing and use prose.

### Comparisons

Keep the same actors, units, scale, and context on both sides. Change one dimension. Label both conditions clearly. Do not depict a real before/after outcome unless it is supported; an illustrative comparison is not an observed improvement. In the supplied example, lines encode information flow, not work quantity or authority.

### Timelines

Use a proportional axis only when there are meaningful sourced durations. Otherwise label it as an event sequence and avoid hour marks, unequal bars, or spacing that implies measured time. Name the action at each step. Connectors show order, not proof of causality. The example is an editorial ordering of the source's practices, not a timestamped account of Scott's day.

For a training-session or weekly-program timeline, retrieve the actual session/week source first. Do not invent dose, recovery windows, safe workload thresholds, or calendar placements just to fill the graphic. When source detail is missing, use a conceptual sequence or choose another format.

### Annotated Examples

Use 3-4 callouts, each linked to one identifiable item. A callout should explain what to notice or do, not repeat the label. Keep the underlying object legible. Label invented rows visibly as illustrative and never use real private athlete data without authorization.

Keep commentary separate from original entries. In the supplied example, eight minutes is fictional report data, not a suggested addition. 'Roster overlap' combines the source's shared-sheet practice with its named JV/varsity check; the table is a new explanatory layout, not a screenshot of Scott's actual report.

## Production Layout Rules

- Render at the existing 1080x1350 output dimensions. Keep content inside the selected pack's established safe area and persistent frame.
- Check at an actual phone-sized display, not just at 1080 pixels. Narrow the teaching if labels become tiny. Do not solve overcrowding by endlessly shrinking text.
- The proofs use GW document tokens and locally embedded Oswald fonts. They are not a new registered carousel pack. Translate the layout into the currently selected pack during production.
- Preserve the pack's photo requirements across the whole deck. These isolated body-slide proofs have no cover or photo sequence and must not be mistaken for finished compliant carousels.
- Use position, labels, numbering, or line style in addition to color. If a connection or distinction disappears without color, add a semantic cue.
- Lines, arrows, and highlights must identify a specific relationship. Remove decorative chart elements that could be mistaken for measured data.
- Keep explanatory charts self-contained enough to screenshot, but do not stuff every caveat from the source onto one slide. Narrow the claim until its essential context fits.

## Saved-Copy Compatibility

All visible teaching text must remain editable HTML bound to the existing master record in production. Each label, entry, annotation, and takeaway uses an ordinary string field on the existing body slide. Do not flatten the entire diagram into an image and lose the text-edit workflow.

Repeated visible labels need separate unique field bindings, even when their strings happen to match. Never attach the same data-gw-copy key to two DOM nodes. Keep each binding inside its correct data-gw-slide. Do not add a new slide role or bypass the current assembler.

Represent the essential relationship in saved text as well as geometry: condition labels, step order, units, and a plain-language takeaway. A line or color alone is not a sufficient permanent record of the teaching.

For style-only rebuilds, preserve both exact saved text and the diagram's meaning. Export from saved HTML, not an older Markdown pack. Compare actors, links, ordering, units, and callout targets before replacing the old deck. If a new style cannot preserve a relationship clearly, retain the existing diagram arrangement within the new style or flag the restyle; do not silently simplify away the teaching.

An explicit action rewrite may change the diagram's job, body, and CTA together, but retains the existing identity and requires renewed review. All copy/renderer/approval checks still apply.

## Preflight

1. Source supports the relationship shown; illustrations and measured data are distinguished.
2. No unsupported outcome, dose, scale, or personal story is introduced.
3. Every label is legible at phone size and contained in its area.
4. Arrows/connectors land on the intended objects; sequence direction is unambiguous.
5. No decorative shape is mistaken for data; visual meaning survives without color.
6. Takeaway, brief action, and final deck CTA/caption agree.
7. Editable labels survive save/reopen and style-only restyle without semantic drift.
8. Existing voice, novelty, photo-floor, selected-variant, and token-bound approval gates pass.

The prototype checks cover rendering and framing, not full production saved-copy integration. That integration must be tested after Claude ports a layout into a managed deck.

---

## Appendix A: source and adaptation boundaries of the Codex proofs

Read on 2026-09-09:

- C:/Claude Projects/Gridiron Warrior/wiki/concepts/weekly-load-ownership.md
- C:/Claude Projects/GW-DESIGN.md
- C:/Claude Projects/plugins/gw-command-center/skills/ig-carousel/references/style-packs.md

Local embedded font files: C:/Claude Projects/Gridiron Warrior/Deliverables/projects/summit-2026-brochure/fonts/osw400.woff2, osw600.woff2, osw700.woff2. Existing local assets reused; no external downloads.

### Comparison

Source support: different staff members add work while seeing only their pieces; a named reporting owner and a shared sheet bring the week together. The source explicitly distinguishes information ownership from veto power.

Adaptation: the two-state diagram and connector layout are newly authored. 'Before' and 'after' mean alternative information structures, not a measured case study or proof that an intervention improved performance. The source does not assign the ownership role to a new person in this fictional diagram.

### Event Timeline

Source support: name an owner, write additions before they happen, identify athletes on overlapping JV/varsity rosters, and discuss the overall week in the staff room.

Adaptation: the four-step sequence is an editorial organization of those practices. It does not claim Scott performs four discrete steps at exact times. Equal spacing represents sequence only, not equal duration. No rules, contact-time limits, or workload thresholds are asserted.

### Annotated Report

Source support: record added work, duration, affected group, and check cross-roster athletes by name.

Adaptation: the table is newly authored, not a screenshot of an actual report. Extended Indy / 8 minutes / varsity receivers is invented sample data, visibly labeled illustrative and not a work prescription. No athlete names or private records are present. Callout wording is draft explanatory copy, not a verbatim Scott quote.

### Design Boundary

These prototypes use the GW document palette and Oswald typography. They demonstrate body-slide teaching geometry, not complete compliance with one of the registered carousel packs. Production must preserve its selected pack and whole-deck photo requirements. No new palette or font rule is being installed.

---

## Appendix B: layout geometry of the three proofs

Body-slide geometry only, as authored by Codex at 1080x1350 with a 64px side margin. Translate the geometry into the selected pack's tokens, fonts, safe area, and footer; do not ship these colors or Oswald. Every visible string becomes its own bound field in production (`data-gw-copy`), including repeated labels, and invented rows keep a visible illustrative label.

```css
.mast{height:46px;display:flex;justify-content:space-between;align-items:center;border-bottom:3px solid var(--ink);padding-bottom:13px;font-size:27px;font-weight:600}.mast b{font-weight:700}.mast span{font-size:26px}
h1{font-size:86px;line-height:1.08;font-weight:700;margin:36px 0 30px;max-width:930px}h1 span{display:block}.lead{font-size:43px;line-height:1.28;margin:0 0 30px}.label{font:600 29px Oswald,sans-serif;margin:0 0 12px;text-transform:uppercase}.bodytext{font-size:44px;line-height:1.28;margin:0}.takeaway{border-top:4px solid var(--ink);padding-top:20px;font-size:45px;line-height:1.25;margin-top:30px;font-weight:600}
footer{position:absolute;bottom:45px;left:64px;right:64px;display:flex;justify-content:space-between;border-top:2px solid var(--line);padding-top:14px;font-size:26px}
.comparison{display:grid;gap:24px}.case{padding:23px 26px;background:white;border-left:8px solid var(--maroon)}.case.after{border-color:var(--ink);background:#e0e7ea}.role-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:16px}.role{font-size:41px;line-height:1.12;text-align:center;border:2px solid var(--ink);padding:15px 4px;background:var(--paper)}.separate{font-size:35px;text-align:center;line-height:1.15;padding-top:13px}.junction{height:36px;position:relative;margin:0 15%;border-bottom:3px solid var(--ink);border-left:3px solid var(--ink);border-right:3px solid var(--ink)}.junction:before{content:'';position:absolute;left:50%;top:0;height:55px;border-left:3px solid var(--ink)}.shared{margin:18px auto 0;background:var(--ink);color:var(--paper);font-size:40px;line-height:1.1;text-align:center;padding:14px 10px;position:relative}
.time-layout{margin-top:38px;position:relative;padding-left:88px}.time-layout:before{content:'';position:absolute;left:28px;top:28px;bottom:42px;width:4px;background:var(--ink)}.event{position:relative;margin-bottom:28px;padding:0 0 26px;border-bottom:2px solid var(--line)}.event:last-child{margin-bottom:0;border-bottom:0;padding-bottom:0}.event .num{position:absolute;left:-88px;top:0;width:60px;height:60px;background:var(--ink);color:var(--paper);display:flex;align-items:center;justify-content:center;font-size:36px;font-weight:600}.event h2{font-size:49px;line-height:1.08;margin:0 0 9px;font-weight:600}.event p{font-size:40px;line-height:1.22;margin:0}.event.final .num{background:var(--maroon)}.event.final h2{color:var(--maroon)}
.illustration{display:inline-block;margin:0 0 24px;padding:8px 15px;background:var(--ink);color:var(--paper);font-size:34px;font-weight:600}.report{width:100%;border-collapse:collapse;font-size:44px;line-height:1.2;background:white;border:3px solid var(--ink)}.report th,.report td{padding:17px 22px;text-align:left;border-bottom:2px solid var(--line);vertical-align:middle}.report th{width:42%;font-weight:600;background:#e0e7ea}.report td{font-weight:400}.mark{display:inline-flex;width:43px;height:43px;margin-right:13px;background:var(--maroon);color:white;font-size:28px;align-items:center;justify-content:center;vertical-align:middle}.annotations{display:grid;grid-template-columns:1fr 1fr;gap:23px 32px;margin-top:30px}.annotation{font-size:40px;line-height:1.2}.annotation strong{display:block;font-weight:600;font-size:42px;margin-bottom:4px}.annotation strong:before{content:attr(data-number) ' / ';color:var(--maroon)}
```

### Comparison (two states, one declared dimension)

```html
<article class="slide" aria-label="Before and after information flow">
<h1><span>Same staff.</span><span>A shared picture.</span></h1>
<div class="comparison">
<section class="case"><p class="label">Before / separate information</p><div class="role-grid"><div class="role">Position<br>coach</div><div class="role">Head<br>coach</div><div class="role">Strength<br>coach</div></div><div class="role-grid"><div class="separate">Own view</div><div class="separate">Own view</div><div class="separate">Own view</div></div></section>
<section class="case after"><p class="label">After / one reporting owner</p><div class="role-grid"><div class="role">Position<br>coach</div><div class="role">Head<br>coach</div><div class="role">Strength<br>coach</div></div><div class="junction" aria-hidden="true"></div><div class="shared">One person gathers the whole week</div></section>
</div>
<p class="takeaway">Change who gathers the information.<br>Not who owns every decision.</p>
<footer><span>Weekly load ownership</span><span>Information flow, not training load</span></footer>
</article>
```

### Event sequence (order only, no time scale)

```html
<article class="slide" aria-label="Event sequence before adding work">
<h1><span>Before the work</span><span>gets added.</span></h1>
<p class="lead">Get the whole picture into the decision.</p>
<div class="time-layout">
<section class="event"><span class="num">1</span><h2>Name the reporting owner</h2><p>Who gathers the week's information?</p></section>
<section class="event"><span class="num">2</span><h2>Write down the proposed add</h2><p>What work, how long, and which group?</p></section>
<section class="event"><span class="num">3</span><h2>Check the overlapping rosters</h2><p>Name JV athletes also taking varsity reps.</p></section>
<section class="event final"><span class="num">4</span><h2>Bring the week to the room</h2><p>Then the staff can discuss the addition.</p></section>
</div>
<footer><span>Weekly load ownership</span><span>Sequence only. Not a time scale.</span></footer>
</article>
```

### Annotated example (labeled illustrative entry plus 3 to 4 callouts)

```html
<article class="slide" aria-label="Annotated illustrative staff report">
<h1><span>Make the addition</span><span>visible.</span></h1>
<p class="illustration">ILLUSTRATIVE ENTRY / NOT A WORK PRESCRIPTION</p>
<table class="report" aria-label="Example proposed addition"><tbody>
<tr><th scope="row"><span class="mark">1</span>Proposed work</th><td>Extended Indy</td></tr>
<tr><th scope="row"><span class="mark">2</span>Duration</th><td>8 minutes</td></tr>
<tr><th scope="row"><span class="mark">3</span>Who gets it?</th><td>Varsity receivers</td></tr>
<tr><th scope="row"><span class="mark">4</span>Roster overlap</th><td>JV call-ups: check names</td></tr>
</tbody></table>
<div class="annotations">
<div class="annotation"><strong data-number="1">Name the work</strong>Not just "a little extra."</div>
<div class="annotation"><strong data-number="2">Show the duration</strong>Example data, not a dose.</div>
<div class="annotation"><strong data-number="3">Identify the group</strong>Who gets the added work?</div>
<div class="annotation"><strong data-number="4">Check both rosters</strong>List the shared athletes.</div>
</div>
<p class="takeaway">Give this to the reporting owner<br>before the work is added.</p>
<footer><span>Weekly load ownership</span><span>Example data. No athlete records.</span></footer>
</article>
```
