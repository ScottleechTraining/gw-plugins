# Seamless Image Spreads

Instagram carousel's native swipe creates a built-in reveal effect. One wide photo sliced across 2–3 slides gives the feeling that swiping pans the camera. This doc explains how to implement it in the HTML output.

## When to use

- Wide or horizontally-composed photos (landscapes, full-body action, stadium shots)
- Photos where the subject stretches across the frame
- Never for tight headshots; they look broken when sliced

## How the slicing works

Instagram displays each slide at 1080×1350 (4:5). When you span a photo across N slides, the **effective canvas** is `(1080 × N) wide × 1350 tall`.

For each spanning slide `k` (0-indexed) out of N total:

```css
.slide-span {
  background-image: url('{BASE64_FULL_IMAGE}');
  background-size: calc(100% * {N}) 100%;   /* e.g. 300% for 3-slide span */
  background-position: calc(-100% * {k}) 0; /* 0% for slide 0, -100% slide 1, -200% slide 2 */
  background-repeat: no-repeat;
}
```

No need to actually slice the image into separate files; CSS `background-size` + `background-position` does it. Each slide shows a 1080-wide window into the wider image.

## Implementation pattern

```html
<!-- Slides 3 and 4 share one image, span=2 -->
<div class="slide" data-span-group="a" data-span-index="0" data-span-total="2">
  <div class="image-layer" style="
    background-image: url('data:image/jpeg;base64,...');
    background-size: 200% 100%;
    background-position: 0% 0%;
  "></div>
  <div class="overlay"></div>
  <div class="content"><!-- headline, body --></div>
</div>

<div class="slide" data-span-group="a" data-span-index="1" data-span-total="2">
  <div class="image-layer" style="
    background-image: url('data:image/jpeg;base64,...');  /* SAME base64 string */
    background-size: 200% 100%;
    background-position: -100% 0%;
  "></div>
  <div class="overlay"></div>
  <div class="content"><!-- headline continues, body --></div>
</div>
```

**Important:** both slides embed the same base64 string. The file gets heavy, but it's the only way to guarantee identical rendering. Keep source images under 1.5MB before encoding for sanity.

## Text placement on spanning slides

- **Slide 0 of a spread:** text goes on the left third (where the image's empty/darker zone usually lives after you crop)
- **Slide 1 of a spread:** text goes on the right third
- **Slide 2 of a spread (if 3-wide):** either text-free (let the image breathe) or text goes where the photographer left negative space
- **Overlay:** apply the overlay treatment uniformly across all spanning slides (same gradient, same opacity) or the seam is visible

## Asking the user

At Step 1, the skill asks:

> Want any photos to span multiple slides for a swipe-reveal effect? Format: "slide 3–4" or "slide 2–3–4". Skip if you'd rather keep slides independent.

Parse the answer into span groups. Each group has: start slide, length (2 or 3), source image filename.

In the slide plan table, mark spanning slides with the `Span` column showing the group (e.g., `3–4` on both rows).

## Preview check

When rendering the HTML preview (all slides in a flex grid), spanning slides should visibly line up if placed next to each other. If they don't line up, the slicing math is off, most likely `background-size` doesn't match N or `background-position` percentages are wrong.
