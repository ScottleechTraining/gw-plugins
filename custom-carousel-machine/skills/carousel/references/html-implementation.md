# Carousel HTML Implementation Reference

All raw markup for the carousel skill lives here, not in SKILL.md. SKILL.md stays prose-only so the skill registers cleanly; this file holds the verbatim HTML, CSS, and JS to copy when generating a carousel.

Read the section you need at the step SKILL.md points you to.

---

## 1. Document head + font loading

Used at Step 5 (Generate the HTML). Fonts come from the buyer's Brand Profile (`fonts.display` and `fonts.body`).

- A family with `source: google` (the defaults are Roboto Slab display + Barlow body) loads from Google Fonts via the `<link>`.
- A family with `source: baked` embeds its `custom_base64` inline as an `@font-face` data URL, no external file path.

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=1080">
<title>...</title>
<!-- Request the Brand Profile's google-sourced families. Defaults shown below. -->
<link href="https://fonts.googleapis.com/css2?family=Roboto+Slab:wght@400;700;900&family=Barlow:wght@400;600;700;900&display=swap" rel="stylesheet">
<style>
  /* Emit this @font-face ONLY for a baked custom font (Brand Profile source: baked): */
  /* @font-face {
    font-family: '{DISPLAY_FONT}';
    src: url('data:font/otf;base64,{DISPLAY_FONT_BASE64}') format('opentype');
    font-weight: 700; font-style: normal; font-display: block;
  } */

  :root {
    --font-heading: '{DISPLAY_FONT}', 'Georgia', serif;   /* Brand Profile fonts.display.family; default Roboto Slab */
    --font-body: '{BODY_FONT}', sans-serif;               /* Brand Profile fonts.body.family; default Barlow */
    /* pack tokens go here (see Step 2A) */
  }

  /* rest of stylesheet */
