---
name: carousel
description: Create editable, export-ready Instagram carousels as a single self-contained HTML file, in the buyer's own brand. Use whenever the user mentions Instagram carousel, IG carousel, social media slides, carousel post, swipeable slides, or says "make me a carousel about X", "create slides for Instagram", or references carousel templates. Produces a self-contained HTML file with click-to-edit text, one-click PNG export at 1080x1350 (4:5), a stitched multi-page PDF for Canva, a save-to-disk button, and inline font-resize. Reads the buyer's Brand Profile for palette, fonts, logo, handle, and voice. Supports buyer-authored style packs plus two shipped starters, and seamless image spreads.
---

# Carousel Engine v0.2.2

Create editable, export-ready Instagram carousels as self-contained HTML files, wearing the buyer's brand.

**Changelog:** 0.2.2, export-safety release: html2canvas (the export library) does not implement CSS `filter`, so photo treatments and logo ink now bake into the image pixels at prep time; see "Known export trap" below. 0.1.0, first white-label release. De-branded from the original GW carousel skill: identity now comes from the Brand Profile, default fonts are Roboto Slab + Barlow (free), starter packs reduced to Mono Series + Editorial Long-Form, pack authoring and Brand Setup added.

All raw markup (HTML, CSS, JS) lives in `references/html-implementation.md`. This file stays prose-only; when a step needs code, it points to a numbered section there.

---

## Brand Profile: read FIRST, every run

Before anything else, read the buyer's Brand Profile at `carousel/brand-profile.md` in the current project.

- **If it does not exist**, stop and run the **brand-setup** skill first ("Looks like you haven't set up your brand yet. Let's do that, it takes a minute"). Do not generate a carousel with placeholder identity.
- **If it exists**, load it. Everything brand-specific in this skill comes from there: `palette` (the values behind every palette role), `fonts`, `logo`, `handle`, `brand_name`, and `voice`. Never hardcode a brand value into a carousel.

The Brand Profile is the only source of identity. This engine ships with no brand of its own.

---

## What this skill produces

A single, self-contained HTML file:
- 5–10 slides at 4:5 (1080×1350 on export)
- All text fields click-to-edit (contenteditable)
- Toolbar: EXPORT ALL PNGs, EXPORT PDF (Canva), 💾 SAVE CHANGES, per-slide DOWNLOAD
- Inline resize controls (A− / A+ / RESET; Ctrl+Up / Ctrl+Down; Shift for 1px; Mega-Cover resizes per line)
- html2canvas + jsPDF from CDN (only runtime dependency)
- Fonts from Google Fonts by default, or the buyer's base64-baked custom font from the Brand Profile
- The buyer's logo (base64 from the Brand Profile) in the footer; handle text fallback if no logo
- Slide number, handle, swipe arrow (except last), progress bar. No page dots.
- Optional seamless image spreads across 2–3 slides

---

## Typography

Two families, both configurable in the Brand Profile.

- **Defaults:** Roboto Slab (display) and Barlow (body), loaded from Google Fonts. Both are free to redistribute. This is the only allowed external dependency for fonts.
- **Custom font:** if the Brand Profile sets a font's `source: baked`, embed its `custom_base64` inline as an `@font-face` data URL (no external file path). Read section 1 of `references/html-implementation.md` for the head + inline @font-face skeleton; substitute the Brand Profile's base64 where the font placeholder sits.

Banned font patterns (break silently or cache-stale): external stylesheet links to a project font file, `src: url()` to a relative font path, splitting @font-face into its own imported CSS file, omitting `font-display: block`.

Packs differ in weight, size, casing, and tracking, never family.

---

## Workflow

### Step 0: Detect mode
Image Mode if the user provides images or an image folder; otherwise Text-Only Mode (skip image cataloging steps).

### Step 0.5: Style Pack selection: HARD GATE
Do not proceed without a pack choice. Build the menu from **two sources**:
1. The shipped starters in `starter-packs/starter-packs.md` (Mono Series, Editorial Long-Form).
2. Any buyer-authored packs in `carousel/packs/*.md` in the current project.

List each pack as `N. NAME: one-line description. Good for: <use cases>`. Ask "Which one? (number or name)". If the buyer wants a look none of these cover, offer the **pack-author** skill.

After they pick, re-read that pack's section and copy its layout rules and palette-role mapping verbatim. The actual colors come from the Brand Profile's `palette`, mapped onto the pack's roles.

### Step 1: Gather inputs
Confirm topic, CTA, tone, and (Image Mode) the image folder. Brand name, handle, palette, fonts, and logo all come from the Brand Profile; do not ask for them. Ask about seamless spreads (default: none). Do not ask about fonts.

