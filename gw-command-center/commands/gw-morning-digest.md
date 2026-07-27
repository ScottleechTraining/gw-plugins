---
name: gw-morning-digest
model: claude-opus-5
description: "Daily morning digest - synthesize the overnight pipeline output into a 'what to dig into first' briefing. Fires at 7:15am after the rest of the morning pipeline finishes. Writes a markdown source-of-truth, a phone-optimized HTML for email, and a self-contained 4-panel dashboard page deployed to Netlify."
---

# /gw-morning-digest - Daily Action-Oriented Briefing



Fires daily at 7:15am after the rest of the morning pipeline has finished. Reads everything the pipeline produced overnight, maps it to GW products, and writes an action-oriented digest that Scott reads with morning coffee to decide what to dig into first.



## Output targets



Write THREE files (all overwritten each morning):



1. `C:\Claude Projects\Gridiron Warrior\_morning-briefing.md` - markdown source-of-truth, archived to git

2. `C:\Claude Projects\Gridiron Warrior\_morning-briefing.html` - phone-optimized HTML used by the email sender

3. `C:\Claude Projects\Gridiron Warrior\_dashboard-index.html` - self-contained dashboard page (4-panel dropdown) that the `build-gw-dashboard.ps1` script deploys to Netlify each morning



The PowerShell email script reads the `.html` file and sends it as an HTML email to scott@scottleechtraining.com. The dashboard build script reads `_dashboard-index.html` and deploys it to Netlify.



## What to read (in this order)



Use the local operational date in `America/New_York`. Do not use the UTC date for file matching.



1. `scripts\health\*-YYYY-MM-DD.status.json` - scoreboard source of truth. Read these before judging whether a pipeline ran, blocked, or missed.

2. `Deliverables\_daily-seeds\YYYY-MM-DD.md` - today's content seed (highest signal)

3. `External Library\BusinessDocuments\YYYY-MM-DD-*-brief.md` - today's business research brief

4. `External Library\AI\YYYY-MM-DD-*-brief.md` - today's AI research brief

5. `External Library\S-and-C\YYYY-MM-DD-*-brief.md` - today's S&C research brief

6. `wiki\log.md` - last 24h of pipeline log entries (errors, counts, anything flagged)

7. `External Library\BusinessDocuments\_topic-queue.md`, `External Library\AI\_topic-queue.md`, `External Library\S-and-C\_topic-queue.md` - queue depths



Dewey, screenshots, voice notes are intentionally NOT read here. Their daily counts and standouts already land in `wiki/log.md` via the `/gw-dewey-daily`, `/gw-screenshot-ingest`, and `/gw-voice-ingest` skills, and the Dewey daily confirmation arrives in a separate email. Pull their numbers from `wiki/log.md` only.



## Operational truth rules



- If a status file exists for a gate, trust it over inference from missing output files.

- If a status file says `blocked`, report `<lane> blocked: <root_cause>. Next action: <next_action>`. Do not say "no pipeline run."

- If a status file says `complete` but the expected output file is missing, report `<lane> completed preflight but artifact missing` and include the exact expected path.

- If no status file exists for a normally scheduled gate after its scheduled time, report `<lane> missing status file` and list the gate name.

- Queue files must be checked by exact path. Never report "S&C no queue file" unless `C:\Claude Projects\Gridiron Warrior\External Library\S-and-C\_topic-queue.md` cannot be read. If a queue read fails, include the exact path and error.

- The retired Sunday Film Study weekly-batch flow is dead. Do not recommend opening `wiki\pending\weekly-batch-*.md`. Do not reference Sunday/Tuesday/Thursday batch production. The active Film Study lane is `/gw-film-study-brief "<topic>"`, then manual `/gw-content-forge "<brief path>"` if Scott wants assets.

- Old weekly batch files under `wiki\pending\` are historical artifacts unless Scott explicitly asks about them.



## Digest structure (markdown source)



Write the markdown file using this exact structure. Keep it tight - every section earns its spot.

Opportunity Radar rule: before writing, check `Gridiron Warrior/wiki/business/opportunity-radar.md`. If it gained a RUN-WITH-IT entry since the last digest (unchecked, score 80+), name it in its own line at the top of Today's Move: what the idea is, its score, and the save it came from. Scott decides same-week: build, park, or kill. If nothing new, say nothing.



```markdown

