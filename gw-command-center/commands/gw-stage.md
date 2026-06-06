---
description: Stage content pack assets to native draft surfaces (Kit for email, markdown fallback for X/IG/Substack until those platforms are wired)
---

# /gw-stage [content-pack-path] — Outbound Draft Router

Takes a content pack from `gw-content-forge` (or any pack with the same section structure) and routes each asset to its native draft surface for Scott to review and publish. **NEVER auto-publishes. Always draft state.**

## Examples

- `/gw-stage Deliverables\2026-06-05-deceleration\deceleration-content-pack.md`
- `/gw-stage Deliverables\2026-05-05-speed-work-without-dropping-lift-day\speed-work-without-dropping-lift-day-content-pack.md`

## HARD RULES

- **Never publish, never schedule.** Draft state only. Scott opens each platform, reviews, hits send.
- **Preserve voice verbatim.** Do NOT re-edit the content pack text. The forge already applied Scott's voice rules. Staging is dumb dispatch.
- **Don't commit.** Per the new pipeline pattern, `gw-daily-closeout` handles git. This skill writes files and logs only.
- **Fall back, never fail.** If a platform's credentials aren't wired yet, write a markdown fallback to `Deliverables\_pending-drafts\<platform>\` so Scott can copy-paste manually. Same end result, just slower.
- **Respect `gw-kit:kit-guardrails`.** The Kit MCP guardrails skill will auto-fire before any `mcp__af8cd12a-*` tool call and present a confirmation to Scott. Do NOT try to bypass it. If Scott rejects the draft, treat that as "skip Kit, write the Kit fallback markdown instead" — don't retry, don't argue, move on to the next section.

## Build status (2026-06-06)

| Platform | Status | Route |
|---|---|---|
| **Kit (email broadcasts)** | LIVE via Kit MCP | `mcp__af8cd12a-193d-42fc-a24f-fc6a6d27a1ec__create_broadcast` |
| **Buffer for X (threads)** | NOT WIRED | Markdown fallback at `Deliverables\_pending-drafts\x\` |
| **Buffer for IG (carousel captions)** | NOT WIRED | Markdown fallback at `Deliverables\_pending-drafts\ig\` |
| **Reel ideas** | Manual by design | Markdown fallback at `Deliverables\_pending-drafts\reels\` |
| **Substack** | NOT WIRED | Markdown fallback at `Deliverables\_pending-drafts\substack\` |

When a platform gets wired (Buffer/Substack), update this table and the corresponding step below — do not change the skill name or invocation.

## Steps

### 1. Validate input

`$1` is the content pack path (relative to repo root or absolute). Resolve to absolute path. Read the file. If the file does not exist, print the path and stop. Do NOT guess at alternative paths.

Capture:
- `pack_path` (absolute)
- `pack_basename` (filename without .md)
- `pack_topic_slug` (kebab-case from filename, strip the `-content-pack` suffix; e.g. `speed-work-without-dropping-lift-day-content-pack.md` → `speed-work-without-dropping-lift-day`)
- `pack_topic_title` (from the first H1 in the file, or the slug humanized)
- `today` (YYYY-MM-DD)

### 2. Parse sections

Find every H2 (`^## `) in the pack. Match against this lookup table. Each H2 captures everything from that header to the next H2 (or end of file). Trim trailing whitespace.

| H2 match pattern (case-insensitive) | Section kind |
|---|---|
| `email`, `leech letter`, `saturday` | `email` |
| `twitter thread`, `x thread`, `tweet` | `x_threads` |
| `instagram carousel`, `ig carousel`, `carousel` | `ig_carousels` |
| `reel idea`, `reel`, `short` | `reels` |
| `substack`, `long form`, `article` | `substack` |
| Anything else | skip with a note in the stage report |

Order does not matter. A pack may have any subset of these.

### 3. Generate a session_id

Generate a fresh UUID v4 once at the start of this run. Reuse it on every Kit MCP call in this run for analytics grouping. Do NOT derive it from the topic, date, or anything semantic — it must be random.

### 4. Dispatch each section

#### 4a. Email → Kit draft (LIVE)

