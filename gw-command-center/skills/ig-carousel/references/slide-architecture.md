# Slide Architecture — Instagram Carousel Skill v2

Shared HTML structure, component patterns, and template definitions. Style packs (see `style-packs.md`) override tokens but not structure.

---

## Slide sizing — CANONICAL PATTERN (copy verbatim, do not improvise)

Every slide renders at native **1080×1350px**. The browser displays it at preview size by scaling the slide element; html2canvas captures at native size by clearing the scale transform on capture.

**Why this section exists:** earlier versions of the skill let each run write its own scaling math. Two failure modes kept appearing:
- `position: absolute; inset: 0` on `.slide` — the `inset` shorthand overrides `width/height`, so the slide collapses to the wrap size and everything inside breaks.
- `transform: scale(calc(720px / 1080))` — `scale()` requires a unitless number, not a pixel ratio. The transform silently fails to apply.

The pattern below is the only one that ships. Don't substitute.

```css
.slide-wrap {
  width: min(720px, 90vw);
  aspect-ratio: 1080 / 1350;
  position: relative;
  overflow: hidden;
}

.slide {
  position: absolute;
  top: 0;
  left: 0;
  width: 1080px;
  height: 1350px;
  transform-origin: top left;
  transform: scale(var(--slide-scale, 0.6667));
  overflow: hidden;
  background: var(--bg-dominant);
}
```

Set `--slide-scale` from JS so it stays responsive when the viewport changes:

```javascript
function updateSlideScale() {
  const wrap = document.querySelector('.slide-wrap');
  if (!wrap) return;
  const w = wrap.getBoundingClientRect().width;
  document.documentElement.style.setProperty('--slide-scale', String(w / 1080));
}
updateSlideScale();
window.addEventListener('resize', updateSlideScale);
```

In the html2canvas capture function, clear the transform before capture and restore it after:

```javascript
async function captureSlide(slideEl) {
  const prev = slideEl.style.transform;
  slideEl.style.transform = 'none';
  try {
    return await html2canvas(slideEl, {
      width: 1080, height: 1350,
      windowWidth: 1080, windowHeight: 1350,
      scale: 1, useCORS: true, backgroundColor: null, logging: false
    });
  } finally {
    slideEl.style.transform = prev;
  }
}
```

This combination is tested and works. If you find yourself reaching for `inset: 0`, `calc()` inside `scale()`, or a non-unitless scale factor — stop, come back to this section, copy what's here.

---

## Slide shell (every slide)

```html
<div class="slide" data-slide-index="N" data-total="T">
  <!-- optional image or span layer -->
  <div class="image-layer" style="background-image: url(...); background-size: cover; background-position: center;"></div>

  <!-- overlay for legibility -->
  <div class="overlay"></div>

  <!-- ghosted oversized slide number (some packs) -->
  <div class="slide-number-ghost">02</div>

  <!-- primary content -->
  <div class="content">
    <div class="eyebrow" contenteditable="true">EYEBROW</div>
    <h1 class="headline" contenteditable="true">Headline</h1>
    <p class="body" contenteditable="true">Body copy.</p>
  </div>

  <!-- persistent frame -->
  <div class="handle-stamp">@Sleech72</div>
  <div class="slide-number-stamp">01 / 07</div>
  <div class="swipe-arrow">→</div>

  <!-- progress bar + logo -->
  <div class="progress-bar">
    <img class="tgw-logo" src="data:image/png;base64,{TGW}" alt="">
    <div class="progress-track"><div class="progress-fill" style="width: calc(100% * N / T);"></div></div>
    <div class="progress-count">N / T</div>
  </div>
</div>
```

Hide `.slide-number-ghost` by default; individual pack CSS un-hides it. Mono Series uses its own `.mono-ghost-num` element with different positioning rules — see the pack spec.

Hide `.slide-number-stamp` where the pack uses the ghost version instead, OR where the pack strips the stamp entirely (The Case removes slide-number-stamp, swipe-arrow, and handle-stamp on inner slides).

Last slide: hide `.swipe-arrow`, fill progress to 100%.