Subject: GW Daily - YYYY-MM-DD - <3-word essence of today's move>



# GW Daily - YYYY-MM-DD



## Today's Move



ONE action. The single highest-leverage thing to do today. One sentence. Bold the verb. Reference the file or command it lives in.



Example: **Run** `/gw-content-forge "1,808 saved posts - saving vs doing"` to expand Angle 1 from today's seed.



## If You Have Time



Up to 2 more actions. One line each. Skip the section entirely if there's only the one move.



- (one-line action with file ref)

- (one-line action with file ref)



## What's New



One line per source. Skip lines for sources with zero new items. Lead with the count, then the standout. Dewey / voice / screenshot counts come from `wiki/log.md` only - do NOT open those folders.



- **Business brief**: <topic-slug>. <one-line takeaway>.

- **AI brief**: <topic-slug>. <one-line takeaway>.

- **S&C brief**: <topic-slug>. <one-line takeaway>.

- **Dewey** (from log): N saves. Top: <author> on <topic if log captured it>.

- **Voice** (from log): N notes.

- **Screenshots** (from log): N processed.



## Heads Up



ONLY include this section if there's something to flag. Otherwise omit entirely.



- Queue: <Business N / AI N / S&C N> (flag if any < 5)

- Errors in last 24h: <count + brief>

- Flagged from yesterday: <if any>



## Today's Seed Angles



Paste the daily seed angles verbatim. These ARE the day's content raw material.



## Deep Dive



File paths for anything mentioned above, listed for the laptop session later in the day.



- Seed: `Deliverables\_daily-seeds\YYYY-MM-DD.md`

- Business brief: `External Library\BusinessDocuments\YYYY-MM-DD-<topic>-brief.md`

- AI brief: `External Library\AI\YYYY-MM-DD-<topic>-brief.md`

- S&C brief: `External Library\S-and-C\YYYY-MM-DD-<topic>-brief.md`

- (etc - only include sections that actually have content today)

```



## HTML structure (email body)



Write `_morning-briefing.html` with the SAME content rendered for mobile email clients (iOS Mail, Gmail iOS, Gmail Android). Rules:



- Doctype HTML4 transitional, table-based layout (NOT divs/flex - clients strip them)

- All CSS inline on every element (`<style>` blocks get stripped)

- Single column, `max-width: 600px`, centered

- Font: `-apple-system, "Segoe UI", Roboto, sans-serif` so iOS and Android use system fonts

- Body bg `#f5f5f5`, content card `#ffffff` with `12px` padding, `border-radius: 8px`

- No images, no remote assets (block on most phones by default)

- **"Open Dashboard" button at the top**: red URI-colored button linking to the Netlify dashboard so Scott can tap straight to the 4-panel view from the email.

- "Today's Move" rendered LARGE: `font-size: 20px`, `font-weight: 600`, distinctive `border-left: 4px solid #c8102e` (URI navy/red), `padding-left: 12px`, `margin-bottom: 24px`

- Section headers `<h2>` with `font-size: 14px`, `text-transform: uppercase`, `letter-spacing: 1px`, `color: #666`, `margin-top: 28px`

- Body text `font-size: 16px`, `line-height: 1.5`, `color: #222`

- Inline code (file paths, slash commands) wrapped in `<code>` with `background: #f0f0f0`, `padding: 2px 6px`, `border-radius: 3px`, `font-size: 14px`

- Lists: `<ul style="padding-left: 20px; margin: 8px 0">`, `<li style="margin-bottom: 6px">`

- NO tables for data (single-column lists only - multi-column tables overflow on phone)

- NO emoji in headings (render inconsistently on phone)

- Skeleton template:



