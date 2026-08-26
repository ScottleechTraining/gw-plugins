---
name: ig-carousel
description: Create editable, export-ready Instagram carousel slides as a single HTML file. Use this skill whenever the user mentions Instagram carousel, IG carousel, social media slides, carousel post, swipeable slides, or wants to create visual slide content for Instagram. Also trigger when the user says "make me a carousel about X", "create slides for Instagram", "social media graphics", or references carousel templates. This skill produces a self-contained HTML file with click-to-edit text fields, one-click PNG export at 1080x1350 (Instagram 4:5 ratio), and a stitched multi-page PDF export for Canva import. Supports content archetypes selected at Step 0.25 (what the post is, picked by the outcome it should win), visual style packs selected at Step 0.5 (what it looks like), and seamless image spreads across multiple slides.
---

# Instagram Carousel Skill — v3.6

Create editable, export-ready Instagram carousels as self-contained HTML files.

---

## IDENTITY — print this line FIRST, every run (non-negotiable)

The very first thing you output when this skill runs, before Step 0 or anything else, must be this line, verbatim:

`▶ ig-carousel v3.6 · gw-command-center plugin · canonical single source`

This is Scott's guarantee that the canonical plugin skill ran, not a loose shadow. If you are following carousel instructions and this IDENTITY block is not in the skill file you loaded, you are running a stale copy: stop and tell Scott the exact file path you loaded from.

---

## Known traps (non-negotiable)

Six ways carousel builds fail silently. Every one has cost real time. Check them.

1. **Hero photo must be a compact JPEG, never PNG.** A multi-MB PNG base64 overflows Chromium's CSS custom-property length limit; the `--hero-photo` variable silently drops to empty and the slide renders as a charcoal/near-black background with no error. Ship a brightened JPEG around 230KB (quality ~80, resized to slide dimensions). If a hero slide renders dark or blank, this is the first suspect.
2. **The Case pack selector trap.** Putting the `pack--case` class on the slide element itself breaks descendant selectors like `.pack--case .slide::before` (there is no descendant), and the hero photo silently fails to near-black. Either keep `pack--case` on a wrapper element around the slide, or write the selector as `.slide.pack--case::before`.
3. **Headless render quirks on this machine.** Use Edge/Chromium with `--headless=new` or embedded fonts will not load. Kill stray msedge and http.server processes before starting, and use a unique `--user-data-dir` per run plus `127.0.0.1` (not `localhost`). Use a fresh port for every throwaway static server. A desktop-width scrollbar can fake mobile clipping in screenshots, so size the window to the exact slide width.
4. **Kill your servers.** Orphaned http.server processes and hung headless Edge leave files in delete-pending state ("Access is denied" on delete that looks like an ACL problem but is an open handle). Every render script must terminate the processes it started, even on failure.
5. **Visual verification is mandatory.** Render every slide to PNG and actually look at the images (Read the PNG files) before reporting the carousel done. A file that passes a portability or lint check can still render wrong. Cover slide especially: verify the hero photo is visible, text is not clipped, and contrast holds.
6. **html2canvas does not implement CSS `filter`.** The pinned CDN build (1.4.1) silently drops every `filter:` declaration (invert, grayscale, contrast, all of it) at capture time. The live tab, the scaled editor preview, and the /gw-queue Playwright renders all apply filters correctly, so the file looks right everywhere you check — but EXPORT ALL PNGs / DOWNLOAD SLIDE / EXPORT PDF ship wrong: a `filter:invert(1)` white logo exports white-on-paper (invisible), a `filter:grayscale(1)` photo exports full color and breaks the pack palette law. Bake every photo treatment and logo ink into the source pixels with Pillow at prep time; no element inside `.slide` may carry `filter:`. Confirmed 2026-08-01 by exporting a real PNG and reading the pixels back — that is also the only way to catch it.

---

**All raw markup (HTML, CSS, JS) lives in `references/html-implementation.md`.** SKILL.md stays prose-only. When a step needs the actual code, it points you to a numbered section in that reference. Do not inline raw markup into this file.