**Handle-stamp clearance law (every pack that keeps the stamp):** the `.handle-stamp` box occupies roughly x=868–1016, y=56–85 (top:56, right:64, ~148px wide). Any text element whose FIRST rendered line can start above y=100 MUST carry `max-width: 800px` (or equivalent right clearance) so that line cannot run under the stamp. This bit for real on Editorial Long-Form's `.subhead` (stop-maxing-out-60-kids build, 2026-07-28): the reference example's subhead phrases were coincidentally short, longer first lines collided with `@Sleech72` on 5 of 5 content slides. The Case is immune (it strips the stamp on inner slides), Newsprint Bauhaus clears it structurally (kicker chip pushes headlines below the band), and Mono Series is exempt by construction (no `.handle-stamp` at all — its handle lives in the flow-layout `.header-strip`, which pushes all content below the band); every pack that DOES keep the absolute-positioned stamp follows the law. Mega-covers are NOT exempt: `autoFitMegaCover()` fits to the full 952px safe width with no reservation for the stamp corner, so a short 2-line cover headline can auto-fit large enough to run under the stamp — push the block below the band with `margin-top:56px` on `.mega-cover` (october-shrinking build, 2026-07-28) rather than shrinking the fit width.

---

## Templates

### Mega-Cover
Stacked headline, auto-fit to safe zone. Each line is a `<span>` inside the `<h1>`. Default cover for all packs.

```html
<h1 class="headline mega-cover">
  <span>YOUR</span>
  <span>POWER</span>
  <span>STATEMENT</span>
</h1>
```

```css
.mega-cover {
  font-family: var(--font-heading);
  font-weight: 700;
  line-height: 0.88;
  letter-spacing: -0.02em;
  text-transform: uppercase;
  display: flex;
  flex-direction: column;
  /* font-size set by auto-fit JS — starts at 220pt, shrinks until fits */
}
.mega-cover span { display: block; white-space: nowrap; }
```

`white-space: nowrap` on the span is load-bearing, not cosmetic. Without it a multi-word line (e.g. `ONE TICKET.`) wraps internally and `scrollWidth` then reports the *wrapped* (narrower) width, which hides the real overflow from the fit loop and the cover renders too big.

Auto-fit JS: copy the `autoFitMegaCover()` function and its call sites verbatim from section 8 of `references/html-implementation.md`. Do not re-derive it from this description. It shrinks `font-size` on each `.mega-cover` from 220px down until BOTH (a) every child `<span>` fits the horizontal safe zone (`scrollWidth <= 1080 - 128`) AND (b) the whole cover fits the vertical space left inside `.slide-content` (`scrollHeight <= availH`). It re-runs on `document.fonts.ready` because the real Vitesse glyphs are wider than the fallback font and otherwise leave the cover oversized after the swap. Minimum size 80px. Below that it stops shrinking (the skill narrative already told the user at Step 3 to trim). A width-only fit (no height guard) is the historical bug: multi-line headlines clip the top word and collide with the footer.

### Image-Dominant Hook
Full-bleed photo, headline in corner (bottom-left default). Uses `overlay` at 60% opacity bottom gradient.

### Numbered Content
Ghosted oversized slide number in background. Headline + body in foreground.

### Split-Image Spread
See `seamless-image-spread.md`. Two or three adjacent slides share an image via `background-size` + `background-position` math.

### Highlighted-Word Paragraph
Body copy with specific words wrapped in `<span class="hl">` for the accent-block effect (Acid Block) OR the gold underline effect (The Case).

```html
<p class="body">The best time to start was <span class="hl">yesterday</span>. The second best time is <span class="hl">today</span>.</p>
```

```css
/* Default (Acid Block style — solid block behind word) */
.hl {
  background: var(--accent);
  color: var(--accent-ink);
  padding: 0.05em 0.25em;
}

/* The Case override — color shift + underline, no block */
.pack--case .hl {
  background: transparent;
  color: var(--accent);
  border-bottom: 6px solid var(--accent);
  padding-bottom: 8px;
  padding-left: 0;
  padding-right: 0;
}
```

### Pull Quote
Large display-font quote, attribution below in Barlow small caps. Quote marks are a separate `::before` element in Vitesse at 2x the quote size.

### Color-Block Statement
Solid accent background, huge contrast text. No photo. Used sparingly — max one per carousel.

### Long-Form Text
Reading column, numbered subhead. Editorial Long-Form pack leans on this. `.subhead` MUST carry `max-width: 800px` — its first line starts inside the handle-stamp band (see the clearance law in the Persistent frame section).

```html
<div class="content long-form">
  <div class="subhead"><span class="num">03.</span> How to train hard without breaking</div>
  <hr class="hairline">
  <p class="body-column">Paragraph of ~40 words. Left-aligned. Ragged right. Max 58ch.</p>
</div>
```

### Checklist
Editorial Long-Form only. Items use a square outline marker instead of a bullet.

### CTA / Follow
Last slide. No swipe arrow. Handle prominent. Clear instruction ("Follow @Sleech72 for more.").

Comment-trigger variant (default for The Template archetype, available to any): "Comment WORD and I'll send you X." Rules in `content-archetypes.md`: the asset must exist, the trigger word is one uppercase easy word, and fulfillment is manual by design.