```html

<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">

<html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1"></head>

<body style="margin:0;padding:0;background:#f5f5f5;font-family:-apple-system,'Segoe UI',Roboto,sans-serif;color:#222;">

<table width="100%" cellpadding="0" cellspacing="0" style="background:#f5f5f5;padding:20px 0;">

  <tr><td align="center">

    <table width="600" cellpadding="0" cellspacing="0" style="max-width:600px;background:#ffffff;border-radius:8px;padding:24px;">

      <tr><td>

        <p style="font-size:12px;color:#888;margin:0 0 4px 0;text-transform:uppercase;letter-spacing:1px;">GW Daily - YYYY-MM-DD</p>

        <p style="margin:8px 0 16px 0;"><a href="https://gw-command-center.netlify.app" style="display:inline-block;background:#c8102e;color:#ffffff;text-decoration:none;font-size:14px;font-weight:600;padding:10px 18px;border-radius:6px;">Open Dashboard &rarr;</a></p>

        <div style="font-size:20px;font-weight:600;line-height:1.4;border-left:4px solid #c8102e;padding-left:12px;margin:16px 0 24px 0;color:#111;">

          [Today's Move text, with <code> for inline file refs]

        </div>

        <h2 style="font-size:14px;text-transform:uppercase;letter-spacing:1px;color:#666;margin:28px 0 8px 0;">If You Have Time</h2>

        <ul style="padding-left:20px;margin:8px 0;font-size:16px;line-height:1.5;">

          <li style="margin-bottom:6px;">[item]</li>

        </ul>

        <h2 style="font-size:14px;text-transform:uppercase;letter-spacing:1px;color:#666;margin:28px 0 8px 0;">What's New</h2>

        [same pattern]

        <!-- Heads Up only if non-empty -->

        <h2 style="font-size:14px;text-transform:uppercase;letter-spacing:1px;color:#666;margin:28px 0 8px 0;">Today's Seed Angles</h2>

        [seed angles as paragraphs]

        <h2 style="font-size:14px;text-transform:uppercase;letter-spacing:1px;color:#666;margin:28px 0 8px 0;">Deep Dive</h2>

        <ul style="padding-left:20px;margin:8px 0;font-size:14px;line-height:1.5;color:#555;">

          <li style="margin-bottom:4px;"><code style="background:#f0f0f0;padding:2px 6px;border-radius:3px;font-size:13px;">[path]</code></li>

        </ul>

        <p style="font-size:11px;color:#aaa;margin-top:32px;border-top:1px solid #eee;padding-top:12px;">Keep the Fire Burning, / Leech</p>

      </td></tr>

    </table>

  </td></tr>

</table>

</body></html>

```



DO NOT include the `Subject:` line in the HTML body (the sender extracts it from the .md and sets it separately).



## Dashboard structure (`_dashboard-index.html`)



This is the self-contained file deployed to Netlify each morning by `build-gw-dashboard.ps1`. ONE HTML document. Phone-first **editorial sports tabloid** aesthetic - think SI 1987 + locker room + Coach Leech voice. Confident, tactile, magazine-issue energy.



**DO NOT regress this to generic SaaS dashboard styling** (light gray bg + white card + system fonts + plain dropdown). The bold design is intentional and on-brand. If you find yourself reaching for `-apple-system` or `border-radius: 8px` on the card, stop - the spec below is the design.



Rules:



- Doctype HTML5. `<meta name="robots" content="noindex,nofollow">` REQUIRED in head.

- `<meta name="viewport" content="width=device-width, initial-scale=1">` REQUIRED.

- Preconnect + load Google Fonts: Oswald (300/500/700) + Source Serif 4 (regular/600/italic).

- Color tokens (CSS variables - use exactly these in `:root`):

  - `--ink: #0a0a0a` (near-black for bars, headlines, primary text)

  - `--paper: #f1ece1` (newsprint cream page bg)

  - `--paper-deep: #e6dfd0` (shadow tone)

  - `--rust: #c8102e` (URI red - the command color, used sparingly for impact)

  - `--navy: #18243d` (URI navy, used on code/path text)

  - `--rule: #c9bfa9` (cream-tinted hairline rules)

  - `--muted: #6b6157` (warm gray for secondary text, signoff)

  - `--cream: #faf6ec` (panel surface, lighter than --paper)

- Body bg: `--paper` with subtle two-layer radial-gradient dot grain (see template).