**What's new in v3.6 (content archetypes):**
- New Step 0.25: content archetype selection, outcome-first (saves / shares / comments+DMs / follows), before the visual pack is chosen. The archetypes live in `references/content-archetypes.md` and nowhere else, same anti-drift rule as style packs.
- New comment-trigger CTA option ("Comment WORD and I'll send you X"), default for The Template archetype. Fulfillment is manual by design; see the reference file.
- Step 3B slide plan now names the archetype, and the compliance pass checks archetype structure alongside pack architecture.

**What's new in v3.4 (cover headline overflow fix):**
- The Mega-Cover auto-fit is now a verbatim, copy-exactly block (section 8 of `references/html-implementation.md`) instead of a prose description that each run re-derived. The re-derived version only fit per-span WIDTH, so multi-line headlines overflowed the frame (top word clipped, words breaking mid-word, last line colliding with the footer/handle).
- The canonical `autoFitMegaCover()` now also fits the cover to available HEIGHT and re-runs on `document.fonts.ready` (the real Vitesse glyphs are wider than the fallback the first pass measures against).
- `.mega-cover span` gains `white-space: nowrap` so a wrapped multi-word line can't hide its true width from the fit loop.
- One-off patcher for already-generated carousels: `scripts/gwqueue/patch_carousels_megacover_autofit.py` (idempotent; mirrors `patch_carousels_savebtn.py`; skips files carrying the `MEGACOVER_FIT_V1` marker).

**What's new in v3.3 (save button + identity):**
- Every generated carousel now emits the 💾 SAVE CHANGES button (new section 9 of `references/html-implementation.md`), so in-browser edits persist to disk. Copied verbatim from `scripts/gwqueue/patch_carousels_savebtn.py` so generated files self-skip the patcher.
- Added the IDENTITY banner above so every run self-identifies as the canonical plugin skill.
- This file is now `SKILL.md` inside the plugin (was `workflow.md`), so the plugin registers it directly. The loose `~/.claude/skills/ig-carousel/` shadow was removed.

**What's new in v3.2 (registration fix):**
- Every HTML, CSS, and JS block moved out of SKILL.md into `references/html-implementation.md`. SKILL.md was failing to register as a skill because it contained raw document markup (doctype, html, script tags). Behavior is unchanged; the code is one file away now.

**What's new in v3.1 (bug fix):**
- **Spread positioning fixed.** Seamless image spreads now use pixel-based background sizing and positioning. The previous percentage-based formula silently rendered slide 2+ of a spread as empty. If you have any v3 carousels with spreads, open them and check. See `references/seamless-image-spread.md` for the corrected formula.

**What's new in v3 (changes from v2):**
- Step 0.5 (style pack selection) is now hard-gated — no HTML until a pack is chosen.
- Vitesse embedding is locked to an inline style block only. External stylesheets for fonts are banned (they cache-stale and render the wrong font).
- New **pack-compliance pass** at the end of Step 3B — the slide plan must respect the chosen pack's architecture rules (reading columns, centered body allowances, photo sizing), not just its colors.
- Each carousel HTML file is **self-contained**. No shared CSS files, no external pack stylesheets, no imports beyond Barlow from Google Fonts. If it doesn't open correctly from a USB drive with no internet, it's broken.

---

## Single Source of Truth — Style Packs

**`references/style-packs.md` is the only place style packs are defined.** Pack names, descriptions, color tokens, architecture rules, overrides, and use-case mappings live there and nowhere else.

This SKILL.md must NEVER hardcode pack names ("Asphalt Editorial", "Mono Series", etc.), descriptions, color values, or architecture rules. Every place a pack is referenced, this file instructs the agent to read `references/style-packs.md`. If you find a hardcoded pack name or description in this SKILL.md outside of an example illustrating how to read style-packs.md, that's drift — fix it.

**Why:** for months the pack list lived in three places that drifted independently. Packs were renamed (High Contrast Hype to The Case, Dark Project to Mono Series) and SKILL.md kept presenting the old names to users. The structural fix is delegation, not vigilance.

