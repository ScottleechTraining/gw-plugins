# Style Packs — Instagram Carousel Skill v2

Seven visual packs. User picks one at Step 0.5. Packs 1–6 use Vitesse Bold (display) and Barlow (body) — only weight/size/casing/color changes. Pack 7 (Newsprint Bauhaus) swaps the display face to Anton (Google Fonts, same `<link>` as Barlow: add `family=Anton`); Vitesse is not used in that pack.

**The cover is planned separately.** Every carousel also picks a COVER TREATMENT — the scroll-stopper layer for slide 1 — from `cover-treatments.md`. The pack governs slides 2+; the treatment governs the cover and inherits the pack's palette and faces. Type Plate (the pack's own mega-cover) is the default treatment.

Each pack defines:
- Accent color + contrast ink
- Dominant background / inverse background
- Overlay treatment for photos
- Slide-number treatment
- Cover slide behavior
- Corner ornament (if any)

---

## 1. ASPHALT EDITORIAL

Moody B&W photos, heavy dark overlays, gold accent. The default GW look, tightened.

```css
--bg-dominant: #1A1A1A;      /* asphalt */
--bg-inverse:  #F5F0E8;      /* paper-warm */
--fg-dominant: #F5F0E8;
--fg-inverse:  #1A1A1A;
--accent:      #C8A84E;       /* gold */
--accent-ink:  #1A1A1A;
--overlay-dark: linear-gradient(180deg, rgba(0,0,0,0.25) 0%, rgba(0,0,0,0.85) 100%);
```

- **Cover:** Mega-Cover on asphalt or full-bleed photo with bottom gradient. Vitesse 700 at auto-fit size, 0.88 line-height, uppercase, `letter-spacing: -0.02em`.
- **Photo treatment:** B&W or desaturated — bake grayscale(1) contrast(1.05) into the JPEG with Pillow at prep time (`ImageOps.grayscale` + `ImageEnhance.Contrast`); never CSS `filter`, which html2canvas drops at export (SKILL.md trap 6). Strong bottom gradient. Gold hairline bar above headline on image slides.
- **Slide number:** Small gold "01 / 07" in top-right. Barlow 700 small caps.
- **Body copy:** Paper on asphalt, Barlow 400 18px equivalent.
- **Recommend for:** mindset content, grit/discipline topics, long training narratives.

---

## 2. THE CASE

Hero photo carried across every slide. Scanline overlay. Gold accent. Argument-building carousel format where each slide is one act of the case being made.

```css
--bg-dominant: #1A1A1A;       /* asphalt fallback if no photo */
--bg-inverse:  #F5F0E8;
--fg-dominant: #FFFFFF;        /* pure white headlines on photo */
--fg-inverse:  #1A1A1A;
--accent:      #C8A84E;        /* gold — brand */
--accent-ink:  #FFFFFF;        /* white reads on gold for the section tag */
--overlay-dark: linear-gradient(180deg, rgba(0,0,0,0.55) 0%, rgba(0,0,0,0.88) 100%);
/* photo treatment saturate(0.65) contrast(1.05) brightness(0.92) is BAKED into
   the hero JPEG with Pillow at prep time — never a CSS filter token; html2canvas
   drops filter at export (SKILL.md trap 6) */
```