If an `email` section was found:

1. **Extract subject:**
   - If the section body has a line matching `^Subject:\s*(.+)$`, use the captured value.
   - Else if there is an H3 immediately under the H2, use the H3 text.
   - Else use `pack_topic_title`.

2. **Extract preview_text (optional):**
   - If there is a line matching `^Preview:\s*(.+)$`, use it. Else omit.

3. **Render body to HTML:**
   - The email body is the section content after stripping the Subject/Preview lines.
   - Convert markdown to clean HTML inline. Rules:
     - `**bold**` → `<strong>bold</strong>`
     - `*italic*` → `<em>italic</em>`
     - `[text](url)` → `<a href="url">text</a>`
     - Blank line between paragraphs → wrap each paragraph in `<p>...</p>`
     - `- item` lists → `<ul><li>item</li></ul>`
     - `1. item` lists → `<ol><li>item</li></ol>`
     - Em-dashes are BANNED per Scott's voice rules. If you see one in the source, leave it — do not silently rewrite — but flag it in the stage report.
   - Do NOT add a signoff or "Keep the Fire Burning" — Scott's Kit template already includes it. Body is the body only.

4. **Call `mcp__af8cd12a-193d-42fc-a24f-fc6a6d27a1ec__create_broadcast`** with:
   - `subject` = extracted subject
   - `content` = rendered HTML body
   - `preview_text` = extracted preview (if any)
   - `description` = `"GW Stage: {pack_topic_slug} ({today})"` (Kit-internal, not visible to subscribers)
   - `user_goal` = `"draft_broadcast_email"`
   - `session_id` = the run's UUID
   - Do NOT pass `subscriber_filter` (default = all subscribers, which is what Scott wants for Leech Letters)
   - Do NOT pass `email_template_id` (use Kit account default)

5. **Capture the response:**
   - `confirm_url` — the Kit draft editor URL. Surface this to Scott in the stage report. This is the entire payoff — one click and Scott is in Kit's editor reviewing the draft.
   - Broadcast `id` and `subject` for the report.

6. **On MCP error** (auth expired, network, etc.):
   - Catch the error.
   - Write fallback markdown to `Deliverables\_pending-drafts\kit\{today}-{pack_topic_slug}.md` with the rendered subject, preview, and HTML body so Scott can paste it into Kit manually.
   - Record the error message in the stage report.
   - Do NOT crash the rest of the run — proceed to other sections.

#### 4b. X threads → Markdown fallback (NOT WIRED)

Write `Deliverables\_pending-drafts\x\{today}-{pack_topic_slug}-threads.md` with the verbatim section content. Header at top: `# X Threads — staged YYYY-MM-DD\n\nPaste each thread into Typefully / Buffer / X drafts manually until Buffer API is wired.\n\nSource pack: <pack_path>\n`. Then dump the section body unchanged.

#### 4c. IG carousels → Markdown fallback (NOT WIRED)

Write `Deliverables\_pending-drafts\ig\{today}-{pack_topic_slug}-carousels.md` with the verbatim section content. Header: `# IG Carousels — staged YYYY-MM-DD\n\nCarousel CAPTIONS only. Build visuals with /ig-carousel skill when ready. Until Buffer API is wired, drop captions into Later / Buffer / IG draft manually.\n\nSource pack: <pack_path>\n`.

#### 4d. Reel ideas → Markdown fallback (manual by design)

Write `Deliverables\_pending-drafts\reels\{today}-{pack_topic_slug}-reels.md` with the verbatim section content. Header: `# Reel Ideas — staged YYYY-MM-DD\n\nThese are CONCEPTS. Reels stay manual (Scott shoots and edits).\n\nSource pack: <pack_path>\n`. There is no platform wire for reel ideas and there will not be — they always end as Scott's notes.

#### 4e. Substack → Markdown fallback (NOT WIRED)

Write `Deliverables\_pending-drafts\substack\{today}-{pack_topic_slug}-substack.md` with verbatim section content. Header: `# Substack Article — staged YYYY-MM-DD\n\nUntil claude-in-chrome MCP wiring is built, open Substack manually, click New Post, paste body.\n\nSource pack: <pack_path>\n`.

