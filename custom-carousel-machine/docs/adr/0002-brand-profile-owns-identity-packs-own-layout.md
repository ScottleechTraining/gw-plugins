# Brand Profile owns identity; Style Packs own layout

White-label requires that any buyer's brand can be applied to any layout. The internal skill's six style packs entangle brand identity (hardcoded asphalt/gold/paper hex, `@Sleech72` in Mono Series' header, the TGW logo) with layout architecture (Mega-Cover, hero-photo, ghost numbers, reading columns) inside each pack.

Decision: split the two. The Brand Profile owns identity — palette (ink, paper, dark, primary + secondary accent), fonts, logo, handle, voice defaults. A Style Pack is pure layout: it references semantic Palette Roles (`--accent`, `--bg-dominant`, `--fg-dominant`), never literal hex, so applying a brand to a pack makes the pack wear that brand.

Escape hatch: a Style Pack may override a single Palette Role only when the color is the pack's defining identity (a pack whose whole point is one pop color, or a pack defined by having no accent). The existing `:root` semantic-token CSS is the seam this split builds on.
