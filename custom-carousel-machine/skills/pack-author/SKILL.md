---
name: pack-author
description: Author a new white-label Style Pack for the Carousel Engine. Use when the user says "build me a new style pack", "create a style pack", "author a pack", "I want a new look", "make a pack that looks like X", or attaches inspiration images and asks for a matching pack. Generates an original pack spec (layout + palette-role mapping) into the buyer's project. Optionally reads a 1-3 image moodboard for DIRECTION ONLY and never reproduces an uploaded design.
---

# Pack Author

Creates a new **Style Pack** — pure layout and architecture that references palette roles, so it wears the buyer's Brand Profile automatically. The buyer is building their own portfolio of looks.

## Where packs live

In the buyer's **own project**, never inside the engine:

```
<buyer project>/carousel/packs/<pack-slug>.md
```

The two starter packs (`skills/carousel/starter-packs/`) ship read-only inside the engine and are worked examples to copy from. Authored packs are the buyer's and survive engine updates (ADR 0004).

## How a pack is defined

A pack is layout, not color. Read `skills/carousel/starter-packs/starter-packs.md` for the exact section shape and copy it. Each pack defines:

- Cover behavior, content-slide architecture, photo treatment, slide-number treatment, ornaments, body-copy alignment, list markers, frame-system overrides.
- A **palette-role mapping** — which role (`accent`, `bg-dominant`, `fg-dominant`, `paper`, `ink`) paints what. NEVER literal hex. The Brand Profile supplies the colors.
- Per-pack headline character budgets (see the budget formula in `starter-packs.md`).

**Escape hatch:** a pack may hardcode ONE palette role only when that color is the pack's defining identity (a single pop-color, or "no accent at all"). Everything else flows from the Brand Profile.

## Two ways the buyer drives it

1. **Describe a look** — "brutalist, huge type, one photo, no accent." Translate the description into a pack spec.
2. **Moodboard (optional, 1–3 inspiration images)** — the buyer attaches reference designs they admire.

### Moodboard rule (non-negotiable — ADR 0003)

Inspiration images set **abstract direction only**: density (dense vs airy), type-forward vs photo-forward, contrast level, casing, where type sits, rhythm. Read those signals, synthesize an **original** pack across the whole moodboard so no single source dominates, and let the Brand Profile supply all color, font, and logo.

**Never trace or reproduce an uploaded design.** Say this once to the buyer: "I use these for direction, not copying — and you're responsible for what you upload." If a buyer asks for a near-exact clone of a specific design, decline and offer to capture the direction instead.

## Output

Write the pack to `carousel/packs/<slug>.md`, then tell the buyer how to use it: "make a carousel with the <name> pack." Offer to render a quick test carousel so they can see the new look on real slides before they trust it.