- **Layout (three structural blocks plus a footer):**

  - `<header class="masthead">` - full-width ink-black bar with 6px URI-red bottom border. Inside (max-width 760px centered): brand mark "Gridiron Warrior" in Oswald 700 caps letter-spaced, "Command" sub-label in Oswald 300 in URI red. Right side: "Issue" label + date as `YYYY.MM.DD` (dots, not dashes) in Oswald 700.

  - `<nav class="tabs">` - full-width ink-black bar with 4 button tabs flush across. Active tab gets URI red bg with cream text and weight 700. Tabs use Oswald 500/700 caps, letter-spacing 0.18em. **Tab labels: "Today" / "AI" / "Business" / "S&C"**. NOT a `<select>` dropdown - this is a tab bar.

  - `<main class="paper">` - max-width 760px centered container. Inside: four `<section class="panel">` blocks, only `.active` visible.

  - `<footer class="colophon">` - tiny letterspaced Oswald caps, "Keep the Fire Burning" in URI red, then "Leech Â· Gridiron Warrior" in muted gray.

- **Typography rules inside panels:**

  - `h1` = Oswald 700 ALL CAPS, `clamp(28px, 6.5vw, 36px)`, line-height 1.05, 3px ink bottom border. Brief title.

  - `h2` = Oswald 700 caps, 13px, letter-spacing 0.22em, CREAM text on INK BACKGROUND, full-bleed inside the panel (`margin: 32px -26px 16px; padding: 9px 26px`). These are editorial section bars, not gray subtitles.

  - `h3` = Oswald 500 caps, 18px, ink text, with 4px URI red left border.

  - `p, li` = Source Serif 4, 17px, line-height 1.6, ink color.

  - `code` = JetBrains Mono / Consolas / monospace, 13.5px, navy text on `--paper` bg with `--rule` border.

  - `blockquote` = italic Source Serif 4, 18px, 4px URI red left border, with paper-to-transparent gradient bg. Pull-quote treatment.

  - `.quote` (smaller seed-angle quote) = italic Source Serif 4, 16px, muted, 2px rule left border.

  - `.today-move` (the "Today's Move" callout in the Today panel) = Oswald 500, `clamp(20px, 4.5vw, 26px)`, line-height 1.25, ink color, `--paper` bg, 6px URI red left border, 18px 20px padding. Inside, `<strong>` is URI red. **This is the dashboard's hero element.**

  - `.signoff` = italic Source Serif 4, 14px, muted, with rule top border and 32px top margin. Format: `<strong>Keep the Fire Burning,</strong> / Leech` (the strong is URI red, not italic).

- **Tables** (Business briefs etc): th in Oswald caps 12px on `--paper` bg with 2px ink bottom border; td in Source Serif 15px with rule hairline separators.

- **Responsive (`@media max-width: 520px`):** masthead/paper padding tightens; h2 bars extend to `-18px` margins; tabs drop to 13px font with 0.14em letter-spacing; today-move padding tightens.

- **Tab behavior:** Vanilla JS at end of body. On tab click, swap `.active` class across `.tab` buttons (set `aria-selected` too) and `.panel` sections. Always `window.scrollTo({ top: 0, behavior: 'instant' })` after tab change so the new panel reads from the top.

- **Content rules:**

  - **Today panel** = the full digest content (same content as the email body). "Today's Move" wrapped in `<div class="today-move">`, then h2 bars for If You Have Time / What's New / Today's Seed Angles / Deep Dive. Each seed angle gets an h3 with red leading border. Seed pull-quotes use `class="quote"`.

  - **AI / Business / S&C panels** = the full content of today's brief, rendered as clean HTML. Strip YAML frontmatter. Convert markdown to HTML: `## Heading` â†’ `<h2>`, `### Subhead` â†’ `<h3>`, lists, blockquote, code for inline code/paths. Topic name from frontmatter is the `<h1>`.

  - Sign-off at bottom of every panel: `<p class="signoff"><strong>Keep the Fire Burning,</strong> / Leech</p>`.

  - If a brief is missing for today (pipeline failure / pre-launch), that panel still renders with its `<h1>` set to the panel name (e.g. "AI Brief") and a single paragraph: "No brief produced today. Check pipeline logs." Followed by the signoff. The dashboard never breaks.

