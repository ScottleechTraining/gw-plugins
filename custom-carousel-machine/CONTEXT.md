# IG Carousel Product (white-label)

A productized, white-label version of Scott's internal `ig-carousel` skill: a brand-agnostic engine other creators install to generate their own Instagram carousels under their own brand, never Gridiron Warrior's.

## Language

**Engine**:
The brand-agnostic carousel-generation logic — slide templates, layout rules, editable HTML output, PNG/PDF export. Knows nothing about any specific brand.
_Avoid_: skill, tool, command (too vague for the sellable artifact)

**Brand Profile**:
The single owner of brand identity the Engine reads: palette (ink, paper, dark, primary + secondary accent), fonts, logo, social handle, voice defaults. Replaces everything currently hardcoded to Gridiron Warrior.
_Avoid_: brand kit, theme, config

**Style Pack**:
Pure layout and architecture — slide templates, type treatment, photo handling — referencing palette roles rather than literal colors, so any Brand Profile applied to it makes it wear that brand. Two de-branded starter packs ship (Mono Series and Editorial Long-Form); buyers author the rest themselves via AI-assisted authoring.
_Avoid_: template, preset, theme

**Palette Role**:
A semantic color slot a Style Pack paints with (accent, bg-dominant, fg-dominant, paper, ink). The Brand Profile supplies the actual color for each role. A pack may override one role only when that color is the pack's defining identity.
_Avoid_: token, variable, swatch

**Brand Setup**:
The guided first-run step that interviews a buyer and writes their Brand Profile, base64-baking the logo (and any custom fonts) into the file. The Profile is the source of truth; Setup is onboarding so a buyer never edits raw YAML to get started.
_Avoid_: onboarding, wizard, install

**Inspiration Image**:
A reference design (NOT carousel content) a buyer supplies during pack authoring to set a new Style Pack's direction. One to three form a Moodboard. The Engine derives abstract direction from them and never reproduces them; the Brand Profile still supplies all color, font, and logo.
_Avoid_: reference, mockup, sample, content photo

**White-label**:
The buyer's carousels carry the buyer's brand, never Gridiron Warrior's. The GW look exists only as Scott's own private Brand Profile and is never shipped inside the product.