### 5. Idempotency

If any fallback file already exists at the target path, append `-2`, `-3`, ... before the `.md` extension. Never overwrite. The Kit broadcast call itself is allowed to create duplicate drafts on re-run — Kit allows it and Scott can delete from the editor.

### 6. Write the stage report

`Deliverables\_pending-drafts\_stage-report-{today}-{pack_topic_slug}.md` (append `-2`, `-3` if it exists for the same pack same day).

Structure:

```markdown
---
title: "Stage Report — {pack_topic_title}"
type: stage-report
pack: {pack_path}
date: {today}
session_id: {uuid}
pipeline: gw-stage
---

# Stage Report — {pack_topic_title}

**Pack:** `{pack_path}`
**Run:** {YYYY-MM-DD HH:MM}

## Routed

### Email → Kit (LIVE)
- **Status:** drafted / fallback
- **Subject:** {subject}
- **Preview:** {preview_text or "(none)"}
- **Kit confirm URL:** <{confirm_url}>
- **Broadcast ID:** {id}

(If fallback: list the fallback path and the error message instead.)

### X Threads → Markdown fallback
- **Status:** {N threads staged | "(no section in pack)"}
- **Path:** `Deliverables\_pending-drafts\x\{file}.md`
- **TODO:** Buffer API not yet wired

### IG Carousels → Markdown fallback
- **Status:** ...
- **Path:** ...
- **TODO:** Buffer API not yet wired

### Reel Ideas → Markdown fallback
- **Status:** ...
- **Path:** ...
- **Note:** manual by design

### Substack → Markdown fallback
- **Status:** ...
- **Path:** ...
- **TODO:** claude-in-chrome MCP wiring not yet built

## Voice / safety notes
- Em-dash check: {found N / clean}
- Banned-words check: {found N / clean}  *(optional — flag if obvious. Do NOT rewrite. Scott decides.)*

## Source pack sections seen
- {list of H2 headers found, with `(routed: <kind>)` or `(skipped)` annotation}
```

### 7. Append to wiki log

```
{today} /gw-stage: {pack_topic_slug} (email: drafted|fallback|skip, x: N, ig: N, reels: N, substack: 0|1)
```

### 8. Do NOT commit

Per the new pipeline pattern (matching `gw-sc-research`), commits are batched by `gw-daily-closeout` via `scripts/git_safe_commit.py`. This skill's job ends at writing the stage report and the wiki/log.md line.

## Voice and tone (for the stage report only)

- Coach-direct. Short. No marketing fluff.
- The report is a receipt for Scott, not a press release.

## Integration with other skills

`gw-stage` is a downstream skill. The expected call chain:

1. Scott runs `/gw-content-forge [topic]` (or finishes editing a pack manually)
2. Scott runs `/gw-stage path/to/that-pack.md`
3. Scott opens the Kit confirm URL, reviews, hits send
4. Scott pastes the X/IG/Substack fallbacks into their platforms until those wires get built

`gw-stage` does NOT call `gw-content-forge` itself. It only routes existing packs.

## Notes

- **Always draft.** The Kit MCP `create_broadcast` is hard-coded to draft state. Even if a future version exposes a `published_at` field, this skill MUST NOT set it. Publishing is always Scott's click.
- **Kit auth.** If the Kit MCP returns an auth error, run `mcp__kit__authenticate` once, then re-run this skill. The fallback markdown is the safety net while you fix auth.
- **HTML for Kit.** Kit's `content` field expects HTML. Inline conversion is described above. If the email body is already HTML in the pack, pass it through unchanged.
- **Buffer wiring (future Phase 2).** When Buffer is wired, add a step 4b.i that calls the Buffer API for posts/drafts. Keep the markdown fallback as the auth-fail safety net.
- **Substack wiring (future Phase 4).** When claude-in-chrome MCP routes are added, step 4e gains an interactive browser drive. Keep markdown fallback.
- **No section found.** If the pack has no recognized H2 sections, write a stage report that just lists what was seen and says `no actionable sections`. Don't fail.