- **Issue date format:** dots not dashes in the masthead (`2026.05.18`), per editorial convention. Keep dashes in file paths.



Skeleton template (use this exactly - replace YYYY.MM.DD with the dotted date for masthead, YYYY-MM-DD with the standard date in file paths, and the content inside each `<section class="panel">`):



```html

<!DOCTYPE html>

<html lang="en">

<head>

<meta charset="UTF-8">

<meta name="viewport" content="width=device-width, initial-scale=1">

<meta name="robots" content="noindex,nofollow">

<title>GW Command - YYYY-MM-DD</title>

<link rel="preconnect" href="https://fonts.googleapis.com">

<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>

<link href="https://fonts.googleapis.com/css2?family=Oswald:wght@300;500;700&family=Source+Serif+4:ital,opsz,wght@0,8..60,400;0,8..60,600;1,8..60,400&display=swap" rel="stylesheet">

<style>

  :root {

    --ink: #0a0a0a; --paper: #f1ece1; --paper-deep: #e6dfd0;

    --rust: #c8102e; --navy: #18243d; --rule: #c9bfa9;

    --muted: #6b6157; --cream: #faf6ec;

  }

  * { box-sizing: border-box; }

  html, body { margin:0; padding:0; }

  body {

    background: var(--paper);

    background-image:

      radial-gradient(rgba(10,10,10,0.025) 1px, transparent 1px),

      radial-gradient(rgba(10,10,10,0.018) 1px, transparent 1px);

    background-size: 3px 3px, 7px 7px;

    background-position: 0 0, 1px 1px;

    color: var(--ink);

    font-family: 'Source Serif 4', Charter, 'Iowan Old Style', Georgia, serif;

    font-size: 17px; line-height: 1.55;

    -webkit-font-smoothing: antialiased;

  }

  .masthead { background: var(--ink); color: var(--cream); border-bottom: 6px solid var(--rust); }

  .masthead-inner { max-width: 760px; margin: 0 auto; padding: 22px 24px 18px; display: flex; align-items: flex-end; justify-content: space-between; gap: 16px; }

  .brand-mark { font-family: 'Oswald', sans-serif; font-weight: 700; font-size: clamp(26px, 7vw, 38px); letter-spacing: 0.06em; line-height: 0.95; text-transform: uppercase; color: var(--cream); }

  .brand-sub { font-family: 'Oswald', sans-serif; font-weight: 300; font-size: clamp(13px, 3vw, 16px); letter-spacing: 0.4em; text-transform: uppercase; color: var(--rust); margin-top: 4px; }

  .meta-block { text-align: right; font-family: 'Oswald', sans-serif; color: var(--cream); flex-shrink: 0; }

  .meta-label { font-size: 10px; font-weight: 500; letter-spacing: 0.3em; text-transform: uppercase; color: var(--paper-deep); opacity: 0.7; }

  .meta-value { font-size: clamp(16px, 4vw, 20px); font-weight: 700; letter-spacing: 0.04em; margin-top: 2px; }

  .tabs { background: var(--ink); border-bottom: 1px solid var(--rule); }

  .tabs-inner { max-width: 760px; margin: 0 auto; display: flex; flex-wrap: wrap; }

  .tab { flex: 1 1 0; min-width: 25%; appearance: none; background: var(--ink); color: var(--cream); border: none; border-right: 1px solid rgba(255,255,255,0.08); padding: 14px 8px; font-family: 'Oswald', sans-serif; font-weight: 500; font-size: 14px; letter-spacing: 0.18em; text-transform: uppercase; cursor: pointer; transition: background 120ms ease-out; }

  .tab:last-child { border-right: none; }

  .tab:hover { background: #1c1c1c; }

  .tab.active { background: var(--rust); color: var(--cream); font-weight: 700; }

  .tab:focus-visible { outline: 2px solid var(--cream); outline-offset: -4px; }

  .paper { max-width: 760px; margin: 28px auto 0; padding: 0 16px; }

  .panel { display: none; background: var(--cream); border: 1px solid var(--rule); border-top: 4px solid var(--ink); padding: 28px 26px 36px; box-shadow: 0 1px 0 var(--paper-deep), 0 8px 20px rgba(10,10,10,0.04); }

  .panel.active { display: block; }

  .panel h1 { font-family: 'Oswald', sans-serif; font-weight: 700; font-size: clamp(28px, 6.5vw, 36px); line-height: 1.05; letter-spacing: 0.01em; text-transform: uppercase; color: var(--ink); margin: 0 0 18px 0; padding-bottom: 14px; border-bottom: 3px solid var(--ink); }

  .panel h2 { font-family: 'Oswald', sans-serif; font-weight: 700; font-size: 13px; letter-spacing: 0.22em; text-transform: uppercase; color: var(--cream); background: var(--ink); margin: 32px -26px 16px; padding: 9px 26px; }

  .panel h3 { font-family: 'Oswald', sans-serif; font-weight: 500; font-size: 18px; letter-spacing: 0.04em; text-transform: uppercase; color: var(--ink); margin: 22px 0 8px; padding-left: 14px; border-left: 4px solid var(--rust); }

  .panel p, .panel li { font-family: 'Source Serif 4', Georgia, serif; font-size: 17px; line-height: 1.6; color: var(--ink); }

  .panel p { margin: 10px 0 14px; }

  .panel ul, .panel ol { padding-left: 22px; margin: 10px 0 18px; }

  .panel li { margin-bottom: 8px; }

  .panel strong { font-weight: 600; color: var(--ink); }

  .panel code { font-family: 'JetBrains Mono', 'Consolas', 'SF Mono', Menlo, monospace; font-size: 13.5px; background: var(--paper); color: var(--navy); padding: 2px 7px; border-radius: 2px; border: 1px solid var(--rule); word-break: break-word; }

  .today-move { font-family: 'Oswald', sans-serif; font-weight: 500; font-size: clamp(20px, 4.5vw, 26px); line-height: 1.25; letter-spacing: 0.005em; color: var(--ink); background: var(--paper); border-left: 6px solid var(--rust); padding: 18px 20px; margin: 14px 0 28px; }

  .today-move strong { color: var(--rust); font-weight: 700; }

  .today-move code { font-size: 14px; background: var(--cream); border-color: var(--paper-deep); }

  .panel blockquote { font-family: 'Source Serif 4', Georgia, serif; font-style: italic; font-size: 18px; line-height: 1.5; color: var(--ink); border-left: 4px solid var(--rust); margin: 18px 0; padding: 6px 16px; background: linear-gradient(to right, var(--paper) 0%, transparent 60%); }

  .quote { font-family: 'Source Serif 4', Georgia, serif; font-style: italic; color: var(--muted); font-size: 16px; margin: 4px 0 10px; padding-left: 12px; border-left: 2px solid var(--rule); }

  .panel table { border-collapse: collapse; width: 100%; margin: 14px 0 18px; font-family: 'Source Serif 4', Georgia, serif; font-size: 15px; }

  .panel th, .panel td { border-bottom: 1px solid var(--rule); padding: 9px 8px; text-align: left; vertical-align: top; }

  .panel th { font-family: 'Oswald', sans-serif; font-weight: 500; font-size: 12px; letter-spacing: 0.15em; text-transform: uppercase; color: var(--ink); background: var(--paper); border-bottom: 2px solid var(--ink); }

  .colophon { max-width: 760px; margin: 24px auto 28px; padding: 14px 26px; text-align: center; font-family: 'Oswald', sans-serif; font-size: 11px; letter-spacing: 0.5em; text-transform: uppercase; color: var(--muted); border-top: 1px solid var(--rule); }

  .colophon .flame { color: var(--rust); font-weight: 700; }

  .signoff { margin-top: 32px; padding-top: 16px; border-top: 1px solid var(--rule); font-family: 'Source Serif 4', Georgia, serif; font-style: italic; font-size: 14px; color: var(--muted); }

  .signoff strong { color: var(--rust); font-style: normal; font-weight: 600; }

  @media (max-width: 520px) {

    .masthead-inner { padding: 18px 16px 14px; }

    .paper { padding: 0 10px; margin-top: 18px; }

    .panel { padding: 22px 18px 28px; }

    .panel h2 { margin-left: -18px; margin-right: -18px; padding: 8px 18px; }

    .tab { padding: 13px 4px; font-size: 13px; letter-spacing: 0.14em; }

    .today-move { padding: 14px 16px; }

  }

</style>

</head>

<body>

<header class="masthead">

  <div class="masthead-inner">

    <div>

      <div class="brand-mark">Gridiron Warrior</div>

      <div class="brand-sub">Command</div>

    </div>

    <div class="meta-block">

      <div class="meta-label">Issue</div>

      <div class="meta-value">YYYY.MM.DD</div>

    </div>

  </div>

</header>

<nav class="tabs" role="tablist" aria-label="Briefs">

  <div class="tabs-inner">

    <button class="tab active" data-target="today" role="tab" aria-selected="true">Today</button>

    <button class="tab" data-target="ai" role="tab" aria-selected="false">AI</button>

    <button class="tab" data-target="business" role="tab" aria-selected="false">Business</button>

    <button class="tab" data-target="sc" role="tab" aria-selected="false">S&amp;C</button>

  </div>

</nav>

<main class="paper">

  <section id="today" class="panel active" role="tabpanel">

    <h1>GW Daily &middot; YYYY-MM-DD</h1>

    <!-- Today's Move as <div class="today-move">, then h2 bars for If You Have Time / What's New / Today's Seed Angles / Deep Dive. Seed angle subheads use h3 with red border. Seed pull-quotes use class="quote". -->

    <p class="signoff"><strong>Keep the Fire Burning,</strong> / Leech</p>

  </section>

  <section id="ai" class="panel" role="tabpanel">

    <h1>[AI brief topic name]</h1>

    <!-- full AI brief rendered as clean HTML, frontmatter stripped -->

    <p class="signoff"><strong>Keep the Fire Burning,</strong> / Leech</p>

  </section>

  <section id="business" class="panel" role="tabpanel">

    <h1>[Business brief topic name]</h1>

    <!-- full Business brief rendered as clean HTML, frontmatter stripped -->

    <p class="signoff"><strong>Keep the Fire Burning,</strong> / Leech</p>

  </section>

  <section id="sc" class="panel" role="tabpanel">

    <h1>[S&C brief topic name]</h1>

    <!-- full S&C brief rendered as clean HTML, frontmatter stripped -->

    <p class="signoff"><strong>Keep the Fire Burning,</strong> / Leech</p>

  </section>

</main>

<footer class="colophon">

  <span class="flame">Keep&nbsp;the&nbsp;Fire&nbsp;Burning</span> &middot; Leech &middot; Gridiron Warrior

</footer>

<script>

(function(){

  var tabs = document.querySelectorAll('.tab');

  var panels = document.querySelectorAll('.panel');

  tabs.forEach(function(t){

    t.addEventListener('click', function(){

      var target = t.getAttribute('data-target');

      tabs.forEach(function(x){ x.classList.remove('active'); x.setAttribute('aria-selected', 'false'); });

      panels.forEach(function(p){ p.classList.remove('active'); });

      t.classList.add('active');

      t.setAttribute('aria-selected', 'true');

      var panel = document.getElementById(target);

      if (panel) panel.classList.add('active');

      window.scrollTo({ top: 0, behavior: 'instant' });

    });

  });

})();

</script>

</body>

</html>

```



