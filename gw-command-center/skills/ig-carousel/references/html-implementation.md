# Carousel HTML Implementation Reference

All raw markup for the carousel skill lives here, not in SKILL.md. SKILL.md stays prose-only so the skill registers cleanly; this file holds the verbatim HTML, CSS, and JS to copy when generating a carousel.

Read the section you need at the step SKILL.md points you to.

---

## 1. Document head + inline @font-face skeleton

Used at Step 5 (Generate the HTML). Vitesse Bold ships inside the file as a base64 data URL in an inline style block. Barlow loads from Google Fonts. Inline-only — no external stylesheet for the font.

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

**Banned patterns (these break silently or cache-stale):**
- External stylesheet link pointing to a shared pack file that contains the @font-face
- Referencing `assets/Vitesse-Bold.otf` as a `src: url()` path (won't resolve when the user opens the file elsewhere)
- Splitting the @font-face into its own .css file and importing it
- Omitting `font-display: block` (causes a paint flash before Vitesse loads)

---

## 2. Color system `:root` tokens

Used at Step 2A. All packs share the same structural tokens; only the values shift. Exact values live in `references/style-packs.md` — copy them, do not improvise.

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

---

## 3. File structure order (top to bottom)

Used at Step 5. Build the single HTML file in this order:

1. Doctype and document head with:
   - charset meta tag
   - viewport meta tag set to `width=1080`
   - title — `{Topic} — {Pack Name} — Gridiron Warrior`
   - Barlow font link from Google Fonts (weights 400, 600, 700, 900)
   - **One** inline style block containing, in order:
     1. @font-face for Vitesse (base64 data URL)
     2. Reset + box-sizing
     3. `:root` pack tokens
     4. Typography base (body, h1–h3, paragraph defaults)
     5. Slide frame (`.slide` at 1080x1350, scaled down for preview)
     6. Persistent frame system (slide number, handle, swipe arrow, progress bar, logo)
     7. Template classes (Mega-Cover, Numbered Content, Long-Form Text, etc. — only the ones used)
     8. Pack-specific overrides (see `references/style-packs.md` for each pack's CSS block)
     9. Toolbar styles, then the inline resize toolbar CSS (see section 5 below)
     10. Edit highlight states (contenteditable hover / focus)
   - html2canvas + jsPDF CDN script tags
2. Body:
   - Toolbar at top (fixed)
   - One slide section element per slide, in order
   - Resize toolbar element (the resize-toolbar div) immediately before the closing body tag (see section 6 below)
   - Export / edit JS, then the Inline Resize Controls JS block, as the final inline script block

**Pack CSS loads once.** Copy the pack's full CSS block from `references/style-packs.md` into the inline style block — do not split into a separate file and link it.

---

## 4. PDF export script

Used at Step 5 (Toolbar). Add these two script tags — the jsPDF CDN tag plus the export function. html2canvas and jsPDF come from CDN URLs, never relative paths.

**html2canvas 1.4.1 does not implement CSS `filter`.** Every export path on this page (EXPORT ALL PNGs, DOWNLOAD SLIDE, PDF) silently drops `filter:` declarations even though the live tab renders them. Photo treatments and logo ink must already be baked into the embedded image pixels with Pillow (SKILL.md trap 6) — if a slide needs `filter:` to look right, the export is already wrong.

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

---

## 5. Inline Resize Controls — CSS

Add after the existing toolbar rules in style slot 9. For the light packs (Editorial, White Board, and the legacy paper packs) the dark toolbar still works — do not invert it per pack.

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

---

## 6. Inline Resize Controls — HTML

Add once, immediately before the closing body tag.

```html
<div class="resize-toolbar" id="resize-toolbar" role="toolbar" aria-label="Text size">
  <span class="resize-label">SIZE</span>
  <button data-resize="-4" title="Shrink (Ctrl+Down)">A−</button>
  <span class="size-display" id="resize-size">--px</span>
  <button data-resize="+4" title="Grow (Ctrl+Up)">A+</button>
  <button data-resize="reset" title="Reset to template default">RESET</button>
</div>
```

---

## 7. Inline Resize Controls — JavaScript

Add inside the final script block, after the export functions and after `autoFitMegaCover()`.

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

---

## 8. Auto-fit Mega-Cover — JavaScript

Used at Step 5. The cover headline shrinks to fit the safe zone. Copy this function and its three call sites VERBATIM into the final script block (before the section 7 resize-controls JS). Do not re-derive it from the prose in `slide-architecture.md`. A from-scratch version reliably reintroduces the width-only bug (top word clipped, words break mid-word, last line collides with the footer/handle).

What it does, and why each part exists:
- **Width fit:** shrinks until every child `<span>` satisfies `scrollWidth <= safeW` (64px margins each side). Requires `.mega-cover span { white-space: nowrap; }` (see `slide-architecture.md`). Without nowrap a multi-word span wraps and reports the wrapped width, hiding overflow.
- **Height fit:** also shrinks until the whole cover satisfies `scrollHeight <= availH`, where `availH` is the space left inside `.slide-content` after the eyebrow/sub siblings and row gaps. This is the part a hand-written version forgets, and it is what stops multi-line headlines from overflowing vertically.
- **Font-load re-fit:** runs again on `document.fonts.ready`. The first pass runs against fallback-font metrics (narrower); the real Vitesse glyphs are wider, so without the re-fit the cover stays oversized after the webfont swaps in.
- **Manual-size guard:** the `if (el.dataset.manualSize === 'true') return;` line skips covers the user resized by hand with the section 7 controls.
- **`MEGACOVER_FIT_V2` marker:** leave the marker comment in place. The standalone patcher (`scripts/gwqueue/patch_carousels_megacover_autofit.py`) treats any file containing the current marker as already-current and skips it, so freshly-generated files are never re-patched; files carrying an older `MEGACOVER_FIT_V1` marker get upgraded.
- **V2 fix (2026-08-12):** V1 summed EVERY `.slide-content` child's scrollHeight as reserved height. Packs with a full-slide absolutely-positioned overlay inside the content box (Newsprint Bauhaus `.grain`) reserved the whole slide, so the fit loop pinned the headline at the 80px floor and the cover rendered as a small corner block over dead paper. V2 skips `position:absolute/fixed` children in both the height sum and the gap count.

```javascript
function autoFitMegaCover() {
  // MEGACOVER_FIT_V2: fits each span to width AND the cover to available height; re-runs on font load
  document.querySelectorAll('.mega-cover').forEach((el) => {
    if (el.dataset.manualSize === 'true') return;
    const container = el.closest('.slide');
    if (!container) return;
    const safeW = 1080 - 128;
    const spans = el.querySelectorAll('span');
    if (!spans.length) return;
    // Available height inside .slide-content (layout px): 1350 minus 64 top / 120 bottom,
    // minus the non-mega siblings (eyebrow, sub) and the column gaps, with a little slack.
    let availH = 1166;
    const content = el.closest('.slide-content');
    if (content) {
      const cs = getComputedStyle(content);
      const gap = parseFloat(cs.rowGap || cs.gap || '0') || 0;
      const kids = Array.from(content.children);
      // V2: out-of-flow siblings (position absolute/fixed, e.g. Newsprint's
      // full-slide .grain overlay) take no flow height. Counting them starved
      // availH and pinned the headline at the size floor.
      let reserved = 0;
      let inFlow = 0;
      kids.forEach(ch => {
        const pos = getComputedStyle(ch).position;
        if (pos === 'absolute' || pos === 'fixed') return;
        inFlow += 1;
        if (ch !== el) reserved += ch.scrollHeight;
      });
      reserved += gap * Math.max(0, inFlow - 1);
      availH = 1166 - reserved - 40;
    }
    let size = 220;
    while (size > 80) {
      el.style.fontSize = size + 'px';
      let fits = true;
      spans.forEach(s => { if (s.scrollWidth > safeW) fits = false; });
      if (el.scrollHeight > availH) fits = false;
      if (fits) break;
      size -= 4;
    }
    el.style.fontSize = size + 'px';
  });
}

document.addEventListener('DOMContentLoaded', () => { autoFitMegaCover(); });
// Re-fit once the webfont actually loads. Fallback-font metrics are narrower and
// otherwise leave the cover oversized after the real glyphs swap in.
if (document.fonts && document.fonts.ready) {
  document.fonts.ready.then(() => { autoFitMegaCover(); });
}
autoFitMegaCover();
```

If the file also defines `updateSlideScale()` (the preview scaler), keep calling it where it already runs. It is independent of the auto-fit and the two coexist (call both inside the `DOMContentLoaded` handler if present).


---

## 9. Save Changes button (every carousel)

Used at Step 5. Every generated carousel ships with Save Changes and Ctrl+S/Cmd+S support. The canonical implementation lives in runtime `scripts/gwqueue/patch_carousels_savebtn.py`; use its helper through `scripts.gwqueue.build_carousel`, preserving the emitted button and version marker. Do not copy or re-derive the save JavaScript here. Legacy files keep the helper's existing save behavior.

The assembler calls `patch_html` on the candidate file to supply `SAVE_BUTTON_HTML` and `SAVE_SCRIPT_HTML`. Preserve the Save button, status and dirty indicators, input tracking, unsaved-change warning, page-load/serialized-content guards, first-save file picker and subsequent in-place saves, download fallback, cancellation/error handling, and Ctrl+S/Cmd+S shortcut. These behaviors remain in the helper; removing the duplicated script from this reference does not make them optional. Do not invoke the patcher's bulk-scanning CLI as part of a build or migrate existing decks. The assembler's content-hash replacement backup is separate from browser Save Changes.

**Opted-in files:** capability-check and follow [copy-record.md](copy-record.md), the single schema and lifecycle contract. The assembler embeds the master and injects `scripts/gwqueue/carousel_copy_browser.js` plus copy-aware save integration into the standalone HTML. No relative script dependency and no hand-built caption editor: the helper supplies the editable caption outside slides. Skeleton copy uses stable bindings, including the required final CTA binding.

Save captures current bound text, explicit newlines, caption, and CTA into escaped master JSON before serializing the document. Invalid copy must stop saving before the file is touched. Do not bypass that preparation by serializing the DOM yourself. After editing, save/reopen and run the copy validator; a restyle must read the saved master and preserve wording exactly. A capability failure is not permission to downgrade opted-in files to legacy saving.

---

## 10. White Board pack — namespaced CSS (proof-verified 2026-09-12)

Verbatim from the proof decks rendered through the real export path (`docs/superpowers/carousel-style-refresh-2026-09-12/`). Tokens live on the slide itself (`.slide.pack--white-board`, SKILL.md trap 2). Every visible string on a board slide is its own `data-gw-copy` binding; the CSS carries only rules, discs, and connectors. Photos are baked B&W JPEGs in `--cover-photo` / `--body-photo` (`/*GW_HERO*/`, `/*GW_HERO2*/`), never a CSS filter (trap 6). The persistent frame uses the dark logo (`/*GW_LOGO_DARK*/`).

```css
  /* ---- pack tokens: on the slide itself (SKILL.md trap 2) ---- */
  .slide.pack--white-board {
    --bg-dominant: #FAFCFA;
    --bg-inverse:  #17201D;
    --fg-dominant: #17201D;
    --fg-inverse:  #FAFCFA;
    --accent:      #176B47;
    --accent-ink:  #FFFFFF;
    --board-rule:  #C9D4CE;
    --overlay-dark: none;
    --edit-highlight: var(--accent);
  }

  /* Prose, photo, and card bridges sit centered; the drawing slide stays top-aligned. */
  .slide-content.bridge { justify-content: center; padding-bottom: 170px; }

  /* ---- persistent frame ---- */
  .num-stamp {
    position: absolute; top: 56px; left: 64px; z-index: 6;
    font-family: var(--font-body); font-weight: 700; font-size: 22px;
    letter-spacing: 2px; opacity: 0.6;
  }
  .handle-stamp {
    position: absolute; top: 56px; right: 64px; z-index: 6;
    font-family: var(--font-body); font-weight: 700; font-size: 22px;
    letter-spacing: 3px; text-transform: uppercase; opacity: 0.6;
  }
  .swipe-arrow { position: absolute; bottom: 100px; right: 64px; z-index: 6; font-size: 40px; line-height: 1; opacity: 0.55; }
  .progress-bar {
    position: absolute; bottom: 0; left: 0; right: 0; z-index: 6;
    display: flex; align-items: center; gap: 20px; padding: 26px 64px;
  }
  .tgw-logo {
    width: 108px; height: 26px; flex-shrink: 0;
    background-image: var(--tgw-logo-dark);
    background-size: contain; background-repeat: no-repeat; background-position: left center;
    opacity: 0.8;
  }
  .progress-track { flex: 1; height: 3px; background: var(--board-rule); position: relative; }
  .progress-fill { position: absolute; top: -1px; bottom: -1px; left: 0; background: var(--accent); }
  .progress-count { font-family: var(--font-body); font-weight: 700; font-size: 16px; letter-spacing: 2px; opacity: 0.6; }

  /* ---- shared board type ---- */
  .board-headline {
    max-width: 940px;
    font-family: var(--font-heading); font-weight: 700;
    font-size: 84px; line-height: 1.1; letter-spacing: 0; text-wrap: balance;
  }
  .green-rule { width: 200px; height: 10px; background: var(--accent); margin: 30px 0 34px; }
  .board-body {
    max-width: 900px;
    font-family: var(--font-body); font-weight: 400;
    font-size: 42px; line-height: 1.4; white-space: pre-line;
  }
  .takeaway {
    margin-top: 20px; max-width: 940px;
    border-top: 4px solid var(--fg-dominant); padding-top: 16px;
    font-family: var(--font-body); font-weight: 600; font-size: 44px; line-height: 1.25;
  }

  /* ---- cover (Type Plate: headline, one green rule, one contained photo) ---- */
  .mega-cover {
    font-family: var(--font-heading); font-weight: 700;
    font-size: 96px; line-height: 1.02; letter-spacing: 0; text-transform: uppercase;
    display: flex; flex-direction: column;
  }
  .mega-cover span { display: block; white-space: normal; }
  .mega-cover br { display: none; }
  .cover-photo {
    width: 952px; height: 470px; flex-shrink: 0;
    background-image: var(--cover-photo); background-size: cover; background-position: center;
    border: 3px solid var(--fg-dominant);
  }

  /* ---- compare layout (visual teaching: two conditions, one dimension) ---- */
  .compare { position: relative; display: grid; grid-template-columns: 1fr 1fr; column-gap: 56px; margin-top: 26px; }
  .compare::before { content: ''; position: absolute; left: 50%; top: 0; bottom: 0; border-left: 3px solid var(--board-rule); }
  .cond-label {
    font-family: var(--font-body); font-weight: 600; font-size: 44px; line-height: 1.1;
    padding-bottom: 12px; border-bottom: 6px solid var(--fg-dominant); margin-bottom: 14px;
  }
  .cond.after .cond-label { color: var(--accent); border-color: var(--accent); }
  /* Fixed row height keeps the two conditions aligned even when one label wraps to two lines. */
  .row { display: flex; gap: 16px; align-items: flex-start; min-height: 118px; padding: 4px 0; }
  .row .disc {
    flex-shrink: 0; width: 44px; height: 44px; margin-top: 4px; border-radius: 50%;
    border: 4px solid var(--fg-dominant);
    font-family: var(--font-body); font-weight: 700; font-size: 22px;
    display: flex; align-items: center; justify-content: center;
  }
  /* Told apart without color: outlined discs on the straight column, filled on the paired one. */
  .cond.after .row .disc { background: var(--fg-dominant); color: var(--accent-ink); }
  .row .txt { font-family: var(--font-body); font-weight: 400; font-size: 38px; line-height: 1.3; }
  /* The one focal relationship in green: what happens in the rest. */
  .cond.after .row.focal .txt { color: var(--accent); font-weight: 600; }
  .cond.after .row.focal .disc { background: var(--accent); border-color: var(--accent); }
  .dimension { margin-top: 20px; max-width: 940px; font-family: var(--font-body); font-weight: 400; font-size: 40px; line-height: 1.35; }

  /* ---- sequence layout (order only unless durations are sourced) ---- */
  .sequence { position: relative; margin-top: 30px; padding-left: 96px; }
  .sequence::before { content: ''; position: absolute; left: 30px; top: 26px; bottom: 44px; width: 5px; background: var(--fg-dominant); }
  .step { position: relative; padding-bottom: 20px; margin-bottom: 16px; border-bottom: 2px solid var(--board-rule); }
  .step:last-child { border-bottom: 0; margin-bottom: 0; padding-bottom: 0; }
  .step .disc { position: absolute; left: -96px; top: 0; width: 64px; height: 64px; border-radius: 50%; background: var(--fg-dominant); color: var(--accent-ink); font-weight: 700; font-size: 30px; display: flex; align-items: center; justify-content: center; }
  .step h3 { font-weight: 600; font-size: 48px; line-height: 1.1; margin-bottom: 8px; }
  .step p { font-weight: 400; font-size: 40px; line-height: 1.3; }
  /* The turn: the final step is the one focal relationship in green. */
  .step.final .disc { background: var(--accent); }
  .step.final h3 { color: var(--accent); }
  .scale-note { margin-top: 22px; font-weight: 600; font-size: 30px; letter-spacing: 1px; text-transform: uppercase; opacity: 0.7; }

  /* ---- annotated example (labeled illustrative artifact + numbered callouts) ---- */
  .illustrative { align-self: flex-start; margin: 22px 0 18px; padding: 8px 16px; background: var(--fg-dominant); color: var(--accent-ink); font-weight: 700; font-size: 26px; letter-spacing: 2px; text-transform: uppercase; }
  .report { width: 100%; border-collapse: collapse; border: 4px solid var(--fg-dominant); }
  .report th, .report td { padding: 16px 22px; text-align: left; border-bottom: 2px solid var(--board-rule); vertical-align: middle; font-size: 40px; line-height: 1.2; }
  .report tr:last-child th, .report tr:last-child td { border-bottom: 0; }
  .report th { width: 46%; font-weight: 600; }
  .report td { font-weight: 400; }
  .report .mark { display: inline-flex; width: 44px; height: 44px; margin-right: 14px; border-radius: 50%; background: var(--fg-dominant); color: var(--accent-ink); font-weight: 700; font-size: 24px; align-items: center; justify-content: center; vertical-align: middle; }
  .report tr.focal .mark { background: var(--accent); }
  .annotations { display: grid; grid-template-columns: 1fr 1fr; gap: 16px 36px; margin-top: 26px; }
  .annotation { font-weight: 400; font-size: 36px; line-height: 1.25; }
  .annotation strong { display: block; font-weight: 600; font-size: 40px; margin-bottom: 2px; }
  .annotation strong::before { content: attr(data-number) " / "; color: var(--accent); }
  .annotation.focal strong { color: var(--accent); }

  /* ---- photo bridge ---- */
  .body-photo {
    width: 952px; height: 500px; flex-shrink: 0; margin-top: 38px;
    background-image: var(--body-photo); background-size: cover; background-position: center;
    border: 3px solid var(--fg-dominant);
  }

  /* ---- reference card (source-supported list) ---- */
  .card { border: 4px solid var(--fg-dominant); padding: 40px 44px 36px; }
  .card-title {
    font-family: var(--font-heading); font-weight: 700; font-size: 60px; line-height: 1.05;
    padding-bottom: 22px; margin-bottom: 20px; border-bottom: 6px solid var(--accent);
  }
  .check { display: flex; gap: 20px; align-items: flex-start; padding: 11px 0; }
  .check .box { flex-shrink: 0; width: 34px; height: 34px; margin-top: 9px; border: 4px solid var(--fg-dominant); }
  .check .txt { font-family: var(--font-body); font-weight: 400; font-size: 40px; line-height: 1.3; }
  .card-note {
    margin-top: 22px; padding-top: 20px; border-top: 3px solid var(--board-rule);
    font-family: var(--font-body); font-weight: 600; font-size: 34px; line-height: 1.35;
  }

  /* ---- cta ---- */
  .slide-content.cta { justify-content: center; padding-bottom: 190px; }
  .cta-block { background: var(--bg-inverse); color: var(--fg-inverse); padding: 52px 56px 56px; max-width: 952px; }
  .cta-headline { font-family: var(--font-heading); font-weight: 700; font-size: 72px; line-height: 1.08; letter-spacing: 0; }
  .cta-follow { margin-top: 44px; font-family: var(--font-body); font-weight: 700; font-size: 30px; letter-spacing: 4px; text-transform: uppercase; }
```

Board markup pattern for the three layouts (labels shown as static text here; bind each one in production):

```html
<!-- Compare: two conditions, aligned rows, divider, one focal row in green -->
<div class="compare">
  <section class="cond before"><p class="cond-label">Condition A</p>
    <div class="row"><span class="disc">1</span><span class="txt">…</span></div> …
  </section>
  <section class="cond after"><p class="cond-label">Condition B</p>
    <div class="row"><span class="disc">1</span><span class="txt">…</span></div>
    <div class="row focal"><span class="disc">3</span><span class="txt">the changed thing</span></div> …
  </section>
</div>
<p class="dimension">The one dimension that changed.</p>
<p class="takeaway">…</p>

<!-- Sequence: one rail, numbered discs, final step green, order note -->
<div class="sequence">
  <section class="step"><span class="disc">1</span><h3>…</h3><p>…</p></section> …
  <section class="step final"><span class="disc">4</span><h3>…</h3><p>…</p></section>
</div>
<p class="scale-note">Order only. Not a time scale.</p>

<!-- Annotated: labeled artifact, numbered marks, matching callouts, focal callout green -->
<p class="illustrative">Illustrative entry / not a work prescription</p>
<table class="report"><tbody><tr class="focal"><th><span class="mark">4</span>…</th><td>…</td></tr></tbody></table>
<div class="annotations"><div class="annotation focal"><strong data-number="4">…</strong>…</div></div>
```
