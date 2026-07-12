# Starter Style Packs

Two shipped packs. The buyer authors the rest with the **pack-author** skill. Both are layout only; colors come from the buyer's Brand Profile via palette roles, never literal hex.

## Palette roles

A pack paints with roles, not colors. The Brand Profile `palette` supplies the value for each:

| Role | CSS token | Brand Profile field |
|------|-----------|---------------------|
| ink | `--fg-inverse` / dark type | `palette.ink` |
| paper | `--bg-inverse` / light bg | `palette.paper` |
| dark | `--bg-dominant` / dark bg | `palette.dark` |
| accent primary | `--accent` | `palette.accent_primary` |
| accent secondary | `--accent-2` / tonal | `palette.accent_secondary` |

`--fg-dominant` is paper-on-dark; `--fg-inverse` is ink-on-paper. The engine resolves these in Step 2A from the Brand Profile. Type is the Brand Profile's display (headings) and body families.

**Escape hatch:** a pack may hardcode ONE role only when that color is the pack's defining identity. Mono Series uses it (accent: none).

---

## 1. MONO SERIES

Monochrome, type-and-number driven. Oversized ghosted slide numbers are the hero element. Edge gradients create swipe-continuity. **No accent color; the absence of color is the pack's identity (escape hatch: `--accent` is suppressed, tonal only).**

Roles used: `dark` (default dark slide), `paper` (alternates), `accent_secondary` as a third tonal gray. `--accent` is unused.

- **Cover:** Mega-Cover only. No ghost number. Stacked tight headline ~140–160pt, fg-dominant on dark (or fg-inverse on paper).
- **Ghost number (LIST-indexed, not slide-indexed):** the number reflects the item's position in the list, not the carousel. Cover and CTA carry no number. Render in the display font, ~340–400pt, opacity 0.13–0.18. Position follows content alignment.
- **Alternating rhythm:** slides rotate dark / paper / tonal-gray. Never two adjacent in the same tone. The rhythm IS the pack.
- **Edge gradients:** every slide carries a vertical gradient strip down one edge (alternating sides), ~25–30% width, fading to transparent. Light-into-dark on dark/gray slides, dark-into-light on paper.
- **Header strip:** thin top header (~88px) with the buyer's handle (avatar dot + `{handle}` from Brand Profile) left, topic tag right. Body font 600 small caps, 22pt.
- **No slide-number stamp.** The ghost number is the counter.
- **Body alignment:** left/center/right rotates slide to slide. Centered body allowed up to 3 lines on declarative slides only.
- **Lists:** allowed. Marker is an 8×8 filled square in fg-dominant at 0.5 opacity. No dots, no dashes.
- **Photos:** rare; when used, small contained rectangles, B&W, ~50% width max.
- **Recommend for:** numbered teaching listicles ("5 ways to ___", "Top 7 ___", "3 lessons from ___"), breakdown series.

### Headline budgets (1080×1350, 64px margins → 952px content width; display caps ~0.57 × font-size)
| Element | Font size | Chars/line | Max lines |
|---|---|---|---|
| `.mega-cover` | ~150px | 13 | 3 |
| `.content-headline` | ~96px | 21 | 3 |

---

## 2. EDITORIAL LONG-FORM

Paper background, ink body copy in real reading columns, numbered subheads. Built for text-heavy educational content.

Roles used: `paper` (bg), `ink` (body + type), `accent_primary` (numbered subheads, eyebrow).

- **Cover:** Mega-Cover in ink on paper. Optional small `GUIDE` / `EDITORIAL` eyebrow in accent-primary above the headline.
- **Content slides:** reading-column layout, max 58ch wide, body font 400 at 36px (renders ~18px in feed), line-height 1.5, left-aligned ragged right. Numbered subhead (`01.` in accent-primary, display font 700 at 72pt) above the paragraph.
- **Photos:** allowed but small, 100% width × 40% height max, above or below the column every 2–3 slides.
- **Slide number:** small ink "Page 3 / 8" bottom-left, body font 600 16pt, reads like a magazine folio.
- **Ornament:** thin 1px ink hairline between subhead and body column.
- **Lists:** checkbox square (8×8 ink outline), the only starter pack where lists are explicitly allowed.
- **Recommend for:** how-to guides, teaching content, frameworks, multi-point educational posts.

### Headline budgets
| Element | Font size | Chars/line | Max lines |
|---|---|---|---|
| `.mega-cover` | ~104px | 19 | 4 |
| Numbered subhead | 72px | 28 | 2 (reading body has its own 58ch max) |

---

## Headline budget check (at Step 3B)
For each plan row: count visible headline characters, divide by the pack's chars-per-line, round up to lines. If it exceeds max lines, tighten the copy (preferred) or split across more `<span class="line">` elements. Do NOT just shrink the font; that breaks the pack's rhythm.