## Voice and tone



- Action-oriented. Every bullet should imply a concrete next step.

- Coach-direct. Short sentences. No marketing fluff.

- Scott's voice rules apply (no em-dashes ever, no banned words, "Keep the Fire Burning" as sign-off if you sign at all).

- If something has no clear GW application, do NOT force one. Better to have a short section than padded fluff.



## Read budget (HARD CAPS - do not exceed)



This skill MUST finish in under 5 minutes wall-clock. Aggressive read discipline:



- **Max 8 individual Read tool calls total.** This is a synthesis pass, not an archival pass.

- **Do NOT Glob or Grep the whole vault.** Use date-pattern globs only against known directories.

- **Always read:** today's seed file, today's business brief, today's AI brief, today's S&C brief, wiki/log.md tail (last 50 lines).

- **Do NOT read voice notes, Dewey notes, or screenshot notes.** Pull their counts and top hits from `wiki/log.md` - `/gw-voice-ingest`, `/gw-dewey-daily`, and `/gw-screenshot-ingest` already wrote one-line summaries there. That's the digest's source of truth for those sources.

- **CLAUDE.md: already in your project context - do NOT re-Read it.**

- If you hit the read cap mid-pass, STOP and synthesize with what you have. A short crisp digest beats a long thorough one for the morning-email use case.