### Step 2A: Resolve the color system
Map the chosen pack's palette roles to the Brand Profile `palette` values. For the `:root` token list, read section 2 of `references/html-implementation.md`. A pack may hardcode one role only if its section declares that color as the pack's identity (escape hatch).

### Step 2B: Catalog images (Image Mode only)
For each file note filename, energy, mood, best use, and whether it is a span candidate for a seamless spread.

### Step 3A: Map slide content
Read `references/slide-architecture.md` for templates (Mega-Cover, Image-Dominant Hook, Numbered Content, Split-Image Spread, Pull Quote, Color-Block, Long-Form Text, Checklist, CTA). Cover is a phone-legible power statement; auto-fit handles length. Narrative arc, 7 slides ideal (flex 5–10).

### Step 3B: Slide plan: CHECKPOINT
Present the plan as a table. Run a **pack-compliance pass**: confirm every row respects the chosen pack's architecture rules (from its section), not just its colors. Check headlines against the pack's character budget. Fix violations before showing the plan. Do not write HTML until the user approves.

### Step 4: Logo + frame
The footer logo is the Brand Profile's `logo.base64`. If empty, show the handle text instead. If the pack mixes dark and light slides and the logo is a single-ink mark, derive the opposite-ink variant at build time (invert the RGB channels, keep alpha; one Pillow pass) and give each slide the variant that contrasts with its background. Never flip it in CSS with `filter: invert(1)`; html2canvas drops `filter` at export (see Known export trap). See `references/slide-architecture.md` for the progress-bar markup and the two-variant logo pattern.

### Step 5: Generate the HTML
Build in the order in section 3 of `references/html-implementation.md`. Copy the chosen pack's CSS into the single inline style block. Prep each assigned image first: resize AND bake the pack's photo treatment (B&W, contrast, desaturation) into the pixels in the same pass, then base64-embed. Gradient overlays stay CSS; anything filter-like lives in the pixels, never in a CSS `filter:` declaration (see Known export trap). For seamless spreads use pixel-based sizing (see `references/seamless-image-spread.md`). Copy the `autoFitMegaCover()` block from section 8 verbatim. Add the Save Changes button (section 9). The button and its save script are standalone here; there is no external patcher to match.

Frame on every slide (except where noted): slide number, handle (from Brand Profile), swipe arrow (not on last), footer logo, progress bar. No page dots.

### Step 6: Output
Save to the buyer's output folder as `{topic-slug}-carousel.html`. Confirm: pack chosen, how to edit, how to resize, how to export PNGs and a Canva PDF, how to swap an image.

---

## Self-contained file check (before Step 6)
- [ ] No external stylesheet link except Google Fonts (for default Roboto Slab + Barlow)
- [ ] html2canvas and jsPDF come from CDN URLs, not relative paths
- [ ] A custom font, if used, is inline base64 @font-face, not a file path
- [ ] All images and the logo are base64 data URLs
- [ ] Double-click opening (no dev server) renders correctly
- [ ] Save Changes button (`id="saveChangesBtn"`) is in the toolbar and the save script is before `</body>`
- [ ] Seamless spreads use pixel values for `background-size` / `background-position`, not percentages
- [ ] No `filter:` declaration anywhere inside `.slide` CSS or markup; photo treatments and logo ink are baked into the image pixels

---

## Known export trap: CSS filter

html2canvas 1.4.1 (the pinned export library) does not implement CSS `filter`. It silently drops every `filter:` declaration (invert, grayscale, contrast, all of it) at capture time. The live tab, the scaled preview, and any browser-screenshot QA render all apply filters correctly, so a filtered slide looks right everywhere you check, then EXPORT ALL PNGs, DOWNLOAD SLIDE, and EXPORT PDF ship wrong: a `filter: invert(1)` logo exports invisible, a `filter: grayscale(1)` photo exports full color. Bake every photo treatment and every logo ink variant into the source pixels at prep time (one Pillow pass, or any image tool; the pixels are the point, not the tool). No element inside `.slide` may carry `filter:`. The only way to catch a violation is to export a real PNG and look at it.

---

## Content rules (from the Brand Profile `voice`)
- Write in the buyer's voice. Honor `voice.tone`, `voice.no_em_dashes`, and `voice.banned_words`.
- Short sentences. Active verbs.
- Every changeable text element is contenteditable. Non-editable: logo, progress bars, swipe arrows, image layers, overlays.
- No drop shadows on text, no rounded corners on slides, no emoji, no decorative borders, no script fonts, no strikethrough. Bullet lists only where a pack explicitly allows them. Center only single-line headings unless a pack permits centered body. Minimum 40px safe-zone margins. No page dots.

## Canonical pack definitions
`starter-packs/starter-packs.md` is the spec for the two shipped packs. Buyer-authored packs in `carousel/packs/` follow the same shape. If a rendered preview disagrees with a pack spec, trust the spec.
