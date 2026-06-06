---
name: gw-image-forge
description: Generate a PNG image for Gridiron Warrior via the OpenAI Images API (gpt-image-1). Use this skill whenever Scott provides a subject or concept and wants an image. Trigger on phrases like "generate an image", "make me an image for", "image forge", "create an image", "build me an image for", or any request to produce image gen output for Gridiron Warrior or Scott Leech Training. Defaults to B&W editorial aesthetic (SI 1987, Tri-X 400, chiaroscuro, no faces). Switches to cinematic color mode when Scott says "color", "in color", or "full color".
---

# GW Image Forge

Converts Scott's raw subject/concept into a fully constructed prompt and ships it through OpenAI's `gpt-image-1` model to produce a PNG. Two modes: B&W editorial (default) and cinematic color. Scott provides the subject and optional mode. The skill handles the rest.

---

## What This Skill Does

1. Takes Scott's raw concept (one sentence or phrase)
2. Detects mode: B&W (default) or color (if Scott says "color", "in color", "full color")
3. Asks for platform/aspect ratio if not provided
4. Builds the full structured prompt with the locked-in GW aesthetic
5. Writes a config JSON, shells `python scripts/generate.py --config -`, and reports the resulting PNG path
6. PNG lands in `D:\Claude Projects\Gridiron Warrior\Images\`

**Expect a wait** — `quality: "high"` takes ~30 seconds. Tell Scott "generating, give it ~30s" before the shell call so it doesn't feel hung.

---

## MODE 1: B&W Editorial (Default)

Use this unless Scott explicitly requests color. This is the primary GW look.

### Locked-In B&W Style Guide

```
Sports Illustrated 1987 editorial photograph
Tri-X 400 black and white film grain
Low-key chiaroscuro lighting
Desaturated steel grays and deep blacks
Blue hour or 5am pre-dawn atmosphere
Volumetric light with visible dust particles and breath condensation
Aggressive bokeh with sharp foreground subject
Cinematic wide-angle OR extreme macro (pick based on subject)
Industrial textures throughout
No visible faces — no portraits, no eyes, no recognizable facial features
```

### B&W Style Opener (always this exact phrase)
```
Sports Illustrated 1987 editorial photograph, Tri-X 400 black and white film grain,
```

### B&W Quality Line
```
ultra detailed, photographic grain texture, high contrast blacks and whites, cinematic depth of field
```

### B&W Lighting Line
```
low-key chiaroscuro lighting, volumetric light shafts with visible dust particles and breath condensation, blue hour atmosphere, deep blacks with single hard overhead light source
```

---

## MODE 2: Cinematic Color

Triggered when Scott says "color", "in color", or "full color". Keeps all structural elements of the GW look — chiaroscuro, industrial, no faces, pre-dawn — but switches to a muted cinematic color grade. Not vivid. Not bright. Think Kodak Vision 500T, not Instagram filter.

### Color Palette Logic
The GW palette for cinematic color images:
- **Shadows:** cool steel blue and slate gray
- **Practical lights (overhead weight room, stadium):** tungsten amber and warm orange — this is the one place warmth is allowed
- **Midtones:** desaturated and muted, pulled toward gray
- **No lifted blacks** — shadows stay deep and crushed

### Color Style Opener
```
Cinematic editorial photograph, Kodak Vision 500T color film stock, muted desaturated color grade,
```

### Color Quality Line
```
ultra detailed, Kodak film grain texture, cinematic color grade with crushed blacks, desaturated mids, tungsten warm accent light, cinematic depth of field
```

### Color Lighting Line
```
low-key chiaroscuro lighting with muted cinematic color, cool blue shadows, tungsten amber from practical overhead lights, volumetric light shafts with visible dust particles and breath condensation, 5am pre-dawn atmosphere, deep crushed blacks with single warm practical light source
```

---

## Platform Presets

Ask Scott which platform this is for if not stated. Default to Instagram post (square) if unclear.

| Platform | size | Prompt suffix |
|---|---|---|
| Instagram post (1:1) | `1024x1024` | centered subject, text-safe zone at bottom 20% |
| Instagram story (9:16) | `1024x1536` | vertical composition, text-safe zones top and bottom 15% |
| Twitter/X header (16:9) | `1536x1024` | wide cinematic frame, subject left third, right side open |
| YouTube thumbnail (16:9) | `1536x1024` | bold subject placement, high contrast, space for title text |
| Web banner / general landscape | `1536x1024` | gradient fade right 40% for text overlay |
| Print / general (1:1) | `1024x1024` | full frame composition, no text zones needed |

---

## Fixed Parameters for GW Aesthetic

These are always used unless Scott specifically asks for variation:

```json
"quality": "high",
"n": 1
```

**Why `high`:** Film grain and chiaroscuro depth require the higher-quality render. Standard quality flattens the grain structure and shadow detail.

---

## Negative Guidance (Folded Into Prompt)

`gpt-image-1` does not accept a `negative_prompt` parameter. The negative IP is preserved by appending an `Avoid:` suffix to the main prompt. Always include this exact phrase at the END of the constructed prompt:

```
Avoid: visible face, portrait face, eyes looking at camera, blurry, low quality, distorted, watermark, text overlay, logo, cartoon, anime, illustration, deformed, ugly, noise artifacts, overexposed.
```

For B&W mode, prepend `color, colorful, vivid colors, saturation, warm tones, golden hour, orange` to the Avoid list.

For color mode, prepend `black and white, grayscale, monochrome, oversaturated, neon, bright pop colors` to the Avoid list.

---

## Prompt Construction Formula

Build the prompt in this exact order. Each section is required. Use the B&W or color variants for the opener, lighting, and quality lines depending on mode.

```
[STYLE OPENER] + [SUBJECT] + [ENVIRONMENT] + [CAMERA] + [LIGHTING] + [TEXTURE DETAILS] + [MOOD] + [QUALITY] + [PLATFORM SUFFIX] + [AVOID SUFFIX]
```

### Style Opener
Use the B&W opener (Mode 1) or color opener (Mode 2) from the relevant section above.

### Subject
Translate Scott's concept into a concrete visual subject. Make it specific and physical. No abstract concepts.

- "linemen in pass protection" → "two offensive linemen mid-drive in a three-point stance, padded arms extended, no faces visible"
- "early morning conditioning" → "football cleats digging into frosted turf, legs in motion, silhouetted against pre-dawn sky"
- "weight room grind" → "chalk-dusted barbell loaded with iron plates on a rack, no hands visible, industrial weight room background"

### Environment
Physical, specific. Avoid generic "football field." Use: frosted turf, rubber flooring, concrete walls, chain-link fence, stadium tunnel, under the bleachers, empty field at dawn.

### Camera
Pick ONE: cinematic wide OR extreme macro. Do not mix.

- **Wide:** "low-angle 24mm wide shot" or "35mm medium-wide, slightly elevated"
- **Macro:** "100mm extreme macro" or "85mm tight close-up with aggressive background separation"

If the subject is equipment, texture, or environment → macro.
If the subject involves players or space → wide.

### Lighting
Use the B&W lighting line (Mode 1) or color lighting line (Mode 2) from the relevant section above.

### Texture Details
Add 2-3 specific materials relevant to the subject. Examples: chrome barbell knurling, matte rubber flooring, worn leather chinstrap, chain-link mesh, concrete block wall, painted steel rack.

### Mood
Always (both modes): "raw editorial sports journalism mood, gritty and physical, no sentimentality"

### Quality
Use the B&W quality line (Mode 1) or color quality line (Mode 2) from the relevant section above.

### Platform Suffix
Add the appropriate suffix from the Platform Presets table.

### Avoid Suffix
Append the Avoid phrase from the "Negative Guidance" section, prepended with the mode-specific terms.

---

## How It Ships

Build a config dict, then shell the generator:

```json
{
  "name": "[kebab-case-slug-from-subject]",
  "prompt": "[full constructed prompt as a single string]",
  "size": "[1024x1024 | 1024x1536 | 1536x1024]",
  "quality": "high",
  "n": 1
}
```

Then:

```bash
echo '<config json>' | python "D:/Claude Projects/plugins/gw-command-center/skills/gw-image-forge/scripts/generate.py" --config -
```

Or write the config to a temp file and pass `--config <path>`.

On success the script prints `{"paths": ["D:\\...\\name.png"]}` to stdout. Surface that path back to Scott so he can open it.

### Filename convention

- `n: 1` → `{name}.png`
- `n: 2..4` → `{name}_1.png`, `{name}_2.png`, ...

The `name` field must be a kebab-case slug: `linemen-pass-pro`, `weight-room-dawn`, `contact-drill-macro`.

### Output location

All PNGs land in `D:\Claude Projects\Gridiron Warrior\Images\`.

---

## Example: Full Input to Output

**Scott says:** "make me an image for the Contact Prep course landing page — two players in a combative drill"

**Platform:** Instagram post (square)

**Config JSON:**
```json
{
  "name": "contact-prep-combatives",
  "prompt": "Sports Illustrated 1987 editorial photograph, Tri-X 400 black and white film grain, two football players in a standing combative drill, torsos and arms locked in contact, no faces visible, helmet and shoulder pad textures prominent. Empty weight room concrete floor, industrial steel columns, rubber mat surface. Low-angle 35mm medium shot with aggressive foreground separation. Low-key chiaroscuro lighting, volumetric light shafts with visible dust particles and breath condensation, blue hour atmosphere, deep blacks with single hard overhead light source. Worn leather chinstrap, matte rubber mat, painted steel structural column. Raw editorial sports journalism mood, gritty and physical, no sentimentality. Ultra detailed, photographic grain texture, high contrast blacks and whites, cinematic depth of field. Centered subject, text-safe zone at bottom 20%. Avoid: color, colorful, vivid colors, saturation, warm tones, golden hour, orange, visible face, portrait face, eyes looking at camera, blurry, low quality, distorted, watermark, text overlay, logo, cartoon, anime, illustration, deformed, ugly, noise artifacts, overexposed.",
  "size": "1024x1024",
  "quality": "high",
  "n": 1
}
```

**Output:** `D:\Claude Projects\Gridiron Warrior\Images\contact-prep-combatives.png`

---

## Workflow

1. Read Scott's concept prompt
2. Detect mode (B&W default, color on trigger phrases)
3. If platform is missing, ask one question: "What platform is this for?" with the options from the table
4. Build the prompt using the formula above
5. Tell Scott "generating, give it ~30s"
6. Shell the generator script with the config
7. Surface the returned PNG path back to Scott

Do not ask clarifying questions about style — the aesthetic is locked. Only ask about platform if it's genuinely ambiguous.

---

## Multiple Variants

If Scott asks for multiple variants (e.g., "give me 3 versions"), set `n: 3` in a single config. OpenAI returns 3 distinct images. They're saved as `{name}_1.png`, `{name}_2.png`, `{name}_3.png`. Max `n` is 4.

If Scott wants the variants to differ in framing or subject angle (not just random reroll), run separate calls with slightly modified prompts — different camera distances, different environment details. Keep style locked across all variants.

---

## Errors

The script returns nonzero exit codes:

- `2` — config validation failed (bad JSON, missing required key, invalid size/quality, etc.)
- `3` — `OPENAI_API_KEY` missing from `D:\Claude Projects\Gridiron Warrior\scripts\.env`
- `4` — OpenAI API call failed (network, HTTP error, or empty response)

On `3`, tell Scott to add the key to the .env file. Don't try to work around it.

On `429` (rate limit), the script retries once automatically with 5s backoff before failing.
