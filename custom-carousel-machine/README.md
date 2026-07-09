# The Custom Carousel Machine

A white-label Instagram carousel engine for Claude Code. Generate editable, export-ready IG carousels as a single self-contained HTML file — wearing **your** brand, not anyone else's.

## What it does

- Produces one self-contained HTML file: 5–10 slides at 4:5 (1080×1350 on export), every text field click-to-edit, one-click PNG and Canva-PDF export, a save-to-disk button, and inline font-resize controls.
- Reads your **Brand Profile** (palette, fonts, logo, handle, voice) so every carousel comes out in your look.
- Ships two **starter Style Packs** (Mono Series, Editorial Long-Form). You author the rest — describe a look, optionally drop in a 1–3 image moodboard for direction, and the engine writes a new pack into your project.

See `examples/` for two real carousels the engine produced from one sample brand.

## Install

**Free / your own use — via marketplace:**
```
claude plugin marketplace add <your-marketplace-repo>
claude plugin install custom-carousel-machine@<your-marketplace>
```

**Paid — zip download (Gumroad / Thinkific):** unzip anywhere, then copy the three folders **inside** the `skills/` folder — `carousel`, `brand-setup`, and `pack-author` — into `~/.claude/skills/` (Windows: `C:\Users\YOURNAME\.claude\skills\`). Claude Code discovers personal skills only at `~/.claude/skills/<skill-name>/SKILL.md`, so the skill folders must sit directly under `skills/`, not nested inside a `custom-carousel-machine` folder. Restart Claude Code afterward. Price: **$27**.

There is no license key and no phone-home. The engine runs identically whether it was given away or bought. Don't redistribute what you didn't pay for.

## First run

1. Run **Brand Setup** (`/brand-setup` or just say "set up my brand"). It interviews you once and writes `carousel/brand-profile.md` into your current project, base64-baking your logo (and any custom font) so your files stay portable.
2. Make a carousel: "make me a carousel about X." Pick a style pack, approve the slide plan, export.
3. Author a new pack any time: "build me a new style pack" — describe the look, optionally attach 1–3 inspiration images.

## Fonts

Defaults are **Roboto Slab** (display) and **Barlow** (body), both free to redistribute, loaded from Google Fonts. To use your own brand font, point Brand Setup at the font file; it gets base64-baked into your Brand Profile. **You are responsible for the license of any font you supply.**

## What lives where (important for updates)

- **The engine** (this plugin folder): skills, starter packs, the Brand Profile *template*. Updates overwrite this.
- **Your data** (your project, `carousel/`): your `brand-profile.md` and any packs you author. Updates never touch this.

See [UPDATING.md](./UPDATING.md). See `docs/adr/` in the source repo for why it's built this way.
