# Cover Treatments — the scroll-stopper layer

The cover is the ad for the carousel. Body slides teach; the cover has one job: stop the thumb. Every carousel picks TWO things at planning time: a style pack (the body system, `style-packs.md`) and a COVER TREATMENT from this menu. The treatment governs slide 1 only. Slides 2+ always follow the pack.

Treatments inherit the pack's palette and typefaces unless a treatment says otherwise. One treatment per cover. Never stack two.

**Two standing laws, no exceptions:**
1. **Type Plate is always on the menu.** Every pack's own default cover is a permanent, first-class option — never a downgrade. If a treatment's guardrails can't be met with the available photo and copy, Type Plate is the REQUIRED fallback. A clean default beats a strained treatment every time.
2. **The edge rule.** No headline glyph may touch or cross the slide edge, in any treatment. Oversized display type keeps a visible margin (≥40px) on both sides. Edge-bleed type is a rework, not a style. When sizing a giant word, verify against real rendered width — condensed and slab faces run wider than the budget formula suggests; when in doubt, size down and re-render.

## Selection quick-reference

| Cover material | Treatment |
|---|---|
| One strong single-subject photo, mindset/identity topic | 2. Depth Interlock |
| Crowded scene (huddle, sideline, weight room floor) with one focal point | 3. Spotlight Color |
| Wide scenic shot + a short declarative claim | 4. Torn Paste-Up |
| Two photos that contrast (then/now, right/wrong, young/old) | 5. Quadrant Collage |
| Process/focus/technique topic with a detail worth isolating | 6. Focus Blur |
| No photo earns the cover, or the pack is type-first by identity | 1. Type Plate (default) |

If the topic has no photo that earns full-bleed, use Type Plate. A weak photo full-bleed is worse than no photo.

---

## 1. TYPE PLATE (default — what every pack does today)

The pack's own mega-cover: headline-dominant on the pack's background, photo optional per pack rules. This is the fallback and the correct choice for Paper Minimal and Mono Series, whose identity is typographic restraint. No new rules; see the pack.

## 2. DEPTH INTERLOCK

Giant word layered BEHIND the photo subject, secondary line in FRONT. The depth illusion is the hook.

**Assets (Pillow, one pass):** from ONE photo export two files at IDENTICAL pixel dimensions: `bg.jpg` (full frame, pack photo treatment baked in with Pillow — not CSS filter, trap 6) and `cut.png` (rembg subject cutout, same B&W treatment, alpha kept). Identical dimensions are what make alignment trivial.

**Layering (CSS):** `img.bg` and `img.cut` get IDENTICAL `left/top/width` (absolute). Sandwich: bg (z1) → big word (z2) → cut (z3) → front line + kicker (z4) → bottom legibility gradient (z5, max 0.5 opacity, bottom 30% only).

**Guardrails (each one broke in the first proof — do not skip):**
- The back word stays ≥70% legible. Subject overlaps 15–35% of the word's area, never its middle third. If the subject is centered, shift the word up or enlarge it until its top half clears the subject's head.
- Word color: pack accent (or white). One word, max two. Anton/Vitesse per pack, 260–360px.
- Front line is short (3–6 words) and sits on visually quiet ground. NEVER over feet, hands, or busy texture. Check the rendered photo, not the layout box.
- Kicker gets its own clear band; if the subject fills the bottom, drop the kicker entirely.

## 3. SPOTLIGHT COLOR

Full-bleed photo desaturated to B&W; one circle zone reveals the original color, tinted with the pack accent, and carries a short quote/claim.

