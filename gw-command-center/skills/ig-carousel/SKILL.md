---
name: ig-carousel
description: Create editable, export-ready Instagram carousel slides as a single HTML file. Use this skill whenever the user mentions Instagram carousel, IG carousel, social media slides, carousel post, swipeable slides, or wants to create visual slide content for Instagram. Also trigger when the user says "make me a carousel about X", "create slides for Instagram", "social media graphics", or references carousel templates. This skill produces a self-contained HTML file with click-to-edit text fields, one-click PNG export at 1080×1350 (Instagram 4:5 ratio), and a stitched multi-page PDF export for Canva import. Supports 6 distinct visual style packs selected at Step 0.5, plus seamless image spreads across multiple slides.
---

# Instagram Carousel Skill — v3.1

Create editable, export-ready Instagram carousels as self-contained HTML files.

**What's new in v3.1 (bug fix):**
- **Spread positioning fixed.** Seamless image spreads now use pixel-based `background-size` and `background-position`. The previous percentage-based formula silently rendered slide 2+ of a spread as empty. If you have any v3 carousels with spreads, open them and check. See `references/seamless-image-spread.md` for the corrected formula.

**What's new in v3 (changes from v2):**
- Step 0.5 (style pack selection) is now hard-gated — no HTML until a pack is chosen.
- Vitesse embedding is locked to **inline `<style>` only**. External stylesheets for fonts are banned (they cache-stale and render the wrong font).
- New **pack-compliance pass** at the end of Step 3B — the slide plan must respect the chosen pack's architecture rules (reading columns, centered body allowances, photo sizing), not just its colors.
- Each carousel HTML file is **self-contained**. No shared CSS files, no external pack stylesheets, no imports beyond Barlow from Google Fonts. If it doesn't open correctly from a USB drive with no internet, it's broken.
- Canonical visual references for each pack live in the project as `Carousel Test - <Pack Name>.html`. Read them when authoring slides to pattern-match the pack's feel.

---

## Visual Brain Reference

**Before building any carousel, read `GW_Visual_Brain.md` in the project knowledge files.** That document is the canonical source for the core brand identity (Vitesse + Barlow type, gold accent, asphalt/paper palette, negative constraints). This skill inherits all of those rules.

**Style Packs vs Visual Brain:** Style packs (Step 0.5) adjust *how* Visual Brain rules are applied — background-dominant color, accent hue, overlay strength, slide-number treatment — but never violate core constraints unless explicitly listed below. If a pack appears to conflict with the Visual Brain and the conflict is not in the Authorized Overrides list, the Visual Brain wins.

### Authorized Overrides (approved by Scott)

Three specific exceptions to Visual Brain rules are allowed inside this skill. These are scoped, not global — they apply only to the packs named. Every other pack and every other skill must follow the Visual Brain verbatim.

