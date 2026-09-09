---
name: gw-carousel-batch
description: "Batch-build IG carousel HTML for multiple content packs in parallel. Run bare (no arguments) to discover every content pack still waiting on a carousel; the style-pack recommendation is used without confirmation. Central photo assignment, ~5 subagents per wave, mandatory render-and-eyeball verification of every cover before done. Runs nightly at 3:00am as the gw-carousel-batch scheduled job, and on demand."
model: claude-opus-5
---

# /gw-carousel-batch — Parallel IG Carousel Builds

Orchestrates many carousel builds at once. Photo assignment is centralized so no two carousels share a hero. Every cover is rendered and eyeballed before the batch is called done. Each subagent runs the canonical `ig-carousel` skill.

## 1. Input

Two ways in:

**A. Explicit list.** A list of content-pack folders (from `Deliverables/ready/` or `Deliverables/_inbox/`) or slugs, plus the style pack chosen for each carousel.

**B. No arguments — discovery mode.** This is the standing "what's waiting on a carousel" entry point (Louis runs it bare, see `Deliverables/LOUIS-NOTE.md`). Four kinds of waiting work:

1. **New builds:** scan `Deliverables/_inbox/` and `Deliverables/ready/` for every topic folder that has a `*content-pack*.md` but no `*-carousel.html`. For each, recommend a style pack: read the "Pack selection quick-reference" table in the ig-carousel skill's `references/style-packs.md` and match the pack's title/hook keywords against it. Present one table (slug, title hook, recommended pack, why) and build on the recommendations immediately. Do not wait for confirmation (Scott 2026-08-12: the review page's restyle dropdown is the correction path, so a wrong pack costs one rebuild, not a blocked batch).
2. **Restyle rebuilds:** topics in `queue-state.json` where `carousel_needs_polish` is true and `polish_note` starts with `restyle: <Pack Name>` (optionally followed by `. user note`). The dropdown choice is confirmed. For new-format decks, use `--restyle-from EXISTING_HTML` to preserve the saved master exactly; only legacy rebuilds read copy from the content pack. Clear nothing yourself; /gw-review re-judges the result and SHIP clears the polish flag.
3. **Cover rebuilds:** topics where `carousel_needs_polish` is true and `polish_note` starts with `cover:`. Rebuild ONLY slide 1 per the note (new treatment and/or photo from the ig-carousel skill's `references/cover-treatments.md`); body slides stay untouched.
4. **Action rerolls:** new-format topics with `carousel_needs_polish` and an `action: save|share|conversation|conversion` note, optionally followed by `. user note`. Discover alongside style notes, without asking again. Read the saved master, redraft brief/body/caption/CTA together for that action, and build with `--rewrite-from EXISTING_HTML --copy NEW_JSON`. Preserve deck/variant/source identity and require new review; changing just the final ask is not a reroll.

Follow the capability gate and lifecycle in [copy-record.md](../skills/ig-carousel/references/copy-record.md), the single schema contract. Scott enabled creation on 2026-09-08; when capabilities report `enabled: true`, Forge supplies copy records automatically for NEW decks. Use that explicit copy input or the existing HTML schema marker, not discovery/plugin version alone. Existing managed decks remain editable/rerollable even if creation is later disabled. If helpers are missing, report managed work as pending without stripping its marker or falling back to unmanaged output; continue unrelated legacy work. No per-post opt-in question, no settings edits from this command, and no existing-deck migration.

If nothing is waiting in any bucket, say so, print the completion marker (section 6), and stop.

For initial new-format builds, consume the topic's `carousel-build.json` from
Forge as the selected schema-1 handoff. Verify its variant matches the same
source-pack brief, slides, caption, and CTA; do not reselect or build both
variants. Produce one selected HTML master. Old unbuilt packs without explicit
new schema stay legacy, even with creation enabled; do not manufacture JSON for
them during discovery. Once HTML exists, use its saved master, not the initial
JSON, for subsequent work.
JSON, for subsequent work.

Save-led decks: for an initial build whose `carousel-build.json` brief is `save`, and for an explicit `action: save` reroll, apply the ig-carousel skill's `references/save-reference-slides.md`. Verify one reference body slide exists in the copy, that its rendered PNG reads standalone at phone size, and that CTA and caption name the same later use. On an `action: save` reroll where the saved master's source cannot support a usable card, do not build: leave the master and the polish note untouched, report the slug as REPAIR NEEDED naming what the source lacks, and continue other topics. Style-only rebuilds and cover rebuilds never retrofit a card. Legacy decks and existing managed decks are untouched unless Scott asks for an editorial rewrite.

Share-led decks: for an initial build whose `carousel-build.json` brief is `share`, and for an explicit `action: share` reroll, apply the ig-carousel skill's `references/share-led-decks.md`. A save-to-share reroll rewrites the argument, body, caption, and CTA together while keeping deck, variant, and source identity; a prior reference card stays only if it still serves the shared decision. On an `action: share` reroll where the saved master's source names no plausible recipient or joint decision, do not build: leave the master and the polish note untouched, report the slug as REPAIR NEEDED naming what is missing, and continue other topics. Style-only rebuilds never insert share framing. Existing share decks are not retrofitted.

Teaching progression: an explicit action reroll may change the approach recorded in `brief.reason` when the new action needs it (see the ig-carousel skill's `references/rhetorical-approaches.md`); record the new one the same way and require fresh review. Style-only and cover rebuilds never change it or the words. No existing deck is retrofitted to a new approach.

Pack rules for both modes:

- Explicit list mode: the pack Scott named wins.
- Otherwise the quick-reference recommendation IS the pack, attended or not. If no row clearly matches, pick the closest fit and flag that slug in the summary table so Scott knows to look at it at review.
- Two-row ties resolve by the photo-forward tiebreak in `references/style-packs.md` (photo pack wins), subject to its rotation guard: read `style_pack` off the last 6 built topics in `queue-state.json` first, and if neither Editorial Long-Form nor Mono Series is among them, suspend the tiebreak for this batch. Say which way the guard went in the assignment table.

Build the slugs in the assignment table and stop there. Do not restyle carousels nobody flagged or edit source content packs. Report capability-blocked or failed slugs explicitly, never as completed. Style-only and cover-treatment changes preserve all saved wording, caption, and CTA; an explicit action note is the copy-rewrite route.

## 2. Photo assignment (centrally, FIRST)

Before spawning any agents:

1. List available photos in `C:\IMAGES\Football` and `C:\IMAGES\Gym`.
2. Pick TWO photos per carousel, matched to the topic: a hero for the cover and a body photo for one body slide (photo floor, `references/style-packs.md`). Prefer a landscape body photo so it can carry a two-slide seamless spread. Mono Series carousels get a hero only.
3. Never assign the same photo to two carousels in the batch, hero or body.
4. Record the full assignment table (slug, style pack, content-pack path, hero photo path, body photo path) before anything is spawned. This table is the source of truth for the whole run.

## 3. Build (spawn subagents at 3+ carousels)

One or two carousels: build them yourself, no agents. Three or more: spawn one agent per carousel, at most 5 running at once, next wave after the current one verifies.

Each subagent builds ONE carousel using the `ig-carousel` skill. Spawn with `model: sonnet` set explicitly on every agent (never inherit).

Give each subagent:
- the content-pack path
- the mode (legacy, initial opted-in build, saved-master restyle, or action rewrite), explicit selected variant, and saved HTML/copy input paths as applicable; use the assembler API in `copy-record.md`
- the Forge's pre-draft brief for initial opted-in work; honor its action and archetype rather than overriding it with a generic seven-slide outline. If absent on explicitly opted-in input, select automatically by the contract before drafting; no overnight question
- the chosen style pack
- the chosen cover treatment (from the ig-carousel skill's `references/cover-treatments.md` quick-reference, matched to the topic and the photo's character; Type Plate is the fallback when the photo can't carry a treatment)
- the assigned hero photo path AND the assigned body photo path
- the photo floor: the cover carries the hero and one body slide carries the body photo, each per the pack's own photo treatment and sizing in `references/style-packs.md` (Mono Series exempt: hero only). If the body photo is landscape, run it as a two-slide seamless spread per `references/seamless-image-spread.md`; otherwise a single photo slide. A build that drops the body photo is a bounce, not a fallback.
- the instruction to prepare every photo as a brightened ~230KB JPEG (quality ~80, resized to slide dimensions, pack treatment baked with Pillow), never a PNG
- the instruction to kill any server or browser process it starts, even on failure
- the copy-source rule: initial/legacy slide text comes from the selected pack carousel's "Slide Text" section, with its paired Caption. For new-format restyles the saved HTML master wins, not the pack; action rewrites start from that master and the explicit note. Pack meta (Carousel Brief, THE MESSAGE, PULLED FROM THE BRAIN, Cross-Reference Summary, frontmatter, cta_rationale) NEVER appears on slides or in captions. Report failed message-gate checks instead of building broken copy; action rewrites must pass Forge voice/message gates.

## 4. Verify after each wave

When a wave finishes:

For opted-in decks, first run the copy validator, including binding coverage and saved-master agreement. Check a restyle against the prior record for exact wording, and a rewrite for retained identity and the requested action. State POLISH invalidates managed approvals and sets `ready_to_ship=false`; leave approval to /gw-review with a fresh output snapshot per `copy-record.md`. No action or style reroll auto-ships or reuses approval of earlier outputs.

In-place rebuilds must use the assembler's render-and-verify-before-swap path
with a content-hash backup of the prior HTML. Do not bypass it with a direct
overwrite; this safety check does not replace the visual review below.

1. Render every produced carousel's slides to PNG, respecting the headless quirks documented in the `ig-carousel` skill's "Known traps" section (`--headless=new`, kill stray processes, unique `--user-data-dir`, `127.0.0.1`, fresh port, window sized to exact slide width).
2. LOOK at every cover image (Read the PNG files). Judge the cover FIRST and on one question: would it stop a coach's thumb in a feed full of workout clips? Layout-correct but flat goes back with a stronger treatment or better photo, same as a broken one.
3. Any dark or blank hero, clipped text, broken layout, or flat cover goes back for a fix in the next wave.
3b. Read the body photo slide as a PNG too. A missing body photo (any pack but Mono Series), text sitting on the photo's subject, or an empty spread slide goes back in the next wave.
4. Read the LAST slide and one body slide as text. If any pack meta leaked onto a slide (THE MESSAGE, PULLED FROM THE BRAIN, a cross-reference line, a bare source credit), the carousel goes back in the next wave and the pack gets flagged in the output; meta on a slide is a hard fail, not a style note.

Do not report done on trust. A file passing a portability or lint check can still render wrong.

## 5. Output

A summary table:

| Slug | Style pack | Hero photo | Body photo | Verified | Path |
|------|-----------|------------|------------|----------|------|

Plus the list of anything skipped and why.

## 6. Completion marker

At the end of EVERY run, including a nothing-waiting no-op, print exactly this on its own line so the scheduled-job validator can see it:

GW-DONE: carousel-batch
