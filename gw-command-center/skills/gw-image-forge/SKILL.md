---
name: gw-image-forge
description: "Generate a photographic-realism PNG image for Gridiron Warrior via the OpenAI Images API (gpt-image-1). The north star is a documentary photograph, not an AI image. Use this skill whenever Scott provides a subject or concept and wants an image. Trigger on phrases like 'generate an image', 'make me an image for', 'image forge', 'create an image', 'build me an image for', or any request to produce image gen output for Gridiron Warrior or Scott Leech Training. Defaults to 1987 Sports Illustrated B&W aesthetic. Switches to color (1990s NCAA media guide or modern D1 athletic comms) when Scott says 'color', 'in color', or 'full color'."
---

# GW Image Forge

Build photo-editor prompts for `gpt-image-1`. The north star is **a documentary photograph**, not an AI image of someone's idea of an image. The test is one question:

> Could this image have appeared in a 1987 Sports Illustrated feature, a 1996 NCAA media guide, or a 2026 university athletic communications release?

If the answer is no, the prompt is wrong. Rewrite.

This skill writes prompts the way a photo editor describes an existing photograph — not the way a designer pitches an idea.

---

## What This Skill Does

1. Take Scott's raw concept (one sentence or phrase)
2. Pick an era preset (1980s SI / 1990s NCAA / 2000s ESPN / modern D1) — ask only if ambiguous
3. Build a 5-block prompt: **Subject · Environment · Camera · Medium · Exclusions**
4. Roll 1–3 imperfection variables in
5. Append the **Reality Layer** verbatim
6. Write the config JSON, shell `python scripts/generate.py --config -`
7. Report the PNG path

---

## Banned Words (NEVER USE)

These were useful for AI prompts in 2023. Today they create the exact "AI look" we are trying to avoid. The model trains on prompts containing these words and the output is a tell.

`cinematic` · `epic` · `masterpiece` · `trending on artstation` · `hyper detailed` · `hyper realistic` · `ultra detailed` · `highly detailed` · `8k` · `4k` · `octane render` · `unreal engine` · `dramatic lighting` · `volumetric lighting` · `award winning` · `breathtaking` · `stunning` · `beautiful` · `aesthetic` · `mood lighting` · `bokeh` (as descriptor) · `depth of field` (use camera spec instead) · `studio quality` · `professional photography` · `dynamic` · `striking`

Also banned: any "more X" descriptor. The prompt describes what IS, not what should be added.

---

## Era Presets

Pick one based on Scott's concept. When ambiguous, ask:

> "1980s SI, 1990s NCAA media guide, 2000s ESPN Magazine, or modern D1 athletic comms?"

### Preset A — 1980s Sports Illustrated (default for legacy GW look)

**Medium block (use verbatim):**
> Sports Illustrated assignment photograph, late 1980s, Tri-X 400 negative scan, black and white, editorial framing.

**Camera defaults:**
- 35mm prime, knee-height to chest-height angle
- Available light + occasional flash falloff
- Slight softness from negative grain, not lens softness

### Preset B — 1990s NCAA Media Guide

**Medium block (use verbatim):**
> NCAA media guide team photograph, mid-1990s, color negative film, direct on-camera flash, practical lighting, lower contrast than modern stock.

**Camera defaults:**
- 50mm, eye-level
- Direct on-camera flash visible
- Flat, document-style composition

### Preset C — 2000s ESPN Magazine

**Medium block (use verbatim):**
> ESPN Magazine sports photograph, mid-2000s, color, controlled strobes, sharper rendering than film stock, editorial composition.

**Camera defaults:**
- 24–70mm zoom, knee height
- Studio strobes with visible falloff
- Cleaner composition than 80s SI

### Preset D — Modern D1 Athletic Communications (default for modern GW look)

**Medium block (use verbatim):**
> University athletic communications department photograph, 2026, color, controlled strobes, sharper rendering, recruiting-graphic style.

**Camera defaults:**
- 35mm or 85mm, low angle
- Shallow focus from aperture spec, not "shallow depth of field"
- Clean composition with brand-safe negative space

---

## Prompt Block Structure (5 Blocks, In This Order)

