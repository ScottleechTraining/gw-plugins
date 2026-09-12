# Legacy Paper Packs (historical specifications)

Retired from the active menu on 2026-09-12 when both were combined into the single **Editorial** pack (`style-packs.md`, pack 4). These specifications are kept verbatim so that:

- existing decks built in either pack keep rendering and reporting under their original name (the scanner still recognizes both names);
- an existing `restyle: Paper Minimal` or `restyle: Editorial Long-Form` polish note remains valid and is built to the historical spec below;
- an explicit request to keep an old pack is honored. Explain its legacy status; never force a migration. Selecting Editorial on an old deck is an intentional restyle and follows the normal review gates.

Headings here are deliberately unnumbered so the review-page menu parser (`build_review_page._style_packs`, which reads `## N. NAME` headings in `style-packs.md`) never discovers them as active choices. New automatic builds never choose these packs.

---

## PAPER MINIMAL (legacy, was pack 4)

Paper-dominant, asphalt type, small supporting photos, heavy negative space.

```css
--bg-dominant: #EFEDE3;       /* paper */
--bg-inverse:  #1A1A1A;
--fg-dominant: #1A1A1A;
--fg-inverse:  #EFEDE3;
--accent:      #1A1A1A;       /* no color accent — asphalt IS the accent */
--accent-ink:  #EFEDE3;
--overlay-dark: rgba(0,0,0,0.0);
```

- **Cover:** Mega-Cover in asphalt on paper. Type can go bigger here because there's no image competing — auto-fit has more room.
- **Photo treatment:** Photos appear as small, contained rectangles (not full-bleed) — roughly 60–70% of slide width, left-aligned, with paper margin around them. B&W.
- **Slide number:** Small asphalt "01 / 07" top-right. Same as Asphalt Editorial.
- **Ornament:** None. Restraint is the point.
- **Recommend for:** editorial essays, philosophy posts, anything that benefits from quiet confidence.

---

## EDITORIAL LONG-FORM (legacy, was pack 6)

Paper background, asphalt body copy in real reading columns, numbered subheads. Built for text-heavy educational content.

```css
--bg-dominant: #EFEDE3;
--bg-inverse:  #1A1A1A;
--fg-dominant: #1A1A1A;
--fg-inverse:  #EFEDE3;
--accent:      #C8A84E;
--accent-ink:  #1A1A1A;
--overlay-dark: rgba(0,0,0,0.6);
```

- **Cover:** Mega-Cover in asphalt on paper. Can include a small `EDITORIAL` or `GUIDE` eyebrow label in gold above the headline.
- **Content slides:** reading-column layout. Max 58ch width. Barlow 400 at 36px (renders ~18px at IG display), line-height 1.5, left-aligned ragged right. Numbered subhead (`01.` in gold, Vitesse 700 at 72pt) sits above the paragraph and MUST carry `max-width: 800px` so its first line clears the `@Sleech72` handle-stamp (clearance law: `slide-architecture.md`, Persistent frame section).
- **Photo treatment:** Photos allowed but kept small — 100% width × 40% height max, positioned above or below the text column as a visual break every 2–3 slides.
- **Slide number:** Small asphalt "Page 3 / 8" bottom-left, Barlow 600 16pt. Reads like a magazine folio.
- **Ornament:** Thin 1px asphalt hairline between the subhead and the body column on content slides.
- **Allowed list marker:** checkbox square (8×8 asphalt outline) for checklist slides. This is the only pack where lists are explicitly allowed.
- **Recommend for:** how-to guides, teaching content, frameworks, multi-point educational posts.

---

Headline budgets for these packs (starting estimates, never measured): Paper Minimal `.mega-cover` ~140px, `.content-headline` ~96px; Editorial Long-Form `.mega-cover` ~104px and the numbered subhead at 72px = 15 chars per line (measured 2026-08-02, stamp-safe 800px). Recompute anything else from the Vitesse factor table in `style-packs.md` before trusting it.
