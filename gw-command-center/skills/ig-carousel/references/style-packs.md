# Style Packs — Instagram Carousel Skill v2

Seven visual packs. User picks one at Step 0.5. Packs 1–6 use Vitesse Bold (display) and Barlow (body) — only weight/size/casing/color changes. Pack 7 (Newsprint Bauhaus) swaps the display face to Anton (Google Fonts, same `<link>` as Barlow: add `family=Anton`); Vitesse is not used in that pack.

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
- **Photo treatment:** B&W or desaturated (filter: grayscale(1) contrast(1.05)). Strong bottom gradient. Gold hairline bar above headline on image slides.
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
--photo-filter: saturate(0.65) contrast(1.05) brightness(0.92);
```

- **Hero photo system:** ONE photo loaded once, base64-embedded, used as the full-bleed background of every slide in the carousel. The photo does not change slide to slide. The skill prompts the user for a hero photo path at Step 1 when this pack is selected.
- **Photo treatment:** Slightly desaturated and contrast-pushed (saturate 0.65, contrast 1.05, brightness 0.92). Heavy two-stop dark gradient overlay (55% at top, 88% at bottom) for legibility. Color elements in the photo remain readable but muted.
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
- **Content slides:** reading-column layout. Max 58ch width. Barlow 400 at 36px (renders ~18px at IG display), line-height 1.5, left-aligned ragged right. Numbered subhead (`01.` in gold, Vitesse 700 at 72pt) sits above the paragraph.
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
- **Black block callouts:** solid pure-black rectangles with white Barlow 600 text inside (~28px), 24–32px padding, rotated -1 to 1deg for a paste-up feel. One per slide max. This is the pack's version of a pull-quote.
- **Bauhaus primitives as anchors (never decorative):** each primitive has a JOB. Red circle = the point being made (numbered dot on pillar slides, ~72px, white Anton numeral inside). Blue rectangle/line = structure (section divider bar, margin rule, or the frame around the arc diagram). Black square = warning (anchors The Trap slide). One primitive family per slide region; if a shape has no job, delete it.
- **Hand-drawn marks:** black marker arrows, circles, underlines and scribbles as inline SVG paths — connecting a headline to a stat, circling a number, striking through a myth. Same wobble rule as the highlighter: irregular, organic, never geometric-perfect.
- **Photo treatment (default — torn clipping):** B&W editorial (`grayscale(1) contrast(1.1)`), pasted as a collage clipping: contained box (55–75% slide width), torn-edge `clip-path` polygon on 1–2 sides, slight rotation (-2 to 2deg), and a hand-drawn yellow SVG outline stroke tracing the photo's border. Photos never full-bleed, never behind text. No photorealistic 3D, no stock-look, no icon sets.
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
- **Default slide arc (7 slides):** Cover (provocation) → Core Thesis → Pillar 1 → Pillar 2 → Pillar 3 (red-dot numbered) → The Trap (inverse: pure black slide, white Anton headline, black-square anchor, what NOT to do) → CTA (paper again, black block callout carries the offer).
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

Slide content width at 1080×1350 with 64px left/right margins = **952px**. Vitesse Bold uppercase characters average **~0.57 × font-size** wide. So:

> **chars-per-line ≈ 952 / (0.57 × font-size-in-px)**

This is the only formula you need. Budgets below apply it per pack. Numbers are conservative — assume punctuation/highlight underlines eat 1–2 chars per line.

### Per-pack budgets

| Pack | Element | Font size | Chars per line | Max lines | Verified? |
|---|---|---|---|---|---|
| **The Case** | `.mega-cover` (cover) | 108px | 18 | 4 | ✅ (Marshall carousel, 2026-05-11) |
| **The Case** | `.content-headline` | 88px | 22 | 3 | ✅ (Marshall carousel, 2026-05-11) |
| **The Case** | `.cta-headline` | 96px | 20 | 2 | ✅ (Marshall carousel, 2026-05-11) |
| Asphalt Editorial | `.mega-cover` (cover) | ~120px (auto-fit) | 16 | 4 | starting estimate |
| Asphalt Editorial | `.content-headline` | ~92px | 22 | 3 | starting estimate |
| Acid Block | `.mega-cover` (cover) | ~120px | 16 | 4 | starting estimate |
| Acid Block | `.content-headline` | ~92px | 22 | 3 | starting estimate |
| Paper Minimal | `.mega-cover` (cover) | ~140px | 14 | 4 | starting estimate (bigger headline allowed — no photo competing) |
| Paper Minimal | `.content-headline` | ~96px | 21 | 3 | starting estimate |
| Mono Series | `.mega-cover` (cover) | ~150px | 13 | 3 | starting estimate (oversized headline paired with ghost number) |
| Mono Series | `.content-headline` | ~96px | 21 | 3 | starting estimate |
| Editorial Long-Form | `.mega-cover` (cover) | ~104px | 19 | 4 | starting estimate |
| Editorial Long-Form | Numbered subhead | 72px | 28 | 2 | starting estimate (reading-column body has its own 58ch max — different system) |
| Newsprint Bauhaus | `.mega-cover` (cover, Anton) | ~180px | 11 | 4 | ✅ (pack demo render, 2026-07-12) — Anton is condensed: chars-per-line ≈ 952 / (0.45 × font-size) for this pack, NOT the 0.57 Vitesse factor |
| Newsprint Bauhaus | `.content-headline` (Anton) | ~112px | 18 | 3 | ✅ (pack demo render, 2026-07-12) |
| Newsprint Bauhaus | Black block callout (Barlow 600) | 28px | 40 | 3 | ✅ (pack demo render, 2026-07-12) |

**The first time a pack ships, mark its row Verified after Step 5.5 passes.** Update the Verified column when a real carousel renders cleanly at the listed numbers. If reality forces a different size, update the table — don't leave stale numbers.

### Quick check at Step 3B

For each row of the slide plan: count visible characters in the headline (incl. spaces and punctuation, excluding any markup), divide by the budget's chars-per-line, round up to lines. If the result exceeds the budget's max lines, tighten the copy before showing the plan to the user. Don't ask the user to approve a plan with an oversized headline.