---

## The Case — Pack-specific components

These components are scoped to **The Case** pack only. Do not use them in other packs.

### Hero Photo Layer
Every slide in a Case carousel uses the SAME photo as full-bleed background. Photo is base64-embedded once at the top of the inline style block and referenced by every `.slide` in the carousel.

```css
:root {
  --hero-photo: url('data:image/jpeg;base64,{HERO_PHOTO_BASE64}');
}

.pack--case .slide::before {
  content: "";
  position: absolute;
  inset: 0;
  background-image: var(--hero-photo);
  background-size: cover;
  background-position: center;
  filter: saturate(0.65) contrast(1.05) brightness(0.92);
  z-index: 0;
}
```

### Scanline Overlay
A repeating 2px horizontal scanline pattern at low opacity. Sits over the photo and under the dark gradient. Lifts the photo into a "training film" texture.

```html
<div class="scanlines"></div>
```

```css
.pack--case .scanlines {
  position: absolute;
  inset: 0;
  background: repeating-linear-gradient(
    to bottom,
    transparent 0px,
    transparent 2px,
    rgba(255, 255, 255, 0.04) 2px,
    rgba(255, 255, 255, 0.04) 3px
  );
  mix-blend-mode: overlay;
  pointer-events: none;
  z-index: 1;
}
```

### Dark Gradient Overlay
A two-stop dark gradient that sits above the scanlines and the photo to keep headline copy legible.

```css
.pack--case .photo-overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(180deg, rgba(0,0,0,0.55) 0%, rgba(0,0,0,0.88) 100%);
  pointer-events: none;
  z-index: 2;
}
```

### Section Tag
Filled gold rectangle at top-left of each content slide. Holds a freeform uppercase label.

```html
<div class="section-tag" contenteditable="true">THE PROBLEM</div>
```

```css
.pack--case .section-tag {
  position: absolute;
  top: 88px;
  left: 64px;
  background: var(--accent);
  color: #FFFFFF;
  padding: 12px 24px;
  font-family: var(--font-body);
  font-weight: 700;
  font-size: 22px;
  letter-spacing: 3px;
  text-transform: uppercase;
  z-index: 4;
}
```

### Priority Callout Banner (optional)
Translucent gold-tinted rectangle with a thick gold left border, a hash-number stamp on the left, and a one-line priority statement on the right. Use sparingly — max once per carousel.

```html
<div class="priority-banner">
  <span class="hash-stamp">#1</span>
  <span class="stamp-body">Priority at this age: Relative Strength, not max load.</span>
</div>
```

```css
.pack--case .priority-banner {
  background: rgba(200, 168, 78, 0.20);
  border-left: 4px solid var(--accent);
  padding: 20px 28px;
  display: flex;
  align-items: center;
  gap: 24px;
  z-index: 4;
  position: relative;
}
.pack--case .priority-banner .hash-stamp {
  font-family: var(--font-heading);
  font-weight: 700;
  font-size: 56px;
  color: var(--accent);
  line-height: 1;
  flex-shrink: 0;
}
.pack--case .priority-banner .stamp-body {
  font-family: var(--font-body);
  font-weight: 500;
  font-size: 22px;
  color: #FFFFFF;
  line-height: 1.3;
}
```

### Circle-Badge Numbered List (optional)
Vertical list where each item leads with a 64px circular gold-outlined badge. Use for slides that summarize multiple pillars, steps, or principles.

```html
<ul class="case-list">
  <li>
    <span class="badge">1</span>
    <div>
      <div class="item-subhead">Movement Quality</div>
      <div class="item-body">Master the pattern before you load it. Always.</div>
    </div>
  </li>
  <li>
    <span class="badge">2</span>
    <div>
      <div class="item-subhead">Relative Strength</div>
      <div class="item-body">How strong you are relative to bodyweight matters most.</div>
    </div>
  </li>
</ul>
```

```css
.pack--case .case-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 24px;
  position: relative;
  z-index: 4;
}
.pack--case .case-list li {
  display: flex;
  gap: 28px;
  align-items: flex-start;
}
.pack--case .case-list .badge {
  flex-shrink: 0;
  width: 64px;
  height: 64px;
  border-radius: 50%;
  border: 3px solid var(--accent);
  background: transparent;
  color: var(--accent);
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: var(--font-body);
  font-weight: 700;
  font-size: 28px;
}
.pack--case .case-list .item-subhead {
  font-family: var(--font-heading);
  font-weight: 700;
  font-size: 32px;
  color: #FFFFFF;
  margin-bottom: 4px;
  text-transform: uppercase;
  letter-spacing: -0.01em;
}
.pack--case .case-list .item-body {
  font-family: var(--font-body);
  font-weight: 400;
  font-size: 24px;
  color: #FFFFFF;
  opacity: 0.85;
  line-height: 1.4;
}
```