## Steps



### 1. Read only the inputs above, within the read budget

### 2. Synthesize the digest into the markdown structure above

### 3. Write `_morning-briefing.md` at vault root (overwrite, don't append)

### 4. Render the same content into `_morning-briefing.html` using the email HTML rules above (overwrite, don't append). Both files must reflect the same digest content; HTML omits the `Subject:` line. **Include the "Open Dashboard â†’" button at the top of the email body** linking to `https://gw-command-center.netlify.app`.

### 5. Write `_dashboard-index.html` at vault root (overwrite, don't append). One self-contained HTML file with the 4-panel dropdown described in the Dashboard structure section. Today's Briefing panel mirrors the email body content. The AI / Business / S&C panels render the FULL today's brief (frontmatter stripped, markdown converted to clean HTML). If a brief file is missing for today, that panel shows "No brief produced today. Check pipeline logs."

### 6. Append every forge suggestion in this digest to the backlog

Every `/gw-content-forge "..."` you printed in Today's Move / If You Have Time (the digest often rewrites the seed's hook, so these phrasings would otherwise never reach the queue). Append each to `queue-state.json`'s `forge_backlog`, additive with slug dedup. Do NOT rebuild the array. Fill `titles` with the exact quoted text of each forge suggestion in today's digest.

```bash
python -c "
import json, pathlib, re
from datetime import date
titles = [
    # FILL IN: exact text inside each /gw-content-forge \"...\" you printed today.
]
p = pathlib.Path('C:/Claude Projects/Gridiron Warrior/Deliverables/queue-state.json')
data = json.loads(p.read_text(encoding='utf-8'))
backlog = data.setdefault('forge_backlog', [])
existing = {e['slug'] for e in backlog}
def slugify(t):
    head = t.split(',')[0].strip().lower()
    s = re.sub(r'[^a-z0-9]+', '-', head)
    return re.sub(r'-+', '-', s).strip('-')[:80]
today = date.today().isoformat()
added = 0
for t in titles:
    slug = slugify(t)
    if slug in existing: continue
    backlog.append({'slug': slug, 'title': t, 'format': None, 'score': '14/20',
                    'source': f'daily-report {today}', 'added': today, 'status': 'pending'})
    existing.add(slug); added += 1
p.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding='utf-8')
print(f'forge_backlog: appended {added} suggestion(s) from today\'s digest')
"
```