**Same rule for content archetypes:** `references/content-archetypes.md` is the only place the archetypes are defined. This SKILL.md never hardcodes archetype names, outcomes, or structures.

---

## Visual Brain Reference

**Before building any carousel, read `GW_Visual_Brain.md` in the project knowledge files.** That document is the canonical source for the core brand identity (Vitesse + Barlow type, gold accent, asphalt/paper palette, negative constraints). This skill inherits all of those rules.

**Style Packs vs Visual Brain:** Style packs (Step 0.5) adjust *how* Visual Brain rules are applied — background-dominant color, accent hue, overlay strength, slide-number treatment — but never violate core constraints unless explicitly listed below. If a pack appears to conflict with the Visual Brain and the conflict is not in the Authorized Overrides list, the Visual Brain wins.

### Authorized Overrides (approved by Scott)

Some packs are allowed scoped exceptions to Visual Brain rules (accent color, body centering, word count). The full list of which pack overrides which rule lives in each pack's section in `references/style-packs.md`. Read that file to find them — do not hardcode the override list here.

The principle: overrides are scoped, not global. They apply only to the named pack inside this skill. Every other pack and every other skill follows the Visual Brain verbatim.

### Type Scale — 1080x1350 canvas

The Visual Brain type scale (36px hero, 28px section head, 14px body) is a web/UI scale. Carousel slides render on a 1080px-wide canvas, so those sizes scale up proportionally to maintain intended display sizes in-feed. Pack-specific sizes (e.g., Mega-Cover at 180–240px) are correct for the 1080x1350 canvas and compress back to the Visual Brain's intended feel when Instagram displays the slide in-feed.

---

## What This Skill Produces

A single, self-contained HTML file containing:
- 5–10 slides at 4:5 aspect ratio (1080x1350 on export)
- All text fields click-to-edit (contenteditable)
- **Toolbar:** "EXPORT ALL PNGs" + "EXPORT PDF (Canva)" + "💾 SAVE CHANGES" + per-slide "DOWNLOAD"
- **Inline resize controls:** click any editable element to show a floating A− / size / A+ / RESET toolbar; Ctrl+Up / Ctrl+Down (4px step), Shift for 1px precision; Mega-Cover spans resize per-line; auto-fit stops re-fitting once a line is manually sized
- html2canvas + jsPDF from CDN (only external runtime dependency)
- Barlow from Google Fonts CDN (only external font dependency)
- **Vitesse Bold embedded inline via base64 @font-face** (no external font file, no shared CSS)
- Pack-accent edit highlight on hover/focus
- TGW logo embedded in the progress bar footer on every slide
- Persistent frame system: slide number, handle, swipe arrow (except last). **No page dots.**
- Optional seamless image spreads: one photo sliced across 2–3 slides for the swipe-reveal effect

---

## Typography — Implementation Details

**Required embedding pattern. Do not deviate.**

Vitesse Bold ships inside the HTML file as a base64 data URL in an inline style block. Barlow loads from Google Fonts.

**For the exact document head and inline @font-face skeleton, read section 1 of `references/html-implementation.md`.** Read the full base64 string from `assets/vitesse-bold-base64.txt` and paste it where the `{VITESSE_BASE64}` placeholder sits.

