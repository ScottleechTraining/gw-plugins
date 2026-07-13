---
name: gw-dewey-ingest
model: sonnet
description: "GW Dewey Ingest Pipeline (v3.1 - 3-Domain Classifier). Converts hand-curated Twitter/Instagram saves from the Dewey Google Sheet into richly tagged Obsidian notes in External Library/Twitter-Instagram Saves/. Classifies each row into s-and-c, business, ai, or skip. Never auto-promotes to wiki. Never writes in Scott's voice."
---

# GW Dewey Ingest Pipeline (v3.1 — 3-Domain Classifier)

Converts hand-curated Twitter/Instagram saves from the **Dewey Google Sheet** into richly tagged Obsidian notes inside `External Library/Twitter-Instagram Saves/`. One-way link to the wiki concept layer. Never auto-promotes. Never writes in Scott's voice.

## v3.1 update (2026-05-13): 3-Domain Classification

Every row must now be classified into ONE of these domains (added to frontmatter as `domain:`):

| Domain | What goes here |
|---|---|
| `s-and-c` | S&C coaching, football, weight room, athletic performance, contact prep, programming, recovery, periodization, mobility, speed, agility |
| `business` | Marketing, sales pages, email funnels, sponsorships, pricing, business operations, course launches, lead gen, copywriting, branding |
| `ai` | AI tools, prompts, Claude / GPT / Gemini, automation, agent design, MCP, no-code, AI-assisted content |
| `skip` | Off-topic, spam, duplicates, low quality, personal-only — no file written, just mark Processed |

Use post caption + author + media OCR to decide. When ambiguous between business and s-and-c, prefer business if the angle is positioning/marketing/selling; s-and-c if the angle is tactical coaching.

Also add new frontmatter field `gw_use` to be set by classifier:
- `research-citation` | `hook-bank` | `exercise-bank` | `competitor-intel` | `voice-corpus` | `business-framework` | `ai-pattern`

For business and ai domains, also write a one-line reference note to:
- `External Library/Twitter-Instagram Saves/_by-domain/business/YYYY-MM-DD-[author]-[id].md`
- `External Library/Twitter-Instagram Saves/_by-domain/ai/YYYY-MM-DD-[author]-[id].md`

These reference notes just contain a wikilink to the primary note + a one-line summary. Makes domain-specific browsing easy.

## Daily vs manual modes

- **Manual batch**: original `/gw-dewey-ingest` flow (this command). Run on a fresh batch by Scott.
- **Daily automated**: `/gw-dewey-daily` (sister command). Same logic but triggered by scheduled task, processes only rows newer than `.dewey-cursor.txt`.
- **One-time backfill**: `/gw-dewey-backfill` (sister command). Re-runs the 2,677-row backlog hunting for Business + AI saves missed on first S&C-focused pass.

**Project:** `C:/Claude Projects/Skills/tools/dewey_ingest/`
**Output:** `C:/Claude Projects/Gridiron Warrior/External Library/Twitter-Instagram Saves/`

---

## v3 Architecture: Dewey CDN is the source of truth

The Dewey sheet's **`Media`** column already contains a direct URL to the asset:

| Pattern | Tier | What we do |
|---|---|---|
| `https://static.getdewey.co/upload/<hash>.<ext>` | **Tier 1** | Plain HTTP GET from Dewey's public S3. Save image, embed `![[ ]]`, OCR via Read tool. Zero IG exposure. |
| Contains `cdninstagram.com` or `fbcdn.net` (`.mp4` etc) | **Tier 2** | Video. No download. Note `media_handling: video-skip`. |
| Empty | **Tier 0** | No media. Caption-only note. |
| Anything else | **Tier 0** | Refuse to fetch from unknown hosts. Caption-only. |

The helper's `list-unprocessed` returns each row with `media_url` and `media_kind` already classified (`dewey-cdn-image | video-url | none | other`). The slash command just dispatches.

**No gallery-dl, no Chrome juggling, no Instagram cookies, no rate-limit guardrails.** Those exist as legacy fallbacks in the helper but the default flow doesn't touch them.

---

## Hard Constraints