Build the prompt with EXACTLY these labeled sections. The model parses them better when they are explicit.

```
Subject: [physical description of what is in the photograph]
Environment: [the location, time of day, surface, weather]
Camera: [focal length, angle, lighting source]
Medium: [the era preset's Medium block, verbatim]
Exclusions: [no HDR, no stylization, no AI rendering, plus mode-specific exclusions]
```

### Subject Block

Describe a real person doing a real thing. Physical, observable, no abstractions.

- Bad: "a strong football player"
- Good: "a defensive lineman in two-point stance, arms loaded with chalk, jersey untucked, no helmet"

**No faces visible.** Frame from chest down, use back angles, profiles, motion blur, partial crops, or environment focus. This is both a safety rule (no real person identity) and a realism rule — real action photography rarely catches a clean front-facing portrait of a moving athlete.

### Environment Block

Where, when, what surface, what time of day. Specific.

- Bad: "in a weight room"
- Good: "the West End strength and conditioning room at 5am, fluorescent overhead lights, scuffed rubber flooring, painted concrete block walls"

### Camera Block

Focal length + angle + lighting source. No technical jargon beyond what a photo editor writes on an assignment slip.

- Bad: "shallow depth of field with cinematic bokeh"
- Good: "35mm prime, knee height, available fluorescent light, no flash"

### Medium Block

Copy the era preset Medium block VERBATIM. Do not edit. Do not paraphrase.

### Exclusions Block

Always include:
> no HDR, no stylization, no AI rendering, no cinematic effects, no dramatic lighting, no octane render, no oversaturation, no visible faces

Add mode-specific exclusions:
- **B&W mode:** also include `no color, no color tinting, no warm tones, no golden hour`
- **Color mode:** also include `no neon, no oversaturated colors, no Instagram-style filter, no cinematic color grade`

---

## Imperfection Variables (Roll 1–3)

After the 5 blocks, append 1–3 of these. Pick randomly. Vary across runs — don't always grab the same three.

```
- slight motion blur on the trailing limb
- imperfect framing with subject slightly off-center
- subject partially cropped at the frame edge
- flash falloff darkening the background
- film softness, not lens softness
- focus landing slightly behind the subject
- uneven overhead lighting
- wrinkled jersey
- chalk residue on hands and forearms
- sweat stains on the shirt
- visible breath in cold air
- a piece of equipment intruding into the frame
- one stray detail (water bottle, towel, spotter's hand) at the frame edge
- fingerprint on the lens producing a soft area in one corner
- mis-timed shutter catching the athlete mid-grimace
- a coach's clipboard or stopwatch in the foreground out of focus
```

Real photography contains flaws. AI photography removes them unless instructed otherwise. This is the single highest-leverage change in the prompt structure.

---

## Reality Layer (Always Append, Verbatim)

After the 5 blocks + imperfection variables, append this paragraph EXACTLY:

> Documentary sports journalism photograph. Captured during a real training session. Authentic imperfections. Looks accidental rather than designed. If forced to choose between realism and visual impact, prioritize realism.

This paragraph does more work than 200 words of style descriptors. Do not edit. Do not paraphrase. Do not abbreviate.

---

## Modes

### B&W (Default)

Era preset: **A** (1980s SI) unless Scott specifies otherwise.

Mode-specific exclusions: `no color, no color tinting, no warm tones, no golden hour`

### Color

Triggered by "color", "in color", "full color" in Scott's prompt.

Era preset: **D** (Modern D1) by default — could also be **B** (1990s NCAA) or **C** (2000s ESPN). Ask if ambiguous.

Mode-specific exclusions: `no neon, no oversaturated colors, no Instagram-style filter, no cinematic color grade`

---

## Platform Sizes

| Platform | size value | aspect | extra Camera note |
|---|---|---|---|
| Instagram post / square | `1024x1024` | 1:1 | none |
| Instagram story / portrait | `1024x1536` | 2:3 | vertical composition |
| Twitter/X header / landscape | `1536x1024` | 3:2 | wide framing |
| YouTube thumbnail | `1536x1024` | 3:2 | "subject placed left third, right third clean for title text overlay" |
| Default if unstated | `1024x1024` | 1:1 | none |