**Banned patterns (these will break silently or cache-stale):**
- An external stylesheet link pointing to a shared pack file that contains the @font-face
- Referencing `assets/Vitesse-Bold.otf` as a `src: url()` path (won't resolve when the user opens the file elsewhere)
- Splitting the @font-face into its own .css file and importing it
- Omitting `font-display: block` (causes a paint flash of a fallback font before Vitesse loads)

**Why inline-only:** the HTML is meant to be portable. A user may open it from Desktop, from a Canva import staging folder, from a USB drive, or a colleague's laptop. External CSS files break any of those. Inline @font-face makes the file a true single-file artifact.

Every style pack uses the same two families. Packs differ in weight, size, casing, and tracking — not family.

---

## Workflow

### Step 0: Detect Mode

Check whether the user has provided images or references an image folder.

- **Image Mode** — user mentions images, a folder path, or you find images at `Gridiron Warrior/Images/carousels/`. Run all steps.
- **Text-Only Mode** — no images provided. Skip Steps 2B and 3B.

---

### Step 0.25: Content Archetype Selection (outcome first)

Before picking a look, pick the job. Read `references/content-archetypes.md` — the only place archetypes are defined — and choose what the carousel IS:

1. From the topic or brief, infer what the post should WIN: saves, shares, comments and DMs, or follows.
2. Recommend ONE archetype using the outcome table in that file. If the brief makes it obvious, state the pick and the reason in one line. If two genuinely fit, ask one short either/or question.
3. Carry the choice forward: the archetype's structure shapes the Step 3B slide plan, its CTA guidance shapes the final slide, and its pack-fit suggestions seed the Step 0.5 recommendation.

This is a one-breath step, not a second gate. Present the archetype pick together with the Step 0.5 pack menu in a single message, so the user confirms both in one reply.

---

### Step 0.5: Style Pack Selection — HARD GATE

**Do not proceed past this step without a pack choice.** No color derivation, no slide planning, no HTML. The pack shapes every downstream decision.

**Build the menu from `references/style-packs.md` — do not hardcode it here.**

Open that file. Each top-level pack heading (formatted as "N. PACK NAME") is one menu option, numbered in the order they appear (1 through whatever count is in the file). For each pack, the user-facing line is:

```
N. PACK NAME — one-line description, taken from the first paragraph under the heading.
   Good for: the list from the "Recommend for:" bullet at the end of that pack's section.
```

The "Pack selection quick-reference" table at the bottom of `references/style-packs.md` is the canonical "if user said X, suggest Y" mapping. Use it when recommending a pack.

Then ask: "Which one? (number or name)"

**After the user picks:**
1. Re-read the pack's section in `references/style-packs.md` and copy its `:root` tokens and CSS guidance verbatim. Do not improvise pack values.
2. Note the pack's architecture rules (photo treatment, slide-number treatment, ornaments, body-copy rules) for the compliance pass at Step 3B.

**Drift guardrail:** if your mental model of the pack list does not match what `references/style-packs.md` actually says right now, trust the file. Do not present a pack from memory that has been renamed or removed.

---

### Step 1: Gather Inputs

Check conversation history first. Confirm any missing:

1. **Topic** — what the carousel teaches or promotes
2. **Brand name** — default: Gridiron Warrior
3. **Instagram handle** — default: @Sleech72
4. **Accent color override** *(optional)* — each pack has a locked default; only override if the user explicitly asks
5. **Tone** — coach-tough, professional, playful, minimal
6. **CTA** — follow, link in bio, DM, or comment-trigger ("Comment WORD and I'll send you X" — rules in `references/content-archetypes.md`). The Step 0.25 archetype sets the default.
7. **Image folder** *(Image Mode only)* — default: `Gridiron Warrior/Images/carousels/`
8. **Seamless spreads?** — ask: "Want any photos to span multiple slides for a swipe-reveal effect? e.g., 'slide 3–4' or 'slide 2–3–4'." Default: none.

Do not ask about fonts.

---

### Step 2A: Derive the Color System

Pull the base tokens from the selected style pack. All packs share the same structural tokens, only their values shift. **For the `:root` token list, read section 2 of `references/html-implementation.md`.**

Exact values live in `references/style-packs.md`. Copy them, don't improvise.

---

### Step 2B: Catalog the Images (Image Mode only)

Same as v1/v2. For each file, note filename, energy level (High/Low), mood, best use. Column for v2+: `span-candidate` — is this photo wide enough / composed well enough to work as a seamless multi-slide spread? (Generally: full-body shots, wide landscapes, horizontal action. Not: tight headshots.)

---

### Step 3A: Map Slide Content

Read `references/slide-architecture.md` for the full template structure and component library.

**Copy-source rule (non-negotiable, Scott 2026-08-26).** When building from a content
pack, slide copy comes from the pack's carousel "Slide Text" section (plus its caption)
ONLY. The pack's meta sections — THE MESSAGE, PULLED FROM THE BRAIN, the
Cross-Reference Summary, frontmatter, `cta_rationale` — are triage receipts for Scott
and must NEVER appear on a slide, in a caption, or anywhere in the rendered file. A
bare source credit or label with no on-slide explanation is the same fail: explain it
on the slide or cut it (attribution lives in the pack's thread assets). If the pack's
slide text itself breaks its cover's promise or carries an unexplained label, report
back instead of building it broken.

**Template vocabulary:**

| Template | Purpose |
|---|---|
| **Mega-Cover** | Big font power statement. Stacked lines, tight leading, auto-fit to safe zone. Default cover. |
| **Image-Dominant Hook** | Full-bleed photo with overlay headline in corner |
| **Numbered Content** | Oversized ghosted "02" in background + headline + body |
| **Split-Image Spread** | One wide image sliced across N slides (seamless swipe reveal) |
| **Highlighted-Word Paragraph** | Accent color block behind specific words in body copy |
| **Pull Quote** | Large quote marks, attribution line |
| **Color-Block Statement** | Solid accent background, huge contrast text |
| **Long-Form Text** | Reading-column body copy with numbered subhead. Used heavily in Editorial Long-Form pack. |
| **Checklist** | Numbered or checked list items (Editorial Long-Form only for true checklists) |
| **CTA / Follow** | Final slide, no swipe arrow, logo lockup |

**Cover headline rule:** the cover is a phone-legible power statement. Write whatever length you want — the skill auto-fits the type to the safe zone. If auto-fit drops the size below 80pt (at 1080x1350), stop and recommend trimming. Powerful > short.

**Narrative arc (7 slides ideal, flex 5–10):** Cover, Hook, Build, Turn, Payoff, Reinforce, CTA. Light/dark rhythm still applies within the pack's dominant palette.

---

### Step 3B: Generate the Slide Plan — CHECKPOINT

```
SLIDE PLAN — [Topic] Carousel — [Archetype] — [Style Pack]

| # | Role | Template | Headline | Image | Treatment | Span |
|---|------|----------|----------|-------|-----------|------|
| 1 | Cover | Mega-Cover | ... | ... | Gradient-bottom | — |
| 2 | Hook | Image-Dominant | ... | ... | Full tint | — |
| ... |
| 7 | CTA | CTA | ... | text-only | — | — |

Subtext for each slide:
...
```

**Pack-compliance pass (required before presenting the plan):**

Before showing the plan to the user, run it against the selected pack's architecture rules. A plan that uses the pack's *colors* but ignores its *architecture* is a bad plan.

Read the chosen pack's section in `references/style-packs.md` and confirm the plan respects every architecture bullet listed there (photo treatment, slide-number treatment, ornaments, body-copy alignment, list markers, header strips, alternating-tone rhythms, hero-photo systems, etc.). Do not paraphrase the rules into this file — go read the source.

If any row in the plan violates a pack rule, fix it before the checkpoint. Do not ask the user to approve a plan that breaks pack architecture.

**Archetype check (same pass):** confirm the plan delivers the Step 0.25 archetype's structure and the CTA slide matches the archetype's outcome, per `references/content-archetypes.md`. A Vault plan with four items, or a Template plan whose CTA is just "follow me", fails this check.

**Do not write any HTML until the user says "Approved" or equivalent.**

---

### Step 4: Embed the TGW Logo

See `references/slide-architecture.md` for the progress bar markup with the logo embedded.

---

### Step 5: Generate the HTML

**Build the file in the order documented in section 3 of `references/html-implementation.md`** (doctype and head, single inline style block in its 10-part order, body with toolbar and slide sections, then the final script block).

**Pack CSS loads once.** Copy the pack's full CSS block from `references/style-packs.md` into the inline style block — do not split into a separate file and link it.

**For image slides:** prep each assigned image with Pillow first — resize AND bake the pack's photo treatment (grayscale, contrast, desaturation) into the pixels in the same pass — then base64-encode and embed as a `background-image` data URL. Gradient overlays stay CSS; anything filter-like must live in the pixels, never in a CSS `filter` (trap 6). See `references/slide-architecture.md`.

**For seamless spreads:** see `references/seamless-image-spread.md`. Use pixel-based `background-size: calc(1080px * N) 1350px` and `background-position: calc(-1080px * k) 0` so side-by-side slides reconstruct the full image. Do not use percentages for spread positioning — they silently render slide 2+ as empty.

**For long-form text slides (Editorial Long-Form pack):** reading column max 58ch wide, Barlow 400 at 36px, line-height 1.5, left-aligned ragged right. Numbered subhead in Vitesse 700 at 72pt, gold.

**Toolbar:**
- Sticky top
- Title
- Edit hint ("click any text to edit")
- `EXPORT ALL PNGs` — html2canvas loop, one file per slide, filename `{brand}-{topic}-slide-{n}.png`
- `EXPORT PDF (Canva)` — html2canvas loop into a jsPDF multi-page PDF at 1080x1350 per page, filename `{brand}-{topic}-carousel.pdf`
- Per-slide `DOWNLOAD SLIDE X`

**PDF export script:** read section 4 of `references/html-implementation.md` for the jsPDF CDN tag and the `exportPDF()` function.

**Auto-fit Mega-Cover JS:** read section 8 of `references/html-implementation.md` and copy the `autoFitMegaCover()` function plus its three call sites (`DOMContentLoaded`, `document.fonts.ready`, immediate) into the final script block VERBATIM. Do not write your own from the prose. A hand-rolled version drops the height guard and the font-load re-fit, and the cover headline overflows on any multi-line headline. The matching `.mega-cover span { white-space: nowrap; }` rule must be in the stylesheet (it ships in the Mega-Cover CSS in `references/slide-architecture.md`).

**Save Changes button:** read section 9 of `references/html-implementation.md`. Add its button HTML to the toolbar immediately after the `EXPORT PDF (Canva)` button, and add its save script verbatim immediately before the closing `</body>` tag. Copy both blocks exactly so they match the standalone patcher (`scripts/gwqueue/patch_carousels_savebtn.py`) byte-for-byte, including the `__SAVE_SCRIPT_VERSION__` marker, so freshly-generated files are treated as already-current and never re-patched.

**Persistent frame system on every slide (except where noted):**
- Slide number (`01` / `07`) — position and treatment **per pack** (see pack spec; don't use a generic default)
- Instagram handle — opposite corner, small caps Barlow 600
- Swipe arrow — bottom-right, except last slide
- TGW logo — left side of progress bar footer
- Progress bar — bottom edge, fills from 0 to 100% across slides
- **No page dots.**

---

## Inline Resize Controls

Every carousel HTML ships with inline font-size controls so Scott can adjust type during the editing pass without rewriting copy.

**What it does:** click into any editable text field. A small floating toolbar appears with `A−`, current size in px, `A+`, and `RESET`. Each click shrinks or grows by 4px. `RESET` returns to the template default. Keyboard shortcuts: `Ctrl+Up` / `Ctrl+Down` (4px step), hold `Shift` for 1px precision. For Mega-Cover, each line is a separate resize target — click the specific line, resize that line. Once a Mega-Cover line is manually sized, the auto-fit JS stops re-fitting the parent.

**What not to add:** no font-family picker, no color picker, no alignment toggle, no bold/italic. This control is intentionally narrow — it solves copy that doesn't fit the template's expected length, nothing more.

**The full implementation lives in `references/html-implementation.md`:**
- Section 5 — resize toolbar CSS (add after the existing toolbar rules in style slot 9)
- Section 6 — resize toolbar HTML (add once, immediately before the closing body tag)
- Section 7 — resize controls JavaScript (add inside the final script block, after the export functions and after `autoFitMegaCover()`)
- Section 8 — the full `autoFitMegaCover()` JS (fits width + height, re-fits on font load, and skips manually-sized covers via the guard)

---

### Step 6: Output

Save to the user's output folder as `{topic-slug}-carousel.html`. Present with a short response confirming:
- Pack chosen
- How to edit (click any text)
- How to resize text (click any editable line, then use the floating A− / A+ buttons or Ctrl+Up / Ctrl+Down; Shift adds 1px precision; on the cover headline, click the specific line to resize)
- How to export PNGs (toolbar button)
- How to export a Canva-ready PDF (toolbar button) and how to import it in Canva
- How to swap an image or tweak a slide

---

## Self-Contained File Check (run before Step 6)

The HTML file must open correctly with no internet. Before declaring done, verify:

- [ ] No external stylesheet link pointing to any file in the project (Barlow from Google Fonts is the only allowed external CSS link)
- [ ] No script tags with relative `src` paths — html2canvas and jsPDF come from CDN URLs
- [ ] The Vitesse @font-face is inside the inline style block with a base64 data URL, not a file path
- [ ] All images are embedded as base64 data URLs (no `src="./images/..."` or similar)
- [ ] The TGW logo is inline SVG or base64, not a file reference
- [ ] Opening the file by double-click (not through a dev server) renders Vitesse correctly
- [ ] The Save Changes button (`id="saveChangesBtn"`) is in the toolbar and the save script (`window.__SAVE_SCRIPT_VERSION__`) sits before `</body>`, both copied verbatim from section 9 of `references/html-implementation.md`
- [ ] If the carousel has any seamless spreads, the `background-size` and `background-position` on spread slides use **pixel values**, not percentages. Slide 1+ of every spread should visibly show the correct slice of the image, not be empty.

If any of the above is violated, the file isn't portable or correct — fix before delivering.

---

## Canva Import Flow (document this for the user)

1. Click `EXPORT PDF (Canva)` in the toolbar. Wait for the download.
2. In Canva, go to **Create a design → Import file** and drop the PDF.
3. Canva creates one page per slide. Each slide is a flat image you can layer on top of but not text-edit directly — do final text tweaks in the HTML *before* exporting PDF for cleanest results.
4. Alternative: `EXPORT ALL PNGs` gives you individual 1080x1350 files you can upload to a Canva Instagram Post template (4:5) and arrange as a carousel.

---

## Visual Brain Compliance Check

Before outputting HTML, verify:
- No drop shadows on text
- No rounded corners on slides or cards
- No emoji anywhere
- No decorative borders or flourishes
- No script/handwriting/cursive fonts
- No bullet points (use numbered steps or line breaks). Exception: Editorial Long-Form pack allows checklist items with a custom square marker.
- No strikethrough text
- No centered body copy (left-align body; center only single-line headings). Exception: any pack whose section in `references/style-packs.md` explicitly permits centered body copy.
- No light/thin font weights on headings
- Text never overlays the subject of a background image directly
- Minimum 40px safe zone margins on all edges
- On `.dark`/inverse slides, any highlighter stroke must START its line (`<br>` before the span) — a mid-line highlight's linecap overhang erases adjacent light text (see style-packs.md, Newsprint Bauhaus placement law)
- **No page dots**

---

## Content Rules

- Scott's brand voice (see Visual Brain)
- Short sentences. Active verbs. No em-dashes.
- Every changeable text element: contenteditable
- Non-editable: TGW logo, progress bars, swipe arrows, image layers, overlay divs
- Never use strikethrough
- HTML must work opened locally in Chrome/Safari (no server required)
- Best results on desktop for export

---

## Canonical Pack Definitions

`references/style-packs.md` is the canonical spec for every pack's look — colors, type, photo treatment, ornaments, architecture rules. Read the chosen pack's section at Step 0.5 and again at Step 3B (compliance pass) and Step 5 (HTML generation).

If a rendered preview HTML for a pack exists somewhere in the project and looks different from the spec, trust the spec — preview files can rot.