1. **Never write in Scott's voice.** External-source content gets neutral, descriptive prose. CLAUDE.md voice rules do NOT apply.
2. **Never edit any file inside `wiki/concepts/` or `wiki/entities/`.** Only `wiki/log.md` is touched, and it's append-only.
3. **Never auto-promote a save to a wiki concept page.** Genuinely-rich saves get one line in `External Library/_promotion-candidates.md` for Scott's weekly review.
4. **Only fetch from the Dewey CDN.** Never fetch directly from Instagram or unknown hosts. The helper enforces this.
5. **Videos never download.** Tier 2 is enforced by URL pattern in the helper.

---

## Run

```bash
source ~/.bashrc
python "C:/Claude Projects/Skills/tools/dewey_ingest/dewey_ingest.py" --help
```

No flags. No `--with-images`. The Media column is the only signal.

---

## Steps

### 1. Pull batch

```bash
python "C:/Claude Projects/Skills/tools/dewey_ingest/dewey_ingest.py" list-unprocessed
```

Parse JSON. Each row has: `row, url, caption, author, posted, source, notes, tags, media_url, media_kind`.

Report `Found N unprocessed rows. <count by media_kind>`. If 0, exit cleanly.

**Field-derivation notes (the sheet doesn't populate everything the skill needs):**

- **`source`** — the sheet does NOT have this column. Derive from the URL during note generation:
  - URL contains `instagram.com` → `source: instagram`, `type: ig-save`
  - URL contains `x.com` or `twitter.com` → `source: twitter`, `type: twitter-save`
- **`posted`** — sheet returns human format like `"10:21 PM, May 07, 2026"`. Normalize to `YYYY-MM-DD` for frontmatter (drop the time). If unparseable, write today's date and add a `_note: posted-date-unparseable` field to frontmatter.
- **Twitter media (`media_kind: other`)** — handled by step 3a routing to Tier 0 (caption-only). Twitter is text-first; captions carry the signal. The Tier 0 `## Media` line can mention the platform CDN URL is available at the post URL for visual reference.

### 2. Cache the wiki concept index

Read `C:/Claude Projects/Gridiron Warrior/wiki/index.md` once. Reuse for every row's `wiki_links`.

### 3. Per-row loop

For each row:

#### 3a. Dispatch on `media_kind`

- **`dewey-cdn-image`** → call helper, fetch image, OCR.
- **`video-url`** → Tier 2. No fetch.
- **`none` / `other`** → Tier 0. No fetch.

#### 3b. Tier 1 (image): fetch + OCR

```bash
python "C:/Claude Projects/Skills/tools/dewey_ingest/dewey_ingest.py" fetch-media-url "<media_url>" "<author>" "<post_id>"
```

The helper handles both single URLs and `;`-separated carousel URLs server-side. Pass the whole `media_url` value from the sheet — no bash splitting needed.

For carousels you'll get a JSON response with `files: [...]` and `files_relative: [...]` arrays. Read each file with the Read tool to OCR every slide, then write the OCR section as `**Slide N — short label:**` blocks. If the carousel is a numbered framework (#0/#1/#2 style), preserve the slide numbering verbatim from the images.

Branch on returned top-level `status`:
- `ok` → use the `Read` tool on each path in `files` (or the single `file` for non-carousel posts). Each image renders to your vision context. For each, write either the verbatim text or `No legible text on image. The image shows <one-sentence visual description>.` into `## Image Text (OCR)`. Carousel posts get one `**Slide N — label:**` block per image. Set `media_handling: image-ocr`. Mark row `success-with-image`.
- `partial` → some images fetched, some failed. Embed and OCR what we got; note in the OCR section which slide(s) didn't fetch (use `items[]` to identify). Still mark row `success-with-image`.
- `video` → Tier 2 (shouldn't happen since helper pre-classifies, but defensive).
- `empty` / `other` → fall through to Tier 0.
- `failed` → Tier 0 fallback. Mark `success-no-media` and log the error.

#### 3c. Tier 2 (video)

No fetch. `## Media` section reads:
```
Post: <URL>
*Video / reel — media not extracted. Open the post URL above to view.*
```
Set `media_handling: video-skip`. Mark row `success-video-skip`.

#### 3d. Tier 0 (no media)

No fetch. `## Media` section reads:
```
Post: <URL>
*No media on this post. Caption is the canonical content.*
```
Set `media_handling: caption-only`. Mark row `success-caption-only`.

#### 3e. Classify caption

Claude judgment:
- `content_type`: `exercise-list | framework | quote | data-chart | hook | testimonial | dm | sales-page`
- `topics`: 3-7 lowercase kebab-case tags
- `gw_use`: `film-study-fuel | hook-bank | exercise-bank | research-citation | competitor-intel`
- `audience`: `"HS football coach"` by default
- `quality`: `high | medium | skip` — see criteria below.

**Quality criteria (load-bearing — drives the output tier in 3h):**

- **`high`** = genuinely useful for Insiders / Course / Summit / Film Study / hook-bank. Includes:
  - Coaching ideas, frameworks, drills, programming, hooks an HS football / S&C coach could use
  - Posts from coaches Scott already knows or has hosted (Wildcat Webinar guests, podcast guests, Summit speakers — cross-reference `wiki/index.md` Entities and Summaries before tagging)
  - Posts from authoritative external S&C voices (Building The Elite, Fergus Connolly, Tony Holler, Mike Robertson, Cal Dietz, Joel Smith, etc.)
  - Marketing / business framework posts that directly apply to selling GW (sales copy structure, offer construction, hook patterns, email frameworks)
  - **Graphic design, AI tooling, or Claude/ChatGPT usage posts** — Scott runs the GW Design Studio and uses AI heavily for content production; tag these HIGH if they show a usable technique, MEDIUM if they're general commentary
  - Earns the full v3 schema with description, GW tie-in, and asset suggestions.
- **`medium`** = decent coaching-adjacent content OR off-topic-but-on-an-allowed-theme content. Worth indexing and searchable later, but not directly applicable to a GW asset right now. Captures the post; skips the deep analysis. Default for: general motivational posts from non-network creators, biomechanics/movement content not tied to football, and any graphic-design / AI / Claude post that doesn't deliver a usable technique.
- **`skip`** = promotional spam, off-topic, duplicate-of-existing-save, or non-coaching content with no transferable lesson. Sheet row marked `Processed`; **no markdown file is written**. Examples: NBA/sports memes with no S&C tie-in, pop-culture quotes without a coaching frame, generic startup tweets unrelated to coaching/marketing/AI.

**Pre-flight check before tagging:** scan the `author` field against `wiki/index.md`. If the author appears in any podcast, webinar, summit, or summary entry, the floor is HIGH unless the specific post caption is unambiguously off-topic. Coaches in Scott's network never get downgraded to MEDIUM by default.

When in doubt between two tiers, prefer the higher one. `medium` is cheap to write and easy to upgrade later; a skipped row is invisible until manually re-ingested.

#### 3f. Match wiki concepts

Pick max 4 genuinely overlapping concept pages from `wiki/index.md`. `[[concepts/page-name]]` format. Empty if nothing fits.

#### 3g. Find related saves

Grep `External Library/Twitter-Instagram Saves/*.md` for overlapping topics. List up to 3 as `[[other_postID]]`.

#### 3h. Write the note (branches by `quality`)

Path: `External Library/Twitter-Instagram Saves/[author]_[post_id].md`

**Quality branching (decide BEFORE writing anything):**

- **`skip`** → write NO file. Skip directly to step 3i (promotion check, which will also be a no-op) and step 3j (mark processed with `skip-low-quality`). Do not append the related-saves grep, do not write any markdown. The row is captured by the sheet only.
- **`medium`** → write a **lightweight note**: full frontmatter + `## Caption` + `## Media`. Omit `## Image Text (OCR)`, `## Description`, `## Why this matters for GW`, `## Could feed`, and `## Related saves`. (For Tier 1 medium rows, OCR text was already gathered in 3b — drop it; the image embed in `## Media` and the wiki backlinks in frontmatter carry the indexable signal.)
- **`high`** → write the **full v3 note** below.

**Full v3 note template (used only when `quality: high`):**

```markdown
---
type: ig-save | twitter-save
source: instagram | twitter
author: "[handle]"
post_url: "[URL]"
captured: YYYY-MM-DD
posted: YYYY-MM-DD
content_type: <classification>
topics: [tag1, tag2, tag3]
wiki_links: [[concepts/concept-1]], [[concepts/concept-2]]
gw_use: <classification>
audience: "HS football coach"
quality: high
media_handling: caption-only | image-ocr | video-skip
---

## Caption

<full caption, markdown-formatted, preserve line breaks>

## Media

<Tier 1 ok: ![[_media/[author]_[post_id]/<filename>]]
followed by "Post: <URL>">

<Tier 2: "Post: <URL>" + "*Video / reel — media not extracted...*">

<Tier 0: "Post: <URL>" + "*No media on this post...*">

## Image Text (OCR)

<Tier 1 only. Verbatim text Claude read from the image, OR "No legible text on image. The image shows <one-sentence description>."
Omit this section entirely for Tier 0 / Tier 2.>

## Description

<2-3 neutral sentences describing what the post is. Not in Scott's voice.>

## Why this matters for GW

<1 paragraph, neutral prose. Concrete tie-in to Insiders / DFY / Course / Summit / Film Study. Specific, not generic.>

## Could feed

- <specific GW asset 1>
- <specific GW asset 2>
- <specific GW asset 3>

## Related saves

- [[other_postID_1]] - one-line reason
- [[other_postID_2]] - one-line reason
```

**Lightweight note template (used only when `quality: medium`):**

```markdown
---
type: ig-save | twitter-save
source: instagram | twitter
author: "[handle]"
post_url: "[URL]"
captured: YYYY-MM-DD
posted: YYYY-MM-DD
content_type: <classification>
topics: [tag1, tag2, tag3]
wiki_links: [[concepts/concept-1]], [[concepts/concept-2]]
gw_use: <classification>
audience: "HS football coach"
quality: medium
media_handling: caption-only | image-ocr | video-skip
---

## Caption

<full caption, markdown-formatted, preserve line breaks>

## Media

<same as full template — Tier 1 embed, Tier 2 video note, or Tier 0 caption-only line>
```

**Step 3g (related saves grep) is skipped for `medium` and `skip`.** Only run it for `high`.

#### 3i. Promotion check

If genuinely warrants its own wiki concept page, append ONE line to `External Library/_promotion-candidates.md`:
```
- [[author_postID]] - YYYY-MM-DD - rationale (proposed: kebab-case-suggestion)
```
Default: do NOT promote.

#### 3j. Mark processed

```bash
python "C:/Claude Projects/Skills/tools/dewey_ingest/dewey_ingest.py" mark-processed <row> <status>
```

Status values:
- `success-caption-only` — Tier 0
- `success-with-image` — Tier 1 ok
- `success-no-media` — Tier 1 fell back
- `success-video-skip` — Tier 2
- `skip-low-quality` — quality: skip
- `fail-other` — unhandled failure

#### 3k. Append to wiki log

```
## [YYYY-MM-DD] ingest | dewey-ingest | [author/postID] | <content_type> | <gw_use> | tier-<N>
```

### 4. End-of-batch summary

Counts by tier and status. Promotion candidates flagged.

---

## Frontmatter spec (verbatim)

| Field | Allowed values |
|---|---|
| type | ig-save \| twitter-save |
| source | instagram \| twitter |
| author | string handle (no `@`) |
| post_url | full URL |
| captured | today's date in YYYY-MM-DD |
| posted | sheet's date column or gallery-dl metadata, YYYY-MM-DD |
| content_type | exercise-list \| framework \| quote \| data-chart \| hook \| testimonial \| dm \| sales-page |
| topics | 3-7 lowercase kebab-case tags |
| wiki_links | 0-4 `[[concepts/page]]` backlinks |
| gw_use | film-study-fuel \| hook-bank \| exercise-bank \| research-citation \| competitor-intel |
| audience | "HS football coach" by default |
| quality | high \| medium \| skip |
| media_handling | caption-only \| image-ocr \| video-skip |

---

## Legacy fallback (rare)

If the Dewey sheet's Media column is empty for a row that DOES have an image (e.g., a manual entry from Scott), and Scott explicitly wants the image, the legacy `download-image` subcommand still works (gallery-dl + Chrome cookies + guardrails). To use:

1. Close Chrome.
2. Set `DEWEY_CHROME_PROFILE` if needed.
3. Call `dewey_ingest.py download-image <post_url> <author> <post_id>` directly.

Not part of the default flow. Don't reach for it unless you specifically need to scrape IG for a row Dewey didn't capture.

---

## Troubleshooting

| Symptom | Fix |
|---|---|
| `media_kind: other` for a row | Media URL is from an unknown host. Investigate manually; helper refuses to fetch from non-Dewey hosts. |
| `fetch-media-url` returns `failed` | Dewey CDN occasional hiccup. Retry the row. |
| `gspread.exceptions.APIError: PERMISSION_DENIED` | Re-share the Dewey sheet with the service account email (Editor). |
| Note has wrong author/post_id | Sheet's `Tweet URL` column was wrong. Fix in sheet, clear `Processed`, re-run. |
