---
name: brand-setup
description: One-time guided setup that writes a buyer's Brand Profile for the Carousel Engine. Use when the user says "set up my brand", "brand setup", "/brand-setup", "get me started", "configure my carousel brand", or runs the engine for the first time without a brand-profile.md present. Interviews the user for brand name, handle, palette, fonts, logo, and voice, then writes carousel/brand-profile.md into their project with the logo and any custom font base64-baked in.
---

# Brand Setup

Writes the buyer's **Brand Profile** — the single source of identity the Carousel Engine reads on every run. Run once. Re-run any time to change the brand.

## Where it writes

Always to the buyer's **own project**, never inside the engine:

```
<buyer project>/carousel/brand-profile.md
```

If `carousel/` does not exist in the current working directory, create it. Never write the brand profile inside the engine's own plugin folder (an engine update would wipe it — see ADR 0004 in the source repo).

## Before you start

Read `brand-profile.template.md` at the engine root. That template is the exact shape of the file you will write. Do not invent fields.

## The interview (one question at a time, accept defaults fast)

1. **Brand name** and **Instagram handle**.
2. **Palette** — ask for up to five hex values: ink (darkest type), paper (light background), dark (dark background), accent primary, accent secondary. If the user only has one or two colors, fill the rest with sensible neutrals and tell them what you chose.
3. **Fonts** — default is Roboto Slab (display) + Barlow (body), both free from Google Fonts. Ask only: "Use the free defaults, or your own font file?" If they supply a font file path, set `source: baked` and base64-encode the file into `custom_base64`. Warn once: they are responsible for that font's license.
4. **Logo** — ask for an image path. Base64-encode it into `logo.base64` so exported carousels stay self-contained. If they have no logo, leave it empty; the footer falls back to the handle text.
5. **Voice** — tone (direct / professional / playful / minimal), whether to ban em-dashes, any banned words, and a few sentences of free-text voice notes.

## Writing the file

Fill the template's YAML frontmatter with the answers and base64 blobs, and put the voice notes in the prose section. Confirm the path you wrote to and tell the user they can hand-edit it any time or re-run `/brand-setup`.

## Encoding helper

Base64-encode an image or font file with the buyer's available tooling. On Windows PowerShell:
`[Convert]::ToBase64String([IO.File]::ReadAllBytes("path"))`. Strip newlines before pasting into the YAML value.

## Do not

- Do not write GW / Gridiron Warrior values as defaults. The engine is white-label; the only brand is the buyer's.
- Do not proceed to generate a carousel from this skill — hand back once the profile is written.