---

## Full Example

**Scott says:** "make me an image for the Contact Prep course landing page"

**Constructed prompt:**

```
Subject: two football players in a standing combative drill, locked at shoulder pads, arms framing each other's chest, helmets off, no faces visible, jerseys untucked. One is mid-stride forward, the other rooted.

Environment: the West End strength and conditioning room at 5am, fluorescent overhead lights, painted concrete block walls, scuffed rubber mat surface, steel structural column at the frame edge.

Camera: 35mm prime, knee height, available fluorescent light, no flash. Soft shadow detail in the corners.

Medium: Sports Illustrated assignment photograph, late 1980s, Tri-X 400 negative scan, black and white, editorial framing.

Exclusions: no HDR, no stylization, no AI rendering, no cinematic effects, no dramatic lighting, no octane render, no oversaturation, no visible faces, no color, no color tinting, no warm tones, no golden hour.

Imperfections: slight motion blur on the trailing arm. Chalk residue on both pairs of forearms. A water bottle just visible at the lower right frame edge.

Documentary sports journalism photograph. Captured during a real training session. Authentic imperfections. Looks accidental rather than designed. If forced to choose between realism and visual impact, prioritize realism.
```

**Config JSON to shell:**

```json
{
  "name": "contact-prep-combatives",
  "prompt": "Subject: two football players ... [full prompt as constructed above, joined as a single string]",
  "size": "1024x1024",
  "quality": "high",
  "n": 1
}
```

**Shell:** `python scripts/generate.py --config -`

---

## Workflow

1. Read Scott's concept
2. If platform ambiguous, ask one question: "What platform?"
3. If mode ambiguous, default to B&W (Preset A). Only switch to color if Scott says "color", "in color", or "full color"
4. Pick era preset (A by default for B&W, D by default for color). Ask only if Scott's concept suggests a different era
5. Build the 5 blocks
6. Roll 1–3 imperfection variables — vary the picks across runs
7. Append the Reality Layer paragraph (verbatim)
8. Show Scott the constructed prompt
9. If Scott wants to iterate: shell with `--dry-run` first (costs $0)
10. When he approves: shell live, write the PNG, report the path

**Do NOT ask clarifying questions about style descriptors.** The era preset locks the look. Only ask about platform, mode, or era when truly ambiguous.

---

## Dry-Run Mode (No-Cost Iteration)

Add `--dry-run` to the shell call to validate the config and print the constructed prompt **without calling the OpenAI API**. Costs $0. Useful when:

- Scott wants to see the prompt you'd send before paying for the render
- You're iterating on prompt construction and don't need a real image yet
- You want to confirm the size, quality, and output path are right

```bash
echo '<config json>' | python "C:/Claude Projects/plugins/gw-command-center/skills/gw-image-forge/scripts/generate.py" --config - --dry-run
```

Returns JSON with `mode: "dry-run"`, the full constructed prompt, prompt length, target output path, and API endpoint that would be hit. No PNG is written.

Run live only when Scott confirms the dry-run prompt looks right.

---

## Errors

The script returns nonzero exit codes:

- `2` — config validation failed (bad JSON, missing required key, invalid size/quality, etc.)
- `3` — `OPENAI_API_KEY` missing from `C:\Claude Projects\Gridiron Warrior\scripts\.env`
- `4` — OpenAI API call failed (network, HTTP error, or empty response)

On `3`, tell Scott to add the key to the .env file. Don't try to work around it.

On `429` (rate limit), the script retries once automatically with 5s backoff before failing.

---

## North Star (read this last, every time)

> Could this image have appeared in a 1987 SI feature, a 1996 NCAA media guide, or a 2026 university athletic communications release?

- If yes → ship it.
- If no → rewrite the Subject, Environment, or Camera block. Do NOT add style descriptors. Do NOT reach for the banned words. The fix is always more concrete description and more imperfection, never more "polish".

The aesthetic Scott is chasing is **a real photograph that was taken**, not **an image that was rendered**. Every prompt should obey that distinction.