**Recipe:** TWO Pillow-prepped files from one color JPEG at identical pixel dimensions: `bw.jpg` (grayscale + contrast 1.1 baked in) for the full-bleed base `<img>`, and the color JPEG for the circle. Never one copy with `filter: grayscale(1)` — html2canvas drops CSS filter at export and the base ships in color (SKILL.md trap 6). A circle `div` (44–52% of slide width, `border-radius: 50%`, `overflow: hidden`) containing the color image, offset negatively so it aligns with the base (circle at `left:L, top:T` → inner img at `left:-L, top:-T`, same width as base). Inside the circle: `::after` tint layer, pack accent at 0.35–0.5 opacity, `mix-blend-mode: multiply`.
- Circle placement: over the focal human, rule-of-thirds, never dead center.
- Text inside the circle: quote mark + 2–3 short lines, last line in accent + display face. Text must clear the circle's edge by ≥60px.
- Bottom gradient for the footer only.

## 4. TORN PASTE-UP

Full-bleed photo, slightly dimmed; headline carried on 2–3 torn-paper blocks; film border.

**Recipe:** photo `<img>` full-bleed, treatment baked with Pillow at prep time (`ImageEnhance.Color` 0.85 + `Contrast` 1.05, or the pack's treatment — CSS `filter` is banned on slide content, SKILL.md trap 6). Paper blocks: paper-color background (`#F4F0E4` or pack paper), 12-point jagged `clip-path` polygon (vertices ±6% off the rectangle, no two edges alike), rotation alternating -2° to +2°, headline in the pack display face at 150–190px, near-black. Film border: `box-shadow: inset 0 0 0 14px rgba(20,15,10,0.85), inset 0 0 90px rgba(0,0,0,0.55)`.
- One thought split across the blocks ("AUGUST IS / COMING."), not two thoughts.
- Blocks overlap the photo's dead zones; keep faces/action visible between them.
- Kicker in white with text-shadow on a quiet band.

## 5. QUADRANT COLLAGE

2×2 (or 1/3–2/3) grid alternating photo tiles and type tiles. The Nike look: type tile top-left or top-right, condensed black type on paper/white; two B&W photos diagonal from each other.

**Recipe:** CSS grid, zero gap or 8px pack-ink gap. Photo tiles: B&W, `object-fit: cover`, grain ok. Type tiles: pack paper background, display face at 110–150px, 3–6 words per tile, tight leading (0.9).
- The two type tiles read as ONE sentence across the diagonal ("IF THEY CAN'T FIND YOU" → "MAKE THEM LOOK").
- Photos must differ in scale (one tight portrait, one wide/action) or the grid reads flat.
- Footer strip sits on its own band below the grid.

## 6. FOCUS BLUR

Full-bleed photo blurred; ONE sharp word; 2–3 small SHARP crops of the same photo pinned like specimens with tiny labels.

**Assets (Pillow):** `blur.jpg` = full frame, `GaussianBlur(10–14)`, B&W. Plus 2–3 crops from the ORIGINAL (sharp) at exact regions — hands, eyes, ball — saved as small JPEGs. Record each crop's source position.
**Layout:** blurred base full-bleed; sharp word in white/pack accent, display face 150–220px, dead center or golden-section; crop boxes (180–300px wide, 2px white border) scattered on the slide's clear zones, each with a one-word italic label. Crops must NOT cover the word.
- Works only when the source photo is sharp to begin with. Crops from a soft photo kill the trick.
- Best for: focus, details, technique, film-study topics.

---

## Process wiring (how this runs in the machine)

1. **Planning (skill Step 3B / batch brief):** the plan names pack + cover treatment + cover photo. The orchestrator (or the skill, attended) recommends a treatment from the quick-reference based on the topic and the photo's character; builder may fall back to Type Plate if the photo can't carry the treatment (say so in the return line).
2. **Verification:** the cover is judged FIRST at render review, on one question: would this stop a coach's thumb in a feed full of workout clips? Layout-correct but flat = send back with a stronger treatment or better photo.
3. **Review page:** a polish note starting with `cover:` means rebuild the COVER ONLY (treatment/photo change per the note); body slides stay. `/gw-carousel-batch` picks these up like `restyle:` notes but touches only slide 1.
4. **Size discipline:** all cover assets obey the standing rules — JPEGs ~≤300KB, cutout PNGs ≤500KB, always `<img>` tags, never CSS custom properties.
