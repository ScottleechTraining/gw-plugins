---
# BRAND PROFILE — the single source of your identity. The engine reads this every run.
# Brand Setup writes a filled copy to your project at: carousel/brand-profile.md
# Edit by hand any time, or re-run /brand-setup.

brand_name: "Your Brand"
handle: "@yourhandle"

# PALETTE — the engine paints Style Pack "palette roles" with these.
# Use hex. ink = darkest type, paper = light background, dark = dark background.
palette:
  ink: "#1A1A1A"
  paper: "#F5F0E8"
  dark: "#1A1A1A"
  accent_primary: "#C8A84E"
  accent_secondary: "#3A3A3A"

# FONTS — defaults are free and load from Google Fonts. To use your own font,
# set source: baked and Brand Setup fills custom_base64 from your font file.
# You are responsible for the license of any font you supply.
fonts:
  display:
    family: "Roboto Slab"
    source: google        # google | baked
    custom_base64: ""      # filled by Brand Setup when source: baked
  body:
    family: "Barlow"
    source: google
    custom_base64: ""

# LOGO — base64-baked by Brand Setup so output files stay portable.
# Leave empty to fall back to the handle text in the footer.
logo:
  base64: ""
  alt: "Your Brand logo"

# VOICE — defaults the engine writes copy with. These are yours, not anyone else's.
voice:
  tone: "direct"          # direct | professional | playful | minimal
  no_em_dashes: false     # set true if your brand bans em-dashes
  banned_words: []        # words the engine must never use
---

## Voice notes

Write a few sentences in your own words about how your captions and headlines should sound.
The engine reads this prose alongside the structured fields above. Examples:

- Short sentences. Active verbs. Talk to the reader like a peer.
- Lead with the payoff, not the setup.
- (Anything specific to how YOU write.)