- **Hero photo system:** ONE photo loaded once, base64-embedded, used as the full-bleed background of every slide in the carousel. The photo does not change slide to slide. The skill prompts the user for a hero photo path at Step 1 when this pack is selected.
- **Photo treatment:** Slightly desaturated and contrast-pushed (saturate 0.65, contrast 1.05, brightness 0.92) — baked into the hero JPEG with Pillow at prep time (`ImageEnhance.Color(...)` 0.65 → `Contrast` 1.05 → `Brightness` 0.92), never CSS `filter` (SKILL.md trap 6). Heavy two-stop dark gradient overlay (55% at top, 88% at bottom) for legibility. Color elements in the photo remain readable but muted.
- **Scanline overlay:** A 2px-spaced horizontal scanline pattern at ~4% opacity sits over the photo and under the dark overlay. Implementation: `repeating-linear-gradient(to bottom, transparent 0px, transparent 2px, rgba(255,255,255,0.04) 2px, rgba(255,255,255,0.04) 3px)` with `mix-blend-mode: overlay`.
- **Cover:** No section tag. No eyebrow label of any kind — the cover leads directly with the headline (the reference's "→ STRENGTH & CONDITIONING" line is school-brand chrome that does not belong on a Case carousel). Massive uppercase Vitesse Bold headline at ~120–148pt with one or two key words wrapped in `.hl` spans (gold color + 6px gold underline 8px below the baseline). Subhead line in light gray Barlow 400 ~30pt below the headline. Bottom of slide: "→ SWIPE TO LEARN MORE" in Barlow 600 small caps, white at 0.7 opacity. TGW logo + progress bar remain at the foot.
- **Content slide:** Gold filled rectangle section tag at top-left (Barlow 700, white text, 22pt, 12×24px padding, uppercase, ~3px letter-spacing). Label text is freeform — match the slide's role for the carousel topic. Massive Vitesse Bold headline below the tag with one or two words in `.hl` gold + underline. Body copy below the headline in Barlow 400 at ~30–34pt, white at 0.85 opacity, line-height 1.45. Body may run 2–3 short paragraphs.
- **Headline highlight rule:** Each slide highlights one or two words in gold with a gold underline beneath them. Never more than two words per headline. Underline is 6px tall, 8px below the baseline, same gold as the word. No box around the word — color shift and underline only.
- **Frame system override:** This pack does NOT carry the standard slide-number stamp, swipe arrow, or header strip on inner slides. TGW logo and progress bar remain. The section tags and headline progression ARE the navigation.
- **Optional component — Priority callout banner:** Translucent gold-tinted rectangle with a 4px gold left border. Contains a hash-number stamp ("#1", "#2") in Vitesse 700 ~56pt gold on the left, and a one-line priority statement in Barlow 500 white ~22pt on its right. Use sparingly — max once per carousel.
- **Optional component — Circle-badge numbered list:** Vertical list where each item leads with a 64px circular badge (gold 3px ring, transparent fill, gold numeral inside in Barlow 700 28pt). Item subhead in Vitesse 700 32pt white. Item body in Barlow 400 24pt white at 0.85 opacity. Use for slides that summarize multiple pillars or steps.
- **Body copy voice rule:** Scott's external brand voice forbids em-dashes. Body copy uses periods or commas only. Do NOT mirror the reference's em-dash usage.
- **Recommend for:** authority arguments, "why X is wrong" posts, "the science of Y" breakdowns, "what most coaches miss about Z" — any carousel that walks the reader through a coaching case to a conclusion.
- **Note:** Hero photo is the brand carrier in this pack. Pick a photo that earns the screen real estate. Tight portraits, wide gym scenes, and coach-in-context shots all work. Avoid action blurs — the photo needs to read as a still anchor across 6–8 slides.

---

## 3. ACID BLOCK

Off-black + paper + electric cherry red accent. Color blocks behind individual words.

```css
--bg-dominant: #0F0F0F;
--bg-inverse:  #EFEDE3;
--fg-dominant: #EFEDE3;
--fg-inverse:  #0F0F0F;
--accent:      #FF2E3C;       /* electric cherry red — replaces gold for this pack only */
--accent-ink:  #EFEDE3;
--overlay-dark: rgba(0,0,0,0.5);
```

- **Cover:** Mega-Cover on asphalt. One or two key words wrapped in a cherry-red `<span>` with `background: var(--accent); color: var(--accent-ink); padding: 0.05em 0.25em;` — the "highlighter block" effect. No italic, no underline; the block does the work.
- **Alternating backgrounds:** slides switch between asphalt, paper, and solid cherry-red. Commit to the rhythm — don't make two cherry slides adjacent.
- **Photo treatment:** Full B&W with a cherry-red duotone option on 1–2 slides max (mix-blend-mode: multiply over red fill).
- **Slide number:** Cherry-red circle stamp, 56px, top-left. Barlow 700 paper-colored numeral.
- **Recommend for:** bold opinion/contrarian takes, attention-grabbers, campaign launches.
- **Note:** This is the only pack that replaces gold. Gold and cherry red do not co-exist on a slide.

---

## 4. PAPER MINIMAL

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

## 5. MONO SERIES

Monochrome black / paper / asphalt-tinted gray. Oversized ghosted slide numbers as the hero design element. Edge gradients create swipe-continuity rhythm between slides. No accent color — the absence of color is the pack's identity.

```css
--bg-dominant: #1A1A1A;       /* asphalt — default dark slide */
--bg-inverse:  #F5F0E8;       /* paper — alternates with asphalt */
--bg-tertiary: #3A3A3A;       /* asphalt-tinted gray — third tone for rhythm */
--fg-dominant: #F5F0E8;
--fg-inverse:  #1A1A1A;
--accent:      #3A3A3A;       /* tonal only — never used as a color pop */
--accent-ink:  #F5F0E8;
--overlay-dark: none;          /* edge gradients only, no flat photo overlays */
```

- **Cover:** Mega-Cover only. NO ghost number on the cover. Stacked tight headline at ~140–160pt, paper on asphalt (or asphalt on paper). The cover sets up the list — it isn't the first item of it.
- **Ghost number system (LIST-INDEXED, not slide-indexed):** The ghost number on a content slide reflects the position of that item IN THE LIST, not the slide's index in the carousel. A "5 ways to build speed" carousel reads: Cover (no number) → 01 → 02 → 03 → 04 → 05 → CTA (no number). The cover and final CTA slide are both bare. Ghost number renders in Vitesse 700, ~340–400pt, opacity 0.13–0.18 (lighter on paper, heavier on asphalt). Position matches the slide's content alignment: number-left when content is left-aligned, number-right when content is right-aligned, number-centered when content is centered.
- **CTA / final slide:** No ghost number. No section frame chrome other than the header strip and TGW logo + progress bar. Headline and CTA copy only.
- **Alternating slide rhythm:** Slides alternate between asphalt (#1A1A1A), paper (#F5F0E8), and asphalt-tinted gray (#3A3A3A). Never two adjacent slides in the same tone. The rhythm IS the pack — commit to it.
- **Edge gradients:** Every slide carries a vertical gradient strip down one edge (alternating sides slide to slide). Light-into-dark on asphalt/gray slides, dark-into-light on paper slides. Width ~25–30% of slide width, fades to transparent. This is the pack's signature swipe-continuity device.
- **Photo treatment:** Photos are rare in this pack — the design is text-and-number driven. When used, photos appear as small contained rectangles (not full-bleed), B&W, ~50% slide width max, positioned to balance the ghost number.
- **Header strip:** Every slide carries a thin top header (~88px tall) with handle (avatar dot + @Sleech72) left and a topic tag (`#mindset`, `#offseason`, etc.) right. Barlow 600 small caps, 22pt.
- **No slide-number stamp.** This pack drops the standard "02 / 07" corner stamp entirely. The ghost number IS the counter on content slides. Cover and CTA carry no counter at all. Other packs use the stamp; Mono Series does not.
- **Body copy alignment:** Left, center, or right — alignment rotates slide to slide to create rhythm. Centered body allowed up to 3 lines on declarative-statement slides only.
- **Bullet lists:** Allowed. Custom marker is an 8x8 filled square in fg-dominant at 0.5 opacity. No round dots, no dashes. Match Editorial Long-Form's marker treatment.
- **Recommend for:** numbered teaching listicles ("5 ways to ___", "Top 7 ___", "3 lessons from ___"), breakdown series, coaching-principle drops where each slide is one numbered point.
- **Note:** This is the only pack with zero color accent. If a layout tempts you to add gold or any other color, the pack's identity is gone.

---

## 6. EDITORIAL LONG-FORM

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

## 7. NEWSPRINT BAUHAUS

Vox-explainer editorial fused with classic Bauhaus. Every slide is a magazine spread, not a corporate slide: aged newsprint paper, oversized condensed black headlines, hand-drawn yellow highlighter strokes, and geometric primary-color primitives used with discipline. Journalistic, opinionated, confident — headlines provoke, they don't describe.

```css
--bg-dominant: #EFE8D8;       /* aged newsprint */
--bg-inverse:  #000000;        /* pure black — The Trap slide + callout blocks */
--fg-dominant: #000000;
--fg-inverse:  #FFFFFF;
--red:         #E10600;        /* Bauhaus red — circle/dot only */
--blue:        #0026CA;        /* Bauhaus blue — rectangle/line only */
--yellow:      #FFDE00;        /* highlighter strokes only */
--font-heading: 'Anton', 'Impact', sans-serif;   /* condensed black, replaces Vitesse */
--font-body:    'Barlow', sans-serif;
--overlay-dark: none;          /* no gradients anywhere in this pack */
```

- **Hard palette law:** paper, black, white, plus AT MOST ONE Bauhaus primary per slide region. Red is always a circle or dot. Blue is always a rectangle or line. Yellow is always a hand-drawn highlighter stroke. No gradients, no pastels, no soft tones, no drop shadows, ever.
- **Typography law:** aggressive scale contrast. Anton headlines are massive, uppercase, tight (`letter-spacing: 0.005em`, line-height 0.92), often full-width. Body is Barlow 400 at ~30–34px (reads ~15–17px at IG display), line-height 1.55, max 46ch. Nothing mid-sized: if a text element is not a headline or small refined body, it should not exist.
- **Backgrounds:** aged newsprint. Implementation: flat `--bg-dominant` plus a subtle SVG `feTurbulence` noise data-URI at 4–6% opacity, plus (on 2–3 slides max) a faint technical-grid layer: `repeating-linear-gradient` hairlines in black at 5% opacity, 40px spacing, both axes. Grid shows BEHIND content, never over it.
- **Highlighter strokes:** the signature move. One key phrase per slide (max two) gets an irregular hand-drawn yellow marker stroke BEHIND the text: an inline SVG `<path>` with a wobbly baseline (4–6 anchor points, varying stroke width 0.45–0.6em, `stroke-linecap: round`, opacity 0.85, rotate ~-1deg), absolutely positioned under the words. Never a clean CSS `background` rectangle — it must read as a human hand, not a vector tool.
- **Highlighter stroke on the INVERSE slide (The Trap): legibility law, both halves required.** This shipped broken once (caught 2026-07-29). Half 1: `.hl-text` inherits the inverse headline's white, and white on `#FFDE00` is roughly 1.9:1, unreadable. The highlighted word on the inverse slide must be pure black: `style="color:#000;"` on the `.hl-text` span. Half 2: black text alone does NOT fix it. The default wobbly path dips and climbs across the viewBox, so its band leaves slivers of the cap height uncovered; on paper slides those gaps are invisible (black glyphs stay legible on paper), but on the black slide every uncovered sliver of glyph vanishes into the background. The inverse slide therefore also swaps to a flatter, fatter stroke that fully covers the cap height, at opacity 1 so the black background cannot bleed through the band. Verified by render at 1080x1350 (podcast-drew-fopeano slide 7, 2026-07-29). Copy verbatim, changing only the word:

  ```html
  <span class="line hl-line"><svg class="hl-svg" viewBox="0 0 200 44" preserveAspectRatio="none"><path d="M6,22 C50,19 92,25 132,20 C162,18 180,24 194,21" stroke="#FFDE00" stroke-width="36" stroke-linecap="round" fill="none" opacity="1"/></svg><span class="hl-text" style="color:#000;" contenteditable="true">KEY PHRASE.</span></span>
  ```

  Keep the default `.hl-svg` box (`inset:-8% -3%; width:106%; height:118%`). Paper slides keep the default wobbly stroke; do not flatten them. The wobble is the pack's hand-drawn signature, and paper forgives its gaps.
- **Highlighter placement law: on `.dark` slides the highlight must START a line.** (Caught 2026-08-13, three-coaches polish.) The stroke's `stroke-linecap: round` paints roughly half the stroke-width past each end of the path — with stroke-width 36 in a 200-unit viewBox that is ~12.5% of the highlight's width in real paint (~20px on a 156px highlight), while a body-copy word space is only ~6-7px. A highlight placed mid-line therefore ALWAYS laps 10-15px onto the neighboring word. On paper slides the black glyphs stay legible through the 0.85-opacity yellow, so nobody notices. On the black Trap slide the stroke is opacity 1 and it ERASES the adjacent white letters outright ("will still break him." rendered as "will sti" + yellow pill). Do not fight it with `&nbsp;` padding inside the span (the pill grows with the padding, canceling the gain) or by removing the preceding space (worse). The fix: put a `<br>` immediately before the `span.hl-line` so the highlight opens its line and the left overhang falls harmlessly into the 64px page margin. Mid-line highlights are fine on paper slides only.
- **Black block callouts:** solid pure-black rectangles with white Barlow 600 text inside (~28px), 24–32px padding, rotated -1 to 1deg for a paste-up feel. One per slide max. This is the pack's version of a pull-quote.
- **Bauhaus primitives as anchors (never decorative):** each primitive has a JOB. Red circle = the point being made (numbered dot on pillar slides, ~72px, white Anton numeral inside). Blue rectangle/line = structure (section divider bar, margin rule, or the frame around the arc diagram). Black square = warning (anchors The Trap slide). One primitive family per slide region; if a shape has no job, delete it.
- **Hand-drawn marks:** black marker arrows, circles, underlines and scribbles as inline SVG paths — connecting a headline to a stat, circling a number, striking through a myth. Same wobble rule as the highlighter: irregular, organic, never geometric-perfect.
- **Photo treatment (default — torn clipping):** B&W editorial, baked into the JPEG with Pillow at prep time (`ImageOps.grayscale` + `ImageEnhance.Contrast(...).enhance(1.1)`, in the same pass that resizes it) — never `filter:grayscale` on the `<img>`, which html2canvas drops at export so the posted PNG ships full color (SKILL.md trap 6). Pasted as a collage clipping: contained box (55–75% slide width), torn-edge `clip-path` polygon on 1–2 sides, slight rotation (-2 to 2deg), and a hand-drawn yellow SVG outline stroke tracing the photo's border. Photos never full-bleed, never behind text. No photorealistic 3D, no stock-look, no icon sets.
- **Photo treatment (hero — subject cutout with yellow outline):** the pack's signature image. The subject is cut out of its background and traced with an irregular yellow marker halo. ONE per carousel max, on the slide that earns it (cover or thesis). Verified Pillow recipe (rembg is installed on this machine, model cached at `~/.u2net`):
  1. `img.thumbnail((900, 900))`, then `rembg.remove(img)` → RGBA cutout.
  2. Subject: grayscale + `ImageEnhance.Contrast(...).enhance(1.15)`, re-merge with the cutout's alpha.
  3. Halo: alpha `.point(lambda p: 255 if p > 60 else 0)` → `MaxFilter(31)` dilate → `GaussianBlur(6)` then re-threshold at 90 (the blur+re-threshold is what makes the edge organic, not vector-perfect) → fill `#FFDE00`.
  4. Composite yellow halo under subject on a transparent layer, rotate the whole layer ~-2deg, paste onto the newsprint canvas.
  5. Export as PNG (alpha is required) and embed in an `<img>` tag at ≤500KB. NEVER put this PNG in a CSS custom property — the base64-overflow trap applies there; `<img>` src is safe.
  - The halo counts as that region's yellow. No highlighter stroke in the same region of the slide.
  - Pick photos with one clear subject (portrait, pose, single lifter). Crowded sideline shots segment badly.
- **Slide number:** small black block stamp top-left, white Barlow 700 ("No. 3") — reads like a page marker.
- **Cover:** headline owns the spread. Anton at ~170–200px, full-width, stacked 3–4 lines, one phrase highlighter-struck. Small Barlow body kicker below (max 2 lines). One red circle anchor. No photo on the cover unless it is a torn clipping smaller than 40% of the slide.
- **Default slide arc (7 slides):** Cover (provocation) → Core Thesis → Pillar 1 → Pillar 2 → Pillar 3 (red-dot numbered) → The Trap (inverse: pure black slide, white Anton headline, black-square anchor, what NOT to do; any highlighted word follows the inverse-slide legibility law above) → CTA (paper again, black block callout carries the offer).
- **Editorial tone rule:** one core idea per slide, headline-driven. Write headlines like a Vox cover line: a claim, not a label. "YOUR GASSERS ARE LYING TO YOU", not "CONDITIONING MISTAKES".
- **Body copy voice rule:** Scott's voice rules still apply in full — no em-dashes, no banned words, short sentences.
- **Recommend for:** explainer/breakdown content, myth-vs-fact journalism angles, big-idea essays, anything Scott wants to land like a magazine feature.
- **Note:** centered PowerPoint symmetry is forbidden. Every layout is grid-based and asymmetric: headline block off-axis, body column narrow, primitives balancing the composition.

---

## Pack selection quick-reference

| User said... | Suggest |
|---|---|
| "mindset", "grind", "discipline" | Asphalt Editorial |
| "argument", "case", "why X is wrong", "the science of", "what coaches miss" | The Case |
| "bold take", "hot take", "launch" | Acid Block |
| "essay", "philosophy", "quiet" | Paper Minimal |
| "5 ways to", "top 7", "3 lessons", "numbered listicle" | Mono Series |
| "how-to", "guide", "teach", "framework", "long-form teaching" | Editorial Long-Form |
| "explainer", "breakdown", "magazine", "newsprint", "bauhaus", "vox", "myth vs fact" | Newsprint Bauhaus |

If unclear, ask. Don't guess — the pack shapes everything downstream.

---

## Headline character budgets — REQUIRED, USE AT PLANNING TIME

A carousel breaks when the planner writes a headline that doesn't fit the pack's font size. Before delivering the Step 3B slide plan, check each headline against the pack's budget. If a headline exceeds budget, either:
- Shorten the copy (preferred — tighter Scott voice usually reads better anyway), or
- Split it across more `<span class="line">` elements so each line stays inside its per-line cap.

**Do NOT just bump the font size down to make it fit.** That breaks the pack's visual rhythm. The budgets exist so copy stays at the size the pack was designed for.

### How the budgets are derived

Slide content width at 1080×1350 with 64px left/right margins = **952px**. Character width is a property of the display face, so the factor is per font, not global:

> **chars-per-line ≈ safe-width / (factor × font-size-in-px)**

| Display face | Used by | Factor | Evidence status |
|---|---|---|---|
| Vitesse Bold | packs 1-6, every pack except Newsprint | **0.75** | Measured 2026-08-02, real glyphs at 72 / 88 / 92 / 96 / 108px. Worst real-word rate is a constant 0.735 × font-size at every size; 0.75 is that rounded up to absorb punctuation and `.hl` underlines. |
| Anton | pack 7 Newsprint Bauhaus only | **0.32** | Measured 2026-08-12, real glyphs at 100px (Range widths, rendered band-stations cover, fonts.ready awaited). Real Scott-voice all-caps lines run a constant 0.271–0.302 × font-size ("BUILDING BAND" is the worst at 0.302); 0.32 is that rounded up to absorb punctuation and the highlighter stroke. All-W probe ceiling is 0.478 — a W/M-heavy line can run ~50% wider than the budget, so verify any such headline against real rendered width, not the formula. The old 0.45 was the 2026-07-12 demo declaration, never measured; it under-budgeted real copy by ~40% and pushed planners to shorten headlines that actually fit. |
| anything else | future packs | unmeasured | Measure it before trusting any budget. Never reuse another face's factor. |

**Why 0.57 was retired.** Every budget in this file before 2026-08-02 used a single 0.57 factor. It is not a font constant. It is Vitesse measured on narrow copy: I/L/T/E-heavy lines genuinely run 0.53 × font-size. Real Scott-voice copy runs 0.60 to 0.735, because W and M are close to double the width of an I. That is why the 2026-07-28 Asphalt check appeared to confirm 0.57 and still produced a budget that clips.

**A measured row beats the formula. The formula governs unmeasured rows.** If a row's Verified cell carries a dated worst-case real-glyph note, that row is the authority for its element, so do not override it with a formula result. A row marked "starting estimate" is not evidence: recompute it from the table above before you plan. Every estimate row still in this file predates the corrected factor and runs hot by roughly 30 to 60%.

Headlines use `white-space: nowrap`, so an over-budget line clips silently instead of wrapping. When copy exceeds budget, shorten it (preferred, tighter Scott voice usually reads better) or split it across more `<span class="line">` elements.

### Per-pack budgets

| Pack | Element | Font size | Chars per line | Max lines | Verified? |
|---|---|---|---|---|---|
| **The Case** | `.mega-cover` (cover) | 108px | 11 | 4 | ✅ measured 2026-08-02 (worst-case real glyphs, 1080x1350): at 108px, 17 chars ran 1131-1350px against the 952px zone and the worst real-word rate of 79.4px/char gives 11. Partly guarded: `autoFitMegaCover()` shrinks the cover to fit, so over-budget copy degrades to a smaller headline rather than clipping. Treat 11 as the size-holding budget, not a clip threshold. |
| **The Case** | `.content-headline` | 88px | 14 | 3 | ✅ measured 2026-08-02 (worst-case real glyphs, 1080x1350): at 88px, 22 chars ran 1158-1254px, 19 ran 940-1046px and 17 ran 921-1100px against the 952px zone, while 14 tops out at 880px. Worst real-word rate 64.7px/char. Supersedes the 2026-05-11 value of 22. |
| **The Case** | `.cta-headline` | 96px | 13 | 2 | ✅ measured 2026-08-02 (worst-case real glyphs, 1080x1350): at 96px, 17 chars ran 1005-1200px and even 18 chars of deliberately narrow copy ran 963px, all past the 952px zone; the worst real-word rate of 70.6px/char gives 13. NO auto-fit guard on this element, so an over-budget CTA clips silently. The old 20 came from the retired 0.57 factor. |
| Asphalt Editorial | `.mega-cover` (cover) | ~120px (auto-fit) | 16 | 4 | starting estimate |
| Asphalt Editorial | `.content-headline` | ~92px | 14 | 3 | ✅ measured 2026-08-02 (worst-case real glyphs, 1080x1350): at 92px, 17 chars ran 963-1150px past the 952px zone and the worst real-word rate of 67.6px/char gives 14. Supersedes the 2026-07-28 value of 18. That pass sampled narrow copy only, which is exactly the 1016-1106px band reproduced here by I/L/T/E-heavy lines, so it confirmed the retired 0.57 instead of catching it. Same Vitesse face as The Case, so the same 0.75 factor applies. |
| Acid Block | `.mega-cover` (cover) | ~120px | 16 | 4 | starting estimate |
| Acid Block | `.content-headline` | ~92px | 22 | 3 | starting estimate |
| Paper Minimal | `.mega-cover` (cover) | ~140px | 14 | 4 | starting estimate (bigger headline allowed — no photo competing) |
| Paper Minimal | `.content-headline` | ~96px | 21 | 3 | starting estimate |
| Mono Series | `.mega-cover` (cover) | ~150px | 13 | 3 | starting estimate (oversized headline paired with ghost number) |
| Mono Series | `.content-headline` | ~96px | 21 | 3 | starting estimate |
| Editorial Long-Form | `.mega-cover` (cover) | ~104px | 19 | 4 | starting estimate |
| Editorial Long-Form | Numbered subhead | 72px | 15 | 2 | ✅ measured 2026-08-02 (worst-case real glyphs, 1080x1350): stamp-safe width is 800px, not the full column, and at 72px Vitesse 17 chars ran 754-900px with a worst real-word rate of 52.9px/char, so 800 / 52.9 gives 15. Supersedes the 2026-07-28 value of 19, which was 800 / (0.57 × 72) on the retired factor. Reading-column body has its own 58ch max, a different system. |
| Newsprint Bauhaus | `.mega-cover` (cover, Anton) | ~180px | 16 | 4 | ✅ (measured 2026-08-12, real glyphs) chars-per-line ≈ 952 / (0.32 × font-size) for this pack, never the Vitesse factor. At 180px that is ~16 chars; "FIFTEEN MINUTES" (15ch) fits at 150px+ with margin. W/M-heavy lines: verify against real rendered width (see factor table). |
| Newsprint Bauhaus | `.content-headline` (Anton) | ~112px | 18 | 3 | ✅ (pack demo render, 2026-07-12) |
| Newsprint Bauhaus | Black block callout (Barlow 600) | 28px | 40 | 3 | ✅ (pack demo render, 2026-07-12) |

**The first time a pack ships, mark its row Verified after Step 5.5 passes.** Update the Verified column when a real carousel renders cleanly at the listed numbers. If reality forces a different size, update the table — don't leave stale numbers.

### Quick check at Step 3B

For each row of the slide plan: count visible characters in the headline (incl. spaces and punctuation, excluding any markup), divide by the budget's chars-per-line, round up to lines. If the result exceeds the budget's max lines, tighten the copy before showing the plan to the user. Don't ask the user to approve a plan with an oversized headline.