The nightly forge picker applies its own novelty gate on top of this, so a paraphrase that duplicates an already-forged topic is dropped at pick time. This step only makes sure the idea reaches the queue instead of leaking.

### 7. Append a single line to wiki/log.md:

```

YYYY-MM-DD /gw-morning-digest: digest written (1 top move, N new vault items)

```

### 8. Do NOT commit

The `gw-daily-closeout` job runs after this digest and commits all approved daily-output paths once, via `scripts/git_safe_commit.py`. This skill's job ends at writing `_morning-briefing.md`, `_morning-briefing.html`, `_dashboard-index.html`, and the wiki/log.md line.



## Notes



- Email send is handled by a separate PowerShell script in the wrapper, NOT by this skill. This skill ONLY writes the files.

- Dashboard deploy is handled by `build-gw-dashboard.ps1` in the wrapper, NOT by this skill. This skill ONLY writes `_dashboard-index.html`.

- If nothing new came in overnight (clean no-op morning), still write the digest with "Nothing new since yesterday" in each section. Email send + dashboard deploy happen regardless.

- If a daily brief file is missing (AI / Business / S&C - pipeline failure or pre-launch), the corresponding dashboard panel must still render with "No brief produced today. Check pipeline logs." so the dashboard never breaks.

- Idempotent: re-running on the same day overwrites the previous run's briefing files.