</style>
</head>
```

Substitute `{DISPLAY_FONT}` / `{BODY_FONT}` from the Brand Profile. For a baked font, uncomment the `@font-face` and paste `custom_base64`. For Google fonts, make sure the `<link>` requests that family.

**Banned patterns (these break silently or cache-stale):**
- External stylesheet link pointing to a project file that contains the @font-face
- Referencing a relative font path as a `src: url()` (won't resolve when the user opens the file elsewhere)
- Splitting the @font-face into its own .css file and importing it
- Omitting `font-display: block` on a baked font (causes a paint flash before it loads)

---

## 2. Color system `:root` tokens

Used at Step 2A. All packs share the same structural tokens; only the values shift. Values come from the Brand Profile `palette`, mapped onto the chosen pack's roles; do not improvise hex.

```css
:root {
  --bg-dominant:    /* per pack */;
  --bg-inverse:     /* per pack */;
  --fg-dominant:    /* per pack */;
  --fg-inverse:     /* per pack */;
  --accent:         /* Brand Profile palette.accent_primary, or a pack escape-hatch color */;
  --accent-ink:     /* contrast color to read ON the accent */;
  --overlay-dark:   /* tune per pack, see the chosen pack's section */;
  --edit-highlight: var(--accent);
}
```

---

## 3. File structure order (top to bottom)

Used at Step 5. Build the single HTML file in this order:

1. Doctype and document head with:
   - charset meta tag
   - viewport meta tag set to `width=1080`
   - title: `{Topic} | {Pack Name} | {brand_name}` (brand_name from the Brand Profile)
   - Google Fonts link for the Brand Profile's google-sourced families (default Roboto Slab + Barlow)
   - **One** inline style block containing, in order:
     1. @font-face for a baked custom font (only if the Brand Profile sets source: baked)
     2. Reset + box-sizing
     3. `:root` pack tokens
     4. Typography base (body, h1–h3, paragraph defaults)
     5. Slide frame (`.slide` at 1080x1350, scaled down for preview)
     6. Persistent frame system (slide number, handle, swipe arrow, progress bar, logo)
     7. Template classes (Mega-Cover, Numbered Content, Long-Form Text, etc.; only the ones used)
     8. Pack-specific overrides (see the chosen pack's section in `starter-packs/starter-packs.md` or `carousel/packs/`)
     9. Toolbar styles, then the inline resize toolbar CSS (see section 5 below)
     10. Edit highlight states (contenteditable hover / focus)
   - html2canvas + jsPDF CDN script tags
2. Body:
   - Toolbar at top (fixed)
   - One slide section element per slide, in order
   - Resize toolbar element (the resize-toolbar div) immediately before the closing body tag (see section 6 below)
   - Export / edit JS, then the Inline Resize Controls JS block, as the final inline script block

**Pack CSS loads once.** Copy the pack's full CSS block from the chosen pack's section (`starter-packs/starter-packs.md` or `carousel/packs/`) into the inline style block; do not split into a separate file and link it.

---

## 4. PDF export script

Used at Step 5 (Toolbar). Add these two script tags: the jsPDF CDN tag plus the export function. html2canvas and jsPDF come from CDN URLs, never relative paths.

**html2canvas 1.4.1 does not implement CSS `filter`.** Every export path on the page (EXPORT ALL PNGs, DOWNLOAD SLIDE, EXPORT PDF) silently drops `filter:` declarations even though the live tab and any browser-screenshot QA render apply them. Photo treatments and logo ink must already be baked into the embedded image pixels at prep time (SKILL.md, Known export trap). If a slide needs `filter:` to look right, the export is already wrong.

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

## 5. Inline Resize Controls: CSS

Add after the existing toolbar rules in style slot 9. For Editorial Long-Form (a paper-dominant pack) the dark toolbar still works; do not invert it per pack.

```css
.resize-toolbar {
  position: absolute;
  display: none;
  align-items: center;
  gap: 6px;
  background: #222222;
  border: 1px solid rgba(250, 250, 247, 0.25);
  padding: 6px 8px;
  z-index: 9999;
  font-family: var(--font-body);
  box-shadow: 0 4px 24px rgba(0, 0, 0, 0.55);
  user-select: none;
}
.resize-toolbar.active { display: flex; }
.resize-toolbar .resize-label {
  color: rgba(250, 250, 247, 0.45);
  font-size: 10px;
  letter-spacing: 1.5px;
  text-transform: uppercase;
  font-weight: 700;
  border-right: 1px solid rgba(250, 250, 247, 0.18);
  padding-right: 8px;
  margin-right: 2px;
}
.resize-toolbar button {
  background: transparent;
  border: 1px solid rgba(250, 250, 247, 0.3);
  color: #FAFAF7;
  font-family: var(--font-body);
  font-weight: 700;
  padding: 4px 10px;
  cursor: pointer;
  font-size: 14px;
  letter-spacing: 0.5px;
}
.resize-toolbar button:hover {
  background: rgba(250, 250, 247, 0.12);
  border-color: var(--accent);
  color: var(--accent);
}
.resize-toolbar .size-display {
  color: rgba(250, 250, 247, 0.7);
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

## 6. Inline Resize Controls: HTML

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

## 7. Inline Resize Controls: JavaScript

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

## 8. Auto-fit Mega-Cover: JavaScript

Used at Step 5. The cover headline shrinks to fit the safe zone. Copy this function and its three call sites VERBATIM into the final script block (before the section 7 resize-controls JS). Do not re-derive it from the prose in `slide-architecture.md`. A from-scratch version reliably reintroduces the width-only bug (top word clipped, words break mid-word, last line collides with the footer/handle).

What it does, and why each part exists:
- **Width fit:** shrinks until every child `<span>` satisfies `scrollWidth <= safeW` (64px margins each side). Requires `.mega-cover span { white-space: nowrap; }` (see `slide-architecture.md`). Without nowrap a multi-word span wraps and reports the wrapped width, hiding overflow.
- **Height fit:** also shrinks until the whole cover satisfies `scrollHeight <= availH`, where `availH` is the space left inside `.slide-content` after the eyebrow/sub siblings and row gaps. This is the part a hand-written version forgets, and it is what stops multi-line headlines from overflowing vertically.
- **Font-load re-fit:** runs again on `document.fonts.ready`. The first pass runs against fallback-font metrics (narrower); the real display-font glyphs are wider, so without the re-fit the cover stays oversized after the webfont swaps in.
- **Manual-size guard:** the `if (el.dataset.manualSize === 'true') return;` line skips covers the user resized by hand with the section 7 controls.
- **`MEGACOVER_FIT_V1` marker:** the marker comment is harmless; leave it or drop it. This engine has no external patcher.

```javascript
function autoFitMegaCover() {
  // MEGACOVER_FIT_V1: fits each span to width AND the cover to available height; re-runs on font load
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
      let reserved = 0;
      kids.forEach(ch => { if (ch !== el) reserved += ch.scrollHeight; });
      reserved += gap * Math.max(0, kids.length - 1);
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

Used at Step 5 (toolbar + final script block). Every generated carousel ships with a Save Changes button so in-browser edits persist back to disk. It uses the File System Access API (`showSaveFilePicker` / `createWritable`); Ctrl+S (or Cmd+S) triggers it too. The first click connects the file (pick the same `.html` you are viewing); every later click saves in place.

Copy both blocks VERBATIM from below. Do not retype or "improve" them.

**Button HTML, add into the toolbar immediately after the `EXPORT PDF (Canva)` button:**

```html
<button id="saveChangesBtn" onclick="saveChanges()" style="background:#FFD700;color:#0a0a0a;font-weight:800;">💾 SAVE CHANGES</button>
<span id="saveStatus" class="status" style="display:none;"></span>
<span id="dirtyDot" style="display:none;color:#FFD700;font-weight:bold;margin-left:4px;">●</span>
```

**Save script, add as its own block immediately before the closing `</body>` tag (after the final inline script):**

```html
<script>
(function() {
  let fileHandle = null;
  let isDirty = false;
  // Version marker so the patcher can detect old vs new
  /* standalone save feature, no external patcher to version-match */

  document.addEventListener('input', (e) => {
    if (e.target && (e.target.isContentEditable || e.target.contentEditable === 'true')) {
      isDirty = true;
      const dot = document.getElementById('dirtyDot');
      if (dot) dot.style.display = 'inline';
    }
  });

  window.addEventListener('beforeunload', (e) => {
    if (isDirty) {
      e.preventDefault();
      e.returnValue = '';
    }
  });

  function setStatus(msg, color) {
    const status = document.getElementById('saveStatus');
    if (!status) return;
    status.style.display = 'inline';
    status.textContent = msg;
    status.style.color = color || '';
  }

  window.saveChanges = async function() {
    // Wait until page is fully loaded
    if (document.readyState !== 'complete') {
      alert('Page is still loading. Wait a moment and try again.');
      return;
    }

    // Build the content FIRST, before touching any file
    let html;
    try {
      html = '<!DOCTYPE html>\n' + document.documentElement.outerHTML;
    } catch (err) {
      alert('Could not serialize the page: ' + err.message + '\n\nFile NOT touched.');
      return;
    }

    // Pre-validate: refuse to save if content is suspicious
    if (!html || html.length < 2000) {
      alert(
        'Save aborted: serialized HTML is only ' + (html ? html.length : 0) + ' bytes. ' +
        'That looks like an empty or broken page.\n\n' +
        'File NOT touched.\n\n' +
        'If you think this is wrong, check the browser console for errors.'
      );
      return;
    }

    // Sanity check: make sure body has more than just whitespace
    const bodyMatch = html.match(/<body[^>]*>([\s\S]*?)<\/body>/i);
    if (bodyMatch) {
      const bodyContent = bodyMatch[1].trim();
      if (bodyContent.length < 100) {
        alert(
          'Save aborted: <body> is essentially empty (' + bodyContent.length + ' chars). ' +
          'The page may not have rendered. File NOT touched.'
        );
        return;
      }
    }

    if (!('showSaveFilePicker' in window)) {
      alert('File System Access API not available. Falling back to download.');
      downloadFallback(html);
      return;
    }

    // First save: pick the file
    if (!fileHandle) {
      try {
        setStatus('Pick THIS html file to connect...');
        fileHandle = await window.showSaveFilePicker({
          suggestedName: location.pathname.split('/').pop() || 'carousel.html',
          types: [{ description: 'HTML File', accept: { 'text/html': ['.html'] } }]
        });
      } catch (err) {
        if (err.name === 'AbortError') {
          setStatus('');
          return;
        }
        alert('Could not open file picker: ' + err.message + '\n\nFile NOT touched.');
        return;
      }
    }

    // Now actually write. From this point a failure mid-write WILL leave the file corrupted.
    let writable = null;
    try {
      writable = await fileHandle.createWritable();
      await writable.write(html);
      await writable.close();
      isDirty = false;
      const dot = document.getElementById('dirtyDot');
      if (dot) dot.style.display = 'none';
      setStatus('Saved \u2713 (' + new Date().toLocaleTimeString() + ')', '#6fbf6f');
      setTimeout(() => setStatus(''), 3000);
    } catch (err) {
      if (writable) {
        // File was opened for writing, which truncates. If write/close failed,
        // the file is likely corrupted. Warn loudly with recovery instructions.
        const filename = location.pathname.split('/').pop() || 'carousel.html';
        alert(
          'SAVE FAILED MID-WRITE: ' + err.message + '\n\n' +
          'YOUR FILE (' + filename + ') MAY BE CORRUPTED.\n\n' +
          'Restore it from a backup, or regenerate the carousel. ' +
          'If this happens repeatedly, tell Claude.'
        );
        try { await writable.close(); } catch(e) {}
      } else {
        alert('Save failed (file NOT modified): ' + err.message);
      }
      setStatus('Save failed', '#ff5544');
    }
  };

  function downloadFallback(html) {
    const blob = new Blob([html], { type: 'text/html' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = location.pathname.split('/').pop() || 'carousel-edited.html';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    isDirty = false;
    alert('Downloaded edited HTML. Save it over the original to keep edits.');
  }

  document.addEventListener('keydown', (e) => {
    if ((e.ctrlKey || e.metaKey) && e.key === 's') {
      e.preventDefault();
      window.saveChanges();
    }
  });
})();
</script>
```

The save button and its script are standalone; there is no external patcher. Emit both blocks (the button HTML and the save script) so in-browser edits persist to disk.