| Rule in Visual Brain | Pack allowed to override | Why |
|---|---|---|
| "Gold is the only accent color. No secondary colors." | **Acid Block** may replace gold with cherry red (#FF2E3C). | Bold-statement / attention-grabber carousels where the point is visual jolt. Gold and cherry red never appear on the same slide. |
| "Never center-align body copy." | **Dark Project** may center body copy (max 3 lines). | Cinematic manifesto feel for challenge/transformation posts. |
| "Maximum 25 words per slide." | **Editorial Long-Form** may exceed 25 words on content slides. | Built for teaching/how-to content where the point is reading, not skimming. Cover and CTA still respect the cap. |

### Type Scale — 1080×1350 canvas

The Visual Brain type scale (36px hero, 28px section head, 14px body) is a web/UI scale. Carousel slides render on a 1080px-wide canvas, so those sizes scale up proportionally to maintain intended display sizes in-feed. Pack-specific sizes (e.g., Mega-Cover at 180–240px) are correct for the 1080×1350 canvas and compress back to the Visual Brain's intended feel when Instagram displays the slide in-feed.

---

## What This Skill Produces

A single, self-contained HTML file containing:
- 5–10 slides at 4:5 aspect ratio (1080×1350 on export)
- All text fields click-to-edit (contenteditable)
- **Toolbar:** "EXPORT ALL PNGs" + "EXPORT PDF (Canva)" + per-slide "DOWNLOAD"
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

Vitesse Bold ships inside the HTML file as a base64 data URL in an inline `<style>` block. Barlow loads from Google Fonts.

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>...</title>
<link href="https://fonts.googleapis.com/css2?family=Barlow:wght@400;600;700;900&display=swap" rel="stylesheet">
<style>
  @font-face {
    font-family: 'Vitesse';
    src: url('data:font/otf;base64,{VITESSE_BASE64}') format('opentype');
    font-weight: 700;
    font-style: normal;
    font-display: block;
  }

  :root {
    --font-heading: 'Vitesse', 'Georgia', serif;
    --font-body: 'Barlow', sans-serif;
    /* pack tokens go here — see Step 2A */
  }

  /* rest of stylesheet */
</style>
</head>
```

Read the full base64 string from `assets/vitesse-bold-base64.txt` and paste it where `{VITESSE_BASE64}` sits.

**Banned patterns (these will break silently or cache-stale):**
- External `<link rel="stylesheet">` pointing to a shared pack file that contains the @font-face
- Referencing `assets/Vitesse-Bold.otf` as a `src: url()` path (won't resolve when the user opens the file elsewhere)
- Splitting the @font-face into its own .css file and `@import`-ing it
- Omitting `font-display: block` (causes a paint flash of Archivo Black before Vitesse loads)

**Why inline-only:** the HTML is meant to be portable. A user may open it from Desktop, from a Canva import staging folder, from a USB drive, or a colleague's laptop. External CSS files break any of those. Inline @font-face makes the file a true single-file artifact.

Every style pack uses the same two families. Packs differ in weight, size, casing, and tracking — not family.

---

## Workflow

### Step 0: Detect Mode

Check whether the user has provided images or references an image folder.

- **Image Mode** — user mentions images, a folder path, or you find images at `Gridiron Warrior/Images/carousels/`. Run all steps.
- **Text-Only Mode** — no images provided. Skip Steps 2B and 3B.

---

### Step 0.5: Style Pack Selection — HARD GATE

**Do not proceed past this step without a pack choice.** No color derivation, no slide planning, no HTML. The pack shapes every downstream decision.

Present this exact menu:

```
Pick a style pack for this carousel:

1. ASPHALT EDITORIAL — moody B&W photos, heavy dark overlays, gold accent.
   Good for: mindset, grit, long-form training content.

2. HIGH CONTRAST HYPE — sports collage energy. B&W subject cutouts, bold gold slashes, duotone backgrounds.
   Good for: player features, hype posts, game-day content.

3. ACID BLOCK — off-black + paper + electric cherry red accent. Color blocks behind individual words.
   Good for: bold statements, contrarian takes, attention-grabbers. (Replaces gold with cherry red.)

4. PAPER MINIMAL — paper-dominant, asphalt type, small supporting photos, lots of negative space.
   Good for: editorial pieces, philosophy, quiet confidence.

5. DARK PROJECT — near-black slides, smaller centered type, photos as texture. Cinematic.
   Good for: challenges, programs, transformation narratives.

6. EDITORIAL LONG-FORM — paper background, asphalt body copy in real reading columns, numbered subheads.
   Good for: teaching, how-to, text-heavy educational posts.

Which one? (number or name)
```

**After the user picks:**
1. Load the pack definition from `references/style-packs.md` — this is canonical. Copy its `:root` tokens and CSS guidance verbatim; do not improvise pack values.
2. Open the matching `Carousel Test - <Pack Name>.html` in the project root as a **visual reference**. Read it to understand how the pack's slides actually look — slide-number treatment, type sizes, photo handling, spacing. Pattern-match against this reference during Step 5 (HTML generation).
3. Note the pack's architecture rules for the compliance pass at Step 3B.

---

### Step 1: Gather Inputs

Check conversation history first. Confirm any missing:

1. **Topic** — what the carousel teaches or promotes
2. **Brand name** — default: Gridiron Warrior
3. **Instagram handle** — default: @Sleech72
4. **Accent color override** *(optional)* — each pack has a locked default; only override if the user explicitly asks
5. **Tone** — coach-tough, professional, playful, minimal
6. **CTA** — follow, link in bio, DM, etc.
7. **Image folder** *(Image Mode only)* — default: `Gridiron Warrior/Images/carousels/`
8. **Seamless spreads?** — ask: "Want any photos to span multiple slides for a swipe-reveal effect? e.g., 'slide 3–4' or 'slide 2–3–4'." Default: none.

Do not ask about fonts.

---

### Step 2A: Derive the Color System

Pull the base tokens from the selected style pack. All packs share the same structural tokens, only their values shift:

```css
:root {
  --bg-dominant:    /* per pack */;
  --bg-inverse:     /* per pack */;
  --fg-dominant:    /* per pack */;
  --fg-inverse:     /* per pack */;
  --accent:         /* per pack — gold default, cherry red for Acid Block */;
  --accent-ink:     /* contrast color to read ON the accent */;
  --overlay-dark:   /* tune per pack — see style-packs.md */;
  --edit-highlight: var(--accent);
}
```

Exact values live in `references/style-packs.md`. Copy them, don't improvise.

---

### Step 2B: Catalog the Images (Image Mode only)

Same as v1/v2. For each file, note filename, energy level (High/Low), mood, best use. Column for v2+: `span-candidate` — is this photo wide enough / composed well enough to work as a seamless multi-slide spread? (Generally: full-body shots, wide landscapes, horizontal action. Not: tight headshots.)

---

### Step 3A: Map Slide Content

Read `references/slide-architecture.md` for the full template structure and component library.

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

**Cover headline rule:** the cover is a phone-legible power statement. Write whatever length you want — the skill auto-fits the type to the safe zone. If auto-fit drops the size below 80pt (at 1080×1350), stop and recommend trimming. Powerful > short.

**Narrative arc (7 slides ideal, flex 5–10):** Cover → Hook → Build → Turn → Payoff → Reinforce → CTA. Light/dark rhythm still applies within the pack's dominant palette.

---

### Step 3B: Generate the Slide Plan — CHECKPOINT

```
SLIDE PLAN — [Topic] Carousel — [Style Pack]

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

| Pack | Must respect |
|---|---|
| Asphalt Editorial | B&W photo treatment; gold hairline above headline on image slides |
| High Contrast Hype | Diagonal gold slash element present on every non-cover slide; oversized ghosted slide number behind content |
| Acid Block | Alternating asphalt/paper/cherry-red slide rhythm — never two cherry-red slides adjacent; cherry-red circle stamp for slide number |
| Paper Minimal | Photos are **small contained rectangles**, not full-bleed. ~60–70% slide width, left-aligned. No ornament. |
| Dark Project | Cover type smaller than other packs (~96pt). Centered body allowed (max 3 lines). Photos as dark texture only. |
| Editorial Long-Form | Reading-column layout on content slides (max 58ch). Numbered subheads in gold Vitesse 700. Folio-style slide number ("Page 3 / 8"). |

If any row in the plan violates these rules, fix it before the checkpoint. Do not ask the user to approve a plan that breaks pack architecture.

**Do not write any HTML until the user says "Approved" or equivalent.**

---

### Step 4: Embed the TGW Logo

See `references/slide-architecture.md` for the progress bar HTML with logo embedded.

---

### Step 5: Generate the HTML

**File structure (top to bottom):**

1. `<!DOCTYPE html>` + `<head>` with:
   - `<meta charset="UTF-8">`
   - `<meta name="viewport" content="width=1080">`
   - `<title>` — `{Topic} — {Pack Name} — Gridiron Warrior`
   - Barlow `<link>` from Google Fonts (weights 400, 600, 700, 900)
   - **One** inline `<style>` block containing, in order:
     1. @font-face for Vitesse (base64 data URL)
     2. Reset + box-sizing
     3. `:root` pack tokens
     4. Typography base (`body`, `h1`–`h3`, paragraph defaults)
     5. Slide frame (`.slide` at 1080×1350, scaled down for preview)
     6. Persistent frame system (slide number, handle, swipe arrow, progress bar, logo)
     7. Template classes (Mega-Cover, Numbered Content, Long-Form Text, etc. — only the ones used)
     8. Pack-specific overrides (see `references/style-packs.md` for each pack's CSS block)
     9. Toolbar styles, then the inline resize toolbar CSS (see **Inline Resize Controls** below)
     10. Edit highlight states (`[contenteditable]:hover`, `[contenteditable]:focus`)
   - html2canvas + jsPDF CDN `<script>` tags
2. `<body>`:
   - Toolbar at top (fixed)
   - `<section class="slide">` for each slide, in order
   - Resize toolbar element (`<div id="resize-toolbar">`) immediately before `</body>` (see **Inline Resize Controls** below)
   - Export / edit JS, then the Inline Resize Controls JS block, as the final inline `<script>` block

**Pack CSS loads once.** Copy the pack's full CSS block from `references/style-packs.md` into the inline `<style>` — do not split into a separate file and link it.

**For image slides:** base64-encode each assigned image, embed as `background-image: url('data:image/...;base64,...')`, apply the pack's photo treatment (grayscale filter, overlay gradient, etc.). See `references/slide-architecture.md`.

**For seamless spreads:** see `references/seamless-image-spread.md`. Use pixel-based `background-size: calc(1080px * N) 1350px` and `background-position: calc(-1080px * k) 0` so side-by-side slides reconstruct the full image. Do not use percentages for spread positioning — they silently render slide 2+ as empty.

**For long-form text slides (Editorial Long-Form pack):** reading column max 58ch wide, Barlow 400 at 36px, line-height 1.5, left-aligned ragged right. Numbered subhead in Vitesse 700 at 72pt, gold.

**Toolbar:**
- Sticky top
- Title
- Edit hint ("click any text to edit")
- `EXPORT ALL PNGs` → html2canvas loop, one file per slide, filename `{brand}-{topic}-slide-{n}.png`
- `EXPORT PDF (Canva)` → html2canvas loop → jsPDF multi-page PDF at 1080×1350 per page, filename `{brand}-{topic}-carousel.pdf`
- Per-slide `DOWNLOAD SLIDE X`

**PDF export snippet:**

```html
<script src="https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js"></script>
<script>
async function exportPDF() {
  const { jsPDF } = window.jspdf;
  const pdf = new jsPDF({ unit: 'px', format: [1080, 1350], orientation: 'portrait' });
  const slides = document.querySelectorAll('.slide');
  for (let i = 0; i < slides.length; i++) {
    const canvas = await html2canvas(slides[i], { scale: 1080 / slides[i].offsetWidth });
    const img = canvas.toDataURL('image/png');
    if (i > 0) pdf.addPage([1080, 1350], 'portrait');
    pdf.addImage(img, 'PNG', 0, 0, 1080, 1350);
  }
  pdf.save(`${BRAND_SLUG}-${TOPIC_SLUG}-carousel.pdf`);
}
</script>
```

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

**What it does:** click into any editable text field. A small floating toolbar appears with `A−`, current size in px, `A+`, and `RESET`. Each click shrinks or grows by 4px. `RESET` returns to the template default. Keyboard shortcuts: `Ctrl+Up` / `Ctrl+Down` (4px step), hold `Shift` for 1px precision. For Mega-Cover, each line `<span>` is a separate resize target — click the specific line, resize that line. Once a Mega-Cover line is manually sized, the auto-fit JS stops re-fitting the parent.

**What not to add:** no font-family picker, no color picker, no alignment toggle, no bold/italic. This control is intentionally narrow — it solves copy that doesn't fit the template's expected length, nothing more.

### CSS — add after existing toolbar rules in slot 9

```css
.resize-toolbar {
  position: absolute;
  display: none;
  align-items: center;
  gap: 6px;
  background: #1A1A1A;
  border: 1px solid rgba(245, 240, 232, 0.25);
  padding: 6px 8px;
  z-index: 9999;
  font-family: var(--font-body);
  box-shadow: 0 4px 24px rgba(0, 0, 0, 0.55);
  user-select: none;
}
.resize-toolbar.active { display: flex; }
.resize-toolbar .resize-label {
  color: rgba(245, 240, 232, 0.45);
  font-size: 10px;
  letter-spacing: 1.5px;
  text-transform: uppercase;
  font-weight: 700;
  border-right: 1px solid rgba(245, 240, 232, 0.18);
  padding-right: 8px;
  margin-right: 2px;
}
.resize-toolbar button {
  background: transparent;
  border: 1px solid rgba(245, 240, 232, 0.3);
  color: #F5F0E8;
  font-family: var(--font-body);
  font-weight: 700;
  padding: 4px 10px;
  cursor: pointer;
  font-size: 14px;
  letter-spacing: 0.5px;
}
.resize-toolbar button:hover {
  background: rgba(245, 240, 232, 0.12);
  border-color: var(--accent);
  color: var(--accent);
}
.resize-toolbar .size-display {
  color: rgba(245, 240, 232, 0.7);
  font-size: 11px;
  letter-spacing: 1px;
  font-weight: 600;
  min-width: 56px;
  text-align: center;
  font-variant-numeric: tabular-nums;
}
.mega-cover[data-manual-size="true"] { /* state marker only */ }
```

For Paper Minimal and Editorial Long-Form (paper-dominant packs), the toolbar's dark theme still works — do not invert it per pack.

### HTML — add once, immediately before `</body>`

```html
<div class="resize-toolbar" id="resize-toolbar" role="toolbar" aria-label="Text size">
  <span class="resize-label">SIZE</span>
  <button data-resize="-4" title="Shrink (Ctrl+Down)">A−</button>
  <span class="size-display" id="resize-size">--px</span>
  <button data-resize="+4" title="Grow (Ctrl+Up)">A+</button>
  <button data-resize="reset" title="Reset to template default">RESET</button>
</div>
```

### JavaScript — add inside the final `<script>` block, after the export functions and after `autoFitMegaCover()`

```javascript
// =====================================================================
// Inline Resize Controls
// =====================================================================
(function () {
  const toolbar = document.getElementById('resize-toolbar');
  const sizeDisplay = document.getElementById('resize-size');
  const MIN_SIZE = 12;
  const MAX_SIZE = 400;
  let target = null;

  function isMegaSpan(el) {
    return el && el.matches && el.matches('.mega-cover > span');
  }

  function isEditable(el) {
    if (!el || !el.hasAttribute) return false;
    return el.hasAttribute('contenteditable') &&
           el.getAttribute('contenteditable') !== 'false';
  }

  function eligible(el) {
    return isMegaSpan(el) || (isEditable(el) && !el.classList.contains('mega-cover'));
  }

  function currentSize(el) {
    return parseFloat(getComputedStyle(el).fontSize);
  }

  function applySize(el, newPx) {
    const clamped = Math.max(MIN_SIZE, Math.min(MAX_SIZE, newPx));
    el.style.fontSize = clamped + 'px';
    el.dataset.manualSize = 'true';
    const mega = el.closest('.mega-cover');
    if (mega) mega.dataset.manualSize = 'true';
    refreshDisplay();
  }

  function resetSize(el) {
    el.style.fontSize = '';
    delete el.dataset.manualSize;
    refreshDisplay();
  }

  function refreshDisplay() {
    sizeDisplay.textContent = target
      ? Math.round(currentSize(target)) + 'px'
      : '--px';
  }

  function positionToolbar() {
    if (!target) return;
    const rect = target.getBoundingClientRect();
    const tbRect = toolbar.getBoundingClientRect();
    const tbHeight = tbRect.height || 36;
    let top = window.scrollY + rect.top - tbHeight - 8;
    let left = window.scrollX + rect.left;
    if (rect.top - tbHeight - 8 < 0) {
      top = window.scrollY + rect.bottom + 8;
    }
    const maxLeft = window.scrollX + document.documentElement.clientWidth - tbRect.width - 8;
    if (left > maxLeft) left = maxLeft;
    if (left < window.scrollX + 8) left = window.scrollX + 8;
    toolbar.style.top = top + 'px';
    toolbar.style.left = left + 'px';
  }

  function showFor(el) {
    target = el;
    toolbar.classList.add('active');
    toolbar.offsetHeight; // force layout so getBoundingClientRect on toolbar is correct
    positionToolbar();
    refreshDisplay();
  }

  function hide() {
    target = null;
    toolbar.classList.remove('active');
    refreshDisplay();
  }

  document.addEventListener('click', (e) => {
    if (toolbar.contains(e.target)) return;
    const span = e.target.closest && e.target.closest('.mega-cover > span');
    if (span) { showFor(span); return; }
    if (eligible(e.target)) { showFor(e.target); return; }
    if (target && !target.contains(e.target)) hide();
  });

  toolbar.addEventListener('mousedown', (e) => e.preventDefault());
  toolbar.addEventListener('click', (e) => {
    if (!target) return;
    const btn = e.target.closest('button');
    if (!btn) return;
    const action = btn.dataset.resize;
    if (action === 'reset') {
      resetSize(target);
    } else {
      const delta = parseInt(action, 10);
      applySize(target, currentSize(target) + delta);
    }
    positionToolbar();
  });

  document.addEventListener('keydown', (e) => {
    if (!target) return;
    if (!(e.ctrlKey || e.metaKey)) return;
    if (e.key !== 'ArrowUp' && e.key !== 'ArrowDown') return;
    e.preventDefault();
    const step = e.shiftKey ? 1 : 4;
    const delta = e.key === 'ArrowUp' ? step : -step;
    applySize(target, currentSize(target) + delta);
    positionToolbar();
  });

  window.addEventListener('scroll', positionToolbar, true);
  window.addEventListener('resize', positionToolbar);
})();
```

### Auto-fit guard — add at the top of `autoFitMegaCover()`'s forEach callback

```javascript
document.querySelectorAll('.mega-cover').forEach((el) => {
  if (el.dataset.manualSize === 'true') return;   // skip manually-sized covers
  // ... existing auto-fit logic
});
```

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

- [ ] No `<link rel="stylesheet">` pointing to any file in the project (Barlow from Google Fonts is the only allowed external CSS link)
- [ ] No `<script src="./...">` or relative script paths — html2canvas and jsPDF come from CDN URLs
- [ ] `@font-face` for Vitesse is inside the inline `<style>` block with a base64 data URL, not a file path
- [ ] All images are embedded as base64 data URLs (no `src="./images/..."` or similar)
- [ ] The TGW logo is inline SVG or base64, not a file reference
- [ ] Opening the file by double-click (not through a dev server) renders Vitesse correctly
- [ ] If the carousel has any seamless spreads, the `background-size` and `background-position` on spread slides use **pixel values**, not percentages. Slide 1+ of every spread should visibly show the correct slice of the image, not be empty.

If any of the above is violated, the file isn't portable or correct — fix before delivering.

---

## Canva Import Flow (document this for the user)

1. Click `EXPORT PDF (Canva)` in the toolbar. Wait for the download.
2. In Canva, go to **Create a design → Import file** and drop the PDF.
3. Canva creates one page per slide. Each slide is a flat image you can layer on top of but not text-edit directly — do final text tweaks in the HTML *before* exporting PDF for cleanest results.
4. Alternative: `EXPORT ALL PNGs` gives you individual 1080×1350 files you can upload to a Canva Instagram Post template (4:5) and arrange as a carousel.

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
- No centered body copy (left-align body; center only single-line headings). Exception: Dark Project.
- No light/thin font weights on headings
- Text never overlays the subject of a background image directly
- Minimum 40px safe zone margins on all edges
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

## Canonical Visual References

These files live in the project root and are the ground truth for each pack's final look. Read the matching file at Step 0.5 and pattern-match during Step 5:

- `Carousel Test - Asphalt Editorial.html`
- `Carousel Test - High Contrast Hype.html`
- `Carousel Test - Acid Block.html`
- `Carousel Test - Paper Minimal.html`
- `Carousel Test - Dark Project.html`
- `Carousel Test - Editorial Long-Form.html`

`Carousel Pack Index.html` links all six for side-by-side comparison.

If a pack preview file is missing or looks different from its spec in `references/style-packs.md`, trust the spec and note the discrepancy — don't silently copy a broken preview.