---

## Progress bar with embedded logo

```html
<div class="progress-bar">
  <img class="tgw-logo" src="data:image/png;base64,{TGW}">
  <div class="progress-track">
    <div class="progress-fill"></div>
  </div>
  <div class="progress-count">N / T</div>
</div>
```

```css
.progress-bar { display: flex; align-items: center; gap: 16px; padding: 24px 40px; }
.tgw-logo { height: 20px; width: auto; }
.progress-track { flex: 1; height: 2px; background: currentColor; opacity: 0.2; position: relative; }
.progress-fill { position: absolute; inset: 0 auto 0 0; background: var(--accent); }
.progress-count { font-family: var(--font-body); font-weight: 600; font-size: 14px; letter-spacing: 0.1em; }

/* logo blend — dark slides */
.slide.dark .tgw-logo { mix-blend-mode: screen; opacity: 0.8; }
/* logo blend — light slides */
.slide.light .tgw-logo { mix-blend-mode: multiply; filter: invert(1); opacity: 0.65; }
```

---

## Edit highlight

```css
[contenteditable="true"]:hover,
[contenteditable="true"]:focus {
  outline: 2px solid var(--accent);
  outline-offset: 4px;
}
```

---

## Safe zone

40px on all edges at 1080×1350. All text and critical elements respect it. The frame system (progress bar, handle, slide number) sits at the edge by design — those are frame, not content.

---

## Verification snippets (used by Step 5.5)

These are paste-into-`preview_eval` blocks. They exist so every run audits the rendered file the same way.

### Overlap-checker JS snippet

Returns one row per slide listing the vertical position of every named element, and any overlap where one element's bottom edge crosses the next element's top edge. **Every slide must return `overlaps: []`.** Anything else, fix.

```javascript
(() => {
  const checkSlide = (slide, idx) => {
    const els = [...slide.querySelectorAll(
      '.section-tag, .content-headline, .mega-cover, .cta-headline, ' +
      '.body-copy, .cta-body, .case-list, .case-list-lead, .priority-banner, ' +
      '.subhead-line, .swipe-cta, .cta-handle, .cta-instruction, .progress-bar'
    )];
    const rects = els.map(el => ({
      name: el.className.split(' ')[0],
      top:  el.offsetTop,
      bot:  el.offsetTop + el.offsetHeight,
      h:    el.offsetHeight,
    }));
    rects.sort((a, b) => a.top - b.top);
    const overlaps = [];
    for (let i = 0; i < rects.length - 1; i++) {
      if (rects[i].bot > rects[i + 1].top) {
        overlaps.push(`${rects[i].name}(${rects[i].bot}) > ${rects[i + 1].name}(${rects[i + 1].top})`);
      }
    }
    // Also flag anything that runs into or past the 1350px slide bottom (footer is 1286–1350)
    const clipped = rects.filter(r => r.bot > 1286 && r.name !== 'progress-bar');
    return { slide: idx + 1, rects, overlaps, clipped: clipped.map(r => `${r.name}(bot ${r.bot})`) };
  };
  return [...document.querySelectorAll('.slide')].map(checkSlide);
})()
```

The audit also flags any non-footer element whose bottom edge falls inside the footer band (1286–1350px). That covers the case where layout is technically non-overlapping but the body copy is bleeding into the progress bar.

### Grid-view snippet (for a single all-slides screenshot)

Temporarily rearranges the stage into a 4-column grid so all 7 slides fit in one screenshot. Non-persistent — page reload restores the normal stacked view.

```javascript
(() => {
  const stage = document.querySelector('.stage');
  stage.style.display = 'grid';
  stage.style.gridTemplateColumns = 'repeat(4, 1fr)';
  stage.style.gap = '12px';
  stage.style.padding = '12px';
  document.querySelectorAll('.slide-wrap').forEach(w => { w.style.width = '100%'; });
  document.querySelectorAll('.per-slide-bar').forEach(b => { b.style.display = 'none'; });
  const wrap = document.querySelector('.slide-wrap');
  document.documentElement.style.setProperty('--slide-scale', String(wrap.getBoundingClientRect().width / 1080));
  window.scrollTo(0, 0);
  return 'grid view active — screenshot now, then reload';
})()
```

Call this, then `mcp__Claude_Preview__preview_screenshot`, then reload the page to restore the normal view.
